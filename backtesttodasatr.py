# import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import numpy as np
import pandas_ta as ta
from newcheck import databacktesting

# Lista de criptomonedas a evaluar
timeframe = '5m'
# Especificar el número de hilos que deseas usar
max_workers = 50  # Cambia este valor según tus necesidades

symbols = ['SOLUSDT', 'PHBUSDT', 'POLYXUSDT', 'SNTUSDT', 'CHRUSDT', 'MANTAUSDT', 'OXTUSDT', 'BIGTIMEUSDT', 'POWRUSDT', 'MYROUSDT', 'AEROUSDT', 'ZROUSDT', 'GHSTUSDT', 'XRPUSDT', 'HIVEUSDT', 'AAVEUSDT', 'TAOUSDT', 'OPUSDT', 'JASMYUSDT', 'DUSDT', 'RADUSDT', 'KLAYUSDT', 'QNTUSDT', 'SUSDT', 'BALUSDT', 'ZENUSDT', 'BIOUSDT', 'DEXEUSDT', 'VTHOUSDT', 'BATUSDT', 'NEOUSDT', 'MDTUSDT', 'GMTUSDT', 'SONICUSDT', 'ETHUSDT', 'DEFIUSDT', 'CYBERUSDT', 'FLUXUSDT', 'ALPHAUSDT', 'XVGUSDT', 'JUPUSDT', 'ADAUSDT', 'ONTUSDT', 'KAIAUSDT', 'WLDUSDT', 'FXSUSDT', 'STRKUSDT', 'QUICKUSDT', 'MINAUSDT', 'SEIUSDT', 'MORPHOUSDT', 'LTCUSDT', 'GUSDT', 'HFTUSDT', 'LITUSDT', 'FTMUSDT', 'SOLVUSDT', 'DOGSUSDT', 'ARCUSDT', 'PIXELUSDT', 'AGLDUSDT', '1000FLOKIUSDT', 'GOATUSDT', 'TRXUSDT', 'SSVUSDT', 'ONGUSDT', 'XVSUSDT', 'RONINUSDT', 'ALGOUSDT', 'CTKUSDT', 'UXLINKUSDT', 'NEARUSDT', 'POLUSDT', '1000000MOGUSDT', 'MOVEUSDT', 'HBARUSDT', 'ORCAUSDT', 'JOEUSDT', 'PONKEUSDT', '1000PEPEUSDT', 'BRETTUSDT', 'STEEMUSDT', 'PNUTUSDT', 'ATOMUSDT', 'DUSKUSDT', 'SLPUSDT', 'ACEUSDT', 'STMXUSDT', 'WOOUSDT', 'LDOUSDT', 'AXLUSDT', 'ALPACAUSDT', 'SAFEUSDT', 'ALICEUSDT', 'VETUSDT', 'MBOXUSDT', 'B3USDT', 'XMRUSDT', 'KMNOUSDT', 'RAYSOLUSDT', 'ALTUSDT', '1INCHUSDT', 'AI16ZUSDT', 'GLMUSDT', 'DARUSDT', 'ARPAUSDT', 'TWTUSDT', 'WAXPUSDT', 'DODOXUSDT', 'SHELLUSDT', 'CAKEUSDT', 'ACTUSDT', 'AERGOUSDT', 'RVNUSDT', 'USUALUSDT', 'VOXELUSDT', 'APTUSDT', 'FIOUSDT', 'C98USDT', 'ILVUSDT', 'ETCUSDT', 'LUMIAUSDT', 'RDNTUSDT', 'ARBUSDT', 'ARKUSDT', 'BONDUSDT', 'LSKUSDT', 'EOSUSDT', 'ROSEUSDT', 'TONUSDT', 'BANANAUSDT', 'AVAAIUSDT', 'LRCUSDT', 'KSMUSDT', 'COOKIEUSDT', 'IOUSDT', 'PORTALUSDT', 'DOTUSDT', 'BANDUSDT', 'COMBOUSDT', 'SYSUSDT', 'PEOPLEUSDT', 'AGIXUSDT', 'IPUSDT', 'EDUUSDT', 'CATIUSDT', 'UNFIUSDT', 'ASTRUSDT', 'AVAXUSDT', 'EGLDUSDT', 'SNXUSDT', 'ZKUSDT', 'TNSRUSDT', 'SCRUSDT', 'MAGICUSDT', 'USDCUSDT', 'TUSDT', 'YFIUSDT', 'PENGUUSDT', 'XEMUSDT', 'TROYUSDT', 'LUNA2USDT', 'TUTUSDT', 'VICUSDT', 'AMBUSDT', 'BOMEUSDT', 'ONDOUSDT', 'BLZUSDT', 'XLMUSDT', 'ENJUSDT', 'RIFUSDT', 'MANAUSDT', 'VELODROMEUSDT', 'STXUSDT', 'LPTUSDT', 'MOVRUSDT', 'PERPUSDT', 'TRUMPUSDT', 'MASKUSDT', 'WAVESUSDT', 'OMUSDT', 'XTZUSDT', 'YGGUSDT', 'BICOUSDT', 'AXSUSDT', 'IDUSDT', 'VIRTUALUSDT', 'REEFUSDT', 'BROCCOLIF3BUSDT', 'LOOMUSDT', 'CGPTUSDT', 'COWUSDT', 'SUIUSDT', 'STORJUSDT', 'PIPPINUSDT', 'MEMEUSDT', 'ARKMUSDT', 'SAGAUSDT', 'TRUUSDT', '1000RATSUSDT', 'CFXUSDT', 'BERAUSDT', 'CVXUSDT', 'SWELLUSDT', 'WIFUSDT', 'BAKEUSDT', 'UNIUSDT', 'LISTAUSDT', 'CELOUSDT', 'AIXBTUSDT', 'RENUSDT', 'SLERFUSDT', 'SPXUSDT', 'REZUSDT', 'LINAUSDT', 'JTOUSDT', 'NULSUSDT', 'PHAUSDT', 'NFPUSDT', 'RLCUSDT', 'FLMUSDT', 'VANRYUSDT', 'BANUSDT', 'CTSIUSDT', '1000XECUSDT', 'AKTUSDT', 'LAYERUSDT', 'CETUSUSDT', 'PENDLEUSDT', 'AVAUSDT', 'ANIMEUSDT', 'NEIROETHUSDT', 'GPSUSDT', '1000CHEEMSUSDT', 'BIDUSDT', 'USTCUSDT', 'HOOKUSDT', 'BMTUSDT', 'HOTUSDT', 'GLMRUSDT', 'KOMAUSDT', 'VVVUSDT', 'ANKRUSDT', 'SUPERUSDT', 'MOODENGUSDT', 'KNCUSDT', 'VINEUSDT', 'IMXUSDT', 'SUNUSDT', 'CELRUSDT', 'NTRNUSDT', 'MEUSDT', 'FLOWUSDT', 'FILUSDT', 'ENSUSDT', 'API3USDT', 'BEAMXUSDT', 'ACXUSDT', 'LINKUSDT', 'ZECUSDT', 'IOTXUSDT', 'BNTUSDT', 'KAITOUSDT', 'SYNUSDT', 'ZRXUSDT', 'HIFIUSDT', 'COTIUSDT', 'SANDUSDT', 'DOGEUSDT', 'THETAUSDT', 'MTLUSDT', 'SCRTUSDT', 'ORBSUSDT', 'OMGUSDT', 'BTCUSDT', 'NOTUSDT', 'IOSTUSDT', '1000BONKUSDT', 'STGUSDT', 'BRUSDT', 'BSWUSDT', 'MAVUSDT', 'ZETAUSDT', 'ORDIUSDT', 'GRIFFAINUSDT', 'DENTUSDT', 'SPELLUSDT', 'STRAXUSDT', 'INJUSDT', 'FORMUSDT', 'VIDTUSDT', 'EIGENUSDT', 'HIGHUSDT', '1000SHIBUSDT', 'BTCDOMUSDT', 'IOTAUSDT', 'EPICUSDT', 'OGNUSDT', 'DRIFTUSDT', 'FARTCOINUSDT', 'METISUSDT', 'MUBARAKUSDT', 'BROCCOLI714USDT', 'AIUSDT', 'REIUSDT', 'GRTUSDT', 'CHILLGUYUSDT', 'OMNIUSDT', 'DEGENUSDT', 'RAREUSDT', 'MOCAUSDT', 'HMSTRUSDT', 'CKBUSDT', 'TRBUSDT', 'TURBOUSDT', 'TIAUSDT', 'ZEREBROUSDT', 'GALAUSDT', 'BNXUSDT', 'BNBUSDT', 'WUSDT', 'ONEUSDT', 'COSUSDT', 'GASUSDT', 'THEUSDT', '1000XUSDT', 'PROMUSDT', 'PLUMEUSDT', 'FIDAUSDT', 'SKLUSDT', 'SUSHIUSDT', 'CHZUSDT', 'OCEANUSDT', 'BSVUSDT', 'COMPUSDT', 'AEVOUSDT', 'ATAUSDT', 'ENAUSDT', 'ZILUSDT', 'GRASSUSDT', '1000SATSUSDT', 'PYTHUSDT', 'TSTUSDT', 'RPLUSDT', 'BELUSDT', 'LQTYUSDT', 'DYMUSDT', 'NMRUSDT', 'DEGOUSDT', 'DFUSDT', 'GMXUSDT', 'KAVAUSDT', 'SFPUSDT', 'HIPPOUSDT', 'KASUSDT', 'AUCTIONUSDT', 'BADGERUSDT', 'VANAUSDT', 'MELANIAUSDT', 'IDEXUSDT', 'KEYUSDT', 'TOKENUSDT', 'RSRUSDT', 'NEIROUSDT', 'ALCHUSDT', 'DYDXUSDT', 'BLURUSDT', 'TLMUSDT', '1000WHYUSDT', 'LEVERUSDT', 'XAIUSDT', 'MEWUSDT', 'RENDERUSDT', 'DASHUSDT', 'BBUSDT', 'ETHWUSDT', 'DIAUSDT', 'CHESSUSDT', 'SWARMSUSDT', 'SANTOSUSDT', 'NKNUSDT', 'ACHUSDT', 'MKRUSDT', 'SXPUSDT', '1MBABYDOGEUSDT', '1000LUNCUSDT', 'UMAUSDT', 'RUNEUSDT', 'MAVIAUSDT', 'HEIUSDT', 'APEUSDT', 'DGBUSDT', 'ICXUSDT', 'GTCUSDT', 'ARUSDT', 'KDAUSDT', 'BCHUSDT', 'CRVUSDT', 'POPCATUSDT', 'QTUMUSDT', 'ICPUSDT', '1000CATUSDT', 'STPTUSDT', 'ETHFIUSDT', 'REDUSDT', 'LOKAUSDT', 'FETUSDT']

