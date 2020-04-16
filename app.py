import requests, os, json, timeago, logging
from datetime import datetime
from tabulate import tabulate
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, InlineQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Utility Functions
def get_json_statewise():
    url = 'https://api.covid19india.org/data.json'
    resp = requests.get(url)
    json_statewise = resp.json()

    return json_statewise

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




    responseText = f'''<b>Cases in India 🇮🇳:</b>
🦠Confirmed Cases: <b>{confirmed} [ +{confirmeddelta} ]</b>
💪🏼Recovered Cases: <b>{recovered} [ +{recovereddelta} ]</b>
💀Deaths: <b>{deaths} [ +{deceaseddelta} ]</b>
🏥Active Cases: <b>{active}</b>'''

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

def get_button_list():
    button_list = [
            [InlineKeyboardButton("Andaman and Nicobar Islands", callback_data="Andaman and Nicobar Islands"),
            InlineKeyboardButton("Andhra Pradesh", callback_data="Andhra Pradesh")],
            [InlineKeyboardButton("Arunachal Pradesh", callback_data="Arunachal Pradesh"),
            InlineKeyboardButton("Assam", callback_data="Assam")],
            [InlineKeyboardButton("Bihar", callback_data="Bihar"),
            InlineKeyboardButton("Chandigarh", callback_data="Chandigarh")],
            [InlineKeyboardButton("Chhattisgarh", callback_data="Chhattisgarh"),
            InlineKeyboardButton("Dadra and Nagar Haveli", callback_data="Dadra and Nagar Haveli")],
            [InlineKeyboardButton("Delhi", callback_data="Delhi"),
            InlineKeyboardButton("Goa", callback_data="Goa")],
            [InlineKeyboardButton("Gujarat", callback_data="Gujarat"),
            InlineKeyboardButton("Haryana", callback_data="Haryana")],
            [InlineKeyboardButton("Himachal Pradesh", callback_data="Himachal Pradesh"),
            InlineKeyboardButton("Jammu and Kashmir", callback_data="Jammu and Kashmir")],
            [InlineKeyboardButton("Jharkhand", callback_data="Jharkhand"),
            InlineKeyboardButton("Karnataka", callback_data="Karnataka")],
            [InlineKeyboardButton("Kerala", callback_data="Kerala"),
            InlineKeyboardButton("Ladakh", callback_data="Ladakh")],
            [InlineKeyboardButton("Madhya Pradesh", callback_data="Madhya Pradesh"),
            InlineKeyboardButton("Maharashtra", callback_data="Maharashtra")],
            [InlineKeyboardButton("Manipur", callback_data="Manipur"),
            InlineKeyboardButton("Mizoram", callback_data="Mizoram")],
            [InlineKeyboardButton("Nagaland", callback_data="Nagaland"),
            InlineKeyboardButton("Odisha", callback_data="Odisha")],
            [InlineKeyboardButton("Puducherry", callback_data="Puducherry"),
            InlineKeyboardButton("Punjab", callback_data="Punjab")],
            [InlineKeyboardButton("Rajasthan", callback_data="Rajasthan"),
            InlineKeyboardButton("Tamil Nadu", callback_data="Tamil Nadu")],
            [InlineKeyboardButton("Telangana", callback_data="Telangana"),
            InlineKeyboardButton("Tripura", callback_data="Tripura")],
            [InlineKeyboardButton("Uttar Pradesh", callback_data="Uttar Pradesh"),
            InlineKeyboardButton("Uttarakhand", callback_data="Uttarakhand")],
            [InlineKeyboardButton("West Bengal", callback_data="West Bengal")]
        ]
    return button_list


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    print('In method get_help_text():')
    responseText = '''This bot will give latest stats of COVID-19 Cases in India. 
The data is collected from :
1) covid19india.org
2) NovelCOVID

You can control me by sending these commands:
/help - to see this help.
/get_full_stats - Get overall and statewise stats.
/get_state_wise - Get statewise stats.
/get_overall - Get overall stats.
/get_helpline - Get helpline numbers.
/get_district_wise - Get district wise stats for a state.
/gdw - Short for command /get_district_wise.
/get_country_stats - Gets top 20 countries by no. of confirmed cases.
/get_updates - Get latest updates from India.


Report Bugs: @ishan0445
made with ❤️ after washing 🧼👐 hands.
'''
    update.message.reply_text(responseText)


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def get_full_stats(update, context):
    json_statewise = get_json_statewise()
    responseText = get_stats_overall(json_statewise)
    responseText += "\n\n\n" + get_stats_statewise(json_statewise)
    update.message.reply_html(responseText)

