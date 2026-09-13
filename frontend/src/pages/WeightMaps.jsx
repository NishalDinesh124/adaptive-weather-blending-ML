import { Map, Layers, Info } from "lucide-react";
import Card from "../components/common/Card";
import { mockWeights } from "../data/mockData";

const models = [
  { name: "ECMWF IFS",  key: "IFS",   type: "NWP",      color: "var(--m-ifs)"   },
  { name: "NCEP GFS",   key: "GFS",   type: "NWP",      color: "var(--m-gfs)"   },
  { name: "ECMWF AIFS", key: "AIFS",  type: "AI",       color: "var(--m-aifs)"  },
  { name: "NCEP HGEFS", key: "HGEFS", type: "Ensemble", color: "var(--m-hgefs)" },
];

function WeightMaps() {
  return (
    <div className="page">
      <Card title="Current Weight Distribution">
        <div className="weight-map-layout">
          {/* Map canvas */}
          <div className="map-placeholder">
            <Map size={36} />
            <strong style={{ color: "var(--l2)", fontSize: "13px" }}>Kerala Weight Map</strong>
            <span>
              Spatial visualization will be enabled
              when multi-grid forecast data is connected.
            </span>
            <div className="map-location">● Thiruvananthapuram</div>
          </div>

          {/* Legend — flush rows */}
          <div className="map-legend">
            <h3>Model Influence</h3>
            {models.map((model) => (
              <div className="legend-item" key={model.key}>
                <div className="legend-top">
                  <span style={{ color: model.color }}>{model.name}</span>
                  <strong>{mockWeights[model.key]}%</strong>
                </div>
                <div className="legend-bar">
                  <div
                    style={{
                      width: `${mockWeights[model.key]}%`,
                      background: model.color,
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
            <Layers size={20} />
            <p>
              The system estimates the expected error of each forecast model
              and assigns greater influence to models expected to perform
              better under the current conditions.
            </p>
          </div>
        </Card>

        <Card title="Current Resolution">
          <div className="info-content">
            <Info size={20} />
            <div>
              <strong>Point-based prototype</strong>
              <p>
                Current experiment uses a single location. The same weighting
                system can later be applied independently across a geographic grid.
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}

export default WeightMaps;