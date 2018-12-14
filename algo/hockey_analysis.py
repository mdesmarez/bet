#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 16:04:55 2018

@author: mathieu
"""

# =============================================================================
# 
# =============================================================================
import os
import datetime

import numpy                                                                   as np
import pandas                                                                  as pd

from glob                                                                      import glob
from datetime                                                                  import timedelta



# =============================================================================
# 
# =============================================================================
list_file_          = glob('../dataset/local/___*')
for filename in list_file_:
    os.system('mv "' + filename + '" "' + filename.replace('___','') + '"')



# =============================================================================
# 
# =============================================================================
def recover_team_point(df_temp, list_columns):    
    a = df_temp[df_temp.score_IT_away == df_temp.score_IT_home]
    a['team_loser_add_point'] = 1
    df_temp['team_winner_add_point']    = 2
    df_temp['team_loser_add_point']     = a['team_loser_add_point']
    df_temp.fillna(0, inplace=True)
    
    dict_df_temp        = df_temp.to_dict(orient='index')
    list_keys           = dict_df_temp.keys()
    dict_point          = {}
    dict_point_to_add   = {}
    dict_match_play     = {}
    dict_result_n1      = {}
    dict_result_n2      = {}
    dict_result_n3      = {}
    dict_result_n4      = {}
    dict_result_n5      = {}
    dict_day_last_match = {}


    max_point           = 0
    
    for i, item in enumerate(list_keys):      
        try:
            team_home_temp          = dict_df_temp[item]['team_home']
            team_away_temp          = dict_df_temp[item]['team_away']
            
            ###
            try:
                dict_df_temp[item]['team_home_point'] = dict_point_to_add[team_home_temp]
            except:
                dict_df_temp[item]['team_home_point'] = 0
                
            try:
                dict_df_temp[item]['team_away_point'] = dict_point_to_add[team_away_temp]
            except:
                dict_df_temp[item]['team_away_point'] = 0
            
            ###
            try:
                dict_df_temp[item]['team_home_nbr_match'] = dict_match_play[team_home_temp]
            except:
                dict_df_temp[item]['team_home_nbr_match'] = 0
                
            try:
                dict_df_temp[item]['team_away_nbr_match'] = dict_match_play[team_away_temp]
            except:
                dict_df_temp[item]['team_away_nbr_match'] = 0
            
            ###
            try:
                dict_df_temp[item]['result_n1_home'] = dict_result_n1[team_home_temp]
            except:
                dict_df_temp[item]['result_n1_home'] = 0
                
            try:
                dict_df_temp[item]['result_n1_away'] = dict_result_n1[team_away_temp]
            except:
                dict_df_temp[item]['result_n1_away'] = 0

            try:
                dict_df_temp[item]['result_n2_home'] = dict_result_n2[team_home_temp]
            except:
                dict_df_temp[item]['result_n2_home'] = 0
                
            try:
                dict_df_temp[item]['result_n2_away'] = dict_result_n2[team_away_temp]
            except:
                dict_df_temp[item]['result_n2_away'] = 0
                
            try:
                dict_df_temp[item]['result_n3_home'] = dict_result_n3[team_home_temp]
            except:
                dict_df_temp[item]['result_n3_home'] = 0
                
            try:
                dict_df_temp[item]['result_n3_away'] = dict_result_n3[team_away_temp]
            except:
                dict_df_temp[item]['result_n3_away'] = 0
                
            try:
                dict_df_temp[item]['result_n4_home'] = dict_result_n4[team_home_temp]
            except:
                dict_df_temp[item]['result_n4_home'] = 0
                
            try:
                dict_df_temp[item]['result_n4_away'] = dict_result_n4[team_away_temp]
            except:
                dict_df_temp[item]['result_n4_away'] = 0
                
            try:
                dict_df_temp[item]['result_n5_home'] = dict_result_n5[team_home_temp]
            except:
                dict_df_temp[item]['result_n5_home'] = 0
                
            try:
                dict_df_temp[item]['result_n5_away'] = dict_result_n5[team_away_temp]
            except:
                dict_df_temp[item]['result_n5_away'] = 0


            try:
                dict_df_temp[item]['day_last_match_home'] = dict_day_last_match[team_home_temp]
            except:
                dict_df_temp[item]['day_last_match_home'] = 99
            try:
                dict_df_temp[item]['day_last_match_away'] = dict_day_last_match[team_away_temp]
            except:
                dict_df_temp[item]['day_last_match_away'] = 99


                
            team_home_point_temp    = dict_df_temp[item]['team_home_point']
            team_away_point_temp    = dict_df_temp[item]['team_away_point']
            
            
            
            ###
            try:
                dict_df_temp[item].update({'day_last_match_home': (dict_df_temp[item]['date_match'] - dict_day_last_match[team_home_temp]).days })
            except:
                dict_df_temp[item].update({'day_last_match_home': 0})

            try:
                dict_df_temp[item].update({'day_last_match_away': (dict_df_temp[item]['date_match'] - dict_day_last_match[team_away_temp]).days })
            except:
                dict_df_temp[item].update({'day_last_match_away': 0})
                
            dict_day_last_match[team_home_temp] = dict_df_temp[item]['date_match']
            dict_day_last_match[team_away_temp] = dict_df_temp[item]['date_match']  
            
            
            try:
                dict_result_n5[team_home_temp] = dict_result_n4[team_home_temp] 
            except:
                pass
            try:
                dict_result_n5[team_away_temp] = dict_result_n4[team_away_temp] 
            except:
                pass
    
            try:
                dict_result_n4[team_home_temp] = dict_result_n3[team_home_temp] 
            except:
                pass
            try:
                dict_result_n4[team_away_temp] = dict_result_n3[team_away_temp] 
            except:
                pass
            
            try:
                dict_result_n3[team_home_temp] = dict_result_n2[team_home_temp] 
            except:
                pass
            try:
                dict_result_n3[team_away_temp] = dict_result_n2[team_away_temp] 
            except:
                pass

            try:
                dict_result_n2[team_home_temp] = dict_result_n1[team_home_temp] 
            except:
                pass            
            try:
                dict_result_n2[team_away_temp] = dict_result_n1[team_away_temp] 
            except:
                pass
            
            
            if dict_df_temp[item]['team_winner_HA'] == 'team_home':
                if dict_df_temp[item]['score_IT_home'] == dict_df_temp[item]['score_IT_away']:
                    dict_result_n1[team_home_temp] = 1
                    dict_result_n1[team_away_temp] = -1
                else:
                    dict_result_n1[team_home_temp] = 2
                    dict_result_n1[team_away_temp] = -2
            else:
                if dict_df_temp[item]['score_IT_home'] == dict_df_temp[item]['score_IT_away']:
                    dict_result_n1[team_home_temp] = -1
                    dict_result_n1[team_away_temp] = 1
                else:
                    dict_result_n1[team_home_temp] = -2
                    dict_result_n1[team_away_temp] = 2


            ### Calculation point after match
            team_winner_name       = dict_df_temp[item]['team_winner']
            team_loser_name        = dict_df_temp[item]['team_loser']
            team_winner_point      = dict_df_temp[item]['team_winner_add_point']
            team_loser_point       = dict_df_temp[item]['team_loser_add_point']
            try:
                dict_point_to_add.update({team_winner_name:team_winner_point + dict_point_to_add[team_winner_name]})
            except:
                dict_point_to_add.update({team_winner_name:team_winner_point})
            try:
                dict_point_to_add.update({team_loser_name:team_loser_point + dict_point_to_add[team_loser_name]})
            except:
                dict_point_to_add.update({team_loser_name:team_loser_point})

            try:
                dict_match_play.update({team_winner_name:1 + dict_match_play[team_winner_name]})
            except:
                dict_match_play.update({team_winner_name:1})
            try:
                dict_match_play.update({team_loser_name:1 + dict_match_play[team_loser_name]})
            except:
                dict_match_play.update({team_loser_name:1})
                
            
            dict_point.update({team_home_temp:team_home_point_temp})
            dict_point.update({team_away_temp:team_away_point_temp})
       
            min_point       = 1000
            for j in range(10):
                try:
                    if dict_df_temp[item-j]['team_away_point'] < min_point:
                        min_point = dict_df_temp[item-j]['team_away_point']
                    if dict_df_temp[item-j]['team_home_point'] < min_point:
                        min_point = dict_df_temp[item-j]['team_home_point']
                except:
                    pass
                
            if team_home_point_temp > max_point:
                max_point = team_home_point_temp
            if team_away_point_temp > max_point:
                max_point = team_away_point_temp
                

            dict_df_temp[list_keys[i]].update({'team_max_point':max_point})
            dict_df_temp[list_keys[i]].update({'team_min_point':min_point})
        
#            try:    
#                dict_df_temp[list_keys[i+1]].update({'team_home_point_real':dict_point[dict_df_temp[list_keys[i+1]]['team_home']]})
#            except:
#                pass
#                dict_df_temp[list_keys[i+1]].update({'team_home_point_real':0})
#    
#            try:
#                dict_df_temp[list_keys[i+1]].update({'team_away_point_real':dict_point[dict_df_temp[list_keys[i+1]]['team_away']]})
#            except:
#                pass
#                dict_df_temp[list_keys[i+1]].update({'team_away_point_real':0})
#                
        except IndexError:
            print i, len(list_keys)
            pass
    
    df_temp_new = pd.DataFrame(dict_df_temp).T
#    df_temp_new['team_home_point'] = df_temp_new['team_home_point_real']
#    df_temp_new['team_away_point'] = df_temp_new['team_away_point_real']
#    del df_temp_new['team_home_point_real']
#    del df_temp_new['team_away_point_real']
    
    df_temp_new['nbr_match_diff_home_away'] = df_temp_new['team_home_nbr_match'] - df_temp_new['team_away_nbr_match']
    
    df_temp_new = df_temp_new[[u'competition', u'date_match', u'match_name', u'team_winner',
       u'team_loser', u'team_winner_HA', u'team_loser_HA',
       u'point_diff_home_away', u'score_1P', u'score_2P', u'score_3P',
       u'score_IT_final', u'score_OT_final', u'team_home', u'team_home_point',
       u'score_IT_home', u'score_OT_home', u'team_away', u'team_away_point',
       u'score_IT_away', u'score_OT_away',u'team_min_point',u'team_max_point',u'nbr_match_diff_home_away',
       u'result_n1_home',u'result_n1_away',u'result_n2_home',u'result_n2_away',u'result_n3_home',u'result_n3_away',
       u'result_n4_home',u'result_n4_away',u'result_n5_home',u'result_n5_away',
       u'day_last_match_home', u'day_last_match_away', u'season_period']]
    
    df_temp_new.fillna(0, inplace=True)
    
    df_temp_new['point_diff_home_away'] = df_temp_new['team_home_point'] - df_temp_new['team_away_point']
    
    return df_temp_new


# =============================================================================
# 
# =============================================================================
df_NHL_scores               = pd.read_csv('../dataset/local/df_NHL_scores_espn.csv', index_col=0, encoding='utf-8')
df_NHL_scores.dropna(subset=['date_match'], inplace=True)
df_NHL_scores['date_match'] = pd.to_datetime(df_NHL_scores.date_match)
df_NHL_scores.dropna(subset=['match_name'],inplace=True)
df_NHL_scores.sort_values(['date_match'], inplace=True, ascending=True)
df_NHL_scores.reset_index(drop=True, inplace=True)

year_min                    = df_NHL_scores.date_match.min().year
year_max                    = df_NHL_scores.date_match.max().year
list_year                   = np.linspace(year_min,year_max,year_max-year_min+1).astype(int)

###
#list_year = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
#list_year = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]

list_year = [2018]

###

for year in list_year:
    print year
    try:
        date_season_start           = datetime.datetime.strptime(str(year) + "-10", "%Y-%m")
        date_season_stop            = datetime.datetime.strptime(str(year+1) + "-05", "%Y-%m")
        df_temp                     = df_NHL_scores[(df_NHL_scores.date_match >= date_season_start) & (df_NHL_scores.date_match <= date_season_stop)]
        df_temp['season_period']    = df_temp.date_match.apply(lambda x: 1 if (x.month<5) else 0)
        name                        = 'df_NHL_scores_' + str(year) + '_' + str(year+1)
        list_columns                = df_temp.columns
        df_temp.reset_index(drop=True, inplace=True)
        df_temp                     = recover_team_point(df_temp, list_columns)
        df_temp.to_csv('../dataset/local/' + name + '.csv', encoding='utf-8')
    except:
        pass
    

#%% =============================================================================
# ASSEMBLING SCORES BET
# =============================================================================
df_oddsportal               = pd.read_csv('../dataset/local/df_oddsportal.csv', index_col=0, encoding='utf-8')
df_oddsportal['date_match'] = pd.to_datetime(df_oddsportal.match_date)
df_oddsportal['week_num']   = df_oddsportal.date_match.apply(lambda x : str(x.year) + '_' + str(x.isocalendar()[1]).zfill(2))
df_oddsportal.sort_values(['date_match'], inplace=True, ascending=True)
df_oddsportal.reset_index(drop=True, inplace=True)

df_temp                     = df_oddsportal.bet_V1.replace('-','')
df_oddsportal.bet_V1        = df_temp
df_temp                     = df_oddsportal.bet_V2.replace('-','')
df_oddsportal.bet_V2        = df_temp


for year in list_year:
    print year
    try:
        df_NHL_scores               = pd.read_csv('../dataset/local/df_NHL_scores_' + str(year) + '_' + str(year+1) + '.csv', index_col=0, encoding='utf-8')
        df_NHL_scores.dropna(subset=['date_match'], inplace=True)
        df_NHL_scores['date_match'] = pd.to_datetime(df_NHL_scores.date_match)
    
        aaa={}
        a = pd.DataFrame()
        no_bet = 0
        for i in range(len(df_NHL_scores)):
#            if i == 101 and aaa[100]['0:0'] == 0:
#                print 'No bet data for : ', year
#                no_bet = 1
#                break
            if i%100 == 0:
                print i, len(df_NHL_scores)
            team_home       = df_NHL_scores.team_home.iloc[i].lower().split()[-1]
            team_away       = df_NHL_scores.team_away.iloc[i].lower().split()[-1]
            match_date      = df_NHL_scores.date_match.iloc[i]            
            year_num        = match_date.year
            week_num        = str(year_num) + '_' + str(match_date.isocalendar()[1]).zfill(2)
            week_num_plus = week_num
            week_num_minus = week_num
    #        week_num_plus   = str((match_date + timedelta(days=2)).year) + '_' + str((match_date + timedelta(days=2)).isocalendar()[1]).zfill(2)
    #        week_num_minus  = str((match_date - timedelta(days=2)).year) + '_' + str((match_date - timedelta(days=2)).isocalendar()[1]).zfill(2)
        
            
            a               = df_oddsportal[((df_oddsportal.week_num == week_num) |
                                            (df_oddsportal.week_num == week_num_minus) | 
                                            (df_oddsportal.week_num == week_num_plus)) & 
                                            ((df_oddsportal.team_home.str.contains(team_home, case=False)) & (df_oddsportal.team_away.str.contains(team_away, case=False)))]
            
            if len(a) == 0:
                a = pd.DataFrame([{'0:0':0}])
                
            aa              = a.to_dict(orient='index')
            aaa.update({i:aa[aa.keys()[0]]})
            b               = pd.DataFrame(df_NHL_scores.iloc[i]).T
            bb              = b.to_dict(orient='index')
            aaa[i].update(bb[bb.keys()[0]])
    
        if no_bet == 0:
            df_score_bet    = pd.DataFrame(aaa).T
            df_score_bet    = df_score_bet.reindex_axis(sorted(df_score_bet.columns, reverse=True), axis=1)        
        
            df_score_bet.dropna(subset=['match_date'], inplace=True)
            df_score_bet['match_date'] = pd.to_datetime(df_score_bet.match_date)
            df_score_bet.dropna(subset =['match_name'],inplace=True)
            df_score_bet.reset_index(drop=True, inplace=True)
            df_score_bet.sort_values(['match_date'], inplace=True, ascending=True)
            
            name                    = 'df_scores_bet_' + str(year) + '_' + str(year+1)
            df_temp         =   df_score_bet[[\
                                 u'competition',
                                 u'date_match',
                                 u'match_name',
                                 u'team_winner',
                                 u'team_loser',
                                 u'team_winner_HA',
                                 u'team_loser_HA',
                                 u'point_diff_home_away',
                                 u'score_1P',
                                 u'score_2P',
                                 u'score_3P',
                                 u'score_IT_final',                     
                                 u'score_OT_final',
                                 u'team_home',
                                 u'team_home_point',
                                 u'score_IT_home',                     
                                 u'score_OT_home',
                                 u'team_away',
                                 u'team_away_point',
                                 u'score_IT_away',
                                 u'score_OT_away',    
                                 u'team_min_point',
                                 u'team_max_point',
                                 u'nbr_match_diff_home_away',
                                 u'result_n1_home',
                                 u'result_n1_away',
                                 u'result_n2_home',
                                 u'result_n2_away',
                                 u'result_n3_home',
                                 u'result_n3_away',
                                 u'result_n4_home',
                                 u'result_n4_away',
                                 u'result_n5_home',
                                 u'result_n5_away',
                                 u'day_last_match_home',
                                 u'day_last_match_away',
                                 u'season_period',
                                 u'bet_V1',
                                 u'bet_V2',
                                 u'bet_R1',
                                 u'bet_RN',
                                 u'bet_R2',
        #                         u'9:9',
        #                         u'9:8',
        #                         u'9:7',
        #                         u'9:6',
        #                         u'9:5',
        #                         u'9:4',
        #                         u'9:3',
        #                         u'9:2',
        #                         u'9:10',
        #                         u'9:1',
        #                         u'9:0',
        #                         u'8:9',
        #                         u'8:8',
        #                         u'8:7',
        #                         u'8:6',
        #                         u'8:5',
        #                         u'8:4',
        #                         u'8:3',
        #                         u'8:2',
        #                         u'8:10',
        #                         u'8:1',
        #                         u'8:0',
        #                         u'7:9',
        #                         u'7:8',
        #                         u'7:7',
        #                         u'7:6',
        #                         u'7:5',
        #                         u'7:4',
        #                         u'7:3',
        #                         u'7:2',
        #                         u'7:10',
        #                         u'7:1',
        #                         u'7:0',
        #                         u'6:9',
        #                         u'6:8',
        #                         u'6:7',
        #                         u'6:6',
        #                         u'6:5',
        #                         u'6:4',
    #                             u'6:3',
        #                         u'6:2',
        #                         u'6:10',
        #                         u'6:1',
    #                             u'6:0',
        #                         u'5:9',
        #                         u'5:8',
        #                         u'5:7',
        #                         u'5:6',
                                 u'5:5',
                                 u'5:4',
                                 u'5:3',
                                 u'5:2',
        #                         u'5:10',
                                 u'5:1',
                                 u'5:0',
        #                         u'4:9',
        #                         u'4:8',
        #                         u'4:7',
        #                         u'4:6',
                                 u'4:5',
                                 u'4:4',
                                 u'4:3',
                                 u'4:2',
        #                         u'4:10',
                                 u'4:1',
                                 u'4:0',
        #                         u'3:9',
        #                         u'3:8',
        #                         u'3:7',
        #                         u'3:6',
                                 u'3:5',
                                 u'3:4',
                                 u'3:3',
                                 u'3:2',
        #                         u'3:10',
                                 u'3:1',
                                 u'3:0',
        #                         u'2:9',
        #                         u'2:8',
        #                         u'2:7',
        #                         u'2:6',
                                 u'2:5',
                                 u'2:4',
                                 u'2:3',
                                 u'2:2',
        #                         u'2:10',
                                 u'2:1',
                                 u'2:0',
        #                         u'1:9',
        #                         u'1:8',
        #                         u'1:7',
        #                         u'1:6',
                                 u'1:5',
                                 u'1:4',
                                 u'1:3',
                                 u'1:2',
        #                         u'1:10',
                                 u'1:1',
                                 u'1:0',
        #                         u'10:9',
        #                         u'10:8',
        #                         u'10:7',
        #                         u'10:6',
        #                         u'10:5',
        #                         u'10:4',
        #                         u'10:3',
        #                         u'10:2',
        #                         u'10:10',
        #                         u'10:1',
        #                         u'10:0',
        #                         u'0:9',
        #                         u'0:8',
        #                         u'0:7',
        #                         u'0:6',
                                 u'0:5',
                                 u'0:4',
                                 u'0:3',
                                 u'0:2',
        #                         u'0:10',
                                 u'0:1',
                                 u'0:0',
                                 ]]
            
            df_temp.to_csv('../dataset/local/' + name + '.csv', encoding='utf-8') 
    
    except Exception as e:
        print e


"""
ee

