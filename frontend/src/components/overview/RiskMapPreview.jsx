import { Map } from "lucide-react";
import Card from "../common/Card";

function RiskMapPreview({ forecast }) {
  const data = forecast?.forecast || [];

  const maxRain = data.length
    ? Math.max(...data.map((item) => item.precipitation.hybrid))
    : 0;

  const maxWind = data.length
    ? Math.max(...data.map((item) => item.wind.maximum))
    : 0;

  const maxTemp = data.length
    ? Math.max(...data.map((item) => item.temperature.hybrid))
    : 0;

  const highRisk =
    maxRain > 40 ||
    maxWind > 40 ||
    maxTemp > 35;

  return (
    <Card title="Kerala District Risk">
      <div className="map-placeholder">
        <Map size={42} />

        <span>
          Thiruvananthapuram · {highRisk ? "High Risk" : "Monitoring"}
        </span>

        <small>
          72-hour hybrid forecast risk assessment
        </small>
      </div>
    </Card>
  );
}

export default RiskMapPreview;