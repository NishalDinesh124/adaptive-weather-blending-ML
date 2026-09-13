import { MapPin } from "lucide-react";
import StatusDot from "../common/StatusDot";

function Topbar({ title, description, badge }) {
  return (
    <header className="topbar">
      <div className="topbar-left">
        <h2>{title}</h2>
        <p>{description}</p>
      </div>

      <div className="topbar-right">
        {badge && badge}

        <div className="topbar-location">
          <MapPin size={11} />
          Thiruvananthapuram, Kerala
        </div>

        <StatusDot />
      </div>
    </header>
  );
}

export default Topbar;