# Función para aplicar la estrategia
def aplicar_estrategia(df):

    # Calculamos las condiciones básicas
    cuerpo_pequeno = abs(df['close'] - df['open']) / (df['high'] - df['low']) < 0.3
    sombra_inferior_larga = (df['open'] - df['low']) > 2 * abs(df['close'] - df['open'])
    sombra_superior_corta = (df['high'] - df[['open', 'close']].max(axis=1)) < 0.3 * (df['high'] - df['low'])
    
    # Filtro de volumen (volumen de la vela debe ser mayor al promedio de las últimas 20 velas)
    df['volumen_promedio'] = df['volume'].rolling(window=20).mean()
    volumen_alto = df['volume'] > df['volumen_promedio']
    
    # Filtro de tendencia previa bajista (precio de cierre debe ser menor que la media móvil de 10 períodos)
    df['ema_10'] = df['close'].ewm(span=10, adjust=False).mean()
    tendencia_bajista = df['close'].shift(1) < df['ema_10'].shift(1)
    
    # Condición final para martillo alcista
    df['hammer'] = cuerpo_pequeno & sombra_inferior_larga & sombra_superior_corta & volumen_alto & tendencia_bajista
    
    # Condiciones para martillo invertido bajista
    sombra_superior_larga = (df['high'] - df['open']) > 2 * abs(df['close'] - df['open'])
    sombra_inferior_corta = (df[['open', 'close']].min(axis=1) - df['low']) < 0.3 * (df['high'] - df['low'])
    tendencia_alcista = df['close'].shift(1) > df['ema_10'].shift(1)
    df['inverted_hammer'] = cuerpo_pequeno & sombra_superior_larga & sombra_inferior_corta & volumen_alto & tendencia_alcista

    rsi = ta.rsi(df['close'], 14)
    atr = ta.atr(df['high'], df['low'], df['close'], 14)
    adx = ta.adx(df['high'], df['low'], df['close'], 14)    
    ema200 = ta.ema(df['close'], 100)
    ema50 = ta.ema(df['close'], 50)
    ema21 = ta.ema(df['close'], 21)
    ema9 = ta.ema(df['close'], 9)

    # Calcular el MACD
    """ macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
    df['macd'] = macd['MACD_12_26_9']
    df['macd_signal'] = macd['MACDs_12_26_9']
    df['macd_hist'] = macd['MACDh_12_26_9'] """
    

    df['adx'] = adx['ADX_14']
    df['plus_di'] = adx['DMP_14']
    df['minus_di'] = adx['DMN_14']
    df['longtakeprofit'] = df['close'] + atr * 2.0
    df['shorttakeprofit'] = df['close'] - atr * 2.0
    df['longstoploss'] = df['close'] - atr * 2.0
    df['shortstoploss'] = df['close'] + atr * 2.0
    
    df['rsi'] = rsi
    df['ema200'] = ema200
    df['ema50'] = ema50
    df['ema21'] = ema21
    df['ema9'] = ema9
    df['position'] = np.nan  # 1 = Long, -1 = Short, 0 = Flat
    df['take_profit'] = np.nan
    df['stop_loss'] = np.nan

    for i in range(1, len(df)):  # Comenzamos en 1 para evitar problemas con df.iloc[i-1]
        
        # if df['macd_hist'].iloc[i-1] > 0 and df['macd_hist'].iloc[i] < 0 and df['close'].iloc[i] < df['ema9'].iloc[i] and df['adx'].iloc[i] > 30 and df['plus_di'].iloc[i] < df['minus_di'].iloc[i] and df['adx'].iloc[i] > df['adx'].iloc[i-1] and df['ema21'].iloc[i] < df['ema21'].iloc[i-1] and df['ema9'].iloc[i] < df['ema9'].iloc[i-1] and df['ema9'].iloc[i] < df['ema21'].iloc[i]:

        # if df['macd_hist'].iloc[i-1] < 0 and df['macd_hist'].iloc[i] > 0 and df['close'].iloc[i] > df['ema9'].iloc[i] and df['adx'].iloc[i] > 30 and df['plus_di'].iloc[i] > df['minus_di'].iloc[i] and df['adx'].iloc[i] > df['adx'].iloc[i-1] and df['ema21'].iloc[i] > df['ema21'].iloc[i-1] and df['ema9'].iloc[i] > df['ema9'].iloc[i-1] and df['ema9'].iloc[i] > df['ema21'].iloc[i]:

        if (i > 0 and pd.notna(df['rsi'].iloc[i-1]) and pd.notna(df['rsi'].iloc[i]) and pd.notna(df['close'].iloc[i]) and pd.notna(df['ema200'].iloc[i]) and df['rsi'].iloc[i-1] < 33 and df['rsi'].iloc[i] > df['rsi'].iloc[i-1] and df['close'].iloc[i] > df['ema200'].iloc[i] ):
        # Ejecutar el código si los valores no son None

        
        # if df['rsi'].iloc[i-1] < 30 and df['rsi'].iloc[i] > df['rsi'].iloc[i-1] and df['close'].iloc[i] > df['ema200'].iloc[i]:
        # if df['rsi'].iloc[i-1] <= 27 and df['rsi'].iloc[i] > df['rsi'].iloc[i-1] and df['close'].iloc[i] > df['open'].iloc[i-1]:
        # if df['rsi'].iloc[i-1] <= 33 and df['rsi'].iloc[i] > df['rsi'].iloc[i-1]:
        # if df['rsi'].iloc[i-1] <= 32 and df['rsi'].iloc[i] > 32 and df['close'].iloc[i] > df['ema200'].iloc[i] :
        # if df['rsi'].iloc[i-1] <= 60 and df['rsi'].iloc[i] > 60 and df['adx'].iloc[i] > 30 and df['adx'].iloc[i] > df['adx'].iloc[i-1] and df['minus_di'].iloc[i] <= 15 and df['plus_di'].iloc[i] >= 30:
            if not np.isnan(df['close'].iloc[i]):
                df.at[i, 'position'] = 1
                df.at[i, 'take_profit'] = df.at[i, 'longtakeprofit']
                df.at[i, 'stop_loss'] = df.at[i, 'longstoploss']

        # elif df['macd_hist'].iloc[i-1] < 0 and df['macd_hist'].iloc[i] > 0 and df['close'].iloc[i] > df['ema9'].iloc[i] and df['adx'].iloc[i] > 30 and df['plus_di'].iloc[i] > df['minus_di'].iloc[i] and df['adx'].iloc[i] > df['adx'].iloc[i-1] and df['ema21'].iloc[i] > df['ema21'].iloc[i-1] and df['ema9'].iloc[i] > df['ema9'].iloc[i-1] and df['ema9'].iloc[i] > df['ema21'].iloc[i]:
        # elif df['macd_hist'].iloc[i-1] > 0 and df['macd_hist'].iloc[i] < 0 and df['close'].iloc[i] < df['ema9'].iloc[i] and df['adx'].iloc[i] > 30 and df['plus_di'].iloc[i] < df['minus_di'].iloc[i] and df['adx'].iloc[i] > df['adx'].iloc[i-1] and df['ema21'].iloc[i] < df['ema21'].iloc[i-1] and df['ema9'].iloc[i] < df['ema9'].iloc[i-1] and df['ema9'].iloc[i] < df['ema21'].iloc[i]:
        # elif df['rsi'].iloc[i-1] > 70 and df['rsi'].iloc[i] < df['rsi'].iloc[i-1] and df['close'].iloc[i] < df['ema200'].iloc[i]:
        elif (i > 0 and pd.notna(df['rsi'].iloc[i-1]) and pd.notna(df['rsi'].iloc[i]) and pd.notna(df['close'].iloc[i]) and pd.notna(df['ema200'].iloc[i]) and df['rsi'].iloc[i-1] > 67 and df['rsi'].iloc[i] < df['rsi'].iloc[i-1] and df['close'].iloc[i] < df['ema200'].iloc[i]):
        # elif df['rsi'].iloc[i-1] >= 77 and df['rsi'].iloc[i] < df['rsi'].iloc[i-1] and df['close'].iloc[i] < df['open'].iloc[i-1]:
        # elif df['rsi'].iloc[i-1] >= 67 and df['rsi'].iloc[i] < df['rsi'].iloc[i-1]:
        # elif df['rsi'].iloc[i-1] >= 68 and df['rsi'].iloc[i] < 68 and df['close'].iloc[i] < df['ema200'].iloc[i] :
        # elif df['rsi'].iloc[i-1] >= 40 and df['rsi'].iloc[i] < 40 and df['adx'].iloc[i] > 30 and df['adx'].iloc[i] > df['adx'].iloc[i-1] and df['minus_di'].iloc[i] >= 30 and df['plus_di'].iloc[i] <= 15:
            if not np.isnan(df['close'].iloc[i]):
                df.at[i, 'position'] = -1
                df.at[i, 'take_profit'] = df.at[i, 'shorttakeprofit']
                df.at[i, 'stop_loss'] = df.at[i, 'shortstoploss']
    
    return df


