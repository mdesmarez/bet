#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 15:55:11 2018

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
import sys
import json

import matplotlib.pyplot  as plt
import pandas             as pd
import numpy              as np

from bs4                  import BeautifulSoup
from glob                                                                      import glob
from datetime                                                                  import datetime
from datetime                                                                  import timedelta

from PS3838_support_function                                                   import optimisation_7, optimisation_7_apply, encode_decode

# =============================================================================
# 
# =============================================================================
dict_parameter = {'option':{}}



# =============================================================================
# 
# =============================================================================
###
df_parlay = pd.DataFrame.from_csv('../dataset/local/df_parlay.xls', encoding='utf-8')
df_parlay.team_home = df_parlay.team_home.apply(lambda x : encode_decode(x))
df_result = pd.DataFrame.from_csv('../dataset/local/df_result.xls', encoding='utf-8')

###
df_single = pd.DataFrame.from_csv('../dataset/local/df_single.xls', encoding='utf-8')
df_single.sport = df_single.sport.apply(lambda x : x.lower().replace('-',' '))
df_result_single = df_result.copy()
df_result_single.sport = df_result_single.sport.apply(lambda x : x.lower().replace('-',' '))

###
df_merge                           = pd.merge(df_parlay, df_result, how='inner', on=['match_date','sport','team_home'])
df_merge = df_merge[['match_date','sport','ligue','bet_1','bet_2','bet_X','bet_diff','min_bet','winner','prediction','score']]
df_merge['good_pred']                          = 0
df_merge.good_pred[df_merge.prediction == df_merge.winner] = 1
df_merge['bad_pred']                           = 0
df_merge.bad_pred[df_merge.prediction != df_merge.winner]  = 1
df_merge.match_date                = df_merge.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

###
df_merge_single                           = pd.merge(df_single, df_result_single, how='inner', on=['match_date','sport','team_home'])
df_merge_single = df_merge_single[['match_date','sport','ligue','bet_1','bet_2','bet_X','bet_diff','min_bet','winner','prediction','team_home']]
df_merge_single['good_pred']                          = 0
df_merge_single.good_pred[df_merge_single.prediction == df_merge_single.winner] = 1
df_merge_single['bad_pred']                           = 0
df_merge_single.bad_pred[df_merge_single.prediction != df_merge_single.winner]  = 1
df_merge_single.match_date                = df_merge_single.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))



# =============================================================================
# SOCCER
# =============================================================================
### LOAD DATA
df_soccer = pd.DataFrame()
list_soccer  = glob('../dataset/local/soccer/*.csv')
for i, file_soccer in enumerate(list_soccer):
    df_soccer_temp = pd.DataFrame.from_csv(file_soccer, encoding='utf-8')
    df_soccer = pd.concat((df_soccer, df_soccer_temp))
    
df_soccer['sport']       = 'soccer'
df_soccer['bet_diff']    = df_soccer.bet_1-df_soccer.bet_2
df_soccer['min_bet']     = 0
df_soccer['prediction']  = 0
df_soccer['prediction']  = 0
df_soccer['good_pred']   = 0
df_soccer['bad_pred']    = 0
df_soccer['winner']      = df_soccer['result']  
df_soccer['min_bet']     = df_soccer[['bet_1','bet_2']].min(axis=1)
df_soccer['prediction']  = df_soccer.bet_diff.apply(lambda x : "1" if x<0 else "2")
df_soccer['bet_diff']    = abs(df_soccer['bet_diff'])

df_soccer = df_soccer[['match_date', 'sport', 'ligue','bet_1', 'bet_2', 'bet_X', 'bet_diff', 'min_bet', 'winner', 'prediction', 'team_home', 'good_pred', 'bad_pred']]

df_soccer.winner[df_soccer.winner == 'X'] = 0
df_soccer.winner[df_soccer.winner == '1'] = 1
df_soccer.winner[df_soccer.winner == '2'] = 2

df_soccer.winner = df_soccer.winner.astype(int)
df_soccer.prediction = df_soccer.prediction.astype(int)
df_soccer['good_pred'] = 0
df_soccer.good_pred[df_soccer.winner == df_soccer.prediction] = 1    
df_soccer.bad_pred[df_soccer.good_pred != 1] = 1

