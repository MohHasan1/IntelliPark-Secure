"use client";

import { useEffect, useMemo, useState } from "react";
import { AllowedCar, ApiResponse } from "../types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:5001";

export default function AllowedPage() {
  const [list, setList] = useState<AllowedCar[]>([]);
  const [plate, setPlate] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);
  const [removing, setRemoving] = useState<string | null>(null);

  const normalized = useMemo(
    () =>
      list
        .map((c) => c.plate)
        .filter(Boolean)
        .sort((a, b) => a.localeCompare(b)),
    [list]
  );

  const fetchList = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/allowed/list`, {
        cache: "no-store",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json: ApiResponse<AllowedCar[]> = await res.json();
      const data = Array.isArray(json?.data) ? json.data : [];
      setList(data);
    } catch (err) {
      setError("Could not load allowed list.");
    } finally {
      setLoading(false);
    }
  };

  const addPlate = async () => {
    const value = plate.trim();
    if (!value) return;
    setAdding(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/allowed/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plate: value }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      await fetchList();
      setPlate("");
    } catch {
      setError("Could not add plate.");
    } finally {
      setAdding(false);
    }
  };

  const removePlate = async (target: string) => {
    setRemoving(target);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/allowed/remove`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plate: target }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      await fetchList();
    } catch {
      setError("Could not remove plate.");
    } finally {
      setRemoving(null);
    }
  };

  useEffect(() => {
    fetchList();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto flex max-w-5xl flex-col gap-6 px-6 py-10">
        <div className="rounded-2xl bg-linear-to-b from-slate-900 to-slate-950/60 p-5 shadow-xl shadow-black/50 ring-1 ring-white/5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div className="flex-1">
              <label className="text-xs uppercase tracking-[0.2em] text-slate-400">
                Add plate
              </label>
              <input
                value={plate}
                onChange={(e) => setPlate(e.target.value)}
                placeholder="e.g. ABC123"
                className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-slate-100 outline-none ring-1 ring-white/5 focus:border-sky-400"
              />
            </div>
            <button
              onClick={addPlate}
              disabled={adding || !plate.trim()}
              className="mt-2 w-full rounded-lg bg-linear-to-r from-emerald-400 to-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 shadow-lg shadow-emerald-500/40 transition hover:from-emerald-300 hover:to-cyan-400 disabled:cursor-not-allowed disabled:opacity-60 sm:mt-0 sm:w-auto"
            >
              {adding ? "Adding..." : "Add"}
            </button>
          </div>
          {error && (
            <div className="mt-3 rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-100">
              {error}
            </div>
          )}
        </div>

        <div className="rounded-2xl bg-linear-to-b from-slate-900 to-slate-950/60 p-5 shadow-xl shadow-black/50 ring-1 ring-white/5">
          <div className="mb-3 flex items-center justify-between">
            <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
              Whitelist
            </p>
            <span className="text-xs text-slate-400">{normalized.length} plates</span>
          </div>
          <div className="divide-y divide-slate-800">
            {normalized.length === 0 && (
              <div className="py-6 text-center text-sm text-slate-400">
                No plates added yet.
              </div>
            )}
            {normalized.map((p) => (
              <div
                key={p}
                className="flex items-center justify-between py-3 text-slate-100"
              >
                <div className="font-mono text-lg tracking-wide">{p}</div>
                <button
                  onClick={() => removePlate(p)}
                  className="rounded-lg border border-red-500/40 bg-red-500/10 px-3 py-1 text-xs font-semibold text-red-100 transition hover:border-red-500/70 hover:bg-red-500/20"
                  disabled={removing === p}
                >
                  {removing === p ? "Removing..." : "Remove"}
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
