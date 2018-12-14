#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 16:04:55 2018

@author: mathieu
"""

# =============================================================================
# 
# =============================================================================
import os
import datetime
import cPickle
import time

import numpy                                                                   as np
import pandas                                                                  as pd

from glob                                                                      import glob
from datetime                                                                  import timedelta
from datetime import datetime
from random                                                                    import shuffle
from random                                                                    import randint

import warnings

warnings.filterwarnings(action='ignore')


import xgboost                                                                 as xgb
import matplotlib.pyplot                                                       as plt

from glob                                                                      import glob
from xgboost.sklearn                                                           import XGBClassifier
from sklearn.model_selection                                                   import train_test_split
from sklearn.metrics                                                           import confusion_matrix, f1_score
from sklearn.grid_search                                                       import GridSearchCV
from sklearn                                                                   import metrics
from sklearn                                                                   import preprocessing



# =============================================================================
# GRID GENERATOR
# =============================================================================

#list_year           = [2016, 2017, 2018] 
list_year           = [2018] 
list_season_weaks_target   = np.linspace(25,  80,  55+1).astype(int)

#list_season_weaks_target = [49]

list_years_target   = np.linspace(2014,  2018,  4+1).astype(int)

mise = 1


list_bet_max        = np.linspace(2,  3,   3+1).astype(float)
list_bet_min        = np.linspace(1.2, 1.5,  2+1).astype(float)
list_bet_ecart      = np.linspace(2,   2.5,  1+1).astype(float)
list_target         = np.linspace(3,   4,  1+1).astype(int)


list_grid = []
for bet_max in list_bet_max:
    for bet_min in list_bet_min:
        for bet_ecart in list_bet_ecart:
            for target in list_target:
                list_grid.append([bet_max, bet_min, bet_ecart, target])
       
shuffle(list_grid)             
shuffle(list_grid)             
shuffle(list_grid)   

#
##########################
#bet_max     = 3
#bet_min     = 1.25
#bet_ecart   = 2
#target      = 3
#rep_target  = 5
#
#list_grid = [[bet_max, bet_min, bet_ecart, target]]
#mise = 1
##########################




# =============================================================================
# FUNCTIONS
# =============================================================================
def preprocessing_data(df):
    df['date_match'] = df.match_date.apply(lambda x : (datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')))
    df.sort_values('date_match', inplace =True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    df.date_match = pd.to_datetime(df.date_match)
    
    df['season']        = df.date_match.apply(lambda x : x.year if x.month >= 7 else x.year-1)
    df['season_week']   = df.date_match.apply(lambda x : x.week+52 if x.week <= 25 else x.week)
    
    df['ligue']        = df['pays'] + '_' + df['ligue']
    
    df.reset_index(drop=False, inplace=True)
    df.set_index('date_match', drop=True, inplace=True)
    
    df.drop_duplicates('match_id', inplace=True)
    
    return df
    

def match_selection(df, season_weaks_target, season_weaks_before, season_weaks_after, season=2018, pays='', ligue=''):
    
    df                  = df[df.season == season]
    df['to_predict']    = 0
    
    df                  = df[df.season_week >= season_weaks_target-season_weaks_before]
    df                  = df[df.season_week <= season_weaks_target+season_weaks_after]
    df.to_predict[df.season_week >= season_weaks_target] = 1    
    
    if pays != '':
        df = df[df.pays == pays]
    if ligue != '':
        df = df[df.ligue == ligue]
    
    return df
    

def match_filter_prediction(df, bet_max, bet_min, bet_ecart):
    #####
    df = df[(df.bet_1 < bet_max) | (df.bet_2 < bet_max)]
    
    #####
    df = df[(df.bet_1 > bet_min) & (df.bet_2 > bet_min)]
    
    ####
    df = df[abs(df.bet_1 - df.bet_2) > bet_ecart]
    
    df['bet_diff']              = df.bet_1 - df.bet_2
    df['prediction']            = df.bet_diff.apply(lambda x : "1" if x<0 else "2")
    df['result']                = df.result.apply(lambda x : str(x))
    
    df['good_pred']                          = 0
    df.good_pred[df.prediction == df.result] = 1
    df['bad_pred']                           = 0
    df.bad_pred[df.prediction != df.result]  = 1

    
    return df



def match_result_calcul(df):
    list_bet_result     = df.result_bet.tolist()
    number_good_pred    = 0
    gain                = 0
    perte               = 0
    bet_parlay          = 0

    ### NORMAL BET        
    bet_parlay          = list_bet_result[0]
    number_good_pred    = df.good_pred.sum()

    for i, item in enumerate(list_bet_result):
        if i != 0:
            bet_parlay = bet_parlay*item
        if item > 3 and target == number_good_pred:
            eerree
            
    if target == number_good_pred:
        gain            = bet_parlay*mise
#        print 'COOL : ', gain
    else:
        bet_parlay      = 0
#        print('....')
    perte           = mise
        
    return gain, perte, bet_parlay
        
    


def find_best_and_predict(df):
    df_train = df[df.to_predict == 0]
    list_season_weaks_train  = df_train.season_week.unique()

    df_test = df[df.to_predict == 1]

    # =============================================================================
    #     
    # =============================================================================
    ### ITERATE TO FIND BEST PARAMETERS
    best_ratio = -1000
    best_grid  = 0
    for grid in list_grid:
#        print grid
        bet_max, bet_min, bet_ecart, target = grid  
    
        gain_train          = 0 
        perte_train         = 0
        gain_train_best     = 0
        perte_train_best    = 0
        gain_test           = 0 
        perte_test          = 0
        bet_parlay_test     = 0
        
        for iteration in range(1):
            for season_weak_train in list_season_weaks_train:
#                print 'season : ', season, ' week : ', season_weak_train
                df_train_season_weak = df_train[df_train.season_week == season_weak_train]
    
                ### FILTER MATCH
                df_train_season_weak_prediction = match_filter_prediction(df_train_season_weak, bet_max, bet_min, bet_ecart)
                
                ### CHECK IF ENOUGH MATCH
                if len(df_train_season_weak_prediction) >= target:
                    df_train_season_weak_prediction = df_train_season_weak_prediction[df_train_season_weak_prediction.match_id.isin(df_train_season_weak_prediction.sample(target).match_id)]
                
                    ### CALCUL RESULT OF TRAIN
                    gain, perte, bet_parlay = match_result_calcul(df_train_season_weak_prediction)
                    gain_train  = gain_train  + gain 
                    perte_train = perte_train + perte 
    
        gain_train  = gain_train/float(iteration+1)
        perte_train = perte_train/float(iteration+1)
        ratio_train = gain_train-perte_train
#        print 'gain_train : ', gain_train
#        print 'perte_train : ', perte_train
#        print 'ratio_train : ', ratio_train

        if ratio_train > best_ratio:
            best_ratio = ratio_train
            best_grid = grid
            gain_train_best = gain_train
            perte_train_best = perte_train
            print 'best', best_grid, ratio_train
            
    # =============================================================================
    # 
    # =============================================================================
    bet_max, bet_min, bet_ecart, target = best_grid  
    for iteration in range(5):
        ### CALCUL RESULT OF PREDICTION
        df_test = match_filter_prediction(df_test, bet_max, bet_min, bet_ecart)
        if len(df_test) >= target:
            df_test = df_test[df_test.match_id.isin(df_test.sample(target).match_id)]
            gain_test, perte_test, bet_parlay_test = match_result_calcul(df_test)
        print 'gain_train : ', gain_train_best
        print 'perte_train : ', perte_train_best
        print 'gain_test : ', gain_test
        print 'perte_test : ', perte_test
    
    return 0 


def train_eval(df, season):
    
    df_score_all = df.copy()
    df_score_all.set_index('match_id', inplace=True)
    
    ### SELECT SEASON
    df_pred         = df_score_all[df_score_all.season == season]
    df_score_all    = df_score_all[~(df_score_all.season == season)]
    
#    le = preprocessing.LabelEncoder()
#    df_score_all.pays = le.fit_transform(df_score_all.pays)
#    df_score_all = df_score_all[['bet_1','bet_X','bet_2','pays','result']]
    
    df_score_all = df_score_all[['bet_1','bet_X','bet_2','result']]
    
    df_pred = df_pred[['bet_1','bet_X','bet_2']]
    
    split=0.1
    # =============================================================================
    #  PROCESS DATA FORMAT
    # =============================================================================
    X       = df_score_all.copy()
    del X['result']
    
    columns = df_score_all.columns
    features_name = X.columns
    
    df_score_all.result[df_score_all.result == 'X'] = 0
    y       = df_score_all['result']
    y = y.astype('int')
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=split, random_state=1)
    X_train = X_train.as_matrix().astype('float32')
    X_val = X_val.as_matrix().astype('float32')
    
    #del df, X, y
    xg_train = xgb.DMatrix(X_train, label=y_train, feature_names=features_name)
    xg_val = xgb.DMatrix(X_val, label=y_val, feature_names=features_name)
    
    
    # =============================================================================
    #  PROCESS DATA FORMAT
    # =============================================================================
    X_pred   = df_pred.copy()
    
    columns = df_pred.columns
    features_name = X_pred.columns
    
    
    X_pred = X_pred.as_matrix().astype('float32')
    
    #del df, X, y
    xg_pred = xgb.DMatrix(X_pred, feature_names=features_name)
    
    
    
    
    # =============================================================================
    # TRAIN MODEL PHASE#1: Determine best n_estimators
    # =============================================================================
    params = {
            'booster': 'gbtree',
    #        'tree_method': 'exact',
            'n_estimators': 256,
    #        'grow_policy': 'lossguide',
#            'objective': 'binary:hinge',#'binary:logistic',
            'objective': 'multi:softmax',
#            'eval_metric': 'auc',
            'eval_metric': 'merror',
            'early_stopping_round': 20,
            'scale_pos_weight': 1,# (len(y)-y.sum())/float(y.sum()),
    #        'max_bin' : 3,
            'num_class': 3,
            }
    
    watchlist = [ (xg_train,'train'), (xg_val, 'valid') ]
    
    model = xgb.train(params=params,
                      dtrain=xg_train,
                      num_boost_round=params['n_estimators'],
                      early_stopping_rounds=params['early_stopping_round'],
                      evals=watchlist)

    
    y_pred_init = model.predict(xg_val, ntree_limit=model.best_ntree_limit)
    y_pred = y_pred_init
    
#    thres == 0.5
#    y_pred[y_pred_init <= thres] = 0
#    y_pred[y_pred_init > thres] = 1
    cm = confusion_matrix(y_val,y_pred)
    print y.sum()/float(len(y))
    print cm[1][1]/float(cm[0][1])
    print cm[1][1]/float(cm[0][1]+cm[1][1])
    
    y_val.reset_index(drop=True, inplace=True)
    a = pd.concat((pd.DataFrame(y_val),pd.DataFrame(y_pred)), axis=1)
    a['good'] = 0
    a.columns = ['result', 'true', 'good']
    a.good[a.result == a.true] = 1

    # =============================================================================
    # 
    # =============================================================================
    y_pred = model.predict(xg_pred, ntree_limit=model.best_ntree_limit)


    return a, cm, y_pred




    
def result(df_foot_scores):
    
    df_foot_scores.set_index('match_id', drop=False, inplace=True)
    
    a                                       = df_foot_scores[((df_foot_scores.prediction == df_foot_scores.result))]
    b                                       = df_foot_scores[~((df_foot_scores.prediction == df_foot_scores.result))]
    #a                                       = df_foot_scores[((df_foot_scores.prediction == df_foot_scores.result) | (df_foot_scores.result == 'X'))]
    #b                                       = df_foot_scores[~((df_foot_scores.prediction == df_foot_scores.result) | (df_foot_scores.result == 'X'))]
    
    a['good_pred']                          = 1
    b['bad_pred']                           = 1
    
    print('******')
    if len(df_foot_scores) == 0 :
        ratio = 0    
    else:
        ratio = len(a)/float(len(df_foot_scores))
    print ratio
    print('******')
    
    
    df_foot_scores = pd.concat((df_foot_scores,a['good_pred'],b['bad_pred']),axis=1)
    df_foot_scores.fillna(0, inplace=True)
    
    bet_mean = df_foot_scores.result_bet[df_foot_scores.good_pred == 1].values.mean()
    
    print bet_mean*len(a)*mise - len(a+b)*mise 
    

    


    df_foot_scores = df_foot_scores[
                                    [u'good_pred', u'bad_pred', u'result', u'prediction', u'index', u'bet_1', u'bet_X', u'bet_2', u'result_bet',
                                     u'score', u'score_home', u'score_away',       
                                     u'pays', u'ligue', u'season', u'season_week', u'match_name', u'match_id']
                                    ]
    return df_foot_scores

# =============================================================================
# 
# =============================================================================
"""
df = df_filter.copy()

