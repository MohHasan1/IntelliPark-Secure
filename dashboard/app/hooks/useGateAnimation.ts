import { useRef, useState } from "react";
import { DelayConfig, GateStage } from "../types";

type Result = {
  gateStage: GateStage;
  activePlate: string | null;
  animateGate: (mode?: "entry" | "exit", plate?: string) => void;
  setGateStageDirect: (stage: GateStage, plateLabel?: string | null) => void;
  cancelGate: () => void;
};

export function useGateAnimation(delays?: DelayConfig): Result {
  const [gateStage, setGateStage] = useState<GateStage>("idle");
  const [activePlate, setActivePlate] = useState<string | null>(null);
  const timers = useRef<ReturnType<typeof setTimeout>[]>([]);

  const clearTimers = () => {
    timers.current.forEach((t) => clearTimeout(t));
    timers.current = [];
  };

  const animateGate = (mode: "entry" | "exit" = "entry", plate?: string) => {
    clearTimers();
    setActivePlate(plate || "Detecting...");
    if (mode === "exit") {
      const entryDelay = (delays?.entry_delay ?? 1) * 1000;
      const lotDelay = (delays?.lot_scan_delay ?? 1) * 1000;
      const exitDelay = (delays?.exit_delay ?? 1) * 1000;
      const exitSequence: GateStage[] = ["at_gate", "moving_in", "exited"];
      const exitSteps = [0, entryDelay, entryDelay + lotDelay + exitDelay];
      exitSequence.forEach((stage, idx) => {
        timers.current.push(
          setTimeout(() => {
            setGateStage(stage);
            if (stage === "exited" && plate) {
              setActivePlate(plate);
            }
          }, exitSteps[idx])
        );
      });
      return;
    }

    const sequence: GateStage[] = [
      "at_gate",
      "opening",
      "moving_in",
      "searching",
      "parked",
    ];

    // Duration per stage in ms; gate-opened and parked are status-only (0ms)
    const entryDelay = (delays?.entry_delay ?? 1) * 1000;
    const lotDelay = (delays?.lot_scan_delay ?? 1) * 1000;
    const parkDelay = (delays?.parking_delay ?? 2) * 1000;
    const exitDelay = (delays?.exit_delay ?? 1) * 1000;

    const stepMs = [entryDelay, 0, lotDelay, parkDelay, 0];

    sequence.forEach((stage, idx) => {
      const offset =
        stepMs.slice(0, idx).reduce((acc, cur) => acc + cur, 0) || idx * 800;
      timers.current.push(setTimeout(() => setGateStage(stage), offset));
      // When we hit the final "parked" stage, also keep the plate label visible.
      if (stage === "parked" && plate) {
        timers.current.push(setTimeout(() => setActivePlate(plate), offset));
      }
    });
  };

  const setGateStageDirect = (stage: GateStage, plateLabel?: string | null) => {
    setGateStage(stage);
    if (plateLabel !== undefined) {
      setActivePlate(plateLabel);
    }
  };

  const cancelGate = () => {
    clearTimers();
  };

  return { gateStage, activePlate, animateGate, setGateStageDirect, cancelGate };
}
