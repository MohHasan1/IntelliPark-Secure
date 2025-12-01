import { ParkingSession, Spot } from "../types";

export function buildSpots(total: number, sessions: ParkingSession[]): Spot[] {
  const occupied = new Map<number, ParkingSession>();
  sessions.forEach((s) => {
    if (s.spot && s.status !== "exited") occupied.set(s.spot, s);
  });

  const highestOccupied = occupied.size
    ? Math.max(...Array.from(occupied.keys()))
    : 0;
  const computedTotal = Math.max(total, highestOccupied);

  return Array.from({ length: computedTotal }, (_, i) => {
    const spotNum = i + 1;
    const session = occupied.get(spotNum);
    return {
      spot: spotNum,
      occupied: Boolean(session),
      plate: session?.plate || "",
      status: session?.status || "empty",
    };
  });
}

export function computeStats(spots: Spot[]) {
  const taken = spots.filter((s) => s.occupied).length;
  const total = spots.length;
  return [
    { label: "Total", value: total },
    { label: "Taken", value: taken },
    { label: "Empty", value: total - taken },
  ];
}
