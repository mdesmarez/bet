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
import math

import matplotlib.pyplot  as plt
import pandas             as pd

from sklearn.utils import shuffle
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

        if len(df_train_sport) > 500:
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
        
                if len(df_train_mod)>5 and perc_mod*((mod-1)*mod_value)-99.5>0:
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
def optimisation_6(df_train, mod_value):
    dict_temp   ={}
    list_sport  = df_train.sport.unique().tolist()
    
    df_train['good_pred_draw'] = 0
    df_train.good_pred_draw[df_train.winner == 0] = 1

    for sport in list_sport:
        df_train_sport = df_train[df_train.sport == sport]
#        if sport == 'soccer': ee

        limit_train = 800
        if len(df_train_sport) > limit_train:
            
            ### SHUFFLE
#            df_train_sport = shuffle(df_train_sport)
            
            ###ORDER
#            df_train_sport.sort_values('match_date',ascending=True,inplace=True)
            
#            df_train_sport        = df_train_sport[-limit_train:]
            
            df_train_sport.sort_values('min_bet', inplace=True)
            df_train_sport['mod'] = df_train_sport.min_bet/mod_value
            df_train_sport['mod'] = df_train_sport['mod'].apply(lambda x: int(x))
            
            list_mod = list(set(df_train_sport['mod'].tolist()))
            list_mod.sort()
            list_mod_ok             = [] 
            for mod in list_mod:
                df_train_mod = df_train_sport[df_train_sport['mod'] == int(mod)]
                result              = 0
                result_with_draw    = 0
                for item in range(len(df_train_mod)):
                    min_bet = df_train_mod.min_bet.iloc[item]
                    bet_X   = df_train_mod.bet_X.iloc[item]
                    
                    if df_train_mod.good_pred.iloc[item] == 1:
                        result = result + min_bet
                    result = result - 1
                    
                    if (df_train_mod.good_pred.iloc[item] == 1) or (df_train_mod.good_pred_draw.iloc[item] == 1):
                        if df_train_mod.good_pred.iloc[item] == 1:
                            result_with_draw = result_with_draw + min_bet
                        else:
                            result_with_draw = result_with_draw + bet_X
                    result_with_draw = result_with_draw - 2
            
#                print sport, (mod-1)*mod_value+mod_value, mod*mod_value+mod_value, len(df_train_mod), int(result), int(result_with_draw)
                
                limit_cap_min = 3
                if len(df_train_mod)>10 and (result > limit_cap_min or result_with_draw > limit_cap_min) and (result > 0 and result_with_draw > 0):
#                if len(df_train_mod)>10 and (result > limit_cap_min and result_with_draw > limit_cap_min):
                    
                    if result_with_draw > result:
                        list_mod_ok.append([round((mod-1)*mod_value+mod_value,2),round(mod*mod_value+mod_value,2), len(df_train_mod), mod, 'X', int(result_with_draw)])
                        print sport, (mod-1)*mod_value, mod*mod_value, int(result), int(result_with_draw), 'X'

                    else:
                        list_mod_ok.append([round((mod-1)*mod_value+mod_value,2), round(mod*mod_value+mod_value,2), len(df_train_mod), mod, 'S', int(result)])
                        print sport, (mod-1)*mod_value, mod*mod_value, int(result), int(result_with_draw), 'S'
            
                    dict_temp.update({sport:list_mod_ok})
   
                    
    return dict_temp


####################################

def optimisation_6_apply(df_test, dict_parameter_sport, mod_value):
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
            list_mode_test = [[item[0],item[1]] for item in list_mod_ok]
            list_mode_bet  = [item[4] for item in list_mod_ok]

            for i, mod in enumerate(list_mode_test):
                df_mod              = df_test_sport[(df_test_sport.min_bet > mod[0]) & (df_test_sport.min_bet <= mod[1])]
                mode_bet            = list_mode_bet[i]
                df_mod['mode_bet']  = mode_bet
                df_result_mod = pd.concat((df_result_mod, df_mod))

            for mod in list_mod:
                if mod in list_mode_test:
                    df_mod = df_test_sport[df_test_sport['mod'] == int(mod)]
                    df_result_mod = pd.concat((df_result_mod, df_mod))
        
    return df_result_mod


# =============================================================================
# 
# =============================================================================
def eval_result(df, mode, item, mise):
    min_bet = df.min_bet.iloc[item]+0.0000001
    bet_X   = df.bet_X.iloc[item]+0.0000001
    bet_DC  = 1/((1/min_bet)+(1/bet_X))
    bet_DNB = (1-(1/bet_X))*min_bet
    bet_WNB = (1-(1/min_bet))*bet_X
        
    result = 0
    if mode == 'S':
        result = result - mise
        if df.good_pred.iloc[item] == 1:
            result = result + df.min_bet.iloc[item]*mise
    
    
    if mode == 'DNB':
        result = result - mise

        if df.good_pred.iloc[item] == 1:
            result = result + bet_DNB*mise
            
        if df.winner.iloc[item] == 0:
            result = result + mise

    
    if mode == 'WNB':
        result = result - mise
        
        if df.good_pred.iloc[item] == 1:
            result = result + mise
            
        if df.winner.iloc[item] == 0:
            result = result + bet_WNB*mise
        
    
    
    if mode == 'DC':
        result = result - mise
        
        if df.good_pred.iloc[item] == 1 or df.winner.iloc[item] == 0:
            result = result + bet_DC*mise
        
        
    return result

