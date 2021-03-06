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

from bs4                  import BeautifulSoup
from glob                                                                      import glob
from datetime                                                                  import datetime
from datetime                                                                  import timedelta

from PS3838_support_function                                                   import optimisation_8, optimisation_7, optimisation_7_apply, encode_decode

# =============================================================================
# 
# =============================================================================
dict_parameter_save = {'option':{}}



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
df_result_single.dropna(inplace=True)
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
list_soccer  = glob('../dataset/local/soccer_old/*.csv')
for i, file_soccer in enumerate(list_soccer):
    df_soccer_temp = pd.DataFrame.from_csv(file_soccer, encoding='utf-8')
    df_soccer = pd.concat((df_soccer, df_soccer_temp))

"""
os.system('wget http://35.195.191.78:8080/bet/prod/bet/dataset/local/soccer/df_ALL_soccer.xls')
os.system('mv "df_ALL_soccer.xls" "../dataset/local/soccer/df_ALL_soccer.xls"')
"""

df_ALL = pd.DataFrame.from_csv('../dataset/local/soccer/df_ALL_soccer.xls', encoding='utf-8')
df_soccer = df_ALL[df_ALL.sport == 'soccer']
#df_soccer = pd.concat((df_soccer,df_ALL[df_ALL.sport == 'soccer']))
#df_soccer['bet_1'] = df_soccer.bet_1.apply(lambda x : (x/100)+1 if x>0 else (100/(-x))+1)
#df_soccer['bet_2'] = df_soccer.bet_2.apply(lambda x : (x/100)+1 if x>0 else (100/(-x))+1)
#df_soccer['bet_X'] = df_soccer.bet_X.apply(lambda x : (x/100)+1 if x>0 else (100/(-x))+1)


#df_soccer = df_soccer[df_soccer["ligue"].str.contains('Tercera')]

###
#df_soccer = df_soccer[~df_soccer["ligue"].str.contains('Cup')]
#df_soccer = df_soccer[~df_soccer["ligue"].str.contains('Cop')]
#df_soccer = df_soccer[~df_soccer["ligue"].str.contains('Coup')]
#df_soccer = df_soccer[~df_soccer["ligue"].str.contains('Euro')]
#df_soccer = df_soccer[~df_soccer["ligue"].str.contains('World')]
#df_soccer = df_soccer[df_soccer["pays"].str.contains('israel')]


"""
### old dataset runnning
df_ALL = df_merge_single.copy()
df_soccer = df_ALL[df_ALL.sport == 'soccer']
#df_soccer = df_ALL[df_ALL.sport == 'e sports']
#df_soccer = df_ALL[df_ALL.sport == 'volleyball']
#df_soccer = df_ALL[df_ALL.sport == 'handball']

df_soccer['sport']       = 'soccer'

#datetime_limit = datetime(2019, 01, 11, 0, 46, 43, 100000)
#df_soccer  = df_soccer[(df_soccer.match_date < datetime_limit)]

from sklearn.model_selection import train_test_split
df_train, df_test = train_test_split(df_soccer, test_size=0.5)

df_train['ligue'] = 'ALL - ALL'
df_train['pays'] = 'ALL'
df_test['pays'] = 'ALL'
dict_parameter_sport, df_a_list = optimisation_8(df_train, df_test, dict_training_option)

"""
  
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

df_soccer = df_soccer[['match_date', 'sport', 'pays', 'ligue','bet_1', 'bet_2', 'bet_X', 'bet_diff', 'min_bet', 'winner', 'prediction', 'team_home', 'good_pred', 'bad_pred']]

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


"""
df_soccer = df_soccer[df_soccer.pays == 'spain']
df_soccer = df_soccer[df_soccer["ligue"].str.contains('LaLiga2')]
"""

datetime_limit = datetime(2018, 9, 21, 0, 46, 43, 100000)
df_test  = df_soccer[(df_soccer.match_date > datetime_limit)]# & (df_soccer.match_date < datetime(2018, 11, 20, 0, 46, 43, 100000))]
df_train = df_soccer[(df_soccer.match_date < datetime_limit)]# & (df_soccer.match_date > datetime(2017, 9, 9, 0, 46, 43, 100000))]
ee
"""
df_train.pays.value_counts()
df_train.ligue.value_counts()

"""

