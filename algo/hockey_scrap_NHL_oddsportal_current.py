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
df_NHL_scores               = pd.read_csv('../dataset/local/df_NHL_scores_espn.csv', index_col=0, encoding='utf-8')
df_NHL_scores.dropna(subset=['date_match'], inplace=True)
df_NHL_scores['date_match'] = pd.to_datetime(df_NHL_scores.date_match)
df_NHL_scores.dropna(subset=['match_name'],inplace=True)
df_NHL_scores.reset_index(drop=True, inplace=True)
df_NHL_scores.sort_values(['date_match'], inplace=True, ascending=True)

list_year = [2018]

# =============================================================================
# Recover link to each match for each season in all pages of website
# =============================================================================
### current season
year                            = 2018

season                          = str(year) + '-' + str(year+1)
url_season                      = 'http://www.oddsportal.com/hockey/usa/nhl/results/#/page/'
for page_num in range(35):
    url_season_page             = url_season + str(page_num + 1)
    save_season_page            = '../dataset/local/oddsportal/oddsportal_' + season + '_' + str(page_num+1) + '.html'
    print url_season_page
    os.system('node scrap_odds_first_standalone.js ' + url_season_page + ' ' + save_season_page)
    time.sleep(0.3)
    if os.path.getsize(save_season_page) < 160000:
        break
   
### Next matchs
season                          = str(year) + '-' + str(year+1)
url_season_page                 = 'http://www.oddsportal.com/hockey/usa/nhl/'
save_season_page                = '../dataset/local/oddsportal/oddsportal_next_match.html'
print url_season_page
os.system('node scrap_odds_first_standalone.js ' + url_season_page + ' ' + save_season_page)


ee
#%% =============================================================================
# 
# =============================================================================
list_option = ['', '#home-away', '#cs']

for year in list_year:
    season                          = str(year) + '-' + str(year+1)
    load_season_page                = '../dataset/local/oddsportal/oddsportal_' + season + '_*'
    list_page_season                = glob(load_season_page)
    list_page_season.sort()
    for page in list_page_season:
        print page
        soup                        = BeautifulSoup(open(page), "html.parser")
        page_num                    = page.split('_')[-1].split('.')[0]
        match_name                  = soup.find_all('td', { "class" : "name table-participant"})
        
        for match in match_name:
            match_name              = match.text
            match_name              = match_name.replace(' ','')
            match_name              = match_name.replace('.','_')
            for option_bet in list_option:
                url_match           = 'http://www.oddsportal.com' + match.find_all(href=True)[0]['href'] + option_bet
                option_bet          = option_bet.replace('#','')
                option_bet          = option_bet.replace(';','')
                option_bet          = option_bet.replace('-','_')
                save_name           = match.find_all(href=True)[0]['href'].split('/')[-2][:-1]
                save_match          = '../dataset/local/oddsportal/match/oddsportal_' + season + '_' + save_name + '_' + option_bet +'.html'
                match_id            = save_match.split('-')[-1].split('.')[0].split('_')[0]
                if os.path.isfile(save_match) == 0:
                    print save_match
                    os.system('node scrap_odds_first_standalone.js ' + url_match + ' ' + save_match)
                    time.sleep(0.3)
                else:
                    print 'SKIP'


### Next matchs
page                        = '../dataset/local/oddsportal/oddsportal_next_match.html'
print page
soup                        = BeautifulSoup(open(page), "html.parser")
page_num                    = page.split('_')[-1].split('.')[0]
match_name                  = soup.find_all('td', { "class" : "name table-participant"})

for i, match in enumerate(match_name):
    match_name              = match.text    
    match_name              = match_name.split(';')[-1]
    match_name              = match_name.replace(' ','')
    match_name              = match_name.replace('.','_')
    print match_name

    for option_bet in list_option:
        try:
            url_match           = 'http://www.oddsportal.com' + match.find_all(href=True)[1]['href'] + option_bet
            option_bet          = option_bet.replace('#','')
            option_bet          = option_bet.replace(';','')
            option_bet          = option_bet.replace('-','_')
            save_name           = match.find_all(href=True)[1]['href'].split('/')[-2][:-1]
            save_match          = '../dataset/local/oddsportal/match/oddsportal_next_match_' + save_name + '_' + option_bet +'.html'
            match_id            = save_match.split('-')[-1].split('.')[0].split('_')[0]
            os.system('node scrap_odds_first_standalone.js ' + url_match + ' ' + save_match)
        except Exception,e:
            print 'ERROR :', e
            
#%%
# =============================================================================
# 
# =============================================================================
df_oddsportal                       = pd.read_csv('../dataset/local/df_oddsportal.csv', index_col=0)

list_match_id                       = df_oddsportal.match_id[df_oddsportal.match_id.map(str) != "nan"].tolist()
list_match_id                       = [item[0:7] for item in list_match_id]

load_match_page                     = '../dataset/local/oddsportal/match/oddsportal_2018-*.*'
list_match_page                     = glob(load_match_page)

load_match_next                     = '../dataset/local/oddsportal/match/oddsportal_next*.*'
list_match_next                     = glob(load_match_next)

list_match_page                     = list_match_page+list_match_next

dict_odds                           = {} 


for i, url in enumerate(list_match_page):
    print i, len(list_match_page)
    try:
        match_id    = url.split('-')[-1].split('.')[0].split('_')[0]
        if match_id in list_match_id:
            print 'SKIP'
        else:
            soup        = BeautifulSoup(open(url), "html.parser")
            match_name  = soup.select('h1')[0].text
            match_date  = soup.findAll('p', { "class" : re.compile("^date datet-*")})[0].text 
            
            match_date  = ','.join(match_date.split(',')[1:])
            match_date  = str(datetime.datetime.strptime(match_date," %d %b  %Y, %H:%M"))
            
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
                                'match_id'   : match_id,
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
                                'match_id'   : match_id,
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
                                    'match_id'   : match_id,
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
if len(df_temp) != 0:
    df_temp.fillna('',inplace=True)
    df_temp         = df_temp.reindex_axis(sorted(df_temp.columns, reverse=True), axis=1)
    df_temp         = df_temp.groupby(['match_name', 'match_date'], as_index=False).sum()
    df_temp.sort_values(by='match_date', ascending=True, inplace= True)
    df_temp['team_home']  = df_temp.match_name.apply(lambda x : x.split('-')[0].strip())
    df_temp['team_away']  = df_temp.match_name.apply(lambda x : x.split('-')[1].strip())
    
    df_temp_final = pd.concat((df_oddsportal,df_temp))
    df_temp_final.to_csv('../dataset/local/df_oddsportal.csv', encoding='utf-8')

for filename in list_match_next:
    os.system('rm ' + filename)