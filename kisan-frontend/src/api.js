const api = {
  async get(path, params) {
    const url = new URL(path, window.location.origin);
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
    const res = await fetch(url, { credentials: "include" });
    return res.json();
  },
  async post(path, body) {
    const res = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(body),
    });
    return res.json();
  },
  async upload(path, formData) {
    const res = await fetch(path, { method: "POST", body: formData, credentials: "include" });
    return res.json();
  },
};
export default api;
