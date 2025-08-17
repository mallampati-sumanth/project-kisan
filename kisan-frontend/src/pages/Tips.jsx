import { useEffect, useState } from "react";
import api from "../api";

export default function Tips() {
  const [tips, setTips] = useState(null);
  const [tab, setTab] = useState("irrigation");

  useEffect(() => {
    api.get("/api/tips").then((res) => setTips(res.data));
  }, []);

  if (!tips) return <div className="card">Loading tips...</div>;

  const cats = Object.keys(tips);

  return (
    <div>
      <div className="flex flex-wrap gap-2 mb-6">
        {cats.map((c) => (
          <button
            key={c}
            onClick={() => setTab(c)}
            className={`px-4 py-2 rounded-full ${tab === c ? "bg-green-500 text-white" : "bg-gray-200 text-gray-700"}`}
          >
            {c[0].toUpperCase() + c.slice(1)}
          </button>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {tips[tab].map((t, i) => (
          <div key={i} className="card">
            <div className="flex items-start gap-4">
              <div className="text-4xl">{t.icon}</div>
              <div>
                <h3 className="text-xl font-semibold">{t.title}</h3>
                <p className="text-gray-600">{t.content}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