# =============================================================================
# 
# =============================================================================
def optimisation_7(df_train, dict_training_option):
    list_test = []
    dict_temp   ={}
    list_sport  = df_train.sport.unique().tolist()
    date = str(df_train.match_date.max())[:10]

    df_train.fillna(1, inplace=True)

    df_train['good_pred_draw'] = 0
    df_train.good_pred_draw[df_train.winner == 0] = 1

    for sport in list_sport:
        a = pd.DataFrame()
        a_list = []

        ### only bet upper limit
        df_train = df_train[df_train.min_bet >= dict_training_option[sport]['limit_bet']]

        df_train_sport = df_train[df_train.sport == sport]

        df_train_sport.sort_values('min_bet', inplace=True)
        df_train_sport['mod'] = df_train_sport.min_bet/dict_training_option[sport]['mod_value']
        df_train_sport['mod'] = df_train_sport['mod'].apply(lambda x: int(x))
        list_mod = list(set(df_train_sport['mod'].tolist()))
        list_mod.sort()
        list_mod_ok             = [] 
        for mod in list_mod:
            df_train_mod = df_train_sport[df_train_sport['mod'] == int(mod)]
            
#            print mod
#            if mod == 21 : ee
            limit_train = 5
            if len(df_train_mod) > limit_train:
                result              = 0
                result_with_draw    = 0
                result_DNB          = 0
                result_WNB          = 0
                result_DC           = 0
                
#                df_train_mod = df_train_mod.iloc[-limit_train:]
                
                ###
                list_high_S   = []
                list_high_SX  = []
                nbr_total_bet = len(df_train_mod) 
                step_diff_bet = 0.1
                for i in range(100):
                    df = df_train_mod[df_train_mod.bet_diff > i*step_diff_bet]
            
#                    df_train_mod_analysis_freq = df.set_index('match_date')
#                    df_train_mod_analysis_freq.dropna(inplace=True)
#                    df_train_mod_analysis_freq          = df_train_mod_analysis_freq.resample('W').sum()
#                    df_train_mod_analysis_freq['perc'] = df_train_mod_analysis_freq['good_pred']/(df_train_mod_analysis_freq['good_pred']+df_train_mod_analysis_freq['bad_pred'])
#                    df_train_mod_analysis_freq['gain'] = df_train_mod_analysis_freq['good_pred']*((mod/10.0)-1)-df_train_mod_analysis_freq['bad_pred']
##                    df_train_mod_analysis_freq.gain.hist(bins=20)
#                    if df_train_mod_analysis_freq['gain'].mean() > 0 and len(df)>50:
#                        a[str(mod/10.0)+'_'+str(i*step_diff_bet)] = df_train_mod_analysis_freq.gain
#                        print i*step_diff_bet, mod, df_train_mod_analysis_freq['gain'].sum(), len(df), df_train_mod_analysis_freq['gain'].sum()/float(len(df)), a[str(mod/10.0)+'_'+str(i*step_diff_bet)].std(),  a[str(mod/10.0)+'_'+str(i*step_diff_bet)].mean(), a[str(mod/10.0)+'_'+str(i*step_diff_bet)].median()
#                        a_list.append([i*step_diff_bet, mod, df_train_mod_analysis_freq['gain'].sum(), len(df), df_train_mod_analysis_freq['gain'].sum()/float(len(df)), a[str(mod/10.0)+'_'+str(i*step_diff_bet)].std(),  a[str(mod/10.0)+'_'+str(i*step_diff_bet)].mean(), a[str(mod/10.0)+'_'+str(i*step_diff_bet)].median()])
#                       
#                        ee
#                        df_a_list = pd.DataFrame(a_list)
#                        df_a_list.columns = ['diff', 'mod', 'sum', 'len_df', 'sum/len_df', 'std', 'mean', 'median']
#                        df_a_list['ratio'] = df_a_list['sum']/df_a_list['len_df']
#                        df_a_list['name'] = df_a_list['mod'].map(str) + '_' + df_a_list['diff'].map(str)
#                        ax = df_a_list.plot(kind='scatter',x='mean',y='std')
#                        df_a_list[['mean','std','name']].apply(lambda x: ax.text(*x),axis=1)
#
#                
#                    result_S = 0
#                    for item in range(len(df)):
#                        result_S = result_S + eval_result(df, 'S', item, 1)
#                    result_DNB = 0
#                    for item in range(len(df)):
#                        result_DNB = result_DNB + eval_result(df, 'DNB', item, 1)
#                    result_WNB = 0
#                    for item in range(len(df)):
#                        result_WNB = result_WNB + eval_result(df, 'WNB', item, 1)
#                    result_DC = 0
#                    for item in range(len(df)):
#                        result_DC = result_DC + eval_result(df, 'DC', item, 1)                                        
                    
                    if len(df) > (nbr_total_bet*0.15):
                        list_high_S.append(round(len(df[df.good_pred == 1])/float(len(df)),2))
                        list_high_SX.append(round((len(df[df.good_pred == 1]) + len(df[(df.winner == 0) & (df.good_pred == 0)]))/float(len(df)),2)) 
                        print i*step_diff_bet, len(df), round(len(df[df.good_pred == 1])/float(len(df)),2), round(len(df[df.good_pred == 1])/float(len(df)),2)*(mod/10.0)

