import requests, flask, os, json
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True
bot_token = os.environ['BOT_TOKEN']

url = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise'
resp = requests.get(url)
json_statewise = resp.json()


def get_stats_overall():
    # Download page
    confirmed = json_statewise['data']['total']['confirmed']
    recovered = json_statewise['data']['total']['recovered']
    deaths = json_statewise['data']['total']['deaths']
    active = json_statewise['data']['total']['active']


    responseText = f'''<b>Cases in India:</b>
Confirmed Cases: <b>{confirmed}</b>
Recovered Cases: <b>{recovered}</b>
Deaths: <b>{deaths}</b>
Active Cases: <b>{active}</b>'''

    return responseText

def get_stats_statewise():
    responseText = ''
    for st in json_statewise['data']['statewise']:
        state = st['state']
        confirmed = st['confirmed']
        recovered = st['recovered']
        deaths = st['deaths']
        active = st['active']

        responseText += str(state) + " | " + str(confirmed) + " | " + str(recovered) + " | " + str(deaths) + " | " + str(active) + "\n"

    return responseText

def get_help_text():
    responseText = '''This bot will give latest stats of COVID-19 Cases in India. 
The data is collected from :
covid19india.org

You can control me by sending these commands:
/help - to see this help
/get_full_stats - Get overall and statewise stats
/get_state_wise - Get statewise stats
/get_overall - Get overall stats
/get_helpline - Get helpline numbers
'''
    return responseText

def sendMessage(chatID, responseText):
    url = 'https://api.telegram.org/bot'+ bot_token +'/sendMessage'
    requests.post(url, json= {"chat_id": chatID, "text": responseText , "parse_mode":"html"})

def sendPhoto(chatID, responseText):
    url = 'https://api.telegram.org/bot'+ bot_token +'/sendPhoto'
    requests.post(url, json= {"chat_id": chatID, "caption": responseText , "parse_mode":"html", "photo":"AgACAgUAAxkBAAPdXndhK8i3FUI7cFv8PfBYnX-bM3AAAuKpMRukLrhX11QX20YEUJD9qCUzAAQBAAMCAANtAAMh3wQAARgE"})
    

@app.route('/', methods=['POST'])
def getStats():
    
    json_data = request.get_json()
    print(json_data)
    chatID = json_data['message']['chat']['id']
    responseText = ''
      
    if json_data['message']['text'] == '/get_full_stats': 
        responseText = get_stats_overall()
        responseText += "\n\n\n" + get_stats_statewise()
        sendPhoto(chatID, responseText)
    elif json_data['message']['text'] == '/get_state_wise':
        responseText = get_stats_statewise()
        sendMessage(chatID, responseText)
    elif json_data['message']['text'] == '/get_overall':
        responseText = get_stats_overall()
        sendMessage(chatID, responseText)
    elif json_data['message']['text'] == '/get_helpline':
        sendPhoto(chatID, responseText)
    else:
        responseText = get_help_text()
        sendMessage(chatID, responseText)

    return responseText

if __name__ == '__main__':
    app.run()
