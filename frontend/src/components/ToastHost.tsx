import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router";

/** Reads `successMessage` from router state, shows it for 3s, then clears
 *  the navigation state so back/refresh don't re-show it. */
export function ToastHost() {
  const location = useLocation();
  const navigate = useNavigate();
  const [message, setMessage] = useState<string | null>(null);
  const processedKeyRef = useRef<string | null>(null);

  // Reads the new message and clears the navigation state in one effect.
  // Kept separate from the timer effect below: clearing state via
  // `navigate()` here changes location.key/state, and combining the two
  // effects would cancel the timer we just scheduled.
  useEffect(() => {
    const state = location.state as { successMessage?: string } | null;
    const successMessage = state?.successMessage;

    if (!successMessage || processedKeyRef.current === location.key) {
      return;
    }

    processedKeyRef.current = location.key;
    setMessage(successMessage);
    navigate(location.pathname, { replace: true, state: {} });
  }, [location.key, location.state, location.pathname, navigate]);

  useEffect(() => {
    if (!message) {
      return;
    }

    const timer = setTimeout(() => setMessage(null), 3000);
    return () => clearTimeout(timer);
  }, [message]);

  if (!message) {
    return null;
  }

  return (
    <div className="toast-success" role="status">
      {message}
    </div>
  );
}

export default ToastHost;
