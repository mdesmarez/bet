#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 11:41:56 2018

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

import matplotlib.pyplot  as plt
import pandas             as pd
import numpy              as np

from bs4                  import BeautifulSoup
from glob                                                                      import glob
from datetime                                                                  import datetime
from datetime                                                                  import timedelta

from PS3838_scrap_function                                                     import ps3838_scrap_parlay, ps3838_scrap_single, ps3838_scrap_result
from PS3838_support_function                                                   import encode_decode, optimisation, optimisation_2, optimisation_3, optimisation_apply, match_filter_prediction
from PS3838_bet_function                                                       import ps3838_bet_simulator, ps3838_bet_parlay


# =============================================================================
# 
# =============================================================================
"""

os.system('wget http://35.195.3.155:8080/bet/prod/bet/dataset/local/df_parlay.xls')
os.system('mv df_parlay.xls df_parlay_server.xls')
os.system('mv df_parlay_server.xls ../dataset/local/df_parlay_server.xls')

os.system('wget http://35.195.3.155:8080/bet/prod/bet/dataset/local/df_single.xls')
os.system('mv df_single.xls df_single_server.xls')
os.system('mv df_single_server.xls ../dataset/local/df_single_server.xls')

os.system('wget http://35.195.3.155:8080/bet/prod/bet/dataset/local/df_result.xls')
os.system('mv df_result.xls df_result_server.xls')
os.system('mv df_result_server.xls ../dataset/local/df_result_server.xls')

os.system('wget http://35.195.3.155:8080/bet/prod/bet/dataset/local/df_real_betting_single.xls')
os.system('mv df_real_betting_single.xls df_real_betting_single_serveur.xls')
os.system('mv df_real_betting_single_serveur.xls ../dataset/local/df_real_betting_single_serveur.xls')


df_single_server = pd.DataFrame.from_csv('../dataset/local/df_single_server.xls', encoding='utf-8')
df_parlay_server = pd.DataFrame.from_csv('../dataset/local/df_parlay_server.xls', encoding='utf-8')
df_result_server = pd.DataFrame.from_csv('../dataset/local/df_result_server.xls', encoding='utf-8')
df_real_betting_single_serveur = pd.DataFrame.from_csv('../dataset/local/df_real_betting_single_serveur.xls', encoding='utf-8')

df_single = pd.DataFrame.from_csv('../dataset/local/df_single.xls', encoding='utf-8')
df_parlay = pd.DataFrame.from_csv('../dataset/local/df_parlay.xls', encoding='utf-8')
df_result = pd.DataFrame.from_csv('../dataset/local/df_result.xls', encoding='utf-8')
df_real_betting_single = pd.DataFrame.from_csv('../dataset/local/df_real_betting_single.xls', encoding='utf-8')

"""
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
# Prepare bet SINGLE
# =============================================================================
#df_betting_single_done = pd.DataFrame()
#list_bet_single_done             = glob('../dataset/local/Real_df_betting_single*.xls')
#for i, bet_single_done in enumerate(list_bet_single_done):
#    df_betting_single_done_temp = pd.DataFrame.from_csv(bet_single_done, encoding='utf-8')
#    df_betting_single_done_temp['bet_num'] = i 
#    df_betting_single_done = pd.concat((df_betting_single_done, df_betting_single_done_temp))

df_betting_single_done = pd.DataFrame.from_csv('../dataset/local/df_real_betting_single.xls', encoding='utf-8')

try:
    list_already_bet_single = df_betting_single_done.team_to_bet_id.unique().tolist()
except:
    list_already_bet_single = []
    
df_betting_single_done['prediction'] = 2
df_betting_single_done.prediction[df_betting_single_done.team_to_bet == df_betting_single_done.team_home] = 1

