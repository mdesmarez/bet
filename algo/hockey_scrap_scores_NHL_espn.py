#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 08:23:17 2018

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

import pandas             as pd
import numpy              as np

from bs4                  import BeautifulSoup
from glob                 import glob
from datetime             import timedelta

cur_dir_here = os.path.split(os.path.realpath(__file__))[0]



# =============================================================================
# create folder structure
# =============================================================================
os.system('mkdir -p ' + '../dataset/local')


# =============================================================================
# INIT PARAMETERS
# =============================================================================
now = datetime.datetime.now()

year_start = 2018
year_stop  = int(now.year)



list_date       = []
for k in range(year_start,year_stop+1,1):
    for j in range(1,13,1):
        for i in range(1,32,1):
            list_date.append([i,j,k])


# =============================================================================
# test section
# =============================================================================
#list_date = [[8, 8, 2013]]


# =============================================================================
# ALREADY SCRAP FILE
# =============================================================================
try:
    df_NHL_scores = pd.read_csv('../dataset/local/df_NHL_scores_espn.csv', index_col=0, encoding='utf-8')
    df_NHL_scores.dropna(subset=['date_match'], inplace=True)
    df_NHL_scores.fillna('', inplace=True)
    df_NHL_scores = df_NHL_scores[~((df_NHL_scores.team_winner == '') & (df_NHL_scores.match_name != ''))]
#    list_date_done = df_NHL_scores.date_match.apply(lambda x: [int(str(x)[8:10]),int(str(x)[5:7]),int(str(x)[:4])]).tolist()
#    list_date_done = df_NHL_scores.date_match.apply(lambda x: [datetime.datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S").day,datetime.datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S").month,datetime.datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S").year]).tolist()    
    list_date_done = df_NHL_scores.date_match.apply(lambda x: [datetime.datetime.strptime(str(x), "%Y-%m-%d").day,datetime.datetime.strptime(str(x), "%Y-%m-%d").month,datetime.datetime.strptime(str(x), "%Y-%m-%d").year]).tolist()    
    df_NHL_scores['date_match'] = pd.to_datetime(df_NHL_scores.date_match)

    df_NHL_scores = df_NHL_scores[df_NHL_scores.date_match < (datetime.datetime.utcnow() + timedelta(days=-6))]
    list_date_done = df_NHL_scores.date_match.apply(lambda x : [x.day, x.month, x.year]).tolist()

    for date_done in list_date_done:
        #print date_done
        try:
            list_date.remove(date_done)
        except ValueError:
            pass
except:
    df_NHL_scores   = pd.DataFrame()


#%% ===========================================================================
# MAIN
# =============================================================================
def no_match_today(df_NHL_scores, test_matchs_date):
    dict_temp = {}
    dict_temp.update({'competition':'NHL',
                      'date_match': test_matchs_date,
                      'match_name': '',
                      'score_1P'  : '',
                      'score_2P'  : '',                       
                      'score_3P'  : '',
                      'score_IT_final' : '',
                      'score_OT_final' : '',
                      'team_home'      : '',
                      'team_away'      : '',
                      'team_home_point': '',
                      'team_away_point': '',
                      'score_IT_home'  : '',
                      'score_IT_away'  : '',
                      'score_OT_away'  : '',
                      'score_OT_home'  : '',
                      'team_winner'    : '',
                      'team_loser'     : '',
                      'team_winner_HA' : '',
                      'team_loser_HA'  : '',
                      'point_diff_home_away': '',
                      })
    df_temp         = pd.DataFrame.from_dict(dict_temp, orient='index').T
    print str(test_matchs_date) + ' / ' + 'No match today' 
    df_NHL_scores   = pd.concat((df_NHL_scores,df_temp))
    return df_NHL_scores


    
for date_play in list_date:
    day         = date_play[0]
    month       = date_play[1]
    year        = date_play[2]
    date_str    = str(year) + str(month).zfill(2) + str(day).zfill(2)
    
    url_date    = str(day).zfill(2) + '_' + str(month).zfill(2) + '_' + str(year)
    test_matchs_date = dateparser.parse(url_date, ['%d_%m_%Y'])
