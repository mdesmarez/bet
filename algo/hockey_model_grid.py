#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 10:31:02 2018

@author: thibaut
"""

# =============================================================================
# Library Call
# =============================================================================
import os
import time
import cPickle
import ast


import pandas                                                                  as pd
import numpy                                                                   as np
import xgboost                                                                 as xgb

import matplotlib.pyplot                                                       as plt
import matplotlib.gridspec                                                     as gridspec

from glob                                                                      import glob
from xgboost.sklearn                                                           import XGBClassifier
from sklearn.model_selection                                                   import train_test_split
from sklearn.metrics                                                           import confusion_matrix, f1_score
from sklearn.grid_search                                                       import GridSearchCV
from sklearn                                                                   import metrics

from hyperopt                                                                  import hp
from hyperopt                                                                  import space_eval
from hyperopt                                                                  import fmin, tpe, Trials

from hockey_preprocessing                                                      import fix_bet, pipe_preparation, pipe_preparation_2, pipe_preparation_2_score, pipe_preparation_3_score, pipe_preparation_3
from hockey_model_support                                                      import plot_confusion_matrix, modelfit, hockey_season_preparation
from hockey_model_evaluation                                                   import hockey_model_evaluation
from hockey_model_training                                                     import hockey_model_training_global, hockey_model_training, hockey_model_training_3_score, hockey_model_training_2, hockey_model_training_2_score, hockey_model_training_3

from random                                                                    import shuffle

# =============================================================================
# GRID GENERATOR
# =============================================================================
list_thres              = np.linspace(0.25,0.75,10+1).astype(float)
list_thres_2            = np.linspace(0.25,0.75,10+1).astype(float)
list_thres_3            = np.linspace(0.25,0.75,10+1).astype(float)
list_thres_R1           = np.linspace(1.40,2.65,25+1).astype(float)
list_thres_pos_home     = np.linspace(-4.0,8.00,20+1).astype(float)


list_grid = []
for thres in list_thres:
    for thres_2 in list_thres_2:
        for thres_3 in list_thres_3:
            for thres_R1 in list_thres_R1:
                for thres_pos_home in list_thres_pos_home:
                    list_grid.append([thres, thres_2, thres_3, thres_R1, thres_pos_home])
       
shuffle(list_grid)             
shuffle(list_grid)             
shuffle(list_grid)             


"""
# =============================================================================
# Remove already done
# =============================================================================
with open('../dataset/local/dict_hyper_grid.json') as f: dict_result = cPickle.load(f);

df_result = pd.DataFrame(dict_result).T

list_parameters             = df_result.index.tolist()
list_model_parameter_remove = []
for item in list_parameters:
    parameters_split = item.split('__')
    list_temp = []
    list_temp.append(float(parameters_split[1].split('_')[0]))
    list_temp.append(float(parameters_split[1].split('_')[1]))
    list_temp.append(float(parameters_split[1].split('_')[2]))
    list_temp.append(float(parameters_split[2].split('_')[0]))
    list_temp.append(float(parameters_split[2].split('_')[1]))
    list_model_parameter_remove.append(list_temp)

a = filter(lambda x: x not in list_grid, list_model_parameter_remove)
"""

# =============================================================================
# 
# =============================================================================
### VARIABLES
mise_depart         = 0
mise_pari           = 10
mise_pari_multi     = 0
split               = 0.05
list_season         = [\
        #           '2005_2006',           
        #           '2006_2007',           
        #           '2007_2008',           
        #           '2008_2009',           
        #           '2009_2010',           
                    '2010_2011',           
                    '2011_2012',           
                    '2012_2013',           
                    '2013_2014',           
                    '2014_2015',
                    '2015_2016',
                    '2016_2017',
                    '2017_2018',
                   ]
list_season.sort()


for grid in list_grid:
    time.sleep(1)
    thres, thres_2, thres_3, thres_R1, thres_pos_home = grid
    try:
        with open('../dataset/local/dict_hyper_grid.json') as f:
            dict_result = cPickle.load(f) 
    except:
        dict_result={}            

    #######!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    list_score          = ['1 - 1']
    #######!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    print '***************** list_season : ', str(list_season)
    
    try:
        ### ITERATE EACH SEASON
        dict_bankroll = {}
        for season in list_season:
            print split, thres, thres_2, thres_3, thres_R1, thres_pos_home, season, list_score
            
            # =============================================================================
            # TRAINING
            # =============================================================================            
            print ('START TRAINING ************** ', str(season))
            list_models_features_thres = hockey_model_training_global(season, split, thres, thres_2, thres_3, list_score)
            print ('END TRAINING **************** ', str(season))

               
            # =============================================================================
            # EVALUATING
            # =============================================================================
            print ('START EVALUATING ************** ', str(season))
            df_score_count, df_bankroll, df_bankroll_KPI = hockey_model_evaluation(list_models_features_thres, thres_R1, thres_pos_home, mise_depart, mise_pari, mise_pari_multi)
            print ('END EVALUATING **************** ', str(season))

            # =============================================================================
            # SCORING
            # =============================================================================
            print ('START SCORING ************** ', str(season))
            score = abs((df_bankroll_KPI.bankroll_max/(df_bankroll_KPI.bankroll_min-0.1)).mean())
            df_bankroll_KPI['bankroll_score']       = score
            df_bankroll_KPI['bankroll_score_final'] = abs((df_bankroll_KPI.bankroll_final/(df_bankroll_KPI.bankroll_min-0.1)))            

            id = str(round(score,2))+'__'+str(thres)+'_'+str(thres_2)+'_'+str(thres_3)+'__'+str(thres_R1)+'_'+str(thres_pos_home)+'__'+str(list_score)
            dict_result.update({id:{}})

            dict_bankroll.update({season+'_score_final':round(df_bankroll_KPI.iloc[0].bankroll_score_final,1)})
            dict_bankroll.update({season+'_score':round(df_bankroll_KPI.iloc[0].bankroll_score,1)})
            dict_bankroll.update({season+'_final':round(df_bankroll_KPI.iloc[0].bankroll_final,1)})
            dict_bankroll.update({season+'_max':round(df_bankroll_KPI.iloc[0].bankroll_max,1)})
            dict_bankroll.update({season+'_min':round(df_bankroll_KPI.iloc[0].bankroll_min,1)})
            
            dict_bankroll.update({season+'_good_pred':round(df_bankroll_KPI.iloc[0].bankroll_good,0)})
            dict_bankroll.update({season+'_bad_pred':round(df_bankroll_KPI.iloc[0].bankroll_bad,0)})
            dict_bankroll.update({season+'_perc':round(df_bankroll_KPI.iloc[0].bankroll_perc,2)})
                
            dict_result[id].update({\
                                   'df_score_count_'+season   :"df_score_count",
                                   'df_bankroll_KPI_'+season  :"df_bankroll_KPI",
                                   'score_'+season            :score
                                   })
            print ('END SCORING ************** ', str(season))    
    
        dict_result[id].update(dict_bankroll)
            
        with open('../dataset/local/dict_hyper_grid.json', 'w') as outfile:
            cPickle.dump(dict_result, outfile)
        
        size_file           = os.path.getsize('../dataset/local/dict_hyper_grid.json')
        try:
            size_file_save  = os.path.getsize('../dataset/local/dict_hyper_grid_save.json')
        except:
            size_file_save  = 0
        
        if size_file_save < size_file:
            with open('../dataset/local/dict_hyper_save.json', 'w') as outfile:
                cPickle.dump(dict_result, outfile)
            
        
        
    except:
        pass
    