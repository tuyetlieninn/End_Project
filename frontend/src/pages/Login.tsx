import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router";
import { login } from "../lib/auth";

type ErrorState = { kind: "field" | "toast"; message: string } | null;

const GENERIC_ERROR_MESSAGE = "エラーが発生しました。しばらくしてから再度お試しください";
const CREDENTIALS_ERROR_MESSAGE = "メールアドレスまたはパスワードが正しくありません";

/** NotAuthorizedException / UserNotFoundException share the same message
 * to avoid leaking whether the email exists. */
function classifyError(error: unknown): ErrorState {
  const name = error instanceof Error ? error.name : "";
  if (name === "NotAuthorizedException" || name === "UserNotFoundException") {
    return { kind: "field", message: CREDENTIALS_ERROR_MESSAGE };
  }
  return { kind: "toast", message: GENERIC_ERROR_MESSAGE };
}

export function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<ErrorState>(null);
  const navigate = useNavigate();

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      await login(email, password);
      navigate("/projects", { replace: true });
    } catch (err) {
      setError(classifyError(err));
      setSubmitting(false);
    }
  }

  return (
    <main className="auth-page">
      <div className="auth-card">
        <h1>実績管理システム</h1>
        {error?.kind === "toast" && (
          <p className="toast-error" role="alert">
            {error.message}
          </p>
        )}
        <form onSubmit={handleSubmit}>
          <div className="input-field">
            <label htmlFor="login-email">メールアドレス</label>
            <input
              id="login-email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              disabled={submitting}
              required
            />
          </div>

          <div className={`input-field${error?.kind === "field" ? " input-field-error" : ""}`}>
            <label htmlFor="login-password">パスワード</label>
            <input
              id="login-password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              disabled={submitting}
              required
            />
            {error?.kind === "field" && (
              <p className="field-error-message" role="alert">
                {error.message}
              </p>
            )}
          </div>

          <button type="submit" className="button-primary" disabled={submitting}>
            ログイン
          </button>
        </form>
        <p className="auth-link">
          アカウントをお持ちでない方は <Link to="/register">アカウントを作成</Link>
        </p>
      </div>
    </main>
  );
}

export default Login;
