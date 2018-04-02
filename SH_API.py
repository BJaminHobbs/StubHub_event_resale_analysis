# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 16:31:08 2018

@author: Ben
"""

def API_Login(Prod_Key, Prod_Secret, login_params):
    import requests
        
    basic_auth = requests.auth.HTTPBasicAuth(Prod_Key, Prod_Secret)
        
    body = ''
    for k,v in login_params.items():
        body = body + k + '=' + v + '&'
    body = body[:-1]
    
    login_url = 'https://api.stubhub.com/login'
    
    login = requests.post(login_url, auth=basic_auth, data=body)
    return login
    

def Inv_Get(login, eventID):
    import requests
    
    acc_token = login.json()['access_token']
    acc_type = login.json()['token_type']
    ref_token = login.json()['refresh_token']
    
    token_auth = acc_type + ' ' + acc_token
    headers = {'Authorization': token_auth}
    
    #Call to get totalListings for event. Number of SH listings can only be 
    #called with maximum qty 250. Ideally a while statement could be used instead.
    rows = 1
    qty = '>2'
    
    get_url = 'https://api.stubhub.com/search/inventory/v2?eventid={}' \
    '&sectionstats=true&start=0&rows={}&pricingsummary=true&quantity={}' \
    '&zonestats=true'.format(eventID,rows,qty)
    resp = requests.get(get_url, headers=headers)
    
    if resp.status_code == 200:
        try:
            total_Ls = resp.json()['totalListings']
        except KeyError:
            print('KeyError detected')
            print('Status Code {}'.format(resp.status_code))
            print('Response Keys: \n{}'.format(resp.json().keys()))
            return None
        if total_Ls == 0: return None
    else:
        print('EventId:{}'.format(eventID))
        print('Status Code {}'.format(resp.status_code))
        print(resp.text)
        return None
        
    start = 0
    max_rows = 250
    all_Ls = []

    for i in range(0, total_Ls // max_rows + 1):
        rows = (i+1)*max_rows
        
        get_url = 'https://api.stubhub.com/search/inventory/v2?eventid={}' \
        '&sectionstats=true&start={}&rows={}&pricingsummary=true&quantity={}' \
        '&zonestats=true'.format(eventID,start,rows,qty)
        resp = requests.get(get_url, headers=headers)
        
        if resp.status_code == 200:
            try:
                all_Ls.extend(resp.json()['listing'])
            except KeyError:
                print('KeyError detected')
                print('Status Code {}'.format(resp.status_code))
                print('Response Keys: \n{}'.format(resp.json().keys()))
                return None
        else:
            print('EventId:{}'.format(eventID))
            print('Status Code {}'.format(resp.status_code))
            print(resp.text)
            return None

        start = (i+1)*max_rows
        
    ds_event = resp.json()
    ds_event['listing'] = all_Ls
    
    return ds_event
