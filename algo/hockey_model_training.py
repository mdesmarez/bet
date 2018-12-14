#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 17:25:37 2018

@author: mathieu
"""



# =============================================================================
# Library Call
# =============================================================================
import os
import time
import cPickle

import pandas                                                                  as pd
import numpy                                                                   as np
import xgboost                                                                 as xgb
import matplotlib.pyplot                                                       as plt

from glob                                                                      import glob
from xgboost.sklearn                                                           import XGBClassifier
from sklearn.model_selection                                                   import train_test_split
from sklearn.metrics                                                           import confusion_matrix, f1_score
from sklearn.grid_search                                                       import GridSearchCV
from sklearn                                                                   import metrics

from hockey_preprocessing                                                      import fix_bet, pipe_preparation, pipe_preparation_2, pipe_preparation_2_score, pipe_preparation_3_score, pipe_preparation_3
from hockey_model_support                                                      import hockey_season_preparation


# =============================================================================
# HOCKEY MODEL TRAINING
# =============================================================================
def hockey_model_training_global(season, split, thres, thres_2, thres_3, list_score):
    hockey_season_preparation(season)

    id_model            = season + '_' + str(split) + '_' + str(thres) + '_' + str(thres_2) + '_' + str(thres_3) + '_' + str(list_score)
    id_model_filename   = '../model/local/' + id_model + '.pickle'
    if os.path.isfile(id_model_filename) == False:
        cm, y_val, y_pred, model, features_name, thres                      = hockey_model_training(split, thres)
    
        cm_2, y_val_2, y_pred_2, model_2, features_name_2, thres_2            = hockey_model_training_2(split, thres_2)
    #    hockey_model_dashboard(cm_2, y_val_2, y_pred_2, model_2, [1,1,1])
                      
        cm_3, y_val_3, y_pred_3, model_3, features_name_3, thres_3            = hockey_model_training_3(split, thres_3)
    #    hockey_model_dashboard(cm_3, y_val_3, y_pred_3, model_3, [1,1,1])
    
        cm_2_score, y_val_2_score, y_pred_2_score, model_2_score, features_name_2_score, thres_2_score = hockey_model_training_2_score(split, thres, list_score)
    #    hockey_model_dashboard(cm_2_score, y_val_2_score, y_pred_2_score, model_2_score, [1,1,1])
    
        cm_3_score, y_val_3_score, y_pred_3_score, model_3_score, features_name_3_score, thres_3_score = hockey_model_training_3_score(split, thres, list_score)
    #    hockey_model_dashboard(cm_3_score, y_val_3_score, y_pred_3_score, model_3_score, [1,1,1])
    
        list_models_features_thres = [model, model_2, model_2_score, model_3, model_3_score, features_name, features_name_2, features_name_2_score, features_name_3, features_name_3_score, thres, thres_2, thres_2_score, thres_3, thres_3_score, list_score]
        
        with open(id_model_filename, 'w') as outfile:
            cPickle.dump(list_models_features_thres, outfile)
            
    else:
        with open(id_model_filename) as f:
            list_models_features_thres = cPickle.load(f) 

    return list_models_features_thres



def hockey_model_training(split, thres):
    list_filename       = glob('../dataset/local/df_scores_bet_*.csv')
    list_filename.sort()
    df_score_all        = pd.DataFrame()
    for i, filename in enumerate(list_filename):
        df_score_bet        = pd.read_csv(filename, sep=',', encoding='utf-8')
        ### Fix bet issue scraping
        df_score_bet.bet_R1 = fix_bet(df_score_bet.bet_R1)
        df_score_bet.bet_RN = fix_bet(df_score_bet.bet_RN)
        df_score_bet.bet_R2 = fix_bet(df_score_bet.bet_R2)
        print 'bet_R1', float(df_score_bet.bet_R1.mean())
        print 'bet_R2', float(df_score_bet.bet_R2.mean())
        print 'bet_R1-bet_R2', float(df_score_bet.bet_R1.mean()-df_score_bet.bet_R2.mean())
        exec('df_score_bet_' + str(i) + '  = df_score_bet')
        df_score_all        = pd.concat((df_score_all,df_score_bet))
    print 'bet_R1', float(df_score_all.bet_R1.mean())
    print 'bet_R2', float(df_score_all.bet_R2.mean())
    print 'bet_R1-bet_R2', float(df_score_all.bet_R1.mean()-df_score_bet.bet_R2.mean())
    
    
    ### Normalization
    df_score_all_normalized        = pd.DataFrame()
    for i, filename in enumerate(list_filename):
        df_bet_temp             = pd.DataFrame()
        exec('df_bet_temp = df_score_bet_' + str(i))
        diff_R1                 = float(df_score_all.bet_R1.mean()) - float(df_bet_temp.bet_R1.mean())
        diff_RN                 = float(df_score_all.bet_R2.mean()) - float(df_bet_temp.bet_RN.mean())
        diff_R2                 = float(df_score_all.bet_R2.mean()) - float(df_bet_temp.bet_R2.mean())
        print filename
        print float(df_bet_temp.bet_R1.mean())
        df_bet_temp.bet_R1      = df_bet_temp.bet_R1 + diff_R1
        df_bet_temp.bet_RN      = df_bet_temp.bet_RN + diff_RN
        df_bet_temp.bet_R2      = df_bet_temp.bet_R2 + diff_R2
        print float(df_bet_temp.bet_R1.mean())
        exec('df_score_bet_' + str(i) + ' = df_bet_temp')
        df_score_all_normalized = pd.concat((df_score_all_normalized,df_bet_temp))
    
    ### data preparation pipe
    df_score_all = pipe_preparation(df_score_all_normalized)
    
    
    
    # =============================================================================
    #  PROCESS DATA FORMAT
    # =============================================================================
    X       = df_score_all.copy()
    del X[u'team_winner_HA']
    
    columns = df_score_all.columns
    features_name = X.columns
    
    y       = df_score_all[u'team_winner_HA'].apply(lambda x: 1 if x == 'team_home' else 0)
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=split, random_state=1)
    X_train = X_train.as_matrix().astype('float32')
    X_val = X_val.as_matrix().astype('float32')
    
    #del df, X, y
    xg_train = xgb.DMatrix(X_train, label=y_train, feature_names=features_name)
    xg_val = xgb.DMatrix(X_val, label=y_val, feature_names=features_name)
    
    # =============================================================================
    # TRAIN MODEL PHASE#1: Determine best n_estimators
    # =============================================================================
    params = {
            'booster': 'gbtree',
    #        'tree_method': 'exact',
            'n_estimators': 1024,
    #        'grow_policy': 'lossguide',
#            'objective': 'binary:hinge',#'binary:logistic',
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
#            'eval_metric': 'error',
            'early_stopping_round': 20,
            'scale_pos_weight': 1,# (len(y)-y.sum())/float(y.sum()),
    #        'max_bin' : 3,
            }
    
    watchlist = [ (xg_train,'train'), (xg_val, 'valid') ]
    
    model = xgb.train(params=params,
                      dtrain=xg_train,
                      num_boost_round=params['n_estimators'],
                      early_stopping_rounds=params['early_stopping_round'],
                      evals=watchlist)

    
    y_pred_init = model.predict(xg_val, ntree_limit=model.best_ntree_limit)
    y_pred = y_pred_init
    
    y_pred[y_pred_init <= thres] = 0
    y_pred[y_pred_init > thres] = 1
    cm = confusion_matrix(y_val,y_pred)
    print y.sum()/float(len(y))
    print cm[1][1]/float(cm[0][1])
    print cm[1][1]/float(cm[0][1]+cm[1][1])
    
    return cm, y_val, y_pred, model, features_name, thres



def hockey_model_training_3_score(split, thres, list_score):
#    list_score = ["3 - 3", "2 - 2", "1 - 1", "2 - 3", "1 - 4", "1 - 3", "2 - 4"]
#    list_score = ["1 - 4", "1 - 3", "2 - 4"]
#    list_score = ["1 - 4", "1 - 3"]
#    list_score          = ['1 - 3','1 - 4','3 - 4']
#    list_score          = ['1 - 3','1 - 4','2 - 5']



    list_filename       = glob('../dataset/local/df_scores_bet_*.csv')
    list_filename.sort()
    df_score_all        = pd.DataFrame()
    for i, filename in enumerate(list_filename):
        df_score_bet        = pd.read_csv(filename, sep=',', encoding='utf-8')
        df_score_all        = pd.concat((df_score_all,df_score_bet))
    
    ### data preparation pipe
    list_score_df = []
    for score in list_score:
        score_modif = score[-1] + ':' + score[0]
        list_score_df.append(score_modif)
    df_score_all = pipe_preparation_3_score(df_score_all)
    
    # =============================================================================
    #  PROCESS DATA FORMAT
    # =============================================================================
    X       = df_score_all.copy()
    del X[u'score_IT_final']
    
    columns = df_score_all.columns
    features_name = X.columns
    
    y       = df_score_all[u'score_IT_final'].apply(lambda x: 1 if x in list_score else 0)
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=split, random_state=1)
    X_train = X_train.as_matrix().astype('float32')
    X_val = X_val.as_matrix().astype('float32')
    
    #del df, X, y
    xg_train = xgb.DMatrix(X_train, label=y_train, feature_names=features_name)
    xg_val = xgb.DMatrix(X_val, label=y_val, feature_names=features_name)
    
    # =============================================================================
    # TRAIN MODEL PHASE#1: Determine best n_estimators
    # =============================================================================
    params = {
            'booster': 'gbtree',
    #        'tree_method': 'exact',
            'n_estimators': 1024,
    #        'grow_policy': 'lossguide',
#            'objective': 'binary:hinge',#'binary:logistic',
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
#            'eval_metric': 'error',
            'early_stopping_round': 20,
            'scale_pos_weight': 1.5#(len(y)-y.sum())/float(y.sum()),
    #        'max_bin' : 3,
            }
    
    watchlist = [ (xg_train,'train'), (xg_val, 'valid') ]
    
    model = xgb.train(params=params,
                      dtrain=xg_train,
                      num_boost_round=params['n_estimators'],
                      early_stopping_rounds=params['early_stopping_round'],
                      evals=watchlist)

    
    y_pred_init = model.predict(xg_val, ntree_limit=model.best_ntree_limit)
    y_pred = y_pred_init
    
    thres = y_pred_init.mean()

    
    y_pred[y_pred_init <= thres] = 0
    y_pred[y_pred_init > thres] = 1
    cm = confusion_matrix(y_val,y_pred)
    print y.sum()/float(len(y))
    print cm[1][1]/float(cm[0][1])
    print cm[1][1]/float(cm[0][1]+cm[1][1])

    return cm, y_val, y_pred, model, features_name, thres



def hockey_model_training_2(split, thres):
    list_filename       = glob('../dataset/local/df_NHL_scores_*_*.csv')
    list_filename.sort()
    df_score_all        = pd.DataFrame()
    for i, filename in enumerate(list_filename):
        df_score_bet        = pd.read_csv(filename, sep=',', encoding='utf-8')
        df_score_all        = pd.concat((df_score_all,df_score_bet))
    
    ### view repartion scorss
    aa = pd.DataFrame(df_score_all.groupby('score_IT_final').count()['score_OT_final'])
    
    ### data preparation pipe
    df_score_all = pipe_preparation_2(df_score_all)
    
    
    # =============================================================================
    #  PROCESS DATA FORMAT
    # =============================================================================
    X       = df_score_all.copy()
    del X[u'team_winner_HA']
    
    columns = df_score_all.columns
    features_name = X.columns
    
    y       = df_score_all[u'team_winner_HA'].apply(lambda x: 1 if x == 'team_home' else 0)
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=split, random_state=1)
    X_train = X_train.as_matrix().astype('float32')
    X_val = X_val.as_matrix().astype('float32')
    
    #del df, X, y
    xg_train = xgb.DMatrix(X_train, label=y_train, feature_names=features_name)
    xg_val = xgb.DMatrix(X_val, label=y_val, feature_names=features_name)
    
    # =============================================================================
    # TRAIN MODEL PHASE#1: Determine best n_estimators
    # =============================================================================
    params = {
            'booster': 'gbtree',
    #        'tree_method': 'exact',
            'n_estimators': 1024,
    #        'grow_policy': 'lossguide',
#            'objective': 'binary:hinge',#'binary:logistic',
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
#            'eval_metric': 'error',
            'early_stopping_round': 20,
            'scale_pos_weight':  1,#(len(y)-y.sum())/float(y.sum()),
    #        'max_bin' : 3,
            }
    
    watchlist = [ (xg_train,'train'), (xg_val, 'valid') ]
    
    model = xgb.train(params=params,
                      dtrain=xg_train,
                      num_boost_round=params['n_estimators'],
                      early_stopping_rounds=params['early_stopping_round'],
                      evals=watchlist)

    
    y_pred_init = model.predict(xg_val, ntree_limit=model.best_ntree_limit)
    y_pred = y_pred_init
    
    y_pred[y_pred_init <= thres] = 0
    y_pred[y_pred_init > thres] = 1
    cm = confusion_matrix(y_val,y_pred)
    print y.sum()/float(len(y))
    print cm[1][1]/float(cm[0][1])
    print cm[1][1]/float(cm[0][1]+cm[1][1])
    
    return cm, y_val, y_pred, model, features_name, thres


def hockey_model_training_2_score(split, thres, list_score):
    list_filename       = glob('../dataset/local/df_NHL_scores_*_*.csv')
    list_filename.sort()
    df_score_all        = pd.DataFrame()
    for i, filename in enumerate(list_filename):
        df_score_bet        = pd.read_csv(filename, sep=',', encoding='utf-8')
        df_score_all        = pd.concat((df_score_all,df_score_bet))
    
    ### data preparation pipe
    df_score_all = pipe_preparation_2_score(df_score_all)
    
    
    # =============================================================================
    #  PROCESS DATA FORMAT
    # =============================================================================
    X       = df_score_all.copy()
    del X[u'score_IT_final']
    
    columns = df_score_all.columns
    features_name = X.columns
    
    y       = df_score_all[u'score_IT_final'].apply(lambda x: 1 if x in list_score else 0)
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=split, random_state=1)
    X_train = X_train.as_matrix().astype('float32')
    X_val = X_val.as_matrix().astype('float32')
    
    #del df, X, y
    xg_train = xgb.DMatrix(X_train, label=y_train, feature_names=features_name)
    xg_val = xgb.DMatrix(X_val, label=y_val, feature_names=features_name)
    
    # =============================================================================
    # TRAIN MODEL PHASE#1: Determine best n_estimators
    # =============================================================================
    params = {
            'booster': 'gbtree',
    #        'tree_method': 'exact',
            'n_estimators': 1024,
    #        'grow_policy': 'lossguide',
#            'objective': 'binary:hinge',#'binary:logistic',
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
#            'eval_metric': 'error',
            'early_stopping_round': 20,
            'scale_pos_weight': 1.5,#(len(y)-y.sum())/float(y.sum()),
    #        'max_bin' : 3,
            }
    
    watchlist = [ (xg_train,'train'), (xg_val, 'valid') ]
    
    model = xgb.train(params=params,
                      dtrain=xg_train,
                      num_boost_round=params['n_estimators'],
                      early_stopping_rounds=params['early_stopping_round'],
                      evals=watchlist)

    
    y_pred_init = model.predict(xg_val, ntree_limit=model.best_ntree_limit)
    y_pred = y_pred_init
    
    thres = y_pred_init.mean()
    
    y_pred[y_pred_init <= thres] = 0
    y_pred[y_pred_init > thres] = 1
    cm = confusion_matrix(y_val,y_pred)
    print y.sum()/float(len(y))
    print cm[1][1]/float(cm[0][1])
    print cm[1][1]/float(cm[0][1]+cm[1][1])

    return cm, y_val, y_pred, model, features_name, thres


def hockey_model_training_3(split, thres):
    list_filename       = glob('../dataset/local/df_scores_bet_*.csv')
    list_filename.sort()
    df_score_all        = pd.DataFrame()
    for i, filename in enumerate(list_filename):
        df_score_bet        = pd.read_csv(filename, sep=',', encoding='utf-8')
        ### Fix bet issue scraping
        df_score_bet.bet_R1 = fix_bet(df_score_bet.bet_R1)
        df_score_bet.bet_RN = fix_bet(df_score_bet.bet_RN)
        df_score_bet.bet_R2 = fix_bet(df_score_bet.bet_R2)
        print 'bet_R1', float(df_score_bet.bet_R1.mean())
        print 'bet_R2', float(df_score_bet.bet_R2.mean())
        print 'bet_R1-bet_R2', float(df_score_bet.bet_R1.mean()-df_score_bet.bet_R2.mean())
        exec('df_score_bet_' + str(i) + '  = df_score_bet')
        df_score_all        = pd.concat((df_score_all,df_score_bet))
    print 'bet_R1', float(df_score_all.bet_R1.mean())
    print 'bet_R2', float(df_score_all.bet_R2.mean())
    print 'bet_R1-bet_R2', float(df_score_all.bet_R1.mean()-df_score_bet.bet_R2.mean())
    
    
    ### Normalization
    df_score_all_normalized        = pd.DataFrame()
    for i, filename in enumerate(list_filename):
        df_bet_temp             = pd.DataFrame()
        exec('df_bet_temp = df_score_bet_' + str(i))
        diff_R1                 = float(df_score_all.bet_R1.mean()) - float(df_bet_temp.bet_R1.mean())
        diff_RN                 = float(df_score_all.bet_R2.mean()) - float(df_bet_temp.bet_RN.mean())
        diff_R2                 = float(df_score_all.bet_R2.mean()) - float(df_bet_temp.bet_R2.mean())
        print filename
        print float(df_bet_temp.bet_R1.mean())
        df_bet_temp.bet_R1      = df_bet_temp.bet_R1 + diff_R1
        df_bet_temp.bet_RN      = df_bet_temp.bet_RN + diff_RN
        df_bet_temp.bet_R2      = df_bet_temp.bet_R2 + diff_R2
        print float(df_bet_temp.bet_R1.mean())
        exec('df_score_bet_' + str(i) + ' = df_bet_temp')
        df_score_all_normalized = pd.concat((df_score_all_normalized,df_bet_temp))
    
    ### data preparation pipe
    df_score_all = pipe_preparation_3(df_score_all_normalized)
    
    
    # =============================================================================
    #  PROCESS DATA FORMAT
    # =============================================================================
    X       = df_score_all.copy()
    del X[u'team_winner_HA']
    
    columns = df_score_all.columns
    features_name = X.columns
    
    y       = df_score_all[u'team_winner_HA'].apply(lambda x: 1 if x == 'team_home' else 0)
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=split, random_state=1)
    X_train = X_train.as_matrix().astype('float32')
    X_val = X_val.as_matrix().astype('float32')
    
    #del df, X, y
    xg_train = xgb.DMatrix(X_train, label=y_train, feature_names=features_name)
    xg_val = xgb.DMatrix(X_val, label=y_val, feature_names=features_name)
    
    # =============================================================================
    # TRAIN MODEL PHASE#1: Determine best n_estimators
    # =============================================================================
    params = {
            'booster': 'gbtree',
    #        'tree_method': 'exact',
            'n_estimators': 1024,
    #        'grow_policy': 'lossguide',
#            'objective': 'binary:hinge',#'binary:logistic',
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
#            'eval_metric': 'error',
            'early_stopping_round': 20,
            'scale_pos_weight': 1,#  (len(y)-y.sum())/float(y.sum()),
    #        'max_bin' : 3,
            }
    
    watchlist = [ (xg_train,'train'), (xg_val, 'valid') ]
    
    model = xgb.train(params=params,
                      dtrain=xg_train,
                      num_boost_round=params['n_estimators'],
                      early_stopping_rounds=params['early_stopping_round'],
                      evals=watchlist)

    
    y_pred_init = model.predict(xg_val, ntree_limit=model.best_ntree_limit)
    y_pred = y_pred_init
    
    y_pred[y_pred_init <= thres] = 0
    y_pred[y_pred_init > thres] = 1
    cm = confusion_matrix(y_val,y_pred)
    print y.sum()/float(len(y))
    print cm[1][1]/float(cm[0][1])
    print cm[1][1]/float(cm[0][1]+cm[1][1])

    return cm, y_val, y_pred, model, features_name, thres
