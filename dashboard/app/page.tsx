"use client";

import { useEffect, useMemo, useState } from "react";
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
  const [blockedInfo, setBlockedInfo] = useState<{ plate?: string; message?: string } | null>(null);

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
    setBlockedInfo(null);
    animateGate(mode);
    try {
      const res = await fetch(`${API_BASE}/scene/${sceneId}`, {
        method: "POST",
      });
      const json = await res.json();
      const data = json?.data as any;

      if (data?.error) {
        setBlockedInfo({ plate: data.plate, message: data.message || data.error });
        setGateStageDirect("at_gate", data.plate || "Access Denied");
        return;
      }

      if (json?.data && Array.isArray((json.data as any).db)) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const db = data.db;
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
    <>
        {error && (
          <div className="rounded-lg border border-sky-500/40 bg-sky-500/10 px-4 py-3 text-sm text-sky-100">
            {error}
          </div>
        )}
        {blockedInfo && (
          <div className="rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-100">
            <div className="font-semibold">Access Denied</div>
            <div>{blockedInfo.message || "Car is not on the allowed list."}</div>
            {blockedInfo.plate && (
              <div className="mt-1 text-xs text-red-200">Plate: {blockedInfo.plate}</div>
            )}
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
            <SceneTriggers
              onTrigger={runScene}
              sceneIds={Object.keys(defaultConstants.scenes || {})}
            />
          </div>
        </div>
    </>
  );
}
