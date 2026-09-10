import type { ReactNode } from "react";
import { useBackendReadiness } from "../lib/useBackendReadiness";
import Header from "./Header";
import Sidebar from "./Sidebar";
import ToastHost from "./ToastHost";

/** Top-level layout for authenticated routes. Shows a full-screen overlay
 *  while the backend is still starting up (or has timed out) so users can't
 *  try to interact with anything before the API is reachable. */
export function AppShell({ children }: { children: ReactNode }) {
  const { status, retry } = useBackendReadiness();

  if (status !== "ready") {
    return (
      <div className="backend-readiness-overlay">
        {status === "checking" ? (
          <p role="status">システムを起動しています...</p>
        ) : (
          <>
            <p className="toast-error" role="alert">
              システムの起動に時間がかかっています。もう一度お試しください。
            </p>
            <button type="button" className="button-primary" onClick={retry}>
              再試行
            </button>
          </>
        )}
      </div>
    );
  }

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="app-main">
        <Header />
        <ToastHost />
        {children}
      </div>
    </div>
  );
}

export default AppShell;
