import requests, flask, os, json
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True
bot_token = os.environ['BOT_TOKEN']


def get_stats_overall(json_statewise):
    print('In method get_stats_overall():')
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

def get_stats_statewise(json_statewise):
    print('In method get_stats_statewise():')
    responseText = '<b>State Wise Cases in India:</b>\n<b>State / UT | Confirmed | Recovered | Deaths | Active</b>\n'
    for st in json_statewise['data']['statewise']:
        state = st['state']
        confirmed = st['confirmed']
        recovered = st['recovered']
        deaths = st['deaths']
        active = st['active']

        if confirmed != 0:
            responseText += state + " | " + str(confirmed) + " | " + str(recovered) + " | " + str(deaths) + " | " + str(active) + "\n"

    return responseText

def get_help_text():
    print('In method get_help_text():')
    responseText = '''This bot will give latest stats of COVID-19 Cases in India. 
The data is collected from :
covid19india.org

You can control me by sending these commands:
/help - to see this help
/get_full_stats - Get overall and statewise stats
/get_state_wise - Get statewise stats
/get_overall - Get overall stats
/get_helpline - Get helpline numbers
/patients_from_state state_name - Get patients details
/patients_from_city city_name - Get patients details
'''
    return responseText

def sendMessage(chatID, responseText):
    print('In method sendMessage():')
    url = 'https://api.telegram.org/bot'+ bot_token +'/sendMessage'
    requests.post(url, json= {"chat_id": chatID, "text": responseText , "parse_mode":"html"})

def sendPhoto(chatID, responseText):
    print('In method sendPhoto:')
    url = 'https://api.telegram.org/bot'+ bot_token +'/sendPhoto'
    requests.post(url, json= {"chat_id": chatID, "caption": responseText , "parse_mode":"html", "photo":"AgACAgUAAxkBAAPdXndhK8i3FUI7cFv8PfBYnX-bM3AAAuKpMRukLrhX11QX20YEUJD9qCUzAAQBAAMCAANtAAMh3wQAARgE"})
    
def get_patients_from_city(ct):
    url = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org'
    resp = requests.get(url)
    json_patients = resp.json()


    responseText = ''

    for pt in json_patients['data']['rawPatientData']:
        patientId = str(pt['patientId'])
        reportedOn = pt['reportedOn']
        city = pt['city']
        state = pt['state']
        status = pt['status']

        if city.lower() == ct.lower() :
            responseText +=f'''Patient ID: {patientId}
Reported On: {reportedOn}
City: {city}
State: {state}
Status: {status}

'''

    return responseText

def get_patients_from_state(st):
    url = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org'
    resp = requests.get(url)
    json_patients = resp.json()


    responseText = ''

    for pt in json_patients['data']['rawPatientData']:
        patientId = str(pt['patientId'])
        reportedOn = pt['reportedOn']
        city = pt['city']
        state = pt['state']
        status = pt['status']

        if state.lower() == st.lower() :
            responseText +=f'''Patient ID: {patientId}
Reported On: {reportedOn}
City: {city}
State: {state}
Status: {status}

'''

    return responseText

@app.route('/', methods=['POST'])
def getStats():
    print('In method getStats():')
    url = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise'
    resp = requests.get(url)
    json_statewise = resp.json()
    
    json_data = request.get_json()
    print(json_data)
    chatID = json_data['message']['chat']['id']
    responseText = ''
    
    command = json_data['message']['text'].lower()
    if command == '/get_full_stats': 
        responseText = get_stats_overall(json_statewise)
        responseText += "\n\n\n" + get_stats_statewise(json_statewise)
        sendPhoto(chatID, responseText)
    elif command == '/get_state_wise':
        responseText = get_stats_statewise(json_statewise)
        sendMessage(chatID, responseText)
    elif command == '/get_overall':
        responseText = get_stats_overall(json_statewise)
        sendMessage(chatID, responseText)
    elif command == '/get_helpline':
        sendPhoto(chatID, responseText)
    elif command.startswith('/patients_from_city'):
        cmd_split = command.strip().split(' ',1)
        city = ''
        if len(cmd_split) == 2:
            city = cmd_split[1]
            responseText = get_patients_from_city(city)
        else:
            responseText = 'invalid command!!'

        if not responseText.strip():
            responseText = 'No data for state: ' + city
        sendMessage(chatID, responseText)
    elif command.startswith('/patients_from_state'):
        cmd_split = command.strip().split(' ',1)
        state = ''
        if len(cmd_split) == 2:
            state = cmd_split[1]
            responseText = get_patients_from_state(state)
        else:
            responseText = 'invalid command!!'
        if not responseText.strip():
            responseText = 'No data for state: ' + state
        sendMessage(chatID, responseText)
    else:
        responseText = get_help_text()
        sendMessage(chatID, responseText)

    return responseText

if __name__ == '__main__':
    app.run()
