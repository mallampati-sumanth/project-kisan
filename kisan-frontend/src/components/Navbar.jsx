import { Link, NavLink } from "react-router-dom";

export default function Navbar() {
  const link = "px-3 py-2 rounded hover:bg-gray-100";
  const active = ({ isActive }) => (isActive ? "bg-gray-200 " + link : link);
  return (
    <nav className="bg-white border-b">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="font-bold text-xl">Kisan+</Link>
        <div className="flex gap-2">
          <NavLink className={active} to="/">Home</NavLink>
          <NavLink className={active} to="/weather">Weather</NavLink>
          <NavLink className={active} to="/tips">Tips</NavLink>
          <NavLink className={active} to="/diagnosis">Diagnosis</NavLink>
          <NavLink className={active} to="/forum">Forum</NavLink>
        </div>
      </div>
    </nav>
  );
}
