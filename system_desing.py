
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
import data as dt
import ta 
dt.con.is_connected()

#Criterio 1
#mid OHLC de 30 min de EUR/USD
#Agosto 2021 a Ene 2022

data_ohlc = dt.fxcm_ohlc('BTC/USD', 'H4' , '2018-01-31 00:00:00', '2021-12-31 23:59:59')

# Visualizar
#len(data_ohlc)
#data_ohlc.head(5)
#data_ohlc.tail(5)

#descripcion
#data_ohlc.describe()
#data_ohlc.info()

#separar conjuntos de entrenamiento, validacion y prueba
train_ohlc = data_ohlc.loc['2018-06-24 21:00:00' :'2020-01-31 23:59:59']
#train_ohlc.head(5)
#train_ohlc.tail(5)

val_ohlc = data_ohlc.loc['2021-02-01 00:00:00' : '2021-03-31 23:59:59']
#val_ohlc.head(5)
#val_ohlc.tail(5)
#val_ohlc.describe()

test_ohlc = data_ohlc.loc['2021-04-01 00:00:00' : '2021-12-31 23:59:59']
#test_ohlc.head(5)
#test_ohlc.tail(5)
#test_ohlc.describe()

# -- Entrenamiento se utiliza todas las veces que sean
# -- Validación se utiliza 5 veces (durante el mismo ciclo que entrenamiento, o, después de haberlo terminado)
# -- Prueba se utiiza 1 vez (Hasta el final)

#Criterio 2
# Obtener media movil exponencial periodo corto y largo
# Comparar cada media entre sí por cada vela 
# Momento en que EMA corto > EMA largo, señal de compra
# Si EMA[t-1] es menor y EMA[t] es mayor, significa que hubo un cruce y se da la señal
# Momento en que EMA corto < EMA largo, señal de venta
# 

#short_ema = train_ohlc['midOpen'].ewm(span=13).mean()
#long_ema = train_ohlc['midOpen'].ewm(span=36).mean()
def ema(close, short_length, long_length):
    short_ema = ta.trend.ema_indicator(close, window=short_length, fillna=False)
    long_ema = ta.trend.ema_indicator(close, window=long_length, fillna=False)

    ema = pd.concat([short_ema,long_ema], axis=1)


#Criterio 3
# tp = 50
# sl = 25

#Criterio 4
# 0.01% del balance
# Balance inicial = 20,000

# -- Backtest
# 1. Operaciones ejecutadas
# 2. Ganancias en Pisps y en $ por operación
# 3. Tiempo de duración
# 4. Deflated Sharpe Ratio