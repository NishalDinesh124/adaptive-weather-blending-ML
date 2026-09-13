import pandas as pd

TEMP__FORECAST_COLUMNS=[
    "ifs_temp",
    "gfs_temp",
    "aifs_temp",
    "hgefs_temp",
]

def build_temperature_features(df: pd.DataFrame)->pd.DataFrame:
    features=pd.DataFrame(index=df.index)

    time=pd.to_datetime(df["time"])
    features["hour"]= time.dt.hour
    features["month"]=time.dt.month
    features["day_of_year"] = time.dt.dayofyear

    for column in TEMP__FORECAST_COLUMNS:
        features[column]=df[column]

    forecasts=df[TEMP__FORECAST_COLUMNS]

    features["temp_mean"]=forecasts.mean(axis=1)
    features["temp_std"]= forecasts.std(axis=1)
    features["temp_min"]= forecasts.min(axis=1)
    features["temp_max"]= forecasts.max(axis=1)

    return features


