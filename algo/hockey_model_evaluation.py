#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 10:31:19 2018

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

from hyperopt                                                                  import hp
from hyperopt                                                                  import space_eval
from hyperopt                                                                  import fmin, tpe, Trials

from hockey_preprocessing                                                   import fix_bet, pipe_preparation, pipe_preparation_2, pipe_preparation_2_score, pipe_preparation_3_score, pipe_preparation_3
from hockey_model_support                                                      import plot_confusion_matrix


# =============================================================================
# 
# =============================================================================
def hockey_model_evaluation(list_models_features_thres, thres_R1, thres_pos_home, mise_depart, mise_pari, mise_pari_multi):
    model, model_2, model_2_score, model_3, model_3_score, features_name, features_name_2, features_name_2_score, features_name_3, features_name_3_score, thres, thres_2, thres_2_score, thres_3, thres_3_score, list_score = list_models_features_thres

    list_file_          = glob('../dataset/local/___df_scores_bet*')        
    df_validation_init = pd.read_csv(list_file_[0], sep=',', encoding='utf-8')

    df_validation_init.reset_index(drop=True, inplace=True)

    df_validation_init.bet_R1 = fix_bet(df_validation_init.bet_R1)
    df_validation_init.bet_RN = fix_bet(df_validation_init.bet_RN)
    df_validation_init.bet_R2 = fix_bet(df_validation_init.bet_R2)

#    diff_R1_s = diff_R1
#    diff_R2_s = diff_R2
#    df_validation_init.bet_R1 = df_validation_init.bet_R1 + diff_R1_s
#    df_validation_init.bet_RN = df_validation_init.bet_RN + diff_RN
#    df_validation_init.bet_R2 = df_validation_init.bet_R2 + diff_R2_s
#    
    df_validation               = pipe_preparation(df_validation_init)
    df_validation_2             = pipe_preparation_2(df_validation_init)
    df_validation_2_score       = pipe_preparation_2_score(df_validation_init)
    df_validation_3             = pipe_preparation_3(df_validation_init)
    df_validation_3_score       = pipe_preparation_3_score(df_validation_init)
    
    
    ### FILTER
    df_validation             = df_validation[df_validation.bet_R1 < thres_R1]    
    df_validation             = df_validation[df_validation.diff_pos_home > thres_pos_home]
    
    
    ################################
    XX                    = df_validation.copy()
    del XX[u'team_winner_HA']
    yy       = df_validation[u'team_winner_HA'].apply(lambda x: 1 if x == 'team_home' else 0)
    yy       = pd.DataFrame(yy)
    index_yy = yy.index
#    yy.reset_index(drop=True, inplace=True)
    XX       = XX.as_matrix().astype('float32')
    xxg_val  = xgb.DMatrix(XX, label=yy, feature_names=features_name)
    ################################
    XX_2                    = df_validation_2.copy()
    del XX_2[u'team_winner_HA']
    yy_2       = df_validation_2[u'team_winner_HA'].apply(lambda x: 1 if x == 'team_home' else 0)
    yy_2       = pd.DataFrame(yy_2)
    index_yy_2 = yy_2.index
#    yy_2.reset_index(drop=True, inplace=True)
    XX_2       = XX_2.as_matrix().astype('float32')
    xxg_val_2  = xgb.DMatrix(XX_2, label=yy_2, feature_names=features_name_2)
    ################################
    XX_2_score                    = df_validation_2_score.copy()
    del XX_2_score[u'score_IT_final']
    yy_2_score       = df_validation_2_score[u'score_IT_final'].apply(lambda x: 1 if x in list_score else 0)
    yy_2_score       = pd.DataFrame(yy_2_score)
    index_yy_2_score = yy_2_score.index
#    yy_2_score.reset_index(drop=True, inplace=True)
    XX_2_score       = XX_2_score.as_matrix().astype('float32')
    xxg_val_2_score  = xgb.DMatrix(XX_2_score, label=yy_2_score, feature_names=features_name_2_score)
    ################################
    XX_3                    = df_validation_3.copy()
    del XX_3[u'team_winner_HA']
    yy_3       = df_validation_3[u'team_winner_HA'].apply(lambda x: 1 if x == 'team_home' else 0)
    yy_3       = pd.DataFrame(yy_3)
    index_yy_3 = yy_3.index
