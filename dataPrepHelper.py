import pandas as pd 
import numpy as np
import glob
import sys
import os
from tqdm import tqdm

# from statsmodels.tsa.seasonal import seasonal_decompose
# series = ...
# result = seasonal_decompose(series, model='additive')
# print(result.trend)
# print(result.seasonal)
# print(result.resid)
# print(result.observed)


DATA_DIR="D:\experiments\data\Research_data\ochctp"
PM_DIR=os.path.join(DATA_DIR,"ochctp.csv")

data_gen=pd.read_csv(PM_DIR,chunksize=1000000)
first=True
INDEX=['performance_metrics.nodename', 'performance_metrics.module', 
'performance_metrics.ts']
COLUMNS='performance_metrics.measure'
VAL='performance_metrics.val'
csv_name_to_save="pivoted_ochctp"
for df in tqdm(data_gen,desc="pivoting"):
    if first:
        
        # print(df.head())
        #print(df.columns.tolist())
        df1=df.pivot_table(index= INDEX,columns=COLUMNS,values=VAL).reset_index()
        # print(df1.head())
        #print(df1.columns.tolist())
        first=False
        df1.to_csv(os.path.join(DATA_DIR,'{}.csv'.format(csv_name_to_save)),header=True,mode='a')
    else:
        # print(df.head())
        
        df1=df.pivot_table(index= INDEX,columns=COLUMNS,values=VAL).reset_index()
        # print(df1.head())
        df1.to_csv(os.path.join(DATA_DIR,'{}.csv'.format(csv_name_to_save)),header=False,mode='a')
        

['performance_metrics.nodeid', 'performance_metrics.section', 'performance_metrics.module', 
'performance_metrics.ts', 'performance_metrics.valid', 'performance_metrics.measure',
 'performance_metrics.val', 'performance_metrics.nodename']