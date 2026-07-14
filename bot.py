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
        [InlineKeyboardButton(text="🚀 ABRIR TIENDA VIP", web_app=WebAppInfo(url="https://cute-guys-bot.vercel.app"))]
    ])
    await message.answer(
        "✨ *BIENVENIDO A CUTE GUYS SUBSCRIPTIONS* ✨\n\n"
        "👑 El acceso VIP más exclusivo de Telegram\n"
        "⚡ Entrega inmediata después del pago\n"
        "🎁 Incluye 2 grupos gratis\n"
        "Elige tu plan aquí abajo:",
        reply_markup=keyboard, parse_mode="Markdown"
    )

@dp.message(F.web_app_data)
async def webapp_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    plan_id = data["plan_id"]
    dias = int(data["dias"])
    total_usd = int(data["total_usd"])
    total_stars = int(data["total_stars"])
    metodo = data["metodo"]
    
    plan = VIP[plan_id]
    dur_text = "♾️ Permanente" if dias==9999 else f"{dias} días"
    
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
        await message.answer(f"✅ *PEDIDO RECIBIDO*\n\n**Plan:** {plan['nombre']}\n**Duración:** {dur_text}\n**Total:** ${total_usd} USD\n\nPaga aquí: {invoice}", parse_mode="Markdown")
    elif metodo == "Paypal":
        await message.answer(f"✅ *PEDIDO RECIBIDO*\n\n**Plan:** {plan['nombre']}\n**Duración:** {dur_text}\n**Total:** ${total_usd} USD\n\n💰 Paga por Paypal a: {PAYPAL_USER}\nLink: {PAYPAL_LINK}\n\nMándame el comprobante aquí para activar ⚡")
    elif metodo == "Stripe":
        await message.answer(f"✅ *PEDIDO RECIBIDO*\n\n**Plan:** {plan['nombre']}\n**Duración:** {dur_text}\n**Total:** ${total_usd} USD\n\n💳 Toca CryptoBot y elige pagar con tarjeta. Stripe procesa y te llega USDT.")

async def main():
    print("Bot iniciado...")
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