#    yy_3.reset_index(drop=True, inplace=True)
    XX_3       = XX_3.as_matrix().astype('float32')
    xxg_val_3  = xgb.DMatrix(XX_3, label=yy_3, feature_names=features_name_3)
    ################################
    XX_3_score                    = df_validation_3_score.copy()
    del XX_3_score[u'score_IT_final']
    yy_3_score       = df_validation_3_score[u'score_IT_final'].apply(lambda x: 1 if x in list_score else 0)
    yy_3_score       = pd.DataFrame(yy_3_score)
    index_yy_3_score = yy_3_score.index
#    yy_3_score.reset_index(drop=True, inplace=True)
    XX_3_score       = XX_3_score.as_matrix().astype('float32')
    xxg_val_3_score  = xgb.DMatrix(XX_3_score, label=yy_3_score, feature_names=features_name_3_score)
    ################################
    
    if model != '':
        yy_pred = model.predict(xxg_val, ntree_limit=model.best_ntree_limit)  #####################ùùùùùùùùù
        yy_pred[yy_pred <= thres] = 0
        yy_pred[yy_pred > thres] = 1
    if model_2 != '':
        yy_pred_2 = model_2.predict(xxg_val_2, ntree_limit=model_2.best_ntree_limit)  #####################ùùùùùùùùù
        yy_pred_2[yy_pred_2 <= thres_2] = 0
        yy_pred_2[yy_pred_2 > thres_2] = 1
    if model_2_score != '':
        yy_pred_2_score = model_2_score.predict(xxg_val_2_score, ntree_limit=model_2_score.best_ntree_limit)  #####################ùùùùùùùùù
        yy_pred_2_score[yy_pred_2_score <= thres_2_score] = 0
        yy_pred_2_score[yy_pred_2_score > thres_2_score] = 1
    if model_3 != '':
        yy_pred_3 = model_3.predict(xxg_val_3, ntree_limit=model_3.best_ntree_limit)  #####################ùùùùùùùùù
        yy_pred_3[yy_pred_3 <= thres_3] = 0
        yy_pred_3[yy_pred_3 > thres_3] = 1
    if model_3_score != '':
        yy_pred_3_score = model_3_score.predict(xxg_val_3_score, ntree_limit=model_3_score.best_ntree_limit)  #####################ùùùùùùùùù
        yy_pred_3_score[yy_pred_3_score <= thres_3_score] = 0
        yy_pred_3_score[yy_pred_3_score > thres_3_score] = 1    
    
    df_yy = pd.DataFrame(yy)
    df_yy.set_index(index_yy, drop=True, inplace=True)
    df_yy_2 = pd.DataFrame(yy_2)
    df_yy_2.set_index(index_yy_2, drop=True, inplace=True)
    df_yy_2_score = pd.DataFrame(yy_2_score)
    df_yy_2_score.set_index(index_yy_2_score, drop=True, inplace=True)
    df_yy_3 = pd.DataFrame(yy_3)
    df_yy_3.set_index(index_yy_3, drop=True, inplace=True)
    df_yy_3_score = pd.DataFrame(yy_3_score)
    df_yy_3_score.set_index(index_yy_3_score, drop=True, inplace=True)
    
    
    df_yy_pred = pd.DataFrame(yy_pred)
    df_yy_pred.set_index(index_yy, drop=True, inplace=True)
    df_yy_pred_2 = pd.DataFrame(yy_pred_2)
    df_yy_pred_2.set_index(index_yy_2, drop=True, inplace=True)
    df_yy_pred_2_score = pd.DataFrame(yy_pred_2_score)
    df_yy_pred_2_score.set_index(index_yy_2_score, drop=True, inplace=True)
    df_yy_pred_3 = pd.DataFrame(yy_pred_3)
    df_yy_pred_3.set_index(index_yy_3, drop=True, inplace=True)
    df_yy_pred_3_score = pd.DataFrame(yy_pred_3_score)
    df_yy_pred_3_score.set_index(index_yy_3_score, drop=True, inplace=True)

    
    a = pd.concat((df_yy_pred, df_yy_pred_2, df_yy_pred_2_score, df_yy_pred_3, df_yy_pred_3_score), axis=1)
    a.columns = ['model', 'model_2', 'model_2_score', 'model_3', 'model_3_score'] 
    a.fillna(0, inplace=True)
    a['model'] = a['model']
    a['model_2'] = a['model_2']
    a['model_3'] = a['model_3']
    a['model_2_3'] = a['model_2']*a['model_3']
    a['model_1_2_3'] = a['model']*a['model_2']*a['model_3']
    a['model_1_2_2_score_3'] = a['model']*a['model_2']*a['model_2_score']*a['model_3']
    a['model_1_2_2_score_3_3_score'] = a['model']*a['model_2']*a['model_2_score']*a['model_3']*a['model_3_score']
    yy_pred = a['model']
    yy_pred_2 = a['model_2']
    yy_pred_3 = a['model_3']
    yy_pred_2_3 = a['model_2_3']
    yy_pred_1_2_3 = a['model_1_2_3']
    yy_pred_1_2_2_score_3 = a['model_1_2_2_score_3']
    yy_pred_1_2_2_score_3_3_score = a['model_1_2_2_score_3_3_score']


    b = pd.concat((df_yy, df_yy_2, df_yy_2_score, df_yy_3, df_yy_3_score), axis=1)
    b.columns = ['model', 'model_2', 'model_2_score', 'model_3', 'model_3_score'] 
    b.fillna(0, inplace=True)
    b['model'] = b['model']
    b['model_2'] = b['model_2']
    b['model_3'] = b['model_3']
    b['model_2_3'] = b['model_2']*b['model_3']
    b['model_1_2_3'] = b['model']*b['model_2']*b['model_3']
    b['model_1_2_2_score_3'] = b['model']*b['model_2']*b['model_2_score']*b['model_3']
    b['model_1_2_2_score_3_3_score'] = b['model']*b['model_2']*b['model_2_score']*b['model_3']*b['model_3_score']
    yy                          = pd.DataFrame(b['model'])
    yy_2                        = pd.DataFrame(b['model_2'])
    yy_3                        = pd.DataFrame(b['model_3'])
    yy_2_3                      = pd.DataFrame(b['model_2_3'])
    yy_1_2_3                    = pd.DataFrame(b['model_1_2_3'])
    yy_1_2_2_score_3            = pd.DataFrame(b['model_1_2_2_score_3'])
    yy_1_2_2_score_3_3_score    = pd.DataFrame(b['model_1_2_2_score_3_3_score'])
    
    cm          = confusion_matrix(yy,yy_pred)
    cm_2_3      = confusion_matrix(yy_2_3,yy_pred_2_3)
    cm_1_2_3    = confusion_matrix(yy_1_2_3,yy_pred_1_2_3)
    cm_1_2_2_score_3    = confusion_matrix(yy_1_2_2_score_3,yy_pred_1_2_2_score_3)
    cm_1_2_2_score_3_3_score    = confusion_matrix(yy_1_2_2_score_3,yy_pred_1_2_2_score_3_3_score)
