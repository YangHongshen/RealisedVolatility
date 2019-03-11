import numpy as np
import pandas as pd
import datetime
import calendar
import math

tickData = pd.read_csv("DataSource/Sample.csv", names=['TimeStamp', 'Price', 'Quantity'])
tickData['Date'] = pd.to_datetime(tickData['TimeStamp'], unit='s').dt.date

incomplete_first_day_removal = tickData.loc[tickData["Date"] == tickData.iloc[0]["Date"]]
tickData = tickData.drop(incomplete_first_day_removal.index)
incomplete_last_day_removal = tickData.loc[tickData["Date"] == tickData.iloc[-1]["Date"]]
tickData = tickData.drop(incomplete_last_day_removal.index)

start_unix_stamp = calendar.timegm((datetime.datetime.strptime(str(tickData.iloc[0]["Date"]), "%Y-%m-%d").timetuple()))

# M is the length of each intervals
M_intervals = {"ten_min": 600, "half_hour": 1800, "one_hour": 3600}
first_day_unix = calendar.timegm((datetime.datetime.strptime(str(tickData.iloc[0]["Date"]), "%Y-%m-%d").timetuple()))
last_day_unix = calendar.timegm((datetime.datetime.strptime(str(tickData.iloc[-1]["Date"]), "%Y-%m-%d").timetuple()))
total_day_unix = last_day_unix - first_day_unix

daily_loop_unix_stamp = start_unix_stamp
loop_unix_stamp = daily_loop_unix_stamp
RV_dataframe = pd.DataFrame(columns=["TimeStamp", "RV"])

i = 0
while loop_unix_stamp <= start_unix_stamp + total_day_unix:
    while loop_unix_stamp <= daily_loop_unix_stamp + 86400:
        RV_daily = np.square(
            (math.log(tickData[tickData["TimeStamp"] < (loop_unix_stamp + M_intervals["half_hour"])].iloc[0]["Price"])
             - math.log(tickData[tickData["TimeStamp"] < (loop_unix_stamp + M_intervals["half_hour"])].iloc[-1][
                            "Price"])))
        loop_unix_stamp = loop_unix_stamp + M_intervals["half_hour"]
    RV_dataframe.loc[i] = [daily_loop_unix_stamp, RV_daily]
    i = i + 1
    daily_loop_unix_stamp = daily_loop_unix_stamp + 86400
    loop_unix_stamp = daily_loop_unix_stamp

RV_dataframe.to_csv('DataSource/RV_' + list(M_intervals.keys())[0] + '.csv')
