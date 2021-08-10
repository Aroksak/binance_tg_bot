import os

import pandas as pd
from binance.spot import Spot
from dataframe_image import export


class MyWallet:
    def __init__(self, key, secret, earn_file, history_file):
        self.client = Spot(key=key, secret=secret)
        self.earn_file = earn_file
        self.history_file = history_file
        self.update()

    def update(self):
        all_coins = pd.DataFrame(self.client.coin_info())
        earn = pd.read_csv(self.earn_file, parse_dates=['start_date', 'end_date'])
        earn = earn.loc[earn['end_date'] > pd.to_datetime('today'), ['coin', 'amount']]
        spot_wallet = all_coins.loc[all_coins['free'].astype(float) > 0, ['coin', 'name', 'free']]
        spot_wallet['free'] = spot_wallet['free'].astype(float)
        full_wallet = pd.merge(spot_wallet, earn, how="outer", on="coin").fillna(0.0).rename(
            columns={"amount": "locked"})
        full_wallet['price'] = full_wallet['coin'].apply(self._get_price)
        full_wallet['USDT'] = (full_wallet['free'] + full_wallet['locked']) * full_wallet['price']
        self.wallet = full_wallet[['coin', 'name', 'free', 'locked', 'price', 'USDT']]\
            .sort_values("USDT", ascending=False)
        self.total_usd = full_wallet['USDT'].sum()
        self.total_btc = full_wallet['USDT'].sum() / self._get_price("BTC")
        pd.DataFrame({
            "total_usd": self.total_usd,
            "total_btc": self.total_btc
        }, index=[pd.to_datetime("now")]).to_csv(self.history_file, mode='a', header=not os.path.exists(self.history_file))

    def wallet_to_png(self, filename):
        export(self.wallet, filename, table_conversion='matplotlib')

    def _get_price(self, coin):
        if coin == "USDT":
            return 1.0
        return float(self.client.avg_price(coin + "USDT")['price'])