# Realizar backtest
def backtest(df):
    balance = 1000  # Balance inicial
    position = 0
    entry_price = 0
    trades = []  # Lista para almacenar las operaciones
    commission = 0.0005  # 0.05% de comisión
    
    for i in range(len(df)):
        if position == 0 and not np.isnan(df['position'].iloc[i]):
            # Abrir una nueva posición
            position = df['position'].iloc[i]
            entry_price = df['close'].iloc[i]
            
            # Aplicar la comisión del 0.05% al precio de entrada
            entry_price_with_commission = entry_price * (1 + commission) if position == 1 else entry_price * (1 - commission)
            
            take_profit = df['take_profit'].iloc[i]
            stop_loss = df['stop_loss'].iloc[i]
            open_time = df['timestamp'].iloc[i]

            # Asegúrate de que no haya valores NaN antes de añadir la operación
            if not np.isnan(entry_price) and not np.isnan(take_profit) and not np.isnan(stop_loss):
                trades.append({
                    'type': 'Long ' if position == 1 else 'Short',
                    'entry_time': open_time,
                    'entry_price': entry_price_with_commission,  # Precio de entrada con comisión
                    'take_profit': take_profit,
                    'stop_loss': stop_loss
                })
        
        elif position != 0:
            # Verificar si cerramos la posición en take profit o stop loss
            if position == 1:
                if df['close'].iloc[i] >= take_profit or df['close'].iloc[i] <= stop_loss:
                    # Cerrar la posición long
                    close_time = df['timestamp'].iloc[i]
                    close_price = df['close'].iloc[i]

                    # Aplicar la comisión del 0.05% al precio de salida
                    close_price_with_commission = close_price * (1 - commission)
                    
                    balance += (close_price_with_commission - entry_price_with_commission) * (balance / entry_price_with_commission)
                    trades[-1]['exit_time'] = close_time
                    trades[-1]['exit_price'] = close_price_with_commission  # Precio de salida con comisión
                    trades[-1]['profit'] = (close_price_with_commission - entry_price_with_commission) * (balance / entry_price_with_commission)
                    position = 0
            elif position == -1:
                if df['close'].iloc[i] <= take_profit or df['close'].iloc[i] >= stop_loss:
                    # Cerrar la posición short
                    close_time = df['timestamp'].iloc[i]
                    close_price = df['close'].iloc[i]

                    # Aplicar la comisión del 0.05% al precio de salida
                    close_price_with_commission = close_price * (1 + commission)
                    
                    balance += (entry_price_with_commission - close_price_with_commission) * (balance / entry_price_with_commission)
                    trades[-1]['exit_time'] = close_time
                    trades[-1]['exit_price'] = close_price_with_commission  # Precio de salida con comisión
                    trades[-1]['profit'] = (entry_price_with_commission - close_price_with_commission) * (balance / entry_price_with_commission)
                    position = 0
    
    return balance, trades

