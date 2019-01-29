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
import unicodedata

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
list_year                       = [2015, 2016, 2017, 2018]


# =============================================================================
# 
# =============================================================================
def bs4_recover_bet(soup, dict_odds, pays, sport, ligue):
    match_list                  = soup.find_all('tr', { "class" : "deactivate"}) + soup.find_all('tr', { "class" : "odd deactivate"})
    count_no_bookmaker          = 0
    for match in match_list:
        count_no_bookmaker      = count_no_bookmaker + 1
        print count_no_bookmaker
        if count_no_bookmaker >= 7 :
            break        ### GO INSIDE MATCH DETAILS
        match_detail_url = match.find('td', { "class" : "name table-participant"}).a.get('href')
        url_page        = 'https://www.oddsportal.com' + match_detail_url
        save_web_page   = '../dataset/local/' + sport + '/oddsportal_' + sport + '_match_detail.html'
        os.system('rm "' + save_web_page + '"')
        os.system('node scrap_odds_first_standalone.js ' + url_page + ' ' + save_web_page)
        soup_detail     = BeautifulSoup(open(save_web_page), "html.parser")
        match_detail_list    = soup_detail.find_all('tr', { "class" : "lo odd"}) + soup_detail.find_all('tr', { "class" : "lo even"})
        
        ### detail each bookmaker
        for match_detail in match_detail_list:
            bookmakers_name         = match_detail.find('a', { "class" : "name"}).text
            if bookmakers_name == 'Pinnacle':
                bookmaker = bookmakers_name  
                count_no_bookmaker = 0
                print 'bookmakers_name :', bookmakers_name
                try:
                    match_name              = match.find('td', { "class" : "name table-participant"}).text
                    print 'match_name'
                    match_name = unicodedata.normalize("NFKD", match_name)
                    print match_name
                    match_date              = str(match.find_all('td')[0]).split('"')[1].split('t')[-1].split('-')[0]
                    print 'team_home'
                    team_home               = match_name.split('-')[0].strip()
                    team_away               = match_name.split('-')[1].strip()
                    if len(match_detail.find_all('td', { "class" : re.compile(r'right odds*')})) == 2:
                        print ('X=0')
                        bet_1                   = float(match_detail.find_all('td', { "class" : re.compile(r'right odds*')})[0].text)
                        bet_X                   = 0
                        bet_2                   = float(match_detail.find_all('td', { "class" : re.compile(r'right odds*')})[1].text) 
                    else:
                        print ('X=X')
                        bet_1                   = float(match_detail.find_all('td', { "class" : re.compile(r'right odds*')})[0].text)
                        bet_X                   = float(match_detail.find_all('td', { "class" : re.compile(r'right odds*')})[1].text)
                        bet_2                   = float(match_detail.find_all('td', { "class" : re.compile(r'right odds*')})[2].text)
                    print 'score'
                    score                   = match.find('td', { "class" : "center bold table-odds table-score"}).text
                    try:
                        score_home              = score.split(':')[0]
                        score_away              = score.split(':')[1].split(' ')[0]
                    except Exception,e :
                        print 'ERROR LINE : 96'
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
                        
                    print 'dict_odd'
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
                                        'bookmaker'  : bookmaker,
                                        }}) 
                    ### exit looking for bookmaker
                    break
                
                except Exception,e :
                    print 'ERROR LINE : 134'
                    print e
            
    return dict_odds, count_no_bookmaker


def bs4_recover_bet_old(soup, dict_odds, pays, sport, ligue):
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




def save_df():
    with open('../dataset/local/dict_archived.json') as json_file:  
        dict_archived = json.load(json_file)
    
    list_pays = [item for item, _ in dict_archived.items()]
    list_pays.sort()
    list_sport = []
    
    for pays in list_pays:
        for sport, sport_v in dict_archived[pays].items():
            list_sport.append(sport)
    list_sport = list(set(list_sport))

    for sport in list_sport:        
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


# =============================================================================
# RECOVER RESULTS FROM SPORT
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
#              'hockey',  
#              'esports', 
              'soccer',
              ]


# =============================================================================
# 
# =============================================================================
for sport in list_sport:
    if sport in list_sport:
        print sport
