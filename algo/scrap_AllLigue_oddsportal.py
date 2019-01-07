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
import json

import pandas             as pd
import numpy              as np

from bs4                  import BeautifulSoup
from glob                 import glob

from datetime             import datetime


# =============================================================================
# create folder structure
# =============================================================================


# =============================================================================
# 
# =============================================================================
process_scrap                   = 1
process_scrap_current_season    = 0
process_scrap_next_match        = 0
process_generate                = 0

this_year                       = 2018
list_year                       = [2016, 2017, 2018]


# =============================================================================
# 
# =============================================================================
def bs4_recover_bet(soup, dict_odds, pays, sport, ligue):
    match_list                  = soup.find_all('tr', { "class" : "deactivate"}) + soup.find_all('tr', { "class" : "odd deactivate"})

    for match in match_list:
        try:
            match_name              = match.find('td', { "class" : "name table-participant"}).text
            match_date              = str(match.find_all('td')[0]).split('"')[1].split('t')[-1].split('-')[0]
            team_home               = match_name.split('-')[0].strip()
            team_away               = match_name.split('-')[1].strip()
            if len(match.find_all('td', { "class" : "odds-nowrp"})) == 2:
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
    return dict_odds


# =============================================================================
# 
# =============================================================================
try:    
    with open('../dataset/local/dict_archived.json') as json_file:  
        dict_archived = json.load(json_file)
except:
    dict_archived = {}

    
list_ligue = []
list_sport = [\
#              'volleyball', 
#              'tennis',
#              'handball',
              'hockey',              
              ]


for sport in list_sport:
    if sport in list_sport:
        print sport
        try:
            test = dict_archived[sport]
        except:
            dict_archived.update({sport:{}})
        
        url_page        = 'https://www.oddsportal.com/results/#' + sport
        os.system('mkdir -p ' + '../dataset/local/' + sport + '/oddsportal/match')
        save_web_page   = '../dataset/local/' + sport + '/oddsportal_' + sport + '_list_ligue.html'
        os.system('rm "' + save_web_page + '"')
        os.system('node scrap_odds_first_standalone.js ' + url_page + ' ' + save_web_page)
        soup                        = BeautifulSoup(open(save_web_page), "html.parser")
        ligue_list                  = soup.find_all('a', { "foo" : "f"})
        for ligue in ligue_list:
            ligue_name = ligue.text
            ligue_href = ligue.get('href')
            if ligue_href.split('/')[1] == sport:
                try:
                    test = dict_archived[sport][ligue_name]['done']
                except:
                    dict_archived[sport].update({ligue_name:{}})
                    dict_archived[sport][ligue_name].update({'href':ligue_href,'done':0, 'pays':ligue_href.split('/')[2]})
                    list_ligue.append([ligue_href.split('/')[1],ligue_href.split('/')[2],ligue_href.split('/')[3]])

### SAVE
with open('../dataset/local/dict_archived.json', 'w') as outfile:
    json.dump(dict_archived, outfile)



# =============================================================================
# 
# =============================================================================
for sport, sport_v in dict_archived.items():
    if sport in list_sport:
        print sport
        for ligue, ligue_v in dict_archived[sport].items():
            if ligue_v['done'] == 0:
                url_ligue = 'https://www.oddsportal.com/' + ligue_v['href']
                save_temp = '../dataset/local/' + sport + '/save_temp.html'
                os.system('rm "' + save_temp + '"')
                os.system('node scrap_odds_first_standalone.js ' + url_ligue + ' ' + save_temp)
                soup              = BeautifulSoup(open(save_temp), "html.parser")
                season_list_all   = soup.find_all('div', { "class" : "main-menu2 main-menu-gray"})
                if season_list_all != []:
                    season_list_all   = season_list_all[0].find('ul', { "class" : "main-filter"})
                    season_list       = season_list_all.find_all('li')
        
                    ligue_v['done'] = 1
                    for i in range(len(season_list)):
                        season_url    = season_list[i].a.get('href')
                        season_text   = season_list[i].text
                        print season_text
                        try:
                            if int(season_text.split('/')[0]) in list_year:
                                print ligue, '*************'
                                ligue_v.update({season_text.split('/')[0]:season_url, 'done':2})
                        except Exception,e :
                            print e                    
    
                ### SAVE
                with open('../dataset/local/dict_archived.json', 'w') as outfile:
                    json.dump(dict_archived, outfile)
        

