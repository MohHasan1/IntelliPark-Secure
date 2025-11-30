function statColor(label: string) {
  if (label === "Empty") return "from-emerald-400/60 to-emerald-700/40";
  if (label === "Taken") return "from-red-400/60 to-red-700/40";
  return "from-cyan-400/60 to-blue-700/40";
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
            className={`rounded-xl bg-linear-to-br ${statColor(
              s.label
            )} px-4 py-3 text-center shadow-inner shadow-black/40 ring-1 ring-white/5`}
          >
            <div className="text-2xl font-semibold">{s.value}</div>
            <div className="text-xs uppercase tracking-wide text-slate-100/80">
              {s.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