a, cm, y_pred = train_eval(df, season)

df_pred         = df[df.season == season]

df_pred['y_pred'] = y_pred
df_pred.y_pred = df_pred.y_pred.astype('int')
df_pred.y_pred = df_pred.y_pred.astype('str')
df_pred.y_pred[df_pred.y_pred == '0'] = 'X'


df_filter = match_filter_prediction(df_pred, bet_max, bet_min, bet_ecart)

df_filter = df_pred.copy()

df_filter['good_pred_xg']                      = 0
df_filter.good_pred_xg[df_filter.y_pred == df_filter.result] = 1
df_filter['bad_pred_xg']                       = 0
df_filter.bad_pred_xg[df_filter.y_pred != df_filter.result]  = 1

print ''
print ''
print ''
print 'pred filter : '
print df_filter.good_pred.sum()/float(len(df_filter))
print 'pred XG : '
print df_filter.good_pred_xg.sum()/float(len(df_filter))

ee

"""

def match_statistique(df_filter, list_season):
    df_filter                           = df_filter[df_filter.season.isin(list_season)]    
    df_filter['season_season_week']     = df_filter.season.apply(lambda x: str(x)) + '_' + df_filter.season_week.apply(lambda x: str(x))
    good_pred_ratio                     = df_filter.good_pred.sum()/float(len(df_filter))
    nbr_match_moy_semaine               = df_filter.groupby('season_season_week').count()['match_id'].mean()
    bet_moyen                           = df_filter.result_bet[df_filter.good_pred == 1].mean()
    target_calcul                       = int(good_pred_ratio*nbr_match_moy_semaine)
    return good_pred_ratio, bet_moyen, target_calcul, nbr_match_moy_semaine


def match_statistique_print(good_pred_ratio, bet_moyen, target_calcul, nbr_match_moy_semaine):
    print 'good_pred_ratio : ', round(good_pred_ratio*100,2)
    print 'nbr match année : ', df_filter.season.value_counts().values[0]
    print 'nbr_match_moy_semaine : ', int(nbr_match_moy_semaine)
    print 'bet_moyen : ', round(bet_moyen,2)
    print 'perf_global X nbr_match_moy_semaine (target_calcul) : ', target_calcul
    print '-'
    print 'bet_moyen ^ target : ', bet_moyen**target
    print 'good_pred_ratio ^ target : ', good_pred_ratio**target*100
    print 'good_pred_ratio ^ target * 33: ', good_pred_ratio**target*33*100
    print ''
#    print 'bet_moyen ^ target_calcul : ', bet_moyen**target_calcul
#    print 'good_pred_ratio ^ target_calcul : ', good_pred_ratio**target_calcul*100
#    print 'good_pred_ratio ^ target_calcul * 33: ', good_pred_ratio**target_calcul*33*100
#    print ''



# =============================================================================
# LOAD DATASET
# =============================================================================

##########################    
season_weaks_after      = 0
season_weaks_before     = 0 
season                  = 2017
list_season             = [2017]
list_sport              = ['handball','soccer']
pays                    = ''
ligue                   = ''

mise                    = 10
##########################
dict_parameter   = {'handball':{
                                'bet_max'     : 6,
                                'bet_min'     : 1.15,
                                'bet_ecart'   : 3,
                                'target'      : 2,
                                'rep_target'  : 1,
                                },
                    'soccer':{
                                'bet_max'     : 6,
                                'bet_min'     : 1.15,
                                'bet_ecart'   : 5,
                                'target'      : 2,
                                'rep_target'  : 1,
                                }
                    }
                    


# =============================================================================
# LOAD DATASET
# =============================================================================
df_foot_scores_init = pd.read_csv('../dataset/local/df_ALL.xls', encoding='utf-8')
df_foot_scores_init = preprocessing_data(df_foot_scores_init)

for sport in list_sport:
    print '***********************************'
    print 'SPORT : ', sport
    bet_max     = dict_parameter[sport]['bet_max']
    bet_min     = dict_parameter[sport]['bet_min']
    bet_ecart   = dict_parameter[sport]['bet_ecart']
    target      = dict_parameter[sport]['target']
    rep_target  = dict_parameter[sport]['rep_target']
    
    # =============================================================================
    # FILTER MATCHS
    # =============================================================================    
    df_filter           = match_filter_prediction(df_foot_scores_init, bet_max, bet_min, bet_ecart)
    df_filter           = df_filter[df_filter.sport == sport]

    
    # =============================================================================
    # STATISTIQUE MATCHS
    # =============================================================================
    good_pred_ratio, bet_moyen, target_calcul, nbr_match_moy_semaine = match_statistique(df_filter, list_season)
    match_statistique_print(good_pred_ratio, bet_moyen, target_calcul, nbr_match_moy_semaine)
    
ee

    
#### 
#list_ligue = df_filter.ligue[df_filter.bad_pred == 1].value_counts().index.tolist()
#dict_perf_ligue = {}
#list_keep_ligue = []
#for ligue in list_ligue:
#    df_temp = df_filter[df_filter.ligue == ligue]
##    print ligue
#    perf_ligue = df_temp.ligue[df_temp.good_pred == 1].value_counts().sum()/float(len(df_temp))
#    dict_perf_ligue.update({ligue:perf_ligue})
##    print perf_ligue
#    if perf_ligue > perf_global-0.03:
#        list_keep_ligue.append(ligue)
#
#df_filter = df_filter[df_filter.ligue.isin(list_keep_ligue)]
#perf_global = df_filter.good_pred.sum()/float(len(df_filter))
#nbr_match_moy_semaine = df_filter.groupby('season_season_week').count()['match_id'].mean()
#bet_moyen = df_filter.result_bet[df_filter.good_pred == 1].mean()
#target_calcul = int(perf_global*nbr_match_moy_semaine)
    


pays                    = ''
ligue                   = ''
list_ligue              = df_filter.ligue.unique().tolist()
list_ligue              = ['']


gain_total              = 0
perte_total             = 0
ratio_total             = 0


dict_bankroll           = {}
dict_ratio_GP           = {}
### TRY OVER ALL WEEKS 
for ligue in list_ligue:
    print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
    print 'LIGUE :', ligue
    ratio_GP                = 0
    previous_ratio_GP       = 100
    seuil_ratio_GP          = 10.5
    for season_weaks_target in list_season_weaks_target:
#        time.sleep(0.2)                
        for rep in range(rep_target):
            print '***************************************************************'
            print 'season_weaks_target :', season_weaks_target
            df_foot_scores_filter = match_selection(df_filter, season_weaks_target, season_weaks_before, season_weaks_after, season, pays, ligue)
    
            if len(df_foot_scores_filter) > 0:
                ratio_GP            = df_foot_scores_filter.good_pred.sum()/float(len(df_foot_scores_filter))
            else:
                ratio_GP            = 99
        
            if len(df_foot_scores_filter) >= target and previous_ratio_GP < seuil_ratio_GP:
                df_test = df_foot_scores_filter[df_foot_scores_filter.match_id.isin(df_foot_scores_filter.sample(target).match_id)]
        
                gain_test, perte_test, bet_parlay_test = match_result_calcul(df_test)
                gain_total          = gain_total + gain_test
                perte_total         = perte_total + perte_test
                ratio_total         = gain_total - perte_total
                
                print 'ratio_total : ', ratio_total
                print 'gain_test : ', gain_test
                print 'perte_test : ', perte_test
                print 'bet_parlay_test : ', bet_parlay_test
                print 'potential good : ' , df_foot_scores_filter.good_pred.sum()
                print 'match week : ', len(df_foot_scores_filter)
                print 'ratio_GP : ', ratio_GP
                print 'previous_ratio_GP : ', previous_ratio_GP
                
                dict_bankroll.update({season_weaks_target: ratio_total})
                
                try:
                    _ = dict_ratio_GP[ligue]
                except:
                    dict_ratio_GP.update({ligue:{}})
                    
                dict_ratio_GP[ligue].update({season_weaks_target: ratio_GP})
            else:
                print 'match week : ', len(df_foot_scores_filter)
                print 'ratio_GP : ', ratio_GP

            previous_ratio_GP = ratio_GP
        
print gain_total - perte_total

if gain_total-perte_total >-100:
    df_bankroll = pd.DataFrame.from_dict(dict_bankroll, orient='index')
    df_bankroll.sort_index(ascending=True, inplace=True)
    df_bankroll.plot()
#
#
#df_ratio = pd.DataFrame.from_dict(dict_ratio_GP, orient='index').T
#df_ratio.sort_index(ascending=True, inplace=True)
#df_ratio.plot()
#
#print df_ratio.mean()

ee


#df_foot_scores_init = df_foot_scores_init[df_foot_scores_init.season_week >= 35]


### TRY OVER ALL WEEKS 
for season_weaks_target in list_season_weaks_target:
    time.sleep(0.5)
    print '***************************************************************'
    print 'season_weaks_target :', season_weaks_target
    df_foot_scores_filter = match_selection(df_foot_scores_init, season_weaks_target, season_weaks_before, season_weaks_after, season, pays, ligue)

    df = df_foot_scores_filter.copy()
            
    ratio  = find_best_and_predict(df_foot_scores_filter)
ee







for grid in list_grid:
    bet_max, bet_min, bet_ecart, target, rep_target = grid  
  
    ### LOAD 
    try:
        with open('../dataset/local/dict_grid.json') as f:
            dict_result = cPickle.load(f) 
    except:
        dict_result={}   
            
    
   
    
    
    
    
    
for i in range(0):   
    
    df_foot_scores = df_foot_scores_init.copy()
    
    #####
    df_foot_scores = df_foot_scores[(df_foot_scores.bet_1 < bet_max) | (df_foot_scores.bet_2 < bet_max)]
    
    #####
    df_foot_scores = df_foot_scores[(df_foot_scores.bet_1 > bet_min) & (df_foot_scores.bet_2 > bet_min)]
    
    ####
    df_foot_scores = df_foot_scores[abs(df_foot_scores.bet_1 - df_foot_scores.bet_2) > bet_ecart]
    
    
    df_foot_scores['bet_diff']              = df_foot_scores.bet_1 - df_foot_scores.bet_2
    df_foot_scores['prediction']            = df_foot_scores.bet_diff.apply(lambda x : "1" if x<0 else "2")
    df_foot_scores['result']                = df_foot_scores.result.apply(lambda x : str(x))
    
    df_foot_scores = result(df_foot_scores)
    
    
    
    # =============================================================================
    # FILTER DAYS AND WEEK
    # =============================================================================
#    df_foot_scores = df_foot_scores[df_foot_scores.index.dayofweek >= 4]
#    df_foot_scores = df_foot_scores[df_foot_scores.index.month < 11]
#    df_foot_scores = df_foot_scores[df_foot_scores.index.month > 7]
#    df_foot_scores = df_foot_scores[df_foot_scores.index.week == 44]
#    df_foot_scores = df_foot_scores[df_foot_scores.index.week >= 40]
    
    RATIO_MEAN      = 0
    GAIN_TOTAL_MEAN = 0
    COUT_TOTAL_MEAN = 0
    nbr_good_pred   = 0
    nbr_pred        = 0
    
    for year in list_year:
        print('###############################################################')
        print year
        df_foot_scores_year = df_foot_scores[df_foot_scores.index.year == year]
        list_week = df_foot_scores_year.index.week.unique().tolist()
        list_week.sort()
        
        print('******')
        if len(df_foot_scores_year) == 0 :
            ratio = 0    
        else:
            ratio = (df_foot_scores_year.good_pred.sum())/float(len(df_foot_scores_year))
        print ratio
        print('******')
        
        df_bad_pred = df_foot_scores_year.pays[df_foot_scores_year.bad_pred == 1]
        print df_bad_pred.value_counts()



        exec('gain_'+str(year)+' = 0')
        exec('cout_'+str(year)+' = 0')
        # =============================================================================
        # OLD OK
        # =============================================================================        
        for rep in range(1):
            dict_gain_week = {}
            GAIN_TOTAL = 0
            COUT_TOTAL = 0
            
            for week in list_week:        
                df_test = df_foot_scores_year[df_foot_scores_year.index.week == week]
                gain_week   = 0
                cout_week   = 0
            
            #    if week == 40:
            #        break
            #
            #        
            #    if len(df_test) < target*2:
            #        break
            
                
                try:
                    for i in range(target*rep_target):
                        a           = df_test[df_test.match_id.isin(df_test.sample(target).match_id)]
                        aaa         = a.result_bet.tolist()
                        aa          = 0
                        
#                        ### premier doucble chance
#                        if a.iloc[0].result==a.iloc[0].prediction or a.iloc[0].result=='X':
#                            aa = 1
#                        aa          = aa + a.good_pred.iloc[1:target].sum()
#                        bet_mean_2 = 1.2

                        ### NORMAL BET        
                        bet_mean_2 = aaa[0]
                        aa          = a.good_pred.sum()
        
                        
                        for ii, item in enumerate(aaa):
                            if ii != 0:
                                bet_mean_2 = bet_mean_2*(item-0.)
                        
                                                
                        if target == aa:
            #                print('OK OK PODIUM !!!! ' + str(bet_mean_2) + ' ' + str(aaa))
                            gain_week  = gain_week + bet_mean_2*mise
                            GAIN_TOTAL = GAIN_TOTAL + bet_mean_2*mise
                            exec('gain_'+str(year)+' = gain_'+str(year)+'+'+str(bet_mean_2*mise))
                            nbr_good_pred = nbr_good_pred + 1
            #                print 'GAIN_TOTAL ', GAIN_TOTAL, gain_week, bet_mean_2

#                            if year == 2018 and bet_mean_2 > 100:
#                                ee
            
                        nbr_pred   = nbr_pred + 1
                        cout_week  = cout_week + mise   
                        COUT_TOTAL = COUT_TOTAL + mise
                        exec('cout_'+str(year)+' = cout_'+str(year)+'+'+str(mise))

#                    print a.good_pred.tolist()
#                    print('******************')
#                    print('******************')
#                    print('Year      : ' + str(year))
#                    print('Week      : ' + str(week))
#                    print('Nbr Match : ' + str(len(df_test)))
#                    print('Bet cout  : ' + str(cout_week))
#                    print('Bet gain  : ' + str(gain_week))
#                    print('Bet Net   : ' + str(gain_week-cout_week))
#                    print('******************')
#                    print('******************')
                    
                    dict_gain_week.update({week:(gain_week-target)*mise})
                    
                
                        
                except Exception,e :
                    pass
#                    if year == 2018 and bet_mean_2 > 100:
#                        ee
        #            print e
                    
            #    if week == 41:
            #        break
                    
        #    print GAIN_TOTAL
        #    print COUT_TOTAL        
        #    print GAIN_TOTAL-COUT_TOTAL
            
            GAIN_TOTAL_MEAN = GAIN_TOTAL_MEAN + GAIN_TOTAL
            COUT_TOTAL_MEAN = COUT_TOTAL_MEAN + COUT_TOTAL
            
            if COUT_TOTAL_MEAN == 0:
                RATIO_MEAN      = RATIO_MEAN
            else:
                RATIO_MEAN      = RATIO_MEAN + (GAIN_TOTAL_MEAN / COUT_TOTAL_MEAN)
            
    print ''
    print ''        
    print GAIN_TOTAL_MEAN/(rep+1)
    print COUT_TOTAL_MEAN/(rep+1)   
    GAIN_BET_MEAN = (GAIN_TOTAL_MEAN-COUT_TOTAL_MEAN)/(rep+1)
    print ' ==> ', GAIN_BET_MEAN
    
    if COUT_TOTAL_MEAN == 0:
        ratio = 0
    else:
        ratio = GAIN_TOTAL_MEAN/float(COUT_TOTAL_MEAN)
    print ratio
    print ''
    print ''
    
    dict_result.update({randint(0,100000):{'bet_max'       : bet_max,
                                                  'bet_min'       : bet_min,
                                                  'bet_ecart'     : bet_ecart, 
                                                  'target'        : target, 
                                                  'rep_target'    : rep_target,
                                                  'GAIN_BET_MEAN' : GAIN_BET_MEAN,
                                                  'ratio'         : RATIO_MEAN/float(len(list_year)),
                                                    }})
        
#    with open('../dataset/local/dict_grid.json', 'w') as outfile:
#            cPickle.dump(dict_result, outfile)


df_result = pd.DataFrame.from_dict(dict_result, orient='index')



"""
# =============================================================================
# 
# =============================================================================
GAIN_TOTAL_MEAN = 0
COUT_TOTAL_MEAN = 0

