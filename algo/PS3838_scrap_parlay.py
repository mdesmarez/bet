#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 15:03:27 2018

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
                df_sport = df_sport[(df_sport.match_date < datetime.now()+timedelta(hours=20)) & (df_sport.match_date > datetime.now())]
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
    bet_max             = 1.03
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


def encode_decode(k):
    try:
        k = k.decode('utf-8')
        k = k.encode('utf-8')
    except:
        k = k.encode('utf-8')
    k = k.replace('\xe2\x80\x8e','')
    return k


# =============================================================================
# CLEAN
# =============================================================================
list_parlay             = glob('../dataset/local/mix_parlay*.*')
for parlay in list_parlay:
    os.system('rm ' + parlay)

list_parlay             = glob('../dataset/local/single*.html')
for parlay in list_parlay:
    os.system('rm ' + parlay)

#%%
# =============================================================================
# 
# =============================================================================

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
                                            'bet_1'      : bet_1,
                                            'bet_X'      : bet_X,
                                            'bet_2'      : bet_2,
                                            'sport'      : sport,
                                            'ligue'      : ligue_name,
                                            }}) 
    print sport

                    
                


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
df_single.match_date                = df_single.match_date.apply(lambda x : datetime.strptime(x.replace('Nov','11'), '%Y %m %d%H:%M') if str(x)[5:8]=='Nov' else x)
df_single.match_date                = df_single.match_date.apply(lambda x : datetime.strptime(x.replace('nov.','11'), '%Y %d %m%H:%M') if str(x)[8:12]=='nov.' else x)

df_single.match_date                = df_single.match_date.apply(lambda x : datetime.strptime(x.replace('Dec','12'), '%Y %m %d%H:%M') if str(x)[5:8]=='Dec' else x)
df_single.match_date                = df_single.match_date.apply(lambda x : datetime.strptime(x.replace('dec.','12'), '%Y %d %m%H:%M') if str(x)[8:12]=='dec.' else x)

#### filter live
#ee
#df_single.match_date                = df_single.match_date.apply(lambda x : x if isinstance(x, basestring)!=True else 0)
#df_single                           = df_single[df_single.match_date != 0]

df_single.to_csv('../dataset/local/df_single.xls', encoding='utf-8')

#%%
# =============================================================================
# SCRAP
# =============================================================================


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
                                            'bet_1'      : bet_1,
                                            'bet_X'      : bet_X,
                                            'bet_2'      : bet_2,
                                            'sport'      : sport,
                                            'sport_id'      : sport_id,
                                            'ligue'      : ligue_name,
                                            }}) 
                print sport



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
df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('Nov','11'), '%Y %m %d%H:%M') if str(x)[5:8]=='Nov' else x)
df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('nov.','11'), '%Y %d %m%H:%M') if str(x)[8:12]=='nov.' else x)

df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('Dec','12'), '%Y %m %d%H:%M') if str(x)[5:8]=='Dec' else x)
df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('dec.','12'), '%Y %d %m%H:%M') if str(x)[8:12]=='dec.' else x)


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
                                            'bet_1'      : bet_1,
                                            'bet_X'      : bet_X,
                                            'bet_2'      : bet_2,
                                            'sport'      : sport,
                                            'sport_id'      : sport_id,
                                            'ligue'      : ligue_name,
                                            }}) 
                print sport



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
df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('Nov','11'), '%Y %m %d%H:%M') if str(x)[5:8]=='Nov' else x)
df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('nov.','11'), '%Y %d %m%H:%M') if str(x)[8:12]=='nov.' else x)

df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('Dec','12'), '%Y %m %d%H:%M') if str(x)[5:8]=='Dec' else x)
df_parlay.match_date                = df_parlay.match_date.apply(lambda x : datetime.strptime(x.replace('dec.','12'), '%Y %d %m%H:%M') if str(x)[8:12]=='dec.' else x)


df_parlay.to_csv('../dataset/local/df_parlay.xls', encoding='utf-8')

#%%
# =============================================================================
# 
# =============================================================================
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
    print sport
    
    for match in match_list:
        teams = match.find_all('h6')
        if teams != []:
            if str(match).find('display:none') == -1:
                match_date  = str(datetime.now().year) + ' ' + match.find('td', { "class" : "date"}).text
                match_date  = datetime.strptime(match_date, '%Y %m/%d %H:%M')
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




#%%
# =============================================================================
# 
# =============================================================================


