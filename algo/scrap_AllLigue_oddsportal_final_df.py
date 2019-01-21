#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 13:01:13 2019

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
# 
# =============================================================================
with open('../dataset/local/dict_archived.json') as json_file:  
    dict_archived = json.load(json_file)
    
for sport, sport_v in dict_archived.items():
    print sport
#    sport = 'soccer'
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
