# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 18:20:48 2018

@author: Ben
"""

def SH_EventParse(ds_event):
    import numpy as np
    all_Ls = ds_event['listing']
    
    all_track = []
    track_params = ['listingId', #SH given
                    'currentPrice', #SH given
                    'listingPrice', #SH given
                    'zoneId', #SH given
                    'zoneName', #SH given
                    'sectionId', #SH given
                    'sectionName', #SH given
                    'section_num', #Pulled from sectionName
                    'isGA', #SH given
                    'row', #SH given
                    'row_num', #Numeric position of alphabetic character
                    'rowId', #concat(section_num, row)
                    'seats', #bool for whether seat numbers are provided
                    'seats_ls', #[seat numbers]
                    'quantity', #SH given
                    'deliveryTypeList', #SH given
                    'deliveryMethodList'] #SH given
    
    for i_Ls in all_Ls:
        #Criteria to remove unwanted ticket listings
        if i_Ls['dirtyTicketInd'] == True: continue
        if i_Ls['listingPrice']['amount'] >= 500: continue
        if i_Ls['currentPrice']['amount'] >= 500: continue
        if 'SUITE' in i_Ls['sectionName'].upper(): continue
        if 'STANDING' in i_Ls['sectionName'].upper(): continue
        if i_Ls['isGA'] == 1: continue
        
        track_Ls = {}
        for j in track_params:
            
            if j == 'currentPrice' or j == 'listingPrice':
                track_Ls[j] = i_Ls[j]['amount']
            elif j == 'section_num':
                _ = i_Ls['sectionName']
                try: track_Ls[j] = int(_[-3:])
                except: track_Ls[j] = 999
            elif j == 'row_num':
                alpha = i_Ls['row']
                alpha = alpha.upper()
                #Convert alpha row name to numeric
                num_row = [ord(s)-64 for s in alpha]
                ##For cycling rows from A-Z, AA, AB, AC - ZZ:
                #num_row = num_row[::-1]
                #num_row = sum([s*26**n for n, s in enumerate(num_row)])
                ##For cycling rows from A-Z, AA, BB, CC - ZZ
                num_row = (len(num_row)-1)*26 + num_row[-1]
                track_Ls[j] = num_row
            elif j == 'rowId':
                track_Ls[j] = str(track_Ls['section_num']) + track_Ls['row']
            elif j == 'seats':
                #If 'seatNumbers' exists and has all digits then: True
                if np.in1d('seatNumbers',list(i_Ls.keys())):
                    seatstr = ''.join(i_Ls['seatNumbers'].split(','))
                    if np.str.isdigit(seatstr):
                        track_Ls[j] = True
                    else: 
                        track_Ls[j] = False
                else:
                    track_Ls[j] = False
            elif j == 'seats_ls':
                if track_Ls['seats']:
                    seatls = i_Ls['seatNumbers'].split(',')
                    track_Ls[j] = [int(_) for _ in seatls]
                else: track_Ls[j] = [np.nan]           
            elif j == 'deliveryMethodList':
                try:
                    track_Ls[j] = i_Ls[j]
                except KeyError:
                    track_Ls[j] = np.nan
            else:
                track_Ls[j] = i_Ls[j]
                        
            if i_Ls['isGA'] == 1:
                print('Warning: General Admission in {}'.format(i_Ls['sectionName']))
            
        all_track.append(track_Ls)
    
    return all_track


def LS_Stats(Ls_df):
    import pandas as pd
    import numpy as np
    import scipy.stats as st
    from Routines import Remove_Dup_Ind
    
    df = pd.DataFrame(Ls_df)
    df.set_index('listingId', inplace=True)
    df = Remove_Dup_Ind(df)
    
    #RowId stats at sale
    df['rowId_sum'] = df.groupby('rowId')['quantity'].transform(np.sum)
    
    #Section stats at sale
    df['sec_sum'] = df.groupby('section_num')['quantity'].transform(np.sum)
    df['sec_mean'] = df.groupby('section_num')['currentPrice'].transform(np.mean)
    df['sec_med'] = df.groupby('section_num')['currentPrice'].transform(np.median)
    df['sec_std'] = df.groupby('section_num')['currentPrice'].transform(np.std)
    df['sec_iqr'] = df.groupby('section_num')['currentPrice'].transform(st.iqr)
    df['sec_25th'] = df['sec_mean'] - df['sec_iqr']/2
    df['sec_75th'] = df['sec_mean'] + df['sec_iqr']/2
    
    wmean_map = (df.groupby('section_num').
                apply(lambda x: np.average(x['currentPrice'], weights= x['quantity'])).to_dict())
    df['sec_wmean'] = df['section_num'].map(wmean_map)
    
    
    #Zone stats at sale
    df['zone_sum'] = df.groupby('zoneId')['quantity'].transform(np.sum)
    df['zone_mean'] = df.groupby('zoneId')['currentPrice'].transform(np.mean)
    df['zone_med'] = df.groupby('zoneId')['currentPrice'].transform(np.median)
    df['zone_std'] = df.groupby('zoneId')['currentPrice'].transform(np.std)
    df['zone_iqr'] = df.groupby('zoneId')['currentPrice'].transform(st.iqr)
    df['zone_25th'] = df['zone_mean'] - df['zone_iqr']/2
    df['zone_75th'] = df['zone_mean'] + df['zone_iqr']/2
    
    
    wmean_map = (df.groupby('zoneId').
                apply(lambda x: np.average(x['currentPrice'], weights= x['quantity'])).to_dict())
    df['zone_wmean'] = df['zoneId'].map(wmean_map)
    
    return df

def LS_Days(new_df, old_df=None):
    import pandas as pd
    
    if old_df is None: new_df['ts_ls'] = pd.datetime.today()
    else:
        cons_Ls = new_df[new_df.index.isin(old_df.index)].index
        new_df.loc[cons_Ls, 'ts_ls'] = old_df.loc[cons_Ls, 'ts_ls']

        not_Ls = new_df[~new_df.index.isin(old_df.index)].index
        new_df.loc[not_Ls, 'ts_ls'] = pd.datetime.today()
    
    return new_df