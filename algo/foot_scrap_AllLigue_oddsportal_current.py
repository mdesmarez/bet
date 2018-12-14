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

import pandas             as pd
import numpy              as np

from bs4                  import BeautifulSoup
from glob                 import glob



# =============================================================================
# create folder structure
# =============================================================================


# =============================================================================
# 
# =============================================================================
#df_NHL_scores               = pd.read_csv('../dataset/local/df_NHL_scores_espn.csv', index_col=0, encoding='utf-8')
#df_NHL_scores.dropna(subset=['date_match'], inplace=True)
#df_NHL_scores['date_match'] = pd.to_datetime(df_NHL_scores.date_match)
#df_NHL_scores.dropna(subset=['match_name'],inplace=True)
#df_NHL_scores.reset_index(drop=True, inplace=True)
#df_NHL_scores.sort_values(['date_match'], inplace=True, ascending=True)

process_scrap                   = 1
process_scrap_next_match        = 0
process_generate                = 1 

this_year                       = 2018
list_year                       = [2016, 2017, 2018]
#list_year  = [2016, 2017, 2018]

list_ligue = [
                [u'handball', u'france', u'lidl-starligue'],
                [u'handball', u'germany', u'bundesliga'],
                [u'handball', u'switzerland', u'nla'],
                [u'handball', u'spain', u'liga-asobal'],
                [u'handball', u'portugal', u'andebol-1'],
                [u'handball', u'russia', u'superleague'],
                [u'handball', u'denmark', u'herre-handbold-ligaen'],
                [u'handball', u'norway', u'nm-cup'],
                

                [u'handball', u'sweden', u'handbollsligan'],


                [u'baseball', u'usa', u'handbollsligan'],




                

                [u'basketball', u'spain', u'acb'],
                [u'basketball', u'italy', u'lega-a'],
                [u'basketball', u'usa', u'nba'],
                [u'basketball', u'germany', u'bbl'],
                [u'basketball', u'russia', u'vtb-united-league'],                
                [u'basketball', u'finland', u'korisliiga'],

                
                [u'volleyball', u'italy', u'serie-a1'],
                [u'volleyball', u'brazil', u'superliga-women'],


                
        
                [u'soccer', u'france', u'ligue-1'],
                [u'soccer', u'france', u'ligue-2'],
                
                [u'soccer', u'belgium', u'jupiler-league'],
                [u'soccer', u'belgium', u'proximus-league'],
                
                [u'soccer', u'portugal', u'primeira-liga'],
                [u'soccer', u'portugal', u'segunda-liga'],

                [u'soccer', u'germany', u'bundesliga'],
                
                [u'soccer', u'netherlands', u'eredivisie'],
                
                [u'soccer', u'spain', u'laliga'],
                
                [u'soccer', u'england', u'premier-league'],
                [u'soccer', u'england', u'efl-cup'],
                [u'soccer', u'cyprus', u'first-division'],
                [u'soccer', u'bulgaria', u'parva-liga'],
                [u'soccer', u'italy', u'serie-a'],
                
                [u'soccer', u'croatia', u'1-hnl'],
                [u'soccer', u'argentina', u'superliga'],
                [u'soccer', u'switzerland', u'super-league'],
                [u'soccer', u'poland', u'ekstraklasa'],
                
                [u'soccer', u'algeria', u'ligue-1'],
                [u'soccer', u'czech-republic', u'1-liga'],
                [u'soccer', u'luxembourg', u'national-division'],
                

                [u'soccer', u'serbia', u'prva-liga'],
                [u'soccer', u'scotland', u'premiership'],

                
              ]


# =============================================================================
# 
# =============================================================================
try:
    df_all              = pd.read_csv('../dataset/local/df_ALL.xls', index_col=0, encoding='utf-8')
    df_all.drop_duplicates('match_id', inplace=True)
except:
    df_all = pd.DataFrame()
    

list_ligue_already  = df_all.groupby(['sport','pays','ligue']).mean().index.tolist()

list_ligue          = [str(item) for item in list_ligue]
list_ligue_already  = [str(list(item)) for item in list_ligue_already]

list_ligue_diff     = list(set(list_ligue)-set(list_ligue_already))

list_ligue_diff     = [ast.literal_eval(item) for item in list_ligue_diff]

    
# =============================================================================
# 
# =============================================================================
df_oddsportal           = pd.DataFrame()
dict_odds               = {}
        
