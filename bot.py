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
    asyncio.run(main())    paquete = data['paquete']; metodo = data['metodo']; user_id = update.effective_user.id
    precio = PRECIOS.get(paquete, {"usd": 0, "stars": 0})
    if metodo == "CryptoBot": await cobrar_cryptobot(update, context, paquete, precio, user_id)
    elif metodo == "Paypal": await cobrar_paypal(update, context, paquete, precio)

def crear_invoice_crypto(amount, description):
    headers = {"Crypto-Pay-API-Token": CRYPTOBOT_TOKEN}
    payload = {"asset": "USDT", "amount": str(amount), "description": description}
    r = requests.post(f"{CRYPTO_API}/createInvoice", headers=headers, json=payload)
    return r.json()["result"]

def revisar_invoice_crypto(invoice_id):
    headers = {"Crypto-Pay-API-Token": CRYPTOBOT_TOKEN}
    r = requests.get(f"{CRYPTO_API}/getInvoices?invoice_ids={invoice_id}", headers=headers)
    return r.json()["result"]["items"][0]

async def cobrar_cryptobot(update, context, paquete, precio, user_id):
    invoice = crear_invoice_crypto(precio['usd'], f"Acceso {paquete}")
    PENDIENTES[invoice["invoice_id"]] = {"user": user_id, "paquete": paquete}
    await update.message.reply_text(f"💎 **PAGO CON CRYPTOBOT USDT**\n\nPaquete: **{paquete}**\nMonto: **${precio['usd']} USDT**\n\nPaga aquí: {invoice['pay_url']}\n\nAl pagar se genera tu link de 1 solo uso automático.", parse_mode="Markdown")
    asyncio.create_task(revisar_pago(invoice["invoice_id"], context))

async def revisar_pago(invoice_id, context):
    while True:
        await asyncio.sleep(5)
        invoice = revisar_invoice_crypto(invoice_id)
        if invoice["status"] == "paid":
            data = PENDIENTES.pop(invoice_id, None)
            if data: await generar_link(context, data["user"], data["paquete"])
            break

async def cobrar_paypal(update, context, paquete, precio):
    await update.message.reply_text(f"💙 **PAGO CON PAYPAL**\n\nPaquete: **{paquete}**\nMonto: **${precio['usd']} USD**\n\n1. Envía a: {PAYPAL_LINK}\n2. Manda comprobante a {SOPORTE}", parse_mode="Markdown")

async def generar_link(context, user_id, paquete):
    bot = context.bot
    if paquete == "VIP 3: PERSONALIZADO 👑":
        await bot.send_message(user_id, f"✅ **PAGO CONFIRMADO**\n\nEscribe a {SOPORTE} con tu petición para el grupo personalizado 👑")
        return
    chat_id = GRUPOS.get(paquete)
    invite = await bot.create_chat_invite_link(chat_id=chat_id, member_limit=1)
    await bot.send_message(user_id, f"✅ **PAGO CONFIRMADO**\n\nTu acceso a **{paquete}**:\n`{invite.invite_link}`\n\n⚠️ Link de 1 SOLO USO", parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data))
    print("Bot iniciado en Railway...")
    app.run_polling()

if __name__ == "__main__":
    main()