### 2 bets
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
    
    
### 3 bets
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

### 5 bets
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
    
### 7 bets
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
    
### 10 bets
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
    
    
    
df_parlay = pd.DataFrame.from_csv('../dataset/local/df_parlay.xls', encoding='utf-8')
df_parlay.team_home = df_parlay.team_home.apply(lambda x : encode_decode(x))
df_result = pd.DataFrame.from_csv('../dataset/local/df_result.xls', encoding='utf-8')

df_single = pd.DataFrame.from_csv('../dataset/local/df_single.xls', encoding='utf-8')
df_single.sport = df_single.sport.apply(lambda x : x.lower().replace('-',' '))
df_result_single = df_result.copy()
df_result_single.sport = df_result_single.sport.apply(lambda x : x.lower().replace('-',' '))

###
df_bet_result_2 = pd.merge(df_bet_2, df_result, how='inner', on=['match_date','sport','team_home'])
df_bet_result_2['prediction'] = 2
df_bet_result_2['prediction'][df_bet_result_2.team_home == df_bet_result_2.team_to_bet] = 1
df_bet_result_2['good_pred']  = 0
df_bet_result_2['good_pred'][df_bet_result_2['prediction'] == df_bet_result_2['winner']] = 1

df_bet_result = pd.merge(df_bet, df_result, how='inner', on=['match_date','sport','team_home'])
df_bet_result['prediction'] = 2
df_bet_result['prediction'][df_bet_result.team_home == df_bet_result.team_to_bet] = 1
df_bet_result['good_pred']  = 0
df_bet_result['good_pred'][df_bet_result['prediction'] == df_bet_result['winner']] = 1

df_bet_result_5 = pd.merge(df_bet_5, df_result, how='inner', on=['match_date','sport','team_home'])
df_bet_result_5['prediction'] = 2
df_bet_result_5['prediction'][df_bet_result_5.team_home == df_bet_result_5.team_to_bet] = 1
df_bet_result_5['good_pred']  = 0
df_bet_result_5['good_pred'][df_bet_result_5['prediction'] == df_bet_result_5['winner']] = 1

df_bet_result_7 = pd.merge(df_bet_7, df_result, how='inner', on=['match_date','sport','team_home'])
df_bet_result_7['prediction'] = 2
df_bet_result_7['prediction'][df_bet_result_7.team_home == df_bet_result_7.team_to_bet] = 1
df_bet_result_7['good_pred']  = 0
df_bet_result_7['good_pred'][df_bet_result_7['prediction'] == df_bet_result_7['winner']] = 1

df_bet_result_10 = pd.merge(df_bet_10, df_result, how='inner', on=['match_date','sport','team_home'])
df_bet_result_10['prediction'] = 2
df_bet_result_10['prediction'][df_bet_result_10.team_home == df_bet_result_10.team_to_bet] = 1
df_bet_result_10['good_pred']  = 0
df_bet_result_10['good_pred'][df_bet_result_10['prediction'] == df_bet_result_10['winner']] = 1



###
df_merge                           = pd.merge(df_parlay, df_result, how='inner', on=['match_date','sport','team_home'])
df_merge = df_merge[['match_date','sport','ligue','bet_1','bet_2','bet_X','bet_diff','min_bet','winner','prediction','score']]
df_merge['good_pred']                          = 0
df_merge.good_pred[df_merge.prediction == df_merge.winner] = 1
df_merge['bad_pred']                           = 0
df_merge.bad_pred[df_merge.prediction != df_merge.winner]  = 1
df_merge.match_date                = df_merge.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

df_merge_single                           = pd.merge(df_single, df_result_single, how='inner', on=['match_date','sport','team_home'])
df_merge_single = df_merge_single[['match_date','sport','ligue','bet_1','bet_2','bet_X','bet_diff','min_bet','winner','prediction']]
df_merge_single['good_pred']                          = 0
df_merge_single.good_pred[df_merge_single.prediction == df_merge_single.winner] = 1
df_merge_single['bad_pred']                           = 0
df_merge_single.bad_pred[df_merge_single.prediction != df_merge_single.winner]  = 1
df_merge_single.match_date                = df_merge_single.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))



###
number_bet  = 10

list_sport = df_merge.sport.unique().tolist()
dict_parameter_sport = {}
for item in list_sport:
    print '\n' + item
    exec('df_merge_' + item.replace(' ','_') + ' = df_merge[df_merge.sport == "' + item + '"]')
    exec('df_temp = df_merge_' + item.replace(' ','_'))
    dict_temp = optimisation_2(df_temp)
    dict_parameter_sport.update(dict_temp)
