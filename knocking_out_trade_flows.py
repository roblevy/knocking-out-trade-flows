# -*- coding: utf-8 -*-
"""
Created on Wed Dec 04 16:23:12 2013

@author: Rob
"""
import sys, config
import pandas as pd
sys.path.insert(0, config.demo_model_dir)
import global_demo_model
reload (config)
reload(global_demo_model)

#%%
# Get data
file = '../../gdm.test'
model = global_demo_model.GlobalDemoModel.from_pickle(file)

#%%
# Initialise
# GGO is Gross Global Output
init_ggo = model.gross_output().sum()
ggodelta = pd.DataFrame(columns=['sector','from_iso3','to_iso3','ggodelta'])
  
for sector in model.sectors:
    P = model._import_propensities[sector]
    for to_iso3 in model.countries:
        # Get a column from the import propensities matrix
        # (which must sum to 1)
        P_i = P[to_iso3].squeeze().copy()
        for from_iso3 in model.countries:        
            print "%s: %s to %s" % (sector, from_iso3, to_iso3)
            P_i_new = P_i.copy()
            P_i_new.ix[from_iso3] = 0
            if P_i_new.sum() > 0:
                P_i_new = P_i_new * (1 / P_i_new.sum())
                model._import_propensities[sector][to_iso3] = P_i_new
                model.recalculate_world()
                new_ggo = model.gross_output().sum()
                go_delta = {'sector':sector,
                             'from_iso3':from_iso3,
                             'to_iso3':to_iso3,
                             'ggodelta':new_ggo - init_ggo}
                ggodelta = ggodelta.append(go_delta,ignore_index=True)                           
                model = global_demo_model.GlobalDemoModel.from_pickle(file)
            else:
                print 'trade propensities are all zero'
    ggodelta.to_csv('ggodelta.csv',index=False)
ggodelta.to_csv('ggodelta.csv',index=False)