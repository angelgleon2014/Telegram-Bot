# import logging
# from unittest import result
# from tkinter.tix import Tree
from goto import with_goto
from goto import goto, label
import config, logging, os.path
from binance.client import Client
from binance.futures import Futures as ClientFutures
from pandas import DataFrame
# from pandas_ta import adx, rsi, ema, atr, cdl_inside, cdl_doji
from pandas_ta import adx, rsi, atr, sma, bbands, macd, cdl_inside, cdl_doji, ema
import pandas as pd
import numpy as np
import pytz
import pandas_ta as ta
# from numpy import item
client = Client(config.API_KEY, config.API_SECRET, tld='com')
clientfutures = ClientFutures(config.API_KEY, config.API_SECRET, base_url="https://fapi.binance.com")
# logging.basicConfig(level=logging.DEBUG,filename='C:\\Users\\Angel Leon Alvarez\\PycharmProjects\\botautomaticofuturos\\previuscheck.log')  # ruta windows
logging.basicConfig(level=logging.ERROR,filename='/home/angel/Documentos/botscalping/newcheck.log')  # ruta linux
logging.basicConfig(level=logging.ERROR,filename='newcheck.log')  # ruta linux
import os

#__________________Funcion para ver el cambio de las ultimas 24h _____________________________________

def change24h(symbol):
    try:
        change24h = clientfutures.ticker_24hr_price_change(symbol=symbol)
        lst = list(change24h.values())
        change = float(lst[2])
        changeconsult = True
        return change, changeconsult
    except Exception as error:
        change = 0
        changeconsult = False
        return change, changeconsult
        
# print(change24h("KNCUSDT")[0])
# change24 = float(change24h("KNCUSDT")[0])
# print(type(change24))
# if change24 < 5 and change24 > -5:
  #   print("dentro de rango")
# else:
    # print("fuera de rango")

#__________________Funcion para tener una sola vez la info del exchange _________________________________

def exchangeinfo():
    global client
    try:
        # client = Client(API_KEY, API_SECRET, tld='com')
        lista = client.futures_exchange_info()
        # print(lista)
        return lista
    except Exception as error:

        # print(error)
        pass
# print(exchangeinfo())

#__________________Funcion para la precision de los decimales de las monedas______________________________
def precision(symbol):
    
    # print(lista)
    # lista = client.futures_exchange_info()
    # lista = client.get_exchange_info()
    lista = exchangeinfo()
    # print(lista)
    cont = 0
    try: 
        while True:
            
            if lista['symbols'][cont]['symbol'] == symbol:
                # pass
                # print(lista['symbols'][cont]['symbol'])
                quantityPrecisiondef = lista['symbols'][cont]['quantityPrecision']
                priceprecisiondef = lista['symbols'][cont]['pricePrecision']
                # print("quantityPrecisiondef ",quantityPrecisiondef)
                # print("priceprecisiondef ", priceprecisiondef)
                # cont = 0
                return quantityPrecisiondef, priceprecisiondef
                # break
            cont += 1
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetprecision.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        return 0,0
        # print(error)

print(precision('YFIUSDT'))
#___________________________________________________ DATA ____________________________________________#
@with_goto
def data(symbol, temporality, cross):
    lcloseprice, lopenprice = [], []
    lhighprice, llowprice = [], []
    # global dfc, dfh, dfl
    # while True:
    try:
        if cross is True:
            label .datam
            if temporality == '1m':
                # print(symbol)
                # print(temporality)
                # print(cross)
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, '250 minute ago UTC')
                # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, '10080 minute ago UTC')
                # print("Len de data_hist ",len(data_historical))
                # label .data3m
            if temporality == '3m':
                # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '3750 minute ago UTC')
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '1500 minute ago UTC')
            if temporality == '5m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_5MINUTE, '3750 minute ago UTC')
                # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_5MINUTE, '2500 minute ago UTC')
            if temporality == '15m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, '7500 minute ago UTC')
            if temporality == '30m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_30MINUTE, '15000 minute ago UTC')

            if temporality == '1h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1HOUR, '500 hour ago UTC')
            if temporality == '2h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_2HOUR, '1000 hour ago UTC')
            if temporality == '4h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_4HOUR, '2000 hour ago UTC')
            if temporality == '6h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_6HOUR, '3000 hour ago UTC')
            if temporality == '8h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_8HOUR, '4000 hour ago UTC')
            if temporality == '12h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_12HOUR, '6000 hour ago UTC')
            if temporality == '1D':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1DAY, '250 day ago UTC')
            # print(len(data_historical))
            columns = ['Open time', 'open', 'high','low', 'close', 'volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore' ]
            df = pd.DataFrame(data_historical, columns=columns)
            # print(df)
            df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
            df.set_index('Open time', inplace=True)
            # print(type(df))
            # print(df)
            # print(type(data_historical))
            # print(data_historical)
            # print(len(data_historical))
            if len(data_historical) != 750:
                # print("data INCOMPLETA")
                goto .datam
                datacomplete = False
                return 0, 0, 0, 0, datacomplete, 0, 0, 0, 0,0,0,0,0,0
                
            # if len(data_historical) == 250:
            # if len(data_historical) == 250 or len(data_historical) != 250 :
            if len(data_historical) == 750:
                # print("DATA COMPLETA")
                for i in range(len(data_historical)):
                    lopenprice.append(float(data_historical[i][1]))
                    lhighprice.append(float(data_historical[i][2]))
                    llowprice.append(float(data_historical[i][3]))
                    lcloseprice.append(float(data_historical[i][4]))
                antclose = lcloseprice[-4]
                anthigh  = lhighprice[-4]
                antlow   = llowprice[-4]
                antopen = lopenprice[-4]
                close    = lcloseprice[-2]
                penclose = lcloseprice[-3]
                penhigh  = lhighprice[-3]
                penlow   = llowprice[-3]
                penopen  = lopenprice[-3]
                dic_lpo = {"Open": lopenprice}
                dic_lph = {"High": lhighprice}
                dic_lpl = {"Low": llowprice}
                dic_lpc = {"Close": lcloseprice}     

                odf = DataFrame(dic_lpo)
                dfo = odf.get('Open')
                
                cdf = DataFrame(dic_lpc)
                # print(type(cdf))
                dfc = cdf.get('Close')
                # print(dfc)
                # print(type(dfc))

                hdf = DataFrame(dic_lph)
                dfh = hdf.get('High')

                ldf = DataFrame(dic_lpl)
                dfl = ldf.get('Low')
                # print("El len de data dentro del si es: ", len(data_historical))
                # print(type(dfl))
                datacomplete = True
                # return dfc, dfh, dfl, dfo, datacomplete, penclose, penhigh, penlow, penopen, antclose, anthigh, antlow, antopen, lcloseprice
                return dfc, dfh, dfl, penclose, close, datacomplete
            else:
                datacomplete = False
                # print("entro en el primer else")
                # return datacomplete
                return 0, 0, 0, 0, datacomplete, 0, 0, 0, 0,0,0,0,0,0
                # print("El len de data dentro del else es: ", len(data_historical))
                # return len(data_historical)
        else:
            # print ("entro en else")
            label .data
            if temporality == '1m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, '5 minute ago UTC')
                # print("Len de data_hist ",len(data_historical))
            if temporality == '3m':
                # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '2250 minute ago UTC')
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '750 minute ago UTC')
            if temporality == '5m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_5MINUTE, '1250 minute ago UTC')
            if temporality == '15m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, '11250 minute ago UTC')
            if temporality == '30m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_30MINUTE, '7500 minute ago UTC')

            if temporality == '1h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1HOUR, '250 hour ago UTC')
            if temporality == '2h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_2HOUR, '500 hour ago UTC')
            if temporality == '4h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_4HOUR, '1000 hour ago UTC')
            if temporality == '6h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_6HOUR, '1500 hour ago UTC')
            if temporality == '8h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_8HOUR, '2000 hour ago UTC')
            if temporality == '12h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_12HOUR, '3000 hour ago UTC')
            if temporality == '1D':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1DAY, '250 day ago UTC')
            # print(len(data_historical))
            if len(data_historical) != 250:
                # print("data incompleta")
                # goto .data
                pass
            # if len(data_historical) == 250:
            if len(data_historical) == 250 or len(data_historical) == 249:
                # print("DATA COMPLETA")
                for i in range(len(data_historical)):
                    lopenprice.append(float(data_historical[i][1]))
                    lhighprice.append(float(data_historical[i][2]))
                    llowprice.append(float(data_historical[i][3]))
                    lcloseprice.append(float(data_historical[i][4]))
                antclose = lcloseprice[-4]
                anthigh  = lhighprice[-4]
                antlow   = llowprice[-4]
                antopen = lopenprice[-4]
                penclose = lcloseprice[-3]
                penhigh  = lhighprice[-3]
                penlow   = llowprice[-3]
                penopen  = lopenprice[-3]
                dic_lpo = {"Open": lopenprice}
                dic_lph = {"High": lhighprice}
                dic_lpl = {"Low": llowprice}
                dic_lpc = {"Close": lcloseprice}     

                odf = DataFrame(dic_lpo)
                dfo = odf.get('Open')
                
                cdf = DataFrame(dic_lpc)
                # print(type(cdf))
                dfc = cdf.get('Close')
                # print(dfc)
                # print(type(dfc))

                hdf = DataFrame(dic_lph)
                dfh = hdf.get('High')

                ldf = DataFrame(dic_lpl)
                dfl = ldf.get('Low')
                # print("El len de data dentro del si es: ", len(data_historical))
                # print(type(dfl))
                datacomplete = True
                return dfc, dfh, dfl, dfo, datacomplete, penclose, penhigh, penlow, penopen, antclose, anthigh, antlow, antopen, lcloseprice
                # return dfc
            else:
                datacomplete = False
                print("entro en el segundo else")
                return 0, 0, 0, 0, datacomplete, 0, 0, 0, 0,0,0,0,0,0
            
                # print("El len de data dentro del else es: ", len(data_historical))
                # return len(data_historical)
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetdata.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        datacomplete = False
        # print(error)
        print(f'entro en el error')
        # return 0, 0, 0, 0, False, 0
        return 0, 0, 0, 0, datacomplete, 0, 0, 0, 0,0,0,0,0,0