#    plot_confusion_matrix(cm, ['0','1'], normalize=True)
    
    
    ###
    print('*******************************************************************')
    print('*****************************    1    *****************************')
    y_comp = pd.concat((pd.DataFrame(yy), pd.DataFrame(yy_pred)), axis=1)
    y_comp.fillna(0, inplace=True)
    y_comp.columns  = ['ground','pred']
    y_comp['pred']  = y_comp['pred'].apply(int) 
    win_real = len(y_comp[(y_comp['ground'] == 1)])
    win  = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 1)])
    loss = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 0)])
    perc = win/(float(loss)+float(win+1))
    print 'win : ', str(win)
    print 'loss : ', str(loss)
    print 'perc : ', str(perc)
    
    ###
    print('*******************************************************************')
    print('*****************************    2    *****************************')
    y_comp = pd.concat((pd.DataFrame(yy_2), pd.DataFrame(yy_pred_2)), axis=1)
    y_comp.fillna(0, inplace=True)
    y_comp.columns  = ['ground','pred']
    y_comp['pred']  = y_comp['pred'].apply(int) 
    win_real = len(y_comp[(y_comp['ground'] == 1)])
    win  = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 1)])
    loss = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 0)])
    perc = win/(float(loss)+float(win+1))
    print 'win : ', str(win)
    print 'loss : ', str(loss)
    print 'perc : ', str(perc)
    
    ###
    print('*******************************************************************')
    print('*****************************    3    *****************************')
    y_comp = pd.concat((pd.DataFrame(yy_3), pd.DataFrame(yy_pred_3)), axis=1)
    y_comp.fillna(0, inplace=True)
    y_comp.columns  = ['ground','pred']
    y_comp['pred']  = y_comp['pred'].apply(int) 
    win_real = len(y_comp[(y_comp['ground'] == 1)])
    win  = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 1)])
    loss = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 0)])
    perc = win/(float(loss)+float(win+1))
    print 'win : ', str(win)
    print 'loss : ', str(loss)
    print 'perc : ', str(perc)
    
    ###
    print('*******************************************************************')
    print('***************************    2_3    *****************************')
    y_comp = pd.concat((pd.DataFrame(yy_2_3), pd.DataFrame(yy_pred_2_3)), axis=1)
    y_comp.fillna(0, inplace=True)
    y_comp.columns  = ['ground','pred']
    y_comp['pred']  = y_comp['pred'].apply(int) 
    win_real = len(y_comp[(y_comp['ground'] == 1)])
    win  = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 1)])
    loss = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 0)])
    perc = win/(float(loss)+float(win+1))
    print 'win : ', str(win)
    print 'loss : ', str(loss)
    print 'perc : ', str(perc)
    
    ###
    print('*******************************************************************')
    print('*************************    1_2_3    *****************************')
    y_comp = pd.concat((pd.DataFrame(yy_1_2_3), pd.DataFrame(yy_pred_1_2_3)), axis=1)
    y_comp.fillna(0, inplace=True)
    y_comp.columns  = ['ground','pred']
    y_comp['pred']  = y_comp['pred'].apply(int) 
    win_real = len(y_comp[(y_comp['ground'] == 1)])
    win  = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 1)])
    loss = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 0)])
    perc = win/(float(loss)+float(win+1))
    print 'win : ', str(win)
    print 'loss : ', str(loss)
    print 'perc : ', str(perc)

    ###
    print('*******************************************************************')
    print('***********************    2_score    *****************************')
    y_comp = pd.concat((pd.DataFrame(yy_2_score), pd.DataFrame(yy_pred_2_score)), axis=1)
    y_comp.fillna(0, inplace=True)
    y_comp.columns  = ['ground','pred']
    y_comp['pred']  = y_comp['pred'].apply(int) 
    win_real = len(y_comp[(y_comp['ground'] == 1)])
    win  = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 1)])
    loss = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 0)])
    perc = win/(float(loss)+float(win+1))
    print 'win : ', str(win)
    print 'loss : ', str(loss)
    print 'perc : ', str(perc)

    ###
    print('*******************************************************************')
    print('***********************    3_score    *****************************')
    y_comp = pd.concat((pd.DataFrame(yy_3_score), pd.DataFrame(yy_pred_3_score)), axis=1)
    y_comp.fillna(0, inplace=True)
    y_comp.columns  = ['ground','pred']
    y_comp['pred']  = y_comp['pred'].apply(int) 
    win_real = len(y_comp[(y_comp['ground'] == 1)])
    win  = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 1)])
    loss = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 0)])
    perc = win/(float(loss)+float(win+1))
    print 'win : ', str(win)
    print 'loss : ', str(loss)
    print 'perc : ', str(perc)
    
    ###
    print('*******************************************************************')
    print('*****************    1_2_2_score_3    *****************************')
    y_comp = pd.concat((pd.DataFrame(yy_1_2_2_score_3), pd.DataFrame(yy_pred_1_2_2_score_3)), axis=1)
    y_comp.fillna(0, inplace=True)
    y_comp.columns  = ['ground','pred']
    y_comp['pred']  = y_comp['pred'].apply(int) 
    win_real = len(y_comp[(y_comp['ground'] == 1)])
    win  = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 1)])
    loss = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 0)])
    perc = win/(float(loss)+float(win+1))
    print 'win : ', str(win)
    print 'loss : ', str(loss)
    print 'perc : ', str(perc)  
    
    ###
    print('*******************************************************************')
    print('*****************    1_2_2_score_3_3_score    *********************')
    y_comp = pd.concat((pd.DataFrame(yy_1_2_2_score_3_3_score), pd.DataFrame(yy_pred_1_2_2_score_3_3_score)), axis=1)
    y_comp.fillna(0, inplace=True)
    y_comp.columns  = ['ground','pred']
    y_comp['pred']  = y_comp['pred'].apply(int) 
    win_real = len(y_comp[(y_comp['ground'] == 1)])
    win  = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 1)])
    loss = len(y_comp[(y_comp['pred'] == 1) & (y_comp['ground'] == 0)])
    perc = win/(float(loss)+float(win+1))
    print 'win : ', str(win)
    print 'loss : ', str(loss)
    print 'perc : ', str(perc)  
    print('*******************************************************************')
    print('*******************************************************************')
    
    
    # =============================================================================
    # SELECT PRED 
    # =============================================================================
    df_yypred = pd.DataFrame(yy_pred_1_2_3).astype('int')
    cm      = cm_1_2_3
    yy      = yy_1_2_3
    yy_pred = yy_pred_1_2_3


