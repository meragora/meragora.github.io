from flask import Flask, render_template, request
import requests

app = Flask(__name__)

current_page = "loading"
TELEGRAM_BOT_TOKEN = '7124508860:AAEaFWSDAS8hj83416gHhCqwF3FpzgI9dpQ'
CHAT_ID = '1038031342'

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

if __name__ == '__main__':
    app.run(debug=True)