""" dflow = (data('ETHUSDT', '1m', True))[0] 
print(type(dflow))
print(dflow) """
# print(type(data('ETHUSDT', '5m'))[0])
# print(data('FIOUSDT', '4h', True))
#___________________________________________________ DATA2 ____________________________________________#
@with_goto
def data2(symbol, temporality, cross):
    lcloseprice, lopenprice = [], []
    lhighprice, llowprice = [], []
    # global dfc, dfh, dfl
    # while True:
    try:
        if cross is True:
            label .data2
            if temporality == '1m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, '100 minute ago UTC')
                # print("Len de data_hist ",len(data_historical))
                # label .data3m
            if temporality == '3m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '2250 minute ago UTC')
                #data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '750 minute ago UTC')
            if temporality == '5m':
                # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_5MINUTE, '3750 minute ago UTC')
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_5MINUTE, '3750 minute ago UTC')
            if temporality == '15m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, '11250 minute ago UTC')
            if temporality == '30m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_30MINUTE, '7500 minute ago UTC')

            if temporality == '1h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1HOUR, '250 hour ago UTC')
            if temporality == '2h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_2HOUR, '500 hour ago UTC')
            if temporality == '4h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_4HOUR, '1000 hour ago UTC')
            if temporality == '6h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_6HOUR, '1500 hour ago UTC')
            if temporality == '8h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_8HOUR, '2000 hour ago UTC')
            if temporality == '12h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_12HOUR, '3000 hour ago UTC')
            if temporality == '1D':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1DAY, '250 day ago UTC')
            # print(len(data_historical))
            if len(data_historical) != 250:
                # print("data incompleta")
                # goto .data2
                pass
            if len(data_historical) == 250:
            # if len(data_historical) == 250 or len(data_historical) != 250:
                # print("DATA COMPLETA")
                for i in range(len(data_historical)):
                    lopenprice.append(float(data_historical[i][1]))
                    lhighprice.append(float(data_historical[i][2]))
                    llowprice.append(float(data_historical[i][3]))
                    lcloseprice.append(float(data_historical[i][4]))
                antclose = lcloseprice[-4]
                anthigh  = lhighprice[-4]
                antlow   = llowprice[-4]
                antopen = lopenprice[-4]
                penclose = lcloseprice[-3]
                penhigh  = lhighprice[-3]
                penlow   = llowprice[-3]
                penopen  = lopenprice[-3]
                close2 = lcloseprice[-2]
                dic_lpo = {"Open": lopenprice}
                dic_lph = {"High": lhighprice}
                dic_lpl = {"Low": llowprice}
                dic_lpc = {"Close": lcloseprice}     

                odf = DataFrame(dic_lpo)
                dfo = odf.get('Open')
                
                cdf = DataFrame(dic_lpc)
                # print(type(cdf))
                dfc = cdf.get('Close')
                # print(dfc)
                # print(type(dfc))

                hdf = DataFrame(dic_lph)
                dfh = hdf.get('High')

                ldf = DataFrame(dic_lpl)
                dfl = ldf.get('Low')
                # print("El len de data dentro del si es: ", len(data_historical))
                # print(type(dfl))
                datacomplete2 = True
                return dfc, dfh, dfl, dfo, datacomplete2, penclose, penhigh, penlow, penopen, antclose, anthigh, antlow, antopen, lcloseprice, close2
                # return dfc
            else:
                datacomplete = False
                return 0, 0, 0, 0, datacomplete, 0, 0, 0, 0,0,0,0,0,0,0
                # print("El len de data dentro del else es: ", len(data_historical))
                # return len(data_historical)
        else:
            label .data
            if temporality == '1m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, '750 minute ago UTC')
                # print("Len de data_hist ",len(data_historical))
            if temporality == '3m':
                # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '2250 minute ago UTC')
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '750 minute ago UTC')
            if temporality == '5m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_5MINUTE, '3750 minute ago UTC')
            if temporality == '15m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, '11250 minute ago UTC')
            if temporality == '30m':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_30MINUTE, '7500 minute ago UTC')

            if temporality == '1h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1HOUR, '250 hour ago UTC')
            if temporality == '2h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_2HOUR, '500 hour ago UTC')
            if temporality == '4h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_4HOUR, '1000 hour ago UTC')
            if temporality == '6h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_6HOUR, '1500 hour ago UTC')
            if temporality == '8h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_8HOUR, '2000 hour ago UTC')
            if temporality == '12h':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_12HOUR, '3000 hour ago UTC')
            if temporality == '1D':
                data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1DAY, '250 day ago UTC')
            # print(len(data_historical))
            if len(data_historical) != 750:
                # print("data incompleta")
                # goto .data
                pass
            if len(data_historical) == 750:
                # print("DATA COMPLETA")
                for i in range(len(data_historical)):
                    lopenprice.append(float(data_historical[i][1]))
                    lhighprice.append(float(data_historical[i][2]))
                    llowprice.append(float(data_historical[i][3]))
                    lcloseprice.append(float(data_historical[i][4]))
                antclose = lcloseprice[-4]
                anthigh  = lhighprice[-4]
                antlow   = llowprice[-4]
                antopen = lopenprice[-4]
                penclose = lcloseprice[-3]
                penhigh  = lhighprice[-3]
                penlow   = llowprice[-3]
                penopen  = lopenprice[-3]
                dic_lpo = {"Open": lopenprice}
                dic_lph = {"High": lhighprice}
                dic_lpl = {"Low": llowprice}
                dic_lpc = {"Close": lcloseprice}     

                odf = DataFrame(dic_lpo)
                dfo = odf.get('Open')
                
                cdf = DataFrame(dic_lpc)
                # print(type(cdf))
                dfc = cdf.get('Close')
                # print(dfc)
                # print(type(dfc))

                hdf = DataFrame(dic_lph)
                dfh = hdf.get('High')

                ldf = DataFrame(dic_lpl)
                dfl = ldf.get('Low')
                # print("El len de data dentro del si es: ", len(data_historical))
                # print(type(dfl))
                datacomplete = True
                return dfc, dfh, dfl, dfo, datacomplete, penclose, penhigh, penlow, penopen, antclose, anthigh, antlow, antopen, lcloseprice
                # return dfc
            else:
                datacomplete = False
                return 0, 0, 0, 0, datacomplete, 0, 0, 0, 0,0,0,0,0,0
                # print("El len de data dentro del else es: ", len(data_historical))
                # return len(data_historical)
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetdata.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        datacomplete = False
        # print(error)
        # return 0, 0, 0, 0, False, 0
        return 0, 0, 0, 0, datacomplete, 0, 0, 0, 0,0,0,0,0,0
""" dflow = (data('ETHUSDT', '1m', True))[0] 
print(type(dflow))
print(dflow) """
# print(type(data('ETHUSDT', '5m'))[0])
# print(data('BLZUSDT', '5m')[5])

#______________________________SMA delRsi___________________________________#
def SimpleMovingAverage(rsisma):
    try:

        # print(rsisma)
        # print(type(rsisma))
        # getrsisma = rsisma.get()
        # print(getrsisma)
        # print(type(getrsisma))
        sma14 = sma(rsisma, 14).iloc[-2]
        # print(type(sma14))
        # print("sma14 ",sma14)
        fsma14 = sma14.item()
        # print(type(fsma14))
        # print("fsma14 ",fsma14)
        psma14 = sma(rsisma, 14).iloc[-3]
        # print(psma14)
        pfsma14 = psma14.item()
        # print(pfsma14)
        return round(fsma14,2), round(pfsma14,2)
        # return round(fresultsrsipen,2), round(fresultsrsi,2)
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetrsisma.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        # print(error)
        return 0, 0

""" resultsdata = data("YFIUSDT", "3m", False)
dfc = resultsdata[0]
# dfh = resultsdata[1]
# dfl = resultsdata[2]
# dfo = resultsdata[3]

print(SimpleMovingAverage(dfc)) """

#___________________________________________________________________________#

#_______________________________________________ CDL INSIDE ________________________________________#
""" def candleinside2(dfc, dfh, dfl, dfo):

    resultcandleinside = cdl_inside(dfo, dfh, dfl, dfc)
    return resultcandleinside

resultsdata = data("BELUSDT", "1h")
dfc = resultsdata[0]
dfh = resultsdata[1]
dfl = resultsdata[2]
dfo = resultsdata[3]

print(candleinside2(dfo, dfh, dfl, dfc)) """


def candleinside(dfc, dfh, dfl, dfo):

    # resultcandledoji = cdl_doji(dfo, dfh, dfl, dfc)
    try:
        resultcandleinside = cdl_inside(dfo, dfh, dfl, dfc).iloc[-2]
        # resultsatr = atr(dfh, dfl, dfc).iloc[-3]
        fresultcandleinside = resultcandleinside.item()
        return fresultcandleinside
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetcandleinside.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        # print(error)
        return 0
    # return resultcandledoji

""" resultsdata = data("BELUSDT", "1h")
dfc = resultsdata[0]
dfh = resultsdata[1]
dfl = resultsdata[2]
dfo = resultsdata[3]

# print(candledoji(dfo, dfh, dfl, dfc))
inside = candleinside(dfo, dfh, dfl, dfc)
print(type(inside))
print(inside) """

""" resultsdata = data("ARUSDT", "15m")
dfc = resultsdata[0]
dfh = resultsdata[1]
dfl = resultsdata[2]
dfo = resultsdata[3]

print(candleinside(dfo, dfh, dfl, dfc)) """

#_______________________________________________ CDL DOJI ________________________________________#
""" def candledoji2(dfc, dfh, dfl, dfo):

    resultcandledoji = cdl_doji(dfo, dfh, dfl, dfc)
    return resultcandledoji

resultsdata = data("ICPUSDT", "3m")
dfc = resultsdata[0]
dfh = resultsdata[1]
dfl = resultsdata[2]
dfo = resultsdata[3]

print(candledoji2(dfo, dfh, dfl, dfc)) """


