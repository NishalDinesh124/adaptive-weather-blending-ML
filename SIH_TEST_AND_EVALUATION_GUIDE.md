# SIH Weather Forecasting — Test & Evaluation Scripts

This document explains the purpose of the testing, evaluation, and diagnostic scripts currently built for the SIH prototype.

The scripts are separated from the core ML pipeline because they are mainly used to **evaluate, inspect, and sanity-check** the forecasting system rather than generate the final production forecast.

---

## 1. `test_predict.py`

### Purpose
A basic test of the **trained temperature prediction pipeline**.

### What it does
1. Loads the processed historical training dataset.
2. Runs the trained adaptive temperature models through:
   `generate_adaptive_temperature_forecast()`
3. Prints the first few prediction rows.
4. Checks that the generated temperature model weights add up to approximately `1`.

### What it verifies

The important sanity check is:

```text
weight_ifs + weight_gfs + weight_aifs + weight_hgefs ≈ 1
```

This confirms that the adaptive blending logic is producing a valid convex combination of the four temperature forecasts.

### What it is NOT
This is **not the main accuracy evaluation**.

It is primarily an inference/sanity test:
> “Can the saved models load, produce predictions, and generate valid weights?”

---

## 2. `evaluate_adaptive.py`

### Purpose
This is the main **temperature model evaluation script**.

It compares the individual forecasting systems, a simple equal-weight baseline, and our adaptive XGBoost blend.

### Models compared

- IFS
- GFS
- AIFS
- HGEFS
- Equal-weight blend
- Adaptive XGBoost blend

### Evaluation process

The historical dataset is sorted chronologically and divided into:

```text
80% → training period
20% → unseen test period
```

The evaluation is therefore time-ordered rather than randomly shuffled.

### Metrics

It calculates:

- **MAE — Mean Absolute Error**
- **RMSE — Root Mean Squared Error**

Lower values are better.

### Why this script matters

This is the script that supports the main temperature claim:

> Adaptive weighting substantially improves over a simple equal-weight blend and is competitive with the strongest individual model.

For the current prototype's test period, the recorded results were approximately:

| Method | MAE (°C) | RMSE (°C) |
|---|---:|---:|
| IFS | 0.249 | 0.402 |
| GFS | 0.896 | 1.109 |
| AIFS | 0.886 | 1.070 |
| HGEFS | 0.845 | 1.011 |
| Equal-weight blend | 0.442 | 0.577 |
| Adaptive XGBoost | 0.267 | 0.394 |

The adaptive model therefore improves substantially over equal weighting, while IFS remains slightly better on MAE for this particular location and evaluation period.

### Important interpretation

This does **not** prove that IFS is always the best model.

It only describes performance for the current prototype:

```text
Thiruvananthapuram
+
current historical period
+
current variables/features
+
current lead-time setup
```

---

## 3. `diagnose_temperature_weights.py`

### Purpose
This is a **diagnostic script for understanding what the adaptive temperature model is actually doing**.

Accuracy alone doesn't tell us whether the model is genuinely adapting its weights.

This script investigates the generated weights.

### What it examines

It calculates things such as:

- Average weight assigned to each model
- Which model has the highest weight most often
- How frequently each model receives at least:
  - 50% weight
  - 75% weight
  - 90% weight

### Current diagnostic result

For the evaluated test period:

```text
Average weights

IFS     ≈ 56.7%
GFS     ≈ 14.4%
AIFS    ≈ 16.0%
HGEFS   ≈ 12.9%
```

IFS was the dominant model for most rows, but the other models still received meaningful weight.

This was useful because it checked whether the adaptive system had simply become:

```text
IFS = 100%
everything else = 0%
```

It had not.

### Why we built it

The script answers:

> “Is our adaptive blender actually adapting, or is it secretly just an IFS selector?”

For the current prototype, it provides evidence that the model is doing more than simply selecting IFS every time.

---

## 4. `evaluate_precipitation.py`

### Purpose
This is the main **precipitation evaluation script**.

Unlike temperature, precipitation uses a **Tweedie XGBoost predictor** rather than the temperature inverse-error weighting system.

