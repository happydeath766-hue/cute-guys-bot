import os
import json
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram import F
from aiocryptopay import AioCryptoPay, Networks
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")
PAYPAL_LINK = "https://www.paypal.me/Worldtwinks" # CAMBIA ESTO
PAYPAL_USER = "@Worldtwinks" # CAMBIA ESTO
SOPORTE_LINK = "https://telegram.me/CuteGuyspg"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
crypto = AioCryptoPay(token=CRYPTOBOT_TOKEN, network=Networks.MAIN_NET)
VIP = {
"prohibido": {"nombre": "Prohibido", "usd": 15, "stars": 800},
"twinks": {"nombre": "Twinks", "usd": 15, "stars": 800},
"adultos": {"nombre": "Adultos", "usd": 10, "stars": 500},
"personalizado": {"nombre": "Personalizado", "usd": 70, "stars": 3500},
"twinks_prohibido": {"nombre": "Twinks + Prohibido", "usd": 27, "stars": 1600},
"twinks_adultos": {"nombre": "Twinks + Adultos", "usd": 17, "stars": 1100},
"prohibido_adultos": {"nombre": "Prohibido + Adultos", "usd": 15, "stars": 1100},
"personalizado_otro": {"nombre": "Personalizado + Otro", "usd": 80, "stars": 3800},
"todos": {"nombre": "Todos 🔥", "usd": 100, "stars": 4800}
}

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔥 COMPRAR VIP", web_app=WebAppInfo(url="https://happydeath766-hue.github.io/cute-guys-bot/"))],
    [InlineKeyboardButton(text="💬 Soporte", url="https://t.me/CuteGuyspg")]
])
    await message.answer(
        "✨ *BIENVENIDO A CUTE GUYS SUBSCRIPTIONS* ✨\n\n"
        "👑 *El acceso VIP más exclusivo de Telegram*\n\n"
        "🎁 Incluye acceso a 2 grupos gratis\n"
        "⚡ *Entrega inmediata* después de confirmar tu pago\n"
        "🔒 Pagos seguros: Paypal, Crypto, Stars, Tarjeta\n"
        "Selecciona tu plan VIP aquí abajo:",
        reply_markup=keyboard, parse_mode="Markdown"
    )

@dp.message(F.content_type == "web_app_data") # ESTA ERA LA FALLA CLAVE
async def webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        logging.info(f"Datos recibidos: {data}")

        plan_id = data["plan_id"]
        dias = int(data["dias"])
        total_usd = int(data["total_usd"])
        total_stars = int(data["total_stars"])
        descuento = int(data["descuento"])
        metodo = data["metodo"]

        plan = VIP[plan_id]
        dur_text = "♾️ Permanente" if dias==9999 else f"{dias} días"
        desc_text = f"\n**Descuento:** -{descuento}%" if descuento>0 else ""

        if metodo == "Stars":
            await bot.send_invoice(
                chat_id=message.from_user.id, title=f"{plan['nombre']} - {dur_text}",
                description=f"Acceso VIP {dur_text}. Entrega inmediata ⚡",
                payload=f"vip_{plan_id}_{dias}_{message.from_user.id}", provider_token="", currency="XTR",
                prices=[LabeledPrice(label=f"{plan['nombre']} {dur_text}", amount=total_stars)]
            )
        elif metodo == "CryptoBot":
            invoice = await bot.create_invoice_link(
                title=f"{plan['nombre']} - {dur_text}", description=f"Acceso VIP {dur_text}. Entrega inmediata ⚡",
                payload=f"vip_{plan_id}_{dias}_{message.from_user.id}", provider_token=CRYPTOBOT_TOKEN, currency="USDT",
                prices=[LabeledPrice(label=f"{plan['nombre']} {dur_text}", amount=total_usd*100)]
            )
            await message.answer(f"✅ *PEDIDO RECIBIDO*\n\n**Plan:** {plan['nombre']}\n**Duración:** {dur_text}{desc_text}\n**Total:** ${total_usd} USD\nPaga aquí: {invoice}", parse_mode="Markdown")
        elif metodo == "Paypal":
            await message.answer(f"✅ *PEDIDO RECIBIDO*\n\n**Plan:** {plan['nombre']}\n**Duración:** {dur_text}{desc_text}\n**Total:** ${total_usd} USD\n💰 *Paga por Paypal a:* {PAYPAL_USER}\nLink: {PAYPAL_LINK}\n\nMándame el comprobante aquí para activar ⚡")
        elif metodo == "Stripe":
            await message.answer(f"✅ *PEDIDO RECIBIDO*\n\n**Plan:** {plan['nombre']}\n**Duración:** {dur_text}{desc_text}\n**Total:** ${total_usd} USD\n💳 *Paga con tarjeta:* Toca CryptoBot > Pagar con Tarjeta. Stripe procesa y recibo USDT.")

    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("❌ Hubo un error procesando tu pago. Habla con soporte.")
import json

@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        print(f"📦 DATOS RECIBIDOS: {data}")
        
        metodo = data.get("metodo")
        plan_id = data.get("plan_id")
        precio = float(data.get("precio"))
        
        if metodo == "CryptoBot":
            invoice = await crypto.create_invoice(
                asset="USDT", 
                amount=precio,
                description=f"Plan {plan_id} - CuteGuys"
            )
            await message.answer(f"💎 Paga aquí con CryptoBot:\n{invoice.pay_url}")
        
        elif metodo == "Paypal":
            await message.answer(f"✅ Recibí Paypal\nPlan: {plan_id}\nPrecio: ${precio} USD")
            
    except Exception as e:
        print(f"Error: {e}")
        await message.answer("❌ Error creando factura")
    except Exception as e:
        print(f"Error: {e}")
async def main():
    print("Bot iniciado...")
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
