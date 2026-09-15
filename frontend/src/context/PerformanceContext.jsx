import { createContext, useContext, useEffect, useState } from "react";

const PerformanceContext = createContext(null);

export function PerformanceProvider({ children }) {
  const [performance, setPerformance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/performance`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch performance");
        }

        return response.json();
      })
      .then((data) => {
        setPerformance(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load performance data");
        setLoading(false);
      });
  }, []);

  return (
    <PerformanceContext.Provider
      value={{ performance, loading, error }}
    >
      {children}
    </PerformanceContext.Provider>
  );
}

export function usePerformance() {
  return useContext(PerformanceContext);
}