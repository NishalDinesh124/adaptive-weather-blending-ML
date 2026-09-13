import { CloudRain, Wind, Droplets } from "lucide-react";
import Card from "../common/Card";

function WeatherCard() {
  return (
    <Card title="Current Weather — Kerala">
      <div className="weather-hero">
        <div className="weather-icon-wrap">
          <CloudRain size={32} />
        </div>

        <div>
          <div className="temperature">28.4°C</div>
          <div className="condition">Light Rain · Thiruvananthapuram</div>
        </div>
      </div>

      <div className="weather-stat-row">
        <div className="weather-stat">
          <div className="weather-stat-label">
            <CloudRain size={11} />
            Rainfall
          </div>
          <div className="weather-stat-value">4.2 mm</div>
        </div>

        <div className="weather-stat">
          <div className="weather-stat-label">
            <Wind size={11} />
            Wind
          </div>
          <div className="weather-stat-value">18 km/h</div>
        </div>

        <div className="weather-stat">
          <div className="weather-stat-label">
            <Droplets size={11} />
            Humidity
          </div>
          <div className="weather-stat-value">82%</div>
        </div>
      </div>
    </Card>
  );
}

export default WeatherCard;