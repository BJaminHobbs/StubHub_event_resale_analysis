# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 18:07:23 2018

@author: Ben
"""

#Remove duplicate indices, keeping one original
def Remove_Dup_Ind(df_in):
    import pandas as pd
    
    max_dups = df_in.index.value_counts().max()    
    
    df_out = pd.DataFrame(columns = df_in.columns)
    for i in range(1, max_dups+1):
        _ = df_in.loc[df_in.index.value_counts()==i]
        _ = _.sort_index()[::i]
        df_out = pd.concat([df_out, _])
        
    df_out = df_out.sort_index()
    return df_out