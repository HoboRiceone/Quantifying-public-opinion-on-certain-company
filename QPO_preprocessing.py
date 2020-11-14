import numpy as np
import pandas as pd
import gc
import time

def processing(filename):
    raw_df = pd.read_csv(filename)
    raw_df = raw_df[raw_df.lang=='en']
    df = raw_df[['id','created_at','user','text']]
    
    del raw_df
    gc.collect()
    
    df.insert(0, 'target', 0)
    df.insert(3, 'flag', 'NO_QUERY')
    
    df.columns=['target','ids','date','flag','user','text']
    
    df=df.reset_index(drop=True)
    gc.collect()
    
    for index in range(df.index.size):
        user = df.loc[index,'user']
        userid = int(user.split(',')[0].split(':')[1])
        df.loc[index,'user'] = userid
        userdate = df.loc[index,'date'].split()
        df.loc[index,'date'] = userdate[0]+' '+userdate[1]+' '+userdate[2]+' '+userdate[3]
        day = userdate[1]+userdate[2]
        
    return df