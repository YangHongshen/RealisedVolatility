import numpy as np
import pandas as pd
import datetime
import calendar
import math

# set the M here
M_interval = 3600

tickData = pd.read_csv("DataSource/Sample.csv", names=['TimeStamp', 'Price', 'Quantity'])
tickData['Date'] = pd.to_datetime(tickData['TimeStamp'], unit='s').dt.date

incomplete_first_day_removal = tickData.loc[tickData["Date"] == tickData.iloc[0]["Date"]]
tickData = tickData.drop(incomplete_first_day_removal.index)
incomplete_last_day_removal = tickData.loc[tickData["Date"] == tickData.iloc[-1]["Date"]]
tickData = tickData.drop(incomplete_last_day_removal.index)

first_day_unix = calendar.timegm((datetime.datetime.strptime(str(tickData.iloc[0]["Date"]), "%Y-%m-%d").timetuple()))
last_day_unix = calendar.timegm((datetime.datetime.strptime(str(tickData.iloc[-1]["Date"]), "%Y-%m-%d").timetuple()))

daily_loop_unix_stamp = first_day_unix
loop_unix_stamp = daily_loop_unix_stamp
RV_dataframe = pd.DataFrame(columns=["TimeStamp", "RV"])

i = 0
while loop_unix_stamp <= last_day_unix:
    RV_daily = 0
    while loop_unix_stamp <= daily_loop_unix_stamp + 86400:
        condition_1 = tickData["TimeStamp"] < loop_unix_stamp + M_interval
        condition_2 = tickData["TimeStamp"] > loop_unix_stamp
        try:
            p_later = tickData[condition_1 & condition_2].iloc[-1]["Price"]
            p_former = tickData[condition_1 & condition_2].iloc[0]["Price"]
            r = math.log(p_later/p_former)
        except IndexError:
            r = 0
        RV_daily = RV_daily + np.square(r)
        loop_unix_stamp = loop_unix_stamp + M_interval
    RV_dataframe.loc[i] = [daily_loop_unix_stamp, RV_daily]
    i = i + 1
    daily_loop_unix_stamp = daily_loop_unix_stamp + 86400
    loop_unix_stamp = daily_loop_unix_stamp

RV_dataframe.to_csv('outcome.csv')