def candledoji(dfc, dfh, dfl, dfo):

    # resultcandledoji = cdl_doji(dfo, dfh, dfl, dfc)
    try:
        resultcandledoji = cdl_doji(dfo, dfh, dfl, dfc).iloc[-2]
        # resultsatr = atr(dfh, dfl, dfc).iloc[-3]
        fresultcandledoji = resultcandledoji.item()
        return fresultcandledoji
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetcandledoji.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        # print(error)
        return 0
    # return resultcandledoji

""" resultsdata = data("OGNUSDT", "3m")
dfc = resultsdata[0]
dfh = resultsdata[1]
dfl = resultsdata[2]
dfo = resultsdata[3]

# print(candledoji(dfo, dfh, dfl, dfc))
doji = candledoji(dfo, dfh, dfl, dfc)
print(type(doji))
print(doji) """

#___________________________________________________ ATR ____________________________________________#

# def atrindicator(dfc, dfh, dfl)
""" @with_goto
def indicatoratr(dfc, dfh, dfl):
    try:
        label .dataatr
        # priresultsatr = atr(dfh, dfl, dfc).iloc[-2]
        resultsatr = atr(dfh, dfl, dfc).iloc[-2]
        fresultsatr = resultsatr.item()

        penresultsatr = atr(dfh, dfl, dfc).iloc[-3]
        penfresultsatr = penresultsatr.item()
        # prifresultsatr = priresultsatr.item()
        # return fresultsatr, prifresultsatr
        # return fresultsatr, penfresultsatr
        if fresultsatr is None or fresultsatr == 0:
            goto .dataatr
        else:
            return fresultsatr
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetatr.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        print(error)
        # goto .dataatr
        return 0, 0 """


def indicatoratr(dfc, dfh, dfl):
    try:
        
        # priresultsatr = atr(dfh, dfl, dfc).iloc[-2]
        resultsatr = atr(dfh, dfl, dfc).iloc[-1]
        fresultsatr = resultsatr.item()

        penresultsatr = atr(dfh, dfl, dfc).iloc[-3]
        penfresultsatr = penresultsatr.item()
        # prifresultsatr = priresultsatr.item()
        # return fresultsatr, prifresultsatr
        # return fresultsatr, penfresultsatr
        
        # return fresultsatr, penfresultsatr
        return fresultsatr
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetatr.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        # print(error)
        # goto .dataatr
        return 0, 0

""" resultsdata = data("NEIROETHUSDT", "1m", True)
dfc = resultsdata[0]
dfh = resultsdata[1]
dfl = resultsdata[2]
dfo = resultsdata[3]
close = resultsdata[4]
penclose = resultsdata[3]
atrvalor = indicatoratr(dfc, dfh, dfl)
priatr = atrvalor[0]
secatr = atrvalor[1] """
""" print("pri atr ", priatr)
print("sec atr ", secatr) """

""" resultsdata = data("RLCUSDT", "3m", False)
dfc = resultsdata[0]
dfh = resultsdata[1]
dfl = resultsdata[2]
dfo = resultsdata[3]
atrvalor = indicatoratr(dfc, dfh, dfl)

print("pri atr ", atrvalor) """


""" shortstoploss = round((close + priatr * 1.5), 4)
penshortstoploss = round((penclose + secatr * 1.5), 4)
penlongsstoploss = round((penclose - secatr * 1.5), 4)
shorttakeprofit = round((close - priatr * 1.5), 4)
longtakeprofit = round((close + priatr * 1.5), 4)
print("close ", close)
print("shortstoploss        ", shortstoploss)
print("pen shortstoploss    ", penshortstoploss)
print("shortstakeprofit     ", shorttakeprofit) """

""" lastpriceTPdistance = round((close - longtakeprofit) / longtakeprofit * 100, 3)
penpriceSLdistance  = round((penultimeCloseDiv - penlongsstoploss) / penlongsstoploss * 100, 3)
positiveTPpriceDistance = lastpriceTPdistance * -1 """

""" lastpriceTPdistance = round((close - shorttakeprofit) / shorttakeprofit * 100, 4)
penpriceSLdistance  = round((penshortstoploss - penclose) / penclose * 100, 4)
positiveTPpriceDistance = lastpriceTPdistance * -1 """

""" lastpriceTPdistance = round((longtakeprofit - close) / close * 100, 3)
penpriceSLdistance  = round((penclose - penlongsstoploss) / penlongsstoploss * 100, 3)

print("lastpriceTPdistance      ", lastpriceTPdistance)
print("penpriceSLdistance       ", penpriceSLdistance) """
# print("positiveTPpriceDistance  ", positiveTPpriceDistance)
# print(indicatoratr(dfc))

#___________________________________________________ EMA _____________________________________________#

# def ExponentialMovingAverage(symbol, temporality):
""" def ExponentialMovingAverage(dfc):
    # lhighprice, lopenprice, llowprice = [], [], []
    # lcloseprice = []
    # global dfc
    print("dentro", dfc)
    try:
        
        # ema16 = ema(dfc, 16).iloc[-2]
        # ema160 = ema(dfc, 160).iloc[-2]
        # ema96 = ema(dfc, 96).iloc[-2]
        # fema96 = ema96.item()
        # fema16 = ema16.item()
        # fema160 = ema160.item()
        ema20 = ema(dfc, 20).iloc[-2]
        fema20 = ema20.item()
        pema20 = ema(dfc, 20).iloc[-3]
        pfema20 = pema20.item()
        uema20 = ema(dfc, 20).iloc[-8]
        ufema20 = uema20.item()

        ema400 = ema(dfc, 400).iloc[-2]
        fema400 = ema400.item()
        pema400 = ema(dfc, 400).iloc[-3]
        pfema400 = pema400.item()

        ema100 = ema(dfc, 100).iloc[-2]
        fema100 = ema100.item()
        pema100 = ema(dfc, 100).iloc[-3]
        pfema100 = pema100.item()
        uema100 = ema(dfc, 100).iloc[-8]
        ufema100 = uema100.item()

        ema200 = ema(dfc, 200).iloc[-2]
        fema200 = ema200.item()
        pema200 = ema(dfc, 200).iloc[-3]
        pfema200 = pema200.item()

        ema50 = ema(dfc, 50).iloc[-2]
        fema50 = ema50.item()
        pema50 = ema(dfc, 50).iloc[-3]
        pfema50 = pema50.item()
        uema50 = ema(dfc, 50).iloc[-8]
        ufema50 = uema50.item()

        ema5 = ema(dfc, 5).iloc[-2]
        fema5 = ema5.item()
        pema5 = ema(dfc, 5).iloc[-3]
        pfema5 = pema5.item()
        # pema200 = ema(dfc, 200).iloc[-3]
        # pfema200 = ema200.item()
        return fema200
        # return fema20, fema50, fema100, ufema20, ufema50, ufema100
        # return fema100, pfema100, fema200, pfema200
        # return fema50, fema100, fema200
        # return fema50, pfema50, fema200, pfema200, ufema50
        # return fema50, ufema50
        # priceprecision = precision(symbol)[1]
        # return fema50, pfema50, fema200, pfema200, ufema50
        # return fema200, fema100, fema50
        # return round(pema50,priceprecision), round(ema50,priceprecision), round(pema100,priceprecision), round(ema100,priceprecision), round(pema100,priceprecision), round(ema100,priceprecision)
        # return pema13, ema13, pema50, ema50
        # return round(ema16, priceprecision), round(ema96, priceprecision)
        # return fema16, fema96
        # return fema10, fema100
        # return fema100, fema50
        # return fema50, pfema50, fema100, pfema100, fema200, pfema200
        # return fema20, pfema20, fema100, pfema100
        # return fema50, pfema50, fema5, pfema5
        # return fema20, pfema20
        # return round(pema50, priceprecision), round(ema50, priceprecision), round(pema100, priceprecision), round(ema100, priceprecision)

    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetema.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        # print(error)
        return 0 """

""" resultsdata = data("BTCUSDT", "3m", False)
dfc = resultsdata[0]
# print(dfc)
# dfh = resultsdata[1]
# dfl = resultsdata[2]
# dfo = resultsdata[3]

print(ExponentialMovingAverage(dfc)) """

#__________________________________________________otra ema ___________________________________________#

