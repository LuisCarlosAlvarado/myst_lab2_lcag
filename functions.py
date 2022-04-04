
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A python project for algorithmic trading in FXCM                                           -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- script: requirements.txt : text file with the required libraries for the project                    -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: MIT License                                                                                -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Template repository: https://github.com/IFFranciscoME/trading-project                               -- #
# -- --------------------------------------------------------------------------------------------------- -- #

import ta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import calendar
import time
from datetime import datetime, timedelta
import string
from pandas.core.common import flatten

#La usaré como decorador para obtener el tiempo de ejecución de cada función
def metrica_computacional(funcion):
    """
    Decorador que evuelve el tiempo que le toma a una función ejecutarse

    Parámetros
    ---------

    funcion: La función de la que quieras obtener el tiempo

    Returns
    -------
    print() del tiempo de ejecución
    
    """
    def funcion_medida(*args, **kwargs):
        inicio = time.time()
        c = funcion(*args, **kwargs)
        print(time.time() - inicio)
        return c
    return funcion_medida

@metrica_computacional
def ema(serie, length):
    """
    Devuelve el promedio móvil exponencial de una serie

    Parámetros
    ----------
    
    serie: Serie de datos de la cuál se obtendrá el promedio móvil exponencial
    length: Longitud del promedio móvil exponencial (¿cuántos datos hacia atrás se tomarán en cuenta?)

    Returns
    -------
    ema: Lista con los promedio móviles exponenciales 

    """
    ema = ta.trend.ema_indicator(serie, window=length, fillna=False)
    return ema

@metrica_computacional
def signals(short_ema, long_ema, serie):
    """
    Devuelve las señales de compra según el cruce de las velas

    Parámetros
    ----------
    
    short_ema: Longitud promedio móvil corto
    long_ema: Longitud promedio móvil largo
    serie: Serie de datos de la cuál se obtendrá el promedio móvil exponencial

    Returns
    -------
    señales: Lista con [0,1,2]
            1 -> Señal de compra 
            0 -> Sin señal
            2 -> Señal de venta

    """
    señales = np.zeros(len(serie))
    for i in range(1,len(serie)):
        if short_ema[i-1] <= long_ema[i-1] and short_ema[i] > long_ema[i]:
            señales[i] = 1
        elif short_ema[i-1] >= long_ema[i-1] and short_ema[i] < long_ema[i]:
            señales[i] = 2
        else:
            señales[i] = 0
    return señales

@metrica_computacional
def signal_index(lista):
    """
    Devuelve el índice de las señales de compra

    Parámetros
    ----------
    
    lista: Lista con señales de compra/venta

    Returns
    -------
    indice_señal: Lísta con los índices de las señales de compra/venta

    """
    indice_señal = []
    for i in range(1,len(lista)):
        if lista[i-1] == 1:
            for j in range(i,len(lista)):
                if lista[j] == 2:
                    indice_señal.append([i,j+2])
                    break
                continue
    return indice_señal

@metrica_computacional
def operations(lista, precios):
    """
    Devuelve fechas y precios que hay entre una señal de compra y una de venta

    Parámetros
    ----------
    
    lista: Índices del DataFrame con las señales de compra/venta
    precios: Los precios que vas a usar en tus operaciones (close, open, high, low), dependiendo de la estrategia

    Returns
    -------
    operaciones: Lista con DataFrame individual de cada una de las operaciones realizadas

    """
    operaciones = []
    for i in range(len(lista)):
        operaciones.append(pd.DataFrame(precios[lista[i][0]:lista[i][1]]))
    return operaciones

@metrica_computacional
def open_price_profit(lista):
    """
    Devuelve el rendimiento que cada vela tiene con el precio de apertura de la operación

    Parámetros
    ----------
    
    lista: Lista de las operaciones realizadas

    Returns
    -------
    retorno_operacion: Lista anidada, que contiene rendimiento respecto al precio de apertura
        de cada precio guardado, de cada una de las operaciones del periodo.

    """
    retorno_operacion = []
    for i in range(len(lista)):
        retorno_vela = []
        for j in range(len(lista[i])):
            retorno_vela.append((lista[i].iloc[j][0]/ lista[i].iloc[0][0]-1))
        retorno_operacion.append(retorno_vela)
    return retorno_operacion

