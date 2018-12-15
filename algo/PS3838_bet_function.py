#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 18:04:48 2018

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
import warnings
    
import matplotlib.pyplot  as plt
import pandas             as pd
import numpy              as np

from bs4                  import BeautifulSoup
from glob                                                                      import glob
from datetime                                                                  import datetime
from datetime                                                                  import timedelta

from PS3838_support_function                                                   import encode_decode, optimisation, optimisation_2, optimisation_3, optimisation_apply, match_filter_prediction, optimisation_5, optimisation_5_apply


# =============================================================================
# 
# =============================================================================
def ps3838_bet_simulator(df_single_filter, df_parlay_filter, df_result):
    warnings.filterwarnings('ignore')
    def ps3838_bet_simulator_result(df_bet_result_visu, name):
        print(name)
        result = 0
        cave = 0
        list_bet_id = df_bet_result_visu.bet_num.unique().tolist()
        for id in list_bet_id:
            bet_parlay = 1
            cave = cave + mise
            df_bet_result_visu_id = df_bet_result_visu[df_bet_result_visu.bet_num == id]
            if df_bet_result_visu_id.good_pred.sum() == len(df_bet_result_visu_id):
                for item in range(len(df_bet_result_visu_id)):
                    bet_parlay = bet_parlay*df_bet_result_visu_id.min_bet.iloc[item]
        #            print bet_parlay, (bet_parlay-1)*mise
                result = result  + (bet_parlay-1)*mise
            else:
