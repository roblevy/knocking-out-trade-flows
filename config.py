# -*- coding: utf-8 -*-
"""
Created on Tue Dec 03 12:59:16 2013

@author: Rob
"""

import ConfigParser

_linux_mode = False

config = ConfigParser.SafeConfigParser()
config.read('config.cfg')

config_linux = ConfigParser.SafeConfigParser()
config_linux.read('config_linux.cfg')

def set_cfg(cfg):
    global datadir, csv_file, demo_model_dir, gdm_datadir
    datadir = cfg.get('data','data_basedir')
    csv_file = cfg.get('data','csv_file')
    demo_model_dir = cfg.get('demomodel','demo_model_dir')
    gdm_datadir = cfg.get('data','gdm_datadir')


def set_linux_mode():
    set_cfg(config_linux)
    
set_cfg(config)