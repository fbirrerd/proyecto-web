# estrategias.py
import ta

def detectar_tendencia(df):
    df['ema5'] = ta.trend.ema_indicator(close=df['close'], window=5)
    df['ema15'] = ta.trend.ema_indicator(close=df['close'], window=15)

    if df['ema5'].iloc[-1] > df['ema15'].iloc[-1]:
        return "alcista"
    elif df['ema5'].iloc[-1] < df['ema15'].iloc[-1]:
        return "bajista"
    return "neutral"

def calcular_volatilidad(df):
    df['returns'] = df['close'].pct_change()
    return df['returns'].std() * 100  # %

def estrategia_scalping(df):
    if df['close'].iloc[-1] < df['close'].iloc[-2] * 0.995:
        return 'compra'
    elif df['close'].iloc[-1] > df['close'].iloc[-2] * 1.005:
        return 'venta'
    return None

def estrategia_swing(df, precio_actual):
    soporte = df['close'].min()
    resistencia = df['close'].max()

    if precio_actual > resistencia * 0.995:
        return 'compra'
    elif precio_actual < soporte * 1.005:
        return 'venta'
    return None

def estrategia_adaptativa(df, precio_actual, logger):
    tendencia = detectar_tendencia(df)
    volatilidad = calcular_volatilidad(df)

    logger.info(f"Tendencia: {tendencia} | Volatilidad: {volatilidad:.2f}%")

    if volatilidad > 0.5:
        logger.info("Activando SCALPING por volatilidad")
        return estrategia_scalping(df)
    else:
        logger.info("Activando SWING por baja volatilidad")
        return estrategia_swing(df, precio_actual)