#                print 'lose'
                result = result - mise
        print 'cave     : ', int(cave),' €'
        print 'gain pur : ', int(result),' €'
        #print 'ROI cave : ', round(result/float(cave)*100,2), '%'
        print round(result/mise,2)*100,"%"
        print ''
        
    mise = 10


    # =============================================================================
    #  SINGLE
    # =============================================================================
    df_bet_single = pd.DataFrame()
    list_bet_single             = glob('../dataset/local/df_betting_simulatorsingle_*.xls')
    for i, bet_single in enumerate(list_bet_single):
        df_bet_temp_single = pd.DataFrame.from_csv(bet_single, encoding='utf-8')
        df_bet_temp_single['bet_num'] = i 
        df_bet_single = pd.concat((df_bet_single, df_bet_temp_single))
    try:
        list_already_bet_single = df_bet_single.team_to_bet_id.unique().tolist()
    except:
        list_already_bet_single = []
        
    number_bet  = 1
    df_parlay_filter_simulator_single = df_single_filter[~(df_single_filter.team_to_bet_id.isin(list_already_bet_single))]
    
    if len(df_parlay_filter_simulator_single)>=1:
        print 'OK TO SIMULATOR SINGLE'
        df_betting_simulator_single = df_parlay_filter_simulator_single[['match_date','sport','ligue','index','team_to_bet','min_bet','bet_diff','team_to_bet_id','team_home']]
        df_betting_simulator_single = df_betting_simulator_single.iloc[0:number_bet]
        date_bet = datetime.now()
        date_bet_string = str(date_bet.hour).zfill(2) + ':' + str(date_bet.minute).zfill(2) + '_' + str(date_bet.day) + '_' + str(date_bet.month) + '_' + str(date_bet.year)
        df_betting_simulator_single.to_csv('../dataset/local/df_betting_simulatorsingle_' + date_bet_string + '.xls', encoding='utf-8')
    else:
        print 'SIMULATOR SINGLE - ', len(df_parlay_filter_simulator_single)
    
    df_bet_result_single = pd.merge(df_bet_single, df_result, how='inner', on=['match_date','sport','team_home'])
    df_bet_result_single['prediction'] = 2
    df_bet_result_single['prediction'][df_bet_result_single.team_home == df_bet_result_single.team_to_bet] = 1
    df_bet_result_single['good_pred']  = 0
    df_bet_result_single['good_pred'][df_bet_result_single['prediction'] == df_bet_result_single['winner']] = 1
    
    ps3838_bet_simulator_result(df_bet_result_single, 'Single')
    

    # =============================================================================
    #  2 bets
    # =============================================================================
    df_bet_2 = pd.DataFrame()
    list_bet_2             = glob('../dataset/local/df_betting_simulator2_*.xls')
    for i, bet_2 in enumerate(list_bet_2):
        df_bet_temp_2 = pd.DataFrame.from_csv(bet_2, encoding='utf-8')
        df_bet_temp_2['bet_num'] = i 
        df_bet_2 = pd.concat((df_bet_2, df_bet_temp_2))
    try:
        list_already_bet_2 = df_bet_2.team_to_bet_id.unique().tolist()
    except:
        list_already_bet_2 = []
        
    number_bet  = 2
    df_parlay_filter_simulator_2 = df_parlay_filter[~(df_parlay_filter.team_to_bet_id.isin(list_already_bet_2))]
    
    if len(df_parlay_filter_simulator_2)>=number_bet:
        print 'OK TO SIMULATOR 2'
        df_betting_simulator_2 = df_parlay_filter_simulator_2[['match_date','sport','ligue','index','team_to_bet','min_bet','bet_diff','team_to_bet_id','team_home']]
        df_betting_simulator_2 = df_betting_simulator_2.iloc[0:number_bet]
        date_bet = datetime.now()
        date_bet_string = str(date_bet.hour).zfill(2) + ':' + str(date_bet.minute).zfill(2) + '_' + str(date_bet.day) + '_' + str(date_bet.month) + '_' + str(date_bet.year)
        df_betting_simulator_2.to_csv('../dataset/local/df_betting_simulator2_' + date_bet_string + '.xls', encoding='utf-8')
    else:
        print 'SIMULATOR 2 - ', len(df_parlay_filter_simulator_2)
    
    df_bet_result_2 = pd.merge(df_bet_2, df_result, how='inner', on=['match_date','sport','team_home'])
    df_bet_result_2['prediction'] = 2
    df_bet_result_2['prediction'][df_bet_result_2.team_home == df_bet_result_2.team_to_bet] = 1
    df_bet_result_2['good_pred']  = 0
    df_bet_result_2['good_pred'][df_bet_result_2['prediction'] == df_bet_result_2['winner']] = 1
    
    ps3838_bet_simulator_result(df_bet_result_2, '2 by 2')
    

    # =============================================================================
    #  3 bets
    # =============================================================================
    df_bet = pd.DataFrame()
    list_bet             = glob('../dataset/local/df_betting_simulator_*.xls')
    for i, bet in enumerate(list_bet):
        df_bet_temp = pd.DataFrame.from_csv(bet, encoding='utf-8')
        df_bet_temp['bet_num'] = i 
        df_bet = pd.concat((df_bet, df_bet_temp))
    try:
        list_already_bet = df_bet.team_to_bet_id.unique().tolist()
    except:
        list_already_bet = []
        
    number_bet  = 3
    df_parlay_filter_simulator = df_parlay_filter[~(df_parlay_filter.team_to_bet_id.isin(list_already_bet))]
    
    if len(df_parlay_filter_simulator)>=number_bet:
        print 'OK TO SIMULATOR 3'
        df_betting_simulator = df_parlay_filter_simulator[['match_date','sport','ligue','index','team_to_bet','min_bet','bet_diff','team_to_bet_id','team_home']]
        df_betting_simulator = df_betting_simulator.iloc[0:number_bet]
        date_bet = datetime.now()
        date_bet_string = str(date_bet.hour).zfill(2) + ':' + str(date_bet.minute).zfill(2) + '_' + str(date_bet.day) + '_' + str(date_bet.month) + '_' + str(date_bet.year)
        df_betting_simulator.to_csv('../dataset/local/df_betting_simulator_' + date_bet_string + '.xls', encoding='utf-8')
    else:
        print 'SIMULATOR 3 - ', len(df_parlay_filter_simulator)
    
    df_bet_result = pd.merge(df_bet, df_result, how='inner', on=['match_date','sport','team_home'])
    df_bet_result['prediction'] = 2
    df_bet_result['prediction'][df_bet_result.team_home == df_bet_result.team_to_bet] = 1
    df_bet_result['good_pred']  = 0
    df_bet_result['good_pred'][df_bet_result['prediction'] == df_bet_result['winner']] = 1
    
    ps3838_bet_simulator_result(df_bet_result, '3 by 3')

    
    
    # =============================================================================
    #  5 bets
    # =============================================================================    
    df_bet_5 = pd.DataFrame()
    list_bet_5             = glob('../dataset/local/df_betting_simulator5_*.xls')
    for i, bet_5 in enumerate(list_bet_5):
        df_bet_temp_5 = pd.DataFrame.from_csv(bet_5, encoding='utf-8')
        df_bet_temp_5['bet_num'] = i 
        df_bet_5 = pd.concat((df_bet_5, df_bet_temp_5))
    try:
        list_already_bet_5 = df_bet_5.team_to_bet_id.unique().tolist()
    except:
        list_already_bet_5 = []
    
    number_bet  = 5
    df_parlay_filter_simulator_5 = df_parlay_filter[~(df_parlay_filter.team_to_bet_id.isin(list_already_bet_5))]
    
    if len(df_parlay_filter_simulator_5)>=number_bet:
        print 'OK TO SIMULATOR 5'
        df_betting_simulator_5 = df_parlay_filter_simulator_5[['match_date','sport','ligue','index','team_to_bet','min_bet','bet_diff','team_to_bet_id','team_home']]
        df_betting_simulator_5 = df_betting_simulator_5.iloc[0:number_bet]
        date_bet = datetime.now()
        date_bet_string = str(date_bet.hour).zfill(2) + ':' + str(date_bet.minute).zfill(2) + '_' + str(date_bet.day) + '_' + str(date_bet.month) + '_' + str(date_bet.year)
        df_betting_simulator_5.to_csv('../dataset/local/df_betting_simulator5_' + date_bet_string + '.xls', encoding='utf-8')
    else:
        print 'SIMULATOR 5 - ', len(df_parlay_filter_simulator_5)
    
    df_bet_result_5 = pd.merge(df_bet_5, df_result, how='inner', on=['match_date','sport','team_home'])
    df_bet_result_5['prediction'] = 2
    df_bet_result_5['prediction'][df_bet_result_5.team_home == df_bet_result_5.team_to_bet] = 1
    df_bet_result_5['good_pred']  = 0
    df_bet_result_5['good_pred'][df_bet_result_5['prediction'] == df_bet_result_5['winner']] = 1
    
    ps3838_bet_simulator_result(df_bet_result_5, '5 by 5')


    
    # =============================================================================
    #  7 bets
    # =============================================================================    
    df_bet_7 = pd.DataFrame()
    list_bet_7             = glob('../dataset/local/df_betting_simulator7_*.xls')
    for i, bet_7 in enumerate(list_bet_7):
        df_bet_temp_7 = pd.DataFrame.from_csv(bet_7, encoding='utf-8')
        df_bet_temp_7['bet_num'] = i 
        df_bet_7 = pd.concat((df_bet_7, df_bet_temp_7))
    try:
        list_already_bet_7 = df_bet_7.team_to_bet_id.unique().tolist()
    except:
        list_already_bet_7 = []
        
    number_bet  = 7
    df_parlay_filter_simulator_7 = df_parlay_filter[~(df_parlay_filter.team_to_bet_id.isin(list_already_bet_7))]
    
    if len(df_parlay_filter_simulator_7)>=number_bet:
        print 'OK TO SIMULATOR 7'
        df_betting_simulator_7 = df_parlay_filter_simulator_7[['match_date','sport','ligue','index','team_to_bet','min_bet','bet_diff','team_to_bet_id','team_home']]
        df_betting_simulator_7 = df_betting_simulator_7.iloc[0:number_bet]
        date_bet = datetime.now()
        date_bet_string = str(date_bet.hour).zfill(2) + ':' + str(date_bet.minute).zfill(2) + '_' + str(date_bet.day) + '_' + str(date_bet.month) + '_' + str(date_bet.year)
        df_betting_simulator_7.to_csv('../dataset/local/df_betting_simulator7_' + date_bet_string + '.xls', encoding='utf-8')
    else:
        print 'SIMULATOR 7 - ', len(df_parlay_filter_simulator_7)
    
    df_bet_result_7 = pd.merge(df_bet_7, df_result, how='inner', on=['match_date','sport','team_home'])
    df_bet_result_7['prediction'] = 2
    df_bet_result_7['prediction'][df_bet_result_7.team_home == df_bet_result_7.team_to_bet] = 1
    df_bet_result_7['good_pred']  = 0
    df_bet_result_7['good_pred'][df_bet_result_7['prediction'] == df_bet_result_7['winner']] = 1
    
    ps3838_bet_simulator_result(df_bet_result_7, '7 by 7')

    
        
    # =============================================================================
    #  10 bets
    # =============================================================================    
    df_bet_10 = pd.DataFrame()
    list_bet_10             = glob('../dataset/local/df_betting_simulator10_*.xls')
    for i, bet_10 in enumerate(list_bet_10):
        df_bet_temp_10 = pd.DataFrame.from_csv(bet_10, encoding='utf-8')
        df_bet_temp_10['bet_num'] = i 
        df_bet_10 = pd.concat((df_bet_10, df_bet_temp_10))
    try:
        list_already_bet_10 = df_bet_10.team_to_bet_id.unique().tolist()
    except:
        list_already_bet_10 = []
        
    number_bet  = 10
    df_parlay_filter_simulator_10 = df_parlay_filter[~(df_parlay_filter.team_to_bet_id.isin(list_already_bet_10))]
    
    if len(df_parlay_filter_simulator_10)>=number_bet:
        print 'OK TO SIMULATOR 10'
        df_betting_simulator_10 = df_parlay_filter_simulator_10[['match_date','sport','ligue','index','team_to_bet','min_bet','bet_diff','team_to_bet_id','team_home']]
        df_betting_simulator_10 = df_betting_simulator_10.iloc[0:number_bet]
        date_bet = datetime.now()
        date_bet_string = str(date_bet.hour).zfill(2) + ':' + str(date_bet.minute).zfill(2) + '_' + str(date_bet.day) + '_' + str(date_bet.month) + '_' + str(date_bet.year)
        df_betting_simulator_10.to_csv('../dataset/local/df_betting_simulator10_' + date_bet_string + '.xls', encoding='utf-8')
    else:
        print 'SIMULATOR 10 - ', len(df_parlay_filter_simulator_10)
     
    df_bet_result_10 = pd.merge(df_bet_10, df_result, how='inner', on=['match_date','sport','team_home'])
    df_bet_result_10['prediction'] = 2
    df_bet_result_10['prediction'][df_bet_result_10.team_home == df_bet_result_10.team_to_bet] = 1
    df_bet_result_10['good_pred']  = 0
    df_bet_result_10['good_pred'][df_bet_result_10['prediction'] == df_bet_result_10['winner']] = 1
    
    ps3838_bet_simulator_result(df_bet_result_10, '10 by 10')


    # =============================================================================
    #  1 bet
    # =============================================================================    
    print('1 BY 1')
    result = 0
    cave = 0
    for item in range(len(df_bet_result)):
        cave = cave + mise
        if df_bet_result.good_pred.iloc[item] == 1:
            result = result+(df_bet_result.min_bet.iloc[item]+0.03-1)*mise
        else:
