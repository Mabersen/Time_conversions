# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 23:46:47 2022

@author: maber
"""
import datetime as dt
import julian as jd
import numpy as np
import os as os
import urllib as urllib
import pandas as pd
""" Retrieving the two time correction datasets; I chose finals2000Adaily - 90 days and gpsrapiddaily - 15 days"""


def get_time_conversion_tables():
    
    URL1 = r'https://maia.usno.navy.mil/ser7/finals2000A.daily'
    request_url1 = urllib.request.urlopen(URL1)
    read_url1 = request_url1.read()
    global data_table
    FINALS2000A = read_url1.decode("utf-8")
    
    FINALS2000A = FINALS2000A.splitlines()
    f2000Afix = [float(i[58:67]) for i in FINALS2000A]
    f2000AJD = [(float(i[7:14]) + 2400000.5) for i in FINALS2000A] #converts from MJD to JD
    
    data_table = pd.DataFrame(np.array([f2000AJD, f2000Afix]).T)
    data_table.columns = ['julian_date', 'ut1-utc']
    data_table['datetime_correction'] = data_table['julian_date'].apply(jd.from_jd).apply(str)
    
    data_table[['date', 'time_correction']] = data_table['datetime_correction'].str.split(' ',1, expand =True)
    
    current_date = dt.datetime.now()
    
    if not os.path.exists(f'{current_date.date()}'):
        # print('1')
        os.mkdir(f'{current_date.date()}')
        data_table[['julian_date','ut1-utc']].to_csv(fr'{current_date.date()}/utc2ut1.csv')
        
        
    elif not os.path.exists(fr'{current_date.date()}\utc2ut1.csv'):
        # print('2')
        data_table[['julian_date','ut1-utc']].to_csv(fr'{current_date.date()}/utc2ut1.csv')
    
    return data_table

get_time_conversion_tables()

def get_leap_second_value():
    
    current_date = dt.datetime.now()

    if not os.path.exists(f'{current_date.date()}'):
        # print('1')
        os.mkdir(f'{current_date.date()}')
        
        url = 'https://maia.usno.navy.mil/ser7/tai-utc.dat'
        request_url1 = urllib.request.urlopen(url)
        read_url1 = request_url1.read()
        leapsecond_dat = read_url1.decode("utf-8")
        
        with open(fr'{current_date.date()}\leapsecond_dat.txt', 'w') as f:
            f.write(leapsecond_dat)
            
        leapseconds = float(leapsecond_dat.splitlines()[-1].split(' ')[10])
    
        return leapseconds, leapsecond_dat
    
    elif not os.path.exists(f'{current_date.date()}\leapsecond_dat.txt'):
        # print('2')
        url = 'https://maia.usno.navy.mil/ser7/tai-utc.dat'
        request_url1 = urllib.request.urlopen(url)
        read_url1 = request_url1.read()
        leapsecond_dat = read_url1.decode("utf-8")
        
        with open(fr'{current_date.date()}\leapsecond_dat.txt', 'w') as f:
            f.write(leapsecond_dat)
            
        leapseconds = float(leapsecond_dat.splitlines()[-1].split(' ')[10])
        
        return leapseconds, leapsecond_dat
    
    else:
        # print('3')
        
        with open(fr'{current_date.date()}\leapsecond_dat.txt') as f:
            lines = f.readlines()
            
        leapsecond_dat = lines
        leapseconds = float(leapsecond_dat[-1].split(' ')[10])
        
        return leapseconds, leapsecond_dat


def utc2ut1(timelist):
    
    current_date = dt.datetime.now()
    
    if not os.path.exists(f'{current_date.date()}'):
        os.mkdir(f'{current_date.date()}')
        
        timecorrections = get_time_conversion_tables()
        timecorrections.to_csv(fr'{current_date.date()}\time_conv_tab')
        
        uncorrected_jd = pd.DataFrame(timelist)
        uncorrected_jd.columns = ['datetime_data']
        uncorrected_jd['datetime_data'] = uncorrected_jd['datetime_data'].apply(str)
        uncorrected_jd[['date', 'time']] = uncorrected_jd['datetime_data'].str.split(' ',1, expand = True)
        # uncorrected_jd.columns['combined_date'] = jd.from_jd((uncorrected_jd['julian_date'] + uncorrected_jd['fractional_day']), fmt = 'jd')
        
        merged_data = timecorrections.merge(uncorrected_jd, how = 'inner', on = ['date'])
        merged_data['ut1-utc'] = merged_data['ut1-utc'].apply(float)
        merged_data['timedelta'] = pd.to_timedelta(merged_data['ut1-utc'],'s')
        merged_data['datetime_data'] = pd.to_datetime(merged_data['datetime_data'])
        merged_data['final_datetime_data'] = (merged_data['datetime_data'] + merged_data['timedelta']).apply(pd.DatetimeIndex.tz_localize, tz = ( None))
    
        final_datetime_data = merged_data['final_datetime_data']
        
        
        return final_datetime_data
    
    else:
        timecorrections = pd.read_csv(fr'{current_date.date()}\time_conv_tab')
        
        uncorrected_jd = pd.DataFrame(timelist)
        uncorrected_jd.columns = ['datetime_data']
        uncorrected_jd['datetime_data'] = uncorrected_jd['datetime_data'].apply(str)
        uncorrected_jd[['date', 'time']] = uncorrected_jd['datetime_data'].str.split(' ',1, expand = True)
        # uncorrected_jd.columns['combined_date'] = jd.from_jd((uncorrected_jd['julian_date'] + uncorrected_jd['fractional_day']), fmt = 'jd')
        
        merged_data = timecorrections.merge(uncorrected_jd, how = 'inner', on = ['date'])
        merged_data['ut1-utc'] = merged_data['ut1-utc'].apply(float)
        merged_data['timedelta'] = pd.to_timedelta(merged_data['ut1-utc'],'s')
        merged_data['datetime_data'] = pd.to_datetime(merged_data['datetime_data'])
        merged_data['final_datetime_data'] = (merged_data['datetime_data'] + merged_data['timedelta']).apply(pd.DatetimeIndex.tz_localize, tz = ( None))
    
        final_datetime_data = merged_data['final_datetime_data']
        
        return final_datetime_data

def utc2gps(datetime):
    
    leapseconds = get_leap_second_value()[0]
    time = datetime
    time = time + dt.timedelta(seconds = leapseconds)
    return time