for item in list_ligue_diff:
    sport   = item[0]
    pays    = item[1]
    ligue   = item[2]
    
    os.system('mkdir -p ' + '../dataset/local/' + sport + '/oddsportal/match')
    
    # =============================================================================
    # Recover link to each match for each season in all pages of website
    # =============================================================================
    if process_scrap == 1:
        ### previous year
        for year in list_year:
            
            if year == this_year:
                break
            
            season                          = str(year) + '-' + str(year+1)
            url_season                      = 'https://www.oddsportal.com/' + sport + '/' + pays + '/' + ligue + '-' + season + '/results/#/page/'
            for page_num in range(35):
                url_season_page             = url_season + str(page_num + 1)
                save_season_page            = '../dataset/local/' + sport + '/oddsportal/oddsportal_' + pays + '_' + ligue + '_' + season + '_' + str(page_num+1) + '.html'
                print url_season_page
                if os.path.isfile(save_season_page) != True:
                    os.system('node scrap_odds_first_standalone.js ' + url_season_page + ' ' + save_season_page)
                    time.sleep(0.3)
                    if os.path.getsize(save_season_page) < 80000:
                        os.system('rm ' + save_season_page)
                        break
                
                    if page_num > 5:
                        soup                        = BeautifulSoup(open(save_season_page), "html.parser")
                        match_list                  = soup.find_all('tr', { "class" : "deactivate"}) + soup.find_all('tr', { "class" : "odd deactivate"})
                        if len(match_list) == 0:
                            os.system('rm ' + save_season_page)
                            break
            
            
        ### current season
        year                            = this_year
        season                          = str(year) + '-' + str(year+1)
        url_season                      = 'https://www.oddsportal.com/' + sport + '/' + pays + '/' + ligue + '/results/#/page/'
        for page_num in range(35):
            url_season_page             = url_season + str(page_num + 1)
            save_season_page            = '../dataset/local/' + sport + '/oddsportal/oddsportal_' + pays + '_' + ligue + '_' + season + '_' + str(page_num+1) + '.html'
            print url_season_page
            os.system('node scrap_odds_first_standalone.js ' + url_season_page + ' ' + save_season_page)
            time.sleep(0.3)
    
            soup                        = BeautifulSoup(open(save_season_page), "html.parser")
            match_list                  = soup.find_all('tr', { "class" : "deactivate"}) + soup.find_all('tr', { "class" : "odd deactivate"})
            if len(match_list) == 0:
                os.system('rm ' + save_season_page)
                break
            
    if process_scrap_next_match == 1:
        year                            = this_year
        ### Next matchs
        season                          = str(year) + '-' + str(year+1)
        url_season_page                 = 'https://www.oddsportal.com/' + sport + '/' + pays + '/' + ligue + '/'
        save_season_page                = '../dataset/local/' + sport + '/oddsportal/oddsportal_' + pays + '_' + ligue + '_next_match.html'
        print url_season_page
        os.system('node scrap_odds_first_standalone.js ' + url_season_page + ' ' + save_season_page)
    
    
        
    #%% =============================================================================
    # 
    # =============================================================================
    if process_generate == 1:
        
        for year in list_year:
            print 'season'
            season                          = str(year) + '-' + str(year+1)
            print 'season 1'
            load_season_page                = '../dataset/local/' + sport + '/oddsportal/oddsportal_' + pays + '_' + ligue + '_' + season + '*'
            print 'season 2'
            list_page_season                = glob(load_season_page)
            print 'season 3'
            list_page_season.sort()
            print 'season 4'
            for page in list_page_season:
                print page
                soup                        = BeautifulSoup(open(page), "html.parser")
                page_num                    = page.split('_')[-1].split('.')[0]
                match_list                  = soup.find_all('tr', { "class" : "deactivate"}) + soup.find_all('tr', { "class" : "odd deactivate"})
                print 'page 2'

                for match in match_list:
                    print 'match'
                    try:
                        match_name              = match.find('td', { "class" : "name table-participant"}).text
                        match_date              = str(match.find_all('td')[0]).split('"')[1].split('t')[-1].split('-')[0]
                        team_home               = match_name.split('-')[0].strip()
                        team_away               = match_name.split('-')[1].strip()
                        if sport == 'basketball':
                            bet_1                   = float(match.find_all('td', { "class" : "odds-nowrp"})[0].text)
                            bet_X                   = 0
                            bet_2                   = float(match.find_all('td', { "class" : "odds-nowrp"})[1].text) 
                        else:
                            bet_1                   = float(match.find_all('td', { "class" : "odds-nowrp"})[0].text)
                            bet_X                   = float(match.find_all('td', { "class" : "odds-nowrp"})[1].text)
                            bet_2                   = float(match.find_all('td', { "class" : "odds-nowrp"})[2].text)
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
                                            'bet_X'      : bet_X,
                                            'bet_2'      : bet_2,
                                            'result'     : result,
                                            'result_bet' : result_bet,
                                            'score'      : score,
                                            'score_home' : score_home,
                                            'score_away' : score_away,
                                            'ligue'      : ligue,
                                            'pays'       : pays,
                                            'sport'      : sport,
                                            }}) 
                    except Exception,e :
                        print e
                        
        df_temp         = pd.DataFrame.from_dict(dict_odds, orient='index')
    
        df_temp_final = pd.concat((df_oddsportal,df_temp))
            
        
        # =============================================================================
        # 
        # =============================================================================
        
        print'ee'
        try:
            df_temp_final = df_temp_final[[
                                        u'sport',
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
            
            df_temp_final.to_csv('../dataset/local/df_oddsportal_' + sport + '_' + pays + '_' + ligue + '.csv', encoding='utf-8')
        except Exception, e:
            print e

# =============================================================================
# 
# =============================================================================
list_all             = glob('../dataset/local/*.csv')
for item in list_all:    
    df_all_temp = pd.read_csv(item, index_col=0, encoding='utf-8')
    df_all = pd.concat((df_all, df_all_temp))
    
df_all.drop_duplicates('match_id', inplace=True)
df_all.to_csv('../dataset/local/df_ALL.xls', encoding='utf-8')