@metrica_computacional
def profit(lista, comision, take_profit, stop_loss):
    """
    Devuelve el rendimiento obtenido por operación, ya sea alcanzado el take profit, stop loss o bien recibiendo 
    una señal de venta

    Parámetros
    ----------
    
    lista: Lista anidada, que contiene rendimiento respecto al precio de apertura
        de cada precio guardado, de cada una de las operaciones del periodo.
    comision: Comisión que cobra el broker por operación
    take_profit: Nivel de rendimiento con el cual finalizamos la operación
    stop_loss: Nivel de pérdida máximo con el cuál decidimos abandonar la operación

    Returns
    -------
    rendimiento: Lista con los rendimientos obtenidos en las operaciones del periodo

    """
    rendimiento = [] 
    for i in range(len(lista)):
        for j in range(len(lista[i])):
            if j < len(lista[i])-1:
                if lista[i][j] >= take_profit or lista[i][j] <= stop_loss:
                    rendimiento.append(lista[i][j] - comision)
                    break
            else:
                rendimiento.append(lista[i][-1] - comision)
    return rendimiento

@metrica_computacional
def capital_flow(lista, capital):
    """
    Devuelve el flujo del capital durante el periodo de trading

    Parámetros
    ----------
    
    lista: Lista de rendimientos del periodo
    capital: Capital con el que se trabajará durante el periodo

    Returns
    -------
    flujo_capital: Lista con el movimiento del capital durante el periodo 

    """
    flujo_capital = []
    flujo_capital.append(capital)
    for i in range(len(lista)):
        flujo_capital.append(flujo_capital[i] * (1+lista[i]))
    return flujo_capital

## MEDIDAS ATRIBUCIÓN AL DESEMPEÑO
@metrica_computacional
def f_pip_size(name:str):
    """
    Devuelve los pips del símbolo con el que estás trabajando

    Parámetros
    ----------
    
    name: Símbolo con el que estás trabajando 

    Returns
    -------
    pip_size: pips

    """
    diccionario = pd.read_csv("instruments_pips.csv", index_col="Instrument")["TickSize"].to_dict()
    name = name.replace("/","_").upper()
    if name in diccionario:
        pip_size = diccionario[name]
    else:
        pip_size = 1/100
    return pip_size

@metrica_computacional
def columnas_tiempos(rend_individual, operaciones, take_profit, stop_loss):
    """
    Devuelve el tiempo que duró cada operación hasta el cierre de cualquier tipo 
                                            (take profit, stop loss, señal de venta)

    Parámetros
    ----------
    
    rend_individual: Lista anidada, que contiene rendimiento respecto al precio de apertura
        de cada precio guardado, de cada una de las operaciones del periodo.
    operaciones: Lista con las operaciones del periodo
    take_profit: Nivel de rendimiento con el cual finalizamos la operación
    stop_loss: Nivel de pérdida máximo con el cuál decidimos abandonar la operación

    Returns
    -------
    dataframe: DatafRame con el número de operación y el tiempo que duró la misma

    """
    tiempo_operacion = []
    for i in range(len(rend_individual)):
        for j in range(len(rend_individual[i])):
            if j < len(rend_individual[i])-1:
                if rend_individual[i][j] >= take_profit or rend_individual[i][j] <= stop_loss:
                    tiempo_operacion.append(operaciones[i].index[j] - operaciones[i].index[0])
                    break
            else:
                tiempo_operacion.append(operaciones[i].index[-1] - operaciones[i].index[0])
    dataframe = pd.DataFrame(tiempo_operacion)
    dataframe.columns = ["Tiempo"]
    dataframe.index.name = "# Operación"
    return dataframe

