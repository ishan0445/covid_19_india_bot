import os

HELP_TEXT = '''This bot will give latest stats of COVID-19 Cases in India. 
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


Report Bugs: @ishan0445
made with ❤️ after washing 🧼👐 hands.
'''


UNDER_MAINTAINANCE_TEXT = '''Sorry under maintenance!!! Check back later.
Meanwhile try other commands from /help
'''


INVALID_COMMAND_TEXT = '''invalid command!!
Try:
/gdw state
or
/get_district_wise state
'''

bot_token = os.environ['BOT_TOKEN']
chatbase_token = os.environ['CHATBASE_TOKEN']