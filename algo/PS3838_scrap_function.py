#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 17:20:03 2018

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
from dateutil.relativedelta                                                    import relativedelta

from PS3838_support_function                                                   import encode_decode, optimisation, optimisation_2, optimisation_apply


# =============================================================================
# 
# =============================================================================
def date_ajustement(df, GMT_to_add):
    df                = df.apply(lambda x : datetime.strptime(x.replace('Nov','11'), '%Y %m %d%H:%M') if str(x)[5:8]=='Nov' else x)
    df                = df.apply(lambda x : datetime.strptime(x.replace('nov.','11'), '%Y %d %m%H:%M') if str(x)[8:12]=='nov.' else x)
    
    df                = df.apply(lambda x : datetime.strptime(x.replace('Dec','12'), '%Y %m %d%H:%M') if str(x)[5:8]=='Dec' else x)
    df                = df.apply(lambda x : datetime.strptime(x.replace('dec.','12'), '%Y %d %m%H:%M') if str(x)[8:12]=='dec.' else x)

    df                = df.apply(lambda x : datetime.strptime(x.replace('Jan','01'), '%Y %m %d%H:%M') if str(x)[5:8]=='Jan' else x)
    df                = df.apply(lambda x : datetime.strptime(x.replace('jan.','01'), '%Y %d %m%H:%M') if str(x)[8:12]=='jan.' else x)

    df                = df.apply(lambda x : datetime.strptime(x.replace('Feb','02'), '%Y %m %d%H:%M') if str(x)[5:8]=='Feb' else x)
    df                = df.apply(lambda x : datetime.strptime(x.replace('feb.','02'), '%Y %d %m%H:%M') if str(x)[8:12]=='feb.' else x)

    df                = df.apply(lambda x : datetime.strptime(x.replace('Mar','03'), '%Y %m %d%H:%M') if str(x)[5:8]=='Mar' else x)
    df                = df.apply(lambda x : datetime.strptime(x.replace('mar.','03'), '%Y %d %m%H:%M') if str(x)[8:12]=='mar.' else x)

    df                = df.apply(lambda x : datetime.strptime(x.replace('Apr','04'), '%Y %m %d%H:%M') if str(x)[5:8]=='Apr' else x)
    df                = df.apply(lambda x : datetime.strptime(x.replace('apr.','04'), '%Y %d %m%H:%M') if str(x)[8:12]=='apr.' else x)

    df                = df.apply(lambda x : datetime.strptime(x.replace('May','05'), '%Y %m %d%H:%M') if str(x)[5:8]=='May' else x)
    df                = df.apply(lambda x : datetime.strptime(x.replace('may.','05'), '%Y %d %m%H:%M') if str(x)[8:12]=='may.' else x)

    df                = df.apply(lambda x : datetime.strptime(x.replace('Jun','06'), '%Y %m %d%H:%M') if str(x)[5:8]=='Jun' else x)
    df                = df.apply(lambda x : datetime.strptime(x.replace('jun.','06'), '%Y %d %m%H:%M') if str(x)[8:12]=='jun.' else x)

    df                = df.apply(lambda x : datetime.strptime(x.replace('Jul','07'), '%Y %m %d%H:%M') if str(x)[5:8]=='Jul' else x)
    df                = df.apply(lambda x : datetime.strptime(x.replace('jul.','07'), '%Y %d %m%H:%M') if str(x)[8:12]=='jul.' else x)
    
    df                = df.apply(lambda x : str(x))
    df                = df.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S') + timedelta(hours=GMT_to_add))

    df                = df.apply(lambda x : x+ relativedelta(years=1) if (x.year==2018 and x.month<9) else x)

    return df