### Models compared

It evaluates:

- IFS
- GFS
- AIFS
- HGEFS
- Equal-weight blend
- Tweedie XGBoost

### Continuous metrics

It calculates:

- MAE
- RMSE

Current recorded results:

| Method | MAE (mm/h) | RMSE (mm/h) |
|---|---:|---:|
| IFS | 0.134 | 0.425 |
| GFS | 0.236 | 0.738 |
| AIFS | 0.245 | 0.662 |
| HGEFS | 0.210 | 0.700 |
| Equal-weight blend | 0.175 | 0.588 |
| Tweedie XGBoost | 0.139 | 0.471 |

### Event-based evaluation

Because rainfall is highly skewed and contains many zero values, the script also evaluates rainfall events using thresholds:

```text
≥ 0.1 mm/h
≥ 2.5 mm/h
≥ 15.6 mm/h
```

It calculates contingency-table metrics such as:

- POD — Probability of Detection
- FAR — False Alarm Ratio
- CSI — Critical Success Index
- ETS — Equitable Threat Score

### Important interpretation

The Tweedie model improves over the equal-weight blend and produces fewer false alarms, but it does **not** beat IFS on every precipitation metric.

The highest threshold has very few events in the current dataset, so conclusions about extreme rainfall performance must remain cautious.

---

## 5. `test_live_pipeline.py`

### Purpose
This is the **end-to-end live system test**.

While the evaluation scripts use historical data, this script checks whether the actual live pipeline works from beginning to end.

### Pipeline

```text
Open-Meteo
    ↓
Fetch forecasts for the 4 models
    ↓
Merge common timestamps
    ↓
Adaptive temperature prediction
    ↓
Tweedie precipitation prediction
    ↓
Hybrid forecast JSON
```

### Models fetched

- ECMWF IFS
- NCEP GFS
- ECMWF AIFS
- NCEP HGEFS

### Prototype location

The current test uses:

```text
Thiruvananthapuram
Latitude:  8.5241
Longitude: 76.9366
```

### What it displays

For the first forecast timestamp, it shows:

- Time
- Hybrid temperature
- Temperature model weights
- Hybrid precipitation
- Individual precipitation forecasts

### What it verifies

This answers:

> “Can we actually connect to the weather APIs, feed the returned forecasts into our trained models, and get a usable hybrid forecast?”

This is different from `test_predict.py`, which tests inference using the historical processed dataset.

---

# 6. How the scripts differ

The easiest way to remember them:

| Script | Main job |
|---|---|
| `test_predict.py` | **Does inference work?** |
| `evaluate_adaptive.py` | **How accurate is adaptive temperature blending?** |
| `diagnose_temperature_weights.py` | **Are the temperature weights actually adapting?** |
| `evaluate_precipitation.py` | **How accurate is the precipitation model?** |
| `test_live_pipeline.py` | **Does the entire live pipeline work end-to-end?** |

---

# 7. Historical vs Live Testing

There are two broad categories.

## Historical evaluation

These use the processed historical dataset and the ERA5 reference:

```text
evaluate_adaptive.py
evaluate_precipitation.py
diagnose_temperature_weights.py
```

They answer questions about **model quality and behavior**.

## Pipeline/inference tests

These test whether the software itself works:

```text
test_predict.py
test_live_pipeline.py
```

They answer questions about **implementation correctness and integration**.

---

# 8. What should NOT be presented as production components

These scripts are supporting tools.

The actual forecasting pipeline is:

```text
fetch_weather.py
       ↓
predict.py
       ↓
forecast_engine.py
```

The evaluation/test scripts are there to prove and inspect that pipeline.

So during the SIH presentation, the clean story is:

```text
Historical data
      ↓
Model evaluation
      ↓
Baseline comparison
      ↓
Adaptive ML development
      ↓
Validation
      ↓
Live multi-model ingestion
      ↓
Hybrid forecast engine
      ↓
API / Dashboard
```

The diagnostic and evaluation scripts provide the evidence behind the ML claims; they are not separate forecasting systems.
