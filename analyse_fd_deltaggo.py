# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 16:10:04 2013

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
data = pd.read_csv('ggodelta_fd.csv')
data = data[(data.country_iso3 != 'RoW')]
file = '../../gdm.test'
model = global_demo_model.GlobalDemoModel.from_pickle(file)
data = data.set_index(['country_iso3','sector'])
#%%
# Prepare the data
data['fd'] = model.final_demand()
data['pdggo'] = (data.ggodelta / data.fd).fillna(0)
#%%
# Plot proportional delta GGO kernel density estimations
pdggo = data.pdggo
from scipy.stats.kde import gaussian_kde
from numpy import linspace
import matplotlib.pyplot as plt
plt.figure()
x = linspace(-5,1,1000)
pdf_all_sectors = gaussian_kde(pdggo)
normal = np.random.normal(loc=pdggo.mean(), scale=pdggo.std(), size=len(pdggo)*10)
pdf_normal = gaussian_kde(normal)
plt.plot(x, pdf_all_sectors(x), 'r')
plt.plot(x, pdf_normal(x), 'b')
plt.suptitle('Relative $\Delta GGO$ in response to changes in final demand\n'
             'kernel density estimation (red) with a normal distribution (blue)')
plt.xlabel(r'$\frac{\Delta GGO}{flow size}$')
plt.show()

#%%
# Top 10
pdggo.sort()
print pdggo.reset_index().head(10).to_latex(index=False)