@metrica_computacional
def f_columnas_pips(pips:int, rendimiento):
    """
    Devuelve varciación en pips del rendimiento obtenido durante el periodo

    Parámetros
    ----------
    
    pips: pips
    rendimineto: Lista con los rendimientos del periodo

    Returns
    -------
    Dataframe: DatafRame con:
            Profit: Rendimiento de la operación
            Pips: Variación en pips respecto al rendimiento anterior
            Profit_acum: Suma acumulada del profit
            Pip_acum: Suma acumulada de pips

    """
    rendimiento_porcentual = rendimiento
    rendimiento_pips = []
    rendimiento_pips.append(rendimiento[0]*pips)
    for i in range(1,len(rendimiento)):
        rendimiento_pips.append((rendimiento[i] - rendimiento[i-1]) * pips)
    profit_acum = np.cumsum(rendimiento_porcentual)
    pips_acum = np.cumsum(rendimiento_pips)
    dataframe = pd.DataFrame([rendimiento_porcentual, rendimiento_pips, profit_acum, pips_acum]).T
    dataframe.columns = ["Profit", "Pips", "Profit_acum", "Pip_acum"]

    return dataframe

@metrica_computacional
def f_estadísticas_ba(rendimiento, operaciones, name:str ="df_1_tabla" or  "df_2_ranking"):
    """
    Devuelve un diccionario con 2 DataFrames de estadísticas del trading durante el periodo

    Parámetros
    ----------
    
    rendimineto: Lista con los rendimientos del periodo
    operaciones: Lista con las operaciones del periodo
    name: Tabla que deseas consultar {"df_1_tabla" ,"df_2_ranking"}

    Returns
    -------
    dataframe: DataFrame de estadísticas

    """
    ganadora = 0
    perdedora = 0
    for i in range(len(rendimiento)):
        if rendimiento[i] > 0:
            ganadora += 1
        else:
            perdedora +=1
    column_1 = ["Op_totales", "Ganadoras", "Perdedoras", "Mediana (Profit)", "Mediana (Pips)",\
                "R. efectividad", "R. proporción"]
    column_2 = [int(len(rendimiento)), int(ganadora), int(perdedora), np.median(rendimiento),\
                np.median(f_columnas_pips(pips = f_pip_size("btc/USD"), rendimiento=rendimiento)["Pips"]),\
                ganadora / len(rendimiento), ganadora / perdedora] 
    column_3 = ["Operaciones totales","Operaciones ganadoras","Operaciones perdedoras",\
                "Mediana de profit de operaciones", "Mediana de pips de operaciones",\
                "Ganadoras Totales/Operaciones Totales",\
                "Ganadoras Totales/Perdedoras Totales"]
    df_1_tabla = pd.DataFrame([column_1, column_2, column_3]).T
    df_1_tabla.columns= ["Medida", "Valor", "Descripción"]

    dias = []
    for i in range(len(operaciones)):
        dias.append(calendar.day_name[operaciones[i].index[0].weekday()])

    dias_positivos = []
    dias_negativos = []
    for i in range(len(dias)):
        if rendimiento[i] > 0:
            dias_positivos.append([dias[i],rendimiento[i]])
        else:
            dias_negativos.append([dias[i],rendimiento[i]])
    dias_positivos = pd.DataFrame(dias_positivos)[0].value_counts()
    dias_negativos = pd.DataFrame(dias_negativos)[0].value_counts()

    dias_union = pd.concat([dias_positivos,dias_negativos], axis=1).fillna(0)
    dias_union.columns = ["Positivos","Negativos"]

    df_2_ranking = pd.DataFrame(round(dias_union["Positivos"] / (dias_union["Positivos"] + dias_union["Negativos"])\
                             * 100, 2))
    df_2_ranking.columns = ["Rank %"]
    df_2_ranking.index.name = "Día"
    df_2_ranking.sort_values(by="Rank %")

    diccionario = {
        "df_1_tabla": df_1_tabla,
        "df_2_ranking": df_1_tabla
    }

    return diccionario[name]

