#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 10:29:04 2018

@author: mathieu
"""

# =============================================================================
# Library Call
# =============================================================================
import os
import time

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


# =============================================================================
#
# =============================================================================
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    import itertools

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def modelfit(alg, columns, X_train, y_train, X_val, y_val, useTrainCV, cv_folds=5, early_stopping_rounds=50):

    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xg_train = xgb.DMatrix(X_train, label=y_train)
        cvresult = xgb.cv(
                xgb_param,
                xg_train,
                num_boost_round=alg.get_params()['n_estimators'],
                nfold=cv_folds,
                metrics='auc',
                early_stopping_rounds=early_stopping_rounds,
                stratified=True,
                verbose_eval=True,
                )
        alg.set_params(n_estimators=cvresult.shape[0])
        print("\nBest number of estimators: {}".format(cvresult.shape[0]))

    #Fit the algorithm on the data
    alg.fit(X_train, y_train, eval_set=[(X_val, y_val)], eval_metric='auc', early_stopping_rounds=early_stopping_rounds, verbose=True)

    #Predict validation set:
    y_pred = alg.predict(X_val)
    y_predprob = alg.predict_proba(X_val)[:,1]
#    model.predict(xg_val, ntree_limit=model.best_ntree_limit)

    #Print model report:
    print "\nModel Report"
    print "Validation Accuracy : %.4g" % metrics.accuracy_score(y_val.values, y_pred)
    print "AUC Score (Val): %f" % metrics.roc_auc_score(y_val, y_predprob)

    #Plot Confusion Matrix
    cm = confusion_matrix(y_val, y_pred)
    plot_confusion_matrix(cm, ['0','1'], normalize=True)
    plot_confusion_matrix(cm, ['0','1'], normalize=False)

    #Plot Feature Importance
    feat_imp = pd.DataFrame(alg.feature_importances_, columns=[u'Importance'])
    columns.remove(u'AH5_panier')
    feat_imp[u'names'] = columns
    feat_imp.set_index(u'names', inplace=True)
    feat_imp.sort_values(u'Importance', ascending=False, inplace=True)
    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')


def hockey_model_dashboard(cm, y_val, y_pred, model, list_option):

    if list_option[0] == 1:
        xgb.plot_importance(model)
    if list_option[1] == 1:
        plot_confusion_matrix(cm, ['0','1'], normalize=True)
    if list_option[2] == 1:
        plot_confusion_matrix(cm, ['0','1'], normalize=False)
    
    print('Perc : ' + str(round(cm[1][1]/float((cm[1][1]+cm[0][1]))*100,2)) + '%')
    print('Ratio : ' + str(round(cm[1][1]*0.5 - cm[0][1],2)))
    print('Number bet : ' + str(cm[1][1]+cm[0][1]))
    print('Win bet : ' + str(cm[1][1]))
    print('Loss bet : ' + str(cm[0][1]))
    print f1_score(y_val, y_pred)


def hockey_season_preparation(season):
    list_file_          = glob('../dataset/local/___*')
    list_file           = glob('../dataset/local/df_scores_bet_*')
    list_file_scores    = glob('../dataset/local/df_NHL_*')    
    for filename in list_file_:
        os.system('mv "' + filename + '" "' + filename.replace('___','') + '"')

    
    list_file_          = glob('../dataset/local/___*')
    list_file           = glob('../dataset/local/df_scores_bet_*')
    list_file_scores    = glob('../dataset/local/df_NHL_*')
    for i, filename in enumerate(list_file):
        if filename.find(season) != -1:
            filename_new = filename.replace('df_scores','___df_scores')
            os.system('mv "' + filename + '" "' + filename_new + '"')

    for i, filename in enumerate(list_file_scores):
        if filename.find(season) != -1:
            filename_new = filename.replace('df_NHL_','___df_NHL_')
            os.system('mv "' + filename + '" "' + filename_new + '"')