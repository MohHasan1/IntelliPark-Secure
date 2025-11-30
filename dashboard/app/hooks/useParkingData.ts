import { useCallback, useState } from "react";
import { API_BASE, fallbackSessions } from "../config";
import { ApiResponse, ParkingSession } from "../types";

type Result = {
  sessions: ParkingSession[];
  loading: boolean;
  error: string | null;
  apiBase: string;
  refresh: () => Promise<void>;
  setSessionsDirect: (next: ParkingSession[]) => void;
};

export function useParkingData(): Result {
  const [sessions, setSessions] = useState<ParkingSession[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/db`, { cache: "no-store" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json: ApiResponse<ParkingSession[]> = await res.json();
      const data = Array.isArray(json?.data) ? json.data : fallbackSessions;
      setSessions(data);
    } catch (err) {
      setError("Live data unavailable. Showing latest cached layout.");
      setSessions(fallbackSessions);
    } finally {
      setLoading(false);
    }
  }, []);

  const setSessionsDirect = useCallback((next: ParkingSession[]) => {
    setSessions(next);
  }, []);

  return {
    sessions,
    loading,
    error,
    apiBase: API_BASE,
    refresh,
    setSessionsDirect,
  };
}
