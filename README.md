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
```

## Running the App
```bash
python3 app.py
```

## Bot Usage
You can control the bot by sending these commands:
> **/help** - to see this help

>**/get_full_stats** - Get overall and statewise stats

>**/get_state_wise** - Get statewise stats

>**/get_overall** - Get overall stats

>**/get_helpline** - Get helpline numbers

>**/get_district_wise** - Get district wise stats for a state

>**/gdw** - Short for command /get_district_wise.

>**/get_country_stats** - Gets top 20 countries by no. of confirmed cases.

>**/get_updates** - Get latest updtes from India.