#    df_yypred = pd.DataFrame(yy_pred_1_2_2_score_3).astype('int')
#    cm      = cm_1_2_2_score_3
#    yy      = yy_1_2_2_score_3
#    yy_pred = yy_pred_1_2_2_score_3
#    
    
#    df_yypred = pd.DataFrame(yy_pred_1_2_2_score_3_3_score).astype('int')
#    cm      = cm_1_2_2_score_3_3_score
#    yy      = yy_1_2_2_score_3_3_score
#    yy_pred = yy_pred_1_2_2_score_3_3_score
    
    
    # =============================================================================
    # SELECT PRED 
    # =============================================================================    
    
    
    df_yypred.columns = ['y_pred']
#    df_yypred.set_index(index_yy, drop=True, inplace=True)
##    df_validation_init.reset_index(drop=True,inplace=True)
    df_check = pd.concat((df_validation_init,df_yypred),axis=1)
    
    
    a = df_check[(df_check.team_winner_HA == 'team_home') & (df_check.y_pred == 1)]
    b = df_check[(df_check.team_winner_HA == 'team_away') & (df_check.y_pred == 1)]
    a['good_pred'] = 1
    b['bad_pred'] = 1
    a['good_pred_bet_V1'] = a['bet_V1'] 
    df_check = pd.concat((df_check,a['good_pred'],b['bad_pred']),axis=1)
    df_check.fillna(0, inplace=True)
    df_check = pd.concat((df_check,a['good_pred_bet_V1']),axis=1)
    mean_V1  = df_check.good_pred_bet_V1.mean()
    
    
    
    list_bet = []
    for score in list_score:
        score_name      = score[-1] + ':' + score[0]
        score_name_col  = score[-1] + '_' + score[0]
        
        globals()["bet_" + score_name_col] = pd.DataFrame(df_check[score_name][(df_check.good_pred == 1) & (df_check.score_IT_final == score)])
        globals()["bet_" + score_name_col].columns = ['bet']
        list_bet.append(globals()["bet_" + score_name_col])


    