df_NHL_scores['week_num']   = df_NHL_scores.date_match.apply(lambda x : str(x.year) + '_' + str(x.isocalendar()[1]).zfill(2))

df_oddsportal               = pd.read_csv('../dataset/local/df_oddsportal.csv', index_col=0, encoding='utf-8')
df_oddsportal['date_match'] = pd.to_datetime(df_oddsportal.match_date)

aaa={}

for i in range(len(df_oddsportal)):
    print i, len(df_oddsportal)
    team_home   = df_oddsportal.team_home.iloc[i].lower().split()[-1]
    if team_home == u'montr\xe9al':
        team_home = 'canadiens'
        
    team_away   = df_oddsportal.team_away.iloc[i].lower().split()[-1]
    if team_away == u'montr\xe9al':
        team_away = 'canadiens'

    match_date  = df_oddsportal.date_match.iloc[i]            
    year_num        = match_date.year
    week_num        = str(year_num) + '_' + str(match_date.isocalendar()[1]).zfill(2)
    week_num_plus   = str((match_date + timedelta(days=2)).year) + '_' + str((match_date + timedelta(days=2)).isocalendar()[1]).zfill(2)
    week_num_minus  = str((match_date - timedelta(days=2)).year) + '_' + str((match_date - timedelta(days=2)).isocalendar()[1]).zfill(2)

    try:    
        a   = df_NHL_scores[((df_NHL_scores.week_num == week_num) | (df_NHL_scores.week_num == week_num_minus) | (df_NHL_scores.week_num == week_num_plus)) & (df_NHL_scores.team_home.str.contains(team_home, case=False)) & (df_NHL_scores.team_away.str.contains(team_away, case=False))]
        aa  = a.to_dict(orient='index')
        aaa.update({i:aa[aa.keys()[0]]})
        b   = pd.DataFrame(df_oddsportal.iloc[i]).T
        bb  = b.to_dict(orient='index')
        aaa[i].update(bb[bb.keys()[0]])
    except:
        pass