### OPTIONS
dict_training_option = {'soccer':{
                                'mod_value':                0.1,
                                'limit_bet':                1.,
                                'limit_DC':                 0.0,
                                'limit_perf_min':           0,
                                'force_mode':               '',
                                'limit_mean_min':           0.0,
                                'limit_std_max':            5.8,
                                'nbr_min_match_by_pays':    10,
                                'COMPROMIZE_MIN':           0.5,
                                 }}


### TRAINING
dict_parameter_sport, df_a_list = optimisation_8(df_train, df_test, dict_training_option)
dict_parameter_save.update({dict_parameter_sport.keys()[0]:dict_parameter_sport[dict_parameter_sport.keys()[0]]})
dict_parameter_save['option'].update(dict_training_option)


### SAVE
with open('../model/local/dict_parameter.json', 'w') as outfile:
    json.dump(dict_parameter_save, outfile, sort_keys = True, indent = 4,)

    
"""
df = optimisation_7_apply(df_test, dict_parameter)
dict_parameter_sport = dict_parameter
"""


ee
# =============================================================================
# esports
# =============================================================================
### LOAD DATA
#df_ALL = pd.DataFrame.from_csv('../dataset/local/df_ALL.xls', encoding='utf-8')
df_ALL = pd.DataFrame.from_csv('../dataset/local/esports/df_ALL_esports.xls', encoding='utf-8')
#df_ALL = df_merge_single.copy()

df_esports = df_ALL[df_ALL.sport == 'esports']

#df_esports = df_esports[df_esports.ligue == 'NHL']
    
df_esports['sport']       = 'e sports'
df_esports['bet_diff']    = df_esports.bet_1-df_esports.bet_2
df_esports['min_bet']     = 0
df_esports['prediction']  = 0
df_esports['prediction']  = 0
df_esports['good_pred']   = 0
df_esports['bad_pred']    = 0
df_esports['winner']      = df_esports['result']  
df_esports['min_bet']     = df_esports[['bet_1','bet_2']].min(axis=1)
df_esports['prediction']  = df_esports.bet_diff.apply(lambda x : "1" if x<0 else "2")
df_esports['bet_diff']    = abs(df_esports['bet_diff'])

df_esports = df_esports[['match_date', 'sport', 'ligue','bet_1', 'bet_2', 'bet_X', 'bet_diff', 'min_bet', 'winner', 'prediction', 'team_home', 'good_pred', 'bad_pred']]

df_esports.winner[df_esports.winner == 'X'] = 0
df_esports.winner[df_esports.winner == '1'] = 1
df_esports.winner[df_esports.winner == '2'] = 2

df_esports.winner = df_esports.winner.astype(int)
df_esports.prediction = df_esports.prediction.astype(int)
df_esports['good_pred'] = 0
df_esports.good_pred[df_esports.winner == df_esports.prediction] = 1    
df_esports.bad_pred[df_esports.good_pred != 1] = 1

df_esports.match_date = df_esports.match_date.apply(lambda x : datetime.fromtimestamp(x))#.strftime('%Y-%m-%d %H:%M:%S'))

df_test  = df_esports[df_esports.match_date > datetime(2017, 8, 8, 0, 46, 43, 100000)]
df_train = df_esports[df_esports.match_date < datetime(2018, 8, 8, 0, 46, 43, 100000)]


### OPTIONS
dict_training_option = {'e sports':{
                                'mod_value':       0.1,
                                'limit_bet':       0,
                                'limit_DC':        0.01,
                                'limit_perf_min':  0,
                                'force_mode':      '',
                                 }}

### TRAINING
dict_parameter_sport, df_parameter_esports = optimisation_7(df_train, dict_training_option)
dict_parameter.update({dict_parameter_sport.keys()[0]:dict_parameter_sport[dict_parameter_sport.keys()[0]]})
dict_parameter['option'].update(dict_training_option)
        
### SAVE
with open('../model/local/dict_parameter_sport.json', 'w') as outfile:
    json.dump(dict_parameter, outfile)
    
ee
# =============================================================================
# hockey
# =============================================================================
### LOAD DATA
#df_ALL = pd.DataFrame.from_csv('../dataset/local/df_ALL.xls', encoding='utf-8')
df_ALL = pd.DataFrame.from_csv('../dataset/local/hockey/df_ALL_hockey.xls', encoding='utf-8')
#df_ALL = df_merge_single.copy()

