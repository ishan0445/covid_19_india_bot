import constants
import requests, flask, os, json
from tabulate import tabulate
import urls

class TelegramBot:
    def __init__(self):
        
        self.chatID = ''
        self.command = ''
        self.user_id = ''
        self. responseText = ''
        self.state_wise_etag = None
        self.json_statewise = None
        self.district_etag = None
        self.json_district_wise = None

    def parse_json_data(self, json_data):
        # Handeling message type
        print(json_data)
        if 'message' in json_data.keys():
            try:
                self.chatID = json_data['message']['chat']['id']
                self.command = json_data['message']['text'].lower()
                self.user_id = str(json_data['message']['from']['id'])
            except KeyError:
                print(f"KeyError Encountered")
                return ''
        elif 'edited_message' in json_data.keys():
            try:
                self.chatID = json_data['edited_message']['chat']['id']
                self.command = json_data['edited_message']['text'].lower()
                self.user_id = str(json_data['edited_message']['from']['id'])
            except KeyError:
                print(f"KeyError Encountered")
                return ''
        if self.chatID < 0:
            print('BLOCKED: '+json_data)
            return 'Blocked groups!!!'

        self.send_analitics()

    def run_command(self):

        if self.command == '/get_full_stats': 
            self.get_json_statewise()
            self.get_stats_overall()
            self.responseText += "\n\n\n" + self.get_stats_statewise()
            self.sendMessage(False)
        elif self.command == '/get_state_wise':
            self.get_json_statewise()
            self.responseText = self.get_stats_statewise()
            self.sendMessage(False)
        elif self.command == '/get_overall':
            self.get_json_statewise()
            self.get_stats_overall()
            self.sendMessage(False)
        elif self.command == '/get_helpline':
            self.sendPhoto(self.chatID, self.responseText)
        elif self.command.startswith('/get_district_wise') or self.command.startswith('/gdw'):
            cmd_split = self.command.strip().split(' ',1)
            state = ''
            if len(cmd_split) == 2:
                resp = self.get(urls.URL_DISTRICTWISE, self.district_etag)
                if resp:
                    self.district_etag = resp.headers.get("etag", None)
                    self.json_district_wise = resp.json()
                # json_district_wise = resp.json()
                state = cmd_split[1].lower()
                self.responseText = self.get_stats_district_wise(state)
            else:
                self.responseText = constants.INVALID_COMMAND_TEXT
            if not self.responseText.strip():
                self.responseText = 'No data for state: ' + state
            self.sendMessage(True)
        elif self.command.startswith('/get_country_stats'):
            self.responseText = self.get_top_country_stats(20, sortBy='cases')
            self.sendMessage(False)
        else:
            self.responseText = self.get_help_text()
            self.sendMessage(False)
        return self.responseText

    def under_maintanance(self):
        return constants.UNDER_MAINTAINANCE_TEXT

    def Sort(self, sub_li):
        return(sorted(sub_li, key = lambda x: x[1], reverse=True)) 


    def get_stats_overall(self, ):
        print('In method get_stats_overall():')

        confirmed = self.json_statewise['statewise'][0]['confirmed']
        confirmeddelta = self.json_statewise['key_values'][0]['confirmeddelta']
        recovered = self.json_statewise['statewise'][0]['recovered']
        recovereddelta = self.json_statewise['key_values'][0]['recovereddelta']
        deaths = self.json_statewise['statewise'][0]['deaths']
        deceaseddelta = self.json_statewise['key_values'][0]['deceaseddelta']
        active = self.json_statewise['statewise'][0]['active']

        self.responseText = f'''<b>Cases in India:</b>
    Confirmed Cases: <b>{confirmed} [ +{confirmeddelta} ]</b>
    Recovered Cases: <b>{recovered} [ +{recovereddelta} ]</b>
    Deaths: <b>{deaths} [ +{deceaseddelta} ]</b>
    Active Cases: <b>{active}</b>'''

    def get_stats_statewise(self):
        print('In method get_stats_statewise():')
        responseText = '<b>State Wise Cases in India:</b><pre>\n'
        respList = []
        for st in self.json_statewise['statewise']:
            if st['state'] == 'Total': continue
            state = st['state']
            confirmed = int(st['confirmed'])
            recovered = int(st['recovered'])
            deaths = int(st['deaths'])

            if confirmed != 0:
                respList.append([state.replace(' ', '\n'), confirmed, recovered, deaths] )
        

        respList = self.Sort(respList)
        respList = [['STATE','C', 'R', 'D' ]] + respList
        responseText += tabulate(respList, tablefmt='grid')
        responseText += '\n</pre>'
        return responseText

    def get_stats_district_wise(self, state):
        print('In method get_stats_district_wise():')
        json_district_wise =  {k.lower(): v for k, v in self.json_district_wise.items()}
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
        

        respList = self.Sort(respList)
        respList = [['DISTRICT','CONFIRMED' ]] + respList + [['Total',cnfTot]]
        # respList = [['DISTRICT','C', 'R', 'D' ]] + respList + [['Total',cnfTot,recTot,detTot]]

        responseText += tabulate(respList, tablefmt='grid')
        responseText += '\n</pre>'
        return responseText

    def get_top_country_stats(self, limit ,sortBy='cases'):
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

    def get_help_text(self):
        print('In method get_help_text():')
        return constants.HELP_TEXT

    def splitResponse(self, responseText):
        respList = responseText.split('\n\n')
        
        n = 10
        final = [respList[i * n:(i + 1) * n] for i in range((len(respList) + n - 1) // n )]

        return final



    def sendMessage(self, do_split):
        print('In method sendMessage():')
        url = 'https://api.telegram.org/bot'+ constants.bot_token +'/sendMessage'
        if do_split:
            listResponse = self.splitResponse(self.responseText)
            
            for l in listResponse:
                newResp = '\n\n'.join(l)
                resp = requests.post(url, json= {"chat_id": self.chatID, "text": newResp , "parse_mode":"html"})
        else:
            resp = requests.post(url, json= {"chat_id": self.chatID, "text": self.responseText , "parse_mode":"html"})
        print(resp.json())

    def sendPhoto(self, chatID, responseText):
        print('In method sendPhoto:')
        url = 'https://api.telegram.org/bot'+ constants.bot_token +'/sendPhoto'
        resp = requests.post(url, json= {"chat_id": chatID, "caption": responseText , "parse_mode":"html", "photo":"AgACAgUAAxkBAAPdXndhK8i3FUI7cFv8PfBYnX-bM3AAAuKpMRukLrhX11QX20YEUJD9qCUzAAQBAAMCAANtAAMh3wQAARgE"})
        print(resp.json())
        


    def get_json_statewise(self):
        resp = self.get(urls.URL_STATEWISE, self.state_wise_etag)
        if resp:
            self.state_wise_etag = resp.headers.get("etag", None)
            self.json_statewise = resp.json()
        return self.json_statewise


    def send_analitics(self):
        resp = requests.post('https://chatbase.com/api/message', json= {
        "api_key": constants.chatbase_token,
        "type": "user",
        "platform": "telegram",
        "message": f"{self.command} is called",
        "intent": "command",
        "version": "1.1",
        "user_id": self.user_id
        })

        print('ChatBase Resp: ' + str(resp.json()))


    def get(self, url, etag=None):
        res = requests.get(url, headers={"If-None-Match": etag})
        res.raise_for_status()
        if res.status_code in range(200,210):
            return res
        return None # indicates the content is not modified use cache

