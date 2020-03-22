import bs4, requests, flask, os
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True
bot_token = os.environ['BOT_TOKEN']

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def Sort(sub_li): 
    sub_li.sort(key = lambda x: x[1], reverse=True) 
    return sub_li 

def get_stats_overall():
    # Download page
    getPage = requests.get('https://covidout.in/')
    getPage.raise_for_status() #if error it will stop the program

    # Parse text for foods
    html = bs4.BeautifulSoup(getPage.text, 'html.parser')
    confirmed = html.select('#dashboard > div.number-graph-wrapper > div:nth-child(1) > div > div.card-body.status-confirmed > div.cases-container > h2')[0].text
    hospitalized = html.select('#dashboard > div.number-graph-wrapper > div:nth-child(2) > div > div.card-body.status-hospitalized > div.cases-container > h2')[0].text
    icu = html.select('#dashboard > div.number-graph-wrapper > div:nth-child(3) > div > div.card-body.status-icu > div.cases-container > h2')[0].text
    recovered = html.select('#dashboard > div.number-graph-wrapper > div:nth-child(4) > div > div.card-body.status-recovered > div.cases-container > h2')[0].text
    died = html.select('#dashboard > div.number-graph-wrapper > div:nth-child(5) > div > div.card-body.status-died > div.cases-container > h2')[0].text

    responseText = f'''<b>Cases in India:</b>
Confirmed Cases: <b>{confirmed}</b>
Hospitalized Cases: <b>{hospitalized}</b>
In ICU: <b>{icu}</b>
Recovered Cases: <b>{recovered}</b>
Deaths: <b>{died}</b>'''

    return responseText

def get_stats_statewise():
    getPage = requests.get('https://www.mohfw.gov.in/')
    getPage.raise_for_status() #if error it will stop the program

    # Parse text for foods
    soup = bs4.BeautifulSoup(getPage.text, 'html.parser')

    table_rows = soup.find_all('tbody')[1].find_all('tr')
    rows_states = []

    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        if is_number(row[0]):
            rows_states.append(row[1:])

    responseText="<b>State Wise Cases in India:</b>\n<b>State / UT | Confirmed(Indians) | Confirmed(Foriegns) | Cured | Death</b>"

    rows = Sort(rows_states)

    for row in rows:
        responseText += "\n" + " | ".join(row)

    return responseText

def get_help_text():
    responseText = '''This bot will give latest stats of COVID-19 Cases in India. 
The data is collected from :
1) www.covidout.in
2) www.mohfw.gov.in

You can control me by sending these commands:
/help - to see this help
/getFullStats - Get overall and statewise stats
/getStateWise - Get statewise stats
/getOverall - Get overall stats
/getHelpline - Get helpline numbers
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
