import re

date_time = "[0-9]+:[0-9]+:[0-9]+"
floater = "[+-]?(\d+(\.\d*)?|\d*)([eE][+-]?\d+)?"
stringer = "[A-Za-z0-9]+"  # ([-][A-Za-z]+)?"

hour_data = re.compile(f"\"datetime\":\"(?P<hour>{date_time}).*?"
                       f"\"temp\":(?P<temperature>{floater}).*?"
                       f"\"feelslike\":(?P<feels_like>{floater}).*?"
                       f"\"humidity\":(?P<humidity>{floater}).*?"
                       f"\"dew\":(?P<dew>{floater}).*?"
                       f"\"precip\":(?P<precipitation>{floater}).*?"
                       f"\"precipprob\":(?P<precip_prob>{floater}).*?"
                       f"\"snow\":(?P<snow>{floater}).*?"
                       f"\"snowdepth\":(?P<snow_depth>{floater}).*?"
                       f"\"preciptype\":\[?\"?(?P<precip_type>{stringer})\"?]?.*?"
                       f"\"windgust\":(?P<wind_gust>{floater}).*?"
                       f"\"windspeed\":(?P<wind_speed>{floater}).*?"
                       f"\"winddir\":(?P<wind_direction>{floater}).*?"
                       f"\"pressure\":(?P<pressure>{floater}).*?"
                       f"\"visibility\":(?P<visibility>{floater}).*?"
                       f"\"cloudcover\":(?P<cloud_cover>{floater}).*?"
                       f"\"solarradiation\":(?P<solar_radiation>{floater}).*?"
                       f"\"solarenergy\":(?P<solar_energy>{floater}).*?"
                       f"\"uvindex\":(?P<uv_index>{floater}).*?"
                       f"\"severerisk\":(?P<severe_risk>{floater}).*?",
                       re.DOTALL
                       )

date_match = re.compile(r"\"days\":\[\{\"datetime\":\"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})\",\"datetimeEpoch")



