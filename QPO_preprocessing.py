import numpy as np
import pandas as pd
import gc
import time
import re
import random
from scipy import stats

class pp_model:
    def __init__(self, filename):
        raw_df = pd.read_csv(filename, encoding='utf-8') #read data file to pandas
        
        raw_df = raw_df[raw_df.lang=='en'] #remove english tweet
        self.df = raw_df[['id','created_at','user','text']]
        self.df.insert(0, 'target', 2)
        self.df.insert(3, 'flag', 'NO_QUERY')
        self.df.columns=['target','ids','date','flag','user','text'] #all features
        
        del raw_df
        gc.collect()
        
    def processing(self):
        t_df=self.df.reset_index(drop=True)

        for index in range(t_df.index.size):
            user = t_df.loc[index,'user']
            userid = int(user.split(',')[0].split(':')[1]) #extract user id 
            t_df.loc[index,'user'] = userid
            userdate = t_df.loc[index,'date'].split()
            t_df.loc[index,'date'] = userdate[0]+' '+userdate[1]+' '+userdate[2]+' '+userdate[3]
            day = userdate[1]+userdate[2] #keep useful time information
            usertext = t_df.loc[index,'text']
            usertext = re.sub('[^0-9A-Za-z]', ' ', usertext) #remove punctuation
            t_df.loc[index,'text'] = usertext

        return t_df
    
    def userBasedSample(self, t_df, filterWay = 1):
        # filterWay: 1 use mean as filter number
        #            2 use mode
        #            3 use median
    
        userdict=dict()
        for index in t_df.index:
            user = t_df.loc[index,'user']
            user = str(user)
            if (userdict.__contains__(user)): #group by
                userdict[user].append(index)
            else:
                userdict[user] = [index]

        numByUser = [len(listByUser) for listByUser in userdict.values()] #count the number
        
        if(filterWay == 1):
            sampleNum = int(round(np.mean(numByUser)))
        elif(filterWay == 2):
            sampleNum = int(stats.mode(numByUser)[0][0])
        elif(filterWay == 3):
            sampleNum = int(np.median(numByUser))

        reList = []
        for listByUser in userdict.values():
            if(len(listByUser) > sampleNum):
                reList.extend(random.sample(listByUser, sampleNum)) # take the sampling
            else:
                reList.extend(listByUser)

        reList=sorted(reList)

        t_df=t_df.loc[reList]
        t_df=t_df.reset_index(drop=True)
        gc.collect()
        
        return t_df

    def dateBasedSample(self, t_df):
        datedict = dict()
        for index in t_df.index:
            time = t_df.loc[index,'date']
            date = time.split()[1]+time.split()[2]
            if (datedict.__contains__(date)):#group by
                datedict[date].append(index)
            else:
                datedict[date] = [index]

        numByDate = [len(listByDate) for listByDate in datedict.values()]#count the number
        sampleNum = min(numByDate)
        reList = []
        for listByDate in datedict.values():
            reList.extend(random.sample(listByDate, sampleNum))# take the sampling

        reList=sorted(reList)

        t_df=t_df.loc[reList]
        t_df=t_df.reset_index(drop=True)
        gc.collect()
        
        return t_df

    def full_processing(self):
        t_df=self.df.reset_index(drop=True)

        for index in range(t_df.index.size):
            user = t_df.loc[index,'user']
            userid = int(user.split(',')[0].split(':')[1])
            t_df.loc[index,'user'] = userid
            userdate = t_df.loc[index,'date'].split()
            t_df.loc[index,'date'] = userdate[0]+' '+userdate[1]+' '+userdate[2]+' '+userdate[3]
            day = userdate[1]+userdate[2]
            usertext = t_df.loc[index,'text']
            usertext = re.sub('[^0-9A-Za-z]', ' ', usertext)
            t_df.loc[index,'text'] = usertext
        
        t_df = self.userBasedSample(t_df, filterWay = 1)
        t_df = self.dateBasedSample(t_df)
    
        return t_df