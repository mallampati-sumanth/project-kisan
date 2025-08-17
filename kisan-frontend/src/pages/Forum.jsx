import { useEffect, useState } from "react";
import api from "../api";

export default function Forum() {
  const [posts, setPosts] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);

  async function load() {
    const res = await api.get("/api/posts");
    setPosts(res.data || []);
  }
  useEffect(() => { load(); }, []);

  async function submit(e) {
    e.preventDefault();
    setLoading(true);
    await api.post("/api/posts", { title, content, user_id: "guest" });
    setTitle(""); setContent(""); setLoading(false);
    load();
  }

  async function like(id) {
    await api.post(`/api/posts/${id}/like`, {});
    load();
  }

  return (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold mb-3">Share Your Experience</h3>
        <form onSubmit={submit} className="space-y-3">
          <input value={title} onChange={(e)=>setTitle(e.target.value)} placeholder="What's your farming question or tip?"
                 className="w-full border rounded px-3 py-2" required />
          <textarea value={content} onChange={(e)=>setContent(e.target.value)} rows={4}
                 placeholder="Share details..." className="w-full border rounded px-3 py-2" required />
          <button className="btn-primary" disabled={loading}>{loading ? "Posting..." : "Post"}</button>
        </form>
      </div>

      <div className="space-y-4">
        {posts.length === 0 && <div className="card text-center text-gray-500">No posts yet</div>}
        {posts.map(p => (
          <div key={p.id} className="card">
            <div className="flex items-start justify-between">
              <div>
                <h4 className="font-semibold">{p.title}</h4>
                <div className="text-sm text-gray-500">Farmer {p.user_id} • {new Date(p.timestamp).toLocaleString()}</div>
              </div>
              <button onClick={()=>like(p.id)} className="text-gray-500 hover:text-red-500">❤️ {p.likes}</button>
            </div>
            <p className="mt-2 text-gray-700">{p.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
