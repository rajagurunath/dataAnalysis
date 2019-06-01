import pandas as pd 
import numpy as np
import glob
import sys
import os


#configs
DATA_DIR=r"D:\experiments\data\\"
PM_DIR=os.path.join(DATA_DIR,"pm")
NETCOOL_DIR=os.path.join(DATA_DIR,"Netcool")
PM_NETCOOL_DIR=os.path.join(DATA_DIR,"pm_netcool")
# pm_nodes_path=glob.glob(PM_DIR+"*.csv")
# netcool_nodes_path=glob.glob(NETCOOL_DIR+"*.csv")
nodenames=['ASBNVACYO3Y.csv', 'ATLNGAMAO4Y.csv', 'CHCGILDTO6Y.csv',
        'CHCGILWUO7Y.csv', 'MIAUFLWSO0Y.csv', 'MIAUFLWSO3P-NE70191.csv',
        'NYCMNYZRO1Y.csv', 'WASHDC12O1Y.csv']

# File reading
for node in nodenames:
    print(node)
    nodeDF=pd.read_csv(os.path.join(PM_DIR,node))
    netcoolDF=pd.read_csv(os.path.join(NETCOOL_DIR,node))


    # column extraction
    netcoolDF['device']=netcoolDF['ALERTKEY'].apply(lambda x:x.split(':')[1])
    netcoolDF['SHORT_SUMMARY']=netcoolDF['SUMMARY'].apply(lambda x:x.split('(')[0])


    FIRSTOCCURRENCE_datetime=pd.to_datetime(netcoolDF['FIRSTOCCURRENCE']).dt.round('15Min')
    ts_datetime=pd.to_datetime(nodeDF['ts'])
    FIRSTOCCURRENCE_datetime.name='firstoccurence_datetime'
    ts_datetime.name='ts_datetime'
    netcoolDF['firstoccurence_datetime']=FIRSTOCCURRENCE_datetime
    nodeDF['ts_datetime']=ts_datetime

    #merging
    nodeDF['device']=nodeDF['device'].str.strip()
    netcoolDF['device']=netcoolDF['device'].str.strip()
    pm_netcool=pd.merge(nodeDF,netcoolDF[['device','firstoccurence_datetime','SHORT_SUMMARY','ORIGINALSEVERITY']],
            left_on=['device','ts_datetime'],right_on=['device','firstoccurence_datetime'],how='left')

    print(pm_netcool['SHORT_SUMMARY'].shape[0]-pm_netcool['SHORT_SUMMARY'].isnull().sum())
    print(netcoolDF[['firstoccurence_datetime','device']].drop_duplicates().shape)
    pm_netcool=pm_netcool.sort_values(by='ts')
    pm_netcool['SHORT_SUMMARY'].fillna('Normal_point',inplace=True)
    pm_netcool.to_csv(os.path.join(PM_NETCOOL_DIR,node))






