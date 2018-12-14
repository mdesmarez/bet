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

cur_dir_here = os.path.split(os.path.realpath(__file__))[0]




# =============================================================================
# create folder structure
# =============================================================================
os.system('mkdir -p ' + '../dataset/local/oddsportal/match')


# =============================================================================
# 
# =============================================================================
df_NHL_scores               = pd.read_csv('../dataset/local/df_NHL_scores_espn.csv', index_col=0, encoding='utf-8')
df_NHL_scores.dropna(subset=['date_match'], inplace=True)
df_NHL_scores['date_match'] = pd.to_datetime(df_NHL_scores.date_match)
df_NHL_scores.dropna(subset=['match_name'],inplace=True)
df_NHL_scores.reset_index(drop=True, inplace=True)
df_NHL_scores.sort_values(['date_match'], inplace=True, ascending=True)

year_min                    = df_NHL_scores.date_match.min().year
year_max                    = df_NHL_scores.date_match.max().year

#####
year_min = 2018
#####

list_year                   = np.linspace(year_min,year_max,year_max-year_min+1).astype(int)

#list_year = [2000, 2001, 2002, 2003, 2004]
list_year = [2018]

## =============================================================================
## Recover link to each match for each season in all pages of website
## =============================================================================
#### current season
#year                            = 2018
#
#season                          = str(year) + '-' + str(year+1)
#url_season                      = 'http://www.oddsportal.com/hockey/usa/nhl/results/#/page/'
#for page_num in range(35):
#    url_season_page             = url_season + str(page_num + 1)
#    save_season_page            = '../dataset/local/oddsportal/oddsportal_' + season + '_' + str(page_num+1) + '.html'
#    print url_season_page
#    os.system('node scrap_odds_first_standalone.js ' + url_season_page + ' ' + save_season_page)
#    time.sleep(0.3)
#
#### previous seasons        
#for year in list_year:
#    season                          = str(year) + '-' + str(year+1)
#    url_season                      = 'http://www.oddsportal.com/hockey/usa/nhl-' + season + '/results/#/page/'
#    for page_num in range(35):
#        url_season_page             = url_season + str(page_num + 1)
#        save_season_page            = '../dataset/local/oddsportal/oddsportal_' + season + '_' + str(page_num+1) + '.html'
#        if os.path.isfile(save_season_page) == 0:
#            print url_season_page
#            os.system('node scrap_odds_first_standalone.js ' + url_season_page + ' ' + save_season_page)
#            time.sleep(0.3)
#


#ee
##%% =============================================================================
## 
## =============================================================================
#list_option = ['', '#home-away', '#cs']
#
#for year in list_year:
#    season                          = str(year) + '-' + str(year+1)
#    load_season_page                = '../dataset/local/oddsportal/oddsportal_' + season + '_*'
#    list_page_season                = glob(load_season_page)
#    list_page_season.sort()
#    for page in list_page_season:
#        print page
#        soup                        = BeautifulSoup(open(page), "html.parser")
#        page_num                    = page.split('_')[-1].split('.')[0]
#        match_name                  = soup.find_all('td', { "class" : "name table-participant"})
#        
#        for match in match_name:
#            
#            match_name              = match.text
#            match_name              = match_name.replace(' ','')
#            match_name              = match_name.replace('.','_')
#            for option_bet in list_option:
#                url_match           = 'http://www.oddsportal.com' + match.find_all(href=True)[0]['href'] + option_bet
#                option_bet          = option_bet.replace('#','')
#                option_bet          = option_bet.replace(';','')
#                option_bet          = option_bet.replace('-','_')
#                save_name           = match.find_all(href=True)[0]['href'].split('/')[-2][:-1]
#                save_match          = '../dataset/local/oddsportal/match/oddsportal_' + season + '_' + str(page_num) + '_' + save_name + '_' + option_bet +'.html'
#                if os.path.isfile(save_match) == 0:
#                    print save_match
#                    
#                    os.system('node scrap_odds_first_standalone.js ' + url_match + ' ' + save_match)
#                    time.sleep(0.3)
#
#ee
#%%
# =============================================================================
# 
# =============================================================================
#df_oddsportal_list_done             = pd.read_csv('../dataset/local/df_oddsportal_list_done.csv', index_col=0)
#df_oddsportal_list_done.columns     = ['list_done'] 
#list_done = df_oddsportal_list_done.list_done.tolist()
#
df_oddsportal                       = pd.read_csv('../dataset/local/df_oddsportal.csv', index_col=0)
#load_match_page                     = '../dataset/local/oddsportal/match/*.*'
#list_match_page                     = glob(load_match_page)
#list_match_page                     = list(set(list_match_page)-set(list_done))
#list_match_page.sort()
#
#dict_odds                           = {} 
#list_match_page.sort()                         
#ee