#    print '#', url_date, test_matchs_date

    url = 'http://www.espn.com/nhl/scoreboard?date=' + date_str
    
    try:
        content_url = urllib2.urlopen(url).read()
        soup                = BeautifulSoup(content_url)
    except:
        print '###### ERREur', url
        time.sleep(20)
        
    all_data            = soup.find_all("div", { "class" : "mod-container mod-no-header-footer mod-scorebox final mod-scorebox-final"})

    if all_data == []:
        df_NHL_scores = no_match_today(df_NHL_scores, test_matchs_date)
                    
    for games in all_data:
        dict_temp       = {}
        
        if games.find_all('ul', { "class" : "game-info"})[0].text.find('ostpon') != -1:
            break
        
        competition             = ""
        date_match              = ""
        match_name              = ""
        score_1P                = ""
        score_2P                = ""          
        score_3P                = ""
        score_IT_final          = ""
        score_OT_final          = ""
        team_home               = ""
        team_away               = ""
        team_home_point         = ""
        team_away_point         = ""
        score_IT_home           = ""
        score_IT_away           = ""
        score_OT_away           = ""
        score_OT_home           = ""
        team_winner             = ""
        team_loser              = ""
        team_winner_HA          = ""
        team_loser_HA           = ""
        point_diff_home_away    = ""
        
        
        try:
            ### DATE
            a = soup.find_all('div', { "class" : "key-dates key-dates_sc"})[0].text
            matchs_date = dateparser.parse(a[a.find('for')+3:a.find('Auto')].strip())
    
            ### NAME
            team_away       = games.find_all('td', { "class" : "team-name"})[0].text
            team_home       = games.find_all('td', { "class" : "team-name"})[2].text
            match_name      = team_away + ' - ' + team_home
            
            ### SCORE
            score_1_away    = int(games.find_all('td', { "id" : "lsAway1"})[0].text)
            score_2_away    = int(games.find_all('td', { "id" : "lsAway2"})[0].text)
            score_3_away    = int(games.find_all('td', { "id" : "lsAway3"})[0].text)
            try:
                score_OT_away = int(games.find_all('td', { "id" : "lsAwayot"})[0].text)
            except:
                score_OT_away = 0
            score_T_away    = int(games.find_all('td', { "class" : "ts gp-awayScore"})[0].text)
    
            score_1_home    = int(games.find_all('td', { "id" : "lsHome1"})[0].text)
            score_2_home    = int(games.find_all('td', { "id" : "lsHome2"})[0].text)
            score_3_home    = int(games.find_all('td', { "id" : "lsHome3"})[0].text)
            try:
                score_OT_home = int(games.find_all('td', { "id" : "lsHomeot"})[0].text)
            except:
                score_OT_home = 0
            score_T_home    = int(games.find_all('td', { "class" : "ts gp-homeScore"})[0].text)
    
            score_IT_home   = score_1_home + score_2_home + score_3_home
            score_IT_away   = score_1_away + score_2_away + score_3_away
    
            ### FORMAT SCOR        
            score_1P        = str(score_1_away) + ' - ' + str(score_1_home)
            score_2P        = str(score_2_away) + ' - ' + str(score_2_home)
            score_3P        = str(score_3_away) + ' - ' + str(score_3_home)        
            score_IT_final  = str(score_IT_away) + ' - ' + str(score_IT_home)
            score_OT_away   = score_IT_away + score_OT_away
            score_OT_home   = score_IT_home + score_OT_home
            score_OT_final  = str(score_OT_away) + ' - ' + str(score_OT_home)
            
            
            ### CURRENT POINT
            team_home_point = games.find_all('td', { "class" : "team-name"})[3].text
            team_home_point = int(team_home_point.split(',')[-1].split('pts')[0].strip())
            team_away_point = games.find_all('td', { "class" : "team-name"})[1].text
            team_away_point = int(team_away_point.split(',')[-1].split('pts')[0].strip())
            
            ### WIN LOSS
            if score_OT_away>score_OT_home:
                team_winner     = team_away
                team_loser      = team_home
                team_winner_HA  = 'team_away'
                team_loser_HA   = 'team_home'
            else:
                team_winner     = team_home
                team_loser      = team_away
                team_winner_HA  = 'team_home'
                team_loser_HA   = 'team_away'

                
            ### POINT SCORE
            point_diff_home_away = team_home_point - team_away_point
            
            ### DATA MERGE
            dict_temp.update({'competition':'NHL',
                              'date_match': matchs_date,
                              'match_name': match_name,
                              'score_1P'  : score_1P,
                              'score_2P'  : score_2P,                       
                              'score_3P'  : score_3P,
                              'score_IT_final' : score_IT_final,
                              'score_OT_final' : score_OT_final,
                              'team_home'      : team_home,
                              'team_away'      : team_away,
                              'team_home_point': team_home_point,
                              'team_away_point': team_away_point,
                              'score_IT_home'  : score_IT_home,
                              'score_IT_away'  : score_IT_away,
                              'score_OT_away'  : score_OT_away,
                              'score_OT_home'  : score_OT_home,
                              'team_winner'    : team_winner,
                              'team_loser'     : team_loser,
                              'team_winner_HA' : team_winner_HA,
                              'team_loser_HA'  : team_loser_HA,
                              'point_diff_home_away': point_diff_home_away,
                              })
            df_temp         = pd.DataFrame.from_dict(dict_temp, orient='index').T
            print matchs_date, ' / ', match_name, ' / ', score_IT_final, ' / ', score_OT_final, ' / ', team_winner
            df_NHL_scores   = pd.concat((df_NHL_scores,df_temp))
        except:
            ### DATA MERGE
            print test_matchs_date
            df_NHL_scores = no_match_today(df_NHL_scores, test_matchs_date)
    
