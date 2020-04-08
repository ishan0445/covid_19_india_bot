import requests, flask, os, json, timeago
from datetime import datetime
from tabulate import tabulate
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

bot_token = os.environ['BOT_TOKEN']
chatbase_token = os.environ['CHATBASE_TOKEN']




def Sort(sub_li):
    return(sorted(sub_li, key = lambda x: x[1], reverse=True)) 


def get_stats_overall(json_statewise):
    print('In method get_stats_overall():')

    confirmed = json_statewise['statewise'][0]['confirmed']
    confirmeddelta = json_statewise['statewise'][0]['deltaconfirmed']
    recovered = json_statewise['statewise'][0]['recovered']
    recovereddelta = json_statewise['statewise'][0]['deltarecovered']
    deaths = json_statewise['statewise'][0]['deaths']
    deceaseddelta = json_statewise['statewise'][0]['deltadeaths']
    active = json_statewise['statewise'][0]['active']




    responseText = f'''<b>Cases in India:</b>
Confirmed Cases: <b>{confirmed} [ +{confirmeddelta} ]</b>
Recovered Cases: <b>{recovered} [ +{recovereddelta} ]</b>
Deaths: <b>{deaths} [ +{deceaseddelta} ]</b>
Active Cases: <b>{active}</b>'''

    return responseText

def get_stats_statewise(json_statewise):
    print('In method get_stats_statewise():')
    responseText = '<b>State Wise Cases in India:</b><pre>\n'
    respList = []
    for st in json_statewise['statewise']:
        if st['state'] == 'Total': continue
        state = st['state']
        confirmed = int(st['confirmed'])
        recovered = int(st['recovered'])
        deaths = int(st['deaths'])

        if confirmed != 0:
            respList.append([state.replace(' ', '\n'), confirmed, recovered, deaths] )
    

    respList = Sort(respList)
    respList = [['STATE','C', 'R', 'D' ]] + respList
    responseText += tabulate(respList, tablefmt='grid')
    responseText += '\n</pre>'
    return responseText

def get_stats_district_wise(json_district_wise, state):
    print('In method get_stats_district_wise():')
    json_district_wise =  {k.lower(): v for k, v in json_district_wise.items()}
    if state not in json_district_wise.keys():
        return ''

    responseText = '<b>Cases in '+state+':</b><pre>\n'
    respList = []
    cnfTot = 0
    # recTot = 0
    # detTot = 0
    
    for dt in json_district_wise[state]['districtData']:
        confirmed = json_district_wise[state]['districtData'][dt]['confirmed']
        cnfTot += confirmed
        # recovered = json_district_wise[state]['districtData'][dt]['recovered']
        # recTot += recovered
        # deaths = json_district_wise[state]['districtData'][dt]['deaths']
        # detTot += deaths

        if confirmed != 0:
            respList.append([dt.replace(' ', '\n'), confirmed]) #, recovered, deaths] )
    

    respList = Sort(respList)
    respList = [['DISTRICT','CONFIRMED' ]] + respList + [['Total',cnfTot]]
    # respList = [['DISTRICT','C', 'R', 'D' ]] + respList + [['Total',cnfTot,recTot,detTot]]

    responseText += tabulate(respList, tablefmt='grid')
    responseText += '\n</pre>'
    return responseText

def get_top_country_stats(limit ,sortBy='cases'):
    url = 'https://corona.lmao.ninja/countries?sort='+sortBy
    resp = requests.get(url)
    json_countries = resp.json()[:limit]
    responseText = '<b>Top '+str(limit)+' countries by no. of comfirmed cases:</b>\n<pre>'
    respList = []
    for ct in json_countries:
        country = ct['country']
        cases = ct['cases']
        deaths = ct['deaths']

        respList.append([country.replace(' ', '\n'), cases, deaths])


    respList = [['COUNTRY', 'CNFM', 'DTHS']] + respList
    responseText += tabulate(respList, tablefmt='grid')

    responseText+= '\n</pre>'

    return responseText

