import { Spot } from "../types";

type Props = {
  spots: Spot[];
};

export function ParkingGrid({ spots }: Props) {
  return (
    <main className="rounded-3xl bg-linear-to-br from-slate-900 to-slate-950/70 p-6 shadow-2xl shadow-black/60 ring-1 ring-white/5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
            Parking Grid
          </p>
          <h2 className="text-2xl font-semibold text-sky-50">Live Occupancy</h2>
        </div>
        <div className="flex items-center gap-3 text-xs text-slate-300">
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-3 rounded-full bg-emerald-400 shadow-[0_0_12px_3px_rgba(52,211,153,0.5)]" />
            Empty
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-3 rounded-full bg-red-400 shadow-[0_0_12px_3px_rgba(248,113,113,0.5)]" />
            Taken
          </span>
        </div>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        {spots.map((spot) => {
          const occupied = spot.occupied;
          return (
            <div
              key={spot.spot}
              className={`group relative overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/70 p-4 ring-1 ring-white/5 transition hover:-translate-y-1 hover:border-slate-700 ${
                occupied
                  ? "shadow-[0_0_30px_rgba(239,68,68,0.25)]"
                  : "shadow-[0_0_22px_rgba(52,211,153,0.18)]"
              }`}
            >
              <div
                className={`absolute inset-0 blur-2xl opacity-60 ${
                  occupied
                    ? "bg-red-500/20 group-hover:bg-red-400/25"
                    : "bg-emerald-400/15 group-hover:bg-emerald-400/20"
                }`}
              />
              <div className="relative flex items-start justify-between">
                <div className="text-xs uppercase tracking-[0.25em] text-slate-400">
                  Spot {spot.spot}
                </div>
                <div
                  className={`h-2 w-2 rounded-full ${
                    occupied ? "bg-red-400" : "bg-emerald-400"
                  }`}
                />
              </div>
              <div className="relative mt-6 flex items-center justify-between">
                <div>
                  <div className="text-lg font-semibold text-slate-50">
                    {occupied ? spot.plate : "Available"}
                  </div>
                  <div className="text-xs uppercase tracking-wide text-slate-400">
                    {occupied ? "Taken" : "Empty"}
                  </div>
                </div>
                <div
                  className={`flex h-12 w-16 items-center justify-center rounded-xl border border-slate-800 bg-slate-950/70 text-xs font-semibold shadow-inner shadow-black/60 ${
                    occupied ? "text-red-200" : "text-emerald-200"
                  }`}
                >
                  <span className="translate-y-px">🚗</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </main>
  );
}
