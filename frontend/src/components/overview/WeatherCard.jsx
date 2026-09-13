import { CloudRain, Wind, Droplets } from "lucide-react";
import Card from "../common/Card";

function WeatherCard() {
  return (
    <Card title="Current Weather — Kerala">
      {/* Hero: icon + temperature — padded section */}
      <div className="weather-hero">
        <div className="weather-icon-wrap">
          <CloudRain size={24} />
        </div>
        <div>
          <div className="temperature">28.4°</div>
          <div className="condition">Light Rain · Thiruvananthapuram</div>
        </div>
      </div>

      {/* Stat row — 3 columns, full-width, flush to card edges */}
      <div className="weather-stat-row">
        <div className="weather-stat">
          <div className="weather-stat-label">Rainfall</div>
          <div className="weather-stat-value">4.2 mm</div>
        </div>

        <div className="weather-stat">
          <div className="weather-stat-label">Wind</div>
          <div className="weather-stat-value">18 km/h</div>
        </div>

        <div className="weather-stat">
          <div className="weather-stat-label">Humidity</div>
          <div className="weather-stat-value">82%</div>
        </div>
      </div>
    </Card>
  );
}

export default WeatherCard;