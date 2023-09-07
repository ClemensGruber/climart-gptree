import pandas as pd
import datetime

def add_current_context(text):
    current_time = datetime.datetime.now().time()
    time_string = current_time.strftime("%H:%M")

    df = pd.read_json("https://weather.hiveeyes.org/api/climart/zku/weatherstation/main/data.json?from=now-168h&to=now")
    COLS = ['time', 'soilmoisture1', 'soilmoisture2', 'hrain_piezo',  'temp']
    df = df[COLS].set_index("time")
    df.index = pd.to_datetime(df.index)
    data = df.resample('H').max().reset_index()
    text = text.replace("UHRZEIT", time_string)
    text = text.replace("TEMP", f"{round(df.temp.iloc[-1])}")
    text = text.replace("BODENFEUCHTE", f"{round(df.soilmoisture2.iloc[-1])}")
    text = text.replace("REGEN", f"{round(.1*df.hrain_piezo.sum())}") #TODO einheit fixen
    return text