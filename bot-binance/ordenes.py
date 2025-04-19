# ordenes.py
from binance.exceptions import BinanceAPIException
from binance.enums import *

def comprar(client, symbol, cantidad, precio, logger):
    try:
        orden = client.order_limit_buy(symbol=symbol, quantity=cantidad, price=str(precio))
        logger.info(f"COMPRA - {orden}")
        return True
    except BinanceAPIException as e:
        logger.error(f"Error al comprar: {e}")
        return False

def vender(client, symbol, cantidad, precio, logger):
    try:
        orden = client.order_limit_sell(symbol=symbol, quantity=cantidad, price=str(precio))
        logger.info(f"VENTA - {orden}")
        return True
    except BinanceAPIException as e:
        logger.error(f"Error al vender: {e}")
        return False
