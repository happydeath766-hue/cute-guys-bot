import os
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram import F

BOT_TOKEN = os.getenv("BOT_TOKEN")
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# TUS PLANES 2X2 + SUSCRIPCIONES
PAQUETES = {
    "1mes": {"nombre": "1 Mes VIP", "precio_usd": 5, "precio_stars": 500, "dias": 30},
    "2meses": {"nombre": "2 Meses VIP", "precio_usd": 9, "precio_stars": 900, "dias": 60},
    "3meses": {"nombre": "3 Meses VIP", "precio_usd": 12, "precio_stars": 1200, "dias": 90},
    "6meses": {"nombre": "6 Meses VIP", "precio_usd": 20, "precio_stars": 2000, "dias": 180},
    "anual": {"nombre": "Anual VIP", "precio_usd": 35, "precio_stars": 3500, "dias": 365},
    "perma": {"nombre": "Permanente VIP", "precio_usd": 60, "precio_stars": 6000, "dias": 9999}
}

# LINKS DE TUS 2 GRUPOS GRATIS - CAMBIALOS
GRUPO1 = "https://t.me/+TU_LINK_GRUPO1"
GRUPO2 = "https://t.me/+TU_LINK_GRUPO2"

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 ABRIR TIENDA VIP 👑", web_app=WebAppInfo(url="https://cute-guys-bot.vercel.app"))]
    ])
    await message.answer(
        "✨ *BIENVENIDO A CUTE GUYS VIP* ✨\n\n"
        "Elige tu acceso VIP aquí abajo. Incluye 2 grupos gratis 👇",
        reply_markup=keyboard, 
        parse_mode="Markdown"
    )

@dp.message(F.web_app_data)
async def webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        paquete_id = data.get("plan_id")
        metodo = data.get("metodo")
        
        if paquete_id not in PAQUETES:
            await message.answer("❌ Plan no válido")
            return
            
        paquete = PAQUETES[paquete_id]
        
        # Si paga con Stars
        if metodo == "Stars":
            await bot.send_invoice(
                chat_id=message.from_user.id,
                title=paquete["nombre"],
                description=f"Acceso VIP por {paquete['dias']} días",
                payload=f"vip_stars_{paquete_id}_{message.from_user.id}",
                provider_token="",
                currency="XTR",
                prices=[types.LabeledPrice(label=paquete["nombre"], amount=paquete["precio_stars"])]
            )
        # Si paga con CryptoBot
        elif metodo == "CryptoBot":
            invoice = await bot.create_invoice_link(
                title=paquete["nombre"],
                description=f"Acceso VIP por {paquete['dias']} días",
                payload=f"vip_crypto_{paquete_id}_{message.from_user.id}",
                provider_token=CRYPTOBOT_TOKEN,
                currency="USDT",
                prices=[types.LabeledPrice(label=paquete["nombre"], amount=paquete["precio_usd"]*100)]
            )
            await message.answer(
                f"✅ *PEDIDO RECIBIDO*\n\n"
                f"**Plan:** {paquete['nombre']}\n"
                f"**Precio:** ${paquete['precio_usd']} USD\n"
                f"**Método:** {metodo}\n\n"
                f"Paga aquí: {invoice}", 
                parse_mode="Markdown"
            )
        else:
            # Para Paypal y Stripe
            await message.answer(
                f"✅ *PEDIDO RECIBIDO*\n\n"
                f"**Plan:** {paquete['nombre']}\n"
                f"**Precio:** ${paquete['precio_usd']} USD\n"
                f"**Método:** {metodo}\n\n"
                f"Ahora te envío los datos para pagar por {metodo} al privado."
            )
            
    except Exception as e:
        await message.answer(f"Error: {e}")

async def main():
    print("Bot iniciado en Railway...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
