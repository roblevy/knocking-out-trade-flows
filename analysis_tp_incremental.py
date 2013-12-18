# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 16:27:22 2013

Analysis of the change in GGO in response to
*incremental* adjustments to import propensities.

@author: Rob
"""

import sys, config
import pandas as pd

sys.path.insert(0, config.demo_model_dir)
import global_demo_model
reload (global_demo_model)

#%%
# Get the data
raw = pd.read_csv('dggo ip incremental.csv')
raw = raw[(raw.from_iso3 != 'RoW') & (raw.to_iso3 != 'RoW')]