df_parlay_filter = optimisation_apply(df_parlay, dict_parameter_sport)
df_parlay_filter.drop_duplicates(subset=['match_date','team_home'], inplace=True)

###
#df_parlay_filter = df_parlay_filter[df_parlay_filter.sport != 'Hockey']

###
print '*****************************'
print str(datetime.now())
df_parlay_filter.sort_values('bet_diff', ascending=False, inplace=True)
print 'df_parlay_filter : ', len(df_parlay_filter)
print '*****************************'

###
df_parlay_filter['team_to_bet']     = df_parlay_filter['team_home']
df_parlay_filter['team_to_bet_id']  = df_parlay_filter['team_home_id']
df_parlay_filter['team_to_bet'][df_parlay_filter.bet_1 > df_parlay_filter.bet_2] = df_parlay_filter['team_away'][df_parlay_filter.bet_1 > df_parlay_filter.bet_2]
df_parlay_filter['team_to_bet_id'][df_parlay_filter.bet_1 > df_parlay_filter.bet_2] = df_parlay_filter['team_away_id'][df_parlay_filter.bet_1 > df_parlay_filter.bet_2]


df_parlay_filter.reset_index(drop=False, inplace = True)
df_parlay_filter.sort_values('match_date', ascending=True, inplace=True)
#df_parlay_filter.sort_values('min_bet', ascending=True, inplace=True)
#df_parlay_filter.sort_values('min_bet', ascending=False, inplace=True)

df_betting = df_parlay_filter[['match_date','sport','ligue','index','team_to_bet','min_bet','bet_diff','team_to_bet_id','team_home']]
df_betting = df_betting.iloc[0:number_bet]

print '*****************************'
print 'df_betting : ', len(df_betting)
for i in range(len(df_betting)):
    if i == 0:
        bet_parlay = df_betting.min_bet.iloc[i]
    if i > 0:
        bet_parlay = bet_parlay*df_betting.min_bet.iloc[i]
print 'bet_parlay : ', bet_parlay
print '*****************************'



# =============================================================================
# 
# =============================================================================
###
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


###
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


###
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


###
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


###
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
    
print('******** RESULT SIMULATION **********')
print 'Number Good pred : ', len(df_bet_result)
print 'Number Bad pred  : ', len(df_bet_result[df_bet_result.good_pred == 0])
print round(df_bet_result.good_pred.sum()/float(len(df_bet_result))*100,2), '%'
print('*************************************')

#%%
# =============================================================================
# PLACE ORDER
# =============================================================================
ee
team_to_bet_id = str(df_betting.team_to_bet_id.tolist())[1:-1].replace('u','').replace("'","").replace(' ','')
sport_to_bet   = str(df_betting.sport.tolist())[1:-1].replace('u','').replace("'","")
os.system('node scrap_ps3838_place_bet_standalone.js "' + team_to_bet_id + '" "' + sport_to_bet + '"')
date_bet = datetime.now()
date_bet_string = str(date_bet.hour).zfill(2) + ':' + str(date_bet.minute).zfill(2) + '_' + str(date_bet.day) + '_' + str(date_bet.month) + '_' + str(date_bet.year)
df_betting.to_csv('../dataset/local/df_betting_' + date_bet_string + '.xls', encoding='utf-8')


#%%
# =============================================================================
# ANALYSIS RESULTS
# =============================================================================

mise = 10.0


###
print('1 BY 1')
result = 0
cave = 0
for item in range(len(df_bet_result)):
    cave = cave + mise
    if df_bet_result.good_pred.iloc[item] == 1:
        result = result+(df_bet_result.min_bet.iloc[item]+0.03-1)*mise
    else:
        print 'lose'
        result = result - mise
print 'cave     : ', int(cave),' €'
print 'gain pur : ', int(result),' €'
print 'ROI cave : ', round(result/float(cave)*100,2), '%'
print round(result/mise,2)*100,"%"
print ''

###
print('2 BY 2')
result = 0
cave = 0
list_bet_id = df_bet_result_2.bet_num.unique().tolist()
for id in list_bet_id:
    bet_parlay = 1
    cave = cave + mise
    df_bet_result_2_id = df_bet_result_2[df_bet_result_2.bet_num == id]
    if df_bet_result_2_id.good_pred.sum() == len(df_bet_result_2_id):
        for item in range(len(df_bet_result_2_id)):
            bet_parlay = bet_parlay*df_bet_result_2_id.min_bet.iloc[item]
