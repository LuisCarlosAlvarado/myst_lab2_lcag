
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A python project for algorithmic trading in FXCM                                           -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- script: requirements.txt : text file with the required libraries for the project                    -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: MIT License                                                                                -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Template repository: https://github.com/IFFranciscoME/trading-project                               -- #
# -- --------------------------------------------------------------------------------------------------- -- #

from cmath import nan
import pandas as pd
import numpy as np
#import data as dt
import functions as fn
import ta 
#dt.con.is_connected()

#Criterio 1
#mid OHLC de 30 min de EUR/USD
#Agosto 2021 a Ene 2022

#data_ohlc = dt.fxcm_ohlc('BTC/USD', 'H4' , '2018-01-31 00:00:00', '2021-12-31 23:59:59')
data_ohlc = pd.read_csv("BTCUSD.csv", index_col="Date")

# Visualizar
#len(data_ohlc)
#data_ohlc.head(5)
#data_ohlc.tail(5)

#descripcion
#data_ohlc.describe()
#data_ohlc.info()

#separar conjuntos de entrenamiento, validacion y prueba
train_ohlc = data_ohlc.loc['31/01/2018' :'31/01/2020']
#train_ohlc.head(5)
#train_ohlc.tail(5)

val_ohlc = data_ohlc.loc['01/02/2021' : '31/03/2021']
#val_ohlc.head(5)
#val_ohlc.tail(5)
#val_ohlc.describe()

test_ohlc = data_ohlc.loc['01/04/2021' : '31/12/2021']
#test_ohlc.head(5)
#test_ohlc.tail(5)
#test_ohlc.describe()

def proceso_completo(cierre, open, comision,\
     short_length, long_length, take_profit, stop_loss, capital):

    cierre = cierre
    open = open
    comision = comision 
    short_length = short_length
    long_length = long_length
    take_profit = take_profit
    stop_loss = stop_loss
    capital = capital

    short_ema = fn.ema(serie = cierre, length = short_length)
    long_ema = fn.ema(serie = cierre, length = long_length)

    señales = fn.signals(short_ema=short_ema, long_ema=long_ema, serie=cierre)
    señales_index = fn.signal_index(lista = señales)
    operaciones = fn.operations(lista = señales_index, precios=open)
    rend_operacion = fn.open_price_profit(lista = operaciones)
    rendimiento = fn.profit(lista = rend_operacion, comision = comision,\
                    take_profit = take_profit, stop_loss = stop_loss)
    flujo = fn.capital_flow(lista = rendimiento, capital = capital)
    resultados = [señales, señales_index, operaciones, rend_operacion, rendimiento, flujo]

    return resultados

