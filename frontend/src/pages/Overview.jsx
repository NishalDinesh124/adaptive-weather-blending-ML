import { useEffect, useState } from "react";
import { CloudRain, Thermometer, Wind } from "lucide-react";

import Card from "../components/common/Card";
import Metric from "../components/common/Metric";

import WeatherCard from "../components/overview/Weathercard";
import AlertsCard from "../components/overview/AlertsCard";
import RiskMapPreview from "../components/overview/RiskMapPreview";

function Overview() {
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
  fetch(`${import.meta.env.VITE_API_URL}/forecast`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch forecast");
      }

      return response.json();
    })
    .then((data) => {
      setForecast(data);
      setLoading(false);
    })
    .catch((err) => {
      console.error(err);
      setError("Unable to load live forecast");
      setLoading(false);
    });
}, []);

  const firstForecast = forecast?.forecast?.[0];

  return (
    <>
      <section className="hero-grid">
        <WeatherCard />
        <AlertsCard />
      </section>

      <section className="dashboard-grid">
        <RiskMapPreview />

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
              value="--"
              confidence="Live"
            />

          </div>

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

        </Card>
      </section>
    </>
  );
}

export default Overview;