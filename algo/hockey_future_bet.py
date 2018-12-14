#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 16:28:52 2018

@author: mathieu
"""

# =============================================================================
# 
# =============================================================================
import os

# =============================================================================
# Recover SCORES of previous matchs plays this season
# =============================================================================
os.system('python hockey_scrap_scores_NHL_espn.py')
print 'DONE - Recover SCORES of previous matchs plays this season'

# =============================================================================
# Recover BETS of previous matchs plays this season
# =============================================================================
os.system('python hockey_scrap_NHL_oddsportal_current.py')
print 'DONE - Recover BETS of previous matchs plays this season'

# =============================================================================
# Merge SCORES and BETS of previous matchs plays this season
# =============================================================================
os.system('python hockey_analysis.py')
print 'DONE - Merge SCORES and BETS of previous matchs plays this season'

# =============================================================================
# Test if BET TODAY
# =============================================================================
print 'START - Test if BET TODAY'
import hockey_result_viewer
