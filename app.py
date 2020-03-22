import bs4, requests, flask
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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

    responseText="\n<b>State Wise Cases in India:</b>\n<b>State / UT | Confirmed(Indians) | Confirmed(Foriegns) | Cured | Death</b>"

    rows = Sort(rows_states)

    for row in rows:
        responseText += "\n" + " | ".join(row)

    return responseText



@app.route('/', methods=['POST'])
def getStats():
    responseText = get_stats_overall()
    responseText += "\n\n" + get_stats_statewise()

    url = 'https://api.telegram.org/bot1030632325:AAELjCpYk2F1bupS_a1Fl0loJoA3JjGSQJA/sendMessage'
    message = request.get_json()
    print(message)
    chatID = message['message']['chat']['id']
    requests.post(url, json= {"chat_id": chatID, "text": responseText , "parse_mode":"html"})
    
    return responseText

if __name__ == '__main__':
    app.run()
