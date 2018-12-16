#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 17:25:19 2018

@author: mathieu
"""

# =============================================================================
# IMPORT PACKAGES
# =============================================================================
import os
import datetime

import pandas             as pd

from datetime                                                                  import datetime
from datetime                                                                  import timedelta

from PS3838_scrap_function                                                     import ps3838_scrap_parlay, ps3838_scrap_single, ps3838_scrap_result
from PS3838_support_function                                                   import encode_decode, optimisation, optimisation_2, optimisation_3, optimisation_apply
from PS3838_bet_function                                                       import ps3838_bet_simulator, ps3838_bet_parlay, ps3838_bet_single
from PS3838_dashboard                                                          import dashboard


# =============================================================================
# 
# =============================================================================
os.system('mkdir -p ../dataset/local')
os.system('mkdir -p ../model/local')

# =============================================================================
# SCRAP
# =============================================================================
ps3838_scrap_parlay()
GMT_to_add = ps3838_scrap_single()
ps3838_scrap_result(GMT_to_add)


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
df_merge_parlay                           = pd.merge(df_parlay, df_result, how='inner', on=['match_date','sport','team_home'])
df_merge_parlay = df_merge_parlay[['match_date','sport','ligue','bet_1','bet_2','bet_X','bet_diff','min_bet','winner','prediction','score']]
df_merge_parlay['good_pred']              = 0
df_merge_parlay.good_pred[df_merge_parlay.prediction == df_merge_parlay.winner] = 1
df_merge_parlay['bad_pred']               = 0
df_merge_parlay.bad_pred[df_merge_parlay.prediction != df_merge_parlay.winner]  = 1
df_merge_parlay.match_date                = df_merge_parlay.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

###
df_merge_single                           = pd.merge(df_single, df_result_single, how='inner', on=['match_date','sport','team_home'])
df_merge_single = df_merge_single[['match_date','sport','ligue','bet_1','bet_2','bet_X','bet_diff','min_bet','winner','prediction']]
df_merge_single['good_pred']              = 0
df_merge_single.good_pred[df_merge_single.prediction == df_merge_single.winner] = 1
df_merge_single['bad_pred']               = 0
df_merge_single.bad_pred[df_merge_single.prediction != df_merge_single.winner]  = 1
df_merge_single.match_date                = df_merge_single.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

draw_activated = 0
dict_parameter_sport = ps3838_bet_single(df_single, df_merge_single, draw_activated)
dashboard(dict_parameter_sport)

"""
# =============================================================================
# Ajust bet parameter
# =============================================================================
df_temp = 0
list_sport = df_merge.sport.unique().tolist()
dict_parameter_sport = {}
for item in list_sport:
    print '\n' + item
    exec('df_merge_' + item.replace(' ','_') + ' = df_merge[df_merge.sport == "' + item + '"]')
    exec('df_temp = df_merge_' + item.replace(' ','_'))
    dict_temp = optimisation_3(df_temp)
    dict_parameter_sport.update(dict_temp)
df_parlay_filter = optimisation_apply(df_parlay, dict_parameter_sport)
df_parlay_filter = df_parlay_filter[(df_parlay_filter.match_date < datetime.now()+timedelta(hours=20)) & (df_parlay_filter.match_date > datetime.now())]
df_parlay_filter.drop_duplicates(subset=['match_date','team_home'], inplace=True)


# =============================================================================
# Ajust bet parameter SINGLE
# =============================================================================
df_temp = 0
list_sport = df_merge_single.sport.unique().tolist()
dict_parameter_sport_single = {}
for item in list_sport:
    print '\n' + item
    exec('df_merge_single_' + item.replace(' ','_') + ' = df_merge_single[df_merge_single.sport == "' + item + '"]')
    exec('df_temp = df_merge_single_' + item.replace(' ','_'))
    dict_temp = optimisation_3(df_temp)
    dict_parameter_sport_single.update(dict_temp)
df_single_filter = optimisation_apply(df_single, dict_parameter_sport_single)
df_single_filter = df_single_filter[(df_single_filter.match_date < datetime.now()+timedelta(hours=1)) & (df_single_filter.match_date > datetime.now())]
df_single_filter.drop_duplicates(subset=['match_date','team_home'], inplace=True)


# =============================================================================
# Print opportunity
# =============================================================================
print '*****************************'
print str(datetime.now())
df_parlay_filter.sort_values('bet_diff', ascending=False, inplace=True)
print 'df_parlay_filter : ', len(df_parlay_filter)
print '*****************************'

# =============================================================================
# Print opportunity SINGLE
# =============================================================================
print '*****************************'
print str(datetime.now())
df_single_filter.sort_values('bet_diff', ascending=False, inplace=True)
print 'df_single_filter : ', len(df_single_filter)
print '*****************************'


