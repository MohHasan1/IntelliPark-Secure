type Props = {
  onTrigger: (id: string) => void;
};

export function SceneTriggers({ onTrigger }: Props) {
  return (
    <div className="rounded-2xl bg-linear-to-b from-slate-900 to-slate-950/40 p-5 shadow-xl shadow-black/50 ring-1 ring-white/5">
      <div className="flex items-center justify-between">
        <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
          Trigger Scene
        </p>
        <span className="text-[11px] text-slate-400">API /scene/:id</span>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-3">
        {["1", "2", "3", "4"].map((id) => (
          <button
            key={id}
            onClick={() => onTrigger(id)}
            className="rounded-xl bg-linear-to-br from-sky-500/80 to-indigo-600/80 px-4 py-3 text-sm font-semibold text-slate-50 shadow-lg shadow-sky-900/60 ring-1 ring-white/5 transition hover:-translate-y-0.5 hover:from-sky-400 hover:to-indigo-500"
          >
            Scene {id}
          </button>
        ))}
      </div>
    </div>
  );
}
