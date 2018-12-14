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
list_season             = [2016, 2017]
list_sport              = ['handball', 'soccer']
pays                    = ''
ligue                   = ''

mise                    = 10
##########################
dict_parameter   = {'handball':{
                                'bet_max'     : 6,
                                'bet_min'     : 1.2,
                                'bet_ecart'   : 4,
                                'target'      : 2,
                                'rep_target'  : 1,
                                },
                    'soccer':{
                                'bet_max'     : 6,
                                'bet_min'     : 1.2,
                                'bet_ecart'   : 8,
                                'target'      : 4,
                                'rep_target'  : 1,
                                },
                    'basketball':{
                                'bet_max'     : 8,
                                'bet_min'     : 0,
                                'bet_ecart'   : 0,
                                'target'      : 1,
                                'rep_target'  : 1,
                                }
                    }
                    


# =============================================================================
# LOAD DATASET
# =============================================================================
df_foot_scores_init = pd.read_csv('../dataset/local/df_ALL.xls', encoding='utf-8')
df_foot_scores_init = preprocessing_data(df_foot_scores_init)

df_filter_ALL = pd.DataFrame()
target_ALL    = 0

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
    df_filter_ALL       = pd.concat((df_filter_ALL, df_filter))
    target_ALL          = target_ALL + target
    
    # =============================================================================
    # STATISTIQUE MATCHS
    # =============================================================================
    good_pred_ratio, bet_moyen, target_calcul, nbr_match_moy_semaine = match_statistique(df_filter, list_season)
    match_statistique_print(good_pred_ratio, bet_moyen, target_calcul, nbr_match_moy_semaine)
    
    


target = target_ALL

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
    



ee


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