def Mediamovilexponencial(dfc):
    # lhighprice, lopenprice, llowprice = [], [], []
    # lcloseprice = []
    # global dfc
    try:
        
        # ema16 = ema(dfc, 16).iloc[-2]
        # ema160 = ema(dfc, 160).iloc[-2]
        # ema96 = ema(dfc, 96).iloc[-2]
        # fema96 = ema96.item()
        # fema16 = ema16.item()
        # fema160 = ema160.item()
        """ ema200 = sma(dfc, 200).iloc[-2]
        fema200 = ema200.item()
        pema200 = sma(dfc, 200).iloc[-3]
        pfema200 = pema200.item() """

        # ema59 = ema(dfc, 59)
        # print(type(ema59))
        # pfema59 = pema59.item()

        pema59 = ema(dfc, 50).iloc[-2]
        pfema59 = pema59.item()

        ema59 = ema(dfc, 50).iloc[-1]
        fema59 = ema59.item()

        ema200 = ema(dfc, 200).iloc[-1]
        fema200 = ema200.item()

        pema200 = ema(dfc, 200).iloc[-2]
        pfema200 = pema200.item()

        ema100 = ema(dfc, 100).iloc[-1]
        fema100 = ema100.item()

        pema100 = ema(dfc, 100).iloc[-2]
        pfema100 = pema100.item()

        """ ema200 = ema(dfc, 200).iloc[-2]
        fema200 = ema200.item() """      
        

        pema20 = ema(dfc, 20).iloc[-2]
        pfema20 = pema20.item()

        ema20 = ema(dfc, 20).iloc[-1]
        fema20 = ema20.item()

        """ ema400 = ema(dfc, 400).iloc[-2]
        fema400 = ema400.item()
        pema400 = ema(dfc, 400).iloc[-3]
        pfema400 = pema400.item()

        sema100 = sma(dfc, 100).iloc[-2]
        fsema100 = sema100.item()
        psema100 = sma(dfc, 100).iloc[-8]
        psfema100 = psema100.item()
        

        sema20 = sma(dfc, 20).iloc[-2]
        fsema20 = sema20.item()
        psema20 = sma(dfc, 20).iloc[-8]
        psfema20 = psema20.item()

        sema50 = sma(dfc, 50).iloc[-2]
        fsema50 = sema50.item()
        psema50 = sma(dfc, 50).iloc[-8]
        psfema50 = psema50.item() """
        """ uema50 = ema(dfc, 50).iloc[-8]
        ufema50 = uema50.item() """

        """ sma150= sma(dfc, 150).iloc[-2]
        fsma150 = sma150.item()
        psma150 = sma(dfc, 150).iloc[-3]
        pfsma150 = psma150.item() """
        # pema200 = ema(dfc, 200).iloc[-3]
        # pfema200 = ema200.item()

        # return ema59
        return fema59, pfema59, fema200, pfema200, fema100, pfema100, fema20, pfema20
        # return fema25, pfema25, fema200, pfema200 #, pema20
        # return fsema20, fsema50, fsema100, psfema20, psfema50, psfema100
        # return fsema50, fsema600, psfema50, psfema600
        # return fema400
        # return fema100, pfema100, fema200, pfema200
        # return fema50, fema100, fema200
        # return fema50, pfema50, fema200, pfema200, ufema50
        # return fema50, ufema50
        # priceprecision = precision(symbol)[1]
        # return fema50, pfema50, fema200, pfema200, ufema50
        # return fema200, fema100, fema50
        # return round(pema50,priceprecision), round(ema50,priceprecision), round(pema100,priceprecision), round(ema100,priceprecision), round(pema100,priceprecision), round(ema100,priceprecision)
        # return pema13, ema13, pema50, ema50
        # return round(ema16, priceprecision), round(ema96, priceprecision)
        # return fema16, fema96
        # return fema10, fema100
        # return fema100, fema50
        # return fsema50, psfema50, fsema100, psfema100, fsema200, psfema200
        # return fsema50, fsema200
        # return fema20, pfema20, fema100, pfema100
        # return fema50, pfema50, fema5, pfema5
        # return fema20, pfema20
        # return round(pema50, priceprecision), round(ema50, priceprecision), round(pema100, priceprecision), round(ema100, priceprecision)

    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetema.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        # print(error)
        return 0, 0

""" resultsdata = data("SYNUSDT", "5m", True)
dfc = resultsdata[0]
# print(dfc)
# dfh = resultsdata[1]
# dfl = resultsdata[2]
# dfo = resultsdata[3]

print(Mediamovilexponencial(dfc)) """

#__________________________________________________ema señales temporalidades grandes ___________________________________________#

def Mediamovilexponencial2(dfc):
    # lhighprice, lopenprice, llowprice = [], [], []
    # lcloseprice = []
    # global dfc
    try:
        
        # ema16 = ema(dfc, 16).iloc[-2]
        # ema160 = ema(dfc, 160).iloc[-2]
        # ema96 = ema(dfc, 96).iloc[-2]
        # fema96 = ema96.item()
        # fema16 = ema16.item()
        # fema160 = ema160.item()
        """ ema200 = sma(dfc, 200).iloc[-2]
        fema200 = ema200.item()
        pema200 = sma(dfc, 200).iloc[-3]
        pfema200 = pema200.item() """

        # ema59 = ema(dfc, 59)
        # print(type(ema59))
        # pfema59 = pema59.item()

        pema50 = ema(dfc, 50).iloc[-3]
        pfema50 = pema50.item()

        ema50 = ema(dfc, 50).iloc[-2]
        fema50 = ema50.item()

        pema100 = ema(dfc, 100).iloc[-3]
        pfema100 = pema100.item()

        ema100 = ema(dfc, 100).iloc[-2]
        fema100 = ema100.item()

        ema200 = ema(dfc, 200).iloc[-2]
        fema200 = ema200.item()

        pema200 = ema(dfc, 200).iloc[-3]
        pfema200 = pema200.item()

        """ ema25 = ema(dfc, 25).iloc[-2]
        fema25 = ema25.item() """

        """ pema25 = ema(dfc, 25).iloc[-3]
        pfema25 = pema25.item()

        ema200 = ema(dfc, 200).iloc[-2]
        fema200 = ema200.item() """        
        

        """ pema20 = sma(dfc, 20).iloc[-10]
        pfema20 = pema20.item() """

        """ ema400 = ema(dfc, 400).iloc[-2]
        fema400 = ema400.item()
        pema400 = ema(dfc, 400).iloc[-3]
        pfema400 = pema400.item()

        sema100 = sma(dfc, 100).iloc[-2]
        fsema100 = sema100.item()
        psema100 = sma(dfc, 100).iloc[-8]
        psfema100 = psema100.item()
        

        sema20 = sma(dfc, 20).iloc[-2]
        fsema20 = sema20.item()
        psema20 = sma(dfc, 20).iloc[-8]
        psfema20 = psema20.item()

        sema50 = sma(dfc, 50).iloc[-2]
        fsema50 = sema50.item()
        psema50 = sma(dfc, 50).iloc[-8]
        psfema50 = psema50.item() """
        """ uema50 = ema(dfc, 50).iloc[-8]
        ufema50 = uema50.item() """

        """ sma150= sma(dfc, 150).iloc[-2]
        fsma150 = sma150.item()
        psma150 = sma(dfc, 150).iloc[-3]
        pfsma150 = psma150.item() """
        # pema200 = ema(dfc, 200).iloc[-3]
        # pfema200 = ema200.item()

        # return ema59
        return fema50, pfema50, fema100, pfema100, fema200, pfema200
        # return fema25, pfema25, fema200, pfema200 #, pema20
        # return fsema20, fsema50, fsema100, psfema20, psfema50, psfema100
        # return fsema50, fsema600, psfema50, psfema600
        # return fema400
        # return fema100, pfema100, fema200, pfema200
        # return fema50, fema100, fema200
        # return fema50, pfema50, fema200, pfema200, ufema50
        # return fema50, ufema50
        # priceprecision = precision(symbol)[1]
        # return fema50, pfema50, fema200, pfema200, ufema50
        # return fema200, fema100, fema50
        # return round(pema50,priceprecision), round(ema50,priceprecision), round(pema100,priceprecision), round(ema100,priceprecision), round(pema100,priceprecision), round(ema100,priceprecision)
        # return pema13, ema13, pema50, ema50
        # return round(ema16, priceprecision), round(ema96, priceprecision)
        # return fema16, fema96
        # return fema10, fema100
        # return fema100, fema50
        # return fsema50, psfema50, fsema100, psfema100, fsema200, psfema200
        # return fsema50, fsema200
        # return fema20, pfema20, fema100, pfema100
        # return fema50, pfema50, fema5, pfema5
        # return fema20, pfema20
        # return round(pema50, priceprecision), round(ema50, priceprecision), round(pema100, priceprecision), round(ema100, priceprecision)

    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetema.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        # print(error)
        return 0, 0

""" resultsdata = data("ETHUSDT", "3m", True)
dfc = resultsdata[0]
# print(dfc)
# dfh = resultsdata[1]
# dfl = resultsdata[2]
# dfo = resultsdata[3]

print(Mediamovilexponencial(dfc)) """

#______________________________________________ DESVIACION ESTANDARD ________________________________#

