# Adaptive Weather Blending

## Project Goal

We are building a **Hybrid AI–NWP Weather Forecast Blending System**.

The basic idea is simple:

> Different weather models perform differently depending on the situation. Instead of trusting only one model, our system learns how much to trust each model and combines them into a better forecast.

Our first prototype focuses on:

- **Location:** around 8.5°N, 77.0°E (Thiruvananthapuram/Kerala region)
- **Variables:** Temperature + Precipitation
- **Forecast sources:** ECMWF IFS, GFS, ECMWF AIFS, NCEP HGEFS
- **Reference dataset:** ERA5
- **Current stage:** Data collection, cleaning, and baseline evaluation
- **Next stage:** Equal-weight blending → ML dynamic weighting

---

## 1. Forecast Sources

We intentionally use different types of forecasting systems because the hackathon problem asks for a hybrid framework.

### Physical NWP models

- **ECMWF IFS** — traditional physics-based numerical weather prediction
- **NCEP GFS** — traditional physics-based numerical weather prediction

### AI/ML weather model

- **ECMWF AIFS** — ECMWF's AI-based forecasting system

### Ensemble forecast

- **NCEP HGEFS Ensemble Mean** — an ensemble-derived forecast representing multiple forecast members

So our architecture is:

```text
Physical NWP       AI model       Ensemble
    IFS              AIFS           HGEFS
     GFS
       \              |              /
        \             |             /
         └────── Forecast Inputs ────┘
                       ↓
                ML Weight Engine
                       ↓
                Blended Forecast
```

---

## 2. Why Do We Need Blending?

No single forecast model is guaranteed to be the best all the time.

For example, our current evaluation shows:

### Temperature

| Model | MAE |
|---|---:|
| IFS | **0.324 °C** |
| HGEFS | 0.857 °C |
| GFS | 1.053 °C |
| AIFS | 1.168 °C |

### Precipitation

| Model | MAE |
|---|---:|
| IFS | **0.145 mm** |
| AIFS | 0.226 mm |
| HGEFS | 0.217 mm |
| GFS | 0.284 mm |

IFS is currently the strongest individual model in our dataset.

However, this is an **average over the whole evaluation period**. It does not mean IFS will be best at every hour.

The purpose of the project is therefore to learn:

> **When should we trust each model, and by how much?**

---

## 3. Data We Have Collected

### Forecast dataset

We downloaded historical forecast data containing:

- ECMWF IFS
- NCEP GFS
- ECMWF AIFS
- NCEP HGEFS Ensemble Mean

For each model we have:

- Temperature
- Precipitation
- Hourly timestamps

The models do not all have the same historical availability.

For example, GFS has a longer history, while AIFS and HGEFS start later.

We **do not fill missing historical model values with zero or fake data**.

Instead, for the full four-model experiment we use the period where all four forecast sources are available.

Current common dataset:

```text
Start: 2026-01-21 07:00
End:   2026-09-12 23:00
Rows:  5,633
```

### ERA5 reference dataset

We also downloaded ERA5 data containing:

- Temperature
- Precipitation
- Hourly timestamps

ERA5 is being used as our **reference/verification dataset**.

It is not treated as a direct observation from a weather station. If we later obtain reliable station/gauge observations, they can be added as a stronger verification source.

---

## 4. Current Project Structure

```text
adaptive-weather-blending/
│
├── .venv/
│
├── backend/
│   ├── ingestion/
│   │   ├── fetch_weather.py
│   │   └── prepare_dataset.py
│   │
│   ├── models/
│   │   └── evaluate_models.py
│   │
│   ├── blending/
│   │
│   └── api/
│
├── frontend/
│
├── data/
│   ├── raw/
│   │   ├── Data from 4 models.csv
│   │   └── ERA5 data(1).csv
│   │
│   └── processed/
│       └── training_dataset.csv
│
├── notebooks/
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 5. What We Have Done So Far

### Step 1 — Created the project

Created the Git/project structure and Python virtual environment.

Installed the basic Python packages needed for data work.

### Step 2 — Tested weather API access

Successfully tested Open-Meteo's ECMWF forecast endpoint.

This confirmed that we can retrieve model forecasts programmatically.

### Step 3 — Downloaded historical model forecasts

Downloaded historical data for:

```text
IFS
GFS
AIFS
HGEFS
```

with:

```text
Temperature
Precipitation
```

### Step 4 — Downloaded ERA5

Downloaded ERA5 temperature and precipitation to act as the reference dataset.

### Step 5 — Created the clean dataset

`prepare_dataset.py`:

1. Reads the model CSV
2. Reads ERA5 CSV
3. Converts timestamps
4. Renames columns
5. Merges both datasets by time
6. Removes rows where one of the four models is unavailable
7. Saves the final dataset

Output:

```text
data/processed/training_dataset.csv
```

The final dataset currently contains 11 columns:

```text
time

