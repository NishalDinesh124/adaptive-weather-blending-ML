import {
  AlertTriangle,
  CloudRain,
  Wind,
  Thermometer,
} from "lucide-react";
import Card from "../components/common/Card";

const risks = [
  {
    title: "Heavy Rain",
    level: "HIGH",
    levelClass: "high",
    value: "42 mm",
    description: "Elevated rainfall expected in the forecast period.",
    icon: CloudRain,
  },
  {
    title: "Strong Wind",
    level: "MODERATE",
    levelClass: "moderate",
    value: "18 km/h",
    description: "Wind conditions currently below severe thresholds.",
    icon: Wind,
  },
  {
    title: "Heat Risk",
    level: "LOW",
    levelClass: "low",
    value: "29.4°",
    description: "Temperature remains within normal range.",
    icon: Thermometer,
  },
];

function ExtremeWeather() {
  return (
    <div className="page">
      <div className="risk-grid">
        {risks.map((risk) => {
          const Icon = risk.icon;
          return (
            <Card key={risk.title} className={`risk-card-glow ${risk.levelClass}`}>
              <div className="risk-card">
                <div className={`risk-icon ${risk.levelClass}`}>
                  <Icon size={20} />
                </div>

                <div className="risk-card-header">
                  <span>{risk.title}</span>
                  <span className={`risk-level-pill ${risk.levelClass}`}>
                    {risk.level}
                  </span>
                </div>

                <div className="risk-value">{risk.value}</div>

                <p>{risk.description}</p>
              </div>
            </Card>
          );
        })}
      </div>

      <Card title="Extreme Weather Assessment">
        <div className="assessment">
          <AlertTriangle size={22} />
          <div>
            <strong>Heavy rainfall requires attention</strong>
            <p>
              The adaptive forecast currently indicates elevated precipitation.
              Risk thresholds can be configured for rainfall, wind and temperature extremes.
            </p>
          </div>
        </div>
      </Card>

      <Card title="Risk Thresholds">
        <div className="threshold-list">
          <div>
            <span>Heavy Rain</span>
            <strong>&gt; 40 mm</strong>
          </div>
          <div>
            <span>Strong Wind</span>
            <strong>&gt; 40 km/h</strong>
          </div>
          <div>
            <span>Heat Risk</span>
            <strong>&gt; 35°C</strong>
          </div>
        </div>
      </Card>
    </div>
  );
}

export default ExtremeWeather;