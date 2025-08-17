import { useEffect, useState } from "react";
import api from "../api";

export default function Weather() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api.get("/api/weather").then((res) => setData(res.data));
  }, []);

  if (!data) return <div className="card">Loading weather...</div>;

  return (
    <div className="space-y-6">
      <div className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-lg">{data.location}</div>
            <div className="text-5xl font-bold">{data.temperature}°C</div>
            <div className="text-blue-100">{data.rainfall}</div>
          </div>
          <div className="text-right">
            <div className="text-6xl">⛅</div>
            <div>Partly Cloudy</div>
          </div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          <div className="text-center"><div className="text-blue-200 text-sm">Humidity</div><div className="text-xl font-semibold">{data.humidity}%</div></div>
          <div className="text-center"><div className="text-blue-200 text-sm">Wind</div><div className="text-xl font-semibold">{data.wind}</div></div>
          <div className="text-center"><div className="text-blue-200 text-sm">Visibility</div><div className="text-xl font-semibold">10 km</div></div>
          <div className="text-center"><div className="text-blue-200 text-sm">UV</div><div className="text-xl font-semibold">6 (High)</div></div>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {data.forecast.map((d) => (
          <div key={d.day} className="card text-center">
            <div className="text-lg font-semibold">{d.day}</div>
            <div className="text-4xl">{d.icon}</div>
            <div className="text-2xl font-bold">{d.temp}°C</div>
            <div className="text-gray-600">{d.condition}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
