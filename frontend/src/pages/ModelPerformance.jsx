import { TrendingDown, Thermometer, CloudRain } from "lucide-react";
import Card from "../components/common/Card";
import { mockPerformance } from "../data/mockData";

const bestTemp   = "IFS";
const bestPrecip = "IFS";

function ScoreBadge({ value, isBest }) {
  if (value === null) return <span className="score-badge mid">Pending</span>;
  if (isBest)         return <span className="score-badge good">★ {value.toFixed(3)}</span>;
  if (value > 0.8)    return <span className="score-badge poor">{value.toFixed(3)}</span>;
  return                     <span className="score-badge mid">{value.toFixed(3)}</span>;
}

function ModelList({ data, best }) {
  return (
    <div className="performance-list">
      {Object.entries(data).map(([model, value]) => {
        const label  = model === "adaptive" ? "AI Adaptive" : model;
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
  const { temperature, precipitation } = mockPerformance;

  return (
    <div className="page">
      <div className="performance-grid">
        <Card title="Temperature — MAE">
          <div className="performance-header">
            <Thermometer size={16} />
            <span>Mean Absolute Error (°C)</span>
          </div>
          <ModelList data={temperature} best={bestTemp} />
        </Card>

        <Card title="Precipitation — MAE">
          <div className="performance-header">
            <CloudRain size={16} />
            <span>Mean Absolute Error (mm)</span>
          </div>
          <ModelList data={precipitation} best={bestPrecip} />
        </Card>
      </div>

      <Card title="Adaptive Blending Improvement">
        <div className="improvement-box">
          <TrendingDown size={26} />
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
            <p>Average absolute difference between the forecast and ERA5. Lower is better.</p>
          </div>
          <div>
            <strong>RMSE</strong>
            <p>Penalizes larger forecast errors more heavily. Lower is better.</p>
          </div>
        </div>
      </Card>
    </div>
  );
}

export default ModelPerformance;