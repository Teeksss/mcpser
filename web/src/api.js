import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
});
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers["Authorization"] = `Bearer ${token}`;
  const tenant = localStorage.getItem("tenant_id");
  if (tenant) config.headers["X-Tenant"] = tenant;
  return config;
});
export default api;