# Realizar backtest Hig Low
def backtesthl(df):
    balance = 1000  # Balance inicial
    position = 0
    entry_price = 0
    trades = []  # Lista para almacenar las operaciones
    commission = 0.0005  # 0.05% de comisión
    
    for i in range(len(df)):
        if position == 0 and not np.isnan(df['position'].iloc[i]):
            # Abrir una nueva posición
            position = df['position'].iloc[i]
            entry_price = df['close'].iloc[i]
            
            # Aplicar la comisión del 0.05% al precio de entrada
            entry_price_with_commission = entry_price * (1 + commission) if position == 1 else entry_price * (1 - commission)
            
            take_profit = df['take_profit'].iloc[i]
            stop_loss = df['stop_loss'].iloc[i]
            open_time = df['timestamp'].iloc[i]

            # Asegúrate de que no haya valores NaN antes de añadir la operación
            if not np.isnan(entry_price) and not np.isnan(take_profit) and not np.isnan(stop_loss):
                trades.append({
                    'type': 'Long ' if position == 1 else 'Short',
                    'entry_time': open_time,
                    'entry_price': entry_price_with_commission,  # Precio de entrada con comisión
                    'take_profit': take_profit,
                    'stop_loss': stop_loss
                })
        
        elif position != 0:
            # Verificar si cerramos la posición en take profit o stop loss
            if position == 1:
                if df['high'].iloc[i] >= take_profit:
                    # Cerrar la posición long
                    close_time = df['timestamp'].iloc[i]
                    close_price = df['high'].iloc[i]

                    # Aplicar la comisión del 0.05% al precio de salida
                    close_price_with_commission = close_price * (1 - commission)
                    
                    balance += (close_price_with_commission - entry_price_with_commission) * (balance / entry_price_with_commission)
                    trades[-1]['exit_time'] = close_time
                    trades[-1]['exit_price'] = close_price_with_commission  # Precio de salida con comisión
                    trades[-1]['profit'] = (close_price_with_commission - entry_price_with_commission) * (balance / entry_price_with_commission)
                    position = 0

                elif df['low'].iloc[i] <= stop_loss:
                    # Cerrar la posición long
                    close_time = df['timestamp'].iloc[i]
                    close_price = df['low'].iloc[i]

                    # Aplicar la comisión del 0.05% al precio de salida
                    close_price_with_commission = close_price * (1 - commission)
                    
                    balance += (close_price_with_commission - entry_price_with_commission) * (balance / entry_price_with_commission)
                    trades[-1]['exit_time'] = close_time
                    trades[-1]['exit_price'] = close_price_with_commission  # Precio de salida con comisión
                    trades[-1]['profit'] = (close_price_with_commission - entry_price_with_commission) * (balance / entry_price_with_commission)
                    position = 0

            elif position == -1:
                if df['low'].iloc[i] <= take_profit:
                    # Cerrar la posición short
                    close_time = df['timestamp'].iloc[i]
                    close_price = df['low'].iloc[i]

                    # Aplicar la comisión del 0.05% al precio de salida
                    close_price_with_commission = close_price * (1 + commission)
                    
                    balance += (entry_price_with_commission - close_price_with_commission) * (balance / entry_price_with_commission)
                    trades[-1]['exit_time'] = close_time
                    trades[-1]['exit_price'] = close_price_with_commission  # Precio de salida con comisión
                    trades[-1]['profit'] = (entry_price_with_commission - close_price_with_commission) * (balance / entry_price_with_commission)
                    position = 0

                elif df['high'].iloc[i] >= stop_loss:
                    # Cerrar la posición short
                    close_time = df['timestamp'].iloc[i]
                    close_price = df['high'].iloc[i]

                    # Aplicar la comisión del 0.05% al precio de salida
                    close_price_with_commission = close_price * (1 + commission)
                    
                    balance += (entry_price_with_commission - close_price_with_commission) * (balance / entry_price_with_commission)
                    trades[-1]['exit_time'] = close_time
                    trades[-1]['exit_price'] = close_price_with_commission  # Precio de salida con comisión
                    trades[-1]['profit'] = (entry_price_with_commission - close_price_with_commission) * (balance / entry_price_with_commission)
                    position = 0
    
    return balance, trades

