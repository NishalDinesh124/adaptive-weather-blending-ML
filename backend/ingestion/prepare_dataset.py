import pandas as pd
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_FILE = BASE_DIR / "data" / "raw" / "Data from 4 models.csv"
ERA5_FILE = BASE_DIR / "data" / "raw" / "ERA5 data.csv"

OUTPUT_FILE = BASE_DIR / "data" / "processed" / "training_dataset.csv"


# --------------------------------------------------
# 1. Load forecast model data
# --------------------------------------------------

models = pd.read_csv(MODEL_FILE, skiprows=3)

models = models.rename(columns={
    "time": "time",

    "precipitation_ecmwf_ifs025 (mm)": "ifs_precip",
    "temperature_2m_ecmwf_ifs025 (°C)": "ifs_temp",

    "precipitation_ecmwf_aifs025_single (mm)": "aifs_precip",
    "temperature_2m_ecmwf_aifs025_single (°C)": "aifs_temp",

    "precipitation_ncep_gfs_global (mm)": "gfs_precip",
    "temperature_2m_ncep_gfs_global (°C)": "gfs_temp",

    "precipitation_ncep_hgefs025_ensemble_mean (mm)": "hgefs_precip",
    "temperature_2m_ncep_hgefs025_ensemble_mean (°C)": "hgefs_temp",
})


# --------------------------------------------------
# 2. Load ERA5 reference data
# --------------------------------------------------

era5 = pd.read_csv(ERA5_FILE, skiprows=3)

era5 = era5.rename(columns={
    "time": "time",
    "temperature_2m (°C)": "era5_temp",
    "precipitation (mm)": "era5_precip",
})


# --------------------------------------------------
# 3. Convert timestamps
# --------------------------------------------------

models["time"] = pd.to_datetime(models["time"])
era5["time"] = pd.to_datetime(era5["time"])


# --------------------------------------------------
# 4. Keep only required columns
# --------------------------------------------------

models = models[
    [
        "time",
        "ifs_precip",
        "ifs_temp",
        "aifs_precip",
        "aifs_temp",
        "gfs_precip",
        "gfs_temp",
        "hgefs_precip",
        "hgefs_temp",
    ]
]

era5 = era5[
    [
        "time",
        "era5_precip",
        "era5_temp",
    ]
]


# --------------------------------------------------
# 5. Merge forecasts with ERA5
# --------------------------------------------------

df = pd.merge(
    models,
    era5,
    on="time",
    how="inner"
)


# --------------------------------------------------
# 6. Remove rows where any model is unavailable
# --------------------------------------------------

forecast_columns = [
    "ifs_precip",
    "ifs_temp",
    "aifs_precip",
    "aifs_temp",
    "gfs_precip",
    "gfs_temp",
    "hgefs_precip",
    "hgefs_temp",
]

df = df.dropna(subset=forecast_columns)


# --------------------------------------------------
# 7. Sort by time
# --------------------------------------------------

df = df.sort_values("time").reset_index(drop=True)


# --------------------------------------------------
# 8. Save
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)


# --------------------------------------------------
# 9. Print summary
# --------------------------------------------------

print("\nDataset created successfully!")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nTime range:")
print("Start:", df["time"].min())
print("End:  ", df["time"].max())

print("\nFirst 5 rows:")
print(df.head())

print("\nSaved to:")
print(OUTPUT_FILE)