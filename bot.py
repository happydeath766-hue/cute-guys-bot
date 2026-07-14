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

PAQUETES = {
    "basico": {"nombre": "VIP Básico 1 Semana", "precio": 5, "dias": 7},
    "premium": {"nombre": "VIP Premium 1 Mes", "precio": 15, "dias": 30},
    "vip": {"nombre": "VIP Ultra 3 Meses", "precio": 35, "dias": 90}
}

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 ABRIR TIENDA VIP", web_app=WebAppInfo(url="https://cute-guys-store.vercel.app"))]
    ])
    await message.answer("✨ *BIENVENIDO A CUTE GUYS VIP* ✨\n\nElige tu acceso VIP aquí abajo:", reply_markup=keyboard, parse_mode="Markdown")

@dp.message(F.web_app_data)
async def webapp_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    paquete_id = data.get("paquete")
    
    if paquete_id not in PAQUETES:
        await message.answer("Paquete no válido")
        return
        
    paquete = PAQUETES[paquete_id]
    
    invoice = await bot.create_invoice_link(
        title=paquete["nombre"],
        description=f"Acceso VIP por {paquete['dias']} días",
        payload=f"vip_{paquete_id}_{message.from_user.id}",
        provider_token=CRYPTOBOT_TOKEN,
        currency="USDT",
        prices=[types.LabeledPrice(label=paquete["nombre"], amount=paquete["precio"]*100)]
    )
    
    await message.answer(f"Para activar *{paquete['nombre']}* paga aquí:\n\n{invoice}", parse_mode="Markdown")

async def main():
    print("Bot iniciado en Railway...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
