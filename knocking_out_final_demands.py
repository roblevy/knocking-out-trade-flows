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
ggodelta = pd.DataFrame(columns=['country', 'sector','ggodelta'])
  
for country_name, country in model.countries.iteritems():
    for sector in model.sectors:
        fd = country.f[sector]
        model.set_final_demand(country_name, sector, 0)
        print "%s: %s" % (country_name, sector)
        new_ggo = model.gross_output().sum()
        go_delta = {'country':country_name,
                    'sector':sector,
                    'ggodelta':new_ggo - init_ggo}
        ggodelta = ggodelta.append(go_delta,ignore_index=True)                           
        model = global_demo_model.GlobalDemoModel.from_pickle(file)
    ggodelta.to_csv('ggodelta_fd.csv',index=False)
