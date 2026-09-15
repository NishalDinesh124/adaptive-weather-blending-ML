import { useWeather } from "../context/WeatherContext";
import {
  AlertTriangle,
  CloudRain,
  Wind,
  Thermometer,
} from "lucide-react";

import Card from "../components/common/Card";

const RAIN_THRESHOLD = 40;
const WIND_THRESHOLD = 40;
const HEAT_THRESHOLD = 35;

function getLevel(value, threshold, type = "high") {
  if (value >= threshold) return "HIGH";

  if (type === "wind" && value >= threshold * 0.7) {
    return "MODERATE";
  }

  if (type === "temp" && value >= threshold * 0.9) {
    return "MODERATE";
  }

  if (type === "rain" && value >= threshold * 0.5) {
    return "MODERATE";
  }

  return "LOW";
}

function levelClass(level) {
  return level.toLowerCase();
}

function ExtremeWeather() {
  const { forecast, loading, error } = useWeather();

  if (error) {
    return (
      <div className="page">
        <Card title="Extreme Weather Assessment">
          <p>{error}</p>
        </Card>
      </div>
    );
  }

  if (loading || !forecast) {
    return (
      <div className="page">
        <Card title="Extreme Weather Assessment">
          <p>Loading live weather assessment...</p>
        </Card>
      </div>
    );
  }

  const forecasts = forecast.forecast;

  // Use the maximum hybrid rainfall/temperature
  // across the available forecast period.
  const maxRain = Math.max(
    ...forecasts.map(
      (item) => item.precipitation.hybrid
    )
  );

    const maxTemp = Math.max(
    ...forecasts.map(
      (item) => item.temperature.hybrid
    )
  );

  const maxWind = Math.max(
    ...forecasts.map(
      (item) => item.wind.maximum
    )
  );

  const rainLevel = getLevel(
    maxRain,
    RAIN_THRESHOLD,
    "rain"
  );

  const heatLevel = getLevel(
    maxTemp,
    HEAT_THRESHOLD,
    "temp"
  );

  const risks = [
    {
      title: "Heavy Rain",
      level: rainLevel,
      levelClass: levelClass(rainLevel),
      value: `${maxRain.toFixed(2)} mm/h`,
      description:
        rainLevel === "HIGH"
          ? "Heavy rainfall threshold exceeded in the forecast."
          : rainLevel === "MODERATE"
            ? "Rainfall is approaching the configured heavy-rain threshold."
            : "No heavy-rain threshold exceedance detected.",
      icon: CloudRain,
    },
        {
      title: "Strong Wind",
      level: getLevel(
        maxWind,
        WIND_THRESHOLD,
        "wind"
      ),
      levelClass: levelClass(
        getLevel(
          maxWind,
          WIND_THRESHOLD,
          "wind"
        )
      ),
      value: `${maxWind.toFixed(1)} km/h`,
      description:
        maxWind >= WIND_THRESHOLD
          ? "At least one forecast source exceeds the configured strong-wind threshold."
          : "Wind conditions remain below the configured strong-wind threshold.",
      icon: Wind,
    },
    {
      title: "Heat Risk",
      level: heatLevel,
      levelClass: levelClass(heatLevel),
      value: `${maxTemp.toFixed(1)}°C`,
      description:
        heatLevel === "HIGH"
          ? "Temperature exceeds the configured heat-risk threshold."
          : heatLevel === "MODERATE"
            ? "Temperature is approaching the configured heat-risk threshold."
            : "Temperature remains below the configured heat-risk threshold.",
      icon: Thermometer,
    },
  ];

  const highRisks = risks.filter(
    (risk) => risk.level === "HIGH"
  );

  return (
    <div className="page">

      {/* Risk cards */}
      <div className="risk-grid">
        {risks.map((risk) => {
          const Icon = risk.icon;

          return (
            <Card
              key={risk.title}
              className={`risk-card-glow ${risk.levelClass}`}
            >
              <div className="risk-card">

                <div
                  className={`risk-icon ${risk.levelClass}`}
                >
                  <Icon size={20} />
                </div>

                <div className="risk-card-header">
                  <span>{risk.title}</span>

                  <span
                    className={`risk-level-pill ${risk.levelClass}`}
                  >
                    {risk.level}
                  </span>
                </div>

                <div className="risk-value">
                  {risk.value}
                </div>

                <p>{risk.description}</p>

              </div>
            </Card>
          );
        })}
      </div>

      {/* Assessment */}
      <Card title="Extreme Weather Assessment">
        <div className="assessment">
          <AlertTriangle size={22} />

          <div>
            <strong>
              {highRisks.length > 0
                ? `${highRisks.length} high-risk condition${
                    highRisks.length > 1 ? "s" : ""
                  } detected`
                : "No high-risk conditions detected"}
            </strong>

            <p>
              Assessment is based on the hybrid forecast
              across the available 72-hour forecast period.
            </p>
          </div>
        </div>
      </Card>

      {/* Thresholds */}
      <Card title="Risk Thresholds">
        <div className="threshold-list">

          <div>
            <span>Heavy Rain</span>
            <strong>&gt; {RAIN_THRESHOLD} mm/h</strong>
          </div>

          <div>
            <span>Strong Wind</span>
            <strong>&gt; {WIND_THRESHOLD} km/h</strong>
          </div>

          <div>
            <span>Heat Risk</span>
            <strong>&gt; {HEAT_THRESHOLD}°C</strong>
          </div>

        </div>
      </Card>

    </div>
  );
}

export default ExtremeWeather;