import { useWeather } from "../context/WeatherContext";
import { Brain, CloudRain, Thermometer, Zap } from "lucide-react";
import Card from "../components/common/Card";



const models = [
  {
    name: "ECMWF IFS",
    key: "ifs",
    type: "NWP",
    cls: "model-ifs",
    color: "var(--m-ifs)",
  },
  {
    name: "NCEP GFS",
    key: "gfs",
    type: "NWP",
    cls: "model-gfs",
    color: "var(--m-gfs)",
  },
  {
    name: "ECMWF AIFS",
    key: "aifs",
    type: "AI",
    cls: "model-aifs",
    color: "var(--m-aifs)",
  },
  {
    name: "NCEP HGEFS",
    key: "hgefs",
    type: "Ensemble",
    cls: "model-hgefs",
    color: "var(--m-hgefs)",
  },
];

function ForecastFusion() {
  const { forecast, loading, error } = useWeather();

  const current = forecast?.forecast?.[0];

  if (loading) {
    return (
      <div className="page">
        <Card title="AI Forecast Fusion">
          <p>Loading live forecast...</p>
        </Card>
      </div>
    );
  }

  if (error || !current) {
    return (
      <div className="page">
        <Card title="AI Forecast Fusion">
          <p>{error || "No forecast data available."}</p>
        </Card>
      </div>
    );
  }

  const weights = current.temperature.weights;
  const temperatureSources = current.temperature.sources;
  const precipitationSources = current.precipitation.sources;

  return (
    <div className="page">

      {/* Dynamic Model Weights */}
      <Card title="Dynamic Model Weights" action="Current conditions">
        <div className="weight-list">
          {models.map((model) => {
            const weight = weights[model.key] * 100;

            return (
              <div className="weight-row" key={model.key}>

                <div className="weight-info">
                  <div className={`model-name ${model.cls}`}>
                    <span
                      className="model-dot"
                      style={{ background: model.color }}
                    />
                    {model.name}
                  </div>

                  <span className="model-type">
                    {model.type}
                  </span>
                </div>

                <div className="weight-bar-container">
                  <div
                    className="weight-bar"
                    style={{
                      width: `${weight}%`,
                      background: model.color,
                    }}
                  />
                </div>

                <strong>
                  {weight.toFixed(1)}%
                </strong>

              </div>
            );
          })}
        </div>
      </Card>

      {/* Fusion Pipeline */}
      <Card title="Fusion Pipeline">
        <div className="fusion-flow">

          <div className="fusion-node">
            <CloudRain size={22} />
            <strong>4 Forecast Models</strong>
            <span>IFS · GFS · AIFS · HGEFS</span>
          </div>

          <div className="flow-arrow">›</div>

          <div className="fusion-node highlight">
            <Brain size={22} />
            <strong>XGBoost</strong>
            <span>Predict model error</span>
          </div>

          <div className="flow-arrow">›</div>

          <div className="fusion-node">
            <Zap size={22} />
            <strong>Dynamic Weights</strong>
            <span>Adaptive trust scores</span>
          </div>

          <div className="flow-arrow">›</div>

          <div className="fusion-node success">
            <Brain size={22} />
            <strong>Blended Forecast</strong>
            <span>Optimized prediction</span>
          </div>

        </div>
      </Card>

      {/* Forecast comparison */}
      <div className="fusion-grid">

        {/* Temperature */}
        <Card title="Temperature Forecast">

          <div className="forecast-result">
            <Thermometer size={22} />

            <div>
              <span>AI Blended Forecast</span>

              <strong>
                {current.temperature.hybrid.toFixed(1)}°
              </strong>
            </div>
          </div>

          <div className="mini-model-list">

            {models.map((model) => (
              <div key={model.key}>
                <span>{model.key.toUpperCase()}</span>

                <b>
                  {temperatureSources[model.key].toFixed(1)}°C
                </b>
              </div>
            ))}

          </div>
        </Card>

        {/* Rainfall */}
        <Card title="Rainfall Forecast">

          <div className="forecast-result">
            <CloudRain size={22} />

            <div>
              <span>AI Blended Forecast</span>

              <strong>
                {current.precipitation.hybrid.toFixed(2)} mm
              </strong>
            </div>
          </div>

          <div className="mini-model-list">

            {models.map((model) => (
              <div key={model.key}>
                <span>{model.key.toUpperCase()}</span>

                <b>
                  {precipitationSources[model.key].toFixed(2)} mm
                </b>
              </div>
            ))}

          </div>
        </Card>

      </div>

      {/* Why These Weights */}
      <Card title="Why These Weights?">

        <div className="explanation">
          <Brain size={20} />

          <p>
            The XGBoost error models estimate how accurate each forecast
            source is likely to be under the current conditions. Models
            expected to have lower error receive higher weights.
          </p>
        </div>

      </Card>

    </div>
  );
}

export default ForecastFusion;