df_soccer.match_date = df_soccer.match_date.apply(lambda x : datetime.fromtimestamp(x))#.strftime('%Y-%m-%d %H:%M:%S'))

###
#df_soccer = pd.concat((df_soccer,df_merge_single[df_merge_single.sport == 'soccer']))


df_test  = df_soccer[df_soccer.match_date > datetime(2019, 8, 8, 0, 46, 43, 100000)]
df_train = df_soccer[df_soccer.match_date < datetime(2019, 8, 8, 0, 46, 43, 100000)]


### OPTIONS
dict_training_option = {'soccer':{
                                'mod_value':       0.1,
                                'limit_bet':       2.0,
                                'limit_DC':        0.025,
                                'limit_perf_min':  0,
                                'force_mode':      '',
                                 }}

### TRAINING
dict_parameter_sport, df_parameter_sport = optimisation_7(df_train, dict_training_option)
dict_parameter.update({dict_parameter_sport.keys()[0]:dict_parameter_sport[dict_parameter_sport.keys()[0]]})
dict_parameter['option'].update(dict_training_option)
        
### SAVE
with open('../model/local/dict_parameter_sport.json', 'w') as outfile:
    json.dump(dict_parameter, outfile)



# =============================================================================
# 
# =============================================================================
### LOAD DATA
df_ALL = pd.DataFrame.from_csv('../dataset/local/df_ALL.xls', encoding='utf-8')
df_handball = df_ALL[df_ALL.sport == 'handball']

    
df_handball['sport']       = 'handball'
df_handball['bet_diff']    = df_handball.bet_1-df_handball.bet_2
df_handball['min_bet']     = 0
df_handball['prediction']  = 0
df_handball['prediction']  = 0
df_handball['good_pred']   = 0
df_handball['bad_pred']    = 0
df_handball['winner']      = df_handball['result']  
df_handball['min_bet']     = df_handball[['bet_1','bet_2']].min(axis=1)
df_handball['prediction']  = df_handball.bet_diff.apply(lambda x : "1" if x<0 else "2")
df_handball['bet_diff']    = abs(df_handball['bet_diff'])

df_handball = df_handball[['match_date', 'sport', 'ligue','bet_1', 'bet_2', 'bet_X', 'bet_diff', 'min_bet', 'winner', 'prediction', 'team_home', 'good_pred', 'bad_pred']]

df_handball.winner[df_handball.winner == 'X'] = 0
df_handball.winner[df_handball.winner == '1'] = 1
df_handball.winner[df_handball.winner == '2'] = 2

df_handball.winner = df_handball.winner.astype(int)
df_handball.prediction = df_handball.prediction.astype(int)
df_handball['good_pred'] = 0
df_handball.good_pred[df_handball.winner == df_handball.prediction] = 1    
df_handball.bad_pred[df_handball.good_pred != 1] = 1

df_handball.match_date = df_handball.match_date.apply(lambda x : datetime.fromtimestamp(x))#.strftime('%Y-%m-%d %H:%M:%S'))

df_test  = df_handball[df_handball.match_date > datetime(2019, 8, 8, 0, 46, 43, 100000)]
df_train = df_handball[df_handball.match_date < datetime(2019, 8, 8, 0, 46, 43, 100000)]


### OPTIONS
dict_training_option = {'handball':{
                                'mod_value':       0.1,
                                'limit_bet':       1.5,
                                'limit_DC':        0.01,
                                'limit_perf_min':  0,
                                'force_mode':      '',
                                 }}

### TRAINING
dict_parameter_sport, df_parameter_handball = optimisation_7(df_train, dict_training_option)
dict_parameter.update({dict_parameter_sport.keys()[0]:dict_parameter_sport[dict_parameter_sport.keys()[0]]})
dict_parameter['option'].update(dict_training_option)
        
### SAVE
with open('../model/local/dict_parameter_sport.json', 'w') as outfile:
    json.dump(dict_parameter, outfile)
    

