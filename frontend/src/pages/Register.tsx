import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router";
import { register } from "../lib/auth";

const PASSWORD_POLICY_MESSAGE =
  "パスワードの条件を満たしていません（8文字以上、大文字・小文字・数字を含む）";
const MISMATCH_MESSAGE = "パスワードが一致しません";
const EMAIL_TAKEN_MESSAGE = "このメールアドレスは既に登録されています";
const GENERIC_ERROR_MESSAGE =
  "登録に失敗しました。しばらくしてから再度お試しください";

/** Mirrors the backend password policy: >=8 chars, upper, lower, digit. */
function meetsPasswordPolicy(password: string): boolean {
  return (
    password.length >= 8 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /[0-9]/.test(password)
  );
}

type ErrorState = { kind: "field" | "toast"; message: string } | null;

function classifyError(error: unknown): ErrorState {
  const name = error instanceof Error ? error.name : "";
  if (name === "UsernameExistsException") {
    return { kind: "field", message: EMAIL_TAKEN_MESSAGE };
  }
  return { kind: "toast", message: GENERIC_ERROR_MESSAGE };
}

export function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<ErrorState>(null);
  const navigate = useNavigate();

  const emailOk = /.+@.+\..+/.test(email);
  const policyOk = meetsPasswordPolicy(password);
  const mismatch = confirmPassword.length > 0 && password !== confirmPassword;
  const canSubmit =
    !submitting && emailOk && policyOk && password === confirmPassword;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit) return;
    setSubmitting(true);
    setError(null);

    try {
      await register(email, password);
      navigate("/projects", { replace: true });
    } catch (err) {
      setError(classifyError(err));
      setSubmitting(false);
    }
  }

  return (
    <main className="auth-page">
      <div className="auth-card">
        <h1>アカウントを作成</h1>
        {error?.kind === "toast" && (
          <p className="toast-error" role="alert">
            {error.message}
          </p>
        )}
        <form onSubmit={handleSubmit}>
          <div
            className={`input-field${
              error?.kind === "field" ? " input-field-error" : ""
            }`}
          >
            <label htmlFor="register-email">メールアドレス</label>
            <input
              id="register-email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              disabled={submitting}
              required
            />
            {error?.kind === "field" && (
              <p className="field-error-message" role="alert">
                {error.message}
              </p>
            )}
          </div>

          <div className="input-field">
            <label htmlFor="register-password">パスワード</label>
            <input
              id="register-password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              disabled={submitting}
              required
            />
            <p className="input-hint">{PASSWORD_POLICY_MESSAGE}</p>
          </div>

          <div
            className={`input-field${mismatch ? " input-field-error" : ""}`}
          >
            <label htmlFor="register-confirm">パスワード（確認）</label>
            <input
              id="register-confirm"
              type="password"
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
              disabled={submitting}
              required
            />
            {mismatch && (
              <p className="field-error-message" role="alert">
                {MISMATCH_MESSAGE}
              </p>
            )}
          </div>

          <button
            type="submit"
            className="button-primary"
            disabled={!canSubmit}
          >
            登録する
          </button>
        </form>
        <p className="auth-link">
          すでにアカウントをお持ちですか？ <Link to="/login">ログイン</Link>
        </p>
      </div>
    </main>
  );
}

export default Register;