dict_gain_week = {}
GAIN_TOTAL = 0
COUT_TOTAL = 0
    
for week in list_week:        
        df_test = df_foot_scores[df_foot_scores.index.week == week]
        
        mise        = 1
        target      = 5
        gain_week   = 0
        cout_week   = 0    
        
        try:
            for i in range(target*2):
                ### SAMPLE
                df_sample       = df_test[df_test.match_id.isin(df_test.sample(target).match_id)]
                                
                # =============================================================================
                # First Bet no X
                # =============================================================================                
                list_bet_1      = df_sample.result_bet.tolist()
                bet_mean_1      = list_bet_1[0]
                nbr_goodpred_1  = df_sample.good_pred.sum()

                for ii, item in enumerate(list_bet_1):
                    if ii != 0:
                        bet_mean_1 = bet_mean_1*item
                
                if nbr_goodpred_1 == target:
                    gain_week  = gain_week + bet_mean_1*mise
                    GAIN_TOTAL = GAIN_TOTAL + bet_mean_1*mise
    
                cout_week  = cout_week + mise
                COUT_TOTAL = COUT_TOTAL + mise
                
                
                # =============================================================================
                # Second Bet with X
                # =============================================================================                
                list_bet_2      = [df_sample.result_bet.iloc[0].tolist()] + df_sample.result_bet.iloc[1:target].tolist()
                bet_mean_2      = list_bet_2[0]
                
                if df_sample.iloc[0].result=='X':
                    nbr_goodpred_2 = 1
                else:
                    nbr_goodpred_2 = 0
                    
                nbr_goodpred_2     = nbr_goodpred_2 + df_sample.good_pred.iloc[1:target].sum()


                for ii, item in enumerate(list_bet_2):
                    if ii != 0:
                        bet_mean_2 = bet_mean_2*item
                
                if nbr_goodpred_2 == target:
                    gain_week  = gain_week + bet_mean_2*mise
                    GAIN_TOTAL = GAIN_TOTAL + bet_mean_2*mise
    
                cout_week  = cout_week + mise
                COUT_TOTAL = COUT_TOTAL + mise
                
                
            
            print('******************')
            print('******************')
            print('Week      : ' + str(week))
            print('Nbr Match : ' + str(len(df_test)))
            print('Bet cout  : ' + str(cout_week))
            print('Bet gain  : ' + str(gain_week))
            print('Bet Net   : ' + str(gain_week-cout_week))
            print('******************')
            print('******************')
            
            dict_gain_week.update({week:(gain_week-target)*mise})
            
        except Exception,e :
            print e
            
    #    if week == 41:
    #        break
            
