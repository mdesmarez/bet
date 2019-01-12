#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 11:41:56 2018

@author: mathieu
"""

# =============================================================================
# IMPORT PACKAGES
# =============================================================================
import datetime
import json
import os

import matplotlib.pyplot  as plt
import pandas             as pd
import numpy              as np

from datetime                                                                  import datetime
from datetime                                                                  import timedelta

from PS3838_support_function                                                   import encode_decode, match_filter_prediction, optimisation_7_apply




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
df_result_single.dropna(inplace=True)
df_result_single.sport = df_result_single.sport.apply(lambda x : x.lower().replace('-',' '))

###
df_merge                           = pd.merge(df_parlay, df_result, how='inner', on=['match_date','sport','team_home'])
df_merge = df_merge[['match_date','sport','ligue','bet_1','bet_2','bet_X','bet_diff','min_bet','winner','prediction','score']]
df_merge['good_pred']                          = 0
df_merge.good_pred[df_merge.prediction == df_merge.winner] = 1
df_merge['bad_pred']                           = 0
df_merge.bad_pred[df_merge.prediction != df_merge.winner]  = 1
df_merge.match_date                = df_merge.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

###
df_merge_single                           = pd.merge(df_single, df_result_single, how='inner', on=['match_date','sport','team_home'])
df_merge_single = df_merge_single[['match_date','sport','ligue','bet_1','bet_2','bet_X','bet_diff','min_bet','winner','prediction','team_home']]
df_merge_single['good_pred']                          = 0
df_merge_single.good_pred[df_merge_single.prediction == df_merge_single.winner] = 1
df_merge_single['bad_pred']                           = 0
df_merge_single.bad_pred[df_merge_single.prediction != df_merge_single.winner]  = 1
df_merge_single.match_date                = df_merge_single.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))


# =============================================================================
# 
# =============================================================================
initial_bankroll            = 300
bankroll                    = initial_bankroll
mise                        = 20
min_cave                    = 0
max_cave                    = 0    
day_train                   = 1
day_shift                   = 0
total_result                = 0
total_cave                  = 0
total_nbr_bet               = 0
list_day_shift              = list(np.linspace(0,50,51))
#list_day_shift              = [0, 1, 2, 3, 4, 5, 6, 7]#, 8, 9, 10]
#list_day_shift              = [10, 11, 12, 13]#, 4, 5, 6, 7]#, 8, 9, 10]
df_loss                     = pd.DataFrame()
df_win                      = pd.DataFrame()

list_day_shift.sort(reverse=True)
dict_bankroll               = {}
dict_bankroll_day           = {}
dict_parameter_sport_single = {}
dict_result_sport           = {}
df_merge_single_modif       = df_merge_single.copy()
df_parameter_sport          = pd.DataFrame()


########
#df_single = df_single[((df_single.sport == 'hockey') & (df_single.bet_X != 0)) | (df_single.sport == 'soccer')]
#df_single.dropna(inplace=True)
########

for day_shift in list_day_shift:
#    mise       = bankroll*3/100
    result     = 0
    cave       = 0.001
        
    date_min = datetime.now()-timedelta(hours=24*day_shift) - timedelta(hours=24*day_train)
    date_max = datetime.now()-timedelta(hours=24*day_shift)
    
    hour_test = 23
    date_min = date_min.replace(hour=hour_test, minute=59, second=00)
    date_max = date_max.replace(hour=hour_test, minute=59, second=00)
    
    df_train    = df_merge_single_modif[(df_merge_single_modif.match_date < date_min)]
    df_test     = df_merge_single_modif[(df_merge_single_modif.match_date >= date_min) & (df_merge_single_modif.match_date <= date_max)]

    date_text = (datetime.now()-timedelta(hours=24*day_shift))

#    if date_text.strftime("%w") in ['0','5','6']:
    if date_text.strftime("%w") in ['0','1','2','3','4','5','6']:
        
        print '\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print date_min.strftime('%d, %B %Y - %a'), ' / ', date_max.strftime('%d, %B %Y - %a')    
        with open('../model/local/dict_parameter_sport.json') as json_file:  
            dict_parameter_sport = json.load(json_file)
        
        """
        df_test = df_single.copy()
        df_test = df_single[df_single.sport == 'esports']
        """
        df_single_filter = optimisation_7_apply(df_test, dict_parameter_sport)
    #        df_parameter_sport = pd.concat((df_parameter_sport, df_parameter_sport_temp))
    
        
        num_good_pred         = 0
        num_good_draw_pred    = 0
        num_bad_pred          = 0
        for item in range(len(df_single_filter)):
            total_nbr_bet = total_nbr_bet + 1
            
            min_bet = df_single_filter.min_bet.iloc[item]+0.0000001
            bet_X   = df_single_filter.bet_X.iloc[item]+0.0000001
            bet_DC  = 1/((1/min_bet)+(1/bet_X))
            bet_DNB = (1-(1/bet_X))*min_bet
            bet_WNB = (1-(1/min_bet))*bet_X
            sport   = df_single_filter.sport.iloc[item]
    
            try:
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result']
            except:
                dict_result_sport.update({sport:{'result':0}})
                                    
    
            if df_single_filter.mode_bet.iloc[item] == 'DC':
                cave = cave + mise
                result = result - mise
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] - mise})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] - mise
    
                if df_single_filter.good_pred.iloc[item] == 1 or df_single_filter.winner.iloc[item] == 0:
                    result = result + bet_DC*mise
                    dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + bet_DC*mise})
                    dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + bet_DC*mise
                    num_good_draw_pred = num_good_draw_pred + 1
                    df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
                else:
                    num_bad_pred = num_bad_pred + 1
                    df_loss = pd.concat((df_loss, pd.DataFrame(df_single_filter.iloc[item]).T))
    
    
            if df_single_filter.mode_bet.iloc[item] == 'DNB':
                cave = cave + mise
                result = result - mise
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] - mise})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] - mise
    
                if df_single_filter.good_pred.iloc[item] == 1:
                    result = result + bet_DNB*mise
                    dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + bet_DNB*mise})
                    dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + bet_DNB*mise
    
                    df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
                    
                if df_single_filter.winner.iloc[item] == 0:
                    result = result + mise
                    dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + mise})
                    dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + mise
    
                    num_good_draw_pred = num_good_draw_pred + 1
                    df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
    
                
                if df_single_filter.good_pred.iloc[item] == 0 and df_single_filter.winner.iloc[item] != 0:
                    num_bad_pred = num_bad_pred + 1
                    df_loss = pd.concat((df_loss, pd.DataFrame(df_single_filter.iloc[item]).T))
    
                    
            if df_single_filter.mode_bet.iloc[item] == 'WNB':
                cave = cave + mise
                result = result - mise
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] - mise})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] - mise
    
                
                if df_single_filter.good_pred.iloc[item] == 1:
                    result = result + mise
                    dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + mise})
                    dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + mise
    
                    df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
                    
                if df_single_filter.winner.iloc[item] == 0:
                    result = result + bet_WNB*mise
                    dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + bet_WNB*mise})
                    dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + bet_WNB*mise
    
                    num_good_draw_pred = num_good_draw_pred + 1
                    df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
                
                if df_single_filter.good_pred.iloc[item] == 0 and df_single_filter.winner.iloc[item] != 0:
                    num_bad_pred = num_bad_pred + 1
                    df_loss = pd.concat((df_loss, pd.DataFrame(df_single_filter.iloc[item]).T))
                    
                                        
            
            if df_single_filter.mode_bet.iloc[item] == 'X':
                cave = cave + mise*2
                result = result - mise*2
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] - mise*2})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] - mise*2
    
                if df_single_filter.good_pred.iloc[item] == 1 and df_single_filter.winner.iloc[item] != 0:
                    result = result + df_single_filter.min_bet.iloc[item]*mise
                    dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + df_single_filter.min_bet.iloc[item]*mise})
                    dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + df_single_filter.min_bet.iloc[item]*mise
    
                    num_good_draw_pred = num_good_draw_pred + 1
                    df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
                
                if df_single_filter.winner.iloc[item] == 0:
                    result = result + df_single_filter.bet_X.iloc[item]*mise
                    dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + df_single_filter.bet_X.iloc[item]*mise})
                    dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + df_single_filter.bet_X.iloc[item]*mise
    
                    num_good_draw_pred = num_good_draw_pred + 1
                    df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
                
                if df_single_filter.good_pred.iloc[item] == 0 and df_single_filter.winner.iloc[item] != 0:
                    num_bad_pred = num_bad_pred + 1
                    df_loss = pd.concat((df_loss, pd.DataFrame(df_single_filter.iloc[item]).T))
    
    
            if df_single_filter.mode_bet.iloc[item] == 'S':
                cave = cave + mise
                result = result - mise
                dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] - mise})
                dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] - mise
    
                if df_single_filter.good_pred.iloc[item] == 1:
                    result = result + df_single_filter.min_bet.iloc[item]*mise
                    dict_result_sport[sport].update({day_shift:dict_result_sport[sport]['result'] + + df_single_filter.min_bet.iloc[item]*mise})
                    dict_result_sport[sport]['result'] = dict_result_sport[sport]['result'] + df_single_filter.min_bet.iloc[item]*mise
    
                    num_good_pred = num_good_pred + 1
                    df_win = pd.concat((df_win, pd.DataFrame(df_single_filter.iloc[item]).T))
                else:
                    num_bad_pred = num_bad_pred + 1
                    df_loss = pd.concat((df_loss, pd.DataFrame(df_single_filter.iloc[item]).T))
            
            
        if len(df_single_filter) != 0:
            print('******** RESULT SIMULATION **********')
    #        print dict_parameter_sport
            print 'Mise                  : ', int(mise), '€'
            print 'Number Good pred      : ', num_good_pred
            print 'Number Good Draw pred : ', num_good_draw_pred
            print 'Number Bad pred       : ', num_bad_pred
            print '% : ', round(num_good_pred/float(num_good_pred+num_bad_pred+0.01)*100,2), '%'
            print 'Mean bet : ', df_single_filter.min_bet.mean()
            print 'cave     : ', int(cave),' €'
            print 'gain pur : ', int(result),' €'
            print 'ROI cave : ', round(result/float(cave)*100,2), '%'
            print 'ROI mise : ',round(result/mise,2)*100,"%"
            print('*************************************')
                
        bankroll     = bankroll + result
        total_result = total_result + result
        total_cave   = total_cave + cave   
        
        if total_result < min_cave:
            min_cave = total_result 
        if total_result > max_cave:
            max_cave = total_result
            
    
        print 'BANKROLL       : ', int(bankroll), '€'
        print 'GAIN TOTAL     : ', int(total_result), '€'
        print 'INVEST TOTAL   : ', int(total_cave)
        print 'NBR BET TOTAL  : ', total_nbr_bet
        print 'ROI cave       : ', round(total_result/float(total_cave)*100,2), '%'
        print 'ROC cave       : ', round(total_result/float(initial_bankroll)*100,2), '%'
        print 'MIN CAVE       : ', int(min_cave), '€', int(round(min_cave/mise))
        print 'MAX CAVE       : ', int(max_cave), '€', int(round(max_cave/mise))
        print ''
        
        try:
            list_sport_win_loss = list(set(df_win.sport.unique().tolist()+df_loss.sport.unique().tolist()))
            for sport in list_sport_win_loss:
                df_win['mod'] = df_win.min_bet/dict_parameter_sport['option'][sport]['mod_value']
                df_win['mod'] = df_win['mod'].apply(lambda x: int(x))
                df_loss['mod'] = df_loss.min_bet/dict_parameter_sport['option'][sport]['mod_value']
                df_loss['mod'] = df_loss['mod'].apply(lambda x: int(x))
                
                
                df_win['gain'] = 0
                df_win.gain[df_win.mode_bet == 'S'] = (df_win.min_bet[df_win.mode_bet == 'S']-1) * mise
                df_win.gain[(df_win.mode_bet == 'WNB') & (df_win.winner == 0)] = (df_win.bet_X[(df_win.mode_bet == 'WNB') & (df_win.winner == 0)]*(1-(1/df_win.min_bet[(df_win.mode_bet == 'WNB') & (df_win.winner == 0)]))-1) * mise
                df_loss['gain'] = -mise
                
                total = str(len(df_win[df_win.sport == sport]) + len(df_loss[df_loss.sport == sport]))
                total_gain = str(int(df_win[df_win.sport == sport]['gain'].sum() + df_loss[df_loss.sport == sport]['gain'].sum()))
                print sport, '=> ', total.rjust(4), 'bet /', total_gain.rjust(4), 'euros /', round(100*len(df_win[df_win.sport == sport])/float(len(df_win[df_win.sport == sport])+len(df_loss[df_loss.sport == sport])),2),'%'
                list_mod_win_loss = list(set(df_win[u'mod'][df_win.sport == sport].unique().tolist()+df_loss[u'mod'][df_loss.sport == sport].unique().tolist()))
                for mod in list_mod_win_loss:
                    print '*', round(mod*0.1,1), '-', round((mod+1)*0.1,1), '=>', str(len(df_win[df_win[u'mod'] == mod][df_win.sport == sport])+len(df_loss[df_loss[u'mod'] == mod][df_loss.sport == sport])).rjust(4), 'bet /', str(int(sum(df_win['gain'][df_win[u'mod'] == mod])+sum(df_loss['gain'][df_loss[u'mod'] == mod]))).rjust(4)   , 'euros /',  round(100*len(df_win[df_win[u'mod'] == mod][df_win.sport == sport])/float(len(df_win[df_win[u'mod'] == mod][df_win.sport == sport])+len(df_loss[df_loss[u'mod'] == mod][df_loss.sport == sport])),1),'%'
        except:
            pass
        print '******************************************'
    
    
        dict_bankroll.update({date_text.strftime("%Y %m %d - %a"):{'total':total_result,'result':result, 'day':date_text.strftime("%a"), 'nbr_bet':len(df_single_filter)}})
    

df_dict_result = pd.DataFrame.from_dict(dict_bankroll, orient='index')
df_dict_result.sort_index(inplace=True)
df_dict_result['line'] = 0
df_dict_result['ratio'] = df_dict_result.result/df_dict_result.nbr_bet

title = 'mise : ' + str(int(mise))
df_dict_result.plot(title=title)

df_dict_result_sport = pd.DataFrame.from_dict(dict_result_sport, orient='index').T
df_dict_result_sport = df_dict_result_sport[df_dict_result_sport.index != 'result']
df_dict_result_sport.sort_index(ascending=False,inplace=True)
df_dict_result_sport = df_dict_result_sport.fillna(method='bfill')
df_dict_result_sport.fillna(0, inplace=True)
df_dict_result_sport['total'] = df_dict_result_sport.sum(axis=1)
df_dict_result_sport.plot()

print df_dict_result.groupby('day').sum()
#del df_dict_result['total']
df_dict_result.groupby('day').sum().plot()

aa = pd.concat((df_win,df_loss))
aa['date_day'] = aa.match_date.apply(lambda x: x.strftime("%Y %m %d %H"))
aaa = pd.DataFrame(aa.groupby('date_day').gain.sum())
aaa['result'] = aaa.gain.cumsum()
aaa.to_csv('../dataset/local/result_soccer.csv')



"""
## =============================================================================
## 
## =============================================================================
os.system('wget http://35.195.3.155:8080/bet/prod/bet/dataset/local/df_parlay.xls')
os.system('mv df_parlay.xls df_parlay_server.xls')
os.system('mv df_parlay_server.xls ../dataset/local/df_parlay_server.xls')

