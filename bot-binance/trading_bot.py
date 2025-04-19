# trading_bot.py
import time
from datetime import datetime
from binance.client import Client
from config import API_KEY, API_SECRET, SYMBOL, CANTIDAD, INTERVALO
from mercado import obtener_precio_actual, obtener_saldo, obtener_candles
from utils import configurar_logs, registrar_excel
from estrategias import estrategia_adaptativa
from ordenes import comprar, vender

client = Client(API_KEY, API_SECRET)

if __name__ == '__main__':
    while True:
        transacciones_log, montos_log = configurar_logs()
        saldo_inicial = obtener_saldo(client, 'USDT')
        montos_log.info(f"{datetime.now()} - Saldo inicial: {saldo_inicial} USDT")

        precio_actual = obtener_precio_actual(client, SYMBOL)
        df_candles = obtener_candles(client, SYMBOL)

        accion = estrategia_adaptativa(df_candles, precio_actual, transacciones_log)

        if accion == 'compra':
            comprar(client, SYMBOL, CANTIDAD, precio_actual, transacciones_log)
        elif accion == 'venta':
            vender(client, SYMBOL, CANTIDAD, precio_actual, transacciones_log)

        saldo_final = obtener_saldo(client, 'USDT')
        montos_log.info(f"{datetime.now()} - Saldo final: {saldo_final} USDT")
        registrar_excel(saldo_inicial, saldo_final)

        print("⏳ Esperando siguiente ciclo...")
        time.sleep(INTERVALO)
