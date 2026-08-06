from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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

✅ Payment Complete hone ke baad

Payment Screenshot ya UTR sambhal kar rakhein.

Verification ke baad aapko Private Channel ka access diya jayega.

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