ifs_precip
ifs_temp

gfs_precip
gfs_temp

aifs_precip
aifs_temp

hgefs_precip
hgefs_temp

era5_precip
era5_temp
```

### Step 6 — Evaluated individual models

We calculated:

- MAE — Mean Absolute Error
- RMSE — Root Mean Squared Error

for temperature and precipitation.

This gives us our **baseline**.

---

# 6. What Happens Next?

We should NOT jump directly into complicated ML.

The next steps are:

## Step 7 — Equal-weight baseline

First combine all four forecasts equally:

```text
IFS    = 25%
GFS    = 25%
AIFS   = 25%
HGEFS  = 25%
```

For example:

```text
IFS    = 30°C
GFS    = 32°C
AIFS   = 31°C
HGEFS  = 29°C
```

Then:

```text
Blended =

0.25 × 30
+ 0.25 × 32
+ 0.25 × 31
+ 0.25 × 29

= 30.5°C
```

We compare this result against ERA5.

This tells us whether simple averaging is useful.

---

## Step 8 — Build the ML weight model

After the equal-weight baseline, we train ML to predict **weights**.

Instead of always:

```text
25% / 25% / 25% / 25%
```

ML might learn:

```text
IFS    → 50%
GFS    → 10%
AIFS   → 25%
HGEFS  → 15%
```

At another time it might produce completely different weights.

The final forecast becomes:

```text
Final Forecast =
w_IFS × IFS
+ w_GFS × GFS
+ w_AIFS × AIFS
+ w_HGEFS × HGEFS
```

with:

```text
w_IFS + w_GFS + w_AIFS + w_HGEFS = 1
```

This is the core of the project.

---

## 9. What Should ML Consider?

Eventually, the weight model can use features such as:

- Current forecast values
- Month/season
- Forecast lead time
- Recent model errors
- Recent model performance
- Temperature conditions
- Rainfall conditions
- Weather regime
- Location

The goal is:

```text
Current situation
       ↓
ML predicts model weights
       ↓
Combine forecasts
       ↓
Better forecast
```

---

## 10. How We Will Prove It Works

We will compare:

```text
IFS
GFS
AIFS
HGEFS
        ↓
Equal-weight blend
        ↓
ML dynamic blend
```

using:

- MAE
- RMSE

The key result we want is:

```text
ML Blend Error < Best Individual Model Error
```

If that happens, we have strong evidence that adaptive blending is providing value.

---

## 11. Future Architecture

Once the ML experiment works, the system can become operational:

```text
Latest forecasts
     ↓
IFS / GFS / AIFS / HGEFS
     ↓
Feature extraction
     ↓
Trained ML weight model
     ↓
Dynamic weights
     ↓
Blended forecast
     ↓
Risk / uncertainty analysis
     ↓
FastAPI backend
     ↓
React dashboard
```

The dashboard can eventually show:

- Current blended temperature
- Current blended precipitation
- Individual model predictions
- Dynamic model weights
- Model comparison
- Forecast confidence/uncertainty
- Weather risk indicators
- Maps/visualizations

---

# Important Notes for Teammates

### Do not

- Replace missing model data with `0`
- Treat ERA5 as a direct weather-station observation
- Assume IFS will always be the best model
- Train and test on the exact same data
- Start with a complicated neural network unnecessarily

### Do

- Keep the four forecast sources separate
- Keep ERA5 separate as the reference/target
- Preserve timestamps carefully
- Compare individual models first
- Build a simple baseline before ML
- Use a proper train/test time split for the ML stage
- Record MAE/RMSE for every experiment

---

## Current Status

[✓] Project structure
[✓] Python environment
[✓] Multi-model forecast ingestion
[✓] Historical forecast data
[✓] ERA5 reference data
[✓] Data cleaning/merging
[✓] Individual model evaluation
[✓] Equal-weight baseline
[✓] Adaptive temperature XGBoost
[✓] Precipitation Tweedie XGBoost
[✓] Chronological train/test evaluation
[✓] Live hybrid forecast pipeline
[ ] FastAPI backend
[ ] React dashboard
[ ] Deployment
[ ] Final presentation

## Current Stage

The ML prototype and live forecast pipeline are complete.

The current prototype:
- fetches forecasts from four weather models
- dynamically blends temperature forecasts using XGBoost-predicted model error
- predicts precipitation using a Tweedie XGBoost model
- compares against individual models and an equal-weight baseline
- uses chronological train/test evaluation
- produces a unified hybrid forecast output

The remaining work is primarily product integration:
- FastAPI endpoint
- dashboard
- deployment
- final presentation
