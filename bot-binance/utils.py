# utils.py
from datetime import datetime
import os
import logging
import openpyxl

def configurar_logs():
    fecha = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("logs", exist_ok=True)
    transacciones_path = f"logs/transacciones_{fecha}.log"
    montos_path = f"logs/montos_{fecha}.log"

    logging.basicConfig(level=logging.INFO)

    log_transacciones = logging.getLogger("transacciones")
    log_transacciones.handlers.clear()
    handler_t = logging.FileHandler(transacciones_path)
    log_transacciones.addHandler(handler_t)

    log_montos = logging.getLogger("montos")
    log_montos.handlers.clear()
    handler_m = logging.FileHandler(montos_path)
    log_montos.addHandler(handler_m)

    return log_transacciones, log_montos

def registrar_excel(monto_inicial, monto_final):
    from datetime import datetime
    import os

    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    archivo = f"excel/ganancias_{fecha}.xlsx"
    os.makedirs("excel", exist_ok=True)

    if not os.path.exists(archivo):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Hora", "Monto Inicial (USDT)", "Monto Final (USDT)", "Ganancia/Pérdida"])
    else:
        wb = openpyxl.load_workbook(archivo)
        ws = wb.active

    ganancia = round(monto_final - monto_inicial, 4)
    ws.append([hora, monto_inicial, monto_final, ganancia])
    wb.save(archivo)