"""


#%%
"""
# =============================================================================
#     
# =============================================================================
df_score_bet    = pd.DataFrame(aaa).T
df_score_bet    = df_score_bet.reindex_axis(sorted(df_score_bet.columns, reverse=True), axis=1)


# =============================================================================
# 
# =============================================================================
df_score_bet.dropna(subset=['match_date'], inplace=True)
df_score_bet['match_date'] = pd.to_datetime(df_score_bet.match_date)
df_score_bet.dropna(subset =['match_name'],inplace=True)
df_score_bet.reset_index(drop=True, inplace=True)
df_score_bet.sort_values(['match_date'], inplace=True, ascending=True)

year_min                    = df_score_bet.match_date.min().year
year_max                    = df_score_bet.match_date.max().year

list_year                   = np.linspace(year_min,year_max,year_max-year_min+1).astype(int)


for year in list_year:
    date_season_start       = datetime.datetime.strptime(str(year) + "-08", "%Y-%m")
    date_season_stop        = datetime.datetime.strptime(str(year+1) + "-08", "%Y-%m")
    df_temp                 = df_score_bet[(df_score_bet.match_date >= date_season_start) & (df_score_bet.match_date <= date_season_stop)]
    name                    = 'df_scores_bet_' + str(year) + '_' + str(year+1)
    df_temp         =   df_temp[[\
                         u'competition',
                         u'date_match',
                         u'match_name',
                         u'team_winner',
                         u'team_loser',
                         u'team_winner_HA',
                         u'team_loser_HA',
                         u'point_diff_home_away',
                         u'score_1P',
                         u'score_2P',
                         u'score_3P',
                         u'score_IT_final',                     
                         u'score_OT_final',
                         u'team_home',
                         u'team_home_point',
                         u'score_IT_home',                     
                         u'score_OT_home',
                         u'team_away',
                         u'team_away_point',
                         u'score_IT_away',
                         u'score_OT_away',                     
                         u'bet_V1',
                         u'bet_V2',
                         u'bet_R1',
                         u'bet_RN',
                         u'bet_R2',
                         u'9:9',
                         u'9:8',
                         u'9:7',
                         u'9:6',
                         u'9:5',
                         u'9:4',
                         u'9:3',
                         u'9:2',
                         u'9:10',
                         u'9:1',
                         u'9:0',
                         u'8:9',
                         u'8:8',
                         u'8:7',
                         u'8:6',
                         u'8:5',
                         u'8:4',
                         u'8:3',
                         u'8:2',
                         u'8:10',
                         u'8:1',
                         u'8:0',
                         u'7:9',
                         u'7:8',
                         u'7:7',
                         u'7:6',
                         u'7:5',
                         u'7:4',
                         u'7:3',
                         u'7:2',
                         u'7:10',
                         u'7:1',
                         u'7:0',
                         u'6:9',
                         u'6:8',
                         u'6:7',
                         u'6:6',
                         u'6:5',
                         u'6:4',
                         u'6:3',
                         u'6:2',
                         u'6:10',
                         u'6:1',
                         u'6:0',
                         u'5:9',
                         u'5:8',
                         u'5:7',
                         u'5:6',
                         u'5:5',
                         u'5:4',
                         u'5:3',
                         u'5:2',
                         u'5:10',
                         u'5:1',
                         u'5:0',
                         u'4:9',
                         u'4:8',
                         u'4:7',
                         u'4:6',
                         u'4:5',
                         u'4:4',
                         u'4:3',
                         u'4:2',
                         u'4:10',
                         u'4:1',
                         u'4:0',
                         u'3:9',
                         u'3:8',
                         u'3:7',
                         u'3:6',
                         u'3:5',
                         u'3:4',
                         u'3:3',
                         u'3:2',
                         u'3:10',
                         u'3:1',
                         u'3:0',
                         u'2:9',
                         u'2:8',
                         u'2:7',
                         u'2:6',
                         u'2:5',
                         u'2:4',
                         u'2:3',
                         u'2:2',
                         u'2:10',
                         u'2:1',
                         u'2:0',
                         u'1:9',
                         u'1:8',
                         u'1:7',
                         u'1:6',
                         u'1:5',
                         u'1:4',
                         u'1:3',
                         u'1:2',
                         u'1:10',
                         u'1:1',
                         u'1:0',
                         u'10:9',
                         u'10:8',
                         u'10:7',
                         u'10:6',
                         u'10:5',
                         u'10:4',
                         u'10:3',
                         u'10:2',
                         u'10:10',
                         u'10:1',
                         u'10:0',
                         u'0:9',
                         u'0:8',
                         u'0:7',
                         u'0:6',
                         u'0:5',
                         u'0:4',
                         u'0:3',
                         u'0:2',
                         u'0:10',
                         u'0:1',
                         u'0:0']]
#                         u'week_num',
#                         u'match_date']]
    
    df_temp.to_csv('../dataset/local/' + name + '.csv', encoding='utf-8') 
    
"""














