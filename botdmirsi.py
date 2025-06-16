# import websocket, json, os.path, requests, logging
import websocket, json, os.path, requests, os
from binance.futures import Futures as ClientFutures
from datetime import datetime
from time import sleep
from pandas import DataFrame
import multiprocessing
# from binance.lib.utils import config_logging
from binance.error import ClientError
from sys import path
from config import API_KEY
from config import API_SECRET
from newcheck import precision, indicatorrsi, Mediamovilexponencial, datarsi, indicatoradx, indicatorrsi2, indicatoratr, indicatormacd

class TradingBot:
    def __init__(self, PAR, interval):
        self.PAR = PAR
        self.interval = interval
        self.activeSignal = False
        self.clientfutures = ClientFutures(API_KEY, API_SECRET)

        # Obtener el nombre del archivo del script sin la extensión
        self.script_name = os.path.splitext(os.path.basename(__file__))[0]

        # Definir el directorio base
        self.base_directory = f"/home/angel/Documentos/botscalping/symbols/{self.script_name}/"

        # Crear el directorio si no existe
        os.makedirs(self.base_directory, exist_ok=True)

        # Inicialización de listas vacías
        self.penultimePrice = []
        self.tradeWaitlist = []
        self.lista_precios_cierre = []
        self.tradeWaitlistlong = []
        self.precisions = []
        self.penultimeClose = []
        self.penultimeOpen = []
        self.lista_precios_altos = []
        self.lista_precios_bajos = []
        self.penultimeHigh = []
        self.penultimeLow = []
        self.penultimeCloseRSI = []
        self.penultimeOpenRSI = []
        self.copiapenultimeCloseRSI = []
        self.copiapenultimeCloseRSI2 = []

        # Inicialización de valores booleanos y de control
        self.trackTraling = False
        self.trackCurrentprice = False
        self.openTrade = None
        self.tradeFinish = None
        self.first = None
        self.gainprice = None
        self.oncetime = None
        self.entryprice = None
        self.totalquantity = None
        self.quantityPrecision = None
        self.tradeWait = False
        self.side = None
        self.variacionPorcentual = float
        self.tradevariation = float
        self.gainpricevariation = float
        self.firstclose = False
        self.cont = 0
        self.lastrsishort = 0
        self.lastrsilong = 0
        self.warningtradevariation = False
        self.closewithrsi = False
        self.tradeWaitlong = False
        self.setprecisions = False
        self.conected = None
        self.priceprecision = float
        self.firstdatarsi = True
        self.rsitp = 0
        self.pricetp = 0
        self.rsicandelclose = 0
        self.stoploss = 0
        self.shortstoploss = 0
        self.longsstoploss = 0
        self.shortakeprofit = 0
        self.longtakeprofit = 0
        self.firstwin = False
        self.firstlost = False
        self.time = None
        self.closeoperationinshort = False
        self.closeoperationinlong = False
        self.atrshortakeprofit = 0
        self.atrlongtakeprofit = 0
        self.openoperationinshort = False
        self.openoperationinlong = False
        self.crosslong = False
        self.crosshort = False
        self.cross = False
        self.warningcross = False
        self.datacomplete = False
        self.breakeven = False
        self.precisiontrue = False
        self.datacompletersi = False
        self.dfc = None
        self.numero_mayor = 0
        self.numero_menor = 0
        self.pennumero_mayor = 0
        self.pennumero_menor = 0
        self.penclose = None
        self.penopen = None
        self.warninglong = False
        self.warningshort = False
        self.newlastemadistance = 0
        self.mediumlastemaDistance = 0
        self.lastemaDistance = 0
        self.newmediumlastemaDistance = 0
        self.warningdiv = False
        self.cont5 = 0
        self.cont60 = 0
        self.dfh = None
        self.contPenultimeCloseRSI = 0
        self.priclosediv = 0
        self.prirsidiv = 0
        self.priclosedivcopy = 0
        self.prirsidivcopy = 0
        self.dfl = None
    #________ Funcion de telegram para enviar las alertas de los trades automaticos______________#
    def telegram_bot_sendtext(self, bot_message, chat):
        # bot_token = '5119682779:AAGmUeE_uhgtpkgyJeNfwwJk-lKqv-3O1l0' # token del bot de alertas
        # bot_chatID = '-1001568710298' #id del canal
        # bot_chatID = '-1001651140679'  # id del grupo
        bot_chatID = '1047012585' #id del bot
        # bot_token = '5351042739:AAE3KWXgwugEwKOiEmxjO845PIG_hkENQl0'  # token del bot solo dmi
        # bot_token = '5341709591:AAH_XqNnh4BdOdInrKkIkVTHOl9I48EckuY'  # token del bot solo rsi035
        if chat == 1:
            bot_token = '5366902621:AAEagqYH7BFmTS0GAUqI3cVw4IJplokhmh4'  # token del bot solo rsi
        if chat == 2:
            bot_token = '7041551448:AAFcShKMteOb3CqDU0Xb3a3nrwmoyjnJU58'
            # 5372018320:AAEo8cDu22hTbUN1_Sq9HPY_ORc9Qsp4Ur8
        if chat == 3:
            bot_token = '7772811029:AAG5tcxwSFfGBJF3b3WWDxGBwqQyBW_FDhw'

        if chat == 4:
            bot_token = '7533914172:AAHAx_7O5O6EXnVwizjfFWMXTlxsS-B-VEg'

        if chat == 5:
            bot_token = '7270058132:AAF5Ow5MGmjdx36xLojbniGiZv-TiWvu6d4'
        
        enviar_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID \
                    + '&parse_mode=Markdown&text=' + str(bot_message)
        while True:
            try:
                response = requests.get(enviar_text)
                return response.json()
            except Exception:
                continue
    #____________________Funcion para calcular los porcentajes de las criptomonedas______________
    def on_message(self, ws, message, PAR, clientfutures):
        # print("Entro en el on_message")
        
        try:
            # print(f"Estado actual de {self.PAR}: {self.activeSignal}")            

            # Guardo en un json lo que me envia el socket
            json_message = json.loads(message)
            cs = json_message['k']
            # candle_close, close, high, low = cs['x'], round(float(cs['c'], self.priceprecision)), round(float(cs['h']), self.priceprecision), round(float(cs['l'], self.priceprecision))
            candle_close, close, high, low, lopen = cs['x'], float(cs['c']), float(cs['h']), float(cs['l']), float(cs['o'])
            # ______Cuando la vela de 3m cierra entrara en esta condicion________
            # print("candle_close ", candle_close)
            # print("Active Signal ", activeSignal)
            """ print(f'Precio Actual de {PAR} - {close}')
            print("interval ", interval) """
            # print("Precio Actual ", close)
            if candle_close:
                # print(f"Estado actual de {self.PAR}: {self.activeSignal}") 
                closeprice = close
                highprice  = high
                lowprice   = low
                # En esta lista guardo el penultimo close
                self.penultimeCloseRSI.append(close)
                # print("close adentro ",close)
                if len(self.penultimeCloseRSI) == 2:
                    penultimeCloseDiv = self.penultimeCloseRSI[0]
                    # print(f'penultimeCloseDiv {penultimeCloseDiv}')
                    self.contPenultimeCloseRSI += 1
                    # self.copiapenultimeCloseRSI = self.penultimeCloseRSI.copy()
                    # print(f'self.penultimeCloseRSI {self.penultimeCloseRSI}')
                    self.penultimeCloseRSI.pop(0)
                    # print(f'self.penultimeCloseRSI {self.penultimeCloseRSI}')
                    

                # En esta lista guardo el penultimo open
                self.penultimeOpenRSI.append(lopen)            
                if len(self.penultimeOpenRSI) == 2:
                    penultimeOpenDIV = self.penultimeOpenRSI[0]
                    self.penultimeOpenRSI.pop(0)
                    

                # print("Active Signal ", activeSignal)
                # print(candle_close)
                if self.tradeWait is True:
                    self.tradeWaitlist.append(low)
                if len(self.tradeWaitlist) == 60:
                    self.tradeWaitlist.clear()
                    self.tradeWait = False
                if self.tradeWaitlong is True:
                    self.tradeWaitlistlong.append(low)
                if len(self.tradeWaitlistlong) == 20:
                    self.tradeWaitlistlong.clear()
                    self.tradeWaitlong = False
                if self.firstclose is False:
                    while True:
                        resultdatarsi = datarsi(self.PAR, self.interval)
                        # print("resuldata ", resultdatarsi)
                        self.datacompletersi = resultdatarsi[1]
                    
                        if self.datacompletersi is True:
                            # print("Data completa desde newcheck")
                            self.lista_precios_cierre = resultdatarsi[0]
                            self.lista_precios_altos = resultdatarsi[2]
                            self.lista_precios_bajos = resultdatarsi[3]
                            # print(self.lista_precios_altos)
                            # print(self.lista_precios_bajos)
                            # print(self.lista_precios_cierre)
                            break
                        else:
                            sleep(60)
                    
                    # self.lista_precios_cierre = datarsi(PAR, interval)
                    # print("lista antes ",self.lista_precios_cierre)
                    if self.precisiontrue is False:
                        while True:
                            try:
                                self.precisions = precision(self.PAR)
                                if self.precisions is None or self.precisions[1] == 0:
                                    pass
                                else:
                                    self.quantityPrecision = self.precisions[0]
                                    self.priceprecision = self.precisions[1]
                                    self.precisiontrue = True
                                    break
                                
                            except Exception as error:
                                objprecision = open('/home/angel/Documentos/botscalping/errorgetprecision.txt','w')  # ruta linux
                                objprecision.write(str(error))
                                objprecision.close()
                if self.firstclose is True:
                    # self.lista_precios_cierre[-2] = (float(close))
                    # self.lista_precios_cierre.pop(-2)
                    # self.lista_precios_cierre.append(float(close))
                    self.lista_precios_cierre.pop(0)
                    self.lista_precios_cierre.insert(-1, close)

                    #--------------high-------------------------
                    self.lista_precios_altos.pop(0)
                    self.lista_precios_altos.insert(-1, high)

                    #--------------low-------------------------
                    self.lista_precios_bajos.pop(0)
                    self.lista_precios_bajos.insert(-1, low)
                    """ print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
                    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
                    print("lista despues",self.lista_precios_cierre)
                    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
                    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
                    print("lista posicion 250 ",self.lista_precios_cierre[249])
                    print("lista posicion 249 ",self.lista_precios_cierre[248]) """
                    pass
                if self.datacompletersi is True:
                    self.firstclose = True                        
            if self.firstclose is True:
                """ # self.lista_precios_cierre.pop()
                dic_lpc = {"precios_cierre": self.lista_precios_cierre}
                # print("dic_lpc ", len(dic_lpc))
                # print("dic_lpc ", dic_lpc)
                dataframe = DataFrame(dic_lpc)
                diferencia = dataframe["precios_cierre"].diff(1)
                positivos = diferencia.copy()
                negativos = diferencia.copy()
                positivos[positivos < 0] = 0
                negativos[negativos > 0] = 0
                ema_posotivos = positivos.ewm(com=(14 - 1), adjust= False).mean()
                ema_negativos = abs(negativos.ewm(com=(14 - 1), adjust=False).mean())
                rs = ema_posotivos/ema_negativos
                rsi =  100 - (100/(rs+1))
                rsi_valor = (round(rsi.iloc[-1],2)) """
                """ print("lista antes  ",self.lista_precios_cierre)
                print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
                print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------") """
                # print("cierre ", close)
                # self.lista_precios_cierre.pop(249)
                self.lista_precios_cierre.pop(749)
                self.lista_precios_cierre.append(close)
                # print("lista despues ",self.lista_precios_cierre)
                # print("RSI: ", rsi_valor)

                #---------------high--------------------------
                # self.lista_precios_altos.pop(249)
                self.lista_precios_altos.pop(749)
                self.lista_precios_altos.append(high)

                #---------------low--------------------------
                # self.lista_precios_bajos.pop(249)
                self.lista_precios_bajos.pop(749)
                self.lista_precios_bajos.append(low)
                
                if candle_close is True:
                    
                    auxlista = self.lista_precios_cierre.copy()
                    # print(len(auxlista))
                    auxlista.pop(-1)
                    dic_lpc = {"Close": auxlista} 
                    cdf = DataFrame(dic_lpc)
                    self.dfc = cdf.get('Close')
                    # ema_values = dsema(auxlista, 59)
                    # std_deviation = calculate_standard_deviation(auxlista, ema_values)
                    # print(std_deviation)
                    """ print("lista  ",auxlista)
                    print (ema_values)
                    print(len(auxlista))
                    print(len(ema_values)) """
                    # En esta lista guardo el penultimo precio
                    self.penultimeClose.append(closeprice)
                    # print("cierres ", self.penultimeClose)
                    # rsi_valor = indicatorrsi(self.dfc)
                    """ penrsi = rsi_valor[0]
                    # antrsi = rsi_valor[2]
                    lastrsi = rsi_valor[1]
                    print("lasrsi ",lastrsi)
                    print("penrsi ",penrsi) """

                    # -----------------high------------------
                    auxlistahigh = self.lista_precios_altos.copy()
                    auxlistahigh.pop(-1)
                    dic_lph = {"High": auxlistahigh} 
                    cdfh = DataFrame(dic_lph)
                    self.dfh = cdfh.get('High')
                    self.penultimeHigh.append(highprice)

                    # -----------------low------------------
                    auxlistalow = self.lista_precios_bajos.copy()
                    auxlistalow.pop(-1)
                    dic_lpl = {"Low": auxlistalow} 
                    cdfl = DataFrame(dic_lpl)
                    self.dfl = cdfl.get('Low')
                    self.penultimeLow.append(lowprice)                    
                    self.datacomplete = True

                if self.tradeWait is False:
                    
                        if self.activeSignal is True:
                            """ if self.side == 'BUY':
                                # self.longtakeprofit = close
                                self.closeoperationinlong = True
                            if self.side == 'SELL':
                                self.closeoperationinshort = True
                                # self.shortakeprofit = close """

                            """ if close > self.entryprice:
                                if self.side == 'BUY':
                                    # self.longtakeprofit = close
                                    self.closeoperationinlong = True
                            if close < self.entryprice:
                                if self.side == 'SELL':
                                    self.closeoperationinshort = True
                                    # self.shortakeprofit = close """
                            
                            """ rsi_valor = indicatorrsi(self.dfc)
                            penrsi = rsi_valor[0]
                            # antrsi = rsi_valor[2]
                            lastrsi = rsi_valor[1]
                            # print(lastrsi)
                            self.datacomplete = False """

                        if self.activeSignal is False:
                            
                            """ resultsdata = data(PAR, interval, self.cross)
                            # if resultsdata != 500:
                            # print(type(resultsdata))
                            # print(resultsdata)
                            self.dfc = resultsdata[0]
                            self.dfh = resultsdata[1]
                            self.dfl = resultsdata[2]
                            dfo = resultsdata[3]
                            self.datacomplete = resultsdata[4]
                            self.penclose     = resultsdata[5]
                            penhigh      = resultsdata[6]
                            penlow       = resultsdata[7]
                            self.penopen      = resultsdata[8]
                            antpenclose  = resultsdata[9]
                            antpenhigh   = resultsdata[10]
                            antpenlow    = resultsdata[11]
                            antpenopen   = resultsdata[12] """                        

                            # if self.datacomplete is True and changeconsult is True:
                            if self.datacomplete is False:
                                # print("Data Incompleta")
                                pass
                            if self.datacomplete is True:
                                # print("Data completa")  
                                # print("self.dfc ", self.dfc)                     

                                rsi_valor = indicatorrsi(self.dfc)
                                penrsi = rsi_valor[0]
                                # antrsi = rsi_valor[2]
                                lastrsi = rsi_valor[1]
                                # print(lastrsi)

                                """ macd = indicatormacd(self.dfc)
                                lasmacd    = macd[0]
                                penmacd    = macd[1] """

                                resultsAdx = indicatoradx(self.dfh, self.dfl, self.dfc)
                                dmp = resultsAdx[0]
                                dmn = resultsAdx[1]
                                adxvalor = resultsAdx[2]
                                penadx = resultsAdx[3]

                                atr_valor = round(indicatoratr(self.dfc, self.dfh, self.dfl), self.priceprecision)
                                self.shortstoploss = round((close + atr_valor * 2.0), self.priceprecision)
                                self.longsstoploss = round((close - atr_valor * 2.0), self.priceprecision)
                                self.shortakeprofit = round((close - atr_valor * 2.0), self.priceprecision)
                                self.longtakeprofit = round((close + atr_valor * 2.0), self.priceprecision)

                                """ print("priceprecision ", self.priceprecision)

                                print("shortstoploss ", self.shortstoploss)
                                print("longstoploss  ", self.longsstoploss)
                                print("--------------------------------")
                                print("shortakeprofit ", self.shortakeprofit)
                                print("longtakeprofit ", self.longtakeprofit)
                                print("--------------------------------")
                                print("atr ", atr_valor) """

                                """ rsi_valor2 = indicatorrsi2(self.dfc)
                                penrsi2 = rsi_valor2[0]
                                # antrsi = rsi_valor[2]
                                lastrsi2 = rsi_valor2[1] """

                                resultsEmas = Mediamovilexponencial(self.dfc)
                                lastema200      = round(resultsEmas[2], self.priceprecision)
                                """ lastEma20       = round(resultsEmas[0], self.priceprecision)
                                penEma20        = round(resultsEmas[1], self.priceprecision)                                
                                penema200       = round(resultsEmas[3], self.priceprecision)
                                lastema100      = round(resultsEmas[4], self.priceprecision)
                                penema100       = round(resultsEmas[5], self.priceprecision) """
                                """ print("lastema50 ", lastEma50)
                                print("penema50 ", penEma50)
                                print("lastema100 ", lastema100)
                                print("penema100 ", penema100)
                                print("lastema200 ", lastema200)
                                print("penema200 ", penema200) """
                                self.datacomplete = False

                                if penrsi < 70 and lastrsi > 70 and adxvalor >= 25 and adxvalor > penadx and dmn <=15 and dmp >=30 and close > lastema200 and dmp > adxvalor:
                                    # self.openoperationinlong = True
                                    self.openoperationinshort = True

                                if penrsi > 30 and lastrsi < 30 and adxvalor >= 25 and adxvalor > penadx and dmp >=30 and dmn <=15 and close < lastema200 and dmn > adxvalor:
                                    # self.openoperationinshort = True
                                    self.openoperationinlong = True                                         

                                if self.openoperationinshort is True:
                                    self.openoperationinshort = False
                                    # self.crosshort = False
                                    # self.cross = False
                                    # self.newlastemadistance = self.lastemaDistance * -1
                                    now = datetime.now()
                                    auxtime = str(now)
                                    self.time = auxtime[:-10]
                                    self.side = "SELL"
                                    self.entryprice = float(close)
                                    self.openTrade = True
                                    self.first = True
                                    # print("Entro en el si de la señal")
                                    self.activeSignal = True
                                    try:
                                        objficherointents = open(self.base_directory + self.PAR+'S.txt', 'w')
                                        objficherointents.write('tradeopen')
                                        objficherointents.close()
                                    except Exception:
                                        pass
                                    # Me conecto al cliente de binance
                                    
                                    try:
                                        self.clientfutures = ClientFutures(API_KEY, API_SECRET, base_url="https://fapi.binance.com")
                                        self.conected = True
                                        # break
                                    except Exception:
                                        pass                                                

                                if self.openoperationinlong is True:
                                    self.openoperationinlong = False
                                    # self.crosslong = False
                                    # self.cross = False
                                    # self.newlastemadistance = self.lastemaDistance * -1
                                    now = datetime.now()
                                    auxtime = str(now)
                                    self.time = auxtime[:-10]
                                    self.side = "BUY"
                                    self.entryprice = float(close)
                                    self.openTrade = True
                                    self.first = True
                                    # print("Entro en el si de la señal")
                                    self.activeSignal = True
                                    try:
                                        objficherointents = open(self.base_directory + self.PAR+'S.txt', 'w')
                                        objficherointents.write('tradeopen')
                                        objficherointents.close()
                                    except Exception:
                                        pass
                                    # Me conecto al cliente de binance
                                    
                                    try:
                                        self.clientfutures = ClientFutures(API_KEY, API_SECRET, base_url="https://fapi.binance.com")
                                        self.conected = True
                                    except Exception:
                                        pass

            # Aqui obtengo el precio actual de la moneda
            currentprice = close
            
            # En esta lista guardo el penultimo precio
            self.penultimePrice.append(currentprice)
            
            if len(self.penultimePrice) == 2:
                self.penultimePrice.pop(0)

            # Aqui abro la posicion a precio de mercado para los shorts
            if self.side == "SELL":
                # if self.openTrade is True and openorders() is True
                if self.openTrade is True and self.conected is True:
                    self.totalquantity = 10 / self.entryprice
                    try:
                        # self.clientfutures.new_order(symbol=self.PAR, self.side="SELL", type="MARKET", quantity=round(self.totalquantity, self.quantityPrecision), recvWindow=6000)
                        """ newtrade = self.clientfutures.new_order(symbol=self.PAR, self.side="SELL", type="MARKET", quantity=round(self.totalquantity, self.quantityPrecision), recvWindow=6000)
                        logging.info(newtrade) """
                        # print("Se abrio short a precio de mercado ",close)
                        """ print(f'self.newlastemadistance {self.newlastemadistance}')
                        print(type(self.lastemaDistance))
                        print(type(self.mediumlastemaDistance)) """
                        self.tradeFinish = False
                        self.openTrade = False
                        self.telegram_bot_sendtext(f"🔴S Nuevo Short Abierto: {'$' + self.PAR}, {'Entrada ' + str(close)}, {'TP ' + str(self.shortakeprofit)}, {'SL ' + str(self.shortstoploss)}", 2)  
                        # self.telegram_bot_sendtext(f"🔴S Nuevo Short Abierto: {'$' + self.PAR}, {'Entrada ' + str(close)}, {'TP ' + str(self.shortakeprofit)}, {'SL ' + str(self.shortstoploss)}, {'PenMacd ' + str(penmacd)}, {'LastMacd ' + str(lasmacd)}", 2)                    
                        # test = telegram_bot_sendtext(f"🔴S Nuevo Trade Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, \
                        # {'RSI ' + str(rsi_valor)}, {'SL ' + str(self.shortstoploss)} , {'TP ' + str(self.longsstoploss)}",  True)
                        # test = telegram_bot_sendtext(f"🔴S Nuevo Trade Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, \
                        # {'RSI ' + str(rsi_valor)}, {'SL ' + str(self.shortstoploss)}, {'TP ' + str(self.shortakeprofit)}, {'CHG ' + str(change24)}",  True)
                        # telegram_bot_sendtext(f"🔴S Nuevo Short Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, {'EMA Dis ' + str(self.lastemaDistance)+'%'}, {'Media EMA Dis ' + str(self.mediumlastemaDistance)+'%'}", True)
                        # telegram_bot_sendtext(f"🔴S Nuevo Short Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, {'PenRsi' + str(penrsi)}, {'LastRsi ' + str(lastrsi)}, self.mediumlastemaDistance {self.mediumlastemaDistance}, self.newmediumlastemaDistance {self.newmediumlastemaDistance}, self.priclosediv {self.priclosediv}, self.prirsidiv {self.prirsidiv}, penultimeCloseDiv {penultimeCloseDiv}, self.priclosedivcopy {self.priclosedivcopy} self.prirsidivcopy {self.prirsidivcopy}", 2)
                        # test = telegram_bot_sendtext(f"🔴S Nuevo Trade Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, {'SL ' + str(self.shortstoploss)}, {'TP ' + str(self.shortakeprofit)}", True)
                        """ test = telegram_bot_sendtext(f"🔴S Nuevo Trade Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, \
                        {'SL ' + str(self.shortstoploss)}, {'TP ' + str(self.atrshortakeprofit)}, {'ATRSS ' + str(atrshortstoploss)}, {'PENBBU ' + str(penbbu)}", True) """
                        """ test = telegram_bot_sendtext(f"🔴S Nuevo Trade Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, \
                        {'SL ' + str(self.shortstoploss)}", True) """
                    except ClientError as error:
                        # print("Error inesperado al abrir el trade no se abrio ", self.PAR)
                        self.tradeFinish = True
                        self.openTrade = False
                        self.oncetime = True
                        self.telegram_bot_sendtext(f" Error al abrir el trade no se abrio {self.PAR}", 2)
                        # activeSignal =False
                        objerroropentrade = open(self.base_directory  + self.PAR+ '.log'', w')  # ruta linux
                        objerroropentrade.write(str(error))
                        objerroropentrade.close()
                    # test = telegram_bot_sendtext(f"🔴S Nuevo Trade Abierto Variacion de : {'$' + self.PAR}, {str(variacionRedondeada)} %, {'Entrada ' + str(self.entryprice)}")
                if self.tradeFinish is False:
                    # print("entro en trade finish = False")
                    # print("Entry price ", self.entryprice)
                    # print("Currente price ", currentprice)
                    if self.entryprice != currentprice:
                        try:
                            self.tradevariation = round((self.entryprice - currentprice) / currentprice * 100, 3)
                        except Exception:
                            pass
                        # print(f'Variacion de {self.PAR}: {self.tradevariation}')
                        # print("Variacion del trade", self.tradevariation)
                        # print("-------------------")
                        """ print("type de currentprice ", type(currentprice))
                        print("currentprice  ", currentprice)
                        print("type de sl", type(self.shortstoploss))
                        print("SL ", self.shortstoploss) """
                        """ print("type de sl    ", type(self.shortstoploss))
                        print("self.shortstoploss ", self.shortstoploss)  """               
                        # if self.tradevariation < -1.0 and self.closewithrsi is False:
                        # if currentprice > self.shortstoploss or rsirealtime > 70:
                        """ if self.tradevariation >= 0.40 :
                            self.breakeven = True
                            self.entryprice = currentprice  """
                        # if self.tradevariation < self.newmediumlastemaDistance:
                        # if self.tradevariation < self.lastemaDistance:
                        # if self.tradevariation < -0.8:
                        # if rsirealtime > 70:
                        # if currentprice > self.shortstoploss or self.rsicandelclose > 70:
                        if currentprice > self.shortstoploss:
                        # if currentprice > self.stoploss:
                            # print("La variacion supero el limite negativo")
                            # Aqui mando la orden a mercado para cerrar la posicion ya que esta en -0.30 de perdid
                            while True:
                                try:
                                    # self.clientfutures.new_order(symbol=self.PAR, self.side="BUY", type="MARKET", quantity=round(self.totalquantity, self.quantityPrecision), recvWindow=6000)
                                    """ closetrade = self.clientfutures.new_order(symbol=self.PAR, self.side="BUY", type="MARKET", quantity=round(self.totalquantity, self.quantityPrecision), recvWindow=6000)
                                    logging.info(closetrade)
                                    objerrorclosetrade = open(self.base_directory  +self.PAR+ '.log','w')  # ruta linux
                                    objerrorclosetrade.write(str(closetrade))
                                    objerrorclosetrade.close() """
                                    # print("Se cerro la operacion en stoploss")
                                    self.tradeFinish = True
                                    self.openTrade = False
                                    self.oncetime = True
                                    # self.tradeWait = True
                                    # self.cont +=1
                                    if self.firstlost is False:
                                        #____________para crear el archivo y emular el saldo de de 10 dolares
                                        objficherointents = open(self.base_directory +self.PAR+'.txt', 'w')
                                        # objficherointents = open("intents.txt", 'w')
                                        initialbalance = 10
                                        newbalance = (((initialbalance * self.tradevariation) / 100) + initialbalance) / 1.001
                                        objficherointents.write(str(newbalance))
                                        objficherointents.close()

                                        #____________para crear el archivo y contar las veces perdedoras
                                        objficherocont = open(self.base_directory +self.PAR+'p.txt', 'w')
                                        newcont = 1
                                        objficherocont.write(str(newcont))
                                        objficherocont.close()

                                        #____________para crear el archivo y contar las veces ganadoras
                                        objficherocont = open(self.base_directory +self.PAR+'g.txt', 'w')
                                        newcont = 0
                                        objficherocont.write(str(newcont))
                                        objficherocont.close()
                                        self.firstlost = True
                                        self.firstwin  = True   
                                    else:
                                        #____________para emular el saldo de de 10 dolares
                                        objinitalbalance = open(self.base_directory  +self.PAR+ '.txt')
                                        initialbalance = float(objinitalbalance.read())
                                        objinitalbalance.close()
                                        
                                        objficherointents = open(self.base_directory +self.PAR+'.txt', 'w')
                                        # objficherointents = open("intents.txt", 'w')
                                        newbalance = (((initialbalance * self.tradevariation) / 100) + initialbalance) / 1.001
                                        objficherointents.write(str(newbalance))
                                        objficherointents.close()
                                                                
                                        #____________para contar las veces perdedoras
                                        objinitalcont = open(self.base_directory  +self.PAR+ 'p.txt')
                                        initialcont = int(objinitalcont.read())
                                        objinitalcont.close()
                                        
                                        objficherocont = open(self.base_directory +self.PAR+'p.txt', 'w')
                                        # objficherointents = open("intents.txt", 'w')
                                        newcont = initialcont + 1
                                        objficherocont.write(str(newcont))
                                        objficherocont.close()
                                    break
                                except ClientError as error:
                                    objerrorclosetrade = open(self.base_directory  +self.PAR+ '.log','w')  # ruta linux
                                    objerrorclosetrade.write(str(error))
                                    objerrorclosetrade.close()
                                    # print(error)
                                    continue
                            # test = telegram_bot_sendtext(f"Stop loss Short {self.PAR}, {'Variacion ' + str(round(self.tradevariation,3))}, {'Salida ' + str(currentprice)}, {'RSIS ' + str(self.rsicandelclose)}", True)
                            self.telegram_bot_sendtext(f"Stop loss Short {self.PAR}, {'Variacion ' + str(round(self.tradevariation,3))}, {'Salida ' + str(currentprice)},{'Hora Entrada ' + self.time}", 2)
                            try:
                                objficherointents = open(self.base_directory +self.PAR+'S.txt', 'w')
                                objficherointents.write('tradeclose')
                                objficherointents.close()
                            except Exception as error:
                                # print(error)
                                pass
                        # if self.tradevariation >= self.newlastemadistance and self.first is True and self.tradeFinish is False:
                        # if self.tradevariation >= self.mediumlastemaDistance and self.first is True and self.tradeFinish is False:
                        # if self.tradevariation >= 0.8 and self.first is True and self.tradeFinish is False:
                        # if self.tradevariation > 0.10 and self.first is True and self.tradeFinish is False:
                        # if close > ema16 or self.tradevariation > 0.50 and self.first is True and self.tradeFinish is False:
                        # if close < ema16 and self.first is True and self.tradeFinish is False:
                        # if currentprice > self.longsstoploss or self.tradevariation > 0.50 and self.first is True and self.tradeFinish is False:
                        # if self.tradevariation > 0.15 and self.first is True and self.tradeFinish is False:
                        # if lastrsi < 50 and self.first is True and self.tradeFinish is False:
                        # if rsirealtime < 55 or currentprice < self.longsstoploss and self.first is True and self.tradeFinish is False:
                        # if rsirealtime < 55 or self.tradevariation > 0.60 or currentprice < self.longsstoploss and self.first is True and self.tradeFinish is False:
                        # if rsirealtime < 55 or self.tradevariation > 0.50 and self.first is True and self.tradeFinish is False:
                        # if currentprice < self.longsstoploss and self.first is True and self.tradeFinish is False:
                        # if rsirealtime < 51 or self.tradevariation > 0.50 and self.first is True and self.tradeFinish is False:
                        # if currentprice <= self.atrshortakeprofit and self.first is True and self.tradeFinish is False:
                        # if self.tradevariation >= self.shortakeprofit and self.first is True and self.tradeFinish is False:
                        # if self.closeoperationinshort is True or self.tradevariation > 0.30 and self.first is True and self.tradeFinish is False:
                        if currentprice <= self.shortakeprofit and self.first is True and self.tradeFinish is False:
                        # if self.closeoperationinshort is True and self.first is True and self.tradeFinish is False:
                            # self.rsitp = rsirealtime
                            self.pricetp = currentprice
                            self.gainprice = currentprice
                            self.first = False
                            self.trackTraling = True
                            # print("Se guardo el precio de ganancia ", self.gainprice)
                        # Aqui arriba la variable self.first es false porque ya estamos por encima del 0.60% de ganancia

                        # Aqui activo el seguimiento del penultimo precio en tiempo real
                        if self.trackTraling:
                            if self.gainprice > self.penultimePrice[0]:
                                self.gainprice = self.penultimePrice[0]

                        # Aqui activo el seguimiento del trade para cuando se devuelva 0.10% en relacion al penultimo precio
                        if self.first is False:
                            if self.gainprice != currentprice:
                                try:
                                    self.gainpricevariation = (self.gainprice - currentprice) / currentprice * 100
                                except Exception:
                                    pass
                                # print("Variacion del traling ", self.gainpricevariation)
                                # if self.gainpricevariation >= 0.0001 or self.gainpricevariation > -0.10:
                                if self.gainpricevariation >= 0.0001 or self.gainpricevariation > -0.02:
                                    pass
                                    # Dejamos que corra el trade
                                else:
                                    # Se esta regresando en nuestra contra el trade cerramos la operacion
                                    while True:
                                        try:
                                            # self.clientfutures.new_order(symbol=self.PAR, self.side="BUY", type="MARKET", quantity=round(self.totalquantity, self.quantityPrecision), recvWindow=6000)
                                            """ takeprofit = self.clientfutures.new_order(symbol=self.PAR, self.side="BUY", type="MARKET", quantity=round(self.totalquantity, self.quantityPrecision), recvWindow=6000)
                                            logging.info(takeprofit)
                                            objerrortakeprofit = open(self.base_directory  +self.PAR+ '.log','w')  # ruta linux
                                            objerrortakeprofit.write(str(takeprofit))
                                            objerrortakeprofit.close() """
                                            # print("Se cerro la operacion en takeprofit ", self.tradevariation)
                                            self.tradeFinish = True
                                            self.openTrade = False
                                            self.oncetime = True
                                            # self.cont = 0
                                            # self.tradeWait = True
                                            if self.firstwin is False:
                                                #____________para crear el archivo y emular el saldo de de 10 dolares
                                                objficherointents = open(self.base_directory +self.PAR+'.txt', 'w')
                                                # objficherointents = open("intents.txt", 'w')
                                                initialbalance = 10
                                                newbalance = (((initialbalance * self.tradevariation) / 100) + initialbalance) / 1.001
                                                objficherointents.write(str(newbalance))
                                                objficherointents.close()

                                                #____________para crear el archivo y contar las veces perdedoras
                                                objficherocont = open(self.base_directory +self.PAR+'g.txt', 'w')
                                                newcont = 1
                                                objficherocont.write(str(newcont))
                                                objficherocont.close()

                                                #____________para crear el archivo y contar las veces perdedoras
                                                objficherocont = open(self.base_directory +self.PAR+'p.txt', 'w')
                                                newcont = 0
                                                objficherocont.write(str(newcont))
                                                objficherocont.close()
                                                self.firstwin = True
                                                self.firstlost= True   
                                            else:
                                                #____________para emular el saldo de de 10 dolares
                                                objinitalbalance = open(self.base_directory  +self.PAR+ '.txt')
                                                initialbalance = float(objinitalbalance.read())
                                                objinitalbalance.close()
                                                
                                                objficherointents = open(self.base_directory +self.PAR+'.txt', 'w')
                                                # objficherointents = open("intents.txt", 'w')
                                                newbalance = (((initialbalance * self.tradevariation) / 100) + initialbalance) / 1.001
                                                objficherointents.write(str(newbalance))
                                                objficherointents.close()
                                                                        
                                                #____________para contar las veces perdedoras
                                                objinitalcont = open(self.base_directory  +self.PAR+ 'g.txt')
                                                initialcont = int(objinitalcont.read())
                                                objinitalcont.close()
                                                
                                                objficherocont = open(self.base_directory +self.PAR+'g.txt', 'w')
                                                # objficherointents = open("intents.txt", 'w')
                                                newcont = initialcont + 1
                                                objficherocont.write(str(newcont))
                                                objficherocont.close()
                                            break
                                        except ClientError as error:
                                            objerrortakeprofit = open(self.base_directory  +self.PAR+ '.log','w')  # ruta linux
                                            objerrortakeprofit.write(str(error))
                                            objerrortakeprofit.close()
                                            # print(error)
                                            continue
                                    # test = telegram_bot_sendtext(f"Take profit Short {round(self.tradevariation,3)} - {self.PAR}, {'Salida ' + str(currentprice)}, {'RSIS ' + str(self.rsicandelclose)}, {'PTP ' + str(self.pricetp)}", True)
                                    self.telegram_bot_sendtext(f"Take profit Short {round(self.tradevariation,3)} - {self.PAR}, {'Salida ' + str(currentprice)}, {'PTP ' + str(self.pricetp)},{'Hora Entrada ' + self.time}", 2)
                                    try:
                                        objficherointents = open(self.base_directory +self.PAR+'S.txt', 'w')
                                        objficherointents.write('tradeclose')
                                        objficherointents.close()
                                    except Exception as error:
                                        # print(error)
                                        pass
                                    
                                    
            # Aqui abro la posicion a precio de mercado para longs
            if self.side == "BUY":
                if self.openTrade is True and self.conected is True:
                    self.totalquantity = 10 / self.entryprice
                    try:
                        # self.clientfutures.new_order(symbol=self.PAR, self.side="BUY", type="MARKET", quantity=round(self.totalquantity, self.quantityPrecision), recvWindow=6000)
                        """ newtrade = self.clientfutures.new_order(symbol=self.PAR, self.side="BUY", type="MARKET", quantity=round(self.totalquantity, self.quantityPrecision), recvWindow=6000)
                        logging.info(newtrade) """
                        # print("Se abrio long a precio de mercado ", close)
                        """ print(f'self.newlastemadistance {self.newlastemadistance}')
                        print(type(self.lastemaDistance))
                        print(type(self.mediumlastemaDistance)) """
                        self.tradeFinish = False
                        self.openTrade = False
                        self.telegram_bot_sendtext(f"🟢L Nuevo Long  Abierto: {'$' + self.PAR}, {'Entrada ' + str(close)}, {'TP ' + str(self.longtakeprofit)}, {'SL ' + str(self.longsstoploss)}", 2)
                        # self.telegram_bot_sendtext(f"🟢L Nuevo Long  Abierto: {'$' + self.PAR}, {'Entrada ' + str(close)}, {'TP ' + str(self.longtakeprofit)}, {'SL ' + str(self.longsstoploss)}, {'PenMacd ' + str(penmacd)}, {'LastMacd ' + str(lasmacd)}", 2)
                        # test = telegram_bot_sendtext(f"🟢S Nuevo Trade Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, {'RSI ' + str(rsi_valor)}", True)
                        # test = telegram_bot_sendtext(f"🟢L Nuevo Trade Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, \
                        # {'RSI ' + str(rsi_valor)}, {'SL ' + str(self.longsstoploss)}, {'TP ' + str(self.shortstoploss)}",  True)
                        # test = telegram_bot_sendtext(f"🟢L Nuevo Trade Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, \
                        # {'RSI ' + str(rsi_valor)}, {'SL ' + str(self.longsstoploss)}, {'TP ' + str(self.longtakeprofit)}, {'CHG ' + str(change24)}",  True)
                        # test = telegram_bot_sendtext(f"🟢L Nuevo Trade Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, {'SL ' + str(self.longsstoploss)}, {'TP ' + str(self.longtakeprofit)}",  True)
                        # telegram_bot_sendtext(f"🟢L Nuevo Long Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, {'PenRsi' + str(penrsi)}, {'LastRsi ' + str(lastrsi)}, self.mediumlastemaDistance {self.mediumlastemaDistance}, self.newmediumlastemaDistance {self.newmediumlastemaDistance}, self.priclosediv {self.priclosediv}, self.prirsidiv {self.prirsidiv}, penultimeCloseDiv {penultimeCloseDiv}, self.priclosedivcopy {self.priclosedivcopy} self.prirsidivcopy {self.prirsidivcopy} ",  1)
                        """ test = telegram_bot_sendtext(f"🟢L Nuevo Trade Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, \
                        {'SL ' + str(self.longsstoploss)}, {'TP ' + str(self.atrlongtakeprofit)}, {'ATRLS ' + str(atrlongsstoploss)}, {'PENBBL ' + str(penbbl)}",  True) """
                        """ test = telegram_bot_sendtext(f"🟢L Nuevo Trade Abierto : {'$' + self.PAR}, {'Entrada ' + str(self.entryprice)}, \
                        {'SL ' + str(self.longsstoploss)}",  True) """
                    except ClientError as error:
                        # print("Error inesperado al abrir el trade no se abrio ", self.PAR)
                        self.tradeFinish = True
                        self.openTrade = False
                        self.oncetime = True
                        self.telegram_bot_sendtext(f" Error al abrir el trade no se abrio {self.PAR}", 2)
                        # activeSignal =False
                        objerroropentrade = open(self.base_directory  +self.PAR+ '.log', 'w')  # ruta linux
                        objerroropentrade.write(str(error))
                        objerroropentrade.close()
                    # test = telegram_bot_sendtext(f"🟢L Nuevo Trade Abierto Variacion de : {'$' + self.PAR}, {str(variacionRedondeada)} %, {'Entrada ' + str(self.entryprice)}")

                if self.tradeFinish is False:
                    if self.entryprice != currentprice:
                            try:
                                self.tradevariation = round((self.entryprice - currentprice) / currentprice * 100, 3)
                            except Exception:
                                pass
                            # print(f'Variacion de {self.PAR}: {self.tradevariation}')
                            # print("Variacion del trade", self.tradevariation)
                            # print("-------------------")
                            """ print("type de currentprice ",type(currentprice))
                            print("currentprice  ", currentprice)
                            print("type de ls ", type(self.longsstoploss))
                            print("LS ", self.longsstoploss) """
                            """ print("type de ls    ", type(self.longsstoploss))
                            print("self.longsstoploss ", self.longsstoploss) """ 

                            # if self.tradevariation > self.newmediumlastemaDistance :
                            # if self.tradevariation > self.lastemaDistance :
                            # if self.tradevariation > 0.8 :    
                            # if self.tradevariation > 1.00 and self.closewithrsi is False:
                            # if currentprice < self.longsstoploss or rsirealtime < 30:                        
                            # if rsirealtime < 25:
                            if currentprice < self.longsstoploss:
                            # if currentprice < self.stoploss:
                                # print("La variacion supero el limite negativo")
                                # Aqui mando la orden a mercado para cerrar la posicion ya que esta en -0.30 de perdida
                                while True:
                                    try:
                                        # self.clientfutures.new_order(symbol=self.PAR, self.side="SELL", type="MARKET", quantity=round(self.totalquantity, self.quantityPrecision), recvWindow=6000)
                                        """ closetrade = self.clientfutures.new_order(symbol=self.PAR, self.side="SELL", type="MARKET", quantity=round(self.totalquantity, self.quantityPrecision), recvWindow=6000)
                                        logging.info(closetrade)
                                        objerrorclosetrade = open(self.base_directory  +self.PAR+ '.log','w')  # ruta linux
                                        objerrorclosetrade.write(str(closetrade))
                                        objerrorclosetrade.close()
                                        print(closetrade) """
                                        # print("Se cerro la operacion en stoploss")
                                        self.tradeFinish = True
                                        self.openTrade = False
                                        self.oncetime = True
                                        # self.tradeWait = True
                                        # self.cont +=1
                                        # self.tradeWaitlong = True
                                        newtradevariation = self.tradevariation *-1
                                        if self.firstlost is False:
                                            #____________para crear el archivo y emular el saldo de de 10 dolares
                                            objficherointents = open(self.base_directory +self.PAR+'.txt', 'w')
                                            # objficherointents = open("intents.txt", 'w')
                                            initialbalance = 10
                                            newbalance = (((initialbalance * newtradevariation) / 100) + initialbalance) / 1.001
                                            objficherointents.write(str(newbalance))
                                            objficherointents.close()

                                            #____________para crear el archivo y contar las veces perdedoras
                                            objficherocont = open(self.base_directory +self.PAR+'p.txt', 'w')
                                            newcont = 1
                                            objficherocont.write(str(newcont))
                                            objficherocont.close()

                                            #____________para crear el archivo y contar las veces ganadoras
                                            objficherocont = open(self.base_directory +self.PAR+'g.txt', 'w')
                                            newcont = 0
                                            objficherocont.write(str(newcont))
                                            objficherocont.close()
                                            self.firstlost = True
                                            self.firstwin  = True   
                                        else:
                                            #____________para emular el saldo de de 10 dolares
                                            objinitalbalance = open(self.base_directory  +self.PAR+ '.txt')
                                            initialbalance = float(objinitalbalance.read())
                                            objinitalbalance.close()
                                            
                                            objficherointents = open(self.base_directory +self.PAR+'.txt', 'w')
                                            # objficherointents = open("intents.txt", 'w')
                                            newbalance = (((initialbalance * newtradevariation) / 100) + initialbalance) / 1.001
                                            objficherointents.write(str(newbalance))
                                            objficherointents.close()
                                                                    
                                            #____________para contar las veces perdedoras
                                            objinitalcont = open(self.base_directory  +self.PAR+ 'p.txt')
                                            initialcont = int(objinitalcont.read())
                                            objinitalcont.close()
                                            
                                            objficherocont = open(self.base_directory +self.PAR+'p.txt', 'w')
                                            # objficherointents = open("intents.txt", 'w')
                                            newcont = initialcont + 1
                                            objficherocont.write(str(newcont))
                                            objficherocont.close()
                                        break
                                    except ClientError as error:
                                        objerrorclosetrade = open(self.base_directory  +self.PAR+ '.log','w')  # ruta linux
                                        objerrorclosetrade.write(str(error))
                                        objerrorclosetrade.close()
                                        # print(error)
                                        continue
                                self.telegram_bot_sendtext(f"Stop loss Long {self.PAR}, {'Variacion ' + str(round(self.tradevariation,3))}, {'Salida ' + str(currentprice)},{'Hora Entrada ' + self.time}", 2)
                                # test = telegram_bot_sendtext(f"Stop loss Long {self.PAR}, {'Variacion ' + str(round(self.tradevariation,3))}, {'Salida ' + str(currentprice)}, {'RSIS ' + str(self.rsicandelclose)}", True)
                                try:
                                    objficherointents = open(self.base_directory +self.PAR+'S.txt', 'w')
                                    objficherointents.write('tradeclose')
                                    objficherointents.close()
                                except Exception as error:
                                    # print(error)
                                    pass

                            # if self.tradevariation <= self.newlastemadistance and self.first is True and self.tradeFinish is False:
                            # if self.tradevariation <= self.mediumlastemaDistance  and self.first is True and self.tradeFinish is False:
                            # if self.tradevariation < -0.8 and self.first is True and self.tradeFinish is False:
                            # if currentprice > self.shortstoploss or self.tradevariation < -0.50 and self.first is True and self.tradeFinish is False:    
                            # if close > ema16 and self.first is True and self.tradeFinish is False:
                            # if close > ema16 or self.tradevariation < -0.50 and self.first is True and self.tradeFinish is False:                        
                            # if self.tradevariation < -0.15 and self.first is True and self.tradeFinish is False:
                            # if rsirealtime > 45 or currentprice > self.shortstoploss and self.first is True and self.tradeFinish is False:
                            # if rsirealtime > 45 or currentprice > self.shortstoploss or self.tradevariation < -0.60 and self.first is True and self.tradeFinish is False:
                            # if rsirealtime > 45 or self.tradevariation < -0.50 and self.first is True and self.tradeFinish is False:
                            # if currentprice > self.shortstoploss and self.first is True and self.tradeFinish is False:
                            # if rsirealtime > 49 or self.tradevariation < -0.50 and self.first is True and self.tradeFinish is False:
                            # if currentprice >= self.atrlongtakeprofit and self.first is True and self.tradeFinish is False:
                            # if self.tradevariation <= self.longtakeprofit and self.first is True and self.tradeFinish is False:
                            # if self.closeoperationinlong is True or self.tradevariation < -0.30 and self.first is True and self.tradeFinish is False:
                            if currentprice >= self.longtakeprofit and self.first is True and self.tradeFinish is False:
                            # if self.closeoperationinlong is True and self.first is True and self.tradeFinish is False:
                                self.pricetp = currentprice
                                self.gainprice = currentprice
                                self.first = False
                                self.trackTraling = True
                                # print("Se guardo el precio de ganancia ", self.gainprice)
                            # Aqui arriba la variable self.first es false porque ya estamos por encima del 0.60% de ganancia

                            # Aqui activo el seguimiento del penultimo precio en tiempo real
                            if self.trackTraling:
                                if self.gainprice < self.penultimePrice[0]:
                                    self.gainprice = self.penultimePrice[0]

                            # Aqui activo el seguimiento del trade para cuando se devuelva 0.10% en relacion al penultimo precio
                            if self.first is False:
                                if self.gainprice != currentprice:
                                    try:
                                        self.gainpricevariation = (self.gainprice - currentprice) / currentprice * 100
                                    except Exception:
                                        pass
                                    # print("Variacion del traling ", self.gainpricevariation)
                                    if self.gainpricevariation <= -0.0001 or self.gainpricevariation < 0.02:
                                        pass
                                        # Dejamos que corra el trade
                                    else:
                                        # Se esta regresando en nuestra contra el trade cerramos la operacion
                                        while True:
                                            try:
                                                # self.clientfutures.new_order(symbol=self.PAR, self.side="SELL", type="MARKET", quantity=round(self.totalquantity, self.quantityPrecision), recvWindow=6000)
                                                """ takeprofit = self.clientfutures.new_order(symbol=self.PAR, self.side="SELL", type="MARKET", quantity=round(self.totalquantity, self.quantityPrecision), recvWindow=6000)
                                                logging.info(takeprofit)
                                                objerrortakeprofit = open(self.base_directory  +self.PAR+ '.log','w')  # ruta linux
                                                objerrortakeprofit.write(str(takeprofit))
                                                objerrortakeprofit.close() """
                                                # print("Se cerro la operacion en takeprofit ", self.tradevariation)
                                                self.tradeFinish = True
                                                self.openTrade = False
                                                self.oncetime = True
                                                # self.cont = 1
                                                # self.tradeWaitlong = True
                                                newtradevariation = self.tradevariation *-1
                                                if self.firstwin is False:
                                                    #____________para crear el archivo y emular el saldo de de 10 dolares
                                                    objficherointents = open(self.base_directory +self.PAR+'.txt', 'w')
                                                    # objficherointents = open("intents.txt", 'w')
                                                    initialbalance = 10
                                                    newbalance = (((initialbalance * newtradevariation) / 100) + initialbalance) / 1.001
                                                    objficherointents.write(str(newbalance))
                                                    objficherointents.close()

                                                    #____________para crear el archivo y contar las veces perdedoras
                                                    objficherocont = open(self.base_directory +self.PAR+'g.txt', 'w')
                                                    newcont = 1
                                                    objficherocont.write(str(newcont))
                                                    objficherocont.close()

                                                    #____________para crear el archivo y contar las veces perdedoras
                                                    objficherocont = open(self.base_directory +self.PAR+'p.txt', 'w')
                                                    newcont = 0
                                                    objficherocont.write(str(newcont))
                                                    objficherocont.close()
                                                    self.firstwin = True
                                                    self.firstlost = True   
                                                else:
                                                    #____________para emular el saldo de de 10 dolares
                                                    objinitalbalance = open(self.base_directory  +self.PAR+ '.txt')
                                                    initialbalance = float(objinitalbalance.read())
                                                    objinitalbalance.close()
                                                    
                                                    objficherointents = open(self.base_directory +self.PAR+'.txt', 'w')
                                                    # objficherointents = open("intents.txt", 'w')
                                                    newbalance = (((initialbalance * newtradevariation) / 100) + initialbalance) / 1.001
                                                    objficherointents.write(str(newbalance))
                                                    objficherointents.close()
                                                                            
                                                    #____________para contar las veces perdedoras
                                                    objinitalcont = open(self.base_directory  +self.PAR+ 'g.txt')
                                                    initialcont = int(objinitalcont.read())
                                                    objinitalcont.close()
                                                    
                                                    objficherocont = open(self.base_directory +self.PAR+'g.txt', 'w')
                                                    # objficherointents = open("intents.txt", 'w')
                                                    newcont = initialcont + 1
                                                    objficherocont.write(str(newcont))
                                                    objficherocont.close()
                                                break
                                            except ClientError as error:
                                                objerrortakeprofit = open(self.base_directory  +self.PAR+ '.log','w')  # ruta linux
                                                objerrortakeprofit.write(str(error))
                                                objerrortakeprofit.close()
                                                # print(error)
                                                continue
                                        # test = telegram_bot_sendtext(f"Take profit Long {round(abs(self.tradevariation),3)} - {self.PAR}, {'Salida ' + str(currentprice)}, {'RSIS ' + str(self.rsicandelclose)}, {'PTP ' + str(self.pricetp)}", True)
                                        self.telegram_bot_sendtext(f"Take profit Long {round(abs(self.tradevariation),3)} - {self.PAR}, {'Salida ' + str(currentprice)},{'PTP ' + str(self.pricetp)},{'Hora Entrada ' + self.time}", 2)
                                        try:
                                            objficherointents = open(self.base_directory +self.PAR+'S.txt', 'w')
                                            objficherointents.write('tradeclose')
                                            objficherointents.close()
                                        except Exception as error:
                                            # print(error)
                                            pass
                                        
                                    
            if self.tradeFinish is True and self.oncetime is True:
            # if self.tradeFinish is True:
                # print("Entro en trade finish y se cierra el trade")
                # setintents() # Activar cuando valla a ser en real
                self.closeoperationinlong = False
                self.closeoperationinshort = False
                self.oncetime = False
                self.activeSignal = False
                self.trackTraling = False
                self.trackCurrentprice = False
                self.warningtradevariation = False
                self.closewithrsi = False
                self.conected = False
                self.firstdatarsi = True
                """ if self.cont == 1:
                    self.tradeWait = True
                    self.cont = 0    """    
                # client.session.close()
                # print("Active Signal", activeSignal)
                # print("Track Traling", self.trackTraling)
        except Exception as error:

            archivo_path = 'errorgeneral.txt'

            if os.path.exists(archivo_path):
                # Si el archivo existe, abre en modo 'a' para agregar contenido
                with open(archivo_path, 'a') as archivo:
                    # Escribe en una nueva linea
                    archivo.write(str(error))
            else:
                # Si el archivo no existe, crea uno nuevo y escribe en el
                with open(archivo_path, 'w') as archivo:
                    archivo.write(str(error))

            # print("Operacion completada.")


            """ objprecision = open('/home/angel/Documentos/botscalping/errorgeneral.txt','w')  # ruta linux
            objprecision.write(str(error))
            objprecision.close() """
    

    def run(self):
        socket = f'wss://fstream.binance.com/ws/{self.PAR.lower()}@kline_{self.interval}'
        # ws = websocket.WebSocketApp(socket, on_message=lambda ws, msg: self.on_message(ws, msg))
        ws = websocket.WebSocketApp(socket, on_message=lambda ws, msg: self.on_message(ws, msg, self.PAR, self.clientfutures))
        ws.run_forever()

