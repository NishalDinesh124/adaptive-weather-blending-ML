import { CloudRain, Thermometer, Wind } from "lucide-react";

import Card from "../components/common/Card";
import Metric from "../components/common/Metric";

import WeatherCard from "../components/overview/Weathercard";
import AlertsCard from "../components/overview/AlertsCard";
import RiskMapPreview from "../components/overview/RiskMapPreview";

function Overview() {
  return (
    <>
      <section className="hero-grid">
        <WeatherCard />
        <AlertsCard />
      </section>

      <section className="dashboard-grid">
        <RiskMapPreview />

        <Card title="AI Blended Forecast">
          {/* Metrics are flush — no wrapper padding */}
          <div className="forecast-grid">
            <Metric icon={CloudRain}   label="Precipitation" value="42 mm"  confidence="91%" />
            <Metric icon={Thermometer} label="Temperature"   value="29.4°"  confidence="94%" />
            <Metric icon={Wind}        label="Wind"          value="18 km/h" confidence="88%" />
          </div>
        </Card>
      </section>
    </>
  );
}

export default Overview;