# =============================================================================
# 
# =============================================================================
def ps3838_scrap_result(GMT_to_add):
    df_parlay = pd.DataFrame.from_csv('../dataset/local/df_parlay.xls', encoding='utf-8')
    list_sport = df_parlay.sport.unique().tolist()
    list_sport = ','.join(list_sport)
    
    try:
        df_result       = pd.DataFrame.from_csv('../dataset/local/df_result.xls')
        dict_result     = df_result.to_dict(orient='index')
    except:
        df_result       = pd.DataFrame()
        dict_result     = {}
    
    os.system('node scrap_ps3838_results_standalone.js "' + str(list_sport) + '"')
    
    list_result             = glob('../dataset/local/result_mix_parlay*.*')
    list_result.sort()
    
    for result in list_result:
        soup                = BeautifulSoup(open(result), "html.parser")
        result_list         = soup.find('div', { "class" : "result"})
        match_list          = soup.find_all('tr')
        
        sport               = soup.find('th', { "colspan" : "5"}).text
#        print sport
        
        for match in match_list:
            teams = match.find_all('h6')
            if teams != []:
                if str(match).find('display:none') == -1:
                    match_date  = str(datetime.now().year) + ' ' + match.find('td', { "class" : "date"}).text
                    match_date  = datetime.strptime(match_date, '%Y %m/%d %H:%M') + timedelta(hours=GMT_to_add)
                    score       = match.find('td', { "class" : "period"}).text
                    team_home   = teams[0].text
                    team_away   = teams[1].text
                    match_name  = team_home + '_' + team_away + '_' + sport
                
                    team_home           = encode_decode(team_home)
                    team_away           = encode_decode(team_away)
    
                    dict_result.update({match_name:{
                                                'match_date' : match_date,
                                                'team_home'  : team_home,
                                                'team_away'  : team_away,
                                                'sport'      : sport,
                                                'score'      : score,
                                                }}) 
    
    dict_result_new = {}
    for k,v in dict_result.iteritems():
        encode_decode(k)
        dict_result_new.update({k:v}) 
        
    df_result               = pd.DataFrame.from_dict(dict_result_new, orient='index')
    df_result  = pd.DataFrame.from_dict(dict_result, orient='index')
    df_result.team_away = df_result.team_away.apply(lambda x : encode_decode(x))
    df_result.team_home = df_result.team_home.apply(lambda x : encode_decode(x))
    
    
    #df_result.reset_index(drop=False, inplace=True)
    #df_result['index']            = df_result['index'] + '_' + df_result.sport
    #df_result.set_index('index', inplace=True)
    
    #df_result.match_date                = df_result.match_date.apply(lambda x : datetime.strptime(x, '%Y %m/%d %H:%M'))
    df_result.score = df_result.score.apply(lambda x : x.strip())
    df_result = df_result[df_result.score.apply(lambda x : x.find('-') != -1)]
    df_result = df_result[df_result.score.apply(lambda x : x.split('-')[0] != '')]
    df_result['winner'] = df_result.score
    df_result.winner = df_result.winner.apply(lambda x : '0' if int(x.split('-')[0])==int(x.split('-')[1]) else '1' if int(x.split('-')[0])>int(x.split('-')[1]) else '2' if int(x.split('-')[0])<int(x.split('-')[1]) else 99)
    
    df_result.drop_duplicates(inplace=True)
    df_result.to_csv('../dataset/local/df_result.xls', encoding='utf-8')
    