def get_help_text():
    print('In method get_help_text():')
    responseText = '''This bot will give latest stats of COVID-19 Cases in India. 
The data is collected from :
1) covid19india.org
2) NovelCOVID

You can control me by sending these commands:
/help - to see this help
/get_full_stats - Get overall and statewise stats
/get_state_wise - Get statewise stats
/get_overall - Get overall stats
/get_helpline - Get helpline numbers

/get_district_wise state - Get district wise stats for a state
/gdw state - Short for command /get_district_wise
Ex: /gdw Madhya Pradesh

/get_country_stats - Gets top 20 countries by no. of confirmed cases

/get_updates = get latest updates from India


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
    


def get_json_statewise():
    url = 'https://api.covid19india.org/data.json'
    resp = requests.get(url)
    json_statewise = resp.json()

    return json_statewise


def send_analitics(command, user_id):
    resp = requests.post('https://chatbase.com/api/message', json= {
    "api_key": chatbase_token,
    "type": "user",
    "platform": "telegram",
    "message": f"{command} is called",
    "intent": "command",
    "version": "1.1",
    "user_id": user_id
    })

    print('ChatBase Resp: ' + str(resp.json()))

def get_latest_updates():
    url = 'https://api.covid19india.org/updatelog/log.json'
    resp = requests.get(url)
    json_data = resp.json()[-5:]
    resonseText = """
<b>Latest Updates:</b>
"""
    for el in json_data:
        now = datetime.now()
        date = datetime.fromtimestamp(el['timestamp'])
        ago = timeago.format(date, now)
        resonseText += el['update'] + "- <i>" + ago + "</i>\n\n"

    return resonseText


def under_maintanance():
    return '''Sorry under maintenance!!!'''
    
#--------------
# API ROUTES
#--------------
@app.route('/', methods=['POST'])
def getStats():
    print('In method getStats():')
    json_data = request.get_json()
    print(json_data)
    chatID = ''
    command = ''
    user_id = ''

    # Handeling message type
    if 'message' in json_data.keys():
        try:
            chatID = json_data['message']['chat']['id']
            command = json_data['message']['text'].lower()
            user_id = str(json_data['message']['from']['id'])
        except KeyError:
            print(f"KeyError Encountered")
            return ''
    elif 'edited_message' in json_data.keys():
        try:
            chatID = json_data['edited_message']['chat']['id']
            command = json_data['edited_message']['text'].lower()
            user_id = str(json_data['edited_message']['from']['id'])
        except KeyError:
            print(f"KeyError Encountered")
            return ''
    if chatID < 0:
        print('BLOCKED: '+json_data)
        return 'Blocked groups!!!'

    send_analitics(command, user_id)
    
    responseText = ''
  
    if command == '/get_full_stats': 
        json_statewise = get_json_statewise()
        responseText = get_stats_overall(json_statewise)
        responseText += "\n\n\n" + get_stats_statewise(json_statewise)
        sendMessage(chatID, responseText, False)
    elif command == '/get_state_wise':
        json_statewise = get_json_statewise()
        responseText = get_stats_statewise(json_statewise)
        sendMessage(chatID, responseText, False)
    elif command == '/get_overall':
        json_statewise = get_json_statewise()
        responseText = get_stats_overall(json_statewise)
        sendMessage(chatID, responseText, False)
    elif command == '/get_helpline':
        sendPhoto(chatID, responseText)
    elif command.startswith('/get_district_wise') or command.startswith('/gdw'):
        cmd_split = command.strip().split(' ',1)
        state = ''
        if len(cmd_split) == 2:
            url = 'https://api.covid19india.org/state_district_wise.json'
            resp = requests.get(url)
            json_district_wise = resp.json()
            state = cmd_split[1].lower()
            responseText = get_stats_district_wise(json_district_wise, state)
        else:
            responseText = '''invalid command!!
Try:
/gdw state
or
/get_district_wise state
'''
        if not responseText.strip():
            responseText = 'No data for state: ' + state
        sendMessage(chatID, responseText, True)
    elif command.startswith('/get_country_stats'):
        responseText = get_top_country_stats(20, sortBy='cases')
        sendMessage(chatID,responseText, False)
    elif command.startswith('/get_updates'):
        responseText = get_latest_updates()
        sendMessage(chatID,responseText, False)
    else:
        responseText = get_help_text()
        sendMessage(chatID, responseText, False)
    return responseText

if __name__ == '__main__':
    app.run()
