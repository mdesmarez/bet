#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 11:27:31 2018

@author: mathieu
"""

# =============================================================================
# 
# =============================================================================
import pandas as pd
import cPickle
import pprint
import ast
import datetime
import time


import matplotlib.pyplot                                                       as plt
import matplotlib.gridspec                                                     as gridspec

from hockey_model_evaluation                                                   import hockey_model_evaluation
from hockey_model_training                                                     import hockey_model_training_global, hockey_model_training, hockey_model_training_3_score, hockey_model_training_2, hockey_model_training_2_score, hockey_model_training_3
from datetime                                                                  import timedelta

from time                                                                      import gmtime, strftime

from email_handling                                                            import email_send_without_attachments, email_send_html_with_attachment

#%%# =============================================================================
# 
# =============================================================================
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def result_viewer(min_valuemax, min_valuemin):
    pp = pprint.PrettyPrinter(indent=4)
    
    #with open('../dataset/local/dict_hyper_ok1.json') as f: dict_result_1 = cPickle.load(f);
    #with open('../dataset/local/dict_hyper_ok2.json') as f: dict_result_2 = cPickle.load(f);
    with open('../dataset/local/dict_hyper_.json') as f: dict_result_3 = cPickle.load(f);
    with open('../dataset/local/dict_hyper_grid.json') as f: dict_result_4 = cPickle.load(f);
    dict_result    = merge_two_dicts(dict_result_3, dict_result_4)
    #dict_result         = merge_two_dicts(dict_result_temp, dict_result_3)
    #dict_result         = merge_two_dicts(dict_result_temp, dict_result_4)
    
    #with open('../dataset/local/dict_hyper_grid.json') as f: dict_result = cPickle.load(f);
    
    
    
    df_result = pd.DataFrame(dict_result).T
    """
    not_keep = [u'df_bankroll_KPI_2010_2011',
           u'df_bankroll_KPI_2011_2012', u'df_bankroll_KPI_2012_2013',
           u'df_bankroll_KPI_2013_2014', u'df_bankroll_KPI_2014_2015',
           u'df_bankroll_KPI_2015_2016', u'df_bankroll_KPI_2016_2017',
           u'df_bankroll_KPI_2017_2018', u'df_score_count_2010_2011',
           u'df_score_count_2011_2012', u'df_score_count_2012_2013',
           u'df_score_count_2013_2014', u'df_score_count_2014_2015',
           u'df_score_count_2015_2016', u'df_score_count_2016_2017',
           u'df_score_count_2017_2018']
    df_result = df_result[df_result.columns.difference(not_keep)]
    dict_result = df_result.to_dict(orient='index')
    with open('../dataset/local/dict_hyper_grid.json', 'w') as outfile:
        cPickle.dump(dict_result, outfile)
            
    """
    df_result_simple = df_result[[
    #        u'2010_2011_score', u'2011_2012_score', u'2012_2013_score',
            u'2013_2014_score', u'2014_2015_score',
            u'2015_2016_score', u'2016_2017_score', u'2017_2018_score',
            
    #        u'2010_2011_perc', u'2011_2012_perc', u'2012_2013_perc',
    #        u'2013_2014_perc', u'2014_2015_perc',
    #        u'2015_2016_perc', u'2016_2017_perc', u'2017_2018_perc',
    #        
    #        u'2010_2011_score_final', u'2011_2012_score_final', u'2012_2013_score_final',
    #        u'2013_2014_score_final', u'2014_2015_score_final',
    #        u'2015_2016_score_final', u'2016_2017_score_final', u'2017_2018_score_final',
            
    #        u'2010_2011_min', u'2011_2012_min', u'2012_2013_min',
            u'2013_2014_min', u'2014_2015_min',
            u'2015_2016_min', u'2016_2017_min', u'2017_2018_min',
            
    #        u'2010_2011_max', u'2011_2012_max', u'2012_2013_max',
            u'2013_2014_max', u'2014_2015_max',
            u'2015_2016_max', u'2016_2017_max', u'2017_2018_max',
            
    #        u'2010_2011_final', u'2011_2012_final', u'2012_2013_final',
    #        u'2013_2014_final', u'2014_2015_final',
    #        u'2015_2016_final', u'2016_2017_final', u'2017_2018_final',
            ]]
    
    #df_result_simple = df_result[[
    #        u'2010_2011_score', u'2011_2012_score', u'2013_2014_score', u'2014_2015_score', u'2015_2016_score', u'2016_2017_score', u'2017_2018_score',
    #        u'2010_2011_score_final', u'2011_2012_score_final', u'2013_2014_score_final', u'2014_2015_score_final', u'2015_2016_score_final', u'2016_2017_score_final', u'2017_2018_score_final',
    #        u'2010_2011_min', u'2011_2012_min', u'2013_2014_min', u'2014_2015_min', u'2015_2016_min', u'2016_2017_min', u'2017_2018_min',
    #        u'2010_2011_max', u'2011_2012_max', u'2013_2014_max', u'2014_2015_max', u'2015_2016_max', u'2016_2017_max', u'2017_2018_max',
    #        u'2010_2011_final', u'2011_2012_final', u'2013_2014_final', u'2014_2015_final', u'2015_2016_final', u'2016_2017_final', u'2017_2018_final',
    #        u'_']]
    
    df_result_simple = df_result_simple.astype(float)
    df_result_simple = df_result_simple[df_result_simple.sum(axis=1) != 0]
    
    
    #min_valueperc = 50
    #df_result_simple = df_result_simple[
    ##                                    ((df_result_simple[u'2010_2011_perc'] >= min_valueperc) | (df_result_simple[u'2010_2011_perc'] == 0)) & \
    ##                                    ((df_result_simple[u'2011_2012_perc'] >= min_valueperc) | (df_result_simple[u'2011_2012_perc'] == 0)) & \
    ##                                    ((df_result_simple[u'2012_2013_perc'] >= min_valueperc) | (df_result_simple[u'2012_2013_perc'] == 0)) & \
    ##                                    ((df_result_simple[u'2013_2014_perc'] >= min_valueperc) | (df_result_simple[u'2013_2014_perc'] == 0)) & \
    ##                                    ((df_result_simple[u'2014_2015_perc'] >= min_valueperc) | (df_result_simple[u'2014_2015_perc'] == 0)) & \
    #                                    ((df_result_simple[u'2015_2016_perc'] >= min_valueperc) | (df_result_simple[u'2015_2016_perc'] == 0)) & \
    #                                    ((df_result_simple[u'2016_2017_perc'] >= min_valueperc) | (df_result_simple[u'2016_2017_perc'] == 0)) & \
    #                                    ((df_result_simple[u'2017_2018_perc'] >= min_valueperc) | (df_result_simple[u'2017_2018_perc'] == 0))]
    
    
    df_result_simple = df_result_simple[
    #                                    (df_result_simple[u'2014_2015_max'] >= min_valuemax) | \
                                        ((df_result_simple[u'2015_2016_max'] >= min_valuemax)) | \
                                        ((df_result_simple[u'2016_2017_max'] >= min_valuemax)) | \
                                        ((df_result_simple[u'2017_2018_max'] >= min_valuemax)) ]
    
    
    #min_valuescore = 160
    #df_result_simple = df_result_simple[
    ##                                    (df_result_simple[u'2010_2011_score'] >= min_valuescore) & \
    ##                                    (df_result_simple[u'2011_2012_score'] >= min_valuescore) & \
    ##                                    (df_result_simple[u'2013_2014_score'] >= min_valuescore) & \
    ##                                    (df_result_simple[u'2014_2015_score'] >= min_valuescore) & \
    #                                    ((df_result_simple[u'2015_2016_score'] > min_valuescore) | (df_result_simple[u'2015_2016_score'] == 0)) & \
    #                                    ((df_result_simple[u'2016_2017_score'] > min_valuescore) | (df_result_simple[u'2016_2017_score'] == 0)) & \
    #                                    ((df_result_simple[u'2017_2018_score'] > min_valuescore) | (df_result_simple[u'2017_2018_score'] == 0))]
    

    #min_valuemin    = -20
    df_result_simple = df_result_simple[
    #                                    ((df_result_simple[u'2010_2011_min'] >= min_valuemin) | (df_result_simple[u'2010_2011_min'] == 0)) & \
    #                                    ((df_result_simple[u'2011_2012_min'] >= min_valuemin) | (df_result_simple[u'2011_2012_min'] == 0)) & \
    #                                    ((df_result_simple[u'2012_2013_min'] >= min_valuemin) | (df_result_simple[u'2012_2013_min'] == 0)) & \
    #                                    ((df_result_simple[u'2013_2014_min'] >= min_valuemin) | (df_result_simple[u'2013_2014_min'] == 0)) & \
    #                                    ((df_result_simple[u'2014_2015_min'] >= min_valuemin) | (df_result_simple[u'2014_2015_min'] == 0)) & \
                                        ((df_result_simple[u'2015_2016_min'] >= min_valuemin) | (df_result_simple[u'2015_2016_min'] == 0)) & \
                                        ((df_result_simple[u'2016_2017_min'] >= min_valuemin) | (df_result_simple[u'2016_2017_min'] == 0)) & \
                                        ((df_result_simple[u'2017_2018_min'] >= min_valuemin) | (df_result_simple[u'2017_2018_min'] == 0))]
    
    df_result_simple.drop_duplicates(inplace=True)
    list_parameters = df_result_simple.index.tolist()
    
    
    list_model_parameter_auto = []
    for item in list_parameters:
        parameters_split = item.split('__')
        list_temp = []
        list_temp.append(float(parameters_split[1].split('_')[0]))
        list_temp.append(float(parameters_split[1].split('_')[1]))
        list_temp.append(float(parameters_split[1].split('_')[2]))
        list_temp.append(float(parameters_split[2].split('_')[0]))
        list_temp.append(float(parameters_split[2].split('_')[1]))
        list_temp.append(ast.literal_eval(parameters_split[3]))
        list_model_parameter_auto.append(list_temp)
        
    
    #%% ===========================================================================
    # 
    # =============================================================================
    split               = 0.05
    plot_bankroll       = 0
    plot_bankroll_final = 1
    
    mise_depart         = 0
    mise_pari           = 50
    mise_pari_multi     = 0 
    mise_pari_ajust     = 0
    adaptative_beting   = 0
        
    thres                       = 0.5
    thres_2                     = 0.8
    thres_3                     = 0.35
    thres_R1                    = 2.6
    thres_pos_home              = -0.8
    
    
    list_model_parameter        = [
    #                                [0.50, 0.80, 0.35, 2.60, -0.80, ['1 - 2', '2 - 5']],
    #                                [0.50, 0.80, 0.65, 1.90, +0.15, ['1 - 2', '2 - 5']],
    #                                [0.45, 0.90, 0.35, 1.95, -0.55, ['1 - 2', '2 - 5']],
    #                                [0.65, 0.85, 0.35, 2.80, +0.05, ['1 - 2', '2 - 5']],
    #                                [0.70, 0.45, 0.70, 2.15, -4.00, ['1 - 2', '2 - 5']],
    #                                [0.70, 0.50, 0.30, 2.25, -0.25, ['1 - 2', '2 - 5']],
    #                                [0.35, 0.65, 0.70, 2.25, +0.75, ['1 - 2', '2 - 5']],
    #                                [0.25, 0.70, 0.70, 1.65, -1.25, ['1 - 2', '2 - 5']],                                
    
                                    [0.60, 0.45, 0.75, 2.15, -0.25, ['1 - 1']],
                                    [0.50, 0.45, 0.75, 2.15, -0.20, ['1 - 1']],
                                    
                                    [0.45, 0.45, 0.75, 2.15, -0.65, ['1 - 1']],
                                    [0.50, 0.85, 0.35, 2.10, -0.70, ['1 - 1']],
                                    [0.30, 0.60, 0.75, 1.70, -2.80, ['1 - 1']],
                                    
                                    [0.45, 0.80, 0.45, 2.05, -0.90, ['1 - 1']],
                                    [0.65, 0.60, 0.65, 1.70, -3.40, ['1 - 1']],
                                    [0.50, 0.80, 0.35, 2.60, -0.80, ['1 - 1']],
    
                                  ]
    list_model_parameter        = list_model_parameter_auto
    
    
    df_score_count_seasons      = pd.DataFrame()
    
    dict_df = {}
    
    
    
    for season in list_season:
        exec("df_bankroll_" + season + " = pd.DataFrame()")
    
    fig = ''
    
        
    ### ITERATE EACH SEASON
    for i, season in enumerate(list_season):
        ### ITERATE EACH MODEL
        for j, model_parameter in enumerate(list_model_parameter):
            time.sleep(0.5)
            try:
                thres, thres_2, thres_3, thres_R1, thres_pos_home, list_score   = model_parameter
                model_id = str(thres) + str(thres_2) + str(thres_3) + str(thres_R1) + str(thres_pos_home)# + str(list_score)
                model_id = model_id.replace('.','_').replace('-','_')
        
                # =============================================================================
                # TRAINING
                # =============================================================================            
                print ('START TRAINING ************** ', str(season))
                list_models_features_thres = hockey_model_training_global(season, split, thres, thres_2, thres_3, list_score)
                print ('END TRAINING **************** ', str(season))
            
                # =============================================================================
                # EVALUATION
                # =============================================================================
                print ('START EVALUATING ************** ', str(season))
                df_score_count, df_bankroll, df_bankroll_KPI = hockey_model_evaluation(list_models_features_thres, thres_R1, thres_pos_home, mise_depart, mise_pari, mise_pari_multi)
                df_score_count.columns  = [season, season+'_perc']
                df_score_count_seasons  = pd.concat((df_score_count_seasons, df_score_count), axis=1)
                print ('END EVALUATING **************** ', str(season))
                
        #        df_bankroll_temp = df_bankroll[['bankroll','unique_id','bankroll_pos', 'bankroll_neg', 'good_pred','bad_pred','good_pred_bet_V1']]
                df_bankroll_temp = df_bankroll[['unique_id','bankroll_pos', 'bankroll_neg', 'y_pred']]
                df_bankroll_temp.columns = ['unique_id','bankroll_pos_'+season+model_id, 'bankroll_neg_'+season+model_id, 'y_pred_'+season+model_id]
                df_bankroll_temp.set_index('unique_id', drop=True, inplace=True)    
        
                try:
                    exec("df_bankroll_" + season + " = pd.concat([df_bankroll_" + season + ", df_bankroll_temp], axis=1)")
                except:
                    exec("df_bankroll_" + season + " = df_bankroll_temp.copy()")
                    
        #        
        #        
        #        try:
        #            exec("df_bankroll_" + season + " = pd.merge(df_bankroll_" + season + ", df_bankroll_temp, on='unique_id', how='outer')")
        #        except:
        #            exec("df_bankroll_" + season + " = df_bankroll_temp.copy()")
        #        
                if plot_bankroll == 1:
                    if fig == '':
                        fig = plt.figure()
                        # create figure window
                        gs = gridspec.GridSpec(3, 3)
                        # Creates grid 'gs' of a rows and b columns 
                        
                    ax = plt.subplot(gs[(i/3)%3, i%3])        
                    ax.plot(df_bankroll.bankroll)
                    ax.set_xlabel(season) #Add y-axis label 'Foo' to graph 'ax' (xlabel for x-axis)
                    fig.add_subplot(ax) #add 'ax' to figure
                    ax.autoscale(True)
                    plt.pause(0.0001)
            except:
                pass
        
        
        exec("df_bankroll_" + season + "['bankroll_ecart'] = df_bankroll_" + season + ".max(axis=1) + df_bankroll_" + season + ".min(axis=1)")
    
        exec("df_temp = df_bankroll_" + season + ".copy()")
        df_temp.reset_index(drop=False, inplace=True)
    
        dict_df_check = df_temp.to_dict(orient='index')
        mise_pari_ajust = 0
        for i in range(len(dict_df_check)):
            item = dict_df_check[i]
        
            try:
                bankroll = dict_df_check[i-1]['bankroll']
            except:
                bankroll = mise_depart
            
            dict_df_check[i].update({'mise_pari_multi':mise_pari_multi})
    
            if adaptative_beting == 1:
                if df_temp.bankroll_ecart.iloc[i] == 0:
                    bet_ratio = 0
                if df_temp.bankroll_ecart.iloc[i] < 0:
                    bet_ratio = -1
                if df_temp.bankroll_ecart.iloc[i] > 0:
                    bet_ratio = df_temp.bankroll_ecart.iloc[i]/float(mise_pari)
                    
                if mise_pari_ajust < mise_pari:
                    mise_pari_ajust = mise_pari
                else:
                    if mise_pari_ajust < bankroll/4.0:
                        mise_pari_ajust = bankroll/4.0
                
                if bankroll < mise_depart*2:
                    mise_pari_ajust = mise_pari
        
                bankroll = bankroll + mise_pari_ajust*bet_ratio
            else:
                bankroll = bankroll + df_temp.bankroll_ecart.iloc[i]
            
            dict_df_check[i].update({'bankroll' : bankroll})
        
        df_check = pd.DataFrame(dict_df_check).T
        exec("df_bankroll_" + season + "_mix = df_check.copy()")
    
    
    
    
    fig = ''
    
    ### ITERATE EACH SEASON
    nbr_graph = len(list_season)
    for i, season in enumerate(list_season):
        exec("df_bankroll = df_bankroll_" + season + "_mix.copy()")
    #    df_bankroll.set_index('unique_id', drop=True, inplace=True)    
    #    df_bankroll['bankroll_sum'] = df_bankroll.sum(axis=1)
        df_bankroll.reset_index(drop=False, inplace=True)
        
    #    plt.figure()
    #    df_bankroll.bankroll_sum.plot()
    #    
        
        if nbr_graph >= 3:
            x_ = 3
        else:
            x_ = nbr_graph
        
        y_ = 3
        if nbr_graph <= 6:
            y_ = 2
        if nbr_graph <= 3:
            y_ = 1
            
        if plot_bankroll_final == 1:
            if fig == '':
                fig = plt.figure()
                # create figure window
                gs = gridspec.GridSpec(y_, x_)
                # Creates grid 'gs' of a rows and b columns 
                
            ax = plt.subplot(gs[(i/3)%3, i%3])        
            ax.plot(df_bankroll.bankroll)
            ax.set_xlabel(season) #Add y-axis label 'Foo' to graph 'ax' (xlabel for x-axis)
            fig.add_subplot(ax) #add 'ax' to figure
            ax.autoscale(True)
            plt.pause(0.1)
    
    
    # =============================================================================
    # SAVE FIG
    # =============================================================================
    date_str    = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    save_name   = '../model/fig/' + date_str + '_' + str(min_valuemax) + '_' + str(min_valuemin) + '.jpg'
    plt.savefig(save_name)
    
    
    #% ===========================================================================
    # NEXT MATCH BET
    # =============================================================================
    
    a = df_bankroll_2018_2019_mix.copy()
    
    a['date_match'] = df_bankroll_2018_2019_mix.unique_id.apply(lambda x : x[:19])
    a['match_name'] = df_bankroll_2018_2019_mix.unique_id.apply(lambda x : x[19:])
    
    a['date_match'] = pd.to_datetime(a.date_match)
    aa = a.copy()
    a = a[a.date_match > (datetime.datetime.utcnow() + timedelta(days=-1))]
        
    a.set_index('date_match', drop=True, inplace=True)
    
    a               = a[(a.columns[pd.Series(a.columns).str.startswith('y_pred')]) | (a.columns[pd.Series(a.columns).str.startswith('match')])]
    a['bet_action'] = a[a.columns[pd.Series(a.columns).str.startswith('y_pred')]].max(axis=1)
    
    aa['bet_action'] = aa[aa.columns[pd.Series(aa.columns).str.startswith('y_pred')]].sum(axis=1)
    aa = aa[['date_match','match_name','bet_action','bankroll']]
    bb = aa[aa.date_match > (datetime.datetime.utcnow() + timedelta(days=-1))]
    
    bet_todo        = a[a.columns[pd.Series(a.columns).str.startswith('y_pred')]].max(axis=1).sum()
    
    b = a.copy()
    b['Winner_Bet'] = ""
    c = a.match_name[a.bet_action == 1].apply(lambda x : x.split('_')[0].rjust(20, '.'))
    
    if bet_todo >= 1:
        subject         = 'HOCKEY - YES BET TODAY'
        body_message    = 'min_valuemax : ' + str(min_valuemax) + '\nmin_valuemin : ' + str(min_valuemin) + '\nFinal Bankroll : ' + str(aa.bankroll.iloc[-1]) + '\n----------------------------------------------------------------\n'
        body_message    = body_message  + str(c) + '\n----------------------------------------------------------------\n' + str(bb)
        print('8888888888888888888888888888888888888888888888888888888888888888')
        print('8888888888888888888888888888888888888888888888888888888888888888')
        print('8888888888888888888888888888888888888888888888888888888888888888')
        print('88888888888888          BET TIME !!!!!!!!!!      888888888888888')
        print('8888888888888888888888888888888888888888888888888888888888888888')
        print('8888888888888888888888888888888888888888888888888888888888888888')
        print('8888888888888888888888888888888888888888888888888888888888888888')
        print '\n'
        print c
        print '\n'
        print('----------------------------------------------------------------')
        print '\n'
        print bb
        print '\n'
        print('8888888888888888888888888888888888888888888888888888888888888888')
        print('8888888888888888888888888888888888888888888888888888888888888888')
        print('8888888888888888888888888888888888888888888888888888888888888888')
    else:
        subject = 'HOCKEY - .... NO BET TODAY'
        body_message    = 'min_valuemax : ' + str(min_valuemax) + '\nmin_valuemin : ' + str(min_valuemin) + '\nFinal Bankroll : ' + str(aa.bankroll.iloc[-1]) + '\n----------------------------------------------------------------\n'
        body_message    = body_message  + str(c) + '\n----------------------------------------------------------------\n' + str(bb)
        print('................................................................')
        print('...............       NO BET TODAY .....         ...............')
        print('................................................................')
        
    
    
    #email_send_without_attachments('mdesmarez@gmail.com', body_message, subject, "eatsy.me@gmail.com", 'pepitefinder2015')
    email_send_html_with_attachment('mdesmarez@gmail.com', body_message, subject, save_name, "eatsy.me@gmail.com", 'pepitefinder2015')
    
    return a, aa, b, bb, c


# =============================================================================
# =============================================================================
# =============================================================================
# # # 
# =============================================================================
# =============================================================================
# =============================================================================
list_season  = [\
#           '2005_2006',           
#           '2006_2007',           
#           '2007_2008',           
#           '2008_2009',           
#           '2009_2010',           
#            '2010_2011',           
#            '2011_2012',           
#            '2012_2013',           
#            '2013_2014',           
#            '2014_2015',
#            '2015_2016',
#            '2016_2017',
#            '2017_2018',
            '2018_2019',
            ]
list_season.sort()

list_valuemax = [
#                 [30, -20],
                 [40, -10],
#                 [50, -20],
#                 [70, -10],
#                 [80, -10],
#                 [90, -10],
                 ]

min_valuemax = 50
min_valuemin = -8
#a, aa, b, bb, c = result_viewer(min_valuemax, min_valuemin)

for item in list_valuemax:
    min_valuemax = item[0]
    min_valuemin = item[1]
    a, aa, b, bb, c = result_viewer(min_valuemax, min_valuemin)
