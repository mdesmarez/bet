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

from PS3838_support_function                                                   import optimisation_7, optimisation_7_apply


# =============================================================================
# 
# =============================================================================
dict_parameter = {'option':{}}



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

df_test  = df_soccer[df_soccer.match_date > datetime(2019, 8, 8, 0, 46, 43, 100000)]
df_train = df_soccer[df_soccer.match_date < datetime(2019, 8, 8, 0, 46, 43, 100000)]


### OPTIONS
dict_training_option = {'soccer':{
                                'mod_value':       0.1,
                                'limit_bet':       2,
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
                                'mod_value':       0.05,
                                'limit_bet':       1.,
                                'limit_DC':        0.04,
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
                                'mod_value':       0.05,
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

df_test  = df_volleyball[df_volleyball.match_date > datetime(2018, 8, 8, 0, 46, 43, 100000)]
df_train = df_volleyball[df_volleyball.match_date < datetime(2018, 8, 8, 0, 46, 43, 100000)]


### OPTIONS
dict_training_option = {'volleyball':{
                                'mod_value':       0.05,
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