def dsema(data, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    ema_values = np.convolve(data, weights, mode='full')[:len(data)]
    ema_values[:window] = ema_values[window - 1]
    return ema_values

def calculate_standard_deviation(data, ema_values):
    # ema_values = ema(data, window)
    deviations = data - ema_values
    squared_deviations = deviations ** 2
    mean_squared_deviations = np.mean(squared_deviations)
    standard_deviation = np.sqrt(mean_squared_deviations)
    return standard_deviation

#___________________________________________________ SMA _____________________________________________#

# def SimpleMovingAverage(symbol, temporality):
def SimpleMovingAverageStrategy(dfc):
    # lhighprice, lopenprice, llowprice = [], [], []
    # lcloseprice = []
    # global dfc
    try:
        
        # ema16 = ema(dfc, 16).iloc[-2]
        # ema160 = ema(dfc, 160).iloc[-2]
        # ema96 = ema(dfc, 96).iloc[-2]
        # fema96 = ema96.item()
        # fema16 = ema16.item()
        # fema160 = ema160.item()
        """ ema200 = sma(dfc, 200).iloc[-2]
        fema200 = ema200.item()
        pema200 = sma(dfc, 200).iloc[-3]
        pfema200 = pema200.item() """

        ema20 = sma(dfc, 20).iloc[-2]
        fema20 = ema20.item()
        pema20 = sma(dfc, 20).iloc[-10]
        pfema20 = pema20.item()

        """ ema400 = ema(dfc, 400).iloc[-2]
        fema400 = ema400.item()
        pema400 = ema(dfc, 400).iloc[-3]
        pfema400 = pema400.item()

        sema100 = sma(dfc, 100).iloc[-2]
        fsema100 = sema100.item()
        psema100 = sma(dfc, 100).iloc[-8]
        psfema100 = psema100.item()
        

        sema20 = sma(dfc, 20).iloc[-2]
        fsema20 = sema20.item()
        psema20 = sma(dfc, 20).iloc[-8]
        psfema20 = psema20.item()

        sema50 = sma(dfc, 50).iloc[-2]
        fsema50 = sema50.item()
        psema50 = sma(dfc, 50).iloc[-8]
        psfema50 = psema50.item() """
        """ uema50 = ema(dfc, 50).iloc[-8]
        ufema50 = uema50.item() """

        """ sma150= sma(dfc, 150).iloc[-2]
        fsma150 = sma150.item()
        psma150 = sma(dfc, 150).iloc[-3]
        pfsma150 = psma150.item() """
        # pema200 = ema(dfc, 200).iloc[-3]
        # pfema200 = ema200.item()

        return fema20, pema20
        # return fsema20, fsema50, fsema100, psfema20, psfema50, psfema100
        # return fsema50, fsema600, psfema50, psfema600
        # return fema400
        # return fema100, pfema100, fema200, pfema200
        # return fema50, fema100, fema200
        # return fema50, pfema50, fema200, pfema200, ufema50
        # return fema50, ufema50
        # priceprecision = precision(symbol)[1]
        # return fema50, pfema50, fema200, pfema200, ufema50
        # return fema200, fema100, fema50
        # return round(pema50,priceprecision), round(ema50,priceprecision), round(pema100,priceprecision), round(ema100,priceprecision), round(pema100,priceprecision), round(ema100,priceprecision)
        # return pema13, ema13, pema50, ema50
        # return round(ema16, priceprecision), round(ema96, priceprecision)
        # return fema16, fema96
        # return fema10, fema100
        # return fema100, fema50
        # return fsema50, psfema50, fsema100, psfema100, fsema200, psfema200
        # return fsema50, fsema200
        # return fema20, pfema20, fema100, pfema100
        # return fema50, pfema50, fema5, pfema5
        # return fema20, pfema20
        # return round(pema50, priceprecision), round(ema50, priceprecision), round(pema100, priceprecision), round(ema100, priceprecision)

    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetema.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        # print(error)
        return 0, 0

""" resultsdata = data("BTCUSDT", "3m", True)
dfc = resultsdata[0]
# print(dfc)
# dfh = resultsdata[1]
# dfl = resultsdata[2]
# dfo = resultsdata[3]

print(SimpleMovingAverageStrategy(dfc)) """

#________________________________SMMA_________________________________#

def SMMA(dfc):
    # lhighprice, lopenprice, llowprice = [], [], []
    # lcloseprice = []
    # global dfc
    # sma = None
    try:
        
        sema200 = sma(dfc, 200).iloc[-2]
        fsema200 = sema200.item()
        psema200 = sma(dfc, 200).iloc[-3]
        psfema200 = psema200.item()
        # smma = (psfema200 * (200 - 1) + close) / 200

        # Calcula la media móvil simple de 10 periodos
        # smaa = dfc.rolling(window=200, min_periods=1).mean()

        # Calcula la media móvil simple suavizada de 10 periodos
        # smma = smaa.ewm(span=200, adjust=False).mean()
        # smma = dfc.ewm(span=200, adjust=False).mean()

        # Imprime los primeros 10 valores de la SMMA
        # print(smma.tail(10))
        # print(smma.head(10))

        # Calcula la media móvil suavizada de 200 periodos
        # smma = pd.Series(index=dfc.index)
        smma = pd.Series

        for i in range(len(dfc)):
            if pd.isna(smma[i-1]):
                smma[i] = pd.Series(dfc[:i+1]).mean()
            else:
                smma[i] = (smma[i-1] * (200 - 1) + dfc[i]) / 200

        # Imprime los primeros 10 valores de la SMMA
        # print(smma.head(10))
        # return fsema200, psfema200
        

    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetsmma.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        print(error)
        return 0

""" resultsdata = data("BTCUSDT", "3m", True)
dfc = resultsdata[0]
# print(dfc)
# dfh = resultsdata[1]
# dfl = resultsdata[2]
# dfo = resultsdata[3]

print(SMMA(dfc)) """

#________________________________MACD_________________________________#
def indicatormacd(dfc):
    try:
        # macdresults = macd(dfc)
        # histograma del macd
        lastresults = macd(dfc).iloc[-1]
        lastmacdh = lastresults['MACDh_12_26_9'].tolist()
        penresults = macd(dfc).iloc[-2]
        penmacdh = penresults['MACDh_12_26_9'].tolist()
        antpenresults = macd(dfc).iloc[-3]
        antpenmacdh = antpenresults['MACDh_12_26_9'].tolist()
        antpenresults4 = macd(dfc).iloc[-5]
        antpenmacdh4 = antpenresults4['MACDh_12_26_9'].tolist()

        # señal del macd
        """ lastresults = macd(dfc).iloc[-2]
        lastmacds = lastresults['MACDs_12_26_9'].tolist()
        penresults = macd(dfc).iloc[-3]
        penmacds = penresults['MACDs_12_26_9'].tolist() """
        # antpenresults = macd(dfc).iloc[-4]
        # antpenmacds = antpenresults['MACDh_12_26_9'].tolist()

        # macd
        """ lastresults = macd(dfc).iloc[-2]
        lastmacd = lastresults['MACD_12_26_9'].tolist()
        penresults = macd(dfc).iloc[-3]
        penmacd = penresults['MACD_12_26_9'].tolist() """
        # antpenresults = macd(dfc).iloc[-4]
        # antpenmacd = antpenresults['MACDh_12_26_9'].tolist()
        
        # return macdresults
        # return lastmacd, penmacd, lastmacds, penmacds
        # return lastmacdh, penmacdh, antpenmacdh, antpenmacdh4
        return lastmacdh, penmacdh, antpenmacdh
        
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetmacd.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        print(error)
        return 0, 0
    

""" resultsdata = data("WIFUSDT", "5m", True)
dfc = resultsdata[0]

print(indicatormacd(dfc)) """

#________________________________MACD Short_________________________________#
def indicatormacdshort(dfc):
    try:
        
        lastresults = macd(dfc).iloc[-2]
        lastmacd = lastresults['MACDh_12_26_9'].tolist()
        
        penresults = macd(dfc).iloc[-3]
        penmacd = penresults['MACDh_12_26_9'].tolist()

        antpenresults = macd(dfc).iloc[-4]
        antpenmacd = antpenresults['MACDh_12_26_9'].tolist()
        
        return lastmacd, penmacd, antpenmacd
        
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetmacd.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        print(error)
        return 0, 0
    

""" resultsdata = data("AAVEUSDT", "3m")
dfc = resultsdata[0]

print(indicatormacdshort(dfc)) """

#________________________________MACD Long_________________________________#
def indicatormacdlong(dfclong):
    try:
        
        lastresults = macd(dfclong).iloc[-2]
        lastmacd = lastresults['MACDh_12_26_9'].tolist()
        
        penresults = macd(dfclong).iloc[-3]
        penmacd = penresults['MACDh_12_26_9'].tolist()
        
        return lastmacd, penmacd
        
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetmacd.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        print(error)
        return 0, 0
    

""" resultsdatalong = datalong("AAVEUSDT", "15m")
dfclong = resultsdatalong[0]

print(indicatormacdlong(dfclong)) """

#_________________________________RSI______________________________________#

def indicatorrsi(dfc):
    # lhighprice, lopenprice, llowprice = [], [], []
    # lcloseprice = []
    # global dfc
    try:
        
        # print(type(dfc))
        # rsisma = rsi(dfc, 14)

        """ resultsrsi = rsi(dfc, 7).iloc[-2]
        resultsrsipen = rsi(dfc, 7).iloc[-3] """

        resultsrsi         = rsi(dfc, 14).iloc[-1]
        resultsrsipen      = rsi(dfc, 14).iloc[-2]
        # resultsrsiantpen   = rsi(dfc, 5).iloc[-4]
        fresultsrsi        = resultsrsi.item()
        fresultsrsipen     = resultsrsipen.item()
        # fresultsrsiantpen  = resultsrsiantpen.item()
        # print(rsisma)
        # sma = SimpleMovingAverage(rsisma)
        # results3 = rsi(dfc).iloc[-3]
        return round(resultsrsipen,3), round(resultsrsi,3)
        # return round(fresultsrsipen,2), round(fresultsrsi,2), round(fresultsrsiantpen,2)
        # return sma
        # return round(resultsrsi, 2)
        # return round(results,2), round(results3,2)

    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetrsi.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        # print(error)
        return 0, 0
""" resultsdata = data("SYNUSDT", "1m", True)
dfc = resultsdata[0]
print(indicatorrsi(dfc)) """
""" resulrsisma = indicatorrsi(dfc)
smarsi  = resulrsisma[0]
psmarsi = resulrsisma[1]
print(smarsi)
print(psmarsi) """

#_________________________________RSI2______________________________________#

def indicatorrsi2(dfc):
    # lhighprice, lopenprice, llowprice = [], [], []
    # lcloseprice = []
    # global dfc
    try:
        
        # print(type(dfc))
        # rsisma = rsi(dfc, 14)

        """ resultsrsi = rsi(dfc, 7).iloc[-2]
        resultsrsipen = rsi(dfc, 7).iloc[-3] """

        resultsrsi         = rsi(dfc, 3).iloc[-1]
        resultsrsipen      = rsi(dfc, 3).iloc[-2]
        # resultsrsiantpen   = rsi(dfc, 5).iloc[-4]
        fresultsrsi        = resultsrsi.item()
        fresultsrsipen     = resultsrsipen.item()
        # fresultsrsiantpen  = resultsrsiantpen.item()
        # print(rsisma)
        # sma = SimpleMovingAverage(rsisma)
        # results3 = rsi(dfc).iloc[-3]
        return round(resultsrsipen,3), round(resultsrsi,3)
        # return round(fresultsrsipen,2), round(fresultsrsi,2), round(fresultsrsiantpen,2)
        # return sma
        # return round(resultsrsi, 2)
        # return round(results,2), round(results3,2)

    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetrsi.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        # print(error)
        return 0, 0
""" resultsdata = data("SYNUSDT", "5m", True)
dfc = resultsdata[0]
print(indicatorrsi2(dfc))
print(indicatorrsi(dfc)) """
""" resulrsisma = indicatorrsi(dfc)
smarsi  = resulrsisma[0]
psmarsi = resulrsisma[1]
print(smarsi)
print(psmarsi) """

#______________________________B Bands______________________________________#
def indicatorbollingerbands(dfc):
    try:
        lastresults = bbands(dfc, length=20).iloc[-2]
        lastbbl = lastresults['BBL_20_2.0'].tolist()
        lastbbu = lastresults['BBU_20_2.0'].tolist()

        penresults = bbands(dfc, length=20).iloc[-3]
        penbbl = penresults['BBL_20_2.0'].tolist()
        penbbu = penresults['BBU_20_2.0'].tolist()

        antresults = bbands(dfc, length=20).iloc[-4]
        antbbl = antresults['BBL_20_2.0'].tolist()
        antbbu = antresults['BBU_20_2.0'].tolist()

        return lastbbl, lastbbu, penbbl, penbbu, antbbl, antbbu
        
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetbb.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        print(error)

""" resultsdata = data("BTCUSDT", "3m")
dfc = resultsdata[0]
# print(dfc)
# dfh = resultsdata[1]
# dfl = resultsdata[2]
# dfo = resultsdata[3]

print(indicatorbollingerbands(dfc)) """
#___________________________________________________________________________#

#___________________________________________________ DMI _____________________________________________#
def indicatoradx(dfh, dfl, dfc):
    # lhighprice, lopenprice, llowprice = [], [], []
    # lcloseprice = []
    try:
        
        # print(type(dfc))
        results    = adx(dfh, dfl, dfc).iloc[-1]
        penresults = adx(dfh, dfl, dfc).iloc[-2]
        antpenresults = adx(dfh, dfl, dfc).iloc[-4]
        adxvalor = results['ADX_14'].tolist()
        penadx   = penresults['ADX_14'].tolist()
        antpenadx   = antpenresults['ADX_14'].tolist()
        dmp = results['DMP_14'].tolist()
        dmn = results['DMN_14'].tolist()

        # results3 = adx(dfh, dfl, dfc).iloc[-3]
        # adxvalor3 = results3['ADX_14'].tolist()
        # dmp3 = results3['DMP_14'].tolist()
        # dmn3 = results3['DMN_14'].tolist()

        
        # priceprecision = precision(symbol)[1]
        # return adxvalor
        # return adxvalor, adxvalor3
        return dmp, dmn, adxvalor, penadx, antpenadx
        # return round(adxvalor), round(dmp), round(dmn), round(adxvalor3), round(dmp3), round(dmn3)
        # return adxvalor, dmp, dmn, adxvalor3, dmp3, dmn3


    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetadx.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()
        print(error)
        # return 0, 0, 0, 0, 0, 0
        return 0, 0, 0
""" resultsdata = data("WIFUSDT", "5m", True)
dfc = resultsdata[0]
dfh = resultsdata[1]
dfl = resultsdata[2]
# dfo = resultsdata[3]

adx = indicatoradx(dfh, dfl, dfc)
print("dmp ",adx[0])
print("dmn ",adx[1])
print("adx ",adx[2])
print("penadx ",adx[3])
print("antpenadx ",adx[4]) """

#_____________________Data RSI real time 15m_____________________________________________________________
@with_goto
def datarsi15m(symbol, temporality):
    # print("entro en data rsi ", symbol, temporality)
    lcloseprice, lopenprice = [], []
    lhighprice, llowprice = [], []
    lista_precios_cierre = []
    lvolume = []
    # global dfc, dfh, dfl
    # while True:
    try:
        label .datam
        if temporality == '1m':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, '750 minute ago UTC')
            # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, '250 minute ago UTC')
            # print("Len de data_hist ",len(data_historical))
            # print("entro en 1m")
        if temporality == '3m':
            # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '750 minute ago UTC')
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '2250 minute ago UTC')
        if temporality == '5m':
            # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_5MINUTE, '1250 minute ago UTC')
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_5MINUTE, '3750 minute ago UTC')
        if temporality == '15m':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, '11250 minute ago UTC')
        if temporality == '30m':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, '7500 minute ago UTC')
        if temporality == '1h':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1HOUR, '750 hour ago UTC')        
        if temporality == '4h':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_4HOUR, '1000 hour ago UTC')
        if temporality == '12h':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_12HOUR, '3000 hour ago UTC')
        if temporality == '1D':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1DAY, '250 day ago UTC')
        # print("len ",len(data_historical))
        if len(data_historical) != 750:
            # print("data incompleta")
            # goto .datam
            
            """ lista_precios_cierre = 0
            datacomplete = False
            print("data incompleta")
            return datacomplete, lista_precios_cierre """
            pass
            
        if len(data_historical) == 750:
            # print("len ",len(data_historical))
            # print("entro en len 250")
            for i in range(len(data_historical)):
                lopenprice.append(float(data_historical[i][1]))
                lhighprice.append(float(data_historical[i][2]))
                llowprice.append(float(data_historical[i][3]))
                lcloseprice.append(float(data_historical[i][4]))
                lvolume.append(float(data_historical[i][5]))
                # lista_precios_cierre.append(float(data_historical[i][4]))
            penclose = lcloseprice[-3]
            dic_lpo = {"Open": lopenprice}
            dic_lph = {"High": lhighprice}
            dic_lpl = {"Low": llowprice}
            dic_lpc = {"Close": lcloseprice}     

            odf = DataFrame(dic_lpo)
            dfo = odf.get('Open')

            cdf = DataFrame(dic_lpc)
            dfc = cdf.get('Close')

            hdf = DataFrame(dic_lph)
            dfh = hdf.get('High')

            ldf = DataFrame(dic_lpl)
            dfl = ldf.get('Low')
            datacompletersi = True
            return lcloseprice, datacompletersi, lhighprice, llowprice, lvolume
        else:
            # print("Data ICOMPLETA")
            return [0,0], False
            # pass
            # return lcloseprice, dfc, dfh, dfl, penclose, datacomplete
    except Exception as error:

        archivo_path = 'errorgetdatarsi.txt'

        if os.path.exists(archivo_path):
            # Si el archivo existe, abre en modo 'a' para agregar contenido
            with open(archivo_path, 'a') as archivo:
                # Escribe en una nueva linea
                archivo.write(str(error))
        else:
            # Si el archivo no existe, crea uno nuevo y escribe en el
            with open(archivo_path, 'w') as archivo:
                archivo.write(str(error))

        """ objprecision = open('/home/angel/Documentos/botscalping/errorgetdatarsi.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()  """
        return [0,0], False
