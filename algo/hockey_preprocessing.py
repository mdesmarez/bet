#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 16:58:53 2018

@author: mathieu
"""


# =============================================================================
# 
# =============================================================================


import pandas                                                                  as pd


# =============================================================================
# 
# =============================================================================
def fix_bet(df_prepro):
    df_prepro.dropna(inplace=True)
    df_prepro.replace('-','0', inplace=True, method=None)
    df_prepro.replace('--','0', inplace=True, method=None)
    df_prepro.replace('---','0', inplace=True, method=None)
    df_prepro = df_prepro.apply(lambda x: float(str(x)[:3]) if str(x).count('.') != 1 else float(x))
    return df_prepro



def pipe_preparation(df_prepro):
    df_prepro.fillna(0,inplace=True)
    df_prepro.drop_duplicates(keep='first', inplace=True)
    
    list_keep_column     = [\
    #                         u'competition',
    #                         u'date_match',
    #                         u'match_name',
    #                         u'team_winner',
    #                         u'team_loser',
                             u'team_winner_HA',
    #                         u'team_loser_HA',
                             u'point_diff_home_away',
    #                         u'score_1P',
    #                         u'score_2P',
    #                         u'score_3P',
    #                         u'score_IT_final',                     
    #                         u'score_OT_final',
    #                         u'team_home',
                             u'team_home_point',
    #                         u'score_IT_home',                     
    #                         u'score_OT_home',
    #                         u'team_away',
                             u'team_away_point',
    #                         u'score_IT_away',
    #                         u'score_OT_away',    
                             u'team_min_point',
                             u'team_max_point',
                             u'nbr_match_diff_home_away',
                             u'result_n1_home',
                             u'result_n1_away',
                             u'result_n2_home',
                             u'result_n2_away',
                             u'result_n3_home',
                             u'result_n3_away',
                             u'result_n4_home',
                             u'result_n4_away',
                             u'result_n5_home',
                             u'result_n5_away',
                             u'day_last_match_home',
                             u'day_last_match_away',
                             u'season_period',
#                             u'bet_V1',
#                             u'bet_V2',
                             u'bet_R1',
                             u'bet_RN',
                             u'bet_R2',
                             ]
    
    df_prepro         =   df_prepro[list_keep_column]

    #########################################################################################################
    ### BET #################################################################################################
    #########################################################################################################
    round_precision = 1
    round_mult      = 1
        
    df_prepro[u'bet_R1'] = df_prepro[u'bet_R1'].apply(lambda x: round(x,round_precision))
    df_prepro[u'bet_RN'] = df_prepro[u'bet_RN'].apply(lambda x: round(x,round_precision))
    df_prepro[u'bet_R2'] = df_prepro[u'bet_R2'].apply(lambda x: round(x,round_precision))

    df_prepro            = df_prepro[df_prepro[u'bet_R1'] != 0 ]
    df_prepro            = df_prepro[df_prepro[u'bet_RN'] != 0 ]
    df_prepro            = df_prepro[df_prepro[u'bet_R2'] != 0 ]
#    
    df_prepro[u'diff_bet_R1_R2']    = (df_prepro[u'bet_R1'] - df_prepro[u'bet_R2']).apply(lambda x : round(x/1,1))
    df_prepro[u'ratio_bet_R1_R2']   = (df_prepro[u'bet_R1'] / df_prepro[u'bet_R2']).apply(lambda x : round(x/1,1))
#    df_prepro            =   df_prepro[df_prepro.bet_R1 < 1.85*round_mult]    
#    df_prepro            =   df_prepro[df_prepro.diff_bet_R1_R2 > -0.2 ]    

#    del df_prepro[u'bet_R1']
#    del df_prepro[u'diff_bet_R1_R2']
    
    del df_prepro[u'bet_RN']
    del df_prepro[u'bet_R2']    
    del df_prepro[u'ratio_bet_R1_R2']
            
    #########################################################################################################
    ###  RESULTS ############################################################################################
    #########################################################################################################
    df_prepro.result_n1_home[df_prepro.result_n1_home < 0] = -1
    df_prepro.result_n1_home[df_prepro.result_n1_home > 0] = 1
    df_prepro.result_n2_home[df_prepro.result_n2_home < 0] = -1
    df_prepro.result_n2_home[df_prepro.result_n2_home > 0] = 1
    df_prepro.result_n3_home[df_prepro.result_n3_home < 0] = -1
    df_prepro.result_n3_home[df_prepro.result_n3_home > 0] = 1
    df_prepro.result_n4_home[df_prepro.result_n4_home < 0] = -1
    df_prepro.result_n4_home[df_prepro.result_n4_home > 0] = 1
    df_prepro.result_n5_home[df_prepro.result_n5_home < 0] = -1
    df_prepro.result_n5_home[df_prepro.result_n5_home > 0] = 1
    
    df_prepro.result_n1_away[df_prepro.result_n1_away < 0] = -1
    df_prepro.result_n1_away[df_prepro.result_n1_away > 0] = 1
    df_prepro.result_n2_away[df_prepro.result_n2_away < 0] = -1
    df_prepro.result_n2_away[df_prepro.result_n2_away > 0] = 1
    df_prepro.result_n3_away[df_prepro.result_n3_away < 0] = -1
    df_prepro.result_n3_away[df_prepro.result_n3_away > 0] = 1
    df_prepro.result_n4_away[df_prepro.result_n4_away < 0] = -1
    df_prepro.result_n4_away[df_prepro.result_n4_away > 0] = 1
    df_prepro.result_n5_away[df_prepro.result_n5_away < 0] = -1
    df_prepro.result_n5_away[df_prepro.result_n5_away > 0] = 1
    
    df_prepro = df_prepro[df_prepro.result_n1_away != 0] 
    df_prepro = df_prepro[df_prepro.result_n1_home != 0]
    df_prepro = df_prepro[df_prepro.result_n2_away != 0] 
    df_prepro = df_prepro[df_prepro.result_n2_home != 0] 
#    df_prepro = df_prepro[df_prepro.result_n3_away != 0] 
#    df_prepro = df_prepro[df_prepro.result_n3_home != 0] 
#    df_prepro = df_prepro[df_prepro.result_n4_away != 0] 
#    df_prepro = df_prepro[df_prepro.result_n4_home != 0] 
#    df_prepro = df_prepro[df_prepro.result_n5_away != 0] 
#    df_prepro = df_prepro[df_prepro.result_n5_home != 0] 
    
#    del df_prepro[u'result_n1_away']
#    del df_prepro[u'result_n1_home']
    del df_prepro[u'result_n2_away']
    del df_prepro[u'result_n2_home']
    del df_prepro[u'result_n3_away']
    del df_prepro[u'result_n3_home']
    del df_prepro[u'result_n4_away']
    del df_prepro[u'result_n4_home']
    del df_prepro[u'result_n5_away']
    del df_prepro[u'result_n5_home']
    
    
    #########################################################################################################
    ###  POSITION ###########################################################################################
    #########################################################################################################    
#    df_prepro[u'mix']    = df_prepro[u'point_diff_home_away']/(df_prepro[u'team_max_point'])
#    df_prepro[u'mix']    = (df_prepro[u'point_diff_home_away']/(df_prepro[u'team_max_point']-df_prepro[u'team_min_point'])).apply(lambda x : round(x*10,0))
#    df_prepro         =   df_prepro[df_prepro.mix > 1.5]
    
    df_prepro[u'pos_home']      = ((df_prepro[u'team_home_point']-df_prepro[u'team_min_point'])/(df_prepro[u'team_max_point']-df_prepro[u'team_min_point'])).apply(lambda x : round(x,1))
    df_prepro[u'pos_away']      = ((df_prepro[u'team_away_point']-df_prepro[u'team_min_point'])/(df_prepro[u'team_max_point']-df_prepro[u'team_min_point'])).apply(lambda x : round(x,1))
    df_prepro[u'diff_pos_home'] = (df_prepro[u'pos_home'] - df_prepro[u'pos_away']).apply(lambda x : round(x*1,1))
#    df_prepro                   = df_prepro[df_prepro.diff_pos_home > 0.35]
#    df_prepro         =   df_prepro[df_prepro.point_diff_home_away > 8]


    del df_prepro[u'pos_home']
    del df_prepro[u'pos_away']
#    plt.figure()
#    df_prepro.diff_pos_home.hist()
#    plt.figure()
    
#    del df_prepro[u'diff_pos_home']
    

    del df_prepro[u'team_home_point']
    del df_prepro[u'team_away_point']
    del df_prepro[u'point_diff_home_away']
    del df_prepro[u'team_min_point']
    del df_prepro[u'team_max_point']
    del df_prepro[u'nbr_match_diff_home_away']    


    #########################################################################################################
    ###  TIME ###############################################################################################
    #########################################################################################################    
    df_prepro[u'diff_day_off'] = (df_prepro[u'day_last_match_home']-df_prepro[u'day_last_match_away']).apply(lambda x : 0 if x>5 else 1)
    df_prepro[u'diff_day_off'] = (df_prepro[u'day_last_match_home']-df_prepro[u'day_last_match_away']).apply(lambda x : 0 if x>0 else 1)
    
    del df_prepro[u'day_last_match_home']
    del df_prepro[u'day_last_match_away']  
    del df_prepro[u'diff_day_off']  
    del df_prepro[u'season_period']

                             
    
    df_prepro.dropna(inplace=True)    

    return df_prepro


def pipe_preparation_3_score(df_prepro):
    df_prepro.dropna(inplace=True)
#    df_prepro.fillna(0,inplace=True)
    df_prepro.drop_duplicates(keep='first', inplace=True)
    
    list_keep_column     = [\

                             u'score_IT_final',                     
#                             u'5:4',
#                             u'5:3',
#                             u'5:2',
#                             u'5:1',
#                             u'5:0',

                             u'4:3',
                             u'4:2',
                             u'4:1',
                             u'4:0',

                             u'3:2',
                             u'3:1',
                             u'3:0',

                             u'2:1',
                             u'2:0',

                             u'1:0',

                             u'0:1',
 
                             u'0:2',
                             u'1:2',

                             u'0:3',
                             u'1:3',
                             u'2:3',

                             u'0:4',
                             u'1:4',
                             u'2:4',
                             u'3:4',

#                             u'0:5',
#                             u'1:5',
#                             u'2:5',                             
#                             u'3:5',                             
#                             u'4:5',
                             
                             u'0:0',                            
                             u'1:1',
                             u'2:2',
                             u'3:3',
                             u'4:4',
#                             u'5:5',
                             ]
    
#    for score in list_score_df:
#        list_keep_column.append(score)
    
    df_prepro         =   df_prepro[list_keep_column]

    #########################################################################################################
    ### BET #################################################################################################
    #########################################################################################################
    round_precision = 1
    round_mult      = 1
    global dict_quantile_temp
    

#    for score in list(set(list_keep_column)-set([u'score_IT_final'])):
#        exec("df_prepro[u'" + score + "'] = df_prepro[u'" + score + "'].apply(lambda x: round(x*3,2))")

        
#    for score in list(set(list_keep_column)-set([u'score_IT_final'])):
#        score_modif = score
##        exec("df_prepro[u'" + score_modif + "'] = df_prepro[u'" + score_modif + "'].apply(lambda x: round(x,round_precision))")
#        exec("quantile_temp = df_prepro[u'" + score_modif + "'].quantile([0.4,0.5,0.6])")
#        dict_quantile_temp = quantile_temp.to_dict()
#        exec("df_prepro[u'" + score_modif + "'] = df_prepro[u'" + score_modif + "'].apply(lambda x: 0 if x<=dict_quantile_temp[0.4] else x)")
#        exec("df_prepro[u'" + score_modif + "'] = df_prepro[u'" + score_modif + "'].apply(lambda x: 1 if x>dict_quantile_temp[0.6] else x)")
#        exec("df_prepro[u'" + score_modif + "'] = df_prepro[u'" + score_modif + "'].apply(lambda x: 2 if (x>dict_quantile_temp[0.4] and x<=dict_quantile_temp[0.6]) else x)")

  
    df_prepro.dropna(inplace=True)    

    return df_prepro


def pipe_preparation_2(df_prepro):
    df_prepro.fillna(0,inplace=True)
    df_prepro.drop_duplicates(keep='first', inplace=True)
    
    list_keep_column     = [\
    #                         u'competition',
    #                         u'date_match',
    #                         u'match_name',
    #                         u'team_winner',
    #                         u'team_loser',
                             u'team_winner_HA',
    #                         u'team_loser_HA',
                             u'point_diff_home_away',
    #                         u'score_1P',
    #                         u'score_2P',
    #                         u'score_3P',
    #                         u'score_IT_final',                     
    #                         u'score_OT_final',
    #                         u'team_home',
                             u'team_home_point',
    #                         u'score_IT_home',                     
    #                         u'score_OT_home',
    #                         u'team_away',
                             u'team_away_point',
    #                         u'score_IT_away',
    #                         u'score_OT_away',    
                             u'team_min_point',
                             u'team_max_point',
                             u'nbr_match_diff_home_away',
                             u'result_n1_home',
                             u'result_n1_away',
                             u'result_n2_home',
                             u'result_n2_away',
                             u'result_n3_home',
                             u'result_n3_away',
                             u'result_n4_home',
                             u'result_n4_away',
                             u'result_n5_home',
                             u'result_n5_away',
                             u'day_last_match_home',
                             u'day_last_match_away',
                             u'season_period',
#                             u'bet_V1',
#                             u'bet_V2',
#                             u'bet_R1',
#                             u'bet_RN',
#                             u'bet_R2',
                             ]
    
    df_prepro         =   df_prepro[list_keep_column]

            
    #########################################################################################################
    ###  RESULTS ############################################################################################
    #########################################################################################################
#    df_prepro.result_n1_home[df_prepro.result_n1_home < 0] = -1
#    df_prepro.result_n1_home[df_prepro.result_n1_home > 0] = 1
#    df_prepro.result_n2_home[df_prepro.result_n2_home < 0] = -1
#    df_prepro.result_n2_home[df_prepro.result_n2_home > 0] = 1
#    df_prepro.result_n3_home[df_prepro.result_n3_home < 0] = -1
#    df_prepro.result_n3_home[df_prepro.result_n3_home > 0] = 1
#    df_prepro.result_n4_home[df_prepro.result_n4_home < 0] = -1
#    df_prepro.result_n4_home[df_prepro.result_n4_home > 0] = 1
#    df_prepro.result_n5_home[df_prepro.result_n5_home < 0] = -1
#    df_prepro.result_n5_home[df_prepro.result_n5_home > 0] = 1
#    
#    df_prepro.result_n1_away[df_prepro.result_n1_away < 0] = -1
#    df_prepro.result_n1_away[df_prepro.result_n1_away > 0] = 1
#    df_prepro.result_n2_away[df_prepro.result_n2_away < 0] = -1
#    df_prepro.result_n2_away[df_prepro.result_n2_away > 0] = 1
#    df_prepro.result_n3_away[df_prepro.result_n3_away < 0] = -1
#    df_prepro.result_n3_away[df_prepro.result_n3_away > 0] = 1
#    df_prepro.result_n4_away[df_prepro.result_n4_away < 0] = -1
#    df_prepro.result_n4_away[df_prepro.result_n4_away > 0] = 1
#    df_prepro.result_n5_away[df_prepro.result_n5_away < 0] = -1
#    df_prepro.result_n5_away[df_prepro.result_n5_away > 0] = 1
    
    df_prepro = df_prepro[df_prepro.result_n1_away != 0] 
    df_prepro = df_prepro[df_prepro.result_n1_home != 0]
    df_prepro = df_prepro[df_prepro.result_n2_away != 0] 
    df_prepro = df_prepro[df_prepro.result_n2_home != 0] 
    df_prepro = df_prepro[df_prepro.result_n3_away != 0] 
    df_prepro = df_prepro[df_prepro.result_n3_home != 0] 
#    df_prepro = df_prepro[df_prepro.result_n4_away != 0] 
#    df_prepro = df_prepro[df_prepro.result_n4_home != 0] 
#    df_prepro = df_prepro[df_prepro.result_n5_away != 0] 
#    df_prepro = df_prepro[df_prepro.result_n5_home != 0] 
    
#    del df_prepro[u'result_n1_away']
#    del df_prepro[u'result_n1_home']
#    del df_prepro[u'result_n2_away']
#    del df_prepro[u'result_n2_home']
#    del df_prepro[u'result_n3_away']
#    del df_prepro[u'result_n3_home']
    del df_prepro[u'result_n4_away']
    del df_prepro[u'result_n4_home']
    del df_prepro[u'result_n5_away']
    del df_prepro[u'result_n5_home']
    
    
    #########################################################################################################
    ###  POSITION ###########################################################################################
    #########################################################################################################    
#    df_prepro[u'mix']    = df_prepro[u'point_diff_home_away']/(df_prepro[u'team_max_point'])
#    df_prepro[u'mix']    = (df_prepro[u'point_diff_home_away']/(df_prepro[u'team_max_point']-df_prepro[u'team_min_point'])).apply(lambda x : round(x*10,0))
#    df_prepro         =   df_prepro[df_prepro.mix > 1.5]
    
    df_prepro[u'pos_home']      = ((df_prepro[u'team_home_point']-df_prepro[u'team_min_point'])/(df_prepro[u'team_max_point']-df_prepro[u'team_min_point'])).apply(lambda x : round(x,1))
    df_prepro[u'pos_away']      = ((df_prepro[u'team_away_point']-df_prepro[u'team_min_point'])/(df_prepro[u'team_max_point']-df_prepro[u'team_min_point'])).apply(lambda x : round(x,1))
    df_prepro[u'diff_pos_home'] = (df_prepro[u'pos_home'] - df_prepro[u'pos_away']).apply(lambda x : round(x*1,1))
#    df_prepro                   = df_prepro[df_prepro.diff_pos_home > 0.35]
#    df_prepro         =   df_prepro[df_prepro.point_diff_home_away > 8]


    del df_prepro[u'pos_home']
    del df_prepro[u'pos_away']
#    plt.figure()
#    df_prepro.diff_pos_home.hist()
#    plt.figure()
    
#    del df_prepro[u'diff_pos_home']
    

    del df_prepro[u'team_home_point']
    del df_prepro[u'team_away_point']
#    del df_prepro[u'point_diff_home_away']
    del df_prepro[u'team_min_point']
    del df_prepro[u'team_max_point']
#    del df_prepro[u'nbr_match_diff_home_away']    


    #########################################################################################################
    ###  TIME ###############################################################################################
    #########################################################################################################    
    df_prepro[u'diff_day_off'] = (df_prepro[u'day_last_match_home']-df_prepro[u'day_last_match_away']).apply(lambda x : 0 if x>5 else 1)
    df_prepro[u'diff_day_off'] = (df_prepro[u'day_last_match_home']-df_prepro[u'day_last_match_away']).apply(lambda x : 0 if x>0 else 1)
    
#    del df_prepro[u'day_last_match_home']
#    del df_prepro[u'day_last_match_away']  
#    del df_prepro[u'diff_day_off']  
#    del df_prepro[u'season_period']

                             
    
    df_prepro.dropna(inplace=True)    

    return df_prepro


def pipe_preparation_2_score(df_prepro):
    df_prepro.fillna(0,inplace=True)
    df_prepro.drop_duplicates(keep='first', inplace=True)
    
    list_keep_column     = [\
    #                         u'competition',
    #                         u'date_match',
    #                         u'match_name',
    #                         u'team_winner',
    #                         u'team_loser',
#                             u'team_winner_HA',
    #                         u'team_loser_HA',
                             u'point_diff_home_away',
    #                         u'score_1P',
    #                         u'score_2P',
    #                         u'score_3P',
                             u'score_IT_final',                     
    #                         u'score_OT_final',
    #                         u'team_home',
                             u'team_home_point',
#                             u'score_IT_home',                     
    #                         u'score_OT_home',
    #                         u'team_away',
                             u'team_away_point',
    #                         u'score_IT_away',
    #                         u'score_OT_away',    
                             u'team_min_point',
                             u'team_max_point',
                             u'nbr_match_diff_home_away',
                             u'result_n1_home',
                             u'result_n1_away',
                             u'result_n2_home',
                             u'result_n2_away',
                             u'result_n3_home',
                             u'result_n3_away',
                             u'result_n4_home',
                             u'result_n4_away',
                             u'result_n5_home',
                             u'result_n5_away',
                             u'day_last_match_home',
                             u'day_last_match_away',
                             u'season_period',
#                             u'bet_V1',
#                             u'bet_V2',
#                             u'bet_R1',
#                             u'bet_RN',
#                             u'bet_R2',
                             ]
    
    df_prepro         =   df_prepro[list_keep_column]

            
    #########################################################################################################
    ###  RESULTS ############################################################################################
    #########################################################################################################
#    df_prepro.result_n1_home[df_prepro.result_n1_home < 0] = -1
#    df_prepro.result_n1_home[df_prepro.result_n1_home > 0] = 1
#    df_prepro.result_n2_home[df_prepro.result_n2_home < 0] = -1
#    df_prepro.result_n2_home[df_prepro.result_n2_home > 0] = 1
#    df_prepro.result_n3_home[df_prepro.result_n3_home < 0] = -1
#    df_prepro.result_n3_home[df_prepro.result_n3_home > 0] = 1
#    df_prepro.result_n4_home[df_prepro.result_n4_home < 0] = -1
#    df_prepro.result_n4_home[df_prepro.result_n4_home > 0] = 1
#    df_prepro.result_n5_home[df_prepro.result_n5_home < 0] = -1
#    df_prepro.result_n5_home[df_prepro.result_n5_home > 0] = 1
#    
#    df_prepro.result_n1_away[df_prepro.result_n1_away < 0] = -1
#    df_prepro.result_n1_away[df_prepro.result_n1_away > 0] = 1
#    df_prepro.result_n2_away[df_prepro.result_n2_away < 0] = -1
#    df_prepro.result_n2_away[df_prepro.result_n2_away > 0] = 1
#    df_prepro.result_n3_away[df_prepro.result_n3_away < 0] = -1
#    df_prepro.result_n3_away[df_prepro.result_n3_away > 0] = 1
#    df_prepro.result_n4_away[df_prepro.result_n4_away < 0] = -1
#    df_prepro.result_n4_away[df_prepro.result_n4_away > 0] = 1
#    df_prepro.result_n5_away[df_prepro.result_n5_away < 0] = -1
#    df_prepro.result_n5_away[df_prepro.result_n5_away > 0] = 1
    
    df_prepro = df_prepro[df_prepro.result_n1_away != 0] 
    df_prepro = df_prepro[df_prepro.result_n1_home != 0]
    df_prepro = df_prepro[df_prepro.result_n2_away != 0] 
    df_prepro = df_prepro[df_prepro.result_n2_home != 0] 
    df_prepro = df_prepro[df_prepro.result_n3_away != 0] 
    df_prepro = df_prepro[df_prepro.result_n3_home != 0] 
#    df_prepro = df_prepro[df_prepro.result_n4_away != 0] 
#    df_prepro = df_prepro[df_prepro.result_n4_home != 0] 
#    df_prepro = df_prepro[df_prepro.result_n5_away != 0] 
#    df_prepro = df_prepro[df_prepro.result_n5_home != 0] 
    
#    del df_prepro[u'result_n1_away']
#    del df_prepro[u'result_n1_home']
#    del df_prepro[u'result_n2_away']
#    del df_prepro[u'result_n2_home']
#    del df_prepro[u'result_n3_away']
#    del df_prepro[u'result_n3_home']
    del df_prepro[u'result_n4_away']
    del df_prepro[u'result_n4_home']
    del df_prepro[u'result_n5_away']
    del df_prepro[u'result_n5_home']
    
    
    #########################################################################################################
    ###  POSITION ###########################################################################################
    #########################################################################################################    
#    df_prepro[u'mix']    = df_prepro[u'point_diff_home_away']/(df_prepro[u'team_max_point'])
#    df_prepro[u'mix']    = (df_prepro[u'point_diff_home_away']/(df_prepro[u'team_max_point']-df_prepro[u'team_min_point'])).apply(lambda x : round(x*10,0))
#    df_prepro         =   df_prepro[df_prepro.mix > 1.5]
    
    df_prepro[u'pos_home']      = ((df_prepro[u'team_home_point']-df_prepro[u'team_min_point'])/(df_prepro[u'team_max_point']-df_prepro[u'team_min_point'])).apply(lambda x : round(x,1))
    df_prepro[u'pos_away']      = ((df_prepro[u'team_away_point']-df_prepro[u'team_min_point'])/(df_prepro[u'team_max_point']-df_prepro[u'team_min_point'])).apply(lambda x : round(x,1))
    df_prepro[u'diff_pos_home'] = (df_prepro[u'pos_home'] - df_prepro[u'pos_away']).apply(lambda x : round(x*1,1))
#    df_prepro                   = df_prepro[df_prepro.diff_pos_home > 0.35]
#    df_prepro         =   df_prepro[df_prepro.point_diff_home_away > 8]


    del df_prepro[u'pos_home']
    del df_prepro[u'pos_away']
#    plt.figure()
#    df_prepro.diff_pos_home.hist()
#    plt.figure()
    
#    del df_prepro[u'diff_pos_home']
    

    del df_prepro[u'team_home_point']
    del df_prepro[u'team_away_point']
#    del df_prepro[u'point_diff_home_away']
    del df_prepro[u'team_min_point']
    del df_prepro[u'team_max_point']
#    del df_prepro[u'nbr_match_diff_home_away']    


    #########################################################################################################
    ###  TIME ###############################################################################################
    #########################################################################################################    
    df_prepro[u'diff_day_off'] = (df_prepro[u'day_last_match_home']-df_prepro[u'day_last_match_away']).apply(lambda x : 0 if x>5 else 1)
    df_prepro[u'diff_day_off'] = (df_prepro[u'day_last_match_home']-df_prepro[u'day_last_match_away']).apply(lambda x : 0 if x>0 else 1)
    
#    del df_prepro[u'day_last_match_home']
#    del df_prepro[u'day_last_match_away']  
#    del df_prepro[u'diff_day_off']  
#    del df_prepro[u'season_period']

                             
    
    df_prepro.dropna(inplace=True)    

    return df_prepro


def pipe_preparation_3(df_prepro):
    df_prepro.fillna(0,inplace=True)
    df_prepro.drop_duplicates(keep='first', inplace=True)
    
    list_keep_column     = [\
    #                         u'competition',
    #                         u'date_match',
    #                         u'match_name',
    #                         u'team_winner',
    #                         u'team_loser',
                             u'team_winner_HA',
    #                         u'team_loser_HA',
#                             u'point_diff_home_away',
    #                         u'score_1P',
    #                         u'score_2P',
    #                         u'score_3P',
    #                         u'score_IT_final',                     
    #                         u'score_OT_final',
    #                         u'team_home',
#                             u'team_home_point',
    #                         u'score_IT_home',                     
    #                         u'score_OT_home',
    #                         u'team_away',
#                             u'team_away_point',
    #                         u'score_IT_away',
    #                         u'score_OT_away',    
#                             u'team_min_point',
#                             u'team_max_point',
#                             u'nbr_match_diff_home_away',
#                             u'result_n1_home',
#                             u'result_n1_away',
#                             u'result_n2_home',
#                             u'result_n2_away',
#                             u'result_n3_home',
#                             u'result_n3_away',
#                             u'result_n4_home',
#                             u'result_n4_away',
#                             u'result_n5_home',
#                             u'result_n5_away',
#                             u'day_last_match_home',
#                             u'day_last_match_away',
#                             u'season_period',
#                             u'bet_V1',
#                             u'bet_V2',
                             u'bet_R1',
                             u'bet_RN',
                             u'bet_R2',
                             ]
    
    df_prepro         =   df_prepro[list_keep_column]

    #########################################################################################################
    ### BET #################################################################################################
    #########################################################################################################
    round_precision = 1
    round_mult      = 1
        
    df_prepro[u'bet_R1'] = df_prepro[u'bet_R1'].apply(lambda x: round(x,round_precision))
    df_prepro[u'bet_RN'] = df_prepro[u'bet_RN'].apply(lambda x: round(x,round_precision))
    df_prepro[u'bet_R2'] = df_prepro[u'bet_R2'].apply(lambda x: round(x,round_precision))

    df_prepro            = df_prepro[df_prepro[u'bet_R1'] != 0 ]
    df_prepro            = df_prepro[df_prepro[u'bet_RN'] != 0 ]
    df_prepro            = df_prepro[df_prepro[u'bet_R2'] != 0 ]
#    
    df_prepro[u'diff_bet_R1_R2']    = (df_prepro[u'bet_R1'] - df_prepro[u'bet_R2']).apply(lambda x : round(x/1,1))
    df_prepro[u'ratio_bet_R1_R2']   = (df_prepro[u'bet_R1'] / df_prepro[u'bet_R2']).apply(lambda x : round(x/1,1))
#    df_prepro            =   df_prepro[df_prepro.bet_R1 < 1.85*round_mult]    
#    df_prepro            =   df_prepro[df_prepro.diff_bet_R1_R2 > -0.2 ]    

#    del df_prepro[u'bet_R1']
#    del df_prepro[u'diff_bet_R1_R2']
    
#    del df_prepro[u'bet_RN']
#    del df_prepro[u'bet_R2']    
#    del df_prepro[u'ratio_bet_R1_R2']
            
    df_prepro.dropna(inplace=True)    

    return df_prepro
