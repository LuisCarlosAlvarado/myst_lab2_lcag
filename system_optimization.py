
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A python project for algorithmic trading in FXCM                                           -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- script: requirements.txt : text file with the required libraries for the project                    -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: MIT License                                                                                -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Template repository: https://github.com/IFFranciscoME/trading-project                               -- #
# -- --------------------------------------------------------------------------------------------------- -- #

# Método ineficiente
# Cruce de médias móviles , estrategia long, montecralo para obtener la longitud de medias con mayor rendimiento
import system_desing as sd
import numpy as np
import functions as fn

longitud = []
resultado = []
cierre = sd.train_ohlc['close'] 
open = sd.train_ohlc['open'] 
comision = .001 #ya en porcentaje
capital = 20000
for short_length in range(1,5):
    for long_length in range(1,10):
        for take_profit in np.arange(.025,.055,.005):
            for stop_loss in np.arange(-.005,-.03,-.005):
                if long_length > short_length:  
                    short_ema = fn.ema(serie = cierre, length = short_length)
                    long_ema = fn.ema(serie = cierre, length = long_length)

                    señales = fn.signals(short_ema=short_ema, long_ema=long_ema, serie=cierre)
                    señales_index = fn.signal_index(lista = señales)
                    operaciones = fn.operations(lista = señales_index, precios=open)
                    rend_operacion = fn.open_price_profit(lista = operaciones)
                    rendimiento = fn.profit(lista = rend_operacion, comision = comision,\
                                     take_profit = take_profit, stop_loss = stop_loss)
                    flujo = fn.capital_flow(lista = rendimiento, capital = capital)

                    rend_final = (flujo[-1]/flujo[0] - 1)

                    longitud.append([short_length, long_length, take_profit, stop_loss])
                    resultado.append([rend_final])
                else:
                    continue

rend_max, parametros = max(resultado), longitud[resultado.index(max(resultado))]