#                        if result_S >0 or result_DNB>0 or result_WNB>0 or result_DC>0:
#                            perc_restant_after_filter = round(len(df)/float(nbr_total_bet),2)
#                            perc_win_S                = round(len(df[df.good_pred == 1])/float(len(df)),3)
#                            perc_win_SX               = round((len(df[df.good_pred == 1]) + len(df[(df.winner == 0) & (df.good_pred == 0)]))/float(len(df)),3)
#                            min_bet_filter            = df_train_mod.min_bet.mean()
#                            
#                            elasticity_win_number     = round(perc_restant_after_filter*(min_bet_filter*perc_win_S-1)*100,2)
#                            print sport, result_S, result_DNB, result_WNB, result_DC, elasticity_win_number, \
#                                         ' / min_bet : ', min_bet_filter, \
#                                         ' / diff : ', str(i*step_diff_bet).zfill(4), \
#                                         ' / % restant : ', perc_restant_after_filter, \
#                                         ' / perc S : ', perc_win_S, \
#                                         ' / perc SX : ', perc_win_SX



                index_list_high_S  = max(xrange(len(list_high_S)), key=list_high_S.__getitem__)
                index_list_high_SX = max(xrange(len(list_high_SX)), key=list_high_SX.__getitem__)
                bet_diff_high_S    = index_list_high_S*step_diff_bet
                bet_diff_high_SX   = index_list_high_SX*step_diff_bet
                
                df_train_mod = df_train_mod[df_train_mod.bet_diff >= bet_diff_high_S]
#                df_train_mod = df_train_mod[df_train_mod.bet_diff >= bet_diff_high_SX]



                for item in range(len(df_train_mod)):
                    min_bet = df_train_mod.min_bet.iloc[item]
                    bet_X   = df_train_mod.bet_X.iloc[item]
                    
                    if bet_X != 0:
                        bet_DNB = (1-(1/bet_X))*min_bet
                        bet_DC  = 1/((1/min_bet)+(1/bet_X))
                    else:
                        bet_DNB = 0
                        bet_DC  = 0
                    bet_WNB = (1-(1/min_bet))*bet_X

                    ### S
                    if df_train_mod.good_pred.iloc[item] == 1:
                        result = result + min_bet
                    result = result - 1
                    
                    ### X
                    if (df_train_mod.good_pred.iloc[item] == 1) or (df_train_mod.good_pred_draw.iloc[item] == 1):
                        if df_train_mod.good_pred.iloc[item] == 1:
                            result_with_draw = result_with_draw + min_bet/2
                        else:
                            result_with_draw = result_with_draw + bet_X/2
                    result_with_draw = result_with_draw - 1
                    
                    ### DNB
                    if df_train_mod.good_pred.iloc[item] == 1:
#                        S1 = (1-(1/bet_X))*1
                        result_DNB = result_DNB + bet_DNB*1 -1
                    else:
                        if df_train_mod.good_pred_draw.iloc[item] == 1:
                            result_DNB = result_DNB
                        else:
                            result_DNB = result_DNB - 1
                    
                    ### WNB
                    if df_train_mod.good_pred_draw.iloc[item] == 1:
#                        SX = (1-(1/min_bet))*1
                        result_WNB = result_WNB + bet_WNB*1 -1
                    else:
                        if df_train_mod.good_pred.iloc[item] == 1:
                            result_WNB = result_WNB
                        else:
                            result_WNB = result_WNB - 1            

                    ### DC
                    if (df_train_mod.good_pred.iloc[item] == 1) or (df_train_mod.good_pred_draw.iloc[item] == 1):
                        result_DC = result_DC + bet_DC -1
                    else:
                        result_DC = result_DC - 1

                num_good_pred = df_train_mod['good_pred'].sum()#+df_train_mod['good_pred_draw'].sum()
                num_bad_pred  = len(df_train_mod)-num_good_pred
                
                perc_win = num_good_pred/float(num_good_pred+num_bad_pred)
            
                perc_win_good = df_train_mod['good_pred'].sum()/float(len(df_train_mod))
                perc_win_draw = df_train_mod['good_pred_draw'].sum()/float(len(df_train_mod))

                                
                result_mode = result
                mode = 'S'
                
#                print result, result_DNB, result_WNB, result_DC
                if result_mode < result_DNB:
                    result_mode = result_DNB
                    mode = 'DNB'
                if result_mode < result_WNB:
                    result_mode = result_WNB
                    mode = 'WNB'
                if result_mode < result_DC:
                    result_mode = result_DC
                    mode = 'DC'
