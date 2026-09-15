import { createContext, useContext, useEffect, useState } from "react";

const WeatherContext = createContext(null);

export function WeatherProvider({ children }) {
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/forecast`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch forecast");
        }
        return response.json();
      })
      .then((data) => {
        setForecast(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load live forecast");
        setLoading(false);
      });
  }, []);

  return (
    <WeatherContext.Provider
      value={{ forecast, loading, error }}
    >
      {children}
    </WeatherContext.Provider>
  );
}

export function useWeather() {
  return useContext(WeatherContext);
}