#    print 'ya', test_matchs_date
    ### not scrap future
    if isinstance(test_matchs_date, datetime.datetime) == True:
#        if datetime.datetime.utcnow() - timedelta(days=2) <= test_matchs_date:
        if datetime.datetime.utcnow() - timedelta(days=1) <= test_matchs_date:
#            print ('over limit')
#            print str(datetime.datetime.utcnow()), str(test_matchs_date)
            all_data            = soup.find_all("div", { "class" : "game-header"})
        
            for games in all_data:
                dict_temp       = {}

                competition             = ""
                date_match              = ""
                match_name              = ""
                score_1P                = ""
                score_2P                = ""          
                score_3P                = ""
                score_IT_final          = ""
                score_OT_final          = ""
                team_home               = ""
                team_away               = ""
                team_home_point         = ""
                team_away_point         = ""
                score_IT_home           = ""
                score_IT_away           = ""
                score_OT_away           = ""
                score_OT_home           = ""
                team_winner             = ""
                team_loser              = ""
                team_winner_HA          = ""
                team_loser_HA           = ""
                point_diff_home_away    = ""
                
                ### DATE
                a = soup.find_all('div', { "class" : "key-dates key-dates_sc"})[0].text
                matchs_date = dateparser.parse(a[a.find('for')+3:a.find('Auto')].strip())
        
                ### NAME
                team_away       = games.find_all('td', { "class" : "team-name"})[0].text
                team_home       = games.find_all('td', { "class" : "team-name"})[2].text
                match_name      = team_away + ' - ' + team_home
            
                ### CURRENT POINT
                team_home_point = games.find_all('td', { "class" : "team-name"})[3].text
                team_home_point = int(team_home_point.split(',')[-1].split('pts')[0].strip())
                team_away_point = games.find_all('td', { "class" : "team-name"})[1].text
                team_away_point = int(team_away_point.split(',')[-1].split('pts')[0].strip())
            
                ### POINT SCORE            
                point_diff_home_away = team_home_point - team_away_point
            
                ### DATA MERGE
                dict_temp.update({'competition':'NHL',
                              'date_match': matchs_date,
                              'match_name': match_name,
                              'score_1P'  : score_1P,
                              'score_2P'  : score_2P,                       
                              'score_3P'  : score_3P,
                              'score_IT_final' : score_IT_final,
                              'score_OT_final' : score_OT_final,
                              'team_home'      : team_home,
                              'team_away'      : team_away,
                              'team_home_point': team_home_point,
                              'team_away_point': team_away_point,
                              'score_IT_home'  : score_IT_home,
                              'score_IT_away'  : score_IT_away,
                              'score_OT_away'  : score_OT_away,
                              'score_OT_home'  : score_OT_home,
                              'team_winner'    : team_winner,
                              'team_loser'     : team_loser,
                              'team_winner_HA' : team_winner_HA,
                              'team_loser_HA'  : team_loser_HA,
                              'point_diff_home_away': point_diff_home_away,
                              })
            
                df_temp         = pd.DataFrame.from_dict(dict_temp, orient='index').T
                print matchs_date, ' / ', match_name, ' / ', score_IT_final, ' / ', score_OT_final, ' / ', team_winner
                df_NHL_scores   = pd.concat((df_NHL_scores,df_temp))
                
            if datetime.datetime.utcnow() + timedelta(days=2) < test_matchs_date:
                print 'Finish not scaping future'
                break

### EXPORT
df_NHL_scores.drop_duplicates(inplace=True)
df_NHL_scores = df_NHL_scores[['competition',
                               'date_match',
                               'match_name',
                               'team_winner', 
                               'team_loser', 
                               'team_winner_HA', 
                               'team_loser_HA',
                               'point_diff_home_away', 
                              
                               'score_1P',
                               'score_2P',
                               'score_3P',
                               'score_IT_final',
                               'score_OT_final',
                               
                               'team_home',
                               'team_home_point',
                               'score_IT_home',
                               'score_OT_home',
                               
                               'team_away', 
                               'team_away_point',
                               'score_IT_away',
                               'score_OT_away',
                               
                               ]]

df_NHL_scores.dropna(subset=['date_match'], inplace=True)
df_NHL_scores['date_match'] = pd.to_datetime(df_NHL_scores.date_match)
df_NHL_scores.sort_values(['date_match'], inplace=True, ascending=True)
df_NHL_scores.to_csv('../dataset/local/df_NHL_scores_espn.csv', encoding='utf-8')












