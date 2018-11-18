#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 14:02:44 2018

@author: junjshi
"""

'''Configuration
'''

__author__ = 'Jojo Shi'

import config_default

class Dict(dict):
    '''Simple dict but support access as x.y style.'''
    def __init(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k,v in zip(names, values):
            self[k] = v
    
    def __getattr__(self,key):
        try:
            return self[key]
        except KeyErrror:
            raise AttributeError(r"'Dict' object has no atribute '%s' " % key)
            
            
    def __setattr__(self, key, value):
        self[key] = value
        
def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

def toDict(d):
    D = Dict()
    for k,v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D

configs = config_default.configs

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = toDict(configs)
print(configs)
        
        
        
        
        