# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:55:36 2020

@author: crudick
"""
workdir = 'C:/Users/crudick/Documents/D&D/Dice - Python/'

import pandas as pd
import itertools
import random
import numpy as np
import time

    


def roll_dice(d, n, max_for_stat=int(1e5)):
    np = d**n
    if np <= max_for_stat:
        vs = roll_dice_stat(d, n)
        method = 'STAT'
    else:
        vs = roll_dice_ran(d,n, max_for_stat)
        method = 'RAN'

    #Calculate and return distrubution of values
    vc = vs.value_counts()
    tvc = sum(vc)
    rs = []
#    for idx in vc.index:
    possible_values = range(n,n*d+1)
    for idx in possible_values:
        v = vc[idx] if idx in vc else 0
        rs.append((d, n, idx, v/tvc, method))
    return(rs)


def roll_dice_stat(d, n):
    possibles = mk_possibles(d, n)
    vs = pd.Series(sum(p) for p in possibles)
    return(vs)


def roll_dice_ran(d, n, max_for_stat):
    a = []
    for  i in range(max_for_stat):
        aa = 0
        for j in range(n):
            aa += random.randint(1,d)
        a.append(aa)
    vs = pd.Series(a)
    return(vs)
  
    
def roll_dice_ran2(d, n, max_for_stat):
    #I thought this would be faster, but its slower!
    rs = []
    for j in range(n):
        r = np.random.randint(1,d+1,max_for_stat)
        rs.append(r)
    rdf = pd.DataFrame(rs).transpose()
    vs = rdf.sum(axis=1)
    return(vs)
        

def roll_advantage_stat(adv='A'):
    if adv.upper() in ('A', 'ADV', 'ADVANTAGE'):
        adv2 = 'A'
        possibles = mk_possibles(20,2)
        vs = pd.Series(max(p) for p in possibles)
    elif adv.upper() in ('D', 'DIS', 'DISADVANTAGE'):
        adv2 = 'D'
        possibles = mk_possibles(20,2)
        vs = pd.Series(min(p) for p in possibles)
    elif adv.upper() in ('N', 'NON', 'NONE'):
        adv2 = 'N'
        vs = pd.Series(range(1,21))
    
    #Calculate and return distrubution of values
    vc = vs.value_counts()
    tvc = sum(vc)
    rs = []
    for idx in vc.index:
        rs.append((adv2, idx, vc[idx]/tvc))
    return(rs)

        
def mk_possibles(d, n):
    possibles = itertools.product(range(1,d+1),repeat=n)
    return(possibles)
    
def calc_distribution(vs):
    pass


if __name__ == '__main__':
    test = False
    start_time = time.time()
    
    maxn = 33
    ds = [4,6,8,10,12,20]
    max_for_stat= 10 if test else int(1e5)
    rs = []
    ltime = start_time
    minutes = 0
    for d in ds:
        for n in range(maxn+1):
            rs = rs + roll_dice(d=d, n=n, max_for_stat=max_for_stat)
            if time.time() - ltime > 58:
                minutes = minutes + 1
                ltime = time.time()
                print (d, n, minutes, time.time() - start_time)
    df = pd.DataFrame(rs, columns=('Dice', 'Number', 'Sum', 'Probability', 'Method'))
    

    adv = roll_advantage_stat('A')
    dis = roll_advantage_stat('D')
    non = roll_advantage_stat('N')
    rs2 = adv + dis + non
    df2 = pd.DataFrame(rs2, columns=('Advantage', 'Roll', 'Probability'))


    if not test:
        df.to_csv(workdir+'dice.csv', index=False)
        df2.to_csv(workdir+'d20.csv', index=False)
    print("--- %s seconds ---" % (time.time() - start_time))

    