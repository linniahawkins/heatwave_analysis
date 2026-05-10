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
        df = pd.read_csv(filename,header=0,index_col=0, parse_dates=True)
        df.loc['2018', :] = np.NaN
        df_daily = df[df['SW_IN']>sw_thresh].resample('D').mean()
        
    elif (site=='US-Me6'):
        filename = os.path.join(in_dir+'US-Me6.csv')
        df = pd.read_csv(filename,header=0,index_col=0, parse_dates=True)
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
    """Cumulative annual sum of `var` for the site's data record."""
    
    nee_scaler = (1/1e6) * 86400 * 12       # umol/m2/s -> gC/m2/day
    lh_scaler  = (1/2.45e6) * 86400         # W/m2 -> mm/day
    
    site_years = {
        'CA-Ca3':    (2002, 2022),
        'NEON-WREF': (2019, 2024),
        'NEON-ABBY': (2019, 2024),
        'US-Me6':    (2011, 2022),
    }
    if site not in site_years:
        raise ValueError(f"site must be one of: {list(site_years)}")
    
    y0, y1 = site_years[site]
    da = data[var].loc[pd.Timestamp(y0, 1, 1):pd.Timestamp(y1, 12, 31)].copy()
    
    if var == 'NEE':
        da = da * nee_scaler
    elif var == 'LH':
        da = da * lh_scaler
        if site == 'US-Me6':
            da[da < 0] = np.nan   # filter negative LH at Me6 only
    
    return da.groupby(da.index.year).cumsum()