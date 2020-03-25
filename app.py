import requests, flask, os, json
from tabulate import tabulate
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
    responseText = '<b>State Wise Cases in India:</b>\n<b>STATE | CNFM | RCVD | DETH | ACTV</b>\n'
    respList = []
    for st in json_statewise['data']['statewise']:
        state = st['state']
        confirmed = st['confirmed']
        recovered = st['recovered']
        deaths = st['deaths']
        active = st['active']

        if confirmed != 0:
            respList.append([state, str(confirmed), str(recovered), str(deaths), str(active)] )
    
    responseText += tabulate(respList, tablefmt='presto')
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

/patients_from_state state_name - Get patients details for a state
/pfs state_name - Short for command /patients_from_state
Ex: /pfs Madhya Pradesh

/patients_from_city city_name - Get patients details for a city
/pfc city_name - Short for command /patients_from_city
Ex: /pfc Jabalpur

Report Bugs: @ishan0445
made with ❤️ after washing 🧼👐 hands.
'''
    return responseText

def splitResponse(responseText):
    respList = responseText.split('\n\n')
    
    n = 10
    final = [respList[i * n:(i + 1) * n] for i in range((len(respList) + n - 1) // n )]

    return final



def sendMessage(chatID, responseText, do_split):
    print('In method sendMessage():')
    url = 'https://api.telegram.org/bot'+ bot_token +'/sendMessage'
    if do_split:
        listResponse = splitResponse(responseText)
        
        for l in listResponse:
            newResp = '\n\n'.join(l)
            resp = requests.post(url, json= {"chat_id": chatID, "text": newResp , "parse_mode":"html"})
    else:
        resp = requests.post(url, json= {"chat_id": chatID, "text": responseText , "parse_mode":"html"})
    print(resp.json())

def sendPhoto(chatID, responseText):
    print('In method sendPhoto:')
    url = 'https://api.telegram.org/bot'+ bot_token +'/sendPhoto'
    resp = requests.post(url, json= {"chat_id": chatID, "caption": responseText , "parse_mode":"html", "photo":"AgACAgUAAxkBAAPdXndhK8i3FUI7cFv8PfBYnX-bM3AAAuKpMRukLrhX11QX20YEUJD9qCUzAAQBAAMCAANtAAMh3wQAARgE"})
    print(resp.json())
    
def get_patients_from_city(ct):
    url = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org'
    resp = requests.get(url)
    json_patients = resp.json()


    responseText = ''

    for pt in json_patients['data']['rawPatientData']:
        patientId = 'NA' if not pt['patientId'] else pt['patientId']
        reportedOn = 'NA' if not pt['reportedOn'] else pt['reportedOn']
        city = 'NA' if not pt['city'] else pt['city']
        state = 'NA' if not pt['state'] else pt['state']
        status = 'NA' if not pt['status'] else pt['status']
        age = 'NA' if not pt['ageEstimate'] else pt['ageEstimate']
        gender = 'NA' if not pt['gender'] else pt['gender']

        if city.lower() == ct.lower() :
            responseText +=f'''Patient ID: {patientId}
Reported On: {reportedOn}
City: {city}
State: {state}
Age: {age}
Gender: {gender}
Status: {status}

'''

    return responseText

def get_patients_from_state(st):
    url = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org'
    resp = requests.get(url)
    json_patients = resp.json()


    responseText = ''

    for pt in json_patients['data']['rawPatientData']:
        patientId = 'NA' if not pt['patientId'] else pt['patientId']
        reportedOn = 'NA' if not pt['reportedOn'] else pt['reportedOn']
        city = 'NA' if not pt['city'] else pt['city']
        state = 'NA' if not pt['state'] else pt['status']
        status = 'NA' if not pt['status'] else pt['status']
        age = 'NA' if not pt['ageEstimate'] else pt['ageEstimate']
        gender = 'NA' if not pt['gender'] else pt['gender']

        if state.lower() == st.lower() :
            responseText +=f'''Patient ID: {patientId}
Reported On: {reportedOn}
City: {city}
State: {state}
Age: {age}
Gender: {gender}
Status: {status}

'''

    return responseText

@app.route('/', methods=['POST'])
def getStats():
    print('In method getStats():')
    json_data = request.get_json()
    print(json_data)
    chatID = json_data['message']['chat']['id']
    if chatID < 0 :
        print(json_data)
        return 'Blocked groups!!!'
    url = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise'
    resp = requests.get(url)
    json_statewise = resp.json()
    
    
    responseText = ''
    
    command = json_data['message']['text'].lower()
    if command == '/get_full_stats': 
        responseText = get_stats_overall(json_statewise)
        responseText += "\n\n\n" + get_stats_statewise(json_statewise)
        sendMessage(chatID, responseText, False)
    elif command == '/get_state_wise':
        responseText = get_stats_statewise(json_statewise)
        sendMessage(chatID, responseText, False)
    elif command == '/get_overall':
        responseText = get_stats_overall(json_statewise)
        sendMessage(chatID, responseText, False)
    elif command == '/get_helpline':
        sendPhoto(chatID, responseText)
    elif command.startswith('/patients_from_city') or command.startswith('/pfc'):
        cmd_split = command.strip().split(' ',1)
        city = ''
        if len(cmd_split) == 2:
            city = cmd_split[1]
            responseText = get_patients_from_city(city)
        else:
            responseText = 'invalid command!!'

        if not responseText.strip():
            responseText = 'No data for state: ' + city
        sendMessage(chatID, responseText, True)
    elif command.startswith('/patients_from_state')  or command.startswith('/pfs'):
        cmd_split = command.strip().split(' ',1)
        state = ''
        if len(cmd_split) == 2:
            state = cmd_split[1]
            responseText = get_patients_from_state(state)
        else:
            responseText = 'invalid command!!'
        if not responseText.strip():
            responseText = 'No data for state: ' + state
        sendMessage(chatID, responseText, True)
    else:
        responseText = get_help_text()
        sendMessage(chatID, responseText, False)

    return responseText

if __name__ == '__main__':
    app.run()
