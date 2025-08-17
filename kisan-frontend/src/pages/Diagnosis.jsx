import { useState } from "react";
import api from "../api";

export default function Diagnosis() {
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function onFile(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    setLoading(true);
    const fd = new FormData();
    fd.append("image", file);
    const res = await api.upload("/api/diagnosis", fd);
    setResult(res.data);
    setLoading(false);
  }

  return (
    <div className="space-y-6">
      <div className="card text-center">
        <h3 className="text-xl font-semibold mb-2">Upload Crop Image</h3>
        <input type="file" accept="image/*" onChange={onFile} />
        {preview && <img src={preview} alt="" className="mt-4 h-64 object-cover mx-auto rounded" />}
      </div>

      {loading && <div className="card">Analyzing image…</div>}

      {result && (
        <div className="grid md:grid-cols-2 gap-6">
          <div className="card">
            <h4 className="font-semibold mb-2">Uploaded Image</h4>
            <img src={result.image_url} className="h-64 object-cover rounded" />
          </div>
          <div className="card">
            <h4 className="font-semibold mb-2">AI Diagnosis</h4>
            <div className={`p-4 rounded border ${result.diagnosis.severity === "High" ? "bg-red-50 border-red-200" : result.diagnosis.severity === "Moderate" ? "bg-yellow-50 border-yellow-200" : "bg-green-50 border-green-200"}`}>
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium">{result.diagnosis.disease}</div>
                  <div className="text-sm text-gray-600">Confidence: {result.diagnosis.confidence}%</div>
                </div>
                <span className="px-3 py-1 rounded-full text-sm bg-white border">{result.diagnosis.severity}</span>
              </div>
            </div>
            <div className="mt-4">
              <h5 className="font-medium mb-1">Recommended Treatment</h5>
              <p className="text-gray-700">{result.diagnosis.remedy}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
