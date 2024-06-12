# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 11:47:52 2023

@author: lucio
"""

import numpy as np
from itertools import groupby    

def distance(x, y, x0, y0):
    """
    Return distance between point
    P[x0,y0] and a curve (x,y)
    """
    d_x = x - x0
    d_y = y - y0
    dis = np.sqrt( d_x**2 + d_y**2 )
    return dis

def min_distance(x, y, P, precision=5):
    """
    Compute minimum/a distance/s between
    a point P[x0,y0] and a curve (x,y)
    rounded at `precision`.
    
    ARGS:
        x, y      (array)
        P         (tuple)
        precision (int)
        
    Returns min indexes and distances array.
    """
    # compute distance
    d = distance(x, y, P[0], P[1])
    d = np.round(d, precision)
    # find the minima
    glob_min_idxs = np.argwhere(d==np.min(d)).ravel()
    return glob_min_idxs, d

#uso el indice de jaccard para comparar enlaces
def jaccard(list1, list2):
    A=set(list1)
    B=set(list2)
    intersection = len(list(A.intersection(B)))
    union = (len(A) + len(B)) - intersection
    
    if (len(A) == 0) and (len(B) == 0):
        res=1
    else:
        res=float(intersection) / union
    return res

#detecta eventos criterio de cristina
def event_transform_cristina(signal, qi,qf):
    #qi > qf
    ns=np.asarray(signal).copy()

    #me quedo con los que pasaron qf
    bools0=(qf<=ns)
    sublists=[[k,list(g)] for k, g in groupby(bools0)]

    #de esa sublista tengo que ver además cuales tienen valores menores que qf
    reconstructed_signal=[]
    for k,s in sublists:
        reconstructed_signal.extend(s)
    new_signal=[signal[i] if b else 0 for i,b in enumerate(reconstructed_signal)]

    #veo mis conjuntos de posibles eventos
    sublists=[[k,list(g)] for k, g in groupby(new_signal,lambda x: x>0)]

    events_list=[]
    for k,s in sublists:
        if k:
            #me quedo con el primer elemento que supere el umbral
            new_s=[False for i in range(len(s))]
            var=next((x[0] for x in enumerate(s) if x[1] >= qi ), False)
            if type(var) == int:
                new_s[var]=True
            events_list.extend(new_s)
        else:
            events_list.extend(s)

    events_list=list(map(int, events_list)) 
    return events_list


# def func_c(c1,c2,lag=3):
#     times_c1=np.nonzero(c1)[0]
#     times_c2=np.nonzero(c2)[0]
    
#     coincidence=0
#     fails=0
#     indices_c=[]
#     indices_f=[]
#     for t2 in times_c2:
#         for t1 in times_c1:
#             if 0<(t2-t1)<=lag:
#                 indices_c.append(t2)
#                 coincidence+=1
                
#             elif (t2-t1)==0:
#                 coincidence+=0.5
#                 indices_c.append(t2)

#             else:
#                 indices_f.append(t2)
#                 fails+=1
#     return indices_f,fails,indices_c,coincidence

def func_c(c1,c2,lag=1):
    times_c1=np.nonzero(c1)[0]
    times_c2=np.nonzero(c2)[0]
    
    coincidence=0
    #fails=0
    indices_c=[]
    #indices_f=[]
    #print(times_c2)
    for t2 in times_c2:
        elementos_previos=[]
        for t1 in times_c1:
            if (t2-t1)==0:
                #print('(t2-t1)==0',t2,t1)
                indices_c.append(t2)
                elementos_previos.append(0.5)
                
            elif 0<(t2-t1)<=lag:
                #print('0<(t2-t1)<=lag',t2,t1)
                indices_c.append(t2)
                elementos_previos.append(1)
                
        if len(elementos_previos) > 0:
            coincidence+=min(elementos_previos)
        #print(coincidence)       
    return indices_c,coincidence


def eventos_criterios(trend,umbral, criterio_bajada,criterio_subida):
    #criterio_bajada=15#quiero que si hay un descenso del 20% establezca ahi un corte
    #criterio_subida=10#10    
    trend_sig=trend.copy()
    trend_sig[trend_sig>umbral]=1
    trend_sig[trend_sig<=umbral]=0

    sel_lis=list(zip(range(len(trend)),trend,trend_sig))
    #si baja mucho como un 30% le cambio un 1 por un 0 a ese y a todos los que le siguen
    sublists_sig=[[k,list(g)] for k, g in groupby(sel_lis, key = lambda x: x[2]) if k == 1]

    primeros_eventos=[]
    for sub in sublists_sig:
        elementos=list(zip(*sub[1]))
        indices=list(elementos[0])
        valores=list(elementos[1])
        etiquetas=list(elementos[2])
        #lo hago por diferencias
        diferencia=np.diff(valores)
        porcentaje=diferencia*100/valores[1:]
        nuevas_et=np.ones(len(etiquetas))
        estado=1
        for i,p in enumerate(porcentaje):
            if p <= -criterio_bajada:
                estado=0
            elif p > criterio_subida:
                estado=1
            nuevas_et[i+1]=estado

        mergeo=list(zip(indices,valores,nuevas_et))
        subsublists=[[k,list(g)] for k, g in groupby(mergeo, key = lambda x: x[2]) if k == 1]
        for subsub in subsublists:
            #me quedo con el primer elemento en la lista de indices
            first=list(zip(*subsub[1]))[0][0]
            primeros_eventos.append(first)
            
    return primeros_eventos

def moving_average(x, w,**kwargs):
    return np.convolve(x, np.ones(w), **kwargs) / w
