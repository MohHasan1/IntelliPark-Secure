export type ParkingSession = {
  session_id: number;
  plate: string;
  status: "entering" | "parked" | "exited" | string;
  spot?: number | null;
  previous_spot?: number | null;
};

export type ApiResponse<T> = { data?: T; status?: boolean; error?: string };

export type GateStage =
  | "idle"
  | "at_gate"
  | "opening"
  | "moving"
  | "searching"
  | "parked"
  | "exited";

export type GateTimelineItem = { key: GateStage; label: string };

export type Spot = {
  spot: number;
  occupied: boolean;
  plate: string;
  status: string;
};

export type DelayConfig = {
  entry_delay: number;
  lot_scan_delay: number;
  parking_delay: number;
  exit_delay: number;
};

export type ConstantsConfig = {
  total_spots: number;
  delays: DelayConfig;
  scenes?: Record<string, SceneConfig>;
};

export type SceneConfig = {
  entry: string | null;
  lot_before: string | null;
  lot_after: string | null;
  exit: string | null;
  type: "entry" | "exit";
};

export type AllowedCar = {
  plate: string;
};