print GAIN_TOTAL
print COUT_TOTAL        
print GAIN_TOTAL-COUT_TOTAL
   

    

ee
"""


"""
# =============================================================================
# 
# =============================================================================

bet_mise         = 1

bet_align        = 100
number_bet_align = 1


df_foot_scores = df_foot_scores.iloc[:(bet_align*number_bet_align)]
a   = df_foot_scores.good_pred.tolist()
aa  = df_foot_scores.result_bet.tolist()

dict_result = {}
victory = 0
bet_mean_global = 0
for j in range(number_bet_align):
    dict_result.update({j:{}})
    result = 1
    bet_moyen = 0
    for i in range(bet_align):
        bet_moyen = bet_moyen + aa[i+j*bet_align]
        if a[i+j*bet_align] == 0:
            result = 0
    if result == 1:
        dict_result[j] = bet_moyen/float(bet_align)
        victory = victory + 1
        bet_mean_global = bet_mean_global + bet_moyen/float(bet_align)
    else:
        dict_result[j] = 0
        
bet_mean_global = bet_mean_global/float(victory)

bet_mean_global = 1.15

bet_cost = number_bet_align*bet_mise
bet_gain = bet_mean_global ** bet_align * victory*bet_mise

bet_net = bet_gain - bet_cost

print('******************')
print('******************')
print('Victory : ' + str(victory))
print('Bet ratio : ' + str(victory/float(number_bet_align)))
print('Bet Net : ' + str(bet_net))
print('******************')
print('******************')

