import requests, flask, os, json
from tabulate import tabulate
from flask import request
import constants
from constants import bot_token, chatbase_token
from telegram_bot import TelegramBot

app = flask.Flask(__name__)
app.config["DEBUG"] = True
bot = TelegramBot()

#--------------
# API ROUTES
#--------------
@app.route('/', methods=['POST'])
def getStats():
    print('In method getStats():')
    json_data = request.get_json()
    bot.parse_json_data(json_data)
    sent_message = bot.run_command()
    return sent_message
    
if __name__ == '__main__':
    app.run()
    