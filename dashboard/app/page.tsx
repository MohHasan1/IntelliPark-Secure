"use client";

import { useEffect, useMemo, useState } from "react";
import { HeaderBar } from "./components/HeaderBar";
import { StatsPanel } from "./components/StatsPanel";
import { GateStatusPanel } from "./components/GateStatusPanel";
import { SceneTriggers } from "./components/SceneTriggers";
import { ParkingGrid } from "./components/ParkingGrid";
import { SceneMedia } from "./components/SceneMedia";
import { useParkingData } from "./hooks/useParkingData";
import { useGateAnimation } from "./hooks/useGateAnimation";
import { buildSpots, computeStats } from "./utils/parking";
import {
  API_BASE,
  defaultConstants,
  gateTimelineEntry,
  gateTimelineExit,
} from "./config";

export default function Home() {
  const { sessions, loading, error, apiBase, refresh, setSessionsDirect } =
    useParkingData();
  const { gateStage, activePlate, animateGate, setGateStageDirect } =
    useGateAnimation(defaultConstants.delays);
  const [gateMode, setGateMode] = useState<"entry" | "exit">("entry");
  const [currentSceneId, setCurrentSceneId] = useState<string | null>(null);

  const totalSpots = defaultConstants.total_spots;
  const spots = useMemo(
    () => buildSpots(totalSpots, sessions),
    [totalSpots, sessions]
  );
  const stats = useMemo(() => computeStats(spots), [spots]);

  const runScene = async (sceneId: string) => {
    const sceneConfig = defaultConstants.scenes?.[sceneId];
    const mode = sceneConfig?.type === "exit" ? "exit" : "entry";
    setGateMode(mode);
    setCurrentSceneId(sceneId);
    animateGate(mode);
    try {
      const res = await fetch(`${API_BASE}/scene/${sceneId}`, {
        method: "POST",
      });
      const json = await res.json();
      if (json?.data && Array.isArray((json.data as any).db)) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const db = (json.data as any).db;
        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
        setSessionsDirect(db as any);
        if (mode === "exit") {
          setGateStageDirect("exited", "Exited");
        } else {
          // set parked status with the latest active plate after entry completes
          const latestActive = Array.isArray(db)
            ? (db as any[])
                .filter((s) => s && s.status !== "exited")
                .sort(
                  (a, b) =>
                    Number(b.session_id ?? 0) - Number(a.session_id ?? 0)
                )[0]
            : null;
          const plateLabel =
            (latestActive && (latestActive.plate as string)) || "Parked";
          setGateStageDirect("parked", plateLabel);
        }
      }
    } catch {
      // keep existing state; hook handles fallback
    }
  };

  useEffect(() => {
    refresh();
  }, [refresh]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-6 py-8">
        <HeaderBar apiBase={apiBase} loading={loading} onRefresh={refresh} />

        {error && (
          <div className="rounded-lg border border-sky-500/40 bg-sky-500/10 px-4 py-3 text-sm text-sky-100">
            {error}
          </div>
        )}

        <div className="grid gap-6 lg:grid-cols-6 auto-rows-[minmax(120px,1fr)]">
          <div className="lg:col-span-4 lg:row-span-2 flex flex-col gap-4">
            <StatsPanel stats={stats} />
            <ParkingGrid spots={spots} />
          </div>

          <div className="lg:col-span-2 lg:row-span-2 flex flex-col gap-3">
            <GateStatusPanel
              timeline={
                gateMode === "exit" ? gateTimelineExit : gateTimelineEntry
              }
              stage={gateStage}
              activePlate={activePlate}
            />
            <SceneMedia
              scenes={defaultConstants.scenes || {}}
              sceneId={currentSceneId}
              stage={gateStage}
              mode={gateMode}
            />
            <SceneTriggers onTrigger={runScene} />
          </div>
        </div>
      </div>
    </div>
  );
}
