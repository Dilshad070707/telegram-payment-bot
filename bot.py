from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ==========================
# SIRF TOKEN BHARNA HAI
# ==========================
BOT_TOKEN = "8988935332:AAHh3ruhx36wMFzAsDuiwbsTsnxLO8QbcCM"

UPI_ID = "pinelabs.stq4616807@pineaxis"
PAYEE_NAME = "R.s Treding Co"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = f"""
🎬 Welcome

Satlaj Movie Download Karne Ke Liye ₹20 Payment Karein.

━━━━━━━━━━━━━━━━━━━━━━

💳 UPI ID:
{UPI_ID}

👤 Name:
{PAYEE_NAME}

💰 Amount:
₹20

━━━━━━━━━━━━━━━━━━━━━━

✅ QR Code Scan Karke Payment Karein.

📸 Payment Karne Ke Baad **Isi Bot Me** Apna Payment Screenshot Ya UTR Number Bheje.

⏳ Screenshot Verify Hone Ke Baad Aapko **Private Channel Ka Join Link Isi Bot Me** Bhej Diya Jayega.

❌ Screenshot Ya UTR Bheje Bina Channel Access Nahi Diya Jayega.

Thank You ❤️
"""
    with open("qr.png", "rb") as qr:
        await update.message.reply_photo(
            photo=qr,
            caption=message
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot Started Successfully...")

    app.run_polling()


if __name__ == "__main__":
    main()
