export default function Home() {
  return (
    <div className="grid md:grid-cols-2 gap-6">
      <div className="card">
        <h2 className="text-2xl font-bold mb-2">Welcome to Kisan+</h2>
        <p className="text-gray-600">Smart farming tools: local weather, crop tips, AI diagnosis, and a farmer forum.</p>
      </div>
      <div className="card">
        <h3 className="font-semibold mb-2">Quick Links</h3>
        <ul className="list-disc ml-5 text-gray-700 space-y-1">
          <li>Check <b>Weather</b> for your area</li>
          <li>Browse <b>Tips</b> for irrigation, sowing & harvesting</li>
          <li>Try <b>Diagnosis</b> to analyze crop images</li>
          <li>Join the <b>Forum</b> to share and learn</li>
        </ul>
      </div>
    </div>
  );
}
