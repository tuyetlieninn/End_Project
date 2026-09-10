import { getIdToken, logout } from "./auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

/** Shared fetch wrapper. Attaches the JWT and redirects to /login on 401.
 *  Uses `window.location.assign` instead of `useNavigate` because this
 *  module is not inside a React component. */
export async function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const idToken = getIdToken();
  const headers = new Headers(init.headers);
  if (idToken) {
    headers.set("Authorization", `Bearer ${idToken}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, { ...init, headers });

  if (response.status === 401) {
    logout();
    window.location.assign("/login");
  }

  return response;
}
