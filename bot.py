import os
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, LabeledPrice
from aiogram import F

BOT_TOKEN = os.getenv("BOT_TOKEN")
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")
PAYPAL_LINK = "https://www.paypal.me/Worldtwinks" # CAMBIA ESTO
PAYPAL_USER = "@Worldtwinks" # CAMBIA ESTO

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

PAQUETES = {
"prohibido": {"nombre": "Prohibido", "usd": 15, "stars": 800, "dias": 30},
"twinks": {"nombre": "Twinks", "usd": 15, "stars": 800, "dias": 30},
"adultos": {"nombre": "Adultos", "usd": 10, "stars": 500, "dias": 30},
"personalizado": {"nombre": "Personalizado", "usd": 70, "stars": 3500, "dias": 30},
"twinks_prohibido": {"nombre": "Twinks + Prohibido", "usd": 27, "stars": 1600, "dias": 30},
"twinks_adultos": {"nombre": "Twinks + Adultos", "usd": 17, "stars": 1100, "dias": 30},
"prohibido_adultos": {"nombre": "Prohibido + Adultos", "usd": 15, "stars": 1100, "dias": 30},
"personalizado_otro": {"nombre": "Personalizado + Otro", "usd": 80, "stars": 3800, "dias": 30},
"todos": {"nombre": "Todos 🔥", "usd": 100, "stars": 4800, "dias": 30},
"twinks_anual": {"nombre": "Twinks Anual", "usd": 30, "stars": 3000, "dias": 365},
"twinks_perma": {"nombre": "Twinks Permanente", "usd": 60, "stars": 6000, "dias": 9999},
"prohibido_anual": {"nombre": "Prohibido Anual", "usd": 40, "stars": 4000, "dias": 365},
"prohibido_perma": {"nombre": "Prohibido Permanente", "usd": 80, "stars": 8000, "dias": 9999},
"adultos_anual": {"nombre": "Adultos Anual", "usd": 15, "stars": 1500, "dias": 365},
"adultos_perma": {"nombre": "Adultos Permanente", "usd": 30, "stars": 3000, "dias": 9999}
}

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 ABRIR TIENDA VIP 👑", web_app=WebAppInfo(url="https://cute-guys-bot.vercel.app"))]
    ])
    await message.answer("✨ *BIENVENIDO A CUTE GUYS VIP* ✨\n\nElige tu acceso VIP aquí abajo:", reply_markup=keyboard, parse_mode="Markdown")

@dp.message(F.web_app_data)
async def webapp_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    plan_id = data.get("plan_id")
    metodo = data.get("metodo")
    
    if plan_id not in PAQUETES:
        await message.answer("❌ Plan no válido")
        return
        
    plan = PAQUETES[plan_id]
    
    if metodo == "Stars":
        await bot.send_invoice(
            chat_id=message.from_user.id, title=plan["nombre"], description=f"Acceso VIP {plan['dias']} días",
            payload=f"vip_{plan_id}_{message.from_user.id}", provider_token="", currency="XTR",
            prices=[LabeledPrice(label=plan["nombre"], amount=plan["stars"])]
        )
    elif metodo == "CryptoBot":
        invoice = await bot.create_invoice_link(
            title=plan["nombre"], description=f"Acceso VIP {plan['dias']} días",
            payload=f"vip_{plan_id}_{message.from_user.id}", provider_token=CRYPTOBOT_TOKEN, currency="USDT",
            prices=[LabeledPrice(label=plan["nombre"], amount=plan["usd"]*100)]
        )
        await message.answer(f"✅ *PEDIDO: {plan['nombre']}*\n**${plan['usd']} USD**\n\nPaga aquí: {invoice}", parse_mode="Markdown")
    elif metodo == "Paypal":
        await message.answer(f"✅ *PEDIDO: {plan['nombre']}*\n**${plan['usd']} USD**\n\n💰 Paga por Paypal a: {PAYPAL_USER}\nLink: {PAYPAL_LINK}\n\nMándame el comprobante aquí.")
    elif metodo == "Stripe":
        await message.answer(f"✅ *PEDIDO: {plan['nombre']}*\n**${plan['usd']} USD**\n\n💳 Para pagar con tarjeta usa CryptoBot > Pagar con Stripe.\nStripe procesa y CryptoBot me paga en USDT.")

async def main():
    print("Bot iniciado...")
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
