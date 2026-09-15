import { useWeather } from "../context/WeatherContext";
import {
  Map,
  CloudRain,
  Wind,
  Thermometer,
  AlertTriangle,
} from "lucide-react";

const RAIN_THRESHOLD = 40;
const WIND_THRESHOLD = 40;
const HEAT_THRESHOLD = 35;

function getRisk(value, threshold) {
  if (value >= threshold) return "HIGH";
  if (value >= threshold * 0.5) return "MODERATE";
  return "LOW";
}

function RiskMap() {
 const { forecast, loading, error } = useWeather();

  if (error) {
    return (
      <div className="placeholder">
        <Map size={48} />
        <h2>Risk Map</h2>
        <p>{error}</p>
      </div>
    );
  }

  if (loading || !forecast) {
    return (
      <div className="placeholder">
        <Map size={48} />
        <h2>Risk Map</h2>
        <p>Loading live risk data...</p>
      </div>
    );
  }

  const forecasts = forecast.forecast;

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

  const rainRisk = getRisk(
    maxRain,
    RAIN_THRESHOLD
  );

  const windRisk = getRisk(
    maxWind,
    WIND_THRESHOLD
  );

  const heatRisk = getRisk(
    maxTemp,
    HEAT_THRESHOLD
  );

  const risks = [
    {
      label: "Rain",
      value: `${maxRain.toFixed(1)} mm/h`,
      risk: rainRisk,
      icon: CloudRain,
    },
    {
      label: "Wind",
      value: `${maxWind.toFixed(1)} km/h`,
      risk: windRisk,
      icon: Wind,
    },
    {
      label: "Temperature",
      value: `${maxTemp.toFixed(1)}°C`,
      risk: heatRisk,
      icon: Thermometer,
    },
  ];

  const highRiskCount = risks.filter(
    (item) => item.risk === "HIGH"
  ).length;

  return (
    <div className="page">

      <div className="risk-map-header">
        <div>
          <span className="eyebrow">
            LIVE SPATIAL PROTOTYPE
          </span>

          <h2>Thiruvananthapuram Risk Map</h2>

          <p>
            Current prototype location using the
            hybrid forecast system.
          </p>
        </div>

        <div className="risk-map-status">
  <span>●</span> Live
</div>
      </div>

      <div className="risk-map-container">

        <div className="risk-map-center">

          <div className="location-marker">
            <Map size={28} />
          </div>

          <strong>
            Thiruvananthapuram
          </strong>

          <span>
            8.5241°N · 76.9366°E
          </span>

        </div>

      </div>

      <div className="risk-summary-grid">

        {risks.map((item) => {
          const Icon = item.icon;

          return (
            <div
              className={`risk-summary-card ${item.risk.toLowerCase()}`}
              key={item.label}
            >
              <Icon size={20} />

              <div>
                <span>{item.label}</span>
                <strong>{item.value}</strong>
              </div>

              <b>
                {item.risk}
              </b>
            </div>
          );
        })}

      </div>

      <div className="risk-map-assessment">

        <AlertTriangle size={22} />

        <div>
          <strong>
            {highRiskCount > 0
              ? `${highRiskCount} high-risk condition detected`
              : "No high-risk conditions detected"}
          </strong>

          <p>
            Risk assessment is calculated from the
            72-hour hybrid forecast.
          </p>
        </div>

      </div>

    </div>
  );
}

export default RiskMap;