# =============================================================================
# 
# =============================================================================
#%%
for sport, sport_v in dict_archived.items():
    if sport in list_sport:
        print sport
        for ligue, ligue_v in dict_archived[sport].items():
            dict_odds = {}
            if ligue_v['done'] == 2:
                pays = ligue_v['pays']
                for year in list_year:
                    if str(year) in ligue_v:
                        ###
                        url_ligue_year = 'https://www.oddsportal.com' + ligue_v[str(year)]    
                        print url_ligue_year
                        save_web_page   = '../dataset/local/' + sport + '/oddsportal_' + sport + '_list_ligue_year.html'
                        os.system('rm "' + save_web_page + '"')
                        os.system('node scrap_odds_first_standalone.js ' + url_ligue_year + ' ' + save_web_page)                    
                        ###
                        soup              = BeautifulSoup(open(save_web_page), "html.parser")
                        page_max_number = 0
                        find_page_max     = soup.find_all('div', { "id" : "pagination"})
                        if find_page_max != []:
                            page_max_number = find_page_max[0].find_all('a')[-1].get('x-page')
                        else:
                            page_max_number = 0
                        
                        dict_odds = bs4_recover_bet(soup, dict_odds, pays, sport, ligue)
                        
                        if page_max_number !=0:
                            for i in range(int(page_max_number)-1):
                                url_ligue_year = 'https://www.oddsportal.com' + ligue_v[str(year)] + '#/page/' + str(i+2) + '/'
                                print url_ligue_year
                                save_web_page   = '../dataset/local/' + sport + '/oddsportal_' + sport + '_list_ligue_year.html'
                                os.system('rm "' + save_web_page + '"')
                                os.system('node scrap_odds_first_standalone.js ' + url_ligue_year + ' ' + save_web_page)                    
                                ###
                                soup              = BeautifulSoup(open(save_web_page), "html.parser")
                                dict_odds = bs4_recover_bet(soup, dict_odds, pays, sport, ligue)
    
            if dict_odds != {}:
                df_temp         = pd.DataFrame.from_dict(dict_odds, orient='index')
                df_temp.to_csv('../dataset/local/' + sport + '/df_oddsportal_' + sport + '_' + pays + '_' + ligue + '.csv', encoding='utf-8')
            ligue_v['done'] = 3
    
            ### SAVE
            with open('../dataset/local/dict_archived_final.json', 'w') as outfile:
                json.dump(dict_archived, outfile)
                

# =============================================================================
# 
# =============================================================================
with open('../dataset/local/dict_archived.json') as json_file:  
    dict_archived = json.load(json_file)
    
for sport, sport_v in dict_archived.items():
    print sport
    try:    
        df_sport = pd.read_csv('../dataset/local/' + sport + '/df_ALL_' + sport + '.xls', index_col=0, encoding='utf-8')
        df_sport.drop_duplicates('match_id', inplace=True)
    except:
        df_sport = pd.DataFrame()


    list_all             = glob('../dataset/local/' + sport + '/df_oddsportal_' + sport + '*.csv')
    for i, item in enumerate(list_all):    
        df_sport_temp = pd.read_csv(item, index_col=0, encoding='utf-8')
        df_sport = pd.concat((df_sport, df_sport_temp))
        print i, len(list_all)
        
    df_sport.drop_duplicates('match_id', inplace=True)
    df_sport.to_csv('../dataset/local/' + sport + '/df_ALL_' + sport + '.xls', encoding='utf-8')



eeee
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

ee
# =============================================================================
# 
# =============================================================================
df_oddsportal   = pd.DataFrame()
dict_odds       = {}
        
