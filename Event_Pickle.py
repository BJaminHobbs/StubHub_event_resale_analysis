# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 00:57:26 2018

@author: Ben
"""

def Pickle_Save(all_track, eventId, eventName):
    import os
    import pickle

    dirpath = os.path.dirname(__file__)
    savepath = dirpath + '/events/' + eventId + '_' + eventName + '.pickle'
    
    pickle_out = open(savepath,'wb')
    pickle.dump(all_track, pickle_out)
    pickle_out.close()
    
    
def Pickle_Load(eventId, eventName):
    import os
    import pickle
    
    dirpath = os.path.dirname(__file__)
    loadpath = dirpath + '/events/' + eventId + '_' + eventName + '.pickle'
    
    pickle_in = open(loadpath, 'rb')
    all_track = pickle.load(pickle_in)
    pickle_in.close()
    return all_track