def process_symbol(symbol):
    global timeframe

    long_positivos = 0
    long_negativos = 0
    short_positivos = 0
    short_negativos = 0

    long_positivoshl = 0
    long_negativoshl = 0
    short_positivoshl = 0
    short_negativoshl = 0

    print(f'Analizando la cripto: {symbol}...')

    # Obtener datos y aplicar la estrategia
    
    data = databacktesting(symbol, timeframe)  # Asegúrate de obtener los datos correctamente
    if isinstance(data, tuple):
        df, _ = data
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data
    df = aplicar_estrategia(df)

    balance_final, trades = backtest(df)
    balance_finalhl, tradeshl = backtesthl(df)

    for operacion in trades:
        if operacion["type"] == "Long ":
            profit = operacion.get("profit")
            if profit is not None:
                if operacion.get("profit") > 0:
                    long_positivos += 1
                else:
                    long_negativos += 1
        elif operacion["type"] == "Short":
            profit = operacion.get("profit")
            if profit is not None:
                if operacion.get("profit") > 0:
                    short_positivos += 1
                else:
                    short_negativos += 1
    totalgeneralganados = (long_positivos + short_positivos - (short_negativos + long_negativos))
    """ totalganados = (long_positivos + short_positivos)
    totalperdidos = (short_negativos + long_negativos) """

    for operacionhl in tradeshl:
        if operacionhl["type"] == "Long ":
            profit = operacionhl.get("profit")
            if profit is not None:
                if operacionhl.get("profit") > 0:
                    long_positivoshl += 1
                else:
                    long_negativoshl += 1
        elif operacionhl["type"] == "Short":
            profit = operacionhl.get("profit")
            if profit is not None:
                if operacionhl.get("profit") > 0:
                    short_positivoshl += 1
                else:
                    short_negativoshl += 1
    totalgeneralganadoshl = (long_positivoshl + short_positivoshl - (short_negativoshl + long_negativoshl))
    totalganadoshl = (long_positivoshl + short_positivoshl)
    totalperdidoshl = (short_negativoshl + long_negativoshl)

    return symbol, balance_final, totalgeneralganados, balance_finalhl, totalgeneralganadoshl, totalganadoshl, totalperdidoshl

