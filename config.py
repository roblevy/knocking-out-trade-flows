# -*- coding: utf-8 -*-
"""
Created on Tue Dec 03 12:59:16 2013

@author: Rob
"""

import ConfigParser

config = ConfigParser.SafeConfigParser()
config.read('config.cfg')

datadir = config.get('data','data_basedir')
csv_file = config.get('data','csv_file')
demo_model_dir = config.get('demomodel','demo_model_dir')
gdm_datadir = config.get('data','gdm_datadir')