df_merge_single_bet = pd.merge(df_betting_single_done, df_result_single, how='inner', on=['match_date','sport','team_home'])
df_merge_single_bet = df_merge_single_bet[['match_date','sport','ligue','bet_diff','min_bet','winner','prediction','team_home','bet_X']]
df_merge_single_bet['good_pred']                          = 0
df_merge_single_bet.good_pred[df_merge_single_bet.prediction == df_merge_single_bet.winner] = 1
df_merge_single_bet['bad_pred']                           = 0
df_merge_single_bet.bad_pred[df_merge_single_bet.prediction != df_merge_single_bet.winner]  = 1
df_merge_single_bet.match_date                = df_merge_single_bet.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))





df_merge_single_bet = df_merge_single_bet[df_merge_single_bet.sport == 'soccer']




# =============================================================================
#  1 bet
# =============================================================================    
print('1 BY 1')
result  = 0
cave    = 0
mise    = 5
draw_activated              = 1


num_good_pred   = 0
num_bad_pred    = 0
    
for item in range(len(df_merge_single_bet)):
    if (df_merge_single_bet.min_bet.iloc[item] < 1.1) and (draw_activated == 1):
        pass
    else:
        if draw_activated == 1:
            cave = cave + mise*2
        else:
            cave = cave + mise
    
        if draw_activated == 1:
            result = result - mise*2
        else:
            result = result - mise
            
        if df_merge_single_bet.good_pred.iloc[item] == 1:
            result = result+(df_merge_single_bet.min_bet.iloc[item])*mise
        if draw_activated == 1 and df_merge_single_bet.winner.iloc[item] == 0:
            result = result+(df_merge_single_bet.bet_X.iloc[item])*mise
            df_merge_single_bet['good_pred'].iloc[item]  = 1
            df_merge_single_bet['bad_pred'].iloc[item]   = 0
        if (df_merge_single_bet.good_pred.iloc[item] == 1) or (draw_activated == 1 and df_merge_single_bet.winner.iloc[item] == 0):
            num_good_pred = num_good_pred + 1
        else:
            num_bad_pred = num_bad_pred + 1
                

print('******** RESULT SIMULATION **********')
print 'Number bet engaged : ', len(df_betting_single_done)
print 'Cave engaged       : ', (len(df_betting_single_done)-len(df_merge_single_bet))*mise*2
print 'Bet engaged        : ', (len(df_betting_single_done)-len(df_merge_single_bet))
print 'Number Good pred   : ', num_good_pred
print 'Number Bad pred    : ', num_bad_pred
print '% : ', round(num_good_pred/float(num_good_pred+num_bad_pred)*100,2), '%'
print ''
print 'cave     : ', int(cave),' €'
print 'gain pur : ', round(result,2),' €'
print 'ROI cave : ', round(result/float(cave)*100,2), '%'
print round(result/mise,2)*100,"%"
print('*************************************')
print ''



#dict_bankroll = {}
#for i in range(5):
#    print('******************************************')
#    last_X_days = 1*i
#    print last_X_days, ' jours'
#    df_merge_single_bet_result = df_merge_single_bet[(df_merge_single_bet.match_date > datetime.now()-timedelta(hours=24*last_X_days))]
#
#    # =============================================================================
#    #  1 bet
#    # =============================================================================    
#    print('1 BY 1')
#    result  = 0
#    cave    = 0
#    for item in range(len(df_merge_single_bet_result)):
#        cave = cave + mise
#        if df_merge_single_bet_result.good_pred.iloc[item] == 1:
#            result = result+(df_merge_single_bet_result.min_bet.iloc[item]-1)*mise
#        else:
#            result = result - mise
#    print 'cave     : ', int(cave),' €'
#    print 'gain pur : ', round(result,2),' €'
#    print round(result/mise,2)*100,"%"
#    print ''
#    dict_bankroll.update({last_X_days:[result]})
#    
#
#df_dict_result = pd.DataFrame.from_dict(dict_bankroll, orient='index')
#df_dict_result.sort_index(inplace=True)
#df_dict_result.plot()




eee

#%%

last_X_days = 1
    
###
df_merge_train = df_merge[(df_merge.match_date < datetime.now()-timedelta(hours=24*last_X_days))]
###
#df_merge_train = df_merge_single[(df_merge_single.match_date < datetime.now()-timedelta(hours=24*last_X_days))]

df_merge_train['sport'] = df_merge_train['sport'].apply(lambda x : x.lower()) 

# =============================================================================
# Ajust bet parameter
# =============================================================================
df_temp = 0
list_sport = df_merge_train.sport.unique().tolist()
dict_parameter_sport = {}

#list_sport = ['volleyball']
#list_sport = ['soccer']
#list_sport = ['handball']


###
df = df_merge[(df_merge.match_date >= datetime.now()-timedelta(hours=24*last_X_days))]
###
df = df_merge_single[(df_merge_single.match_date >= datetime.now()-timedelta(hours=24*last_X_days))]

list_sport = df.sport.unique().tolist()
df_parlay_filter = pd.DataFrame()

for item in list_sport:
    print '\n' + item
    exec('df_merge_' + item.replace(' ','_') + ' = df_merge_train[df_merge_train.sport == "' + item + '"]')
    exec('df_temp = df_merge_' + item.replace(' ','_'))
    dict_temp = optimisation_3(df_temp)
    dict_parameter_sport.update(dict_temp)
    
#    if item == 'basketball':
#        ee
        
    try:
        bet_min      = dict_parameter_sport[item]['bet_min']
        bet_max      = dict_parameter_sport[item]['bet_max']
        bet_ecart    = dict_parameter_sport[item]['bet_ecart']
        num_total    = dict_parameter_sport[item]['num_total']
        max_bankroll = dict_parameter_sport[item]['max_bankroll']
    
        if num_total > 50:# and max_bankroll >= 2:
            df_sport    = df[df.sport == item]
            df_sport    = match_filter_prediction(df_sport, bet_max, bet_min, bet_ecart)
            df_parlay_filter = pd.concat((df_parlay_filter, df_sport))
        else:
            print 'too less data for ',item
        
    except:
        print 'no', item

#df_parlay_filter = df_parlay_filter[(df_parlay_filter.match_date >= datetime.now()-timedelta(hours=24*3))]
            
#df_parlay_filter.drop_duplicates(subset=['match_date','team_home'], inplace=True)

print('******** RESULT SIMULATION **********')
print 'Number Good pred : ', len(df_parlay_filter)
print 'Number Bad pred  : ', len(df_parlay_filter[df_parlay_filter.good_pred == 0])
print round(df_parlay_filter.good_pred.sum()/float(len(df_parlay_filter))*100,2), '%'
print('*************************************')

mise = 5
print('1 BY 1')
result = 0
cave = 0
for item in range(len(df_parlay_filter)):
    cave = cave + mise
    if df_parlay_filter.good_pred.iloc[item] == 1:
        result = result+(df_parlay_filter.min_bet.iloc[item]+0.0-1)*mise
    else:
#        print 'lose'
        result = result - mise
print 'cave     : ', int(cave),' €'
print 'gain pur : ', int(result),' €'
print 'ROI cave : ', round(result/float(cave)*100,2), '%'
print 'ROI mise : ',round(result/mise,2)*100,"%"
print ''
    
df_parlay_filter[df_parlay_filter.good_pred == 1].min_bet.mean()



#%%

from PS3838_support_function  import optimisation_6, optimisation_6_apply, optimisation_5, optimisation_5_apply

mise                        = 5
draw_activated              = 1

mod_value                   = 0.1
day_train                   = 1
day_shift                   = 0

total_result                = 0
total_cave                  = 0

list_day_shift              = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#list_day_shift              = [0, 1, 2, 3]#, 4, 5, 6, 7, 8, 9, 10]

list_day_shift.sort(reverse=True)
dict_bankroll               = {}
dict_parameter_sport_single = {}

for day_shift in list_day_shift:
    result     = 0
    cave       = 0.1
        
    date_min = datetime.now()-timedelta(hours=24*day_shift) - timedelta(hours=24*day_train)
    date_max = datetime.now()-timedelta(hours=24*day_shift)
    
    hour_test = 01
    date_min = date_min.replace(hour=hour_test, minute=00, second=00)
    date_max = date_max.replace(hour=hour_test, minute=00, second=00)
    
    df_train    = df_merge_single[(df_merge_single.match_date < date_min)]
    df_test     = df_merge_single[(df_merge_single.match_date >= date_min) & (df_merge_single.match_date <= date_max)]
    
