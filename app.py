from flask import Flask, render_template, request
import requests
import telebot
import logging
from threading import Thread

app = Flask(__name__)

current_page = "loading"
TELEGRAM_BOT_TOKEN = '7124508860:AAEaFWSDAS8hj83416gHhCqwF3FpzgI9dpQ'
CHAT_ID = '1038031342'
WEB_SERVER_URL = 'http://localhost:5000/update'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to notify when the loading page is visited
def notify_loading():
    try:
        message = "The loading page has been visited."
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        data = {'chat_id': CHAT_ID, 'text': message}
        response = requests.post(url, data=data)
        logger.info(f"Notify loading response: {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"Error in notify_loading: {e}")

# Flask route to handle the main page
@app.route('/')
def index():
    global current_page
    if current_page == "loading":
        notify_loading()
    return render_template(f'{current_page}.html')

# Flask route to update the page based on the command
@app.route('/update', methods=['POST'])
def update_page():
    global current_page
    command = request.form.get('command')
    if command == 'yes':
        current_page = "yes"
    elif command == 'no':
        current_page = "no"
    else:
        current_page = "loading"
    logger.info(f"Page updated to: {current_page}")
    return 'Page updated', 200

# Telegram bot handler for /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send 'yes' or 'no' to control the web page.")
    logger.info("Sent welcome message")

# Telegram bot handler for 'yes' and 'no' messages
@bot.message_handler(func=lambda message: message.text.lower() in ['yes', 'no'])
def handle_message(message):
    command = message.text.lower()
    logger.info(f"Received command: {command}")
    try:
        response = requests.post(WEB_SERVER_URL, data={'command': command})
        if response.status_code == 200:
            bot.reply_to(message, f"Command '{command}' sent successfully.")
            logger.info(f"Command '{command}' sent successfully")
        else:
            bot.reply_to(message, f"Failed to send command '{command}'.")
            logger.error(f"Failed to send command '{command}': {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"Error handling command '{command}': {e}")
        bot.reply_to(message, f"Error handling command '{command}': {e}")

# Function to run Flask app
def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True)

# Function to run Telegram bot
def run_telegram_bot():
    logger.info("Starting Telegram bot")
    bot.infinity_polling()

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    telegram_thread = Thread(target=run_telegram_bot)

    flask_thread.start()
    telegram_thread.start()

    flask_thread.join()
    telegram_thread.join()
