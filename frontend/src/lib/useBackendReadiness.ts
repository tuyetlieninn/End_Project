import { createContext, useContext } from "react";

export type BackendReadinessStatus = "checking" | "ready" | "error";

export type BackendReadinessContextValue = {
  status: BackendReadinessStatus;
  retry: () => void;
};

/** Split into its own file so the Provider file only exports a component. */
export const BackendReadinessContext = createContext<BackendReadinessContextValue | null>(null);

export function useBackendReadiness(): BackendReadinessContextValue {
  const ctx = useContext(BackendReadinessContext);
  if (!ctx) {
    throw new Error("useBackendReadiness must be used within BackendReadinessProvider");
  }
  return ctx;
}