#                print mode
                
                if dict_training_option[sport]['force_mode'] != '':
                    mode = dict_training_option[sport]['force_mode']

                mod_value  = dict_training_option[sport]['mod_value']
                limit_DC   = dict_training_option[sport]['limit_DC']
                
                list_test.append([sport, (mod-1)*mod_value+mod_value, mod*mod_value+mod_value, len(df_train_mod), int(result)/float(len(df_train_mod)), int(result_with_draw)/float(len(df_train_mod)), int(result_DNB)/float(len(df_train_mod)), int(result_WNB)/float(len(df_train_mod)), int(result_DC)/float(len(df_train_mod)), perc_win, bet_diff_high_S, date, mode])
                
                limit_number_exemple = 10
                
                if int(result)/float(len(df_train_mod)) > limit_DC and mode == 'S' and len(df_train_mod)>limit_number_exemple :
                    list_mod_ok.append([round((mod-1)*mod_value+mod_value,2),round(mod*mod_value+mod_value,2), len(df_train_mod), mod, 'S', int(result)/float(len(df_train_mod)), perc_win_good, bet_diff_high_S])
                    dict_temp.update({sport:list_mod_ok})
                    
                if int(result_DNB)/float(len(df_train_mod)) > limit_DC and mode == 'DNB' and len(df_train_mod)>limit_number_exemple:
                    list_mod_ok.append([round((mod-1)*mod_value+mod_value,2),round(mod*mod_value+mod_value,2), len(df_train_mod), mod, 'DNB', int(result_DNB)/float(len(df_train_mod)), perc_win, bet_diff_high_S])
                    dict_temp.update({sport:list_mod_ok})
   
                if int(result_WNB)/float(len(df_train_mod)) > limit_DC and mode == 'WNB' and len(df_train_mod)>limit_number_exemple:
#                    print sport, (mod-1)*mod_value+mod_value, mod*mod_value+mod_value, len(df_train_mod), int(result)/float(len(df_train_mod)), int(result_with_draw)/float(len(df_train_mod)), int(result_DNB)/float(len(df_train_mod)), int(result_WNB)/float(len(df_train_mod)), int(result_DC)/float(len(df_train_mod)), perc_win    
                    list_mod_ok.append([round((mod-1)*mod_value+mod_value,2),round(mod*mod_value+mod_value,2), len(df_train_mod), mod, 'WNB', int(result_WNB)/float(len(df_train_mod)), perc_win, bet_diff_high_S])
                    dict_temp.update({sport:list_mod_ok})
                    
                if int(result_DC)/float(len(df_train_mod)) > limit_DC and mode == 'DC' and len(df_train_mod)>limit_number_exemple:
#                    print sport, (mod-1)*mod_value+mod_value, mod*mod_value+mod_value, len(df_train_mod), int(result)/float(len(df_train_mod)), int(result_with_draw)/float(len(df_train_mod)), int(result_DNB)/float(len(df_train_mod)), int(result_WNB)/float(len(df_train_mod)), int(result_DC)/float(len(df_train_mod)), perc_win    
                    list_mod_ok.append([round((mod-1)*mod_value+mod_value,2),round(mod*mod_value+mod_value,2), len(df_train_mod), mod, 'DC', int(result_DC)/float(len(df_train_mod)), perc_win, bet_diff_high_S])
                    dict_temp.update({sport:list_mod_ok})                    

    df          = pd.DataFrame(list_test)
    try:
        df.columns  = ['sport','bet_min','bet_max','number_bet','S','X','DNB','WNB','DC','perc', 'bet_diff_high_S', 'date', 'mode']                    
        df_a_list = pd.DataFrame(a_list)
        df_a_list.columns = ['diff', 'mod', 'sum', 'len_df', 'sum/len_df', 'std', 'mean', 'median']
        df_a_list['ratio'] = df_a_list['sum']/df_a_list['len_df']
#        a.plot.box(rot=90, grid=True)                    
    except:
        pass
                
    return dict_temp, df


####################################

def optimisation_7_apply(df_test, dict_parameter_sport):
    list_sport      = df_test.sport.unique().tolist()
    df_result_mod   = pd.DataFrame()
    
    df_test['good_pred_draw'] = 0
    try:
        df_test.good_pred_draw[df_test.winner == 0] = 1
    except:
        pass
    df_test.fillna(1, inplace=True)


    for sport in list_sport:
        if sport in dict_parameter_sport['option']:
            mod_value  = dict_parameter_sport['option'][sport]['mod_value']
            df_test_sport = df_test[df_test.sport == sport]
            df_test_sport.sort_values('min_bet', inplace=True)
            df_test_sport['mod'] = df_test_sport.min_bet/mod_value
            df_test_sport['mod'] = df_test_sport['mod'].apply(lambda x: int(x))
        
            list_mod = list(set(df_test_sport['mod'].tolist()))
            list_mod.sort()
            if sport in dict_parameter_sport.keys():
                list_mod_ok    = dict_parameter_sport[sport]
                list_mode_test = [[item[0],item[1]] for item in list_mod_ok]
                list_mode_bet  = [item[4] for item in list_mod_ok]
                list_diff_bet  = [item[7] for item in list_mod_ok]
    
                for i, mod in enumerate(list_mode_test):
