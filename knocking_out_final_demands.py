# -*- coding: utf-8 -*-
"""
Created on Wed Dec 04 16:23:12 2013

@author: Rob

Knocking out is no longer a sensible description for what this does.
FD is now reduced by a single dollar and changes in the various
flows are recorded.
"""
import sys, config
import pandas as pd
sys.path.insert(0, config.demo_model_dir)
import global_demo_model
reload (config)
reload(global_demo_model)

#%%
# Get data
file = 'model.gdm'
model = global_demo_model.GlobalDemoModel.from_pickle(file)

#%%
# Initialise
# GGO is Gross Global Output
tolerance = 10e-5
init_ggo = model.gross_output().sum()
flow_deltas = pd.DataFrame(columns=['source_country', 'source_sector',
                                 'from_iso3', 'to_iso3', 'delta', 'type'])
model.set_tolerance(tolerance)
  
for country_name in model.countries.iterkeys():
    for sector in model.sectors:
        fd = model.countries[country_name].f[sector]
        model.set_final_demand(country_name, sector, fd - 1, 
                               calculate_deltas=True, tolerance=tolerance)
        deltas = model.deltas
        if len(deltas) > 0:
            deltas['source_country'] = country_name
            deltas['source_sector'] = sector
            flow_deltas = deltas.append(flow_deltas, ignore_index=True)
        print "%s: %s" % (country_name, sector)
        model = global_demo_model.GlobalDemoModel.from_pickle(file)
    flow_deltas.to_csv('flow_deltas_fd.csv',index=False)
