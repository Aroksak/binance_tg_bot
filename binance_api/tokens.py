from pathlib import Path

import mplfinance as mpf
import pandas as pd
from binance.error import ClientError


class TokenMonitor:
    def __init__(self, client):
        self.client = client

    def get_token_chart(self, token: str, filename: str):
        try:
            answer = self.client.klines(
                token,
                interval='15m',
                limit=4*24
            )
        except ClientError:
            raise ValueError("Token not found")
        df = pd.DataFrame(answer, columns=[
            'Open time',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Close time',
            'Quote asset volume',
            'Number of trades',
            'Taker buy base asset volume',
            'Taker buy quote asset volume',
            'Ignore'
        ])
        df = df[['Open time', 'Open', 'Close', 'High', 'Low', 'Volume']]
        df['Open time'] = pd.to_datetime(df['Open time'] * 1_000_000)
        df = df.set_index('Open time')
        df.index.name = 'Date'
        mpf.plot(df.astype(float), type='candle', volume=True, mav=(7, 25), savefig=Path(filename), title=token)
