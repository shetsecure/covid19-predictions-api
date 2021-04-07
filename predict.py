import requests
import pandas as pd
import numpy as np
from prophet import Prophet
from typing import List
from functools import lru_cache

from utils import *

@lru_cache
def get_predictions(country_name : str, attr : str, h_many : int) -> List[int]:
    """
        Fitting the prophet model and making the predictions.
        Will return a list of predictions for "h_many" following days.

        attr: confirmed cases or deaths.
    """

    if not (attr == "confirmed" or attr == "deaths"):
        raise ValueError("Attribute must be either confirmed or deaths !")

    if not int(h_many) > 0:
        raise ValueError("days must be > 0")

    df = construct_time_line(country_name)[['date', attr]]

    # renaming the columns for prophet
    df.columns = ['ds', 'y']

    # log exp trick to never predict negative values
    # df['y'] = df['y'] + 1
    # df['y'] = np.log(df['y'])

    # fitting the model
    model = Prophet()
    model.fit(df)

    # define the period for which we want a prediction
    future = list()

    today = list(df['ds'])[-1] # getting today's date

    for i in range(1, h_many+1):
        s = str(today.year) + '-' + str(today.month)
        date = s + '-%02d' % (i + today.day)
        future.append([date])
    future = pd.DataFrame(future)
    future.columns = ['ds']
    future['ds']= pd.to_datetime(future['ds'])


    # forcasting
    forecast = model.predict(future)

    # constructing the predictions that will be returned
    preds = dict()
    for i in range(len(forecast)):
        date = str(forecast.iloc[i]['ds']).split(' ')[0]
        
        # exp to get original forecast
        # yhat = np.exp(forecast.iloc[i]['yhat']) - 1
        # yhat_lower = np.exp(forecast.iloc[i]['yhat_lower']) - 1
        # yhat_upper = np.exp(forecast.iloc[i]['yhat_upper']) - 1

        yhats = sorted([abs(forecast.iloc[i]['yhat']), abs(forecast.iloc[i]['yhat_lower']),
                        abs(forecast.iloc[i]['yhat_upper'])])

        for i in range(len(yhats)):
            yhats[i] = int(round(yhats[i], 0))

        yhat_lower, yhat, yhat_upper = yhats

        preds[date] = {'yhat' : yhat, 'yhat_lower' : yhat_lower, 'yhat_upper' : yhat_upper}
    
    if len(country_name) == 2:
        country = get_name_from_code[country_name.upper()].capitalize()
    else:
        country = country_name.capitalize()

    p = dict()
    p[country] = preds

    return p