aaa = df_foot_scores[df_foot_scores.bad_pred == 1]
print aaa.result.value_counts()
"""

"""
# =============================================================================
# diff between bet
# =============================================================================
df_foot_scores = pd.DataFrame()
list_ligue = glob('../dataset/local/*.csv')

for item in list_ligue:    
    df_foot_scores_temp = pd.read_csv(item, index_col=0, encoding='utf-8')
    df_foot_scores = pd.concat((df_foot_scores, df_foot_scores_temp))


bet_ = 0.35
df_foot_scores = df_foot_scores[abs(df_foot_scores.bet_1 - df_foot_scores.bet_2) > bet_]

df_foot_scores['bet_diff']              = df_foot_scores.bet_1 - df_foot_scores.bet_2
df_foot_scores['prediction']            = df_foot_scores.bet_diff.apply(lambda x : "1" if x<0 else "2")

#a                                       = df_foot_scores[((df_foot_scores.prediction == df_foot_scores.result))]
#b                                       = df_foot_scores[~((df_foot_scores.prediction == df_foot_scores.result))]
a                                       = df_foot_scores[((df_foot_scores.prediction == df_foot_scores.result) | (df_foot_scores.result == 'X'))]
b                                       = df_foot_scores[~((df_foot_scores.prediction == df_foot_scores.result) | (df_foot_scores.result == 'X'))]


