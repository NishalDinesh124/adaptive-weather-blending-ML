import { AlertCircle, AlertTriangle, CheckCircle2 } from "lucide-react";
import Card from "../common/Card";

function AlertsCard({ forecast, loading, error }) {
  if (loading) {
    return (
      <Card title="Extreme Weather Alerts">
        <div className="alerts">
          <div className="alert">
            <div>Loading live risk assessment...</div>
          </div>
        </div>
      </Card>
    );
  }

  if (error || !forecast?.forecast) {
    return (
      <Card title="Extreme Weather Alerts">
        <div className="alerts">
          <div className="alert">
            <div>Unable to load risk data</div>
          </div>
        </div>
      </Card>
    );
  }

  const data = forecast.forecast;

  const maxRain = Math.max(
    ...data.map((item) => item.precipitation.hybrid)
  );

  const maxWind = Math.max(
    ...data.map((item) => item.wind.maximum)
  );

  const maxTemp = Math.max(
    ...data.map((item) => item.temperature.hybrid)
  );

  const alerts = [
    {
      title: "Heavy Rain",
      level: maxRain > 40 ? "High" : maxRain > 15 ? "Moderate" : "Low",
      type: maxRain > 40 ? "danger" : maxRain > 15 ? "warning" : "safe",
      icon: maxRain > 40 ? AlertCircle : maxRain > 15 ? AlertTriangle : CheckCircle2,
    },
    {
      title: "High Wind",
      level: maxWind > 40 ? "High" : maxWind > 25 ? "Moderate" : "Low",
      type: maxWind > 40 ? "danger" : maxWind > 25 ? "warning" : "safe",
      icon: maxWind > 40 ? AlertCircle : maxWind > 25 ? AlertTriangle : CheckCircle2,
    },
    {
      title: "Heatwave",
      level: maxTemp > 35 ? "High" : maxTemp > 32 ? "Moderate" : "Low",
      type: maxTemp > 35 ? "danger" : maxTemp > 32 ? "warning" : "safe",
      icon: maxTemp > 35 ? AlertCircle : maxTemp > 32 ? AlertTriangle : CheckCircle2,
    },
  ];

  return (
    <Card title="Extreme Weather Alerts">
      <div className="alerts">
        {alerts.map((alert) => {
          const Icon = alert.icon;

          return (
            <div className={`alert ${alert.type}`} key={alert.title}>
              <div className="alert-icon">
                <Icon size={14} />
              </div>

              <div>
                <strong>{alert.title}</strong>
                <span>{alert.level} risk</span>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}

export default AlertsCard;