#                    ee
#                    print sport, mod[0], mod[1]
                    diff_bet            = list_diff_bet[i]                    
                    df_mod              = df_test_sport[(df_test_sport.min_bet > mod[0]) & (df_test_sport.min_bet < mod[1])]
                    df_mod              = df_mod[df_mod.bet_diff >= diff_bet]
                    mode_bet            = list_mode_bet[i]
                    df_mod['mode_bet']  = mode_bet
                    df_result_mod       = pd.concat((df_result_mod, df_mod))
    
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


# =============================================================================
# 
# =============================================================================

def test_tes(df_test_sport, dict_temp_parameter_sport):
    initial_bankroll            = 500
    bankroll                    = initial_bankroll
    mise                        = 20
    cave                        = 0
    result                      = 0
    min_cave                    = 0
    max_cave                    = 0    
    day_shift                   = 0
    total_result                = 0
    total_cave                  = 0
    total_nbr_bet               = 0
    dict_bankroll               = {}
    dict_bankroll_day           = {}
    dict_parameter_sport_single = {}
    dict_result_sport           = {}
    dict_ok                     = {}
    df_loss                     = pd.DataFrame()
    df_win                      = pd.DataFrame()
    
    df_single_filter = optimisation_7_apply(df_test_sport, dict_temp_parameter_sport)
    
    
    num_good_pred         = 0
    num_good_draw_pred    = 0
    num_bad_pred          = 0
    for item in range(len(df_single_filter)):
        total_nbr_bet = total_nbr_bet + 1
        
        min_bet = df_single_filter.min_bet.iloc[item]+0.0000001
        bet_X   = df_single_filter.bet_X.iloc[item]+0.0000001
        bet_DC  = 1/((1/min_bet)+(1/bet_X))
        bet_DNB = (1-(1/bet_X))*min_bet
        bet_WNB = (1-(1/min_bet))*bet_X
        sport   = df_single_filter.sport.iloc[item]

        try:
            dict_result_sport[sport]['result'] = dict_result_sport[sport]['result']
        except:
            dict_result_sport.update({sport:{'result':0}})
                                

        if df_single_filter.mode_bet.iloc[item] == 'DC':
            cave = cave + mise
            result = result - mise
            dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] - mise})
            dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] - mise

            if df_single_filter.good_pred.iloc[item] == 1 or df_single_filter.winner.iloc[item] == 0:
                result = result + bet_DC*mise
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + bet_DC*mise})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + bet_DC*mise
                num_good_draw_pred = num_good_draw_pred + 1
                df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
            else:
                num_bad_pred = num_bad_pred + 1
                df_loss = pd.concat((df_loss, pd.DataFrame(df_single_filter.iloc[item]).T))


        if df_single_filter.mode_bet.iloc[item] == 'DNB':
            cave = cave + mise
            result = result - mise
            dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] - mise})
            dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] - mise

            if df_single_filter.good_pred.iloc[item] == 1:
                result = result + bet_DNB*mise
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + bet_DNB*mise})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + bet_DNB*mise

                df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
                
            if df_single_filter.winner.iloc[item] == 0:
                result = result + mise
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + mise})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + mise

                num_good_draw_pred = num_good_draw_pred + 1
                df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))

            
            if df_single_filter.good_pred.iloc[item] == 0 and df_single_filter.winner.iloc[item] != 0:
                num_bad_pred = num_bad_pred + 1
                df_loss = pd.concat((df_loss, pd.DataFrame(df_single_filter.iloc[item]).T))

                
        if df_single_filter.mode_bet.iloc[item] == 'WNB':
            cave = cave + mise
            result = result - mise
            dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] - mise})
            dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] - mise

            
            if df_single_filter.good_pred.iloc[item] == 1:
                result = result + mise
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + mise})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + mise

                df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
                
            if df_single_filter.winner.iloc[item] == 0:
                result = result + bet_WNB*mise
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + bet_WNB*mise})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + bet_WNB*mise

                num_good_draw_pred = num_good_draw_pred + 1
                df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
            
            if df_single_filter.good_pred.iloc[item] == 0 and df_single_filter.winner.iloc[item] != 0:
                num_bad_pred = num_bad_pred + 1
                df_loss = pd.concat((df_loss, pd.DataFrame(df_single_filter.iloc[item]).T))
                
                                    
        
        if df_single_filter.mode_bet.iloc[item] == 'X':
            cave = cave + mise*2
            result = result - mise*2
            dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] - mise*2})
            dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] - mise*2

            if df_single_filter.good_pred.iloc[item] == 1 and df_single_filter.winner.iloc[item] != 0:
                result = result + df_single_filter.min_bet.iloc[item]*mise
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + df_single_filter.min_bet.iloc[item]*mise})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + df_single_filter.min_bet.iloc[item]*mise

                num_good_draw_pred = num_good_draw_pred + 1
                df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
            
            if df_single_filter.winner.iloc[item] == 0:
                result = result + df_single_filter.bet_X.iloc[item]*mise
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + df_single_filter.bet_X.iloc[item]*mise})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + df_single_filter.bet_X.iloc[item]*mise

                num_good_draw_pred = num_good_draw_pred + 1
                df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
            
            if df_single_filter.good_pred.iloc[item] == 0 and df_single_filter.winner.iloc[item] != 0:
                num_bad_pred = num_bad_pred + 1
                df_loss = pd.concat((df_loss, pd.DataFrame(df_single_filter.iloc[item]).T))


        if df_single_filter.mode_bet.iloc[item] == 'S':
            cave = cave + mise
            result = result - mise
            dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] - mise})
            dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] - mise

            if df_single_filter.good_pred.iloc[item] == 1:
                result = result + df_single_filter.min_bet.iloc[item]*mise
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + + df_single_filter.min_bet.iloc[item]*mise})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + df_single_filter.min_bet.iloc[item]*mise

                num_good_pred = num_good_pred + 1
                df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
            else:
                num_bad_pred = num_bad_pred + 1
                df_loss = pd.concat((df_loss, pd.DataFrame(df_single_filter.iloc[item]).T))
        
        
    if len(df_single_filter) != 0:
        print('******** RESULT SIMULATION **********')
