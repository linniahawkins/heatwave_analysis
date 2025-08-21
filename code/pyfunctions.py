import sys
import os, glob
import csv 
import calendar
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta
import pandas as pd


def load_daily_data(site,sw_thresh):
    in_dir='../data/' 
    
    if (site=='CA-Ca3'):
        # CA-Ca3 
        filename = os.path.join(in_dir+'CA-Ca3.csv')
        df = pd.read_csv(filename,header=0,index_col=0, parse_dates=True, squeeze=True)
        df.loc['2018', :] = np.NaN
        df_daily = df[df['SW_IN']>sw_thresh].resample('D').mean()
        
    elif (site=='US-Me6'):
        filename = os.path.join(in_dir+'US-Me6.csv')
        df = pd.read_csv(filename,header=0,index_col=0, parse_dates=True, squeeze=True)
        df.loc['2018', :] = np.NaN
        df_daily = df[df['SW_IN']>sw_thresh].resample('D').mean()
        
    elif (site=='WREF'):
        filename=os.path.join(in_dir+'NEON-WREF.csv')
        df = pd.read_csv(filename,index_col=0,parse_dates=True,header=0)
        df_daily = df[df['SW_IN']>sw_thresh].resample('D').mean()
        
    elif (site=='ABBY'):
        filename=os.path.join(in_dir+'NEON-ABBY.csv')
        df = pd.read_csv(filename,index_col=0,parse_dates=True,header=0)
        df_daily = df[df['SW_IN']>sw_thresh].resample('D').mean()

    else:
        print("site must be one of: CA-Ca3, US-Me6, WREF, ABBY")

    return df_daily




def get_daily_clim(df,var):
    
    #tmp = df[df.index.year != 2021]
    tmp = df
    df_mean = tmp.groupby(tmp.index.dayofyear).mean()
    df_min = tmp.groupby(tmp.index.dayofyear).min()
    df_max = tmp.groupby(tmp.index.dayofyear).max()
    
    # drop leap day
    out_min = np.delete(df_min[var].values.flatten(),60)
    out_mean = np.delete(df_mean[var].values.flatten(),60)
    out_max = np.delete(df_max[var].values.flatten(),60)
    
    x = pd.date_range(datetime(2021,1,1),datetime(2021,12,31),freq='D')
    df_out = pd.DataFrame({'day_min':out_min,'day_mean':out_mean,'day_max':out_max},index = x)
    
    return df_out 




def get_cumulative(site, data, var):
    
    nee_scaler = (1/1e6)*86400*12 # umol/m2/s to gC/m2/day
    lh_scaler = (1/(2.45e6)) * 86400 # W/m2 to mm/day

    if (site == 'CA-Ca3'):
        if var=='NEE':
            da = data[var][pd.datetime(2002,1,1):pd.datetime(2022,12,31)]*nee_scaler
            out = da.groupby(da.index.year).cumsum()
        elif var=='LH':
            da = data[var][pd.datetime(2002,1,1):pd.datetime(2022,12,31)]*lh_scaler
            out = da.groupby(da.index.year).cumsum()
        else:
            da = data[var][pd.datetime(2002,1,1):pd.datetime(2022,12,31)]
            out = da.groupby(da.index.year).cumsum()
        
    elif (site == 'NEON-WREF'):
        if var=='NEE':
            da = data[var][pd.datetime(2019,1,1):pd.datetime(2023,12,31)]*nee_scaler
            out = da.groupby(da.index.year).cumsum()
        elif var=='LH':
            da = data[var][pd.datetime(2019,1,1):pd.datetime(2023,12,31)]*lh_scaler
            out = da.groupby(da.index.year).cumsum()
        else:
            da = data[var][pd.datetime(2019,1,1):pd.datetime(2023,12,31)]
            out = da.groupby(da.index.year).cumsum()
            
    elif (site == 'NEON-ABBY'):
        if var=='NEE':
            da = data[var][pd.datetime(2021,1,1):pd.datetime(2022,12,31)]*nee_scaler
            out = da.groupby(da.index.year).cumsum()
        elif var=='LH':
            da = data[var][pd.datetime(2021,1,1):pd.datetime(2022,12,31)]*lh_scaler
            out = da.groupby(da.index.year).cumsum()
        else:
            da = data[var][pd.datetime(2021,1,1):pd.datetime(2022,12,31)]
            out = da.groupby(da.index.year).cumsum()
        
    elif (site == 'US-Me6'):
        if var =='GPP':
            da = data[var][pd.datetime(2019,1,1):pd.datetime(2021,12,31)]
            out = da.groupby(da.index.year).cumsum()
        elif var == 'NEE':
            da = data[var][pd.datetime(2011,1,1):pd.datetime(2022,12,31)]*nee_scaler
            out = da.groupby(da.index.year).cumsum()
        elif var =='LH':
            da = data[var][pd.datetime(2011,1,1):pd.datetime(2022,12,31)]*lh_scaler
            da[da<0] = np.NaN
            out = da.groupby(da.index.year).cumsum()
        else:
            print("var must be 'LH','GPP','NEE' ")
    
    else:
        print("site must be one of: CA-Ca3, US-Me6, NEON-WREF, NEON-ABBY")
        
    return out