# print(datarsi('BTCUSDT', '5m'))

#_____________________Data RSI real time_____________________________________________________________
@with_goto
def datarsi(symbol, temporality):
    # print("entro en data rsi ", symbol, temporality)
    lcloseprice, lopenprice = [], []
    lhighprice, llowprice = [], []
    lista_precios_cierre = []
    lvolume = []
    # global dfc, dfh, dfl
    # while True:
    try:
        label .datam
        if temporality == '1m':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, '750 minute ago UTC')
            # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, '250 minute ago UTC')
            # print("Len de data_hist ",len(data_historical))
            # print("entro en 1m")
        if temporality == '3m':
            # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '750 minute ago UTC')
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '2250 minute ago UTC')
        if temporality == '5m':
            # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_5MINUTE, '1250 minute ago UTC')
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_5MINUTE, '3750 minute ago UTC')
        if temporality == '15m':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, '11250 minute ago UTC')
        if temporality == '30m':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, '7500 minute ago UTC')
        if temporality == '1h':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1HOUR, '750 hour ago UTC')        
        if temporality == '4h':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_4HOUR, '1000 hour ago UTC')
        if temporality == '12h':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_12HOUR, '3000 hour ago UTC')
        if temporality == '1D':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1DAY, '250 day ago UTC')
        # print("len ",len(data_historical))
        if len(data_historical) != 750:
            # print("data incompleta")
            # goto .datam
            
            """ lista_precios_cierre = 0
            datacomplete = False
            print("data incompleta")
            return datacomplete, lista_precios_cierre """
            pass
            
        if len(data_historical) == 750:
            # print("len ",len(data_historical))
            # print("entro en len 250")
            for i in range(len(data_historical)):
                lopenprice.append(float(data_historical[i][1]))
                lhighprice.append(float(data_historical[i][2]))
                llowprice.append(float(data_historical[i][3]))
                lcloseprice.append(float(data_historical[i][4]))
                lvolume.append(float(data_historical[i][5]))
                # lista_precios_cierre.append(float(data_historical[i][4]))
            penclose = lcloseprice[-3]
            dic_lpo = {"Open": lopenprice}
            dic_lph = {"High": lhighprice}
            dic_lpl = {"Low": llowprice}
            dic_lpc = {"Close": lcloseprice}     

            odf = DataFrame(dic_lpo)
            dfo = odf.get('Open')

            cdf = DataFrame(dic_lpc)
            dfc = cdf.get('Close')

            hdf = DataFrame(dic_lph)
            dfh = hdf.get('High')

            ldf = DataFrame(dic_lpl)
            dfl = ldf.get('Low')
            datacompletersi = True
            return lcloseprice, datacompletersi, lhighprice, llowprice, lvolume
        else:
            # print("Data ICOMPLETA")
            return [0,0], False
            # pass
            # return lcloseprice, dfc, dfh, dfl, penclose, datacomplete
    except Exception as error:

        archivo_path = 'errorgetdatarsi.txt'

        if os.path.exists(archivo_path):
            # Si el archivo existe, abre en modo 'a' para agregar contenido
            with open(archivo_path, 'a') as archivo:
                # Escribe en una nueva linea
                archivo.write(str(error))
        else:
            # Si el archivo no existe, crea uno nuevo y escribe en el
            with open(archivo_path, 'w') as archivo:
                archivo.write(str(error))

        """ objprecision = open('/home/angel/Documentos/botscalping/errorgetdatarsi.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close()  """
        return [0,0], False
# print(datarsi('BTCUSDT', '5m'))

