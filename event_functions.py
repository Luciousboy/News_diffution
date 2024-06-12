# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 11:47:52 2023

@author: lucio
"""

import numpy as np
from itertools import groupby    

def event_transformer(signal, qi,qf):
    #transform a signal to the event serie
    #qi: activation threshold
    #qf: deactivation threshold
    #signal: time serie
    
    ns=np.asarray(signal).copy()

    #construct boolean sublists of values that exceed the deactivation threshold.
    bools0=(qf<=ns)
    sublists=[[k,list(g)] for k, g in groupby(bools0)]

    #reconstruct the time serie with the original values from the selected sections
    reconstructed_signal=[]
    for k,s in sublists:
        reconstructed_signal.extend(s)
    new_signal=[signal[i] if b else 0 for i,b in enumerate(reconstructed_signal)]
    sublists=[[k,list(g)] for k, g in groupby(new_signal,lambda x: x>0)]

   #select the first event that exceedes the activation threshold  
    events_list=[]
    for k,s in sublists:
        if k:
            new_s=[False for i in range(len(s))]
            var=next((x[0] for x in enumerate(s) if x[1] >= qi ), False)
            if type(var) == int:
                new_s[var]=True
            events_list.extend(new_s)
        else:
            events_list.extend(s)

    #return the event time serie
    events_list=list(map(int, events_list)) 
    return events_list


def f_coin(c1,c2,lag=3):
    #calculate the coincidences of two event series
    #c1,c2 are the event time series
    #the lag is set equal to 3

    #search for the corresponding times of the events
    times_c1=np.nonzero(c1)[0]
    times_c2=np.nonzero(c2)[0]

    #count the coincidences
    coincidence=0
    indices_c=[]
    for t2 in times_c2:
        elementos_previos=[]
        for t1 in times_c1:
            #if the times match at the exact moment the value is taken as 0.5
            if (t2-t1)==0:
                indices_c.append(t2)
                elementos_previos.append(0.5) 
            elif 0<(t2-t1)<=lag:
                indices_c.append(t2)
                elementos_previos.append(1)
        #if two or more events coinceed in the same time window we take the minimum coincidence value
        if len(elementos_previos) > 0:
            coincidence+=min(elementos_previos)
    return indices_c,coincidence