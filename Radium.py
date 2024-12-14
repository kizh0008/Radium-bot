from datetime import datetime, timezone, time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Bot token and username
TOKEN = '7865965920:AAHCo5TK7A2OCE_s25B4PrFdi18ofMy1skA'
BOT_USERNAME = '@RAD_Radium_bot'

# Launch date: December 13th, 10 PM UTC
LAUNCH_DATE = datetime(2024, 12, 13, 22, 0, 0, tzinfo=timezone.utc)

# Launch info text
LAUNCH_INFO = "🚀 Radium Token will be launched on December 13th at 10 PM UTC! 🚀"

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me! I am Radium AI!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am Radium AI! Please type something so I can respond!')

# Countdown message
async def send_countdown_message(context: ContextTypes.DEFAULT_TYPE):
    # Get current time
    now = datetime.now(timezone.utc)
    # Calculate the remaining time until the launch date
    remaining_time = LAUNCH_DATE - now
    # Calculate days, hours, minutes, and seconds
    days = remaining_time.days
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    countdown_text = f"🚀 Countdown to Radium Token Launch! 🚀\n\n" \
                     f"Time remaining: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds."
    
    print(f"Countdown message: {countdown_text}")  # Debug print

    # Send the countdown message to a specific group chat (replace `GROUP_CHAT_ID` with the actual chat ID)
    group_chat_id = -1001234567890  # Replace with your group chat ID
    try:
        await context.bot.send_message(chat_id=group_chat_id, text=countdown_text)
    except Exception as e:
        print(f"Error sending message: {e}")

# Function to handle user responses
def handle_response(text: str) -> str:
    processed = text.lower()

    if 'hello' in processed:
        return 'Hey there!'
    if 'hi' in processed:
        return 'Hey there!'
    if 'how are you' in processed:
        return 'I am good!'
    if 'website' in processed:
        return 'https://radium-crypto.vercel.app/'
    if 'ca' in processed:
        return 'GRaBF72XpqpvdovPfFTV6JxVcL5kcgUpqKiHv2hapump'

    return ""

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    response = handle_response(text)

    # Keywords to trigger the launch message
    keywords = ['token', 'launch', 'rad', 'radium', 'crypto']

    # Check if any of the keywords are in the message text
    if any(keyword in text.lower() for keyword in keywords):
        # Send launch information
        launch_info = "🚀 XRPS Token will be launched on 18.35 UTC! 🚀"
        await update.message.reply_text(launch_info)
        return  # Stop further processing to avoid sending general responses

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    print('Bot:', response)
    await update.message.reply_text(response)

# Handler to delete messages containing "rug" or "rug pull"
async def delete_rug_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
        print(f"Deleted message from user {update.message.chat.id}: {update.message.text}")
    except Exception as e:
        print(f"Error deleting message: {e}")

# Handler to delete messages containing bad words
async def delete_bad_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bad_words = ['fuck', 'suck','mf']  # Add more bad words as needed
    text = update.message.text.lower()  # Make the text lowercase for case-insensitive matching
    if any(word in text for word in bad_words):
        try:
            await update.message.delete()
            print(f"Deleted inappropriate message from user {update.message.chat.id}: {update.message.text}")
        except Exception as e:
            print(f"Error deleting message: {e}")

# Greet new members
async def greet_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        username = member.username if member.username else member.first_name
        await update.message.reply_text(f"Welcome, @{username}! 🎉 We're glad to have you here!")

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# Main function
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Add specific handlers for deleting certain messages
    app.add_handler(MessageHandler(filters.Regex(r'\b(rug|rug pull)\b'), delete_rug_message))  # Rug handler
    app.add_handler(MessageHandler(filters.Regex(r'\b(fuck|suck)\b'), delete_bad_words))  # Bad words handler

    # Add message handler for general responses
    app.add_handler(MessageHandler(filters.TEXT & ~filters.Regex(r'\b(rug|rug pull|fuck|suck)\b'), handle_message))

    # Add handler to greet new members
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_user))

    # Add error handler
    app.add_error_handler(error)

    # Set up JobQueue to send countdown message every day at 10 AM UTC
    job_queue = app.job_queue

    # Fix: Correctly create a time object
    job_queue.run_daily(send_countdown_message, time=time(10, 0), days=(0, 1, 2, 3, 4, 5, 6))  # Daily at 10 AM UTC

    # Send the first countdown immediately after starting the bot (for testing purposes)
    app.job_queue.run_once(send_countdown_message, 0)

    print('Polling...')
    app.run_polling(poll_interval=3)
