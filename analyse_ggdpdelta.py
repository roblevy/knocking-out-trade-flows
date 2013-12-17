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
# Prepare the dggo data. GGO = Global Gross Output
# LOOK: Only flows > $1000 are included!
initial_ggo = model.gross_output().sum()
data['new_ggo'] = data['dggo'] + initial_ggo
d = data.set_index(['sector','from_iso3','to_iso3'])
d['flow_value'] = flows
d = d[d.flow_value > 1000]
d['pdggo'] = d.dggo / d.flow_value
dggo = d['dggo'].copy().squeeze() # Delta Global Gross Output
new_ggo  = d['new_ggo'].squeeze()

#%%
# Calculate the Gross Output delta as a proportion of the original
# flows size. (Proportional Delta Global Gross Output, pdggo)
pdggo = d.pdggo.dropna()

#%%
# Top ten
print "Top 10 pdggo (positive):"
pdggo.sort()
print pd.DataFrame(pdggo).head(10).reset_index().to_latex(index=False)

print "Top 10 pdggo (negative)"
pdggo.sort(ascending=False)
print pd.DataFrame(pdggo).head(10).reset_index().to_latex(index=False)

print "Top 10 dggo (positive)"
dggo.sort()
print pd.DataFrame(dggo).head(10).reset_index().to_latex(index=False)

print "Top 10 pdggo (negative)"
dggo.sort(ascending=False)
print pd.DataFrame(dggo).head(10).reset_index().to_latex(index=False)

#%%
# Plot log cumulative distributions
# Seperate positive and negative values
from matplotlib.artist import setp
import matplotlib.pyplot as plt
from numpy import linspace
d['pos'] = d.dggo > 0
d['ldggo'] = np.log10(d[d.pos]['dggo'])
d['ldggo'][~d.pos] = np.log10(-d[~d.pos]['dggo'])
g = d.groupby('pos')
d['rank'] = g['ldggo'].transform(pd.Series.rank)
d['n'] = g['ldggo'].transform(len)
d['p'] = d['rank'] / d.n

plt.figure()
pos = d[d.pos].sort(['dggo'])
plt.suptitle('positive dggo log cum dist')
for s in pos.index.levels[0].values:
    plt.plot(pos.ix[s].ldggo, pos.ix[s]['p'])
plt.plot(pos.ldggo, pos.ix[s]['p'], 'r')

plt.figure()
neg = d[~d.pos].sort(['ldggo'])
plt.suptitle('negative dggo log cum dist')
for s in neg.index.levels[0].values:
    plt.plot(neg.ix[s].ldggo, neg.ix[s]['p'])
plt.plot(neg.ldggo, neg.p, 'g')

plt.figure()
plt.scatter(d.ldggo, np.log10(d.flow_value))

#%%
# Plot
to_plot = pdggo.unstack('sector')

plt.figure()
plot = to_plot.boxplot(rot=90, sym='o')
setp(plot['fliers'], color='b')
setp(plot['fliers'], linewidth=0)
setp(plot['fliers'], alpha=0.2)
plt.suptitle('Change in Global Gross Output as fraction of flow size')
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
pdf_all_sectors = gaussian_kde(pdggo)
normal = np.random.normal(scale=pdggo.std(), size=len(pdggo))
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
#sectors = pdggo.index.levels[0].values
sectors = ['Agriculture', 'Manufacturing', 'Business Services', 'Financial Services']
for s in sectors:
    samp = pdggo.ix[s].values
    try:
        fail = False
        pdf = gaussian_kde(samp)
    except:
        fail = True
    if not fail:            
        plt.plot(x,pdf(x)) # distribution function
plt.show()