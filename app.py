import bs4, requests, flask
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['POST'])
def getStats():
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

    responseText = f'''Confirmed Cases: {confirmed}
Hospitalized Cases: {hospitalized}
In ICU: {icu}
Recovered Cases: {recovered}
Deaths: {died}'''

    message = request.get_json()
    chatID = message['chat']['id']
    requests.post(url, json= {"chat_id": chatID, "text": responseText }
    
    return responseText

if __name__ == '__main__':
    app.run()