#            print 'lose'
            result = result - mise
    print 'cave     : ', int(cave),' €'
    print 'gain pur : ', int(result),' €'
    print 'ROI cave : ', round(result/float(cave)*100,2), '%'
    print round(result/mise,2)*100,"%"
    print ''

    
    print('******** RESULT SIMULATION **********')
    print 'Number Good pred : ', len(df_bet_result)
    print 'Number Bad pred  : ', len(df_bet_result[df_bet_result.good_pred == 0])
    print round(df_bet_result.good_pred.sum()/float(len(df_bet_result))*100,2), '%'
    print('*************************************')


    return df_bet, df_bet_result


# =============================================================================
# PLACE REAL ORDER
# =============================================================================
def ps3838_bet_parlay(df_betting_parlay):
    team_to_bet_id = str(df_betting_parlay.team_to_bet_id.tolist())[1:-1].replace('u','').replace("'","").replace(' ','')
    sport_to_bet   = str(df_betting_parlay.sport.tolist())[1:-1].replace('u','').replace("'","")
    os.system('node ps3838_place_bet_parlay_standalone.js "' + team_to_bet_id + '" "' + sport_to_bet + '"')
    date_bet = datetime.now()
    date_bet_string = str(date_bet.hour).zfill(2) + ':' + str(date_bet.minute).zfill(2) + '_' + str(date_bet.day) + '_' + str(date_bet.month) + '_' + str(date_bet.year)
    df_betting_parlay.to_csv('../dataset/local/Real_df_betting_parlay_' + date_bet_string + '.xls', encoding='utf-8')