@metrica_computacional
def f_evolucion_capital(df, operaciones, rend_operacion, take_profit, stop_loss, capital, rendimiento):
    """
    Devuelve el día y profit que se tuvo en el mismo, así como el acumulado del capital

    Parámetros
    ----------
    
    df: Precios con los que se van a calcular
    operaciones: Lista con las operaciones del periodo
    rend_operacion = rendimiento individual respecto al precio de apertura
    take_profit: Nivel de rendimiento con el cual finalizamos la operación
    stop_loss: Nivel de pérdida máximo con el cuál decidimos abandonar la operación
    capital: Capital con el que se trabajará durante el periodo
    rendimiento: rendimiento por operación

    Returns
    -------
    dataframe: DataFrame con 
                timestamp: Día de la operación
                profit_d: el profit del día, si tuvo
                profit_d_acum: profit acumulado respecto al capital

    """    
    inicio = datetime.strptime(str(df.index[0])[0:10], "%Y-%m-%d" )
    fin    = datetime.strptime(str(df.index[-1])[0:10], "%Y-%m-%d" )

    lista_fechas = [inicio + timedelta(days=d) for d in range((fin - inicio).days + 1)]

    fechas_cierre_rendimiento = []
    for i in range(len(rend_operacion)):
        for j in range(len(rend_operacion[i])):
            if j < len(rend_operacion[i])-1:
                if rend_operacion[i][j] >= take_profit or rend_operacion[i][j] <= stop_loss:
                    fechas_cierre_rendimiento.append(\
                        [datetime.strptime(str(operaciones[i].index[j])[0:10], "%Y-%m-%d" ),\
                            rendimiento[i]])
                        
                    break
            else:
                fechas_cierre_rendimiento.append(\
                    [datetime.strptime(str(operaciones[i].index[-1])[0:10], "%Y-%m-%d" ),\
                        rendimiento[i]])
    
    rendimientos_periodo = np.zeros(len(lista_fechas))
    for i in range(len(lista_fechas)):
        for j in range(len(fechas_cierre_rendimiento)):
            if fechas_cierre_rendimiento[j][0] == lista_fechas[i]:
                rendimientos_periodo[i] += fechas_cierre_rendimiento[j][1]

    rend_acum = capital_flow(rendimientos_periodo, capital)
    data = pd.DataFrame([lista_fechas, rendimientos_periodo, rend_acum]).fillna(0).T
    data.columns = ["timestamp", "Profit_d", "Profit_acum_d"]
    return data

@metrica_computacional
def f_estadisticas_mad(evolucion_capital):
    """
    Devuelve DataFrame con estadísticas generales

    Parámetros
    ----------
    
    evolucion_capital: DataFrame con el día, profit del día y profit acumulado.

    Returns
    -------
    dataframe: DataFrame con:
                Sharpe Ratio Original: Medida de rendimiento respecto a la rentabilidad sin riesgo
                Sharpe Ratio Actualizado: Medida de rendimiento respecto a el mercado
                DrawDown: Minusvalía máxima del periodo
                DrawUp: Plusvalía máxima del periodo
    """
    rend_log = np.log(1 + evolucion_capital.iloc[:,2].pct_change()).fillna(0)
    minimo = min(rend_log)
    maximo = max(rend_log)
    rp = np.mean(rend_log)
    rf = .05
    sdp = np.std(rend_log)
    column_1 = ["Sharpe Ratio Original", "Sharpe Ratio Actualizado", "DrawDown", "DrawUp"]
    column_2 = [(rp - rf) / sdp, 0, minimo, maximo]
    
    return pd.DataFrame([column_1, column_2]).T

@metrica_computacional
def metrica_optimizacion(short_length_range, long_length_range, take_profit_arange, stop_loss_arange):
    """
    Devuelve el número de iteraciones a realizar en la optimización

    Parámetros
    ---------

    short_length_range: rango de iteracion del promedio móvil corto
    long_length_range: rango de iteracion del promedio móvil largo
    take_profit_arange: rango de iteracion del take profit
    stop_loss_arange: rango de iteracion del stop loss

    Returns
    -------
    suma : # de iteraciones
    
    """
    suma = 0
    for i in short_length_range:
        for j in long_length_range:
            for x in take_profit_arange:
                for y in stop_loss_arange:
                    if j>i:
                        suma +=1
    return suma  
