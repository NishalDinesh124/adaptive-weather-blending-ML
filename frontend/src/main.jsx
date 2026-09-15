import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { WeatherProvider } from "./context/WeatherContext.jsx";
import { PerformanceProvider } from "./context/PerformanceContext.jsx";
createRoot(document.getElementById("root")).render(
  <StrictMode>
    <WeatherProvider>
      <PerformanceProvider>
        <App />
      </PerformanceProvider>
      
    </WeatherProvider>
  </StrictMode>,
);
