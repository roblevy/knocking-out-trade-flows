# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:03:59 2013

@author: Rob
"""

import sys, config
import pandas as pd
import numpy as np
sys.path.insert(0, config.demo_model_dir)
import global_demo_model
reload (global_demo_model)
#%%
# Get the data
data = pd.read_csv('ggodelta.csv')
file = '../../gdm.test'
model = global_demo_model.GlobalDemoModel.from_pickle(file)

#%%
# Prepare the ggodelta data
d = data.set_index(['sector','from_iso3','to_iso3']).squeeze()
#%%
# Prepare the model data
flows = {}
for s in model.sectors:
    sector_flows = model.trade_flows(s)
    sector_flows.columns.name = 'to_iso3'
    flows[s] = sector_flows.stack()
flows = pd.DataFrame(flows)
flows.columns.name = 'sector'
flows = flows.stack()
flows = flows.reorder_levels([2, 0, 1])
flows = flows.sort_index()

#%%
# Calculate the Gross Output delta as a proportion of the original
# flows size. (Proportional Delta Gross Output, pdgo)
pdgo = (d / flows).dropna()

#%%
# Plot
from matplotlib.artist import setp
import matplotlib.pyplot as plt

to_plot = pdgo.unstack('sector')

fig = plt.figure()
plot = to_plot.boxplot(rot=90, sym='o')
setp(plot['fliers'], color='b')
setp(plot['fliers'], linewidth=0)
setp(plot['fliers'], alpha=0.2)
fig.suptitle('Change in Global Gross Output as fraction of flow size')
plt.xlabel('Sector')
plt.ylabel('$\Delta$Gross Output / flow size')

#%%
fig = plt.figure()
to_plot = d.unstack('sector')
plot = to_plot[np.abs(to_plot) > 100].boxplot(rot=90, sym='o')
setp(plot['fliers'], color='r')
setp(plot['fliers'], linewidth=0)
setp(plot['fliers'], alpha=0.2)
fig.suptitle('Change in Global Gross Output')
plt.xlabel('Sector')
plt.ylabel('$\Delta$Gross Output')