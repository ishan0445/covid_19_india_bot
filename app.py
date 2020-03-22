import requests, flask, os
from requests_html import HTMLSession
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True
bot_token = os.environ['BOT_TOKEN']

session = HTMLSession()
r = session.get('https://www.covid19india.org/')

r.html.render()

def get_stats_overall():
    # Download page
    confirmed = r.html.find('#confvalue')[0].text
    confirmed_delta = r.html.find('#confirmed_delta')[0].text

    recovered = r.html.find('#recoveredvalue')[0].text
    recovered_delta = r.html.find('#recovered_delta')[0].text

    death = r.html.find('#deathsvalue')[0].text
    deaths_delta = r.html.find('#deaths_delta')[0].text

    death = r.html.find('#deathsvalue')[0].text
    deaths_delta = r.html.find('#deaths_delta')[0].text

    responseText = f'''<b>Cases in India:</b>
Confirmed Cases: <b>{confirmed} {confirmed_delta}</b>
Recovered Cases: <b>{recovered} {recovered_delta}</b>
Deaths: <b>{death} {deaths_delta}</b>'''

    return responseText

def get_stats_statewise():
    table_rows = r.html.find('#prefectures-table > tbody > tr')
    rows_states = []

    for tr in table_rows:
        td = tr.find('td')
        row = [i.text for i in td]
        rows_states.append(row)

    responseText = "<b>State Wise Cases in India:</b>\n<b>State / UT | Confirmed | Recovered | Death | Active</b>"


    for row in rows_states:
        if len(row) != 0 :
            responseText += "\n" + " | ".join(row)

    return responseText

def get_help_text():
    responseText = '''This bot will give latest stats of COVID-19 Cases in India. 
The data is collected from :
1) www.covid19india.org/

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