df_hockey = df_ALL[df_ALL.sport == 'hockey']

#df_hockey = df_merge_single[df_merge_single.sport == 'hockey']
    
df_hockey['sport']       = 'hockey'
df_hockey['bet_diff']    = df_hockey.bet_1-df_hockey.bet_2
df_hockey['min_bet']     = 0
df_hockey['prediction']  = 0
df_hockey['prediction']  = 0
df_hockey['good_pred']   = 0
df_hockey['bad_pred']    = 0
try:
    df_hockey['winner']      = df_hockey['result']  
except:
    pass
df_hockey['min_bet']     = df_hockey[['bet_1','bet_2']].min(axis=1)
df_hockey['prediction']  = df_hockey.bet_diff.apply(lambda x : "1" if x<0 else "2")
df_hockey['bet_diff']    = abs(df_hockey['bet_diff'])

df_hockey = df_hockey[['match_date', 'sport', 'ligue','bet_1', 'bet_2', 'bet_X', 'bet_diff', 'min_bet', 'winner', 'prediction', 'team_home', 'good_pred', 'bad_pred']]

df_hockey.winner[df_hockey.winner == 'X'] = 0
df_hockey.winner[df_hockey.winner == '1'] = 1
df_hockey.winner[df_hockey.winner == '2'] = 2

df_hockey.winner = df_hockey.winner.astype(int)
df_hockey.prediction = df_hockey.prediction.astype(int)
df_hockey['good_pred'] = 0
df_hockey.good_pred[df_hockey.winner == df_hockey.prediction] = 1    
df_hockey.bad_pred[df_hockey.good_pred != 1] = 1

df_hockey.match_date = df_hockey.match_date.apply(lambda x : datetime.fromtimestamp(x))#.strftime('%Y-%m-%d %H:%M:%S'))

df_test  = df_hockey[df_hockey.match_date > datetime(2018, 12, 30, 0, 46, 43, 100000)]
df_train = df_hockey[df_hockey.match_date < datetime(2018, 12, 30, 0, 46, 43, 100000)]


### OPTIONS
dict_training_option = {'hockey':{
                                'mod_value':       0.1,
                                'limit_bet':       1.80,
                                'limit_DC':        0.02,
                                'limit_perf_min':  0,
                                'force_mode':      '',
                                 }}

### TRAINING
dict_parameter_sport, df_parameter_hockey = optimisation_7(df_train, dict_training_option)
dict_parameter.update({dict_parameter_sport.keys()[0]:dict_parameter_sport[dict_parameter_sport.keys()[0]]})
dict_parameter['option'].update(dict_training_option)
        
### SAVE
with open('../model/local/dict_parameter_sport.json', 'w') as outfile:
    json.dump(dict_parameter, outfile)
    
"""
df = optimisation_7_apply(df_test, dict_parameter)
"""

ee

# =============================================================================
# handball
# =============================================================================
### LOAD DATA
df_ALL = pd.DataFrame.from_csv('../dataset/local/df_ALL.xls', encoding='utf-8')
df_ALL = pd.DataFrame.from_csv('../dataset/local/handball/df_ALL_handball.xls', encoding='utf-8')

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

df_test  = df_handball[df_handball.match_date > datetime(2018, 8, 8, 0, 46, 43, 100000)]
df_train = df_handball[df_handball.match_date < datetime(2018, 8, 8, 0, 46, 43, 100000)]


### OPTIONS
dict_training_option = {'handball':{
                                'mod_value':       0.1,
                                'limit_bet':       1.,
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
    
ee
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
#df_ALL = pd.DataFrame.from_csv('../dataset/local/df_ALL.xls', encoding='utf-8')
df_ALL = pd.DataFrame.from_csv('../dataset/local/volleyball/df_ALL_volleyball.xls', encoding='utf-8')

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
                                'limit_bet':       2.00,
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
#df_ALL = pd.DataFrame.from_csv('../dataset/local/df_ALL.xls', encoding='utf-8')
df_ALL = pd.DataFrame.from_csv('../dataset/local/tennis/df_ALL_tennis.xls', encoding='utf-8')


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