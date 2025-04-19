# mercado.py
import pandas as pd

def obtener_saldo(client, moneda):
    return float(client.get_asset_balance(asset=moneda)['free'])

def obtener_precio_actual(client, symbol):
    return float(client.get_symbol_ticker(symbol=symbol)['price'])

def obtener_candles(client, symbol):
    klines = client.get_klines(symbol=symbol, interval='1m', limit=40)
    df = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                                       'close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore'])
    df['close'] = pd.to_numeric(df['close'])
    return df
