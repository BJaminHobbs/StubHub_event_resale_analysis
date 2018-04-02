# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 09:38:36 2018

@author: Ben
"""
import time
import os
import pandas as pd

from Events import Mined_Events
from SH_API import API_Login, Inv_Get
from SH_EventParse import SH_EventParse, LS_Stats, LS_Days
from Event_Pickle import Pickle_Save, Pickle_Load
from Sale import Sale_Detect, Sale_Valid


Prod_Key = 'XXXX' #StubHub Provided Key
Prod_Secret = 'XXXX' #StubHub Provided Token

login_params = {'grant_type' : 'password',
        'username' : 'XXXX', #Enter Username
        'password' : 'XXXX', #Enter Password
        'scope' : 'PRODUCTION'}

login = API_Login(Prod_Key, Prod_Secret, login_params)

eventdata = Mined_Events()

allstop = max([allstop for _, allstop in eventdata.values()])
allstop -= pd.Timedelta(days=1)

run_one = True
while pd.datetime.today() <= allstop:
    for eventId, [eventName, gameover] in eventdata.items():
        if pd.datetime.today() <= gameover - pd.Timedelta(days=1):           
            ds_event = Inv_Get(login, eventId)
            if ds_event == None: continue
            
            Ls_new = SH_EventParse(ds_event)
            new_df = LS_Stats(Ls_new)
            
            if not run_one: 
                old_df = Pickle_Load(eventId, eventName)
                new_df = LS_Days(new_df, old_df)
            else: 
                new_df = LS_Days(new_df, old_df=None)
                old_df = new_df

            Pickle_Save(new_df, eventId, eventName)  
            
            #Compare new ticket listings to old. Identify listings that have left the market or reduced quantity
            sold_df = Sale_Detect(old_df, new_df, gameover)
            if sold_df.shape[0] >= 1:
                print('Sale in {} at {}'
                      .format(eventName, pd.datetime.today()))
            
            if not run_one:
                #Load prior ledger of ticket listings that have left market
                prior_df = Pickle_Load(eventId, eventName + '_ledger')
                prior_strike = Pickle_Load(eventId, eventName + '_strike')
                
                #Strike from ledger any listings that have re-entered the market
                prior_df, striken = Sale_Valid(prior_df, new_df)
                if striken.shape[0] >= 1:
                    print('Ledger strike in {} at {}'
                          .format(eventName, pd.datetime.today()))

                sold_df = pd.concat([prior_df, sold_df])
                striken = pd.concat([prior_strike, striken])
            else: striken = sold_df
            
            #Save all ticket listings that have left the market or reduced quantities into ledger
            Pickle_Save(sold_df, eventId, eventName + '_ledger')
            #Save all ticket listings that were struck from ledger
            Pickle_Save(striken, eventId, eventName + '_strike')
                            
            
    run_one = False
    time.sleep(60*60) #Rest between repeat calls of same event