# =============================================================================
# 
# =============================================================================
def ps3838_scrap_parlay():
    url_season_page         = 'https://www.ps3838.com/en/euro/sports/mix-parlay'
    save_season_page        = '../dataset/local/mix_parlay'
    os.system('node scrap_ps3838_parlay_standalone.js ' + url_season_page + ' ' + save_season_page)
    
    
    
    # =============================================================================
    # 
    # =============================================================================
    try:
        df_parlay = pd.DataFrame.from_csv('../dataset/local/df_parlay.xls')
        dict_odds = df_parlay.to_dict(orient='index')
    except:
        df_parlay = pd.DataFrame()
        dict_odds = {}
        
        
    list_parlay             = glob('../dataset/local/mix_parlay*.*')
    list_parlay.sort()
    
    
    for parlay in list_parlay:
        print parlay
        soup                = BeautifulSoup(open(parlay), "html.parser")
        money_line_list     = soup.find_all('div', { "class" : "OneXTwo_0"})
        if money_line_list != []:
            money_line_list     = money_line_list[0]
            
            ligue_list          = money_line_list.find_all('div', { "class" : "o_league"})
            for i, ligue in enumerate(ligue_list):
                money_line_ligue_list = money_line_list.find_all('table', { "class" : "o_table events"})[i]
                
                ### GMT        
                GMT                 = soup.find('span', { "id" : "current-time"}).text.strip()
                GMT_value           = GMT[GMT.find('GMT+')+4:-3]
                GMT_to_add          = int(GMT_value) - 1
                
                match_list          = []
                match_list          = money_line_ligue_list.find_all('tr', { "class" : "status_I"}) + money_line_ligue_list.find_all('tr', { "class" : "status_O"})
                
                sport               = parlay.split('_')[-1].split('.')[0]
                ###
                sport_filter        = soup.find('tr', { "id" : "sportFilter"})
                sport_filter_li     = sport_filter.find_all('li')
                for z, li in enumerate(sport_filter_li):
                    if str(li).find("selected") != -1:
                        sport_id            = z+1
    
                for match in match_list:
                    if match.find_all('td', { "class" : "o_A_draw "}) != []:
                        match_odd       = match.find('td', { "class" : "o_A_draw"})
                        team_home       = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        team_home_id    = match_odd.find('a')['id']
                        bet_1           = match_odd.find('span', { "class" : "o_right "}).text.strip()
                
                        bet_X           = 0
                        team_X_id       = 0
                        
                        match_odd       = match.find('td', { "class" : "o_B_draw"})
                        team_away       = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        team_away_id    = match_odd.find('a')['id']
                        bet_2           = match_odd.find('span', { "class" : "o_right "}).text.strip()            
                    else:
                        match_odd       = match.find('td', { "class" : "o_A "})
                        team_home       = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        team_home_id    = match_odd.find('a')['id']
                        bet_1           = match_odd.find('span', { "class" : "o_right "}).text.strip()
            
                        match_odd       = match.find('td', { "class" : "o_draw"})
                        _               = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        bet_X           = match_odd.find('span', { "class" : "o_right "}).text.strip()
                        team_X_id       = match_odd.find('a')['id']

                        match_odd       = match.find('td', { "class" : "o_B "})
                        team_away       = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        team_away_id    = match_odd.find('a')['id']
                        bet_2           = match_odd.find('span', { "class" : "o_right "}).text.strip()
                    match_date          = str(datetime.now().year) + ' ' + match.find('span', { "class" : "DateTime"}).text
                    match_name          = team_home + '_' + team_away + '_' + match_date
                    ligue_name          = ligue.text.strip()
    
                    team_home           = encode_decode(team_home)
                    team_away           = encode_decode(team_away)
                    match_name          = encode_decode(match_name)
    
                    dict_odds.update({match_name:{
                                                'match_date' : match_date,
                                                'team_home'  : team_home,
                                                'team_home_id'  : team_home_id,
                                                'team_away'  : team_away,
                                                'team_away_id'  : team_away_id,
                                                'team_X_id'  : team_X_id,
                                                'bet_1'      : bet_1,
                                                'bet_X'      : bet_X,
                                                'bet_2'      : bet_2,
                                                'sport'      : sport,
                                                'sport_id'      : sport_id,
                                                'ligue'      : ligue_name,
                                                }}) 
