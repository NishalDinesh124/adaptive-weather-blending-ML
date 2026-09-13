import { AlertCircle, AlertTriangle, CheckCircle2 } from "lucide-react";
import Card from "../common/Card";

const alerts = [
  {
    type: "danger",
    title: "Heavy Rain",
    level: "High",
    icon: AlertCircle,
  },
  {
    type: "warning",
    title: "High Wind",
    level: "Moderate",
    icon: AlertTriangle,
  },
  {
    type: "safe",
    title: "Heatwave",
    level: "Low",
    icon: CheckCircle2,
  },
];

function AlertsCard() {
  return (
    <Card title="Extreme Weather Alerts">
      <div className="alerts">
        {alerts.map((alert) => {
          const Icon = alert.icon;

          return (
            <div
              className={`alert ${alert.type}`}
              key={alert.title}
            >
              <div className="alert-icon">
                <Icon size={15} />
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