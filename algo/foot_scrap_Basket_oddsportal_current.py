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

import pandas             as pd
import numpy              as np

from bs4                  import BeautifulSoup
from glob                 import glob



# =============================================================================
# create folder structure
# =============================================================================
os.system('mkdir -p ' + '../dataset/local/oddsportal/match')


# =============================================================================
# 
# =============================================================================
#df_NHL_scores               = pd.read_csv('../dataset/local/df_NHL_scores_espn.csv', index_col=0, encoding='utf-8')
#df_NHL_scores.dropna(subset=['date_match'], inplace=True)
#df_NHL_scores['date_match'] = pd.to_datetime(df_NHL_scores.date_match)
#df_NHL_scores.dropna(subset=['match_name'],inplace=True)
#df_NHL_scores.reset_index(drop=True, inplace=True)
#df_NHL_scores.sort_values(['date_match'], inplace=True, ascending=True)

this_year  = 2018
list_year  = [2018]
list_ligue = [
                ['usa', 'nba'],
                ['spain', 'acb'],
#                ['france', 'ligue-1'],
#                ['england', 'premier-league'],
#                ['england', 'efl-cup'],
#                ['cyprus', 'first-division'],
#                ['bulgaria', 'parva-liga'],
#                ['italy', 'serie-a'],
#                ['portugal','primeira-liga'],
#                ['belgium','jupiler-league'],
#                ['croatia','1-hnl'],
#                ['argentina','superliga'],
#                ['switzerland','super-league'],
#                ['poland','ekstraklasa'],
              ]

for item in list_ligue:
    pays    = item[0]
    ligue   = item[1]
    
    
    # =============================================================================
    # Recover link to each match for each season in all pages of website
    # =============================================================================
    ### previous year
    for year in list_year:
        
        if year == this_year:
            break
        
        season                          = str(year) + '-' + str(year+1)
        url_season                      = 'https://www.oddsportal.com/basketball/' + pays + '/' + ligue + '-' + season + '/results/#/page/'
        for page_num in range(35):
            url_season_page             = url_season + str(page_num + 1)
            save_season_page            = '../dataset/local/oddsportal/oddsportal_' + pays + '_' + ligue + '_' + season + '_' + str(page_num+1) + '.html'
            print url_season_page
            if os.path.isfile(save_season_page) != True:
                os.system('node scrap_odds_first_standalone.js ' + url_season_page + ' ' + save_season_page)
                time.sleep(0.7)
                if os.path.getsize(save_season_page) < 179900:
                    break
            
    
    ### current season
    year                            = this_year
    season                          = str(year) + '-' + str(year+1)
    url_season                      = 'https://www.oddsportal.com/basketball/' + pays + '/' + ligue + '/results/#/page/'
    for page_num in range(35):
        url_season_page             = url_season + str(page_num + 1)
        save_season_page            = '../dataset/local/oddsportal/oddsportal_' + pays + '_' + ligue + '_' + season + '_' + str(page_num+1) + '.html'
        print url_season_page
        os.system('node scrap_odds_first_standalone.js ' + url_season_page + ' ' + save_season_page)
        time.sleep(0.3)
        if os.path.getsize(save_season_page) < 179900:
            break
       
    year                            = this_year
    ### Next matchs
    season                          = str(year) + '-' + str(year+1)
    url_season_page                 = 'https://www.oddsportal.com/basketball/' + pays + '/' + ligue + '/'
    save_season_page                = '../dataset/local/oddsportal/oddsportal_' + pays + '_' + ligue + '_next_match.html'
    print url_season_page
    os.system('node scrap_odds_first_standalone.js ' + url_season_page + ' ' + save_season_page)
    
    
    #%% =============================================================================
    # 
    # =============================================================================
    df_oddsportal           = pd.DataFrame()
    dict_odds               = {}
    
    for year in list_year:
        season                          = str(year) + '-' + str(year+1)
        load_season_page                = '../dataset/local/oddsportal/oddsportal_' + pays + '_' + ligue + '_' + season + '*'
        list_page_season                = glob(load_season_page)
        list_page_season.sort()
        for page in list_page_season:
            print page
            soup                        = BeautifulSoup(open(page), "html.parser")
            page_num                    = page.split('_')[-1].split('.')[0]
            match_list                  = soup.find_all('tr', { "class" : "deactivate"}) + soup.find_all('tr', { "class" : "odd deactivate"})
            
            for match in match_list:
                try:
                    match_name              = match.find('td', { "class" : "name table-participant"}).text
                    match_date              = str(match.find_all('td')[0]).split('"')[1].split('t')[-1].split('-')[0]
                    team_home               = match_name.split('-')[0].strip()
                    team_away               = match_name.split('-')[1].strip()
                    bet_1                   = float(match.find_all('td', { "class" : "odds-nowrp"})[0].text)
#                    bet_X                   = float(match.find_all('td', { "class" : "odds-nowrp"})[1].text)
                    bet_2                   = float(match.find_all('td', { "class" : "odds-nowrp"})[1].text)
                    score                   = match.find('td', { "class" : "center bold table-odds table-score"}).text
                    try:
                        score_home              = score.split(':')[0]
                        score_away              = score.split(':')[1].split(' ')[0]
                    except Exception,e :
                        score_home              = "999"
                        score_away              = "999"
                        print e                    
        
                    if score_home > score_away:
                        result      = 1
                        result_bet  = bet_1 
                    if score_home < score_away:
                        result      = 2     
                        result_bet  = bet_2 
                    if score_home == score_away:
                        result      = 'X'
                        result_bet  = bet_X 
                        
                    dict_odds.update({match['xeid']+'_'+str(year):{
                                        'match_name' : match_name,
                                        'match_id'   : match['xeid'],
                                        'match_date' : match_date,
                                        'team_home'  : team_home,
                                        'team_away'  : team_away,
                                        'bet_1'      : bet_1,
                                        'bet_X'      : 0,
                                        'bet_2'      : bet_2,
                                        'result'     : result,
                                        'result_bet' : result_bet,
                                        'score'      : score,
                                        'score_home' : score_home,
                                        'score_away' : score_away,
                                        'ligue'      : ligue,
                                        'pays'       : pays,
                                        }}) 

                except Exception,e :
                    print e
               
        
        df_temp         = pd.DataFrame.from_dict(dict_odds, orient='index')
    
        df_temp_final = pd.concat((df_oddsportal,df_temp))
        
    
    # =============================================================================
    # 
    # =============================================================================
    
    df_temp_final = df_temp_final[[
                                u'match_id', 
                                u'match_date',
                                u'bet_1', 
                                u'bet_X', 
                                u'bet_2', 
                                u'result',
                                u'result_bet',
    
                                u'score',
                                u'score_home', 
                                u'score_away', 

                                u'pays', 
                                u'ligue', 
                                u'match_name',     
                                u'team_home', 
                                u'team_away',
                                ]]
    
    df_temp_final.to_csv('../dataset/local/df_oddsportal_' + pays + '_' + ligue + '.csv', encoding='utf-8')
