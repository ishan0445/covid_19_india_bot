# COVID-19 India status tracker bot for Telegram

Click on the following [link](https://t.me/covid_19_india_bot) or search for **@covid_19_india_bot** in Telegram.

## Installing Requirements 

```bash
pip install -r requirements.txt
```

## Exporting required environment variables
Please make sure you have set the following environment vars:
```bash
export BOT_TOKEN=[telegram_bot_token]
export CHATBASE_TOKEN=[chatbase_token]
```

## Running the App
```bash
gunicorn app:app
```

## Bot Usage
You can control the bot by sending these commands:
> **/help** - to see this help

>**/get_full_stats** - Get overall and statewise stats

>**/get_state_wise** - Get statewise stats

>**/get_overall** - Get overall stats

>**/get_helpline** - Get helpline numbers

>**/get_district_wise state** - Get district wise stats for a state

>**/gdw state** - Short for command /get_district_wise. **Ex:** /gdw Madhya Pradesh

>**/get_country_stats** - Gets top 20 countries by no. of confirmed cases
