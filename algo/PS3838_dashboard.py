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
import datetime
import sys
import json

import pandas             as pd

from datetime                                                                  import datetime
from datetime                                                                  import timedelta
from tabulate                                                                  import tabulate

from PS3838_scrap_function                                                     import ps3838_scrap_parlay, ps3838_scrap_single, ps3838_scrap_result
from PS3838_support_function                                                   import encode_decode, optimisation, optimisation_2, optimisation_3, optimisation_apply, match_filter_prediction
from PS3838_bet_function                                                       import ps3838_bet_simulator, ps3838_bet_parlay


def dashboard(dict_parameter_sport, GMT_to_add):
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
    try:
        df_betting_single_done = pd.DataFrame.from_csv('../dataset/local/df_real_betting_single.xls', encoding='utf-8')
        list_already_bet_single = df_betting_single_done.team_to_bet_id.unique().tolist()
    except:
        list_already_bet_single = []

    if len(list_already_bet_single) != 0:   
        df_betting_single_done['prediction'] = 2
        df_betting_single_done.prediction[df_betting_single_done.team_to_bet == df_betting_single_done.team_home] = 1
        
        df_merge_single_bet = pd.merge(df_betting_single_done, df_result_single, how='inner', on=['match_date','sport','team_home'])
        list_already_result = df_merge_single_bet.team_to_bet_id.unique().tolist()
        df_merge_single_bet = df_merge_single_bet[['match_date','sport','ligue','bet_diff','min_bet','bet_X','mode_bet','prediction','winner','team_home']]
        df_merge_single_bet['good_pred']                          = 0
        df_merge_single_bet.good_pred[(df_merge_single_bet.prediction == df_merge_single_bet.winner) | ((df_merge_single_bet.mode_bet == 'X') & (df_merge_single_bet.winner == 0))] = 1
        df_merge_single_bet['bad_pred']                           = 0
        df_merge_single_bet.bad_pred[df_merge_single_bet.good_pred == 0]  = 1
        df_merge_single_bet.match_date                = df_merge_single_bet.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        df_merge_single_bet.sort_values('match_date', ascending=False, inplace=True)
        
        try:
            df_single_ongoing   = df_betting_single_done[~(df_betting_single_done.team_to_bet_id.isin(list_already_result))]
            df_single_ongoing   = df_single_ongoing[['match_date','sport','ligue','bet_diff','min_bet','bet_X','mode_bet','prediction','team_to_bet']]
            df_single_ongoing.sort_values('match_date', ascending=False, inplace=True)
        except:
            df_single_ongoing   = pd.DataFrame()
#        df_merge_single_bet = df_merge_single_bet[df_merge_single_bet.sport == 'soccer']
        
        
        
        
        # =============================================================================
        #  1 bet
        # =============================================================================    
        result          = 0
        cave            = 0
        mise            = 5        
        num_good_pred   = 0
        num_bad_pred    = 0
        
        for item in range(len(df_merge_single_bet)):
            if (df_merge_single_bet.min_bet.iloc[item] > 1.):
                if df_merge_single_bet.mode_bet.iloc[item] == 'X':
                    cave = cave + mise*2
                    result = result - mise*2
                    
                    if df_merge_single_bet.good_pred.iloc[item] == 1 and df_merge_single_bet.winner.iloc[item] != 0:
                        result = result + df_merge_single_bet.min_bet.iloc[item]*mise
                        num_good_pred = num_good_pred + 1
                    
                    if df_merge_single_bet.winner.iloc[item] == 0:
                        result = result + df_merge_single_bet.bet_X.iloc[item]*mise
                        num_good_pred = num_good_pred + 1
                        
                    if df_merge_single_bet.good_pred.iloc[item] == 0 and df_merge_single_bet.winner.iloc[item] != 0:
                        num_bad_pred = num_bad_pred + 1
        
        
                if df_merge_single_bet.mode_bet.iloc[item] == 'S':
                    cave = cave + mise
                    result = result - mise
                    if df_merge_single_bet.good_pred.iloc[item] == 1:
                        result = result + df_merge_single_bet.min_bet.iloc[item]*mise
                        num_good_pred = num_good_pred + 1
                    else:
                        num_bad_pred = num_bad_pred + 1
                        
                        
        orig_stdout = sys.stdout
        f = open('../dataset/local/dashbord.txt', 'w')
        sys.stdout = f
        print('********       RESULTS     **********')
        print 'HEURE              : ', str((datetime.now()+timedelta(hours=GMT_to_add)).strftime('%d %B %Y, %H:%M:%S'))
        print 'Bet OnGoing        : ', (len(df_betting_single_done)-len(df_merge_single_bet))
        print 'Cave OnGoing       : ', (len(df_betting_single_done)-len(df_merge_single_bet))*mise*2
        print(tabulate(df_single_ongoing, headers='keys', tablefmt='psql'))
        print('*************************************')
        print(json.dumps(dict_parameter_sport, indent=4, sort_keys=True))
        print('*************************************')
        print 'Bet Done           : ', len(df_merge_single_bet)
        print 'TOTAL cave         : ', int(cave),'euros'
        print 'Number Good pred   : ', num_good_pred
        print 'Number Bad pred    : ', num_bad_pred
        print '% good prediction  : ', round(num_good_pred/float(num_good_pred+num_bad_pred+0.001)*100,2), '%'
        print 'TOTAL gain pur     : ', round(result,2),'euros'
        print 'ROI cave           : ', round(result/float(cave)*100,2), '%'
        print 'ROI mise           : ', round(result/mise,2)*100, "%"
        print(tabulate(df_merge_single_bet, headers='keys', tablefmt='psql'))
        print('*************************************')

        
        f.close()
        sys.stdout = orig_stdout
        
        os.system('clear')
        f = open('../dataset/local/dashbord.txt', 'r')
        print f.read()
        f.close()
    else:
        print('no bet for the moment')