import os
import json
from datetime import datetime
from typing import Dict, Any

from telegram import Update, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ==========================================
# CONFIGURATION VARIABLES
# Replace these with your actual values
# ==========================================
BOT_TOKEN = "8988935332:AAHh3ruhx36wMFzAsDuiwbsTsnxLO8QbcCM"  # Replace with your actual bot token from BotFather
ADMIN_ID = 8197511283  # Replace with your actual numeric Telegram User ID
CHANNEL_INVITE_LINK = "https://t.me/+ZsnmUsE4i3JlM2I9"

# Payment Details
UPI_ID = "pinelabs.stq4616807@pineaxis"
PAYEE_NAME = "R.s Treding Co"
AMOUNT = "₹20"
QR_IMAGE_PATH = "qr.png" # Make sure this file exists in the same directory as the script

# File to store pending users
PENDING_USERS_FILE = "pending_users.json"

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def load_pending_users() -> Dict[str, Any]:
    """Loads pending users from the JSON file."""
    if not os.path.exists(PENDING_USERS_FILE):
        return {}
    try:
        with open(PENDING_USERS_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {PENDING_USERS_FILE}: {e}")
        return {}

def save_pending_users(users: Dict[str, Any]):
    """Saves pending users to the JSON file."""
    try:
        with open(PENDING_USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        print(f"Error saving {PENDING_USERS_FILE}: {e}")

# ==========================================
# BOT HANDLERS
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command. Sends payment details and QR code."""
    chat_id = update.effective_chat.id
    
    # Message to send to the user
    payment_message = (
        f"<b>Payment Details</b>\n\n"
        f"<b>UPI ID:</b> <code>{UPI_ID}</code>\n"
        f"<b>Payee Name:</b> {PAYEE_NAME}\n"
        f"<b>Amount:</b> {AMOUNT}\n\n"
        f"<i>Please make the payment using the QR code or UPI ID above.</i>\n"
        f"<i>After successful payment, send the <b>Payment Screenshot</b> or <b>UTR number</b> here.</i>"
    )

    try:
        # Check if QR image exists
        if os.path.exists(QR_IMAGE_PATH):
            with open(QR_IMAGE_PATH, 'rb') as photo:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=payment_message,
                    parse_mode='HTML'
                )
        else:
            # Fallback if QR image is missing, send just the text
            await context.bot.send_message(
                chat_id=chat_id,
                text=payment_message + "\n\n(QR code image not found on server.)",
                parse_mode='HTML'
            )
    except Exception as e:
        print(f"Error sending start message: {e}")
        await update.message.reply_text("An error occurred while sending payment details.")

async def handle_payment_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming messages (screenshots or text/UTR) from users."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Ignore messages from the admin intended for approval/rejection commands
    if chat_id == ADMIN_ID and update.message.text and update.message.text.startswith('/'):
        return

    # Extract user details
    user_id_str = str(user.id)
    username = f"@{user.username}" if user.username else "No username"
    first_name = user.first_name
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Load pending users, add the new one, and save
    pending_users = load_pending_users()
    pending_users[user_id_str] = {
        "username": username,
        "first_name": first_name,
        "date_time": current_time
    }
    save_pending_users(pending_users)

    # Prepare message for the Admin
    admin_message = (
        f"🚨 <b>New Payment Request</b> 🚨\n\n"
        f"<b>User ID:</b> <code>{user.id}</code>\n"
        f"<b>Name:</b> {first_name}\n"
        f"<b>Username:</b> {username}\n"
        f"<b>Time:</b> {current_time}\n\n"
        f"<b>Reply using:</b>\n"
        f"<code>/approve {user.id}</code>\n"
        f"or\n"
        f"<code>/reject {user.id}</code>"
    )

    try:
        # Forward the proof to the Admin
        if update.message.photo:
            # If user sent a photo
            photo_file_id = update.message.photo[-1].file_id
            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=photo_file_id,
                caption=admin_message,
                parse_mode='HTML'
            )
        elif update.message.text:
             # If user sent text (e.g., UTR)
             await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"{admin_message}\n\n<b>User's Message (UTR):</b>\n{update.message.text}",
                parse_mode='HTML'
            )
        else:
             # Handle other types of documents if needed, falling back to basic text
             await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"{admin_message}\n\n<b>User sent a non-text/photo message.</b>",
                parse_mode='HTML'
            )

        # Acknowledge the user
        await update.message.reply_text(
            "Payment proof received successfully.\n"
            "Please wait while we verify your payment."
        )
    except Exception as e:
        print(f"Error handling payment proof: {e}")
        await update.message.reply_text("There was an error processing your request. Please try again later.")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /approve command (Admin only)."""
    user_id = update.effective_user.id
    
    # Check if the user is the admin
    if user_id != ADMIN_ID:
         await update.message.reply_text("You are not authorized to use this command.")
         return

    # Check for correct arguments
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("Usage: /approve <user_id>")
        return

    target_user_id_str = context.args[0]
    
    # Load and check pending users
    pending_users = load_pending_users()
    if target_user_id_str not in pending_users:
         await update.message.reply_text(f"User ID {target_user_id_str} is not in the pending list.")
         return

    try:
        # Send approval message to the user with an inline button for the channel link
        keyboard = [
            [InlineKeyboardButton("Join Private Channel", url=CHANNEL_INVITE_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=int(target_user_id_str),
            text=(
                "✅ <b>Payment Verified Successfully.</b>\n\n"
                "Click below to join our Private Channel."
            ),
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

        # Remove user from pending list and save
        del pending_users[target_user_id_str]
        save_pending_users(pending_users)

        # Confirm to admin
        await update.message.reply_text(f"Successfully approved User ID: {target_user_id_str}")

    except Exception as e:
        print(f"Error approving user {target_user_id_str}: {e}")
        await update.message.reply_text(f"Failed to send message to user {target_user_id_str}. They might have blocked the bot.")

async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /reject command (Admin only)."""
    user_id = update.effective_user.id
    
    # Check if the user is the admin
    if user_id != ADMIN_ID:
         await update.message.reply_text("You are not authorized to use this command.")
         return

    # Check for correct arguments
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("Usage: /reject <user_id>")
        return

    target_user_id_str = context.args[0]
    
    # It might be good to allow rejection even if not in the list, 
    # just in case, but based on requirements, let's keep it tied to the pending list for cleanliness.
    # However, sometimes an admin might want to reject an old request.
    pending_users = load_pending_users()

    try:
        # Send rejection message to the user
        await context.bot.send_message(
            chat_id=int(target_user_id_str),
            text=(
                "❌ <b>Your payment could not be verified.</b>\n\n"
                "Please send a valid screenshot or UTR."
            ),
            parse_mode='HTML'
        )

        # Optionally remove from pending list upon rejection
        if target_user_id_str in pending_users:
            del pending_users[target_user_id_str]
            save_pending_users(pending_users)

        # Confirm to admin
        await update.message.reply_text(f"Successfully rejected User ID: {target_user_id_str}")

    except Exception as e:
        print(f"Error rejecting user {target_user_id_str}: {e}")
        await update.message.reply_text(f"Failed to send message to user {target_user_id_str}.")

def main():
    """Sets up and runs the Telegram Bot."""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or ADMIN_ID == 123456789:
        print("CRITICAL: Please set your BOT_TOKEN and ADMIN_ID in the configuration variables before running.")
        return

    # Create the application
    application = Application.builder().token(BOT_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("approve", approve))
    application.add_handler(CommandHandler("reject", reject))

    # Message Handler for payment proofs (captures photos and text messages that aren't commands)
    # filters.PHOTO handles screenshots, filters.TEXT & ~filters.COMMAND handles UTR text
    application.add_handler(MessageHandler(
        (filters.PHOTO | filters.TEXT) & ~filters.COMMAND, 
        handle_payment_proof
    ))

    # Run the bot
    print("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
