import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from datetime import date
import re
import logging


load_dotenv()

class weather_hour_data(BaseModel):
    date: str
    hour: str
    temperature: float
    feels_like: float
    dew: float
    precipitation: float
    precip_prob: float
    snow: float
    snow_depth: float
    precip_type: str
    wind_gust: float
    wind_speed: float
    wind_direction: float
    pressure: float
    visibility: float
    cloud_cover: float
    solar_radiation: float
    uv_index: float
    severe_risk: float


class date_data(BaseModel):
    data: str


date_time = "[0-9]+:[0-9]+:[0-9]+"
floater = "[+-]?(\d+(\.\d*)?|\d*)([eE][+-]?\d+)?"
stringer = "[A-Za-z]+"  # ([-][A-Za-z]+)?"

hour_data = re.compile(f"\"datetime\":\"(?P<hour>{date_time}).*?"
                       f"\"temp\":(?P<temperature>{floater}).*?"
                       f"\"feelslike\":(?P<feels_like>{floater}).*?"
                       f"\"humidity\":(?P<humidity>{floater}).*?"
                       f"\"dew\":(?P<dew>{floater}).*?"
                       f"\"precip\":(?P<precipitation>{floater}).*?"
                       f"\"precipprob\":(?P<precip_prob>{floater}).*?"
                       f"\"snow\":(?P<snow>{floater}).*?"
                       f"\"snowdepth\":(?P<snow_depth>{floater}).*?"
                       f"\"preciptype\":(?P<precip_type>{stringer}).*?"
                       f"\"windgust\":(?P<wind_gust>{floater}).*?"
                       f"\"windspeed\":(?P<wind_speed>{floater}).*?"
                       f"\"winddir\":(?P<wind_direction>{floater}).*?"
                       f"\"pressure\":(?P<pressure>{floater}).*?"
                       f"\"visibility\":(?P<visibility>{floater}).*?"
                       f"\"cloudcover\":(?P<cloud_cover>{floater}).*?"
                       f"\"solarradiation\":(?P<solar_radiation>{floater}).*?"
                       f"\"solarenergy\":(?P<solar_energy>{floater}).*?"
                       f"\"uvindex\":(?P<uv_index>{floater}).*?"
                       f"\"severerisk\":(?P<severe_risk>{floater}).*?"
                       )

date_match = re.compile(r"\"days\":\[\{\"datetime\":\"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})\",\"datetimeEpoch")

db_params = {"user": os.getenv("USERNAME"),
             "password": os.getenv("PASSWORD"),
             "host": os.getenv("HOST"),
             "port": os.getenv("PORT"),
             "dbname": os.getenv("DBNAME")
             }

yesterday_url='https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/33.760962%2C%20-116.683304/yesterday?unitGroup=metric&key=ASWC8N4FGJQWAM7MH5DF7JEWU&contentType=json'
tah_yes = requests.get(yesterday_url)
tah_data = str(BeautifulSoup(tah_yes.text, 'html.parser'))
date_matches = date_match.findall(tah_data)
hour_data_matches = hour_data.finditer(tah_data)

for match in hour_data_matches:
    group_dict = match.groupdict()

    # manually add date in & call model for data validation
    group_dict['date'] = str(date_matches[0])
    weather_hour_data_model = weather_hour_data(**group_dict)

    # convert model into dictionary for postgresql upload
    model_dict = weather_hour_data_model.model_dump()

    insert_query = '''
                   INSERT INTO tahquitz_weather (date, hour, temperature, feels_like, dew, precipitation,
                                                 precip_prob, snow, snow_depth, precip_type, wind_gust,
                                                 wind_speed, wind_direction, pressure, visibility, cloud_cover,
                                                 solar_radiation, uv_index, severe_risk)
                   VALUES(%(date)s, %(hour)s, %(temperature)s, %(feels_like)s, %(dew)s, %(precipitation)s,
                         %(precip_prob)s, %(snow)s, %(snow_depth)s, %(precip_type)s, %(wind_gust)s,
                         %(wind_speed)s, %(wind_direction)s, %(pressure)s, %(visibility)s, %(cloud_cover)s,
                         %(solar_radiation)s, %(uv_index)s, %(severe_risk)s)
                   '''

    logger = logging.getLogger(__name__)
    conn = psycopg2.connect(**db_params)

    try:
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute(insert_query, model_dict)
        conn.commit()

    except psycopg2.Error as e:
        logger.error(f"PostgreSQL error: {e}")

    finally:
        if conn:
            conn.close()

print(f'Parsed & Uploaded on {date.today()}')