#    df_test = df_test[df_test.sport == 'soccer']

    
    print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
    print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
    print date_min.strftime('%d, %B %Y - %a'), ' / ', date_max.strftime('%d, %B %Y - %a')
    
    dict_parameter_sport = optimisation_6(df_train, mod_value)
    df_single_filter = optimisation_6_apply(df_test, dict_parameter_sport, mod_value)

#    dict_parameter_sport         = optimisation_6(df_merge_single, mod_value)


    num_good_pred   = 0
    num_bad_pred    = 0
    
    
    for item in range(len(df_single_filter)):
        if (df_single_filter.min_bet.iloc[item] > 1.):
            if df_single_filter.mode_bet.iloc[item] == 'X':
                cave = cave + mise*2
                result = result - mise*2
                if df_single_filter.good_pred.iloc[item] == 1:
                    result = result + df_single_filter.min_bet.iloc[item]*mise
                    num_good_pred = num_good_pred + 1
                if df_single_filter.winner.iloc[item] == 0:
                    result = result + df_single_filter.bet_X.iloc[item]*mise
                    num_good_pred = num_good_pred + 1
                if df_single_filter.good_pred.iloc[item] == 0 and df_single_filter.winner.iloc[item] != 0:
                    num_bad_pred = num_bad_pred + 1
    
    
            if df_single_filter.mode_bet.iloc[item] == 'S':
                cave = cave + mise
                result = result - mise
                if df_single_filter.good_pred.iloc[item] == 1:
                    result = result + df_single_filter.min_bet.iloc[item]*mise
                    num_good_pred = num_good_pred + 1
                else:
                    num_bad_pred = num_bad_pred + 1

        
        """
        if (df_single_filter.min_bet.iloc[item] < 1.1) and (draw_activated == 1):
            print df_single_filter.min_bet.iloc[item]
        else:
            
            if draw_activated == 1:
                cave = cave + mise*2
            else:
                cave = cave + mise
        
            if draw_activated == 1:
                result = result - mise*2
            else:
                result = result - mise
                
            if df_single_filter.good_pred.iloc[item] == 1:
                result = result+(df_single_filter.min_bet.iloc[item])*mise
            if draw_activated == 1 and df_single_filter.winner.iloc[item] == 0:
                result = result+(df_single_filter.bet_X.iloc[item])*mise
    
            if (df_single_filter.good_pred.iloc[item] == 1) or (draw_activated == 1 and df_single_filter.winner.iloc[item] == 0):
                num_good_pred = num_good_pred + 1
            else:
                num_bad_pred = num_bad_pred + 1
        """        
    
    if len(df_single_filter) != 0:
        print('******** RESULT SIMULATION **********')
        print 'Number Good pred : ', num_good_pred
        print 'Number Bad pred  : ', num_bad_pred
        print '% : ', round(num_good_pred/float(num_good_pred+num_bad_pred+0.01)*100,2), '%'
        print 'Mean bet : ', df_single_filter.min_bet.mean()
        print 'cave     : ', int(cave),' €'
        print 'gain pur : ', int(result),' €'
        print 'ROI cave : ', round(result/float(cave)*100,2), '%'
        print 'ROI mise : ',round(result/mise,2)*100,"%"
        print('*************************************')
            
    total_result = total_result + result
    total_cave   = total_cave + cave   
    
    print total_result
    print total_cave
    print 'ROI cave : ', round(total_result/float(total_cave)*100,2), '%'
    print ''
    
    date_text = (datetime.now()-timedelta(hours=24*day_shift))
    dict_bankroll.update({date_text.strftime("%d %m - %a"):{'total':total_result}})


df_dict_result = pd.DataFrame.from_dict(dict_bankroll, orient='index')
df_dict_result.sort_index(inplace=True)
df_dict_result.plot()
        
 
    
    
    
    

