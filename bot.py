import asyncio
import json
import logging
import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")
CRYPTO_API = "https://pay.crypt.bot/api"
PAYPAL_LINK = "https://www.paypal.me/Worldtwinks"
SOPORTE = "@CuteGuyspg"
TIENDA_URL = "https://voluble-kashata-c29f0e.netlify.app/"

GRUPOS = {
    "VIP 1: TWINKS 🔥": -1004397334185,
    "VIP 2: MAYORES 🔥": -1004330286876,
}

PRECIOS = {
    "VIP 1: TWINKS 🔥": {"usd": 15, "stars": 800},
    "VIP 2: MAYORES 🔥": {"usd": 10, "stars": 500},
    "VIP 3: PERSONALIZADO 👑": {"usd": 70, "stars": 3500},
}

PENDIENTES = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🛒 ABRIR TIENDA VIP", web_app=WebAppInfo(url=TIENDA_URL))]]
    await update.message.reply_text("✨ **BIENVENIDO A CUTE GUYS VIP** ✨\n\nToca el botón para ver todos los paquetes +18\nPagos: Stars, CryptoBot, Paypal, Tarjeta\nTodos los links son de 1 SOLO USO 🔒", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.message.web_app_data.data)
    paquete = data['paquete']; metodo = data['metodo']; user_id = update.effective_user.id
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
    main()        paquete = data['paquete']; metodo = data['metodo']; user_id = update.effective_user.id
        precio = PRECIOS.get(paquete, {"usd": 0, "stars": 0})
        if metodo == "CryptoBot": await cobrar_cryptobot(update, context, paquete, precio, user_id)
        elif metodo == "Paypal": await cobrar_paypal(update, context, paquete, precio)

    async def cobrar_cryptobot(update, context, paquete, precio, user_id):
        invoice = await crypto.create_invoice(asset="USDT", amount=precio['usd'], description=f"Acceso {paquete}")
        PENDIENTES[invoice.invoice_id] = {"user": user_id, "paquete": paquete}
        await update.message.reply_text(f"💎 **PAGO CON CRYPTOBOT USDT**\n\nPaquete: **{paquete}**\nMonto: **${precio['usd']} USDT**\n\nPaga aquí: {invoice.pay_url}\n\nAl pagar se genera tu link de 1 solo uso automático.", parse_mode="Markdown")
        asyncio.create_task(revisar_pago(invoice.invoice_id, context))

    async def revisar_pago(invoice_id, context):
        while True:
            await asyncio.sleep(5)
            invoice = await crypto.get_invoices(invoice_ids=[invoice_id])
            if invoice and invoice[0].status == "paid":
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
