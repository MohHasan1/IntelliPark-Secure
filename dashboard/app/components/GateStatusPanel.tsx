import { GateStage, GateTimelineItem } from "../types";

type Props = {
  timeline: GateTimelineItem[];
  stage: GateStage;
  activePlate: string | null;
};

export function GateStatusPanel({ timeline, stage, activePlate }: Props) {
  return (
    <div className="rounded-2xl bg-linear-to-b from-slate-900 to-slate-950/50 p-5 shadow-xl shadow-black/50 ring-1 ring-white/5">
      <div className="flex items-center justify-between">
        <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
          Status
        </p>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-[11px] text-slate-200 ring-1 ring-white/5">
          {activePlate || "Idle"}
        </span>
      </div>
      <div className="mt-4 space-y-3">
        {timeline.map((item, idx) => {
          const isActive = stage === item.key;
          const isDone = timeline.findIndex((g) => g.key === stage) > idx;
          return (
            <div
              key={item.key}
              className="flex items-center gap-3 text-sm text-slate-200"
            >
              <div
                className={`h-3 w-3 rounded-full ring-2 ring-offset-2 ring-offset-slate-900 ${
                  isActive
                    ? "animate-pulse bg-cyan-400 ring-cyan-300"
                    : isDone
                    ? "bg-emerald-400 ring-emerald-300"
                    : "bg-slate-700 ring-slate-600"
                }`}
              />
              <div className="flex-1 rounded-lg bg-slate-800/70 px-3 py-2 ring-1 ring-white/5">
                {item.label}
              </div>
            </div>
          );
        })}
      </div>
      <div className="mt-4 flex flex-wrap gap-2 text-xs text-slate-400">
        <span className="rounded-full bg-slate-800 px-2 py-1 ring-1 ring-white/5">
          Scene → gate opens after 1-2s
        </span>
        <span className="rounded-full bg-slate-800 px-2 py-1 ring-1 ring-white/5">
          Status progresses to parked
        </span>
      </div>
    </div>
  );
}
