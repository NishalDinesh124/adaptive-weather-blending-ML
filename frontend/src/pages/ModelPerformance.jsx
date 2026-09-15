import { usePerformance } from "../context/PerformanceContext";
import { TrendingDown, Thermometer, CloudRain } from "lucide-react";
import Card from "../components/common/Card";

function ScoreBadge({ value, isBest }) {
  if (value === undefined || value === null) {
    return <span className="score-badge mid">Pending</span>;
  }

  return (
    <span className={`score-badge ${isBest ? "good" : "mid"}`}>
      {isBest ? "★ " : ""}
      {value.toFixed(3)}
    </span>
  );
}

function ModelList({ data, metric }) {
  const entries = Object.entries(data);

  const bestValue = Math.min(
    ...entries.map(([, value]) => value[metric])
  );

  return (
    <div className="performance-list">
      {entries.map(([model, value]) => {
        const label =
          model === "adaptive"
            ? "AI Adaptive"
            : model === "tweedie"
              ? "XGBoost Tweedie"
              : model === "equal"
                ? "Equal Weight"
                : model;

        const isBest = value[metric] === bestValue;

        return (
          <div
            className={`performance-row ${
              isBest ? "best-row" : ""
            }`}
            key={model}
          >
            <span>{label}</span>

            <ScoreBadge
              value={value[metric]}
              isBest={isBest}
            />
          </div>
        );
      })}
    </div>
  );
}

function ModelPerformance() {
  const {
  performance,
  loading,
  error,
} = usePerformance();

  if (error) {
    return (
      <div className="page">
        <Card title="Model Performance">
          <p>{error}</p>
        </Card>
      </div>
    );
  }

  if (loading || !performance) {
    return (
      <div className="page">
        <Card title="Model Performance">
          <p>Loading evaluation results...</p>
        </Card>
      </div>
    );
  }

  const { temperature, precipitation } = performance;

  const equalTempMae = temperature.equal?.mae;
  const adaptiveTempMae = temperature.adaptive?.mae;

  const equalTempRmse = temperature.equal?.rmse;
  const adaptiveTempRmse = temperature.adaptive?.rmse;

  const maeImprovement =
    equalTempMae && adaptiveTempMae
      ? ((equalTempMae - adaptiveTempMae) / equalTempMae) * 100
      : null;

  const rmseImprovement =
    equalTempRmse && adaptiveTempRmse
      ? ((equalTempRmse - adaptiveTempRmse) / equalTempRmse) * 100
      : null;

  return (
    <div className="page">

      {/* Temperature */}
      <div className="performance-grid">

        <Card title="Temperature — MAE">
          <div className="performance-header">
            <Thermometer size={16} />
            <span>Mean Absolute Error (°C)</span>
          </div>

          <ModelList
            data={temperature}
            metric="mae"
          />
        </Card>

        <Card title="Temperature — RMSE">
          <div className="performance-header">
            <Thermometer size={16} />
            <span>Root Mean Square Error (°C)</span>
          </div>

          <ModelList
            data={temperature}
            metric="rmse"
          />
        </Card>

      </div>

      {/* Precipitation */}
      <div className="performance-grid">

        <Card title="Precipitation — MAE">
          <div className="performance-header">
            <CloudRain size={16} />
            <span>Mean Absolute Error (mm)</span>
          </div>

          <ModelList
            data={precipitation}
            metric="mae"
          />
        </Card>

        <Card title="Precipitation — RMSE">
          <div className="performance-header">
            <CloudRain size={16} />
            <span>Root Mean Square Error (mm)</span>
          </div>

          <ModelList
            data={precipitation}
            metric="rmse"
          />
        </Card>

      </div>

      {/* Improvement */}
      <Card title="Adaptive Blending Improvement">

        <div className="improvement-box">
          <TrendingDown size={26} />

          <div>
            <span>Live evaluation</span>

            {maeImprovement !== null ? (
              <>
                <strong>
                  {maeImprovement.toFixed(1)}% lower MAE
                </strong>

                <p>
                  Adaptive XGBoost blending is being compared
                  against the equal-weight temperature baseline.
                  RMSE improvement: {rmseImprovement.toFixed(1)}%.
                </p>
              </>
            ) : (
              <p>
                Equal-weight comparison is not available.
              </p>
            )}
          </div>

        </div>

      </Card>

      {/* Explanation */}
      <Card title="What the Metrics Mean">

        <div className="metric-explanation">

          <div>
            <strong>MAE</strong>
            <p>
              Average absolute difference between the forecast
              and ERA5. Lower is better.
            </p>
          </div>

          <div>
            <strong>RMSE</strong>
            <p>
              Penalizes larger forecast errors more heavily.
              Lower is better.
            </p>
          </div>

        </div>

      </Card>

    </div>
  );
}

export default ModelPerformance;