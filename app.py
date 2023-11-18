#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import required libraries
import pandas as pd
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error


# In[2]:


def fahrenheit_to_celsius(temp_f):
    """
    Convert temperature from Fahrenheit to Celsius
    """
    temp_c = (temp_f - 32) * 5/9
    return temp_c

def celsius_to_fahrenheit(temp_c):
    """
    Convert temperature from Celsius to Fahrenheit
    """
    temp_f = (temp_c * 9/5) + 32
    return temp_f
#create class CornGDD and initiate
class CornGDD:
    def __init__(self,hourly_temp_df, time_column, temp_column, celcius= True):
        self.time_column = time_column
        self.temp_column = temp_column
        self.celcius = celcius

        
        # convert the timestamp column to the pandas datetime data type
        hourly_temp_df[self.time_column] = pd.to_datetime(hourly_temp_df[self.time_column])
        
        # Convert the temperature to Celsius if required
        if not celcius:
            hourly_temp_df[self.temp_column] = fahrenheit_to_celsius(hourly_temp_df[self.temp_column])
        # create a new pandas DataFrame
        self.daily_data = pd.DataFrame(columns=['Date', 'Min_temp', 'Max_temp'])
        # group the data by date and calculate the daily temperature range
        self._group_data(hourly_temp_df)
    
    def _group_data(self, hourly_temp_df):
        # loop over each date in the grouped data
        grouped_data = hourly_temp_df.groupby(hourly_temp_df[self.time_column].dt.date)
        dates = grouped_data.groups.keys()
        # create a new row with the date, minimum temperature, and maximum temperature, and append it
        for date in dates:
            grouped_data_daily = grouped_data.get_group(date)
            if self.celcius:
                temp_min = grouped_data_daily[self.temp_column].min()
                temp_max = grouped_data_daily[self.temp_column].max()
            else:
                temp_min = celsius_to_fahrenheit(grouped_data_daily[self.temp_column].min())
                temp_max = celsius_to_fahrenheit(grouped_data_daily[self.temp_column].max())
                row = [date, temp_min, temp_max]
                self.daily_data.loc[len(self.daily_data)] = row
    #define corn gdd as con_gdd that inputs start date and end date in class CornGDD
    def con_gdd(self, start_date, end_date):
            #base temperature of corn is 10°C(50°F)
            """
            Corn Growing Degree Days (Corn AGDD) (°C or °F)
            Growing degree days GDD (°C or °F) for Corn are calculated as follows:
            Daily Corn GDD = ((Daily Max Temp + Daily Min Temp ) / 2) - base temp
            Daily Corn GDD (°C) = ((Daily Max Temp °C + Daily Min Temp °C) / 2) - 10°C
            or
            Daily Corn GDD (°F) = ((Daily Max Temp °F + Daily Min Temp °F)/2) - 50°F
            With the following constraints:
            If daily Max Temp > 30 °c (86 °F) it's set equal to 30°C (86°F).
            If daily Max or Min Temp < 10°C (50°F), it's set equal to 10°C(50°F).
            https://ndawn.ndsu.nodak.edu/help-corn-growing-degree-days.html
                
 
            """
            start_date_str = pd.Timestamp(start_date)
            end_date_str = pd.Timestamp(end_date)


            date_mask = (self.daily_data['Date'] >= start_date) & (self.daily_data['Date'] <= end_date)
            masked_data = self.daily_data.loc[date_mask]

            gdd_values = [0]
            agdd_values = [0]
            cumulative_gdd = 0
            #Since our input data is in F
            # If the daily Max and/or Min Temp < 50°F, it's set equal to 50 °F
            # If the daily Max Temperature > 86°F, it's set equal to 86 °F
            masked_data['Min_temp'] = masked_data['Min_temp'].apply(lambda x: max(x, 50))
            masked_data['Max_temp'] = masked_data['Max_temp'].apply(lambda x: max(x, 50))
            masked_data['Max_temp'] = masked_data['Max_temp'].apply(lambda x: min(x, 86))

            for i in range(1, len(masked_data)):
                mean_temp = (masked_data['Max_temp'].iloc[i] + masked_data['Min_temp'].iloc[i])/2
                gdd = mean_temp - 50

                gdd_values.append(gdd)
                cumulative_gdd += gdd
                agdd_values.append(cumulative_gdd)

            masked_data['gdd'] = gdd_values
            masked_data['agdd'] = agdd_values

            return masked_data


# In[3]:


Becker = pd.read_csv("Becker.csv",on_bad_lines='skip')
Becker['Date'] = pd.to_datetime(Becker[['Year', 'Month', 'Day']])
#Using year 2022 start date and end date for mine gdd
start_date = pd.to_datetime("2022-01-01").date()
end_date = pd.to_datetime("2022-12-31").date()
corn_Becker = CornGDD(Becker, time_column = 'Date', temp_column = 'Avg Air Temp', celcius=False)
corn_gdd_Becker = corn_Becker.con_gdd(start_date, end_date)
#corn_gdd_Becker.to_csv('Becker_output.csv')


# In[6]:


from flask import Flask, request, render_template_string
import pandas as pd
from datetime import datetime

# Sample DataFrame
df = corn_gdd_Becker
df['Date'] = pd.to_datetime(df['Date'])

app = Flask(__name__)

@app.route('/', methods=['GET'])
def form():
    return render_template_string('''
        <form action="/get-data" method="post">
            <input type="date" name="date">
            <input type="submit" value="Get Data">
        </form>
    ''')

@app.route('/get-data', methods=['POST'])
def get_data():
    date = request.form['date']
    print(date)
    result = df[df['Date'].dt.date == pd.to_datetime(date).date()] 
    print(result)
    return result.to_html()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


# In[ ]:




