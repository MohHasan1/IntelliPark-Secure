import { constantConfig } from "./constant";
import { ConstantsConfig, GateTimelineItem, ParkingSession } from "./types";

export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://localhost:5001";

// Keep fallback empty so cached view respects constant.ts total_spots
export const fallbackSessions: ParkingSession[] = [];

export const gateTimelineEntry: GateTimelineItem[] = [
  { key: "at_gate", label: "Reading License" },
  { key: "opening", label: "Gate Opened" },
  { key: "moving_in", label: "Looking for a Spot" },
  { key: "searching", label: "Parking" },
  { key: "parked", label: "Parked" },
];

export const gateTimelineExit: GateTimelineItem[] = [
  { key: "at_gate", label: "Detecting License Plate" },
  { key: "moving_in", label: "Scanning Lot" },
  { key: "exited", label: "Exiting" },
];

export const defaultConstants: ConstantsConfig = constantConfig;