if __name__ == "__main__":
    profits, profitshl = [], []
    selected_cryptos = []  # Lista para criptos con 4 o más victorias y saldo superior a 1030
    listofsymbol = []
    
    # Variables para balance y operaciones de ambas estrategias
    total_balance_base = 0
    total_balance_hl = 0
    total_wins_base = 0
    total_losses_base = 0
    total_wins_hl = 0
    total_losses_hl = 0
    totalganadoshl = 0
    totalperdidoshl = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_symbol, symbol) for symbol in symbols]
        for future in as_completed(futures):
            result = future.result()
            if result:
                symbol, balance_final_base, totalgeneralganados_base, balance_final_hl, totalgeneralganados_hl, ganadoshl, perdidoshl = result

                # Acumular balance total por estrategia
                total_balance_base += balance_final_base
                total_balance_hl += balance_final_hl

                # Contar operaciones ganadoras y perdedoras - Estrategia Base
                if totalgeneralganados_base > 0:
                    total_wins_base += totalgeneralganados_base
                else:
                    total_losses_base += abs(totalgeneralganados_base)

                # Contar operaciones ganadoras y perdedoras - Estrategia High-Low
                if totalgeneralganados_hl > 0:
                    total_wins_hl += totalgeneralganados_hl
                else:
                    total_losses_hl += abs(totalgeneralganados_hl)

                # Acumular ganados y perdidos para High-Low
                totalganadoshl += ganadoshl
                totalperdidoshl += perdidoshl

                # Guardar criptos con balances destacados
                profits.append((symbol, balance_final_base, totalgeneralganados_base))
                profitshl.append((symbol, balance_final_hl, totalgeneralganados_hl))

                """ if balance_final_base >= 1100 or balance_final_base <= 850:
                    profits.append((symbol, balance_final_base, totalgeneralganados_base))
                if balance_final_hl >= 1100 or balance_final_hl <= 850:
                    profitshl.append((symbol, balance_final_hl, totalgeneralganados_hl)) """

                # Ordenar por balance final
                """ profits_sorted = sorted(profits, key=lambda x: x[1], reverse=True)
                profits_sortedhl = sorted(profitshl, key=lambda x: x[1], reverse=True) """

                # Agregar a la lista de criptos seleccionadas
                """ if totalgeneralganados_base >= 4 and balance_final_base > 1030:
                    selected_cryptos.append((symbol, balance_final_base, totalgeneralganados_base)) """
                if totalgeneralganados_hl >= 3 and balance_final_hl > 1030:
                    selected_cryptos.append((symbol, balance_final_hl, totalgeneralganados_hl))

                if totalgeneralganados_hl >= 3 and balance_final_hl > 1030:
                    listofsymbol.append((symbol))

    # Ordenar por ganados y perdidos
    profits_sorted = sorted(profits, key=lambda x: x[2], reverse=True)
    profits_sortedhl = sorted(profitshl, key=lambda x: x[2], reverse=True)

    print()
    print(f"Resultados del Backtest {timeframe}")
    print("-" * 100)
    
    # Imprimir resultados detallados
    if profits_sorted and profits_sortedhl:
        for (symbol1, profit1, totalgeneralganados1), (symbol2, profit2, totalgeneralganados2) in zip(profits_sorted, profits_sortedhl):
            print(f"{symbol1:<20} {profit1:<20.2f} {totalgeneralganados1:<10} {symbol2 :<20} HL {profit2:<20.2f} {totalgeneralganados2:<10}")

    print("\nResumen General del Backtest")
    print("-" * 80)
    print(f"Balance Total (Estrategia Base): {total_balance_base:.2f} USDT")
    print(f"Balance Total (High-Low): {total_balance_hl:.2f} USDT")
    print(f"Operaciones Ganadoras (Estrategia Base): {total_wins_base}")
    print(f"Operaciones Perdedoras (Estrategia Base): {total_losses_base}")
    print(f"Operaciones Ganadoras (High-Low): {total_wins_hl}")
    print(f"Operaciones Perdedoras (High-Low): {total_losses_hl}")
    print(f"Total Ganadas : {totalganadoshl}")
    print(f"Total Perdidas: {totalperdidoshl}")

    # Imprimir criptos seleccionadas
    print("\nCriptomonedas con 4 o más victorias y saldo superior a 1030:")
    print("-" * 80)
    for symbol, balance, wins in selected_cryptos:
        print(f"{symbol:<20} {balance:<20.2f} {wins:<10}")

    print(listofsymbol)