os.system('wget http://35.195.3.155:8080/bet/prod/bet/dataset/local/df_single.xls')
os.system('mv df_single.xls df_single_server.xls')
os.system('mv df_single_server.xls ../dataset/local/df_single_server.xls')

os.system('wget http://35.195.3.155:8080/bet/prod/bet/dataset/local/df_result.xls')
os.system('mv df_result.xls df_result_server.xls')
os.system('mv df_result_server.xls ../dataset/local/df_result_server.xls')

os.system('wget http://35.195.3.155:8080/bet/prod/bet/dataset/local/df_real_betting_single.xls')
os.system('mv df_real_betting_single.xls df_real_betting_single_serveur.xls')
os.system('mv df_real_betting_single_serveur.xls ../dataset/local/df_real_betting_single_serveur.xls')

os.system('wget http://35.195.3.155:8080/bet/prod/bet/dataset/local/df_futur_bet.xls')
os.system('mv df_futur_bet.xls df_futur_bet_serveur.xls')
os.system('mv df_futur_bet_serveur.xls ../dataset/local/df_futur_bet_serveur.xls')

df_single_server                = pd.DataFrame.from_csv('../dataset/local/df_single_server.xls', encoding='utf-8')
df_parlay_server                = pd.DataFrame.from_csv('../dataset/local/df_parlay_server.xls', encoding='utf-8')
df_result_server                = pd.DataFrame.from_csv('../dataset/local/df_result_server.xls', encoding='utf-8')
df_futur_bet_serveur            = pd.DataFrame.from_csv('../dataset/local/df_futur_bet_serveur.xls', encoding='utf-8')
df_real_betting_single_serveur  = pd.DataFrame.from_csv('../dataset/local/df_real_betting_single_serveur.xls', encoding='utf-8')