# Lista de pares a monitorear
pares = ['PHAUSDT', 'API3USDT', '1000LUNCUSDT', 'BALUSDT', 'USDCUSDT', 'HIGHUSDT', 'STMXUSDT', 'SHELLUSDT', 'TONUSDT', 'PNUTUSDT', 'USUALUSDT', 'POPCATUSDT', 'MEWUSDT', 'CAKEUSDT', 'SNXUSDT', 'MORPHOUSDT', 'RSRUSDT', 'STRAXUSDT', 'BBUSDT', '1000WHYUSDT', 'BNXUSDT', 'STXUSDT', 'IDEXUSDT', 'DFUSDT', '1000CATUSDT', 'VVVUSDT', 'DOGEUSDT', 'LOOMUSDT', 'POLUSDT', 'HEIUSDT', 'ENJUSDT', 'AXLUSDT', 'DOGSUSDT', 'FISUSDT', 'CTSIUSDT', 'SOLUSDT', 'SYSUSDT', 'KERNELUSDT', 'BADGERUSDT', 'ORDIUSDT', 'WCTUSDT', 'LUMIAUSDT', 'NILUSDT', 'LITUSDT', 'KDAUSDT', 'AEROUSDT', 'VINEUSDT', 'AIXBTUSDT', 'IOUSDT', 'IMXUSDT', 'REZUSDT', 'PARTIUSDT', 'MTLUSDT', 'KLAYUSDT', 'CELOUSDT', 'LOKAUSDT', 'DRIFTUSDT', 'AUCTIONUSDT', 'RADUSDT', 'TOKENUSDT', 'BRETTUSDT', 'LQTYUSDT', 'BICOUSDT', 'NFPUSDT', 'KASUSDT', 'ANKRUSDT', 'FILUSDT', 'CVXUSDT', 'JOEUSDT', 'CHESSUSDT', 'OPUSDT', 'BERAUSDT', 'DYDXUSDT', 'COMBOUSDT', 'AGLDUSDT', 'DIAUSDT', 'STEEMUSDT', 'BMTUSDT', 'ACXUSDT', 'FHEUSDT', 'TLMUSDT', 'AXSUSDT', 'TNSRUSDT', 'COSUSDT', 'ZEREBROUSDT', 'BELUSDT', 'CFXUSDT', 'EIGENUSDT', 'PONKEUSDT', 'ARBUSDT', 'DENTUSDT', 'PUMPUSDT', 'ORCAUSDT', 'DODOXUSDT', 'PENGUUSDT', 'BANKUSDT', 'ENSUSDT', 'SPELLUSDT', 'RPLUSDT', '1000RATSUSDT', 'ACEUSDT', 'ONEUSDT', 'BRUSDT', 'MAVUSDT', 'SOLVUSDT', 'ALGOUSDT', 'ETHWUSDT', 'VANAUSDT', 'POLYXUSDT', 'MANAUSDT', 'ARCUSDT', 'ILVUSDT', 'ACHUSDT', 'LAYERUSDT', 'GLMUSDT', 'KNCUSDT', 'WOOUSDT', 'ATHUSDT', 'IOTXUSDT', 'THETAUSDT', 'NEIROUSDT', 'POWRUSDT', 'CHZUSDT', 'SAFEUSDT', 'XMRUSDT', 'QNTUSDT', 'PEOPLEUSDT', 'CATIUSDT', 'AAVEUSDT', 'PUNDIXUSDT', 'TRUMPUSDT', 'PENDLEUSDT', 'RLCUSDT', '1MBABYDOGEUSDT', 'BATUSDT', 'SCRUSDT', 'HIPPOUSDT', 'UXLINKUSDT', 'QUICKUSDT', 'ASTRUSDT', 'OXTUSDT', 'MKRUSDT', 'ALCHUSDT', 'MOVEUSDT', 'METISUSDT', 'KAITOUSDT', 'DUSKUSDT', 'STORJUSDT', 'MASKUSDT', 'GUSDT', 'DEGENUSDT', 'LINAUSDT', 'ZROUSDT', 'AVAUSDT', 'SANTOSUSDT', 'DUSDT', 'TWTUSDT', 'LISTAUSDT', 'BANDUSDT', 'AERGOUSDT', 'B3USDT', 'YGGUSDT', 'SUIUSDT', 'GOATUSDT', 'RENUSDT', 'BEAMXUSDT', 'GRIFFAINUSDT', 'BCHUSDT', 'IDUSDT', 'MDTUSDT', 'CGPTUSDT', 'MEMEUSDT', 'HIVEUSDT', 'ARPAUSDT', 'COOKIEUSDT', 'OMGUSDT', 'SAGAUSDT', 'IOTAUSDT', 'ARKUSDT', 'MYROUSDT', 'ZECUSDT', 'MUBARAKUSDT', 'WLDUSDT', 'LDOUSDT', 'MAGICUSDT', 'UNFIUSDT', 'RVNUSDT', 'SIGNUSDT', 'GMTUSDT', 'OCEANUSDT', 'SSVUSDT', 'HOOKUSDT', '1000CHEEMSUSDT', 'NEIROETHUSDT', 'REDUSDT', 'STPTUSDT', 'LSKUSDT', 'CYBERUSDT', 'DGBUSDT', '1INCHUSDT', 'KAVAUSDT', 'SFPUSDT', '1000FLOKIUSDT', 'XRPUSDT', 'ANIMEUSDT', 'EPICUSDT', 'GALAUSDT', 'GTCUSDT', 'TRXUSDT', 'UNIUSDT', 'LUNA2USDT', 'SLERFUSDT', 'BANUSDT', 'LINKUSDT', 'DASHUSDT', 'RAYSOLUSDT', 'ATAUSDT', 'SYNUSDT', 'SPXUSDT', 'ARUSDT', 'AIOTUSDT', 'XEMUSDT', 'SXPUSDT', 'RIFUSDT', 'ZILUSDT', 'SXTUSDT', 'XVSUSDT', 'UMAUSDT', 'DYMUSDT', 'QTUMUSDT', 'HBARUSDT', '1000SATSUSDT', 'BTCUSDT', 'BSVUSDT', 'RONINUSDT', 'FLUXUSDT', 'APEUSDT', 'DOTUSDT', 'BAKEUSDT', 'ZENUSDT', 'MELANIAUSDT', 'RAREUSDT', 'BABYUSDT', 'ALICEUSDT', 'STGUSDT', 'WUSDT', 'NMRUSDT', 'GASUSDT', 'APTUSDT', 'DEFIUSDT', 'BTCDOMUSDT', 'BIDUSDT', 'OGNUSDT', 'NKNUSDT', 'HIFIUSDT', 'ONDOUSDT', 'PHBUSDT', 'ALPHAUSDT', 'KMNOUSDT', 'CETUSUSDT', 'IPUSDT', 'FTMUSDT', 'SLPUSDT', 'MANTAUSDT', 'NTRNUSDT', 'INJUSDT', 'TROYUSDT', 'REEFUSDT', 'ADAUSDT', 'AMBUSDT', 'BSWUSDT', 'VIDTUSDT', 'DOLOUSDT', 'VETUSDT', 'BANANAS31USDT', 'SWELLUSDT', 'DEXEUSDT', 'DEEPUSDT', 'JTOUSDT', 'CHRUSDT', 'WAXPUSDT', '1000SHIBUSDT', 'FARTCOINUSDT', 'AEVOUSDT', 'KEYUSDT', 'LPTUSDT', 'C98USDT', 'HOTUSDT', 'SUNUSDT', 'ICXUSDT', 'ALTUSDT', 'KSMUSDT', 'SUPERUSDT', 'SUSDT', 'NEARUSDT', 'JELLYJELLYUSDT', 'BROCCOLIF3BUSDT', 'WALUSDT', 'LTCUSDT', '1000XECUSDT', 'GUNUSDT', 'GLMRUSDT', 'VTHOUSDT', 'VOXELUSDT', 'SONICUSDT', 'COMPUSDT', 'PROMPTUSDT', 'WAVESUSDT', 'MOODENGUSDT', 'BROCCOLI714USDT', 'SANDUSDT', 'MOVRUSDT', 'ATOMUSDT', 'KAIAUSDT', 'BLZUSDT', 'REIUSDT', 'TRUUSDT', 'XTZUSDT', 'VICUSDT', 'HMSTRUSDT', 'PYTHUSDT', 'AKTUSDT', 'FUNUSDT', 'CTKUSDT', 'OMUSDT', 'ETHUSDT', 'AGIXUSDT', 'GRASSUSDT', 'BONDUSDT', 'BNBUSDT', 'PROMUSDT', 'ONGUSDT', 'THEUSDT', 'FETUSDT', 'RUNEUSDT', 'VIRTUALUSDT', 'EGLDUSDT', 'PAXGUSDT', 'DEGOUSDT', 'SUSHIUSDT', 'ROSEUSDT', 'XCNUSDT', 'FORTHUSDT', 'INITUSDT', 'PERPUSDT', 'SWARMSUSDT', 'EPTUSDT', 'GHSTUSDT', 'GMXUSDT', 'FORMUSDT', 'TSTUSDT', 'OMNIUSDT', '1000000MOGUSDT', 'GPSUSDT', 'ZRXUSDT', 'IOSTUSDT', 'YFIUSDT', '1000BONKUSDT', 'LRCUSDT', 'AIUSDT', 'TUTUSDT', 'STOUSDT', 'HAEDALUSDT', 'MLNUSDT', 'TUSDT', 'PLUMEUSDT', 'BIGTIMEUSDT', 'ARKMUSDT', 'FLOWUSDT', 'ZKUSDT', 'XLMUSDT', 'EOSUSDT', 'SEIUSDT', '1000XUSDT', 'LEVERUSDT', 'ENAUSDT', 'ALPACAUSDT', 'SKLUSDT', 'JASMYUSDT', 'MBOXUSDT', 'BNTUSDT', 'NULSUSDT', 'HYPERUSDT', 'BOMEUSDT', 'COWUSDT', 'AVAXUSDT', 'HFTUSDT', 'ONTUSDT', 'ETCUSDT', 'ZETAUSDT', 'BIOUSDT', 'DARUSDT', 'NEOUSDT', 'MAVIAUSDT', 'WIFUSDT', 'JUPUSDT', 'VANRYUSDT', 'MEUSDT', 'FXSUSDT', 'CKBUSDT', 'FIOUSDT', 'SIRENUSDT', 'MINAUSDT', 'TURBOUSDT', 'JSTUSDT', 'PORTALUSDT', 'TIAUSDT', 'CELRUSDT', 'CRVUSDT', 'COTIUSDT', 'BANANAUSDT', 'BLURUSDT', 'ORBSUSDT', 'STRKUSDT', 'PIPPINUSDT', 'ACTUSDT', 'PIXELUSDT', 'CHILLGUYUSDT', 'XVGUSDT', 'SNTUSDT', 'MOCAUSDT', 'EDUUSDT', 'FIDAUSDT', 'USTCUSDT', 'XAIUSDT', 'AVAAIUSDT', 'GRTUSDT', '1000PEPEUSDT', 'AI16ZUSDT', 'TAOUSDT', 'MEMEFIUSDT', 'VELODROMEUSDT', 'RENDERUSDT', 'NOTUSDT', 'ICPUSDT', 'SCRTUSDT', 'RDNTUSDT', 'KOMAUSDT', 'TRBUSDT', 'FLMUSDT', 'ETHFIUSDT']
# pares = ["BTCUSDT"]
interval = "5m"  # Puedes cambiar el intervalo aquí

# Función para iniciar un bot en un proceso separado
def start_bot(par, interval):
    bot = TradingBot(par, interval)
    bot.run()

# Crear y ejecutar procesos en paralelo
if __name__ == "__main__":
    procesos = []

    for par in pares:
        p = multiprocessing.Process(target=start_bot, args=(par, interval))
        p.start()
        procesos.append(p)

    for p in procesos:
        p.join()