# -*- coding: utf-8 -*-
"""
Created on Wed Dec 04 16:23:12 2013

@author: Rob
"""
import sys, config
reload (config)
import pandas as pd
config.set_linux_mode()
sys.path.insert(0, config.demo_model_dir)
import global_demo_model
reload(global_demo_model)

#%%
# Get data
file = '../../gdm.test'
model = global_demo_model.GlobalDemoModel.from_pickle(file)

#%%
# Initialise
# GGO is Gross Global Output
init_ggo = model.gross_output().sum()
dggo = pd.DataFrame(columns=['sector','from_iso3','to_iso3',
                             'flow_value','import_propensity','factor','dggo'])

countries = ['USA', 'GBR', 'CHN']
sectors = ['Agriculture', 'Financial Services', 'Food']
factors = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]  
for sector in sectors:
    P = model._import_propensities[sector]
    for to_iso3 in countries:
        # Get a column from the import propensities matrix
        # (which must sum to 1)
        P_i = P[to_iso3].squeeze().copy()
        for from_iso3 in countries:
            if P_i[from_iso3] > 0:
                for factor in factors:
                    P_i_new = P_i.copy()
                    print "%s: %s to %s (%f)" % (sector, from_iso3,
                                                 to_iso3, factor)
                    p_ij = P_i_new.ix[from_iso3]
                    P_i_new.ix[from_iso3] = p_ij * factor
                    flow_value = model.trade_flows(sector)[to_iso3][from_iso3]
                    P_i_new = P_i_new * (1 / P_i_new.sum())
                    model._import_propensities[sector][to_iso3] = P_i_new
                    model.recalculate_world()
                    new_ggo = model.gross_output().sum()
                    go_delta = {'sector':sector,'from_iso3':from_iso3,
                                'to_iso3':to_iso3,'flow_value':flow_value,
                                'import_propensity':p_ij,
                                'factor':factor,
                                'dggo':new_ggo - init_ggo}
                    dggo = dggo.append(go_delta,ignore_index=True)                           
                    model = global_demo_model.GlobalDemoModel.from_pickle(file)
            else:
                print '%s to %s: trade propensity is already zero' % (from_iso3,
                                                                     to_iso3)
    dggo.to_csv('dggo ip incremental.csv',index=False)
dggo.to_csv('dggo ip incremental.csv',index=False)