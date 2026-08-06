from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ==============================
# SIRF IN 3 LINES KO BHARNA HAI
# ==============================

BOT_TOKEN = "8988935332:AAHh3ruhx36wMFzAsDuiwbsTsnxLO8QbcCM"

UPI_ID = "pinelabs.stq4616807@pineaxis"

PAYEE_NAME = "R.s Treding Co"

# ==============================


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    upi_link = (
        f"upi://pay?"
        f"pa={UPI_ID}"
        f"&pn={PAYEE_NAME}"
        f"&am=20"
        f"&cu=INR"
        f"&tn=Premium%20Video"
    )
keyboard = [
    [
        InlineKeyboardButton(
            text="💳 Pay ₹20",
            url=upi_link
        )
    ]
]
    
    message = """
🎬 Welcome

Premium Video dekhne ke liye pehle ₹20 payment karein.

👇 Neeche diye gaye button par click karke payment karein.

━━━━━━━━━━━━━━━━━━━━━━

✅ Payment Complete hone ke baad

Payment Screenshot ya UTR sambhal kar rakhein.

Verification ke baad aapko Private Channel ka access diya jayega.

Thank You ❤️
"""

    await update.message.reply_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot Started Successfully...")

    app.run_polling()


if __name__ == "__main__":
    main()
