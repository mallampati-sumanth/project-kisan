import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import Home from "./pages/Home.jsx";
import Weather from "./pages/Weather.jsx";
import Tips from "./pages/Tips.jsx";
import Diagnosis from "./pages/Diagnosis.jsx";
import Forum from "./pages/Forum.jsx";

export default function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="max-w-6xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/weather" element={<Weather />} />
          <Route path="/tips" element={<Tips />} />
          <Route path="/diagnosis" element={<Diagnosis />} />
          <Route path="/forum" element={<Forum />} />
        </Routes>
      </main>
    </div>
  );
}