def ps3838_bet_single(df_single, df_merge_single, draw_activated):
    warnings.filterwarnings('ignore')

    df_merge_single['sport'] = df_merge_single['sport'].apply(lambda x : x.lower()) 
    # =============================================================================
    # Ajust bet parameter SINGLE
    # =============================================================================
    df_temp = 0
    list_sport = df_merge_single.sport.unique().tolist()
    dict_parameter_sport_single = {}
    
    ###
    """
    for item in list_sport:
        print '\n' + item
        exec('df_merge_single_' + item.replace(' ','_') + ' = df_merge_single[df_merge_single.sport == "' + item + '"]')
        exec('df_temp = df_merge_single_' + item.replace(' ','_'))
        dict_temp = optimisation_3(df_temp)
        dict_parameter_sport_single.update(dict_temp)
    df_single_filter = optimisation_apply(df_single, dict_parameter_sport_single)
    """
    
    """
    df_single_filter = df_single[df_single.sport == 'soccer']
    df_single_filter.match_date  = df_single_filter.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    df_single_filter             = df_single_filter[(df_single_filter.match_date < datetime.now()+timedelta(hours=10)) & (df_single_filter.match_date > datetime.now())]
    df_single_filter.dropna(inplace=True)
    """
    
    ###
    mod_value                    = 0.1
    dict_parameter_sport         = optimisation_5(df_merge_single, mod_value)
    df_single_filter             = optimisation_5_apply(df_single, dict_parameter_sport, mod_value)
    
    if len(df_single_filter) == 0:
        return
    
    df_single_filter.match_date  = df_single_filter.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

    df_single_filter             = df_single_filter[(df_single_filter.match_date < datetime.now()+timedelta(minutes=20)) & (df_single_filter.match_date > datetime.now())]
    df_single_filter.drop_duplicates(subset=['match_date','team_home'], inplace=True)
        
    # =============================================================================
    # Print opportunity SINGLE
    # =============================================================================
    print '*****************************'
    print str(datetime.now())
    df_single_filter.sort_values('bet_diff', ascending=False, inplace=True)
    print 'df_single_filter : ', len(df_single_filter)
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
    
    number_bet  = 10
    df_single_filter_bulk = df_single_filter.copy()
    df_single_filter = df_single_filter[~(df_single_filter.team_to_bet_id.isin(list_already_bet_single))]
    df_betting_single = df_single_filter[['match_date','sport','ligue','index','team_to_bet','min_bet','bet_diff','bet_X','team_to_bet_id','team_home','team_X_id']]
    df_betting_single = df_betting_single.iloc[0:number_bet]
    df_betting_single.team_X_id.fillna('0', inplace=True)

    if len(df_betting_single) != 0:
        print '*****************************'
        print 'df_betting single : ', len(df_betting_single)
        for i in range(len(df_betting_single)):
            if i == 0:
                bet_single = df_betting_single.min_bet.iloc[i]
            if i > 0:
                bet_single = bet_single*df_betting_single.min_bet.iloc[i]
        print 'bet_single : ', bet_single
        print str(datetime.now())
        print '*****************************'
    
        # =============================================================================
        # EXECUTE BET
        # =============================================================================
        team_X_id       = str(df_betting_single.team_X_id.tolist())[1:-1].replace('u','').replace("'","").replace(' ','')
        team_to_bet_id  = str(df_betting_single.team_to_bet_id.tolist())[1:-1].replace('u','').replace("'","").replace(' ','')
        sport_to_bet    = str(df_betting_single.sport.tolist())[1:-1].replace('u','').replace("'","")
        if draw_activated == 1:
            team_to_bet_id  = team_to_bet_id + ',' + team_X_id
            sport_to_bet    = sport_to_bet + ', ' + sport_to_bet
            
        os.system('node ps3838_place_bet_single_standalone.js "' + team_to_bet_id + '" "' + sport_to_bet + '"')
        date_bet = datetime.now()
        date_bet_string = str(date_bet.hour).zfill(2) + ':' + str(date_bet.minute).zfill(2) + '_' + str(date_bet.day) + '_' + str(date_bet.month) + '_' + str(date_bet.year)
        df_betting_single.to_csv('../dataset/local/Real_df_betting_single_' + date_bet_string + '.xls', encoding='utf-8')
    else:
        if len(df_single_filter_bulk) != 0:
            print '*****************************'
            print 'All Single bet already placed'
            print str(datetime.now())
            print '*****************************'
        else:
            print '*****************************'
            print 'No single bet single'
            print str(datetime.now())
            print '*****************************'
    
    df_real_betting_single_done = pd.DataFrame()
    list_bet_single_done             = glob('../dataset/local/Real_df_betting_single*.xls')
    for i, bet_single_done in enumerate(list_bet_single_done):
        df_betting_single_done_temp = pd.DataFrame.from_csv(bet_single_done, encoding='utf-8')
        df_betting_single_done_temp['bet_num'] = i 
        df_real_betting_single_done = pd.concat((df_real_betting_single_done, df_betting_single_done_temp))
    df_real_betting_single_done.to_csv('../dataset/local/df_real_betting_single.xls', encoding='utf-8')