a, b, df_foot_scores = result(a, b, df_foot_scores)
"""

"""
#%% =============================================================================
# 
# =============================================================================
df_foot_scores_bundesliga   = pd.read_csv('../dataset/local/df_oddsportal_bundesliga.csv', index_col=0, encoding='utf-8')
df_foot_scores_laliga       = pd.read_csv('../dataset/local/df_oddsportal_laliga.csv', index_col=0, encoding='utf-8')
df_foot_scores_ligue1       = pd.read_csv('../dataset/local/df_oddsportal_ligue1.csv', index_col=0, encoding='utf-8')

df_foot_scores = pd.concat((df_foot_scores_bundesliga, df_foot_scores_laliga, df_foot_scores_ligue1))

#
#df_foot_scores = df_foot_scores[df_foot_scores.bet_1 >= 1.5]
#df_foot_scores = df_foot_scores[df_foot_scores.bet_X >= 1.5]
#df_foot_scores = df_foot_scores[df_foot_scores.bet_2 >= 1.5]

print df_foot_scores.result.value_counts()


df_foot_scores = df_foot_scores[abs(df_foot_scores.bet_1 - df_foot_scores.bet_2) > 1.5]
print df_foot_scores.result.value_counts()

df_foot_scores['bet_diff']              = df_foot_scores.bet_1 - df_foot_scores.bet_2
df_foot_scores['prediction']            = df_foot_scores.bet_diff.apply(lambda x : "1" if x<0 else "2")