# =============================================================================
# Prepare bet
# =============================================================================
df_betting_parlay_done = pd.DataFrame()
list_bet_parlay_done             = glob('../dataset/local/Real_df_betting_parlay*.xls')
for i, bet_parlay_done in enumerate(list_bet_parlay_done):
    df_betting_parlay_done_temp = pd.DataFrame.from_csv(bet_parlay_done, encoding='utf-8')
    df_betting_parlay_done_temp['bet_num'] = i 
    df_betting_parlay_done = pd.concat((df_betting_parlay_done, df_betting_parlay_done_temp))
try:
    list_already_bet_parlay = df_betting_parlay_done.team_to_bet_id.unique().tolist()
except:
    list_already_bet_parlay = []
    
df_parlay_filter['team_to_bet']     = df_parlay_filter['team_home']
df_parlay_filter['team_to_bet_id']  = df_parlay_filter['team_home_id']
df_parlay_filter['team_to_bet'][df_parlay_filter.bet_1 > df_parlay_filter.bet_2] = df_parlay_filter['team_away'][df_parlay_filter.bet_1 > df_parlay_filter.bet_2]
df_parlay_filter['team_to_bet_id'][df_parlay_filter.bet_1 > df_parlay_filter.bet_2] = df_parlay_filter['team_away_id'][df_parlay_filter.bet_1 > df_parlay_filter.bet_2]
df_parlay_filter.reset_index(drop=False, inplace = True)
df_parlay_filter.sort_values('match_date', ascending=True, inplace=True)
#df_parlay_filter.sort_values('min_bet', ascending=True, inplace=True)
#df_parlay_filter.sort_values('min_bet', ascending=False, inplace=True)

number_bet  = 10
df_parlay_filter = df_parlay_filter[~(df_parlay_filter.team_to_bet_id.isin(list_already_bet_parlay))]
df_betting = df_parlay_filter[['match_date','sport','ligue','index','team_to_bet','min_bet','bet_diff','team_to_bet_id','team_home']]
df_betting = df_betting.iloc[0:number_bet]

print '*****************************'
print 'df_betting parlay : ', len(df_betting)
for i in range(len(df_betting)):
    if i == 0:
        bet_parlay = df_betting.min_bet.iloc[i]
    if i > 0:
        bet_parlay = bet_parlay*df_betting.min_bet.iloc[i]
print 'bet_parlay : ', bet_parlay
print '*****************************'

# =============================================================================
# Prepare bet SINGLE
# =============================================================================
df_betting_single_done = pd.DataFrame()
list_bet_single_done             = glob('../dataset/local/Real_df_betting_single*.xls')
for i, bet_single_done in enumerate(list_bet_single_done):
    df_betting_single_done_temp = pd.DataFrame.from_csv(bet_single_done, encoding='utf-8')
    df_betting_single_done_temp['bet_num'] = i 
    df_betting_single_done = pd.concat((df_betting_single_done, df_betting_single_done_temp))
try:
    list_already_bet_single = df_betting_single_done.team_to_bet_id.unique().tolist()
except:
    list_already_bet_single = []

df_single_filter['team_to_bet']     = df_single_filter['team_home']
df_single_filter['team_to_bet_id']  = df_single_filter['team_home_id']
df_single_filter['team_to_bet'][df_single_filter.bet_1 > df_single_filter.bet_2] = df_single_filter['team_away'][df_single_filter.bet_1 > df_single_filter.bet_2]
df_single_filter['team_to_bet_id'][df_single_filter.bet_1 > df_single_filter.bet_2] = df_single_filter['team_away_id'][df_single_filter.bet_1 > df_single_filter.bet_2]
df_single_filter.reset_index(drop=False, inplace = True)
df_single_filter.sort_values('match_date', ascending=True, inplace=True)
#df_single_filter.sort_values('min_bet', ascending=True, inplace=True)
#df_single_filter.sort_values('min_bet', ascending=False, inplace=True)

number_bet  = 10
df_single_filter = df_single_filter[~(df_single_filter.team_to_bet_id.isin(list_already_bet_single))]
df_betting_single = df_single_filter[['match_date','sport','ligue','index','team_to_bet','min_bet','bet_diff','team_to_bet_id','team_home']]
df_betting_single = df_betting_single.iloc[0:number_bet]

print '*****************************'
print 'df_betting single : ', len(df_betting_single)
for i in range(len(df_betting_single)):
    if i == 0:
        bet_single = df_betting_single.min_bet.iloc[i]
    if i > 0:
        bet_single = bet_single*df_betting_single.min_bet.iloc[i]
print 'bet_single : ', bet_single
print '*****************************'


# =============================================================================
# Place bet
# =============================================================================
df_bet, df_bet_result = ps3838_bet_simulator(df_single_filter, df_parlay_filter, df_result)


#df_bet_result[df_bet_result.good_pred == 1].min_bet.mean()
#df_bet.sort_values('match_date', inplace=True)
#plt.plot(df_bet['match_date'], df_bet['min_bet'])
#plt.xticks(rotation='vertical')

"""
