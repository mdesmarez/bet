#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 20:52:24 2018

@author: mathieu
"""


# =============================================================================
# 
# =============================================================================
import subprocess
import time
from datetime                                                                  import datetime

#import PS3838_scrap_parlay
#from PS3838_main import ps3838_main

# =============================================================================
# 
# =============================================================================
debug = 1

while True:
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('**************** BEGIN ****************')
    print str(datetime.now())
    try:
        str_command             = "python PS3838_main.py"
        proc                    = subprocess.Popen(str_command, shell=True, stdout=subprocess.PIPE)  
        if debug == 1:
            out = proc.communicate()
            print out[0]
    except:
        pass
    print('****************   END  ****************')
    print str(datetime.now())
    time.sleep(60*5)
    