#        print dict_temp_parameter_sport
        print 'Mise                  : ', int(mise), '€'
        print 'Number Good pred      : ', num_good_pred
        print 'Number Good Draw pred : ', num_good_draw_pred
        print 'Number Bad pred       : ', num_bad_pred
        print '% : ', round(num_good_pred/float(num_good_pred+num_bad_pred+0.01)*100,2), '%'
        print 'Mean bet : ', df_single_filter.min_bet.mean()
        print 'cave     : ', int(cave),' €'
        print 'gain pur : ', int(result),' €'
        print 'ROI cave : ', round(result/float(cave)*100,2), '%'
        print 'ROI mise : ',round(result/mise,2)*100,"%"
        print('*************************************')
            
    bankroll     = bankroll + result
    total_result = total_result + result
    total_cave   = total_cave + cave   
    
    if total_result < min_cave:
        min_cave = total_result 
    if total_result > max_cave:
        max_cave = total_result
        

    print 'BANKROLL       : ', int(bankroll), '€'
    print 'GAIN TOTAL     : ', int(total_result), '€'
    print 'INVEST TOTAL   : ', int(total_cave)
    print 'NBR BET TOTAL  : ', total_nbr_bet
    print 'ROI cave       : ', round(total_result/float(total_cave+0.0001)*100,2), '%'
    print 'ROC cave       : ', round(total_result/float(initial_bankroll)*100,2), '%'
    print 'MIN CAVE       : ', int(min_cave), '€', int(round(min_cave/mise))
    print 'MAX CAVE       : ', int(max_cave), '€', int(round(max_cave/mise))
    print ''
    
    try:
        list_sport_win_loss = list(set(df_win.sport.unique().tolist()+df_loss.sport.unique().tolist()))
        dict_ok = {}
        for sport in list_sport_win_loss:
            df_win['mod'] = df_win.min_bet/dict_temp_parameter_sport['option'][sport]['mod_value']
            df_win['mod'] = df_win['mod'].apply(lambda x: int(x))
            df_loss['mod'] = df_loss.min_bet/dict_temp_parameter_sport['option'][sport]['mod_value']
            df_loss['mod'] = df_loss['mod'].apply(lambda x: int(x))
            
            
            df_win['gain'] = 0
            df_win.gain[df_win.mode_bet == 'S'] = (df_win.min_bet[df_win.mode_bet == 'S']-1) * mise
            df_win.gain[(df_win.mode_bet == 'WNB') & (df_win.winner == 0)] = (df_win.bet_X[(df_win.mode_bet == 'WNB') & (df_win.winner == 0)]*(1-(1/df_win.min_bet[(df_win.mode_bet == 'WNB') & (df_win.winner == 0)]))-1) * mise
            df_loss['gain'] = -mise 
            
            total = str(len(df_win[df_win.sport == sport]) + len(df_loss[df_loss.sport == sport]))
            total_gain = str(int(df_win[df_win.sport == sport]['gain'].sum() + df_loss[df_loss.sport == sport]['gain'].sum()))
            print sport, '=> ', total.rjust(4), 'bet /', total_gain.rjust(4), 'euros /', round(100*len(df_win[df_win.sport == sport])/float(len(df_win[df_win.sport == sport])+len(df_loss[df_loss.sport == sport])),2),'%'
            df_win.bet_diff = df_win.bet_diff.apply(lambda x: round(math.floor(x*10)/10.0,1))
            df_loss.bet_diff = df_loss.bet_diff.apply(lambda x: round(math.floor(x*10)/10.0,1))
            list_mod_win_loss = list(set(df_win[u'mod'][df_win.sport == sport].unique().tolist()+df_loss[u'mod'][df_loss.sport == sport].unique().tolist()))
            for mod in list_mod_win_loss:
                list_diff_win_loss = list(set(df_win[u'bet_diff'][(df_win.sport == sport) & (df_win[u'mod'] == mod)].unique().tolist()+df_loss[u'bet_diff'][(df_loss.sport == sport) & (df_loss[u'mod'] == mod)].unique().tolist()))
                list_diff_win_loss.sort()
                for diff in list_diff_win_loss:
                    df_win_diff = df_win[(df_win[u'mod'] == mod) & (df_win.sport == sport) & (df_win.bet_diff >= diff)]
                    df_loss_diff = df_loss[(df_loss[u'mod'] == mod) & (df_loss.sport == sport) & (df_loss.bet_diff >= diff)]
                    result_gain  = int(sum(df_win_diff['gain'][df_win_diff[u'mod'] == mod])+sum(df_loss_diff['gain'][df_loss_diff[u'mod'] == mod]))
                    nbr_bet      = len(df_win_diff[(df_win_diff[u'mod'] == mod) & (df_win_diff.sport == sport)])+len(df_loss_diff[(df_loss_diff[u'mod'] == mod) & (df_loss_diff.sport == sport)])
                    perc         = round(100*len(df_win_diff[(df_win_diff[u'mod'] == mod) & (df_win_diff.sport == sport)])/float(len(df_win_diff[(df_win_diff[u'mod'] == mod) & (df_win_diff.sport == sport)])+len(df_loss_diff[(df_loss_diff[u'mod'] == mod) & (df_loss_diff.sport == sport)])),1)
                    if (nbr_bet > 5) and result_gain>0:
#                        try:
#                            _ = dict_ok[sport]
#                        except:
#                            dict_ok.update({sport:{}})
#                            
                        try:
                            if dict_ok[mod]['perc'] < perc:
                                dict_ok[mod]['result_gain'] = result_gain
                                dict_ok[mod]['diff'] = diff    
                                dict_ok[mod]['result_gain'] = result_gain
                        except:
                            dict_ok.update({mod:{'result_gain':result_gain , 'diff':diff, 'perc':perc}})
                        print '*', round(mod*0.1,1), '-', round((mod+1)*0.1,1), '|', str(diff) ,'=>', str(len(df_win_diff[(df_win_diff[u'mod'] == mod) & (df_win_diff.sport == sport)])+len(df_loss_diff[(df_loss_diff[u'mod'] == mod) & (df_loss_diff.sport == sport)])).rjust(4), 'bet /', str(int(sum(df_win_diff['gain'][df_win_diff[u'mod'] == mod])+sum(df_loss_diff['gain'][df_loss_diff[u'mod'] == mod]))).rjust(4)   , 'euros /',  round(100*len(df_win_diff[(df_win_diff[u'mod'] == mod) & (df_win_diff.sport == sport)])/float(len(df_win_diff[(df_win_diff[u'mod'] == mod) & (df_win_diff.sport == sport)])+len(df_loss_diff[(df_loss_diff[u'mod'] == mod) & (df_loss_diff.sport == sport)])),1),'%'
    except Exception, e:
        print e
        pass
    print '******************************************'


    
    return df_win, df_loss, dict_ok

# =============================================================================
# 
# =============================================================================
def optimisation_8(df_train, df_test, dict_training_option):
    dict_temp   = {}
    df_a_list = pd.DataFrame()

    ### only bet upper limit
    df_train = df_train[df_train.min_bet >= dict_training_option[dict_training_option.keys()[0]]['limit_bet']]
                
    a            = pd.DataFrame(df_train.pays.value_counts()>500)
    a            = a[a['pays'] == True]
    list_big_pays = a.index.tolist()
    list_big_pays = [str(item) for item in list_big_pays]
    df_train = df_train[df_train['pays'].isin(list_big_pays)]

    list_sport  = df_train.sport.unique().tolist()
    ###
    list_pays   = df_train.pays.unique().tolist()
    