#_____________________Data Backtesting_____________________________________________________________
@with_goto
def databacktesting(symbol, temporality):
    # print("entro en data rsi ", symbol, temporality)
    lcloseprice, lopenprice = [], []
    lhighprice, llowprice, lvolprice = [], [], []
    lista_precios_cierre = []
    timestamp = []
    # global dfc, dfh, dfl
    # while True:
    try:
        label .datam
        if temporality == '1m':
            # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, '750 minute ago UTC')
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, '60000 minute ago UTC')
            # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, '11250 minute ago UTC')
            # print("Len de data_hist ",len(data_historical))
            # print("entro en 1m")
        if temporality == '3m':
            # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '90000 minute ago UTC') # dos meses
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '60000 minute ago UTC') # un mes
            # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_3MINUTE, '11250 minute ago UTC') # una semana
        if temporality == '5m':
            # data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_5MINUTE, '18750 minute ago UTC')
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_5MINUTE, '2000 minute ago UTC')
        if temporality == '15m':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, '150000 minute ago UTC')
        
        if temporality == '4h':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_4HOUR, '1000 hour ago UTC')
        if temporality == '12h':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_12HOUR, '3000 hour ago UTC')
        if temporality == '1D':
            data_historical = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1DAY, '1100 day ago UTC')
        # print("len ",len(data_historical))
        if len(data_historical) != 250000:
            # goto .datam
            """ lista_precios_cierre = 0
            datacomplete = False
            print("data incompleta")
            return datacomplete, lista_precios_cierre """
            pass
            
        if len(data_historical) == 15000 or len(data_historical) != 15000:
            # print(data_historical)
            # print("len ",len(data_historical))
            print("entro en len 250")
            for i in range(len(data_historical)):
                timestamp.append(float(data_historical[i][0]))
                lopenprice.append(float(data_historical[i][1]))
                lhighprice.append(float(data_historical[i][2]))
                llowprice.append(float(data_historical[i][3]))
                lcloseprice.append(float(data_historical[i][4]))
                lvolprice.append(float(data_historical[i][5]))
                lista_precios_cierre.append(float(data_historical[i][4]))

            df = pd.DataFrame({
                'timestamp': timestamp,
                'open': lopenprice,
                'high': lhighprice,
                'low': llowprice,
                'close': lcloseprice,
                'volume': lvolprice
            })
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

            # Convertir las marcas de tiempo a UTC (que ya lo están) y luego a una zona horaria local
            df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('America/Santiago')

            # Calcular el RSI
            df['rsi'] = ta.rsi(df['close'], length=14)

            # Calcular el EMA de 9 y 20 períodos
            df['ema_9'] = ta.ema(df['close'], length=9)
            df['ema_20'] = ta.ema(df['close'], length=20)
            df['ema_50'] = ta.ema(df['close'], length=50)
            df['ema_100'] = ta.ema(df['close'], length=100)
            df['ema_200'] = ta.ema(df['close'], length=200)

            # Añadir ADX, +DI y -DI al DataFrame original
            adx = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx['ADX_14']
            df['plus_di'] = adx['DMP_14']
            df['minus_di'] = adx['DMN_14']

            # Calcular el MACD
            macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
            df['macd'] = macd['MACD_12_26_9']
            df['macd_signal'] = macd['MACDs_12_26_9']
            df['macd_hist'] = macd['MACDh_12_26_9']

            # Calcular las Bandas de Bollinger
            """ bollinger = ta.bbands(df['close'], length=20, std=2)
            df['bollinger_upper'] = bollinger['BBU_20_2.0']
            df['bollinger_middle'] = bollinger['BBM_20_2.0']
            df['bollinger_lower'] = bollinger['BBL_20_2.0'] """

            # Calcular el stoch
            """ stoch = ta.stoch(df['high'], df['low'], df['close'], fast_k=14, slow_k=3, slow_d=3)
            df['stoch_k'] = stoch['k']
            df['stoch_d'] = stoch['d'] """

            penclose = lcloseprice[-3]
            dic_lpo = {"Open": lopenprice}
            dic_lph = {"High": lhighprice}
            dic_lpl = {"Low": llowprice}
            dic_lpc = {"Close": lcloseprice}
            dic_lpc = {"volume": lvolprice}     

            odf = DataFrame(dic_lpo)
            dfo = odf.get('Open')

            cdf = DataFrame(dic_lpc)
            dfc = cdf.get('Close')

            hdf = DataFrame(dic_lph)
            dfh = hdf.get('High')

            ldf = DataFrame(dic_lpl)
            dfl = ldf.get('Low')
            datacompletersi = True
            # Guardar el DataFrame en un archivo CSV
            csv_filename = f"{symbol}_{temporality}_backtesting.csv"
            df.to_csv(csv_filename, index=False)
            return csv_filename
            # return df
        
        else:
            print("Data ICOMPLETA")
            return [0,0], False
            # pass
            # return lcloseprice, dfc, dfh, dfl, penclose, datacomplete
    except Exception as error:

        archivo_path = 'errorgetdatabacktesting.txt'

        if os.path.exists(archivo_path):
            # Si el archivo existe, abre en modo 'a' para agregar contenido
            with open(archivo_path, 'a') as archivo:
                # Escribe en una nueva linea
                archivo.write(str(error))
        else:
            # Si el archivo no existe, crea uno nuevo y escribe en el
            with open(archivo_path, 'w') as archivo:
                archivo.write(str(error))

        objprecision = open('/home/angel/Documentos/botscalping/errorgetdatabacktesting.txt','w')  # ruta linux
        objprecision.write(str(error))
        objprecision.close() 
        return [0,0], False
# databacktesting('ORCAUSDT', '5m')
# dflow = databacktesting('ETHUSDT', '5m')[0] 
""" dflow = databacktesting('BTCUSDT', '5m')
print(type(dflow))
print(dflow) """
#_____________________Calculo del RSI__________________________________________________________________
def rsimanual(dfc):
    # while True:
    try:
        # lista_precios_cierre = []
        # data_historical = client.futures_historical_klines(ticker, client.KLINE_INTERVAL_1HOUR, '250 hour ago UTC')
        # data_historical = client.futures_historical_klines(ticker, client.KLINE_INTERVAL_1MINUTE, '250 minute ago UTC')
        # data_historical = client.futures_historical_klines(ticker, client.KLINE_INTERVAL_5MINUTE, '1250 minute ago UTC')

        # print("cantidad de velas ", len(data_historical))
        """ if len(data_historical) == 250:
            # print("Velas completas")
            for i in range(len(data_historical)):
                lista_precios_cierre.append(float(data_historical[i][4]))

            dic_lpc = {"precios_cierre": lista_precios_cierre}

            # dataframe = pd.DataFrame(dic_lpc)
            dataframe = DataFrame(dic_lpc)
            # print(dataframe) """

        # diferencia = dataframe["precios_cierre"].diff(1)
        diferencia = dfc.diff(1)
        # print(diferencia)

        positivos = diferencia.copy()
        negativos = diferencia.copy()

        positivos[positivos < 0] = 0
        negativos[negativos > 0] = 0

        # print(positivos)
        # print(negativos)

        ema_posotivos = positivos.ewm(com=(5-1), adjust= False).mean()
        ema_negativos = abs(negativos.ewm(com=(5 - 1), adjust=False).mean())

        rs = ema_posotivos/ema_negativos

        rsi =  100 - (100/(rs+1))

        # print(rsi)
        # print(round(rsi.iloc[-1],2)) # ultima vela
        # print(round(rsi.iloc[-2], 2))  # penultima vela

        # rsi_valor = (round(rsi.iloc[-2],2))
        penrsi = (round(rsi.iloc[-3],2))
        lastrsi = (round(rsi.iloc[-2],2))

        # penrsi = (round(rsi.tail(3),2))
        # lastrsi = (round(rsi.tail(2),2))

        # penrsi = (round(rsi.iat[-3],2))
        # lastrsi = (round(rsi.iat[-2],2))

        # print("RSI: ", rsi_valor)
        # return rsi_valor
        # return penrsi, lastrsi
        return rsi, penrsi, lastrsi
    except Exception as Error:
        ObjFichero = open('/home/angel/Documentos/botscalping/ErrorRSI.txt','w')  # ruta linux
        # ObjFichero = open('errorgetopenorders.txt','w')  # ruta linux
        ObjFichero.write(str(Error))
        ObjFichero.close()

# dfc = data("1INCHUSDT", "1m")[0]

# print(rsimanual(dfc))


# Funcion diseñada para trabajar un solo trade a la vez
""" def openorders():
    try:
        # getOrders = client.futures_get_open_orders()
        objficherocantintents = open("/home/angel/Documentos/botscalping/cantintents.txt")
        # objficherocantintents = open("cantintents.txt")
        cantintents = int(objficherocantintents.read())
        objficherocantintents.close()
        objficherointents = open("/home/angel/Documentos/botscalping/intents.txt")
        # objficherointents = open("intents.txt")
        intents = int(objficherointents.read())
        objficherointents.close()
        objficherotradeopen = open("/home/angel/Documentos/botscalping/tradeopen.txt")
        # objficherotradeopen = open("tradeopen.txt")
        tradeopen = str(objficherotradeopen.read())
        objficherotradeopen.close()
        # if len(getOrders) == 0 and intents < 3:
        if tradeopen == 'False' and intents < cantintents:
            noTradeopen = True
            ObjFichero = open("/home/angel/Documentos/botscalping/tradeopen.txt", 'w')
            # ObjFichero = open("tradeopen.txt", 'w')
            ObjFichero.write("True")
            ObjFichero.close()
        else:
            noTradeopen = False
    except Exception as error:
        noTradeopen = True
        # ObjFichero = open('C:\\Users\\Angel Leon Alvarez\\PycharmProjects\\botautomaticofuturos\\errorgetopenorders.txt','w')  # ruta windows
        ObjFichero = open('/home/angel/Documentos/botscalping/errorgetopenorders.txt','w')  # ruta linux
        # ObjFichero = open('errorgetopenorders.txt','w')  # ruta linux
        ObjFichero.write(str(error))
        ObjFichero.close()
    return noTradeopen """
# Funcion diseñada para trabajar los trades que se deseen
""" def openorders():
    while True:
        try:
            # getOrders = client.futures_get_open_orders()
            objficherocantintents = open("/home/angel/Documentos/botscalping/cantintents.txt")
            # objficherocantintents = open("cantintents.txt")
            cantintents = int(objficherocantintents.read())
            objficherocantintents.close()
            objficherointents = open("/home/angel/Documentos/botscalping/intents.txt")
            # objficherointents = open("intents.txt")
            intents = int(objficherointents.read())
            objficherointents.close()
            objficherotradeopen = open("/home/angel/Documentos/botscalping/tradeopen.txt")
            # objficherotradeopen = open("tradeopen.txt")
            tradeopen = str(objficherotradeopen.read())
            auxtradeopen = int(tradeopen)
            objficherotradeopen.close()
            # if len(getOrders) == 0 and intents < 3:
            # if tradeopen == 'False' and intents < cantintents:
            if auxtradeopen <= 5:
                noTradeopen = True
                ObjFichero = open("/home/angel/Documentos/botscalping/tradeopen.txt", 'w')
                # ObjFichero = open("tradeopen.txt", 'w')
                auxtradeopen +=1
                ObjFichero.write(str(auxtradeopen))
                ObjFichero.close()
                return noTradeopen
            else:
                noTradeopen = False
                return noTradeopen
        except Exception as error:
            noTradeopen = True
            # ObjFichero = open('C:\\Users\\Angel Leon Alvarez\\PycharmProjects\\botautomaticofuturos\\errorgetopenorders.txt','w')  # ruta windows
            ObjFichero = open('/home/angel/Documentos/botscalping/errorgetopenorders.txt','w')  # ruta linux
            # ObjFichero = open('errorgetopenorders.txt','w')  # ruta linux
            ObjFichero.write(str(error))
            ObjFichero.close()
            continue
             """
