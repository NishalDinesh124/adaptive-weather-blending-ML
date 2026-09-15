import { useWeather } from "../context/WeatherContext";
import { CloudRain, Thermometer, Wind } from "lucide-react";

import Card from "../components/common/Card";
import Metric from "../components/common/Metric";

import WeatherCard from "../components/overview/Weathercard";
import AlertsCard from "../components/overview/AlertsCard";
import RiskMapPreview from "../components/overview/RiskMapPreview";

function Overview() {
  const { forecast, loading, error } = useWeather();

  const firstForecast = forecast?.forecast?.[0];

  return (
    <>
      <section className="hero-grid">
        <WeatherCard
  forecast={forecast}
  loading={loading}
  error={error}
/>

        <AlertsCard forecast={forecast} loading={loading} error={error} />
      </section>

      <section className="dashboard-grid">
        <RiskMapPreview forecast={forecast} />

        <Card title="AI Blended Forecast">
          <div className="forecast-grid">
            <Metric
              icon={CloudRain}
              label="Precipitation"
              value={
                loading
                  ? "Loading..."
                  : error
                    ? "--"
                    : `${firstForecast.precipitation.hybrid.toFixed(2)} mm`
              }
              confidence="AI"
            />

            <Metric
              icon={Thermometer}
              label="Temperature"
              value={
                loading
                  ? "Loading..."
                  : error
                    ? "--"
                    : `${firstForecast.temperature.hybrid.toFixed(1)}°`
              }
              confidence="AI"
            />

            <Metric
              icon={Wind}
              label="Wind"
              value={
                loading
                  ? "Loading..."
                  : error
                    ? "--"
                    : `${firstForecast.wind.maximum.toFixed(1)} km/h`
              }
              confidence="Live"
            />
          </div>

          {error && <p className="error-message">{error}</p>}
        </Card>
      </section>
    </>
  );
}

export default Overview;