# =============================================================================
# 
# =============================================================================
### LOAD DATA
df_ALL = pd.DataFrame.from_csv('../dataset/local/df_ALL.xls', encoding='utf-8')
df_basketball = df_ALL[df_ALL.sport == 'basketball']

    
df_basketball['sport']       = 'basketball'
df_basketball['bet_diff']    = df_basketball.bet_1-df_basketball.bet_2
df_basketball['min_bet']     = 0
df_basketball['prediction']  = 0
df_basketball['prediction']  = 0
df_basketball['good_pred']   = 0
df_basketball['bad_pred']    = 0
df_basketball['winner']      = df_basketball['result']  
df_basketball['min_bet']     = df_basketball[['bet_1','bet_2']].min(axis=1)
df_basketball['prediction']  = df_basketball.bet_diff.apply(lambda x : "1" if x<0 else "2")
df_basketball['bet_diff']    = abs(df_basketball['bet_diff'])

df_basketball = df_basketball[['match_date', 'sport', 'ligue','bet_1', 'bet_2', 'bet_X', 'bet_diff', 'min_bet', 'winner', 'prediction', 'team_home', 'good_pred', 'bad_pred']]

df_basketball.winner[df_basketball.winner == 'X'] = 0
df_basketball.winner[df_basketball.winner == '1'] = 1
df_basketball.winner[df_basketball.winner == '2'] = 2

df_basketball.winner = df_basketball.winner.astype(int)
df_basketball.prediction = df_basketball.prediction.astype(int)
df_basketball['good_pred'] = 0
df_basketball.good_pred[df_basketball.winner == df_basketball.prediction] = 1    
df_basketball.bad_pred[df_basketball.good_pred != 1] = 1

df_basketball.match_date = df_basketball.match_date.apply(lambda x : datetime.fromtimestamp(x))#.strftime('%Y-%m-%d %H:%M:%S'))

df_test  = df_basketball[df_basketball.match_date > datetime(2018, 8, 8, 0, 46, 43, 100000)]
df_train = df_basketball[df_basketball.match_date < datetime(2018, 8, 8, 0, 46, 43, 100000)]


### OPTIONS
dict_training_option = {'basketball':{
                                'mod_value':       0.1,
                                'limit_bet':       1.,
                                'limit_DC':        0.04,
                                'limit_perf_min':  0,
                                'force_mode':      '',
                                 }}

### TRAINING
dict_parameter_sport, df_parameter_sport = optimisation_7(df_train, dict_training_option)
try:
    dict_parameter.update({dict_parameter_sport.keys()[0]:dict_parameter_sport[dict_parameter_sport.keys()[0]]})
    dict_parameter['option'].update(dict_training_option)
            
    ### SAVE
    with open('../model/local/dict_parameter_sport.json', 'w') as outfile:
        json.dump(dict_parameter, outfile)
except:
    pass

# =============================================================================
# 
# =============================================================================
### LOAD DATA
df_ALL = pd.DataFrame.from_csv('../dataset/local/df_ALL.xls', encoding='utf-8')
df_volleyball = df_ALL[df_ALL.sport == 'volleyball']

    
df_volleyball['sport']       = 'volleyball'
df_volleyball['bet_diff']    = df_volleyball.bet_1-df_volleyball.bet_2
df_volleyball['min_bet']     = 0
df_volleyball['prediction']  = 0
df_volleyball['prediction']  = 0
df_volleyball['good_pred']   = 0
df_volleyball['bad_pred']    = 0
df_volleyball['winner']      = df_volleyball['result']  
df_volleyball['min_bet']     = df_volleyball[['bet_1','bet_2']].min(axis=1)
df_volleyball['prediction']  = df_volleyball.bet_diff.apply(lambda x : "1" if x<0 else "2")
df_volleyball['bet_diff']    = abs(df_volleyball['bet_diff'])

df_volleyball = df_volleyball[['match_date', 'sport', 'ligue','bet_1', 'bet_2', 'bet_X', 'bet_diff', 'min_bet', 'winner', 'prediction', 'team_home', 'good_pred', 'bad_pred']]

df_volleyball.winner[df_volleyball.winner == 'X'] = 0
df_volleyball.winner[df_volleyball.winner == '1'] = 1
df_volleyball.winner[df_volleyball.winner == '2'] = 2

df_volleyball.winner = df_volleyball.winner.astype(int)
df_volleyball.prediction = df_volleyball.prediction.astype(int)
df_volleyball['good_pred'] = 0
df_volleyball.good_pred[df_volleyball.winner == df_volleyball.prediction] = 1    
df_volleyball.bad_pred[df_volleyball.good_pred != 1] = 1