""" def balance():
    global client
    try:
        getbalance = client.futures_account_balance(recvWindow=6000)
        asset = getbalance[6].get('asset')
        if asset == 'USDT':
            usdtbalance = getbalance[6].get('balance')
            ObjFichero = open("/home/angel/Documentos/botscalping/initialbalance.txt",'w')
            # ObjFichero = open("initialbalance.txt",'w')
            ObjFichero.write(str(usdtbalance))
            ObjFichero.close()
    except Exception as error:
        # ObjFichero = open('C:\\Users\\Angel Leon Alvarez\\PycharmProjects\\botautomaticofuturos\\errorgetbalance.txt','w')  # ruta windows
        ObjFichero = open('/home/angel/Documentos/botscalping/errorgetbalance.txt','w')  # ruta linux
        # ObjFichero = open('errorgetbalance.txt','w')  # ruta linux
        ObjFichero.write(str(error))
        ObjFichero.close()
    return usdtbalance """

""" def setintents():
    global client
    try:
        objinitalbalance = open("/home/angel/Documentos/botscalping/initialbalance.txt")
        # objinitalbalance = open("initialbalance.txt")
        initialbalance = float(objinitalbalance.read())
        objinitalbalance.close()
        getbalance = client.futures_account_balance(recvWindow=6000)
        asset = getbalance[6].get('asset')
        if asset == 'USDT':
            currentusdtbalance = float(getbalance[6].get('balance'))
            # currentusdtbalance = 93.06
            if currentusdtbalance < initialbalance:
                objficherointents = open("/home/angel/Documentos/botscalping/intents.txt")
                # objficherointents = open("intents.txt")
                intents = int(objficherointents.read())
                objficherointents.close()
                #aumento en 1 el numero de veces perdedoras
                acum = intents + 1
                objficherointents = open("/home/angel/Documentos/botscalping/intents.txt", 'w')
                # objficherointents = open("intents.txt", 'w')
                objficherointents.write(str(acum))
                objficherointents.close()
    except Exception as error:
         Objerrorupdatingbalance = open('/home/angel/Documentos/botscalping/errorupdatingbalance.txt','w')  # ruta linux
        # ObjFichero = open('errorgetbalance.txt','w')  # ruta linux
         Objerrorupdatingbalance.write(str(error))
         Objerrorupdatingbalance.close() """
""" def leverage(newsymbol, newleverage):

    try:
        setleverage = client.futures_change_leverage(symbol=newsymbol,leverage = newleverage, recvWindow=6000)
        setleverage = True
        # print("Entro en el try")
    except Exception as error:
        setleverage = True
        # print("Entro en el except")
        # print(error)
        # ObjFichero = open('C:\\Users\\Angel Leon Alvarez\\PycharmProjects\\botautomaticofuturos\\setleverage.txt','w')  # ruta windows
        ObjFichero = open('/home/angel/Documentos/botscalping/setleverage.txt','w')  # ruta linux
        # ObjFichero = open('setleverage.txt','w')  # ruta linux
        ObjFichero.write(str(error))
        ObjFichero.close()
    # print(setleverage)
    # print("leverage")
    return setleverage
def margintype(newsymbol, newmargintype):

    try:
        setmargintype = client.futures_change_margin_type(symbol=newsymbol,marginType=newmargintype,recvWindow=6000)
        margintypeok = True
        # print("Entro en el try")
    except Exception as error:
        margintypeok = True
        # print("Entro en el except")
        # print(error)
        # ObjFichero = open('C:\\Users\\Angel Leon Alvarez\\PycharmProjects\\botautomaticofuturos\\errormargintype.txt','w')  # ruta windows
        ObjFichero = open('/home/angel/Documentos/botscalping/errormargintype.txt','w')  # ruta linux
        # ObjFichero = open('errormargintype.txt','w')  # ruta linux
        ObjFichero.write(str(error))
        ObjFichero.close()
    return margintypeok
def precision(PAR):
    try:
        lista = client.futures_exchange_info()
        cont = 0
        while True:
            if lista['symbols'][cont]['pair'] == PAR:
                quantityPrecision = lista['symbols'][cont]['quantityPrecision']
                cont = 0
                return quantityPrecision
                # break
            cont += 1
    except Exception as error:
        objprecision = open('/home/angel/Documentos/botscalping/errorgetprecision.txt','w')  # ruta Lindows
        objprecision.write(str(error))
        objprecision.close()
def updatebalance(variacion):
    while True:
        try:
            objinitalbalance = open("/home/angel/Documentos/botscalping/initialbalanceshorts.txt")
            initialbalance = float(objinitalbalance.read())
            objinitalbalance.close()
            break
        except Exception:
            continue
    while True:
        try:
            if variacion > 0:
                newbalance = (((initialbalance * variacion) / 100) + initialbalance) * 1.0004
                ObjFichero = open("/home/angel/Documentos/botscalping/initialbalanceshorts.txt",'w')
                # ObjFichero = open("initialbalance.txt",'w')
                ObjFichero.write(str(newbalance))
                ObjFichero.close()
                
                #Aqui cuento las veces positivas
                objficherointents = open("/home/angel/Documentos/botscalping/intentspositivosshorts.txt")
                intents = int(objficherointents.read())
                objficherointents.close()
                #aumento en 1 el numero de veces perdedoras
                acum = intents + 1
                objficherointents = open("/home/angel/Documentos/botscalping/intentspositivosshorts.txt", 'w')
                # objficherointents = open("intents.txt", 'w')
                objficherointents.write(str(acum))
                objficherointents.close()
            if variacion < 0:
                newbalance = (((initialbalance * variacion) / 100) + initialbalance) * 1.0004
                ObjFichero = open("/home/angel/Documentos/botscalping/initialbalanceshorts.txt",'w')
                # ObjFichero = open("initialbalance.txt",'w')
                ObjFichero.write(str(newbalance))
                ObjFichero.close()

                # Aqui cuento las veces negativas
                objficherointents = open("/home/angel/Documentos/botscalping/intentsnegativosshorts.txt")
                intents = int(objficherointents.read())
                objficherointents.close()
                #aumento en 1 el numero de veces perdedoras
                acum = intents + 1
                objficherointents = open("/home/angel/Documentos/botscalping/intentsnegativosshorts.txt", 'w')
                # objficherointents = open("intents.txt", 'w')
                objficherointents.write(str(acum))
                objficherointents.close()
            break
        except Exception as error:
            # ObjFichero = open('C:\\Users\\Angel Leon Alvarez\\PycharmProjects\\botautomaticofuturos\\errorgetopenorders.txt','w')  # ruta windows
            ObjFichero = open('/home/angel/Documentos/botscalping/errorudatebalance.txt','w')  # ruta linux
            # ObjFichero = open('errorgetopenorders.txt','w')  # ruta linux
            ObjFichero.write(str(error))
            ObjFichero.close()
            continue
def updatebalancelong(variacion):
    while True:
        try:
            objinitalbalance = open("/home/angel/Documentos/botscalping/initialbalancelong.txt")
            initialbalance = float(objinitalbalance.read())
            objinitalbalance.close()
            break
        except Exception:
            continue
    while True:
        try:
            if variacion < 0:
                newvariation = abs(variacion)
                newbalance = (((initialbalance * newvariation) / 100) + initialbalance) * 1.0004
                ObjFichero = open("/home/angel/Documentos/botscalping/initialbalancelong.txt",'w')
                # ObjFichero = open("initialbalance.txt",'w')
                ObjFichero.write(str(newbalance))
                ObjFichero.close()
                
                #Aqui cuento las veces positivas
                objficherointents = open("/home/angel/Documentos/botscalping/intentspositivoslong.txt")
                intents = int(objficherointents.read())
                objficherointents.close()
                #aumento en 1 el numero de veces perdedoras
                acum = intents + 1
                objficherointents = open("/home/angel/Documentos/botscalping/intentspositivoslong.txt", 'w')
                # objficherointents = open("intents.txt", 'w')
                objficherointents.write(str(acum))
                objficherointents.close()
            if variacion > 0:
                newvariation = variacion * -1
                newbalance = (((initialbalance * variacion) / 100) + initialbalance) * 1.0004
                ObjFichero = open("/home/angel/Documentos/botscalping/initialbalancelong.txt",'w')
                # ObjFichero = open("initialbalance.txt",'w')
                ObjFichero.write(str(newbalance))
                ObjFichero.close()

                # Aqui cuento las veces negativas
                objficherointents = open("/home/angel/Documentos/botscalping/intentsnegativoslong.txt")
                intents = int(objficherointents.read())
                objficherointents.close()
                #aumento en 1 el numero de veces perdedoras
                acum = intents + 1
                objficherointents = open("/home/angel/Documentos/botscalping/intentsnegativoslong.txt", 'w')
                # objficherointents = open("intents.txt", 'w')
                objficherointents.write(str(acum))
                objficherointents.close()
            break
        except Exception as error:
            noTradeopen = True
            # ObjFichero = open('C:\\Users\\Angel Leon Alvarez\\PycharmProjects\\botautomaticofuturos\\errorgetopenorders.txt','w')  # ruta windows
            ObjFichero = open('/home/angel/Documentos/botscalping/errorbalancelong.txt','w')  # ruta linux
            # ObjFichero = open('errorgetopenorders.txt','w')  # ruta linux
            ObjFichero.write(str(error))
            ObjFichero.close()
            continue """

