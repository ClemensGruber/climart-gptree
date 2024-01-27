import pandas as pd
import datetime

# Get current season 
def get_season(date: datetime.datetime, north_hemisphere: bool = True) -> str:
    now = (date.month, date.day)
    if (3, 21) <= now < (6, 21):
        season = 'spring' if north_hemisphere else 'fall'
    elif (6, 21) <= now < (9, 21):
        season = 'summer' if north_hemisphere else 'winter'
    elif (9, 21) <= now < (12, 21):
        season = 'fall' if north_hemisphere else 'spring'
    else:
        season = 'winter' if north_hemisphere else 'summer'
    return season

# Replace variables in promt with values 
def add_current_context(text):
    # Get current time, date and season
    current_datetime = datetime.datetime.now()
    time_string = current_datetime.strftime("%H:%M")
    date_string = current_datetime.strftime("%Y-%m-%d")
    season_string = get_season(current_datetime, north_hemisphere=True)

    # Get sensor data
    df = pd.read_json("https://weather.hiveeyes.org/api/climart/zku/weatherstation/main/data.json?from=now-168h&to=now")
    COLS = ['time', 'soilmoisture1', 'soilmoisture2', 'hrain_piezo',  'temp']
    df = df[COLS].set_index("time")
    df.index = pd.to_datetime(df.index)
    data = df.resample('H').max().reset_index()
    text = text.replace("UHRZEIT", time_string)
    text = text.replace("DATUM", date_string)
    text = text.replace("JAHRESZEIT", season_string)
    text = text.replace("TEMP", f"{round(df.temp.iloc[-1])}")
    text = text.replace("BODENFEUCHTE", f"{round(df.soilmoisture2.iloc[-1])}")
    text = text.replace("REGEN", f"{round(.1*df.hrain_piezo.sum())}") #TODO einheit fixen
    return text
