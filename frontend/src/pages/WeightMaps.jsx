import { Map, Layers, Info } from "lucide-react";
import Card from "../components/common/Card";
import { mockWeights } from "../data/mockData";

const models = [
  { name: "ECMWF IFS",  key: "IFS",   type: "NWP",      color: "var(--teal)"   },
  { name: "NCEP GFS",   key: "GFS",   type: "NWP",      color: "var(--amber)"  },
  { name: "ECMWF AIFS", key: "AIFS",  type: "AI",       color: "var(--coral)"  },
  { name: "NCEP HGEFS", key: "HGEFS", type: "Ensemble", color: "var(--violet)" },
];

function WeightMaps() {
  return (
    <div className="page">
      <div className="page-heading">
        <div>
          <h2>Model Weight Maps</h2>
          <p>Spatial distribution of adaptive model influence</p>
        </div>
      </div>

      <Card title="Current Weight Distribution">
        <div className="weight-map-layout">

          <div className="map-placeholder">
            <Map size={40} />
            <strong>Kerala Weight Map</strong>
            <span>
              Spatial visualization will be enabled
              when multi-grid forecast data is connected.
            </span>
            <div className="map-location">
              ● Thiruvananthapuram
            </div>
          </div>

          <div className="map-legend">
            <h3>Model Influence</h3>

            {models.map((model) => (
              <div className="legend-item" key={model.key}>
                <div className="legend-top">
                  <span style={{ color: model.color }}>{model.name}</span>
                  <strong style={{ color: model.color }}>{mockWeights[model.key]}%</strong>
                </div>

                <div className="legend-bar">
                  <div
                    style={{
                      width: `${mockWeights[model.key]}%`,
                      background: model.color,
                      opacity: 0.8,
                    }}
                  />
                </div>

                <small>{model.type}</small>
              </div>
            ))}
          </div>

        </div>
      </Card>

      <div className="weight-info-grid">
        <Card title="How Weighting Works">
          <div className="info-content">
            <Layers size={22} />
            <p>
              The system estimates the expected error of each forecast
              model and assigns greater influence to models expected
              to perform better under the current conditions.
            </p>
          </div>
        </Card>

        <Card title="Current Resolution">
          <div className="info-content">
            <Info size={22} />
            <div>
              <strong>Point-based prototype</strong>
              <p>
                Current experiment uses a single location. The same
                weighting system can later be applied independently
                across a geographic grid.
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}

export default WeightMaps;