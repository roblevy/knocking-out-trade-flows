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
data = data[(data.from_iso3 != 'RoW') & (data.to_iso3 != 'RoW')]
file = '../../gdm.test'
model = global_demo_model.GlobalDemoModel.from_pickle(file)

#%%
# Prepare the ggodelta data. GGO = Global Gross Output
initial_ggo = model.gross_output().sum()
data['new_ggo'] = data['ggodelta'] + initial_ggo
d = data.set_index(['sector','from_iso3','to_iso3'])
dggo = d['ggodelta'].squeeze() # Delta Global Gross Output
new_ggo  = d['new_ggo'].squeeze()

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
pdgo = (dggo / flows).dropna()

#%%
# Plot cumulative distributions
from matplotlib.artist import setp
import matplotlib.pyplot as plt
df_dggo = dggo.reset_index()
df_dggo = df_dggo[(df_dggo.from_iso3 != 'RoW') & (df_dggo.to_iso3 != 'RoW')]
g = df_dggo.groupby('sector')
df_dggo['rank'] = g['ggodelta'].transform(pd.Series.rank)
df_dggo['n'] = g['ggodelta'].transform(len)
df_dggo['p'] = df_dggo['rank'] / df_dggo.n
df_dggo = df_dggo.sort(['sector','p'])
ag = df_dggo[df_dggo.sector == 'Agriculture'].sort('p')
plt.plot(ag.ggodelta, ag.p)
#%%
# Plot
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
# Now plot the deltas themselves. They need to be logged, since they're
# mostly bunched around zero, but there are some negative numbers. Thus
# plot positive deltas and negative deltas in different colours.
plt.figure()
positive = np.log(dggo[dggo > 0].unstack('sector'))
negative = np.log(np.abs(dggo[dggo < 0].unstack('sector')))
## TODO: Implement strip charts and plot ontop of each other
p_pos = positive.boxplot(rot=90, sym='o')
p_neg = negative.boxplot(rot=90, sym='o')
setp(p_pos['fliers'], color='r')
setp(p_neg['fliers'], color='b')
setp(p_pos['fliers'], linewidth=0)
setp(p_pos['fliers'], alpha=0.2)
plt.suptitle('Log new Global Gross Output '
             'relative initial Global Gross Output')
plt.xlabel('Sector')
plt.ylabel('log(New Gross Output / Original Gross Output)')
plt.show()

#%%
# Plot delta GGO kernel density estimations
from scipy.stats.kde import gaussian_kde
from numpy import linspace
plt.figure()
x = linspace(-500000000,500000000,100)
pdf_all_sectors = gaussian_kde(dggo)
normal = np.random.normal(scale=dggo.std(), size=len(dggo))
pdf_normal = gaussian_kde(normal)
plt.plot(x, pdf_all_sectors(x), 'r')
plt.plot(x, pdf_normal(x), 'b')
plt.title('$\Delta GGO$ kernel density estimation (red) with a normal distribution (blue)')
plt.show()
#%%
# Plot proportional delta GGO kernel density estimations
from scipy.stats.kde import gaussian_kde
from numpy import linspace
import matplotlib.pyplot as plt
plt.figure()
x = linspace(-2,2,100)
pdf_all_sectors = gaussian_kde(pdgo)
normal = np.random.normal(scale=pdgo.std(), size=len(pdgo))
pdf_normal = gaussian_kde(normal)
plt.rc('text', usetex=True)
#plt.rc('text.latex', preamble = \
#    '\usepackage{amsmath},' \
#    '\usepackage{xfrac}')
plt.plot(x, pdf_all_sectors(x), 'r')
plt.plot(x, pdf_normal(x), 'b')
plt.title('Kernel Density Estimation of Proportional Change in Global Gross Output')
plt.xlabel(r'$\frac{\Delta GGO}{flow value}$')
#%%
# Kernel density estimations per sector
#sectors = pdgo.index.levels[0].values
sectors = ['Agriculture', 'Manufacturing', 'Business Services', 'Financial Services']
for s in sectors:
    samp = pdgo.ix[s].values
    try:
        fail = False
        pdf = gaussian_kde(samp)
    except:
        fail = True
    if not fail:            
        plt.plot(x,pdf(x)) # distribution function
plt.show()