a                                       = df_foot_scores[((df_foot_scores.prediction == df_foot_scores.result) | (df_foot_scores.result == 'X'))]
b                                       = df_foot_scores[~((df_foot_scores.prediction == df_foot_scores.result) | (df_foot_scores.result == 'X'))]
a['good_pred']                          = 1
b['bad_pred']                           = 1

print('******')
ratio = len(a)/float(len(df_foot_scores))
print ratio
print('******')

df_foot_scores = pd.concat((df_foot_scores,a['good_pred'],b['bad_pred']),axis=1)
df_foot_scores.fillna(0, inplace=True)
df_foot_scores['mise'] = 2*mise
df_foot_scores['bankroll'] = df_foot_scores.good_pred*df_foot_scores.result_bet*mise-df_foot_scores.mise

bet_mean = df_foot_scores.result_bet[df_foot_scores.good_pred == 1].values.mean()

print bet_mean*len(a)*mise - len(a+b)*mise*2

print df_foot_scores['bankroll'].sum()

ee
# =============================================================================
# 
# =============================================================================
bet_ = 1.4

df_foot_scores = df_foot_scores[(df_foot_scores.bet_1 < bet_) | (df_foot_scores.bet_2 < bet_)]
df_foot_scores['bet_diff']              = df_foot_scores.bet_1 - df_foot_scores.bet_2

df_foot_scores['prediction']            = df_foot_scores.bet_diff.apply(lambda x : "1" if x<0 else "2")

a                                       = df_foot_scores[((df_foot_scores.prediction == df_foot_scores.result) | (df_foot_scores.result == 'X'))]
b                                       = df_foot_scores[~((df_foot_scores.prediction == df_foot_scores.result) | (df_foot_scores.result == 'X'))]
a['good_pred']                          = 1
b['bad_pred']                           = 1

print('******')
ratio = len(a)/float(len(df_foot_scores))
print ratio
print('******')
df_foot_scores = pd.concat((df_foot_scores,a['good_pred'],b['bad_pred']),axis=1)
df_foot_scores.fillna(0, inplace=True)
"""
