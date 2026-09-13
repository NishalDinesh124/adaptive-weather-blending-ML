import {
  LayoutDashboard,
  Map,
  Brain,
  BarChart3,
  Layers,
  TriangleAlert,
} from "lucide-react";

const navItems = [
  { id: "overview",     label: "Overview",          icon: LayoutDashboard },
  { id: "risk",         label: "Kerala Risk Map",    icon: Map },
  { id: "fusion",       label: "AI Forecast Fusion", icon: Brain },
  { id: "performance",  label: "Model Performance",  icon: BarChart3 },
  { id: "weights",      label: "Weight Maps",        icon: Layers },
  { id: "extreme",      label: "Extreme Weather",    icon: TriangleAlert },
];

function Sidebar({ activePage, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">
          <Brain size={20} />
        </div>

        <div>
          <h1>Weather AI</h1>
          <p>Hybrid AI-NWP System</p>
        </div>
      </div>

      <div className="sidebar-section-label">Navigation</div>

      <nav>
        {navItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.id}
              className={`nav-item ${activePage === item.id ? "active" : ""}`}
              onClick={() => onNavigate(item.id)}
            >
              <Icon size={17} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-status">
        <div className="status-dot-wrapper">
          <div className="status-dot-ring" />
          <div className="status-dot" />
        </div>

        <div>
          <strong>System Operational</strong>
          <span>Data / Model Status</span>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;