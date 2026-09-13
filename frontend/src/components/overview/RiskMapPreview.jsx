import { Map } from "lucide-react";
import Card from "../common/Card";

function RiskMapPreview() {
  return (
    <Card title="Kerala District Risk">
      <div className="map-placeholder">
        <Map size={42} />

        <span>Kerala risk map</span>

        <small>
          Spatial model visualization
        </small>
      </div>
    </Card>
  );
}

export default RiskMapPreview;