# binance_tg_bot
Telegram bot for checking pulse on Binance

# How to use:
- Clone the repo.
- Create new telegram bot via @BotFather.
- Create file config.json in the main directory with the following content:
```
{
  "binance_key": %YOUR_BINANCE_API_KEY%,
  "binance_secret": %YOU_BINANCE_SECRET_API_KEY%,
  "telegram_key": %TELEGRAM_BOT_API_KEY_FROM_@BotFather%,
  "user_id": %YOU_TELEGRAM_USER_ID%,
  "earn_file": "earn.csv" // Add this line if you want to monitor your staking crypto, otherwise just remove it.
}
```
- If you want to track crypto in staking (Binance's "Earn" page) create earn.csv with your current staking coins. Unfortunately Binance API provides no way to aquire this information automatically. Example:
```
coin,amount,start_date,end_date
ADA,100,2021-08-01,2021-09-01
BNB,1.5,2021-08-25,2021-10-25
ETH,0.334,2021-08-30,2021-12-12
```
- Run bot.py, probably you would like to host it somewhere to run full-time.

# Commands:
Currently bot supports two commands:
- /stats
Prints total sum of your binance wallet in USDT and BTC, sends image with info for all possesed coins.
- /history
Sends plot of you totals in USDT and BTC over time you used the bot.
- /chart %TOKEN%
Sends candle plot of provided token-pair. Data is for last 24 hours, with candles 15 minutes wide.

# TODO:
- add daily update on stats
- add command to update earn.csv via the bot
- ~~add command to get plot for any token~~
