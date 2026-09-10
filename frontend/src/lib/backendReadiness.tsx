import { useEffect, useRef, useState, type ReactNode } from "react";
import { BackendReadinessContext, type BackendReadinessStatus } from "./useBackendReadiness";

const POLL_INTERVAL_MS = 5000;
const TIMEOUT_MS = 60000;
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function isBackendReady(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    if (!res.ok) return false;
    const data: { status: string; db: string } = await res.json();
    return data.db === "ok";
  } catch {
    return false;
  }
}

/** Polls /health every 5s until the backend reports db=ok, gives up after
 * 60s with a "retry" button. Sits at the top of the app so it only runs
 * once per session. The useBackendReadiness hook is in a separate file
 * so this file exports only a component. */
export function BackendReadinessProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<BackendReadinessStatus>("checking");
  const generationRef = useRef(0);

  function startPolling() {
    const generation = ++generationRef.current;
    const startedAt = Date.now();
    setStatus("checking");

    async function tick() {
      if (generationRef.current !== generation) return;
      const ready = await isBackendReady();
      if (generationRef.current !== generation) return;
      if (ready) {
        setStatus("ready");
        return;
      }
      if (Date.now() - startedAt >= TIMEOUT_MS) {
        setStatus("error");
        return;
      }
      setTimeout(() => void tick(), POLL_INTERVAL_MS);
    }

    void tick();
  }

  useEffect(() => {
    const ref = generationRef;
    startPolling();
    return () => {
      ref.current += 1;
    };
  }, []);

  return (
    <BackendReadinessContext.Provider value={{ status, retry: startPolling }}>
      {children}
    </BackendReadinessContext.Provider>
  );
}
