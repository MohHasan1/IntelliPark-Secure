"use client";

import { useEffect, useState } from "react";
import { ApiResponse, ParkingSession } from "../types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:5001";

const normalizePlate = (value: string) =>
  value
    .trim()
    .toUpperCase()
    .replace(/[^A-Z0-9]/g, "-")
    .replace(/-+/g, "-")
    .toLowerCase();

function displayStatus(status: string | undefined) {
  if (!status) return "Unknown";
  const s = status.toLowerCase();
  if (s === "entering") return "Entering";
  if (s === "parked") return "Parked";
  if (s === "exited") return "Exited";
  return status;
}

export default function FindCarPage() {
  const [plate, setPlate] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ParkingSession | null>(null);
  const [plateImages, setPlateImages] = useState<Record<string, string>>({});

  const lookup = async () => {
    const value = normalizePlate(plate);
    if (!value) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(
        `${API_BASE}/sessions/plate/${encodeURIComponent(
          value
        )}/latest?t=${Date.now()}`,
        { cache: "no-store", headers: { "Cache-Control": "no-cache" } }
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json: ApiResponse<ParkingSession | null> = await res.json();
      if (!json?.data) {
        setError("No records found for that plate.");
        return;
      }
      setResult(json.data);
    } catch (err) {
      setError("Lookup failed. Try again.");
    } finally {
      setLoading(false);
    }
  };

  const spotValue =
    result?.status === "exited"
      ? result?.previous_spot
      : result?.spot ?? result?.previous_spot;

  const prevSpot = result?.previous_spot;
  const currentSpot = result?.spot;

  const plateImage =
    (result?.plate && plateImages[result.plate]) || "/img/car1.jpeg";

  useEffect(() => {
    try {
      const stored = window.localStorage.getItem("plateImages");
      if (stored) {
        setPlateImages(JSON.parse(stored));
      }
    } catch (e) {
      console.warn("Could not load plate images", e);
    }
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto flex max-w-4xl flex-col gap-6 px-6 py-10">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-sky-300/80">
            IntelliPark
          </p>
          <h1 className="text-3xl font-semibold text-sky-50">Find Car</h1>
          <p className="text-sm text-slate-400">
            Search latest location/status by license plate.
          </p>
        </div>

        <div className="rounded-2xl bg-linear-to-b from-slate-900 to-slate-950/60 p-5 shadow-xl shadow-black/50 ring-1 ring-white/5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div className="flex-1">
              <label className="text-xs uppercase tracking-[0.2em] text-slate-400">
                License plate
              </label>
              <input
                value={plate}
                onChange={(e) => setPlate(e.target.value)}
                placeholder="e.g. ABC123"
                className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-slate-100 outline-none ring-1 ring-white/5 focus:border-sky-400"
              />
            </div>
            <button
              onClick={lookup}
              disabled={loading || !plate.trim()}
              className="mt-2 w-full rounded-lg bg-linear-to-r from-sky-400 to-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 shadow-lg shadow-sky-500/40 transition hover:from-sky-300 hover:to-cyan-400 disabled:cursor-not-allowed disabled:opacity-60 sm:mt-0 sm:w-auto"
            >
              {loading ? "Searching..." : "Find"}
            </button>
          </div>
          {error && (
            <div className="mt-3 rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-100">
              {error}
            </div>
          )}
        </div>

        {result && (
          <div className="rounded-2xl bg-linear-to-b from-slate-900 to-slate-950/60 p-5 shadow-xl shadow-black/50 ring-1 ring-white/5">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-center gap-4">
                <div
                  className="h-16 w-24 rounded-lg border border-slate-800 bg-center bg-cover ring-1 ring-white/5"
                  style={{ backgroundImage: `url(${plateImage.replace(/^\.\//, "/")})` }}
                />
                <div>
                  <div className="text-xs uppercase tracking-[0.2em] text-slate-400">
                    Plate
                  </div>
                  <div className="text-2xl font-semibold text-slate-50">
                    {result.plate}
                  </div>
                </div>
              </div>
              <span
                className={`rounded-full px-3 py-1 text-xs uppercase tracking-wide ${
                  result.status === "exited"
                    ? "bg-red-500/15 text-red-100 ring-1 ring-red-500/30"
                    : "bg-emerald-500/15 text-emerald-100 ring-1 ring-emerald-500/30"
                }`}
              >
                {displayStatus(result.status)}
              </span>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-4 text-sm text-slate-200">
              <div>
                <div className="text-xs uppercase tracking-[0.2em] text-slate-400">
                  Session ID
                </div>
                <div className="text-lg font-semibold">{result.session_id}</div>
              </div>
              <div>
                <div className="text-xs uppercase tracking-[0.2em] text-slate-400">
                  Current Spot
                </div>
                <div className="text-lg font-semibold">
                  {currentSpot ?? "N/A"}
                </div>
              </div>
              <div>
                <div className="text-xs uppercase tracking-[0.2em] text-slate-400">
                  Previous Spot
                </div>
                <div className="text-lg font-semibold">
                  {prevSpot ?? "N/A"}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