#                    print sport
    
    
    
    dict_odds_new = {}
    for k,v in dict_odds.iteritems():
        encode_decode(k)
        dict_odds_new.update({k:v}) 
        
    df_parlay               = pd.DataFrame.from_dict(dict_odds_new, orient='index')
    df_parlay.drop_duplicates(inplace=True)
    
    ###
    df_parlay.bet_1 = df_parlay.bet_1.astype(float)
    df_parlay.bet_2 = df_parlay.bet_2.astype(float)
    df_parlay['bet_diff']              = df_parlay.bet_1 - df_parlay.bet_2
    df_parlay['prediction']            = df_parlay.bet_diff.apply(lambda x : "1" if x<0 else "2")
    df_parlay['bet_diff']              = abs(df_parlay.bet_1 - df_parlay.bet_2)
    df_parlay['min_bet']               = df_parlay[['bet_1','bet_2']].min(axis=1)
    
    ###
    df_parlay.match_date  = date_ajustement(df_parlay.match_date, GMT_to_add)
    
    ###
    """
    df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('Nov','11'), '%Y %m %d%H:%M') if str(x)[5:8]=='Nov' else x)
    df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('nov.','11'), '%Y %d %m%H:%M') if str(x)[8:12]=='nov.' else x)
    
    df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('Dec','12'), '%Y %m %d%H:%M') if str(x)[5:8]=='Dec' else x)
    df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('dec.','12'), '%Y %d %m%H:%M') if str(x)[8:12]=='dec.' else x)
    """
    
    df_parlay.to_csv('../dataset/local/df_parlay.xls', encoding='utf-8')
    
    # =============================================================================
    # 
    # =============================================================================
    try:
        df_parlay = pd.DataFrame.from_csv('../dataset/local/df_parlay.xls')
        dict_odds = df_parlay.to_dict(orient='index')
    except:
        df_parlay = pd.DataFrame()
        dict_odds = {}
        
        
    list_parlay             = glob('../dataset/local/mix_parlay*.*')
    list_parlay.sort()
    
    
    for parlay in list_parlay:
        print parlay
        soup                = BeautifulSoup(open(parlay), "html.parser")
        money_line_list     = soup.find_all('div', { "class" : "OneXTwo_0"})
        if money_line_list != []:
            money_line_list     = money_line_list[0]
            
            ligue_list          = money_line_list.find_all('div', { "class" : "o_league"})
            for i, ligue in enumerate(ligue_list):
                money_line_ligue_list = money_line_list.find_all('table', { "class" : "o_table events"})[i]
                
                ### GMT        
                GMT                 = soup.find('span', { "id" : "current-time"}).text.strip()
                GMT_value           = GMT[GMT.find('GMT+')+4:-3]
                GMT_to_add          = int(GMT_value) - 1
                
                match_list          = []
                match_list          = money_line_ligue_list.find_all('tr', { "class" : "status_I"}) + money_line_ligue_list.find_all('tr', { "class" : "status_O"})
                
                sport               = parlay.split('_')[-1].split('.')[0]
                ###
                sport_filter        = soup.find('tr', { "id" : "sportFilter"})
                sport_filter_li     = sport_filter.find_all('li')
                for z, li in enumerate(sport_filter_li):
                    if str(li).find("selected") != -1:
                        sport_id            = z+1
    
                for match in match_list:
                    if match.find_all('td', { "class" : "o_A_draw "}) != []:
                        match_odd       = match.find('td', { "class" : "o_A_draw"})
                        team_home       = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        team_home_id    = match_odd.find('a')['id']
                        bet_1           = match_odd.find('span', { "class" : "o_right "}).text.strip()
                
                        bet_X           = 0
                        team_X_id       = 0
                        
                        match_odd       = match.find('td', { "class" : "o_B_draw"})
                        team_away       = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        team_away_id    = match_odd.find('a')['id']
                        bet_2           = match_odd.find('span', { "class" : "o_right "}).text.strip()            
                    else:
                        match_odd       = match.find('td', { "class" : "o_A "})
                        team_home       = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        team_home_id    = match_odd.find('a')['id']
                        bet_1           = match_odd.find('span', { "class" : "o_right "}).text.strip()
            
                        match_odd       = match.find('td', { "class" : "o_draw"})
                        _               = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        bet_X           = match_odd.find('span', { "class" : "o_right "}).text.strip()
                        team_X_id       = match_odd.find('a')['id']
                        
                        match_odd       = match.find('td', { "class" : "o_B "})
                        team_away       = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        team_away_id    = match_odd.find('a')['id']
                        bet_2           = match_odd.find('span', { "class" : "o_right "}).text.strip()
                    match_date          = str(datetime.now().year) + ' ' + match.find('span', { "class" : "DateTime"}).text
                    match_name          = team_home + '_' + team_away + '_' + match_date
                    ligue_name          = ligue.text.strip()
    
                    team_home           = encode_decode(team_home)
                    team_away           = encode_decode(team_away)
                    match_name          = encode_decode(match_name)
    
                    dict_odds.update({match_name:{
                                                'match_date' : match_date,
                                                'team_home'  : team_home,
                                                'team_home_id'  : team_home_id,
                                                'team_away'  : team_away,
                                                'team_away_id'  : team_away_id,
                                                'team_X_id'  : team_X_id,
                                                'bet_1'      : bet_1,
                                                'bet_X'      : bet_X,
                                                'bet_2'      : bet_2,
                                                'sport'      : sport,
                                                'sport_id'      : sport_id,
                                                'ligue'      : ligue_name,
                                                }}) 
