function statColor(label: string) {
  if (label === "Empty") return "from-emerald-300/30 via-emerald-500/10 to-emerald-700/5";
  if (label === "Taken") return "from-red-400/30 via-red-500/10 to-red-700/5";
  return "from-cyan-300/30 via-sky-500/10 to-blue-700/5";
}

function glowShadow(label: string) {
  if (label === "Empty") return "0 0 32px 10px rgba(52, 211, 153, 0.28)";
  if (label === "Taken") return "0 0 32px 10px rgba(248, 113, 113, 0.28)";
  return "0 0 32px 10px rgba(56, 189, 248, 0.28)";
}

export type Stat = { label: string; value: number };

type Props = {
  stats: Stat[];
};

export function StatsPanel({ stats }: Props) {
  return (
    <div className="rounded-2xl bg-linear-to-b from-slate-900 to-slate-950/40 p-5 shadow-xl shadow-black/50 ring-1 ring-white/5">
      <p className="mb-3 text-xs uppercase tracking-[0.2em] text-slate-400">
        Lot Stats
      </p>
      <div className="grid grid-cols-3 gap-3">
        {stats.map((s) => (
          <div
            key={s.label}
            className="relative overflow-hidden rounded-xl border border-white/12 bg-slate-900/70 px-4 py-4 text-center shadow-xl shadow-black/35 backdrop-blur-sm"
            style={{ boxShadow: glowShadow(s.label) }}
          >
            <div
              className={`absolute inset-0 bg-linear-to-br ${statColor(
                s.label
              )} blur-md opacity-60`}
            />
            <div className="absolute inset-0 bg-white/7" />
            <div className="relative text-2xl font-semibold text-slate-50 drop-shadow-[0_0_14px_rgba(255,255,255,0.3)]">
              {s.value}
            </div>
            <div className="relative text-xs uppercase tracking-wide text-slate-200 drop-shadow-[0_0_10px_rgba(255,255,255,0.22)]">
              {s.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
