import { useState } from "react";
import { Zap, ShieldAlert } from "lucide-react";

import Sidebar from "./components/layout/Sidebar";
import Topbar from "./components/layout/Topbar";

import Overview from "./pages/Overview";
import RiskMap from "./pages/RiskMap";
import ForecastFusion from "./pages/ForecastFusion";
import ModelPerformance from "./pages/ModelPerformance";
import WeightMaps from "./pages/WeightMaps";
import ExtremeWeather from "./pages/ExtremeWeather";

import "./App.css";

const pages = {
  overview: {
    title: "Overview",
    description: "Adaptive multi-model weather forecasting",
    component: Overview,
  },

  risk: {
    title: "Kerala Risk Map",
    description: "Spatial weather risk analysis",
    component: RiskMap,
  },

  fusion: {
    title: "AI Forecast Fusion",
    description: "Dynamic multi-model forecast blending",
    component: ForecastFusion,
    badge: (
      <div className="live-badge">
        <Zap size={12} />
        Adaptive Mode
      </div>
    ),
  },

  performance: {
    title: "Model Performance",
    description: "Forecast accuracy against ERA5 reference data",
    component: ModelPerformance,
  },

  weights: {
    title: "Weight Maps",
    description: "Adaptive model weight analysis",
    component: WeightMaps,
  },

  extreme: {
    title: "Extreme Weather",
    description: "Risk indicators from the blended forecast",
    component: ExtremeWeather,
    badge: (
      <div className="risk-status">
        <ShieldAlert size={13} />
        Monitoring
      </div>
    ),
  },
};

function App() {
  const [activePage, setActivePage] = useState("overview");

  const page = pages[activePage];
  const PageComponent = page.component;

  return (
    <div className="app">
      <Sidebar
        activePage={activePage}
        onNavigate={setActivePage}
      />

      <main className="main">
        <Topbar
          title={page.title}
          description={page.description}
          badge={page.badge}
        />

        <div className="content">
          <PageComponent />
        </div>
      </main>
    </div>
  );
}

export default App;