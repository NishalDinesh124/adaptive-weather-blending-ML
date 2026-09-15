import { CloudRain } from "lucide-react";
import Card from "../common/Card";

function WeatherCard({ forecast, loading, error }) {
  const current = forecast?.forecast?.[0];

  return (
    <Card title="Current Weather — Kerala">
      <div className="weather-hero">
        <div className="weather-icon-wrap">
          <CloudRain size={24} />
        </div>

        <div>
          <div className="temperature">
            {loading
              ? "..."
              : error
                ? "--"
                : `${current.temperature.hybrid.toFixed(1)}°C`}
          </div>

          <div className="condition">
            Hybrid Forecast · Thiruvananthapuram
          </div>
        </div>
      </div>

      <div className="weather-stat-row">
        <div className="weather-stat">
          <div className="weather-stat-label">Rainfall</div>
          <div className="weather-stat-value">
            {loading
              ? "..."
              : error
                ? "--"
                : `${current.precipitation.hybrid.toFixed(2)} mm`}
          </div>
        </div>

        <div className="weather-stat">
          <div className="weather-stat-label">Wind</div>
          <div className="weather-stat-value">
            {loading
              ? "..."
              : error
                ? "--"
                : `${current.wind.maximum.toFixed(1)} km/h`}
          </div>
        </div>

        <div className="weather-stat">
          <div className="weather-stat-label">Forecast Time</div>
          <div className="weather-stat-value">
            {loading
              ? "..."
              : error
                ? "--"
                : new Date(current.time).toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
          </div>
        </div>
      </div>
    </Card>
  );
}

export default WeatherCard;