#                    print sport
    
    
    
    dict_odds_new = {}
    for k,v in dict_odds.iteritems():
        encode_decode(k)
        dict_odds_new.update({k:v}) 
        
    df_parlay               = pd.DataFrame.from_dict(dict_odds_new, orient='index')
    df_parlay.drop_duplicates(inplace=True)
    
    ###
    df_parlay.bet_1 = df_parlay.bet_1.astype(float)
    df_parlay.bet_2 = df_parlay.bet_2.astype(float)
    df_parlay['bet_diff']              = df_parlay.bet_1 - df_parlay.bet_2
    df_parlay['prediction']            = df_parlay.bet_diff.apply(lambda x : "1" if x<0 else "2")
    df_parlay['bet_diff']              = abs(df_parlay.bet_1 - df_parlay.bet_2)
    df_parlay['min_bet']               = df_parlay[['bet_1','bet_2']].min(axis=1)
    
    df_parlay.match_date  = date_ajustement(df_parlay.match_date, GMT_to_add)
    ###
    """
    df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('Nov','11'), '%Y %m %d%H:%M') if str(x)[5:8]=='Nov' else x)
    df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('nov.','11'), '%Y %d %m%H:%M') if str(x)[8:12]=='nov.' else x)
    
    df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('Dec','12'), '%Y %m %d%H:%M') if str(x)[5:8]=='Dec' else x)
    df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('dec.','12'), '%Y %d %m%H:%M') if str(x)[8:12]=='dec.' else x)
    """    
    
    df_parlay.to_csv('../dataset/local/df_parlay.xls', encoding='utf-8')
    