#        try:
#            test = dict_archived[sport]
#        except:
#            dict_archived.update({sport:{}})
        
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
                pays       = ligue_href.split('/')[2]
                try:
                    _ = dict_archived[pays]
                except:
                    dict_archived.update({pays:{}})
                
                try:
                    _ = dict_archived[pays][sport]
                except:
                    dict_archived[pays].update({sport:{}})

                try:
                    test = dict_archived[pays][sport][ligue_name]['done']
                except:
                    dict_archived[pays][sport].update({ligue_name:{}})
                    dict_archived[pays][sport][ligue_name].update({'href':ligue_href,'done':0, 'pays':ligue_href.split('/')[2]})
                    list_ligue.append([ligue_href.split('/')[1],ligue_href.split('/')[2],ligue_href.split('/')[3]])

### SAVE
with open('../dataset/local/dict_archived.json', 'w') as outfile:
    json.dump(dict_archived, outfile)



# =============================================================================
# DIVE INTO EACH LEAGUE OF SPORT
# =============================================================================
list_pays = [item for item, _ in dict_archived.items()]
list_pays.sort()

list_pays_prio = [
                 u'spain',
                 u'england',
                 u'italy',
                 u'france',
                 u'belgium',
                 u'israel',
                 u'mexico',
                 u'portugal',
                 u'argentina',
                 u'brazil',
                 ]

for pays_prio in list_pays_prio:
    list_pays.remove(pays_prio)
list_pays.sort()
list_pays = list_pays_prio + list_pays

#list_pays = [u'spain']

for pays in list_pays:
    print pays
    for sport, sport_v in dict_archived[pays].items():
        if sport in list_sport:
            print sport
            for ligue, ligue_v in dict_archived[pays][sport].items():
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
# DIVE INTO EACH PAGE AND EACH MATCH OF EACH LEAGUE
# =============================================================================
#%%

#dict_archived['spain']['soccer']['Super Cup']['done'] = 2

for pays in list_pays:
    print pays
    for sport, sport_v in dict_archived[pays].items():
        if sport in list_sport:
            print sport
            for ligue, ligue_v in dict_archived[pays][sport].items():
                dict_odds = {}
                try:
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
                                
                                print 'goto bs4'
                                dict_odds, count_no_bookmaker = bs4_recover_bet(soup, dict_odds, pays, sport, ligue)
                                print 'return count_no_bookmaker other page', count_no_bookmaker
                                if page_max_number !=0 and count_no_bookmaker < 7:
                                    for i in range(int(page_max_number)-1):
                                        url_ligue_year = 'https://www.oddsportal.com' + ligue_v[str(year)] + '#/page/' + str(i+2) + '/'
                                        print url_ligue_year
                                        save_web_page   = '../dataset/local/' + sport + '/oddsportal_' + sport + '_list_ligue_year.html'
                                        os.system('rm "' + save_web_page + '"')
                                        os.system('node scrap_odds_first_standalone.js ' + url_ligue_year + ' ' + save_web_page)                    
                                        ###
                                        soup              = BeautifulSoup(open(save_web_page), "html.parser")
                                        dict_odds, count_no_bookmaker = bs4_recover_bet(soup, dict_odds, pays, sport, ligue)
            
                    print 'len dict_odds', len(dict_odds)
                    if dict_odds != {}:
                        print 'save_dict 415'
                        ### SAVE
                        with open('../dataset/local/' + sport + '/oddsportal/dict_' + pays + '_' + ligue + '.json', 'w') as outfile:
                            json.dump(dict_odds, outfile)
                            
                        df_temp         = pd.DataFrame.from_dict(dict_odds, orient='index')
                        df_temp.to_csv('../dataset/local/' + sport + '/df_oddsportal_' + sport + '_' + pays + '_' + ligue + '.csv', encoding='utf-8')
                    ligue_v['done'] = 3
                    
                    
                    ### SAVE
                    print 'save_df'
                    with open('../dataset/local/dict_archived.json', 'w') as outfile:
                        json.dump(dict_archived, outfile)
                    save_df()
                        
                except Exception, e:
                    print 'error 432'
                    print e, save_web_page
                