#            print bet_parlay, (bet_parlay-1)*mise
        result = result  + (bet_parlay-1)*mise
    else:
        print 'lose'
        result = result - mise
print 'cave     : ', int(cave),' €'
print 'gain pur : ', int(result),' €'
#print 'ROI cave : ', round(result/float(cave)*100,2), '%'
print round(result/mise,2)*100,"%"
print ''


###
print('3 BY 3')
result = 0
cave = 0
list_bet_id = df_bet_result.bet_num.unique().tolist()
for id in list_bet_id:
    bet_parlay = 1
    cave = cave + mise
    df_bet_result_id = df_bet_result[df_bet_result.bet_num == id]
    if df_bet_result_id.good_pred.sum() == len(df_bet_result_id):
        for item in range(len(df_bet_result_id)):
            bet_parlay = bet_parlay*df_bet_result_id.min_bet.iloc[item]
#            print bet_parlay, (bet_parlay-1)*mise
        result = result  + (bet_parlay-1)*mise
    else:
        print 'lose'
        result = result - mise
print 'cave     : ', int(cave),' €'
print 'gain pur : ', int(result),' €'
print 'ROI cave : ', round(result/float(cave)*100,2), '%'
print round(result/mise,2)*100,"%"
print ''


###
print('5 BY 5')
result = 0
cave = 0
list_bet_id = df_bet_result_5.bet_num.unique().tolist()
for id in list_bet_id:
    bet_parlay = 1
    cave = cave + mise
    df_bet_result_5_id = df_bet_result_5[df_bet_result_5.bet_num == id]
    if df_bet_result_5_id.good_pred.sum() == len(df_bet_result_5_id):
        for item in range(len(df_bet_result_5_id)):
            bet_parlay = bet_parlay*df_bet_result_5_id.min_bet.iloc[item]
#            print bet_parlay, (bet_parlay-1)*mise
        result = result  + (bet_parlay-1)*mise
    else:
        print 'lose'
        result = result - mise
print 'cave     : ', int(cave),' €'
print 'gain pur : ', int(result),' €'
#print 'ROI cave : ', round(result/float(cave)*100,2), '%'
print round(result/mise,2)*100,"%"
print ''


###
print('7 BY 7')
result = 0
cave = 0
list_bet_id = df_bet_result_7.bet_num.unique().tolist()
for id in list_bet_id:
    bet_parlay = 1
    cave = cave + mise
    df_bet_result_7_id = df_bet_result_7[df_bet_result_7.bet_num == id]
    if df_bet_result_7_id.good_pred.sum() == len(df_bet_result_7_id):
        for item in range(len(df_bet_result_7_id)):
            bet_parlay = bet_parlay*df_bet_result_7_id.min_bet.iloc[item]
#            print bet_parlay, (bet_parlay-1)*mise
        result = result  + (bet_parlay-1)*mise
    else:
        print 'lose'
        result = result - mise
print 'cave     : ', int(cave),' €'
print 'gain pur : ', int(result),' €'
#print 'ROI cave : ', round(result/float(cave)*100,2), '%'
print round(result/mise,2)*100,"%"
print ''



###
print('10 BY 10')
result = 0
cave = 0
list_bet_id = df_bet_result_10.bet_num.unique().tolist()
for id in list_bet_id:
    bet_parlay = 1
    cave = cave + mise
    df_bet_result_10_id = df_bet_result_10[df_bet_result_10.bet_num == id]
    if df_bet_result_10_id.good_pred.sum() == len(df_bet_result_10_id):
        for item in range(len(df_bet_result_10_id)):
            bet_parlay = bet_parlay*df_bet_result_10_id.min_bet.iloc[item]
#            print bet_parlay, (bet_parlay-1)*mise
        result = result  + (bet_parlay-1)*mise
    else:
        print 'lose'
        result = result - mise
print 'cave     : ', int(cave),' €'
print 'gain pur : ', int(result),' €'
#print 'ROI cave : ', round(result/float(cave)*100,2), '%'
print round(result/mise,2)*100,"%"
print ''


df_bet_result[df_bet_result.good_pred == 1].min_bet.mean()
df_bet.sort_values('match_date', inplace=True)
plt.plot(df_bet['match_date'], df_bet['min_bet'])
plt.xticks(rotation='vertical')


