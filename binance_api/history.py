import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
from matplotlib.ticker import FormatStrFormatter


def history_to_png(history_file, output_file, period=None):
    history = pd.read_csv(history_file, parse_dates=True, index_col=0)
    if period is None:
        history = history.loc[history.index > pd.to_datetime("now") - pd.to_timedelta("30D")]
    elif isinstance(period, str):
        try:
            history = history.loc[history.index > pd.to_datetime(period)]
        except pd.errors.ParserError:
            history = history.loc[history.index > pd.to_datetime("now") - pd.to_timedelta(period)]
    elif isinstance(period, pd.Timestamp):
        history = history.loc[history.index > period]
    elif isinstance(period, pd.Timedelta):
        history = history.loc[history.index > pd.to_datetime("now") - period]
    elif isinstance(period, tuple):
        start, end = period
        if isinstance(start, str) and isinstance(end, str):
            history = history.loc[pd.to_datetime(end) > history.index > pd.to_datetime(start)]
        elif isinstance(start, pd.Timestamp) and isinstance(end, pd.Timestamp):
            history = history.loc[end > history.index > start]
        else:
            raise ValueError("Unknown period format")
    else:
        raise ValueError("Unknown period format")
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(history.index, history['total_usd'], 'g-', alpha=0.9)
    ax2.plot(history.index, history['total_btc'],  color='orange', alpha=0.9)
    ax1.set_xlabel("Datetime")
    ax1.set_ylabel("Total USD")
    ax2.set_ylabel("Total BTC")
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.5f'))
    ax1.xaxis.set_major_formatter(DateFormatter('%d %m %Y'))
    ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
    plt.tight_layout()
    plt.savefig(output_file, facecolor='white')
