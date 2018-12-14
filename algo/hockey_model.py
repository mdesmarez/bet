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

from hockey_model_support                                                      import plot_confusion_matrix, modelfit, hockey_season_preparation
from hockey_model_evaluation                                                   import hockey_model_evaluation
from hockey_model_training                                                     import hockey_model_training_global, hockey_model_training, hockey_model_training_3_score, hockey_model_training_2, hockey_model_training_2_score, hockey_model_training_3



# =============================================================================
# 
# =============================================================================
def optimization_hyperopt(split, list_score):
    # Parameter search space
    space = {}
    space['thres']              = 0.25 + hp.randint('thres', 10)*0.05
    space['thres_2']            = 0.25 + hp.randint('thres_2', 10)*0.05
    space['thres_3']            = 0.25 + hp.randint('thres_3', 10)*0.05
    space['thres_R1']           = 1.40 + hp.randint('thres_R1', 25)*0.05
    space['thres_pos_home']     = -4 + hp.randint('thres_pos_home', 50)*0.25
    space['list_score']         = hp.choice('list_score', [['2 - 2','3 - 3','1 - 1'],
                                                            ['2 - 3','1 - 4','1 - 3','2 - 4'],                                                            
                                                            ['2 - 2'],
                                                            ['2 - 5'],
                                                            ['3 - 3'],
                                                            ['1 - 1'],                                                            
                                                            ])

    def objective(params):
        thres                   = params['thres']
        thres_2                 = params['thres_2']
        thres_3                 = params['thres_3']
        thres_R1                = params['thres_R1']
        thres_pos_home          = params['thres_pos_home']
        list_score              = params['list_score']
        list_score              = list(list_score)

        
        try:
            with open('../dataset/local/dict_hyper.json') as f:
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
                                       'df_score_count_'+season   :df_score_count,
                                       'df_bankroll_KPI_'+season  :df_bankroll_KPI,
                                       'score_'+season            :score
                                       })
                print ('END SCORING ************** ', str(season))    
        
            dict_result[id].update(dict_bankroll)
                
            with open('../dataset/local/dict_hyper.json', 'w') as outfile:
                cPickle.dump(dict_result, outfile)
        
        except Exception, e:
            print 'ERREUR : ', e
            score = 1
            
            
        return 1/score

    # The Trials object will store details of each iteration
    trials = Trials()
    
    # Run the hyperparameter search using the tpe algorithm
    best = fmin(objective,
                space,
                algo=tpe.suggest,
                max_evals=3000,
                trials=trials)
    
    # Get the values of the optimal parameters
    best_params = space_eval(space, best)
    return best, best_params





# =============================================================================
# 
# =============================================================================
### VARIABLES
mise_depart         = 0
mise_pari           = 10
mise_pari_multi     = 0
split               = 0.05
list_score          = ['1 - 3','1 - 4','3 - 4']
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


###
best, best_params = optimization_hyperopt(split, list_score)
    
    
    
    
    
    
    
    
    
    
    
    
    