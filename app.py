from flask import Flask, render_template, request
import requests
import telebot
from threading import Thread

app = Flask(__name__)

current_page = "loading"
TELEGRAM_BOT_TOKEN = '7124508860:AAEaFWSDAS8hj83416gHhCqwF3FpzgI9dpQ'
CHAT_ID = '1038031342'
WEB_SERVER_URL = 'https://meragora-github-io-24.onrender.com/'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def notify_loading():
    message = "The loading page has been visited."
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

@app.route('/')
def index():
    global current_page
    if current_page == "loading":
        notify_loading()
    return render_template(f'{current_page}.html')

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
    return 'Page updated', 200

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send 'yes' or 'no' to control the web page.")

@bot.message_handler(func=lambda message: message.text.lower() in ['yes', 'no'])
def handle_message(message):
    command = message.text.lower()
    response = requests.post(WEB_SERVER_URL, data={'command': command})
    if response.status_code == 200:
        bot.reply_to(message, f"Command '{command}' sent successfully.")
    else:
        bot.reply_to(message, f"Failed to send command '{command}'.")

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True)

def run_telegram_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    telegram_thread = Thread(target=run_telegram_bot)

    flask_thread.start()
    telegram_thread.start()

    flask_thread.join()
    telegram_thread.join()
