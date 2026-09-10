import type { ReactNode } from "react";
import { Navigate } from "react-router";
import { isAuthenticated } from "../lib/auth";

type Props = {
  children: ReactNode;
};

/** Redirects to /login when there is no valid JWT in localStorage. */
export function RouteGuard({ children }: Props) {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

export default RouteGuard;