# =============================================================================
# 
# =============================================================================
def ps3838_scrap_single():
    os.system('node scrap_ps3838_single_standalone.js')
    
    try:
        df_single = pd.DataFrame.from_csv('../dataset/local/df_single.xls')
        dict_odds = df_single.to_dict(orient='index')
    except:
        df_single = pd.DataFrame()
        dict_odds = {}
        
        
    list_single             = glob('../dataset/local/single*.html')
    list_single.sort()
    
    
    for single in list_single:
        print single
        soup                = BeautifulSoup(open(single), "html.parser")
    
        ### GMT        
        GMT                 = soup.find('span', { "id" : "current-time"}).text.strip()
        GMT_value           = GMT[GMT.find('GMT+')+4:-3]
        GMT_to_add          = int(GMT_value) - 1
        
        ###
        money_line_list      = soup.find_all('div', { "class" : "OneXTwo_0 "})
        
        
        if money_line_list != []:
            money_line_list     = money_line_list[0]
            
            ligue_list          = money_line_list.find_all('div', { "class" : "o_league"})
            for i, ligue in enumerate(ligue_list):
                money_line_ligue_list = money_line_list.find_all('table', { "class" : "o_table events"})[i]
                
                match_list          = []
                match_list          = money_line_ligue_list.find_all('tr', { "class" : "status_I"}) + money_line_ligue_list.find_all('tr', { "class" : "status_O"})
                
                sport               = single.split('_')[-1].split('.')[0]
    
                for match in match_list:
                    if match.find_all('td', { "class" : "o_A_draw "}) != []:
                        match_odd       = match.find('td', { "class" : "o_A_draw"})
                        team_home       = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        team_home_id    = match_odd.find('a')['id']
                        bet_1           = match_odd.find('span', { "class" : "o_right "}).text.strip()
                
                        bet_X           = 0
                        team_X_id       = 0
                        
                        match_odd       = match.find('td', { "class" : "o_B_draw"})
                        team_away       = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        team_away_id    = match_odd.find('a')['id']
                        bet_2           = match_odd.find('span', { "class" : "o_right "}).text.strip()            
                    else:
                        match_odd       = match.find('td', { "class" : "o_A "})
                        team_home       = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        team_home_id    = match_odd.find('a')['id']
                        bet_1           = match_odd.find('span', { "class" : "o_right "}).text.strip()
            
                        match_odd       = match.find('td', { "class" : "o_draw"})
                        _               = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        bet_X           = match_odd.find('span', { "class" : "o_right "}).text.strip()
                        team_X_id       = match_odd.find('a')['id']
                        
                        match_odd       = match.find('td', { "class" : "o_B "})
                        team_away       = match_odd.find('span', { "class" : "o_left"}).text.strip()
                        team_away_id    = match_odd.find('a')['id']
                        bet_2           = match_odd.find('span', { "class" : "o_right "}).text.strip()
                    match_date          = str(datetime.now().year) + ' ' + match.find('span', { "class" : "DateTime"}).text
                    match_name          = team_home + '_' + team_away + '_' + match_date
                    ligue_name          = ligue.text.strip()
    
                    team_home           = encode_decode(team_home)
                    team_away           = encode_decode(team_away)
                    match_name          = encode_decode(match_name)
    
                    dict_odds.update({match_name:{
                                                'match_date' : match_date,
                                                'team_home'  : team_home,
                                                'team_home_id'  : team_home_id,
                                                'team_away'  : team_away,
                                                'team_away_id'  : team_away_id,
                                                'team_X_id'  : team_X_id,
                                                'bet_1'      : bet_1,
                                                'bet_X'      : bet_X,
                                                'bet_2'      : bet_2,
                                                'sport'      : sport,
                                                'ligue'      : ligue_name,
                                                }}) 
#        print sport
    
                        
                    
    
    
    dict_odds_new = {}
    for k,v in dict_odds.iteritems():
        encode_decode(k)
        dict_odds_new.update({k:v}) 
        
    df_single               = pd.DataFrame.from_dict(dict_odds_new, orient='index')
    df_single.drop_duplicates(inplace=True)
    
    ###
    df_single.bet_1 = df_single.bet_1.astype(float)
    df_single.bet_2 = df_single.bet_2.astype(float)
    df_single['bet_diff']              = df_single.bet_1 - df_single.bet_2
    df_single['prediction']            = df_single.bet_diff.apply(lambda x : "1" if x<0 else "2")
    df_single['bet_diff']              = abs(df_single.bet_1 - df_single.bet_2)
    df_single['min_bet']               = df_single[['bet_1','bet_2']].min(axis=1)
    
    ###
    df_single.match_date  = date_ajustement(df_single.match_date, GMT_to_add)

    """
    ###
    df_single.match_date                = df_single.match_date.apply(lambda x : datetime.strptime(x.replace('Nov','11'), '%Y %m %d%H:%M') if str(x)[5:8]=='Nov' else x)
    df_single.match_date                = df_single.match_date.apply(lambda x : datetime.strptime(x.replace('nov.','11'), '%Y %d %m%H:%M') if str(x)[8:12]=='nov.' else x)
    
    df_single.match_date                = df_single.match_date.apply(lambda x : datetime.strptime(x.replace('Dec','12'), '%Y %m %d%H:%M') if str(x)[5:8]=='Dec' else x)
    df_single.match_date                = df_single.match_date.apply(lambda x : datetime.strptime(x.replace('dec.','12'), '%Y %d %m%H:%M') if str(x)[8:12]=='dec.' else x)
    """
    
    #### filter live
    #ee
    #df_single.match_date                = df_single.match_date.apply(lambda x : x if isinstance(x, basestring)!=True else 0)
    #df_single                           = df_single[df_single.match_date != 0]
    
    df_single.to_csv('../dataset/local/df_single.xls', encoding='utf-8')

    return GMT_to_add

    
