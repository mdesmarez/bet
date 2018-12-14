#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 17:40:23 2018

@author: mathieu
"""

# =============================================================================
# IMPORT PACKAGES
# =============================================================================
import os
import urllib2
import dateparser
import time
import datetime
import re
import ast

import matplotlib.pyplot  as plt
import pandas             as pd
import numpy              as np

from bs4                  import BeautifulSoup
from glob                                                                      import glob
from datetime                                                                  import datetime
from datetime                                                                  import timedelta


# =============================================================================
# 
# =============================================================================
def match_filter_prediction(df, bet_max, bet_min, bet_ecart):
    #####
    df = df[(df.bet_1 < bet_max) | (df.bet_2 < bet_max)]
    
    #####
    df = df[(df.bet_1 > bet_min) & (df.bet_2 > bet_min)]
    
    ####
    df = df[abs(df.bet_1 - df.bet_2) > bet_ecart]

    return df


def result_merge(df, bet_min, bet_max, bet_ecart):
    good_perc   = 0
    num_good    = 0
    num_total   = len(df)
    df_filter   = df[(df.min_bet >= bet_min) & (df.min_bet <= bet_max) & (df.bet_diff >= bet_ecart)]
    if len(df_filter) != 0:
        good_perc = round(df_filter.good_pred.sum()/float(len(df_filter))*100,2)
        num_good  = len(df_filter)
        num_total = len(df)
    else:
        pass
    return df_filter, good_perc, num_good, num_total


# =============================================================================
# 
# =============================================================================
def encode_decode(k):
    try:
        k = k.decode('utf-8')
        k = k.encode('utf-8')
    except:
        k = k.encode('utf-8')
    k = k.replace('\xe2\x80\x8e','')
    return k


# =============================================================================
# 
# =============================================================================
def optimisation_apply(df, dict_parameter_sport):
    list_sport = df.sport.unique().tolist()
    df_parlay_filter = pd.DataFrame()
    for item in list_sport:
        try:
            bet_min     = dict_parameter_sport[item]['bet_min']
            bet_max     = dict_parameter_sport[item]['bet_max']
            bet_ecart   = dict_parameter_sport[item]['bet_ecart']
            num_total   = dict_parameter_sport[item]['num_total']
            if num_total < 50:
                print 'too less data for ',item
            else:
                df_sport    = df[df.sport == item]
                df_sport    = match_filter_prediction(df_sport, bet_max, bet_min, bet_ecart)
                df_sport.match_date = df_sport.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
                df_parlay_filter = pd.concat((df_parlay_filter, df_sport))
        except:
            print 'no',item
    return df_parlay_filter
    


def optimisation(df):
    bet_min             = 1
    bet_max             = 1
    bet_ecart           = 1
    bet_max_before      = 1
    bet_ecart_before    = 1
    
    for i in range(4000):
        bet_max = bet_max + 0.005
        df_filter, good_perc, num_good, num_total = result_merge(df, bet_min, bet_max, bet_ecart)
        if good_perc != 100 and num_good != 0:
            bet_max = bet_max_before
            break
        bet_max_before = bet_max
    
    df_filter, good_perc, num_good, num_total = result_merge(df, bet_min, bet_max, bet_ecart)
    num_good_before = num_good
    
    for i in range(1000):
        bet_ecart = bet_ecart + 0.1
        df_filter, good_perc, num_good, num_total = result_merge(df, bet_min, bet_max, bet_ecart)
        if good_perc != 100 or num_good != num_good_before:
            bet_ecart = bet_ecart_before
            break
        bet_ecart_before = bet_ecart

    print bet_max, bet_ecart, good_perc, num_good, num_total
    
    if num_good != 0:
        dict_optimisation = {df.sport.unique()[0]:{
                                                'bet_min'             : round(bet_min,2),
                                                'bet_max'             : round(bet_max,2),
                                                'bet_ecart'           : round(bet_ecart,2),
                                                'num_total'           : num_total
                                                }}
    else:
        dict_optimisation = {'null':{
                                                'bet_min'             : 0,
                                                'bet_max'             : 0,
                                                'bet_ecart'           : 0,
                                                }}
    return dict_optimisation





def optimisation_2(df):
    bet_min             = 1
    bet_max             = 1.02
    bet_ecart           = 1
    bet_max_init        = bet_max
    
#    bankroll = []    
#    bankroll_amount = 0
#    df.sort_values('min_bet', inplace=True)
#    for i in range(len(df)):
#        bankroll_amount = bankroll_amount - 1 + df.min_bet.iloc[i]*df.good_pred.iloc[i]
#        bankroll.append(bankroll_amount)
#    

    df_filter, good_perc_init, num_good, num_total = result_merge(df, bet_min, bet_max, bet_ecart)
    
    for i in range(400):
        bet_max = bet_max + 0.005
        df_filter, good_perc, num_good, num_total = result_merge(df, bet_min, bet_max, bet_ecart)
        if good_perc < good_perc_init:
            break
#            print good_perc_init, good_perc, bet_max

        else:
            good_perc_init = good_perc
            bet_max_init   = bet_max
    print good_perc_init, '% ==> ', bet_max_init
    
    df_filter, good_perc, num_good, num_total = result_merge(df, bet_min, bet_max, bet_ecart)
#    num_good_before = num_good
    
    
#    
#    bet_min             = 1
#    bet_max             = 1
#    bet_ecart           = 1
#    bet_max_before      = 1
#    bet_ecart_before    = 1
#    
#    mean_min    = df.min_bet[df.good_pred == 0].mean()
#    std_min     = df.min_bet[df.good_pred == 0].std()
#    
#    mean_bet_ecart    = df.bet_diff[df.good_pred == 0].mean()
#    std_bet_ecart     = df.bet_diff[df.good_pred == 0].std()
#    
#    bet_min     = mean - std*1
#    bet_max     = 100
#    bet_ecart   = mean_bet_ecart + std_bet_ecart*2
#    
#    df_filter, good_perc, num_good, num_total = result_merge(df, bet_min, bet_max, bet_ecart)
#
#    print bet_max, bet_ecart, good_perc, num_good, num_total
#    
    if num_good != 0:
        dict_optimisation = {df.sport.unique()[0]:{
                                                'bet_min'             : round(bet_min,2),
                                                'bet_max'             : round(bet_max,2),
                                                'bet_ecart'           : round(bet_ecart,2),
                                                'num_total'           : num_total
                                                }}
    else:
        dict_optimisation = {'null':{
                                                'bet_min'             : 0,
                                                'bet_max'             : 0,
                                                'bet_ecart'           : 0,
                                                }}
    return dict_optimisation


def optimisation_3(df):
    bet_min             = 1
    bet_max             = 1.0
    bet_ecart           = 1
    
    dict_bankroll = {}
    bankroll = []    
    bankroll_amount = 0
    df.sort_values('min_bet', inplace=True)
    for i in range(len(df)):
        bankroll_amount = bankroll_amount - 1 + df.min_bet.iloc[i]*df.good_pred.iloc[i]
        bankroll.append(bankroll_amount)
        dict_bankroll.update({i:bankroll_amount})
        print df.min_bet.iloc[i], bankroll_amount
        
    index_max = max(xrange(len(bankroll)), key=bankroll.__getitem__)
    bet_max = df.min_bet.iloc[index_max]
    print df.sport.unique()[0], ' / ', bet_max, ' / ', bankroll[index_max]

    df_filter, good_perc, num_good, num_total = result_merge(df, bet_min, bet_max, bet_ecart)

    if num_good != 0:
        dict_optimisation = {df.sport.unique()[0]:{
                                                'bet_min'             : round(bet_min,2),
                                                'bet_max'             : round(bet_max,2),
                                                'bet_ecart'           : round(bet_ecart,2),
                                                'num_total'           : num_total,
                                                'max_bankroll'        : max(bankroll)
                                                }}
    else:
        dict_optimisation = {'null':{
                                                'bet_min'             : 0,
                                                'bet_max'             : 0,
                                                'bet_ecart'           : 0,
                                                }}
    return dict_optimisation


# =============================================================================
# 
# =============================================================================
def optimisation_5(df_train, mod_value):
    dict_temp   ={}
    list_sport  = df_train.sport.unique().tolist()
    
    for sport in list_sport:
        df_train_sport = df_train[df_train.sport == sport]
#        if sport == 'soccer': ee

        if len(df_train_sport) > 600:
            df_train_sport.sort_values('min_bet', inplace=True)
            df_train_sport['mod'] = df_train_sport.min_bet/mod_value
            df_train_sport['mod'] = df_train_sport['mod'].apply(lambda x: int(x))
            
            list_mod = list(set(df_train_sport['mod'].tolist()))
            list_mod.sort()
            
            mod_performance = []
            list_mod_ok = [] 
            count = 0
            for mod in list_mod:
                df_train_mod = df_train_sport[df_train_sport['mod'] == int(mod)]
                sum_good = df_train_mod.good_pred.sum()
                sum_bad = df_train_mod.bad_pred.sum()
                perc_mod = sum_good/float(sum_bad+sum_good)*100
                mod_performance.append(perc_mod)
        
                if len(df_train_mod)>5 and perc_mod*((mod-1)*mod_value)-100>0:
                    list_mod_ok.append([(mod-1)*mod_value, mod*mod_value, len(df_train_mod), mod, perc_mod, perc_mod*((mod-1)*mod_value)-100])
                    count = count + len(df_train_mod)
                    dict_temp.update({sport:list_mod_ok})
                    
    return dict_temp
    

####################################


def optimisation_5_apply(df_test, dict_parameter_sport, mod_value):
    list_sport  = df_test.sport.unique().tolist()
    df_result_mod  = pd.DataFrame()
    
    for sport in list_sport:
        df_test_sport = df_test[df_test.sport == sport]
        df_test_sport.sort_values('min_bet', inplace=True)
        df_test_sport['mod'] = df_test_sport.min_bet/mod_value
        df_test_sport['mod'] = df_test_sport['mod'].apply(lambda x: int(x))
    
        list_mod = list(set(df_test_sport['mod'].tolist()))
        list_mod.sort()
        if sport in dict_parameter_sport.keys():
            list_mod_ok    = dict_parameter_sport[sport]
            list_mode_test = [item[3] for item in list_mod_ok]
           
            for mod in list_mod:
                if mod in list_mode_test:
                    df_mod = df_test_sport[df_test_sport['mod'] == int(mod)]
                    df_result_mod = pd.concat((df_result_mod, df_mod))
        
    return df_result_mod

    
# =============================================================================
# 
# =============================================================================
def optimisation_4_apply(df, list_mod_ok, mod_value):
    bet_min             = 1
    bet_max             = 1
    bet_ecart           = 1
    
    
    bankroll = []    
    bankroll_amount = 0
    df.sort_values('min_bet', inplace=True)
    df['mod'] = df.min_bet/mod_value
    df['mod'] = df['mod'].apply(lambda x: int(x))
    
    list_mod = list(set(df['mod'].tolist()))
    list_mod.sort()
    
    mod_performance = []
    dict_result = {}
    count = 0
    df_result_mod = pd.DataFrame()
    list_mode_test = [item[3] for item in list_mod_ok]
    for mod in list_mod:
        if mod in list_mode_test:
            df_mod = df[df['mod'] == int(mod)]
            df_result_mod = pd.concat((df_result_mod, df_mod))
    
    return df_result_mod
    

def optimisation_4(df, mod_value):
    bet_min             = 1
    bet_max             = 1
    bet_ecart           = 1
        
    bankroll = []    
    bankroll_amount = 0
    df.sort_values('min_bet', inplace=True)
    df['mod'] = df.min_bet/mod_value
    df['mod'] = df['mod'].apply(lambda x: int(x))
    
    list_mod = list(set(df['mod'].tolist()))
    list_mod.sort()
    
    mod_performance = []
    dict_result = {}
    list_mod_ok = [] 
    count = 0
    for mod in list_mod:
        df_mod = df[df['mod'] == int(mod)]
        sum_good = df_mod.good_pred.sum()
        sum_bad = df_mod.bad_pred.sum()
        perc_mod = sum_good/float(sum_bad+sum_good)*100
        mod_performance.append(perc_mod)

        if len(df_mod)>5 and perc_mod*(mod*mod_value)-100>0:
            dict_result.update({(mod)*mod_value:perc_mod*(mod*mod_value)-100})
            list_mod_ok.append([(mod-1)*mod_value, mod*mod_value, len(df_mod), mod])
            count = count + len(df_mod)
#        print (mod)*mod_value, round(sum(mod_performance)/len(mod_performance),2), str(len(df_mod)).zfill(2),  round(perc_mod,2), mod, perc_mod*(mod*mod_value-mod_value/2)-100
    
    df_dict_result = pd.DataFrame.from_dict(dict_result, orient='index')
    df_dict_result.sort_index(inplace=True)
#    df_dict_result.plot()

    return list_mod_ok



