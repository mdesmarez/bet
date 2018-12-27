#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 17:25:19 2018

@author: mathieu
"""

# =============================================================================
# IMPORT PACKAGES
# =============================================================================
import os
import datetime

import pandas             as pd

from datetime                                                                  import datetime
from datetime                                                                  import timedelta

from PS3838_scrap_function                                                     import ps3838_scrap_parlay, ps3838_scrap_single, ps3838_scrap_result
from PS3838_support_function                                                   import encode_decode
from PS3838_bet_function                                                       import ps3838_bet_single
from PS3838_dashboard                                                          import dashboard


# =============================================================================
# 
# =============================================================================
os.system('mkdir -p ../dataset/local')
os.system('mkdir -p ../model/local')

# =============================================================================
# SCRAP
# =============================================================================
#ps3838_scrap_parlay()
#GMT_to_add = ps3838_scrap_single()
#ps3838_scrap_result(GMT_to_add)


# =============================================================================
# 
# =============================================================================
###
df_parlay = pd.DataFrame.from_csv('../dataset/local/df_parlay.xls', encoding='utf-8')
df_parlay.team_home = df_parlay.team_home.apply(lambda x : encode_decode(x))
df_result = pd.DataFrame.from_csv('../dataset/local/df_result.xls', encoding='utf-8')

###
df_single = pd.DataFrame.from_csv('../dataset/local/df_single.xls', encoding='utf-8')
df_single.sport = df_single.sport.apply(lambda x : x.lower().replace('-',' '))
df_result_single = df_result.copy()
df_result_single.sport = df_result_single.sport.apply(lambda x : x.lower().replace('-',' '))

###
df_merge_parlay                           = pd.merge(df_parlay, df_result, how='inner', on=['match_date','sport','team_home'])
df_merge_parlay = df_merge_parlay[['match_date','sport','ligue','bet_1','bet_2','bet_X','bet_diff','min_bet','winner','prediction','score']]
df_merge_parlay['good_pred']              = 0
df_merge_parlay.good_pred[df_merge_parlay.prediction == df_merge_parlay.winner] = 1
df_merge_parlay['bad_pred']               = 0
df_merge_parlay.bad_pred[df_merge_parlay.prediction != df_merge_parlay.winner]  = 1
df_merge_parlay.match_date                = df_merge_parlay.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

###
df_merge_single                           = pd.merge(df_single, df_result_single, how='inner', on=['match_date','sport','team_home'])
df_merge_single = df_merge_single[['match_date','sport','ligue','bet_1','bet_2','bet_X','bet_diff','min_bet','winner','prediction']]
df_merge_single['good_pred']              = 0
df_merge_single.good_pred[df_merge_single.prediction == df_merge_single.winner] = 1
df_merge_single['bad_pred']               = 0
df_merge_single.bad_pred[df_merge_single.prediction != df_merge_single.winner]  = 1
df_merge_single.match_date                = df_merge_single.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))


dict_parameter_sport = ps3838_bet_single(df_single, df_merge_single, GMT_to_add)
dashboard(dict_parameter_sport, GMT_to_add)
