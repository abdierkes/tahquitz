import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

from datetime import date
import re
import logging

from models import weather_hour_data
from regex import date_match, hour_data

#load .env & db params
load_dotenv()

db_params = {"user": os.getenv("USERNAME"),
             "password": os.getenv("PASSWORD"),
             "host": os.getenv("HOST"),
             "port": os.getenv("PORT"),
             "dbname": os.getenv("DBNAME")
             }

#access api thru requests and bs4; finditer using regex matches
yesterday_url='https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/33.760962%2C%20-116.683304/yesterday?unitGroup=metric&key=ASWC8N4FGJQWAM7MH5DF7JEWU&contentType=json'
tah_yes = requests.get(yesterday_url)
tah_data = str(BeautifulSoup(tah_yes.text, 'html.parser'))
date_matches = date_match.findall(tah_data)
hour_data_matches = hour_data.finditer(tah_data)

#pass the capture groups thru model to validate datatypes
for match in hour_data_matches:
    group_dict = match.groupdict()

    # manually add date in & call model for data validation
    group_dict['date'] = str(date_matches[0])
    weather_hour_data_model = weather_hour_data(**group_dict)

    # convert model into dictionary for postgresql upload
    model_dict = weather_hour_data_model.model_dump()

    #sql insert query
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
