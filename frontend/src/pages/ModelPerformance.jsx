import { TrendingDown, Thermometer, CloudRain } from "lucide-react";
import Card from "../components/common/Card";
import { mockPerformance } from "../data/mockData";

// Best score per category (lowest MAE = best)
const bestTemp = "IFS";
const bestPrecip = "IFS";

function ScoreBadge({ value, isBest }) {
  if (value === null) return <span className="score-badge mid">Pending</span>;
  if (isBest) return <span className="score-badge good">★ {value.toFixed(3)}</span>;
  if (value > 0.8) return <span className="score-badge poor">{value.toFixed(3)}</span>;
  return <span className="score-badge mid">{value.toFixed(3)}</span>;
}

function ModelList({ data, unit, best }) {
  return (
    <div className="performance-list">
      {Object.entries(data).map(([model, value]) => {
        const label = model === "adaptive" ? "AI Adaptive" : model;
        const isBest = model === best && value !== null;

        return (
          <div className={`performance-row ${isBest ? "best-row" : ""}`} key={model}>
            <span>{label}</span>
            <ScoreBadge value={value} isBest={isBest} />
          </div>
        );
      })}
    </div>
  );
}

function ModelPerformance() {
  const temperature = mockPerformance.temperature;
  const precipitation = mockPerformance.precipitation;

  return (
    <div className="page">
      <div className="page-heading">
        <div>
          <h2>Model Performance</h2>
          <p>Historical forecast accuracy against ERA5 reference data</p>
        </div>
      </div>

      <div className="performance-grid">
        <Card title="Temperature — MAE">
          <div className="performance-header">
            <Thermometer size={18} />
            <span>Mean Absolute Error (°C)</span>
          </div>
          <ModelList data={temperature} unit="°C" best={bestTemp} />
        </Card>

        <Card title="Precipitation — MAE">
          <div className="performance-header">
            <CloudRain size={18} />
            <span>Mean Absolute Error (mm)</span>
          </div>
          <ModelList data={precipitation} unit="mm" best={bestPrecip} />
        </Card>
      </div>

      <Card title="Adaptive Blending Improvement">
        <div className="improvement-box">
          <TrendingDown size={28} />
          <div>
            <span>Current status</span>
            <strong>Adaptive blend evaluation pending</strong>
            <p>
              Replace this with the final test-set improvement once the
              adaptive model evaluation is complete.
            </p>
          </div>
        </div>
      </Card>

      <Card title="What the Metrics Mean">
        <div className="metric-explanation">
          <div>
            <strong>MAE</strong>
            <p>
              Average absolute difference between the forecast and ERA5.
              Lower is better.
            </p>
          </div>

          <div>
            <strong>RMSE</strong>
            <p>
              Penalizes larger forecast errors more heavily. Lower is better.
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}

export default ModelPerformance;