df_single = pd.DataFrame.from_csv('../dataset/local/df_single.xls', encoding='utf-8')
df_parlay = pd.DataFrame.from_csv('../dataset/local/df_parlay.xls', encoding='utf-8')
df_result = pd.DataFrame.from_csv('../dataset/local/df_result.xls', encoding='utf-8')
df_real_betting_single = pd.DataFrame.from_csv('../dataset/local/df_real_betting_single.xls', encoding='utf-8')


df_result               = df_result_server.copy()
df_single               = df_single_server.copy()
df_result               = df_result_server.copy()
df_futur_bet            = df_futur_bet_serveur.copy()
df_real_betting_single  = df_real_betting_single_serveur.copy()


df_result.to_csv('../dataset/local/df_result.xls', encoding='utf-8')
df_parlay.to_csv('../dataset/local/df_parlay.xls', encoding='utf-8')
df_single.to_csv('../dataset/local/df_single.xls', encoding='utf-8')
df_futur_bet.to_csv('../dataset/local/df_futur_bet.xls', encoding='utf-8')
df_real_betting_single.to_csv('../dataset/local/df_real_betting_single.xls', encoding='utf-8')
"""

#%%

ee
# =============================================================================
# Prepare bet SINGLE
# =============================================================================
#df_betting_single_done = pd.DataFrame()
#list_bet_single_done             = glob('../dataset/local/Real_df_betting_single*.xls')
#for i, bet_single_done in enumerate(list_bet_single_done):
#    df_betting_single_done_temp = pd.DataFrame.from_csv(bet_single_done, encoding='utf-8')
#    df_betting_single_done_temp['bet_num'] = i 
#    df_betting_single_done = pd.concat((df_betting_single_done, df_betting_single_done_temp))

df_betting_single_done = pd.DataFrame.from_csv('../dataset/local/df_real_betting_single.xls', encoding='utf-8')

try:
    list_already_bet_single = df_betting_single_done.team_to_bet_id.unique().tolist()
except:
    list_already_bet_single = []
    
df_betting_single_done['prediction'] = 2
df_betting_single_done.prediction[df_betting_single_done.team_to_bet == df_betting_single_done.team_home] = 1

df_merge_single_bet = pd.merge(df_betting_single_done, df_result_single, how='inner', on=['match_date','sport','team_home'])
df_merge_single_bet = df_merge_single_bet[['match_date','sport','ligue','bet_diff','min_bet','winner','prediction','team_home','bet_X']]
df_merge_single_bet['good_pred']                          = 0
df_merge_single_bet.good_pred[df_merge_single_bet.prediction == df_merge_single_bet.winner] = 1
df_merge_single_bet['bad_pred']                           = 0
df_merge_single_bet.bad_pred[df_merge_single_bet.prediction != df_merge_single_bet.winner]  = 1
df_merge_single_bet.match_date                = df_merge_single_bet.match_date.apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))





df_merge_single_bet = df_merge_single_bet[df_merge_single_bet.sport == 'soccer']




# =============================================================================
#  1 bet
# =============================================================================    
print('1 BY 1')
result  = 0
cave    = 0
mise    = 5
draw_activated              = 1


num_good_pred   = 0
num_bad_pred    = 0
    
for item in range(len(df_merge_single_bet)):
    if (df_merge_single_bet.min_bet.iloc[item] < 1.1) and (draw_activated == 1):
        pass
    else:
        if draw_activated == 1:
            cave = cave + mise*2
        else:
            cave = cave + mise
    
        if draw_activated == 1:
            result = result - mise*2
        else:
            result = result - mise
            
        if df_merge_single_bet.good_pred.iloc[item] == 1:
            result = result+(df_merge_single_bet.min_bet.iloc[item])*mise
        if draw_activated == 1 and df_merge_single_bet.winner.iloc[item] == 0:
            result = result+(df_merge_single_bet.bet_X.iloc[item])*mise
            df_merge_single_bet['good_pred'].iloc[item]  = 1
            df_merge_single_bet['bad_pred'].iloc[item]   = 0
        if (df_merge_single_bet.good_pred.iloc[item] == 1) or (draw_activated == 1 and df_merge_single_bet.winner.iloc[item] == 0):
            num_good_pred = num_good_pred + 1
        else:
            num_bad_pred = num_bad_pred + 1
                

print('******** RESULT SIMULATION **********')
print 'Number bet engaged : ', len(df_betting_single_done)
print 'Cave engaged       : ', (len(df_betting_single_done)-len(df_merge_single_bet))*mise*2
print 'Bet engaged        : ', (len(df_betting_single_done)-len(df_merge_single_bet))
print 'Number Good pred   : ', num_good_pred
print 'Number Bad pred    : ', num_bad_pred
print '% : ', round(num_good_pred/float(num_good_pred+num_bad_pred)*100,2), '%'
print ''
print 'cave     : ', int(cave),' €'
print 'gain pur : ', round(result,2),' €'
print 'ROI cave : ', round(result/float(cave)*100,2), '%'
print round(result/mise,2)*100,"%"
print('*************************************')
print ''



#dict_bankroll = {}
#for i in range(5):
#    print('******************************************')
#    last_X_days = 1*i
#    print last_X_days, ' jours'
#    df_merge_single_bet_result = df_merge_single_bet[(df_merge_single_bet.match_date > datetime.now()-timedelta(hours=24*last_X_days))]
#
#    # =============================================================================
#    #  1 bet
#    # =============================================================================    
#    print('1 BY 1')
#    result  = 0
#    cave    = 0
#    for item in range(len(df_merge_single_bet_result)):
#        cave = cave + mise
#        if df_merge_single_bet_result.good_pred.iloc[item] == 1:
#            result = result+(df_merge_single_bet_result.min_bet.iloc[item]-1)*mise
#        else:
#            result = result - mise
#    print 'cave     : ', int(cave),' €'
#    print 'gain pur : ', round(result,2),' €'
#    print round(result/mise,2)*100,"%"
#    print ''
#    dict_bankroll.update({last_X_days:[result]})
#    
#
#df_dict_result = pd.DataFrame.from_dict(dict_bankroll, orient='index')
#df_dict_result.sort_index(inplace=True)
#df_dict_result.plot()




eee

#%%

last_X_days = 1
    
###
df_merge_train = df_merge[(df_merge.match_date < datetime.now()-timedelta(hours=24*last_X_days))]
###
#df_merge_train = df_merge_single[(df_merge_single.match_date < datetime.now()-timedelta(hours=24*last_X_days))]

df_merge_train['sport'] = df_merge_train['sport'].apply(lambda x : x.lower()) 

# =============================================================================
# Ajust bet parameter
# =============================================================================
df_temp = 0
list_sport = df_merge_train.sport.unique().tolist()
dict_parameter_sport = {}

#list_sport = ['volleyball']
#list_sport = ['soccer']
#list_sport = ['handball']


###
df = df_merge[(df_merge.match_date >= datetime.now()-timedelta(hours=24*last_X_days))]
###
df = df_merge_single[(df_merge_single.match_date >= datetime.now()-timedelta(hours=24*last_X_days))]

list_sport = df.sport.unique().tolist()
df_parlay_filter = pd.DataFrame()

for item in list_sport:
    print '\n' + item
    exec('df_merge_' + item.replace(' ','_') + ' = df_merge_train[df_merge_train.sport == "' + item + '"]')
    exec('df_temp = df_merge_' + item.replace(' ','_'))
    dict_temp = optimisation_3(df_temp)
    dict_parameter_sport.update(dict_temp)
    
#    if item == 'basketball':
#        ee
        
    try:
        bet_min      = dict_parameter_sport[item]['bet_min']
        bet_max      = dict_parameter_sport[item]['bet_max']
        bet_ecart    = dict_parameter_sport[item]['bet_ecart']
        num_total    = dict_parameter_sport[item]['num_total']
        max_bankroll = dict_parameter_sport[item]['max_bankroll']
    
        if num_total > 50:# and max_bankroll >= 2:
            df_sport    = df[df.sport == item]
            df_sport    = match_filter_prediction(df_sport, bet_max, bet_min, bet_ecart)
            df_parlay_filter = pd.concat((df_parlay_filter, df_sport))
        else:
            print 'too less data for ',item
        
    except:
        print 'no', item

#df_parlay_filter = df_parlay_filter[(df_parlay_filter.match_date >= datetime.now()-timedelta(hours=24*3))]
            
#df_parlay_filter.drop_duplicates(subset=['match_date','team_home'], inplace=True)

print('******** RESULT SIMULATION **********')
print 'Number Good pred : ', len(df_parlay_filter)
print 'Number Bad pred  : ', len(df_parlay_filter[df_parlay_filter.good_pred == 0])
print round(df_parlay_filter.good_pred.sum()/float(len(df_parlay_filter))*100,2), '%'
print('*************************************')

mise = 5
print('1 BY 1')
result = 0
cave = 0
for item in range(len(df_parlay_filter)):
    cave = cave + mise
    if df_parlay_filter.good_pred.iloc[item] == 1:
        result = result+(df_parlay_filter.min_bet.iloc[item]+0.0-1)*mise
    else:
#        print 'lose'
        result = result - mise
print 'cave     : ', int(cave),' €'
print 'gain pur : ', int(result),' €'
print 'ROI cave : ', round(result/float(cave)*100,2), '%'
print 'ROI mise : ',round(result/mise,2)*100,"%"
print ''
    
df_parlay_filter[df_parlay_filter.good_pred == 1].min_bet.mean()




#%%

import matplotlib.pyplot                                                       as plt
import matplotlib.gridspec                                                     as gridspec

"""
df_parameter_sport = df_parameter_sport_temp.copy()
"""

df_parameter_sport_soccer = df_parameter_sport[df_parameter_sport.sport == 'soccer']
#df_parameter_sport_soccer = df_parameter_sport[df_parameter_sport.sport == 'hockey']

#df_parameter_sport_soccer.reset_index(inplace=True)

df_parameter_sport_soccer.bet_min = df_parameter_sport_soccer.bet_min.apply(lambda x : int(round(x,2)*10))

fig = ''
num_x = 5
num_y = 4
for i in range(num_x*num_y):
    df = df_parameter_sport_soccer[df_parameter_sport_soccer.bet_min == (10+i)]
    df = df[['date','S','DNB','WNB','DC']]
#    df = df[['date','S']]
    df.sort_values('date', inplace=True)
    df.set_index('date', inplace=True)
    if len(df) != 0:
        if df.iloc[-1].sum() > -100 :
            title = str(round((10+i)/10.0,2))
    #        df.plot(title=title)
    
    
            if fig == '':
                fig = plt.figure()
                # create figure window
                gs = gridspec.GridSpec(num_y, num_x)
                # Creates grid 'gs' of a rows and b columns 
                
            ax = plt.subplot(gs[(i/num_x)%num_x, i%num_x])        
            ax.plot(df)
            ax.set_xlabel(title) #Add y-axis label 'Foo' to graph 'ax' (xlabel for x-axis)
            fig.add_subplot(ax) #add 'ax' to figure
            ax.autoscale(True)
            plt.pause(0.0001)
            
#%%
df = df_train[df_train.sport == 'soccer']
mod = 2.4
df = df[(df.min_bet>mod) & (df.min_bet<=mod+0.1)]

print ''
print df.bet_diff.mean(), df.min_bet.mean(), df.bet_X.mean()
print ''


list_high_S   = []
list_high_SX  = []
nbr_total_bet = len(df) 
step_diff_bet = 0.1
for i in range(80):
    if len(df) > (nbr_total_bet*0.1):
        df = df[df.bet_diff > i*step_diff_bet]
        list_high_S.append(round(len(df[df.good_pred == 1])/float(len(df)),3))
        list_high_SX.append(round((len(df[df.good_pred == 1]) + len(df[(df.winner == 0) & (df.good_pred == 0)]))/float(len(df)),3)) 
        print str(i*step_diff_bet).zfill(4), str(len(df)).zfill(4), round(len(df[df.good_pred == 1])/float(len(df)),3), round((len(df[df.good_pred == 1]) + len(df[(df.winner == 0) & (df.good_pred == 0)]))/float(len(df)),3)
index_list_high_S  = max(xrange(len(list_high_S)), key=list_high_S.__getitem__)
index_list_high_SX = max(xrange(len(list_high_SX)), key=list_high_SX.__getitem__)
bet_diff_high_S    = index_list_high_S*step_diff_bet
bet_diff_high_SX   = index_list_high_SX*step_diff_bet

print 'S  : ', list_high_S[index_list_high_S], 'bet_diff :', bet_diff_high_S
print 'SX : ', list_high_SX[index_list_high_SX], 'bet_diff :', bet_diff_high_SX





ee
