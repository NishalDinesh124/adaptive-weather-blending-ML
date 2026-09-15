import { useEffect, useState } from "react";
import { Map, Layers, Info } from "lucide-react";
import Card from "../components/common/Card";

const API_URL = import.meta.env.VITE_API_URL;

const models = [
  {
    name: "ECMWF IFS",
    key: "ifs",
    type: "NWP",
    color: "var(--m-ifs)",
  },
  {
    name: "NCEP GFS",
    key: "gfs",
    type: "NWP",
    color: "var(--m-gfs)",
  },
  {
    name: "ECMWF AIFS",
    key: "aifs",
    type: "AI",
    color: "var(--m-aifs)",
  },
  {
    name: "NCEP HGEFS",
    key: "hgefs",
    type: "Ensemble",
    color: "var(--m-hgefs)",
  },
];

function WeightMaps() {
  const [forecast, setForecast] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/forecast`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch forecast");
        }

        return response.json();
      })
      .then((data) => {
        setForecast(data);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load live model weights");
      });
  }, []);

  if (error) {
    return (
      <div className="page">
        <Card title="Current Weight Distribution">
          <p>{error}</p>
        </Card>
      </div>
    );
  }

  if (!forecast) {
    return (
      <div className="page">
        <Card title="Current Weight Distribution">
          <p>Loading live model weights...</p>
        </Card>
      </div>
    );
  }

  const current = forecast.forecast[0];

  const weights = current.temperature.weights;

  return (
    <div className="page">

      <Card title="Current Weight Distribution">

        <div className="weight-map-layout">

          {/* Location profile */}
          <div className="map-placeholder">

            <Map size={36} />

            <strong
              style={{
                color: "var(--l2)",
                fontSize: "13px",
              }}
            >
              Thiruvananthapuram Weight Profile
            </strong>

            <span>
              Live model influence at the current
              prototype location.
            </span>

            <div className="map-location">
              ● Thiruvananthapuram
            </div>

          </div>

          {/* Legend */}
          <div className="map-legend">

            <h3>Model Influence</h3>

            {models.map((model) => {

              const weight =
                weights[model.key] * 100;

              return (
                <div
                  className="legend-item"
                  key={model.key}
                >

                  <div className="legend-top">

                    <span
                      style={{
                        color: model.color,
                      }}
                    >
                      {model.name}
                    </span>

                    <strong>
                      {weight.toFixed(1)}%
                    </strong>

                  </div>

                  <div className="legend-bar">

                    <div
                      style={{
                        width: `${weight}%`,
                        background: model.color,
                      }}
                    />

                  </div>

                  <small>
                    {model.type}
                  </small>

                </div>
              );
            })}

          </div>
        </div>
      </Card>

      <div className="weight-info-grid">

        <Card title="How Weighting Works">

          <div className="info-content">

            <Layers size={20} />

            <p>
              The system estimates the expected error of
              each forecast model and assigns greater
              influence to models expected to perform
              better under the current conditions.
            </p>

          </div>

        </Card>

        <Card title="Current Resolution">

          <div className="info-content">

            <Info size={20} />

            <div>

              <strong>
                Point-based prototype
              </strong>

              <p>
                Current experiment uses a single
                location. The same weighting system can
                later be applied independently across a
                geographic grid.
              </p>

            </div>

          </div>

        </Card>

      </div>

    </div>
  );
}

export default WeightMaps;