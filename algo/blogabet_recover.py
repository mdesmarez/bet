#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 13:37:10 2019

@author: mathieu
"""

# =============================================================================
# Library Call
# =============================================================================
import os
import time

import pandas as pd

from glob                           import glob
from bs4                            import BeautifulSoup



# =============================================================================
# RECOVER TIPSTER
# =============================================================================
os.system('node blogabet_tipsters.js')
soup                = BeautifulSoup(open('../dataset/local/blogabet_menu.html'), "html.parser")
candidate_list      = soup.find_all('div', { "class" : "block row no-padding-lg tipster-block"})

dict_candidate      = {}
for candidate in candidate_list:
    candidate_name = candidate.find('h3', {'class' : 'name-t u-db u-mb1'}).text
    candidate_link = candidate.find('span', {'class' : 'e-mail u-db u-mb1 text-ellipsis'}).text
    
    candidate_year      = int(candidate.find_all('div', {'class' : 'col-sh-4 col-xs-2 col-lg-2 no-padding'})[0].find('span', {'class' : 'number'}).text)
    candidate_pick      = int(candidate.find_all('div', {'class' : 'col-sh-4 col-xs-2 col-lg-2 no-padding'})[1].find('span', {'class' : 'number'}).text)
    candidate_profit    = int(candidate.find_all('div', {'class' : 'col-sh-4 col-xs-2 col-lg-2 no-padding'})[2].find('span', {'class' : 'number'}).text)
    candidate_yield     = int(candidate.find_all('div', {'class' : 'col-sh-4 col-xs-2 col-lg-2 no-padding'})[3].find('span', {'class' : 'number'}).text[:-1])
    candidate_verified  = int(candidate.find_all('div', {'class' : 'col-sh-4 col-xs-2 col-lg-2 no-padding'})[4].find('span', {'class' : 'number'}).text[:-1])
    candidate_follower  = int(candidate.find_all('div', {'class' : 'col-sh-4 col-xs-2 col-lg-2 no-padding'})[5].find('span', {'class' : 'number'}).text)
    
    candidate_paying    = candidate.find_all('span', {'class': 'tipster-price'})
    if candidate_paying != []:
        candidate_paying    = 1
    else:
        candidate_paying    = 0
        
    dict_candidate.update({candidate_name:{
                                            'candidate_year':candidate_year,
                                            'candidate_pick':candidate_pick,
                                            'candidate_profit':candidate_profit,
                                            'candidate_yield':candidate_yield,
                                            'candidate_verified':candidate_verified,
                                            'candidate_follower':candidate_follower,
                                            'candidate_paying':candidate_paying,
                                            'candidate_link':candidate_link,
                                            }})

df_candidate_blogabet = pd.DataFrame.from_dict(dict_candidate, orient='index')

#%%
# =============================================================================
# RECOVER TIPSTER TIPS
# =============================================================================
#dict_result         = {}

for i in range(len(df_candidate_blogabet)):
    candidate_link = 'https://' + df_candidate_blogabet.candidate_link.iloc[i]
    print '*****************'
    print candidate_link
    try:
        os.system('rm ../dataset/local/blogabet_details.html')
        os.system('node blogabet_tipsters_details.js "' + candidate_link + '"')
        soup                = BeautifulSoup(open('../dataset/local/blogabet_details.html'), "html.parser")
        candidate_list      = soup.find_all('div', { "class" : "media-body"})
    
        for j, candidate in enumerate(candidate_list):
            candidate_name      = '' 
            candidate_sport     = ''
            candidate_pays      = ''
            candidate_date      = ''
            candidate_result    = ''
            
            try:
                candidate_name      = candidate.find('h3').text.strip()
                print ' * ', candidate_name, j, len(candidate_list)
                candidate_detail    = candidate.find('div', { "class" : "sport-line"}).find_all('small', { "class" : "text-muted"})[0].text
                candidate_sport     = candidate_detail.split('/')[0].strip()
                candidate_pays      = candidate_detail.split('/')[1].strip()
                candidate_date      = candidate_detail.split('/')[2].strip().split('off:')[-1].strip()
                
                candidate_pick      = candidate.find('div', { "class" : "pick-line"})
                candidate_bet_type  = candidate_pick.text.strip().split('@')[0].strip()
                candidate_bet       = candidate_pick.text.strip().split('@')[1].strip()
                
                candidate_label     = candidate.find('div', { "class" : "labels"})
                candidate_result_bulk = candidate_label.text
                if candidate_label.find_all('span', {'data-original-title':'WIN'}) != []:
                    candidate_result = 'WIN'
                if candidate_label.find_all('span', {'data-original-title':'LOST'}) != []:
                    candidate_result = 'LOST'
                    
                candidate_UID       = candidate_name + '__' + candidate_date
                
                try:
                    _ = dict_result[candidate_UID]
                except:
                    dict_result.update({candidate_UID:{}})
                    
                dict_result[candidate_UID].update({df_candidate_blogabet.index[i]:{
                                                'candidate_name':candidate_name,
                                                'candidate_sport':candidate_sport,
                                                'candidate_pays':candidate_pays,
                                                'candidate_date':candidate_date,
                                                'candidate_bet_type':candidate_bet_type,
                                                'candidate_bet':candidate_bet,
                                                'candidate_result':candidate_result,
                                                'candidate_result_bulk':candidate_result_bulk,
                                                }})
            except Exception,e:
                print 'ERROR :',e, candidate_name
        time.sleep(0.5)
    
    except Exception,e:
        print 'ERROR PUPPETTER :',e, candidate_name
ee


#%%

for k,v in dict_result.items():
    if len(dict_result[k]) > 2:
        print k, len(dict_result[k])
        
    
    