#    #########################
##    bet_6_3             = pd.DataFrame(df_check['6:3'][(df_check.good_pred == 1) & (df_check.score_IT_final == '3 - 6')])
##    bet_6_3.columns     = ['bet']
##    
#    bet_5_2             = pd.DataFrame(df_check['5:2'][(df_check.good_pred == 1) & (df_check.score_IT_final == '2 - 5')])
#    bet_5_2.columns     = ['bet']
#    
#    bet_4_3             = pd.DataFrame(df_check['4:3'][(df_check.good_pred == 1) & (df_check.score_IT_final == '3 - 4')])
#    bet_4_3.columns     = ['bet']
#    
#    bet_4_2             = pd.DataFrame(df_check['4:2'][(df_check.good_pred == 1) & (df_check.score_IT_final == '2 - 4')])
#    bet_4_2.columns     = ['bet']
#    
#    bet_4_1             = pd.DataFrame(df_check['4:1'][(df_check.good_pred == 1) & (df_check.score_IT_final == '1 - 4')])
#    bet_4_1.columns     = ['bet']
#    
#    bet_3_1             = pd.DataFrame(df_check['3:1'][(df_check.good_pred == 1) & (df_check.score_IT_final == '1 - 3')])
#    bet_3_1.columns     = ['bet']
#
#    bet_3_2             = pd.DataFrame(df_check['3:2'][(df_check.good_pred == 1) & (df_check.score_IT_final == '2 - 3')])
#    bet_3_2.columns     = ['bet']
#    
#    bet_3_0             = pd.DataFrame(df_check['3:0'][(df_check.good_pred == 1) & (df_check.score_IT_final == '0 - 3')])
#    bet_3_0.columns     = ['bet']
#    
#    bet_2_2             = pd.DataFrame(df_check['2:2'][(df_check.good_pred == 1) & (df_check.score_IT_final == '2 - 2')])
#    bet_2_2.columns     = ['bet']
#    
#    list_bet = [\
##                   bet_6_3,
#    #               bet_5_2,
#                   bet_4_3,
#    #               bet_4_2,
#                   bet_4_1,
#                   bet_3_1,
#    #               bet_3_0,
##                   bet_2_2,
##                   bet_3_2,
#                   ]
    
    a = pd.concat((list_bet),axis=0)
    df_check = pd.concat((df_check,a['bet']),axis=1)
    df_check.bet.fillna(0, inplace=True)
    df_check.sort_values(u'date_match', ascending=True, inplace=True)
    ##########################
    #
    #df_check = df_check.iloc[800:]
    #df_check.reset_index(drop=True, inplace=True)
    
    dict_df_check = df_check.to_dict(orient='index')
    for i in range(len(dict_df_check)):
        item = dict_df_check[i]
    
        try:
            bankroll = dict_df_check[i-1]['bankroll']
        except:
            bankroll = mise_depart
    
        dict_df_check[i].update({'mise_pari_multi':mise_pari_multi})
        
        bankroll_pos = 0
        bankroll_neg = 0
        
        if dict_df_check[i]['good_pred'] == 1:
            bankroll        = bankroll - mise_pari - mise_pari_multi*len(list_bet) + mise_pari*(dict_df_check[i]['bet_V1']) + mise_pari_multi*(dict_df_check[i]['bet'])
            bankroll_pos    = - mise_pari - mise_pari_multi*len(list_bet) + mise_pari*(dict_df_check[i]['bet_V1']) + mise_pari_multi*(dict_df_check[i]['bet'])
        if dict_df_check[i]['bad_pred'] == 1:
            bankroll        = bankroll - mise_pari - mise_pari_multi*len(list_bet)
            bankroll_neg    = - mise_pari - mise_pari_multi*len(list_bet)
            
        dict_df_check[i].update({'bankroll' : bankroll,
                                 'bankroll_pos' : bankroll_pos,
                                 'bankroll_neg' : bankroll_neg})
    
    df_check2 = pd.DataFrame(dict_df_check).T
    
    df_check2['unique_id'] = df_check2['date_match'].map(str) + df_check2['team_home'].map(str) + '_' + df_check2['team_away'].map(str)
    try:    
        print('Perc : ' + str(round(cm[1][1]/float((cm[1][1]+cm[0][1]))*100,2)) + '%')
        print('Ratio : ' + str(round(cm[1][1]*(mean_V1-1) - cm[0][1],2)))
        print('Number bet : ' + str(cm[1][1]+cm[0][1]))
        print('Win bet : ' + str(cm[1][1]))
        print('Loss bet : ' + str(cm[0][1]))
        print('Mean V1 : ' + str(mean_V1))
        print('Max bankroll : ' + str(df_check2.bankroll.max()))
        print('Min bankroll : ' + str(df_check2.bankroll.min()))
        print('Final bankroll : ' + str(df_check2.bankroll.iloc[-1]))

        print('First bet time : ' + str(df_check2[df_check2.good_pred == 1].iloc[0].date_match))
        print('Bankrool 1 Nov : ' + str(df_check2[df_check2.date_match == df_check2.date_match.iloc[0][:4]+'-11-01 00:00:00'].iloc[0].bankroll))
        print('Bankrool 1 Dec : ' + str(df_check2[df_check2.date_match == df_check2.date_match.iloc[0][:4]+'-12-01 00:00:00'].iloc[0].bankroll))
        print('Bankrool 1 Jan : ' + str(df_check2[df_check2.date_match == df_check2.date_match.iloc[-1][:4]+'-01-01 00:00:00'].iloc[0].bankroll))
        print('Bankrool 1 Fev : ' + str(df_check2[df_check2.date_match == df_check2.date_match.iloc[-1][:4]+'-02-01 00:00:00'].iloc[0].bankroll))
        print('Bankrool 1 Mar : ' + str(df_check2[df_check2.date_match == df_check2.date_match.iloc[-1][:4]+'-03-01 00:00:00'].iloc[0].bankroll))
        print('Bankrool 1 Avr : ' + str(df_check2[df_check2.date_match == df_check2.date_match.iloc[-1][:4]+'-04-01 00:00:00'].iloc[0].bankroll))
    except:
        pass
    df_score_IT = pd.DataFrame(df_check2[df_check2.good_pred == 1].groupby('score_IT_final').count()['2:2'])
    df_score_IT.sort_values(u'2:2', ascending=False, inplace=True)
    df_score_IT_sum = df_score_IT.sum().values[0]
    df_score_IT[perc] = (df_score_IT/float(df_score_IT_sum)*100.0)
    df_score_IT[perc] = df_score_IT[perc].apply(lambda x : round(x,0))
    
    bankroll_min    = df_check2.bankroll.min()
    bankroll_mean   = df_check2.bankroll.mean()
    bankroll_max    = df_check2.bankroll.max()
    bankroll_final  = df_check2.bankroll.iloc[-1]  
    bankroll_good   = df_check2.good_pred.sum()
    bankroll_bad    = df_check2.bad_pred.sum()
    
    try:
        if (cm[1][1]+cm[0][1]) == 0:
            bankroll_perc   = 0
        else:
            bankroll_perc   = round(cm[1][1]/float((cm[1][1]+cm[0][1]))*100,2)
    except:
        bankroll_perc   = 0
        
    df_bankroll_KPI         = pd.DataFrame()
    df_bankroll_KPI         = pd.concat((df_bankroll_KPI, pd.DataFrame.from_dict({'bankroll_min'   :bankroll_min,
                                                                                  'bankroll_mean'  :bankroll_mean,
                                                                                  'bankroll_final' :bankroll_final,
                                                                                  'bankroll_max'   :bankroll_max,
                                                                                  'bankroll_good'  :bankroll_good,
                                                                                  'bankroll_bad'   :bankroll_bad,
                                                                                  'bankroll_perc'  :bankroll_perc},
                                                                                    orient='index').T), axis=1)

    return df_score_IT, df_check2, df_bankroll_KPI