df_volleyball.match_date = df_volleyball.match_date.apply(lambda x : datetime.fromtimestamp(x))#.strftime('%Y-%m-%d %H:%M:%S'))

###
#df_volleyball = pd.concat((df_volleyball,df_merge_single[df_merge_single.sport == 'volleyball']))

df_test  = df_volleyball[df_volleyball.match_date > datetime(2018, 8, 22, 0, 46, 43, 100000)]
df_train = df_volleyball[df_volleyball.match_date < datetime(2018, 8, 22, 0, 46, 43, 100000)]


### OPTIONS
dict_training_option = {'volleyball':{
                                'mod_value':       0.1,
                                'limit_bet':       1.55,
                                'limit_DC':        0.01,
                                'limit_perf_min':  0,
                                'force_mode':      '',
                                 }}

### TRAINING
dict_parameter_sport, df_parameter_sport_volleyball = optimisation_7(df_train, dict_training_option)
try:
    dict_parameter.update({dict_parameter_sport.keys()[0]:dict_parameter_sport[dict_parameter_sport.keys()[0]]})
    dict_parameter['option'].update(dict_training_option)
            
    ### SAVE
    with open('../model/local/dict_parameter_sport.json', 'w') as outfile:
        json.dump(dict_parameter, outfile)
except:
    pass

# =============================================================================
# 
# =============================================================================
### LOAD DATA
df_ALL = pd.DataFrame.from_csv('../dataset/local/df_ALL.xls', encoding='utf-8')
df_tennis = df_ALL[df_ALL.sport == 'tennis']

    
df_tennis['sport']       = 'tennis'
df_tennis['bet_diff']    = df_tennis.bet_1-df_tennis.bet_2
df_tennis['min_bet']     = 0
df_tennis['prediction']  = 0
df_tennis['prediction']  = 0
df_tennis['good_pred']   = 0
df_tennis['bad_pred']    = 0
df_tennis['winner']      = df_tennis['result']  
df_tennis['min_bet']     = df_tennis[['bet_1','bet_2']].min(axis=1)
df_tennis['prediction']  = df_tennis.bet_diff.apply(lambda x : "1" if x<0 else "2")
df_tennis['bet_diff']    = abs(df_tennis['bet_diff'])

df_tennis = df_tennis[['match_date', 'sport', 'ligue','bet_1', 'bet_2', 'bet_X', 'bet_diff', 'min_bet', 'winner', 'prediction', 'team_home', 'good_pred', 'bad_pred']]

df_tennis.winner[df_tennis.winner == 'X'] = 0
df_tennis.winner[df_tennis.winner == '1'] = 1
df_tennis.winner[df_tennis.winner == '2'] = 2

df_tennis.winner = df_tennis.winner.astype(int)
df_tennis.prediction = df_tennis.prediction.astype(int)
df_tennis['good_pred'] = 0
df_tennis.good_pred[df_tennis.winner == df_tennis.prediction] = 1    
df_tennis.bad_pred[df_tennis.good_pred != 1] = 1

df_tennis.match_date = df_tennis.match_date.apply(lambda x : datetime.fromtimestamp(x))#.strftime('%Y-%m-%d %H:%M:%S'))

###
#df_tennis = pd.concat((df_tennis,df_merge_single[df_merge_single.sport == 'tennis']))

df_test  = df_tennis[df_tennis.match_date > datetime(2018, 8, 22, 0, 46, 43, 100000)]
df_train = df_tennis[df_tennis.match_date < datetime(2018, 8, 22, 0, 46, 43, 100000)]


### OPTIONS
dict_training_option = {'tennis':{
                                'mod_value':       0.1,
                                'limit_bet':       1.,
                                'limit_DC':        0.1809,
                                'limit_perf_min':  0,
                                'force_mode':      '',
                                 }}

### TRAINING
dict_parameter_sport, df_parameter_sport_tennis = optimisation_7(df_train, dict_training_option)
try:
    dict_parameter.update({dict_parameter_sport.keys()[0]:dict_parameter_sport[dict_parameter_sport.keys()[0]]})
    dict_parameter['option'].update(dict_training_option)
            
    ### SAVE
    with open('../model/local/dict_parameter_sport.json', 'w') as outfile:
        json.dump(dict_parameter, outfile)
except:
    pass