def get_state_wise(update, context):
    json_statewise = get_json_statewise()
    responseText = get_stats_statewise(json_statewise)
    update.message.reply_html(responseText)

def get_overall(update, context):
    json_statewise = get_json_statewise()
    responseText = get_stats_overall(json_statewise)
    update.message.reply_html(responseText)


def get_helpline(update, context):
    responseText = '''Please visit the fillowing page for official helpline numbers:
https://www.mohfw.gov.in/pdf/coronvavirushelplinenumber.pdf
'''
    update.message.reply_html(responseText)

def get_latest_updates(update, context):
    url = 'https://api.covid19india.org/updatelog/log.json'
    resp = requests.get(url)
    json_data = resp.json()[-7:]
    json_data.reverse()
    responseText = """
<b>Latest Updates:</b>
"""
    for el in json_data:
        now = datetime.now()
        date = datetime.fromtimestamp(el['timestamp'])
        ago = timeago.format(date, now)
        responseText += el['update'] + "- <i>" + ago + "</i>\n\n"

    update.message.reply_html(responseText)


def get_country_stats(update, context):
    limit = 20
    sortBy='cases'

    url = 'https://corona.lmao.ninja/countries?sort='+sortBy
    resp = requests.get(url)
    json_countries = resp.json()[:limit]
    responseText = '<b>🌏Top '+str(limit)+' countries by no. of comfirmed cases:</b>\n<pre>'
    respList = []
    for ct in json_countries:
        country = ct['country']
        cases = ct['cases']
        deaths = ct['deaths']

        respList.append([country.replace(' ', '\n'), cases, deaths])


    respList = [['COUNTRY', 'CNFM', 'DTHS']] + respList
    responseText += tabulate(respList, tablefmt='grid')

    responseText+= '\n</pre>'

    update.message.reply_html(responseText)

def get_stats_district_wise(update, context):
    
    keyboard = get_button_list()

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_html('Please choose:', reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query

    state = query.data.lower()
    url = 'https://api.covid19india.org/state_district_wise.json'
    resp = requests.get(url)
    json_district_wise = resp.json()
    
    json_district_wise =  {k.lower(): v for k, v in json_district_wise.items()}
    if state not in json_district_wise.keys():
        return ''

    responseText = '<b>Cases in '+state+':</b><pre>\n'
    respList = []
    cnfTot = 0
    
    for dt in json_district_wise[state]['districtData']:
        confirmed = json_district_wise[state]['districtData'][dt]['confirmed']
        cnfDelta = json_district_wise[state]['districtData'][dt]['delta']['confirmed']
        cnfTot += confirmed

        if confirmed != 0:
            respList.append([dt.replace(' ', '\n'), str(confirmed) + ("" if cnfDelta == 0 else " [+"+str(cnfDelta)+"]") ])
    

    respList = Sort(respList)
    respList = [['DISTRICT','CONFIRMED' ]] + respList + [['Total',cnfTot]]
    

    responseText += tabulate(respList, tablefmt='grid')
    responseText += '\n</pre>'


    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(responseText,parse_mode='html')

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    TOKEN = os.environ['BOT_TOKEN']
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("get_full_stats", get_full_stats))
    dp.add_handler(CommandHandler("get_state_wise", get_state_wise))
    dp.add_handler(CommandHandler("get_overall", get_overall))
    dp.add_handler(CommandHandler("get_helpline", get_helpline))
    dp.add_handler(CommandHandler("get_updates", get_latest_updates))
    dp.add_handler(CommandHandler("get_country_stats", get_country_stats))
    dp.add_handler(CommandHandler("gdw", get_stats_district_wise))
    dp.add_handler(CommandHandler("get_district_wise", get_stats_district_wise))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(CallbackQueryHandler(button))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    
    
    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
    updater.bot.set_webhook("https://tranquil-cove-14056.herokuapp.com/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()