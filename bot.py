import json
import logging

from binance.spot import Spot
from telegram import Update
from telegram.ext import Updater, CommandHandler, Filters, CallbackContext

from binance_api import MyWallet, history_to_png, TokenMonitor

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class BinanceBot:
    def __init__(self, binance_key, binance_secret, telegram_key, user_id, earn_file=None):
        client = Spot(key=binance_key, secret=binance_secret)
        self.wallet = MyWallet(client=client, earn_file=earn_file, history_file='history.csv')
        self.tm = TokenMonitor(client=client)
        self.updater = Updater(token=telegram_key, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue
        self.user_id = user_id
        self._setup_dispatcher()

    def _setup_dispatcher(self):
        self.dispatcher.add_handler(CommandHandler("stats", self.send_standard_stats,
                                                   Filters.user(user_id=self.user_id)))
        self.dispatcher.add_handler(CommandHandler("history", self.send_history_plot,
                                                   Filters.user(user_id=self.user_id)))
        self.dispatcher.add_handler(CommandHandler("chart", self.send_token_chart,
                                                   Filters.user(user_id=self.user_id)))

    def send_standard_stats(self, update: Update, context: CallbackContext):
        self.wallet.update()
        context.bot.send_message(
            chat_id=self.user_id,
            text=f"Total USD: {self.wallet.total_usd:.2f}\nTotal BTC: {self.wallet.total_btc:.5f}"
        )
        self.wallet.wallet_to_png("wallet.png")
        context.bot.send_photo(chat_id=self.user_id, photo=open("wallet.png", 'rb'))

    def send_history_plot(self, update, context):
        history_to_png("history.csv", "history.png")
        context.bot.send_photo(chat_id=self.user_id, photo=open("history.png", 'rb'))

    def send_token_chart(self, update, context):
        token = context.args[0]
        try:
            self.tm.get_token_chart(token, "chart.png")
            context.bot.send_photo(
                chat_id=self.user_id,
                photo=open("chart.png", 'rb')
            )
        except ValueError:
            context.bot.send_message(
                chat_id=self.user_id,
                text=f"Token {token} not found on Binance."
            )

    def serve_forever(self):
        self.updater.start_polling()
        self.updater.idle()


def main():
    config = json.load(open("config.json", 'r'))
    bot = BinanceBot(**config)
    bot.serve_forever()


if __name__ == '__main__':
    main()
