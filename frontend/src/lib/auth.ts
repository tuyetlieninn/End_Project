const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

const STORAGE_KEY_ID_TOKEN = "auth.idToken";

export type IdTokenPayload = {
  email: string;
  role?: "admin" | "member";
  exp?: number;
};

export type CurrentUser = {
  email: string;
  role: "admin" | "member";
};

export type LoginResult = {
  idToken: string;
};

/** Calls `POST /auth/login` and stores the returned JWT. */
/** Calls `POST /auth/register` and stores the returned JWT.
 *  If the backend does not return an idToken, falls back to calling
 *  `login()` so the user lands on the project list either way. */
export async function register(email: string, password: string): Promise<LoginResult> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    let message = "登録に失敗しました";
    try {
      const data = (await response.json()) as { detail?: string; message?: string };
      if (data.detail) message = data.detail;
      else if (data.message) message = data.message;
    } catch {
      // ignore
    }
    const error = new Error(message);
    error.name = response.status === 409 ? "UsernameExistsException" : "RegisterError";
    throw error;
  }

  const data = (await response.json()) as { idToken?: string; access_token?: string };
  const idToken = data.idToken ?? data.access_token;
  if (idToken) {
    localStorage.setItem(STORAGE_KEY_ID_TOKEN, idToken);
    return { idToken };
  }

  // Backend did not auto-login — fall back to a manual login.
  return login(email, password);
}


export async function login(email: string, password: string): Promise<LoginResult> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    let message = "ログインに失敗しました";
    try {
      const data = (await response.json()) as { detail?: string; message?: string };
      if (data.detail) message = data.detail;
      else if (data.message) message = data.message;
    } catch {
      // ignore — fall back to default message
    }
    const error = new Error(message);
    error.name = response.status === 401 ? "NotAuthorizedException" : "LoginError";
    throw error;
  }

  const data = (await response.json()) as { idToken?: string; access_token?: string };
  const idToken = data.idToken ?? data.access_token;
  if (!idToken) {
    throw new Error("サーバからトークンを取得できませんでした");
  }

  localStorage.setItem(STORAGE_KEY_ID_TOKEN, idToken);
  return { idToken };
}

/** Returns the stored JWT, or `null` if the user is not logged in. */
export function getIdToken(): string | null {
  return localStorage.getItem(STORAGE_KEY_ID_TOKEN);
}

export function isAuthenticated(): boolean {
  const token = getIdToken();
  if (!token) return false;

  const payload = decodeIdToken(token);
  if (!payload) return false;

  if (payload.exp && payload.exp * 1000 <= Date.now()) {
    localStorage.removeItem(STORAGE_KEY_ID_TOKEN);
    return false;
  }
  return true;
}

/** Clears the stored JWT. Does not call the backend. */
export function logout(): void {
  localStorage.removeItem(STORAGE_KEY_ID_TOKEN);
}

/** Decodes the JWT payload. Does not verify the signature — backend is the
 *  source of truth; the frontend only reads `email` / `role` to render UI. */
export function decodeIdToken(token: string): IdTokenPayload | null {
  try {
    const payloadBase64Url = token.split(".")[1];
    const payloadBase64 = payloadBase64Url.replace(/-/g, "+").replace(/_/g, "/");
    return JSON.parse(atob(payloadBase64)) as IdTokenPayload;
  } catch {
    return null;
  }
}

/** Returns `{ email, role }` from the stored JWT, or `null` if not logged in. */
export function getCurrentUser(): CurrentUser | null {
  const token = getIdToken();
  if (!token) return null;

  const payload = decodeIdToken(token);
  if (!payload) return null;

  return {
    email: payload.email,
    role: payload.role ?? "member",
  };
}