for item in list_ligue_diff:
    sport       = item[0]
    pays        = item[1]
    ligue       = item[2]
    
    os.system('mkdir -p ' + '../dataset/local/' + sport + '/oddsportal/match')
    # =============================================================================
    # Recover link to each match for each season in all pages of website
    # =============================================================================
    if process_scrap == 1:
        ### previous year
        for year in list_year:
            
            if year == this_year:
                break
            ee
            season                          = str(year) + '-' + str(year+1)
            url_season                      = 'https://www.oddsportal.com/' + sport + '/' + pays + '/' + ligue + '-' + season + '/results/#/page/'
            for page_num in range(35):
                url_season_page             = url_season + str(page_num + 1)
                save_season_page            = '../dataset/local/' + sport + '/oddsportal/oddsportal_' + pays + '_' + ligue + '_' + season + '_' + str(page_num+1) + '.html'
                print url_season_page
                if os.path.isfile(save_season_page) != True:
                    os.system('node scrap_odds_first_standalone.js ' + url_season_page + ' ' + save_season_page)
#                    time.sleep(0.1)
#                    if os.path.getsize(save_season_page) < 80000:
#                        os.system('rm ' + save_season_page)
#                        break
                
#                    if page_num > 5:
#                        soup                        = BeautifulSoup(open(save_season_page), "html.parser")
#                        match_list                  = soup.find_all('tr', { "class" : "deactivate"}) + soup.find_all('tr', { "class" : "odd deactivate"})
#                        if len(match_list) == 0:
#                            os.system('rm ' + save_season_page)
#                            break
            
            
        if process_scrap_current_season == 1:    
            ### current season
            year                            = this_year
            season                          = str(year) + '-' + str(year+1)
            url_season                      = 'https://www.oddsportal.com/' + sport + '/' + pays + '/' + ligue + '/results/#/page/'
            for page_num in range(35):
                url_season_page             = url_season + str(page_num + 1)
                save_season_page            = '../dataset/local/' + sport + '/oddsportal/oddsportal_' + pays + '_' + ligue + '_' + season + '_' + str(page_num+1) + '.html'
                print url_season_page
                os.system('node scrap_odds_first_standalone.js ' + url_season_page + ' ' + save_season_page)
    #            time.sleep(0.3)
        
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
# LIST ALREADY DONE
# =============================================================================
list_sport = df_all.sport.unique()
for sport in list_sport:
    list_pays = df_all[df_all.sport == sport].pays.unique()
    for pays in list_pays:
        list_ligue = df_all[(df_all.sport == sport) & (df_all.pays == pays)].ligue.unique()
        for ligue in list_ligue:
            df = df_all[(df_all.sport == sport) & (df_all.pays == pays) & (df_all.ligue == ligue)]
            df['date_match'] = df.match_date.apply(lambda x : (datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')))
            df.reset_index(drop=True, inplace=True)
            df.date_match       = pd.to_datetime(df.date_match)
            df['season']        = df.date_match.apply(lambda x : x.year if x.month >= 7 else x.year-1)
            df['season_week']   = df.date_match.apply(lambda x : x.week+52 if x.week <= 25 else x.week)
            list_season         = df.season.unique()
            for season in list_season:
                print sport, pays, ligue, season
    

# =============================================================================
# 
# =============================================================================
for item in list_ligue_diff:
    sport   = item[0]
    pays    = item[1]
    ligue   = item[2]
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
                        if len(match.find_all('td', { "class" : "odds-nowrp"})) == 2:
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
list_all             = glob('../dataset/local/df_oddsportal_tennis*.csv')
for i, item in enumerate(list_all):    
    df_all_temp = pd.read_csv(item, index_col=0, encoding='utf-8')
    df_all = pd.concat((df_all, df_all_temp))
    print i, len(list_all)
    
df_all.drop_duplicates('match_id', inplace=True)
df_all.to_csv('../dataset/local/df_ALL.xls', encoding='utf-8')

