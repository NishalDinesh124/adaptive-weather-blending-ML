import { Brain, CloudRain, Thermometer, Wind, Zap } from "lucide-react";
import Card from "../components/common/Card";
import { mockWeights } from "../data/mockData";

const models = [
  { name: "ECMWF IFS",  key: "IFS",   type: "NWP",      colorClass: "model-ifs"   },
  { name: "NCEP GFS",   key: "GFS",   type: "NWP",      colorClass: "model-gfs"   },
  { name: "ECMWF AIFS", key: "AIFS",  type: "AI",       colorClass: "model-aifs"  },
  { name: "NCEP HGEFS", key: "HGEFS", type: "Ensemble", colorClass: "model-hgefs" },
];

function ForecastFusion() {
  return (
    <div className="page">
      <div className="page-heading">
        <div>
          <h2>AI Forecast Fusion</h2>
          <p>Dynamic model weighting based on predicted forecast error</p>
        </div>

        <div className="live-badge">
          <Zap size={14} />
          Adaptive Mode
        </div>
      </div>

      {/* Model weights */}
      <Card title="Dynamic Model Weights" action="Current conditions">
        <div className="weight-list">
          {models.map((model) => (
            <div className="weight-row" key={model.key}>
              <div className="weight-info">
                <div className={`model-name ${model.colorClass}`}>
                  <span className="model-dot" />
                  {model.name}
                </div>
                <span className="model-type">{model.type}</span>
              </div>

              <div className="weight-bar-container">
                <div
                  className={`weight-bar ${model.colorClass}`}
                  style={{ width: `${mockWeights[model.key]}%` }}
                />
              </div>

              <strong className={model.colorClass}>{mockWeights[model.key]}%</strong>
            </div>
          ))}
        </div>
      </Card>

      {/* Fusion flow */}
      <Card title="Fusion Pipeline">
        <div className="fusion-flow">
          <div className="fusion-node">
            <CloudRain size={24} />
            <strong>4 Forecast Models</strong>
            <span>IFS · GFS · AIFS · HGEFS</span>
          </div>

          <div className="flow-arrow">→</div>

          <div className="fusion-node highlight">
            <Brain size={24} />
            <strong>XGBoost</strong>
            <span>Predict model error</span>
          </div>

          <div className="flow-arrow">→</div>

          <div className="fusion-node">
            <Zap size={24} />
            <strong>Dynamic Weights</strong>
            <span>Adaptive trust scores</span>
          </div>

          <div className="flow-arrow">→</div>

          <div className="fusion-node success">
            <Brain size={24} />
            <strong>Blended Forecast</strong>
            <span>Optimized prediction</span>
          </div>
        </div>
      </Card>

      {/* Forecast comparison */}
      <div className="fusion-grid">
        <Card title="Temperature Forecast">
          <div className="forecast-result">
            <Thermometer size={26} />
            <div>
              <span>AI Blended Forecast</span>
              <strong>29.4°C</strong>
            </div>
          </div>

          <div className="mini-model-list">
            <div><span>IFS</span><b>29.1°C</b></div>
            <div><span>GFS</span><b>30.2°C</b></div>
            <div><span>AIFS</span><b>29.8°C</b></div>
            <div><span>HGEFS</span><b>29.5°C</b></div>
          </div>
        </Card>

        <Card title="Rainfall Forecast">
          <div className="forecast-result">
            <CloudRain size={26} />
            <div>
              <span>AI Blended Forecast</span>
              <strong>42 mm</strong>
            </div>
          </div>

          <div className="mini-model-list">
            <div><span>IFS</span><b>39 mm</b></div>
            <div><span>GFS</span><b>47 mm</b></div>
            <div><span>AIFS</span><b>44 mm</b></div>
            <div><span>HGEFS</span><b>43 mm</b></div>
          </div>
        </Card>
      </div>

      {/* Explanation */}
      <Card title="Why These Weights?">
        <div className="explanation">
          <Brain size={22} />
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