######## experimental this season
load_match_page                     = '../dataset/local/oddsportal/match/oddsportal_2018-*.*'
list_match_page                     = glob(load_match_page)
dict_odds                           = {} 

########

for i, url in enumerate(list_match_page):
    print i, len(list_match_page)
    try:
        soup        = BeautifulSoup(open(url), "html.parser")
        match_name  = soup.select('h1')[0].text
        match_date  = soup.findAll('p', { "class" : re.compile("^date datet-*")})[0].text 
        
        match_date  = ','.join(match_date.split(',')[1:])
        match_date  = str(datetime.datetime.strptime(match_date," %d %b  %Y, %H:%M"))
#        match_date  = str(datetime.datetime.strptime(match_date,"%A, %d %b  %Y, %H:%M"))
        
        bet_type    = soup.findAll('li', { "class" : "active"})[1].strong.text
        team_home   = match_name.split('-')[0].strip()
        team_away   = match_name.split('-')[1].strip()
    
        bet_R1      = 0
        bet_RN      = 0
        bet_R2      = 0
        bet_V1      = 0
        bet_V2      = 0
    
    
        if bet_type == '1X2':
            bet_R1 = soup.findAll('tr', { "class" : "aver"})[0].findAll('td', { "class" : "right"})[0].text
            bet_RN = soup.findAll('tr', { "class" : "aver"})[0].findAll('td', { "class" : "right"})[1].text
            bet_R2 = soup.findAll('tr', { "class" : "aver"})[0].findAll('td', { "class" : "right"})[2].text
            dict_odds.update({i:{
                            'match_name' : match_name,
                            'match_date' : match_date,
                            'team_home'  : team_home,
                            'team_away'  : team_away,
                            'bet_R1'     : bet_R1,
                            'bet_RN'     : bet_RN,
                            'bet_R2'     : bet_R2,
                            'bet_V1'     : '',
                            'bet_V2'     : '',
                            }})
    
        if bet_type == 'Home/Away':
            bet_V1 = soup.findAll('tr', { "class" : "aver"})[0].findAll('td', { "class" : "right"})[0].text
            bet_V2 = soup.findAll('tr', { "class" : "aver"})[0].findAll('td', { "class" : "right"})[1].text
            dict_odds.update({i:{
                            'match_name' : match_name,
                            'match_date' : match_date,
                            'team_home'  : team_home,
                            'team_away'  : team_away,
                            'bet_R1'     : '',
                            'bet_RN'     : '',
                            'bet_R2'     : '',
                            'bet_V1'     : bet_V1,
                            'bet_V2'     : bet_V2,
                            }})
        
        if bet_type == 'Correct Score':
            dict_odds.update({i:{
                                'match_name' : match_name,
                                'match_date' : match_date,
                                'team_home'  : team_home,
                                'team_away'  : team_away,
                                'bet_R1'     : '',
                                'bet_RN'     : '',
                                'bet_R2'     : '',
                                'bet_V1'     : '',
                                'bet_V2'     : '',
                                }})
            bet_XX = soup.findAll('div', { "class" : "table-container"})
            for j, item in enumerate(bet_XX):
                score = bet_XX[j].strong.text
                bet   = bet_XX[j].findAll('span', { "class" : "avg nowrp"})[0].text
                dict_odds[i].update({score:bet})
    except Exception, e:
        print 'error : ', e
        pass            

# =============================================================================
#             
# =============================================================================
df_temp         = pd.DataFrame.from_dict(dict_odds, orient='index')
df_temp.fillna('',inplace=True)
df_temp         = df_temp.reindex_axis(sorted(df_temp.columns, reverse=True), axis=1)
df_temp         = df_temp.groupby(['match_name', 'match_date'], as_index=False).sum()
df_temp.sort_values(by='match_date', ascending=True, inplace= True)
df_temp['team_home']  = df_temp.match_name.apply(lambda x : x.split('-')[0].strip())
df_temp['team_away']  = df_temp.match_name.apply(lambda x : x.split('-')[1].strip())

df_temp_final = pd.concat((df_oddsportal,df_temp))
df_temp_final.to_csv('../dataset/local/df_oddsportal.csv', encoding='utf-8')

df_temp_list_done     = pd.DataFrame(list_match_page)
df_temp_list_done.to_csv('../dataset/local/df_oddsportal_list_done.csv', encoding='utf-8')
