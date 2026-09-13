import { useState } from "react";

import Sidebar from "./components/layout/Sidebar";
import Topbar from "./components/layout/TopBar";

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
  },

  performance: {
    title: "Model Performance",
    description: "Forecast accuracy and comparison",
    component: ModelPerformance,
  },

  weights: {
    title: "Weight Maps",
    description: "Adaptive model weight analysis",
    component: WeightMaps,
  },

  extreme: {
    title: "Extreme Weather",
    description: "Extreme weather detection and guidance",
    component: ExtremeWeather,
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
        />

        <div className="content">
          <PageComponent />
        </div>
      </main>
    </div>
  );
}

export default App;