#    df_train.fillna(1, inplace=True)

    df_train['good_pred_draw'] = 0
    df_train.good_pred_draw[df_train.winner == 0] = 1

    dict_result = {}
    for sport in list_sport:
        try:
            _ = dict_result[sport]
        except:
            dict_result.update({sport:{}})
                            
        a = pd.DataFrame()
        a_list = []
        for z, pays in enumerate(list_pays):
            print pays, z+1, len(list_pays)
            
            ### filter on sport
            df_train_sport = df_train[df_train.sport == sport]
    
            ### filter pays
            df_train_sport = df_train_sport[df_train_sport.pays == pays]
            
            ### mod value
            df_train_sport['mod'] = df_train_sport.min_bet/dict_training_option[sport]['mod_value']
            df_train_sport['mod'] = df_train_sport['mod'].apply(lambda x: int(x))
            list_mod = list(set(df_train_sport['mod'].tolist()))
            list_mod.sort()
    
            ###        
            df_train_sport.sort_values('min_bet', inplace=True)
            
            for mod in list_mod:
                df_train_mod = df_train_sport[df_train_sport['mod'] == int(mod)]
    #            print mod
    #            if mod == 21 : ee
                step_diff_bet = 0.1
                for i in range(100):
                    df = df_train_mod[df_train_mod.bet_diff > i*step_diff_bet]
            
                    df_train_mod_analysis_freq = df.set_index('match_date')
                    df_train_mod_analysis_freq.dropna(inplace=True)
                    df_train_mod_analysis_freq          = df_train_mod_analysis_freq.resample('W').sum()
                    df_train_mod_analysis_freq['perc'] = df_train_mod_analysis_freq['good_pred']/(df_train_mod_analysis_freq['good_pred']+df_train_mod_analysis_freq['bad_pred'])
                    df_train_mod_analysis_freq['gain'] = df_train_mod_analysis_freq['good_pred']*((mod/10.0)-1)-df_train_mod_analysis_freq['bad_pred']
    
                    GAIN_MEAN  = df_train_mod_analysis_freq['gain'].mean()
                    GAIN_STD   = df_train_mod_analysis_freq['gain'].std()
                    limit_mean_min = 0.0
                    limit_std_max  = 0.8
                    if GAIN_MEAN > limit_mean_min and GAIN_STD <= limit_std_max and len(df)>10:
                        a_list.append([GAIN_MEAN, GAIN_STD, df_train_mod_analysis_freq['gain'].sum(), len(df), mod, i*step_diff_bet, pays])
                        
            if len(a_list) != 0:
                df_a_list = pd.DataFrame(a_list)
                df_a_list.columns = ['GAIN_MEAN', 'GAIN_STD', 'sum', 'len_df', 'mod', 'diff', 'pays']
                df_a_list['name'] = df_a_list['mod'].map(str) + '_' + df_a_list['diff'].map(str)

        list_pays = df_a_list.pays.unique().tolist()
        fig, axes = plt.subplots(nrows=len(list_pays)/4+1, ncols=4, sharex=True, sharey=True)
        for ax, pays in zip(axes.flat, list_pays):
            dict_result[sport].update({pays:{}})
            print '\n\n\n**********ùùùùùùùù'
            print pays
            print '**********ùùùùùùùù'
            df_a_list[df_a_list.pays == pays].plot(kind='scatter',x='GAIN_MEAN',y='GAIN_STD', title=pays, ax=ax)
            df_a_list[df_a_list.pays == pays][['GAIN_MEAN','GAIN_STD','name']].apply(lambda x: ax.text(*x),axis=1)

            dict_temp_temp = {}
            list_temp_parameter_sport = []     
            dict_temp_parameter_sport = {}
            dict_ok = {}
            for item in range(len(df_a_list[df_a_list.pays == pays])):
                mod     = df_a_list[df_a_list.pays == pays].iloc[item]['mod']
                diff    = df_a_list[df_a_list.pays == pays].iloc[item]['diff']
                GAIN_MEAN = df_a_list[df_a_list.pays == pays].iloc[item]['GAIN_MEAN']
                GAIN_STD  = df_a_list[df_a_list.pays == pays].iloc[item]['GAIN_STD']
                mod_step = 1
#                list_temp_parameter_sport.append([round(mod/10.0,2), round((mod+mod_step)/10.0,2), GAIN_MEAN, GAIN_STD, 'S', '', '', round(diff,2)])

                ### find lowest std                
                try:
                    if dict_temp_temp[mod]['GAIN_STD'] > GAIN_STD:
                        dict_temp_temp[mod]['GAIN_STD'] = GAIN_STD
                        dict_temp_temp[mod]['diff'] = diff

                except:
                    dict_temp_temp.update({mod:{'GAIN_STD':GAIN_STD, 'diff':diff, 'GAIN_MEAN':GAIN_MEAN}})
            
            for key_mod, value_mod in dict_temp_temp.items():
                mod       = int(key_mod)
                GAIN_MEAN = value_mod['GAIN_MEAN'] 
                GAIN_STD  = value_mod['GAIN_STD']
                diff      = value_mod['diff']
                list_temp_parameter_sport.append([round(mod/10.0,2), round((mod+mod_step)/10.0,2), GAIN_MEAN, GAIN_STD, 'S', '', '', round(diff,2)])
                ### shortcut
                dict_ok.update({mod:{'result_gain':0 , 'diff':diff, 'perc':0}})

            dict_temp_parameter_sport.update({sport:list_temp_parameter_sport, 'option':dict_training_option})
            
#            if pays == 'brazil': ee
            ### VALIDATION
            df_test_sport = df_test[df_test.pays == pays].copy()
#            df_win, df_loss, dict_ok = test_tes(df_test_sport, dict_temp_parameter_sport)
            dict_result[sport][pays].update(dict_ok)
            
            
            
            """
            ax = df_a_list[df_a_list.pays == pays].plot(kind='scatter',x='GAIN_MEAN',y='GAIN_STD', title=pays)
            df_a_list[df_a_list.pays == pays][['GAIN_MEAN','GAIN_STD','name']].apply(lambda x: ax.text(*x),axis=1)
            """
                
    return dict_result, df_a_list

# =============================================================================
# 
# =============================================================================
def optimisation_8_apply(df_test, dict_parameter):
    df_test['mod'] = df_test.min_bet/0.1
    df_test['mod'] = df_test['mod'].apply(lambda x: int(x))
     
    df_final = pd.DataFrame()     
    list_sport = dict_parameter['option'].keys()
    for sport in list_sport:
        list_pays = dict_parameter[sport].keys()
        for pays in list_pays:
            list_mod = dict_parameter[sport][pays].keys()
            if len(list_mod) != 0:
                for mod in list_mod:
                    diff = dict_parameter[sport][pays][mod]['diff']
#                    print sport, pays, mod, diff
                    df_mod = df_test[(df_test[u'mod'] == int(mod)) & (df_test[u'bet_diff'] >= diff) & (df_test[u'pays'] == pays) & (df_test[u'sport'] == sport)]
                    df_final = pd.concat((df_final, df_mod))
    df_final['mode_bet'] = 'S'
    return df_final