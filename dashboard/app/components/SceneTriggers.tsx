type Props = {
  onTrigger: (id: string) => void;
  sceneIds: string[];
};

const sceneLabels: Record<string, string> = {
  "1": "Red entry",
  "2": "Black entry",
  "3": "Yellow entry",
  "4": "Blue entry",
  "5": "Blue exit",
  "6": "Yellow exit",
  "7": "Black exit",
  "8": "Red exit",
};

export function SceneTriggers({ onTrigger, sceneIds }: Props) {
  return (
    <details className="overflow-hidden rounded-2xl bg-linear-to-b from-slate-900 to-slate-950/40 shadow-xl shadow-black/50 ring-1 ring-white/5">
      <summary className="flex cursor-pointer list-none items-center justify-between px-5 py-4 text-slate-200 hover:bg-slate-900/60">
        <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
          Trigger Scene (In sequence)
        </p>
        <span className="text-[11px] text-slate-400">API /scene/:id</span>
      </summary>
      <div className="border-t border-slate-800/80 bg-slate-900/60 px-5 py-4">
        <div className="grid grid-cols-2 gap-3">
          {sceneIds.map((id) => (
            <button
              key={id}
              onClick={() => onTrigger(id)}
              className="rounded-xl bg-sky-500/10 px-4 py-3 text-sm font-semibold text-slate-50 shadow-md shadow-sky-900/40 ring-1 ring-sky-500/30 transition hover:-translate-y-0.5 hover:bg-sky-500/20"
            >
              Scene {id}
              {sceneLabels[id] ? ` (${sceneLabels[id]})` : ""}
            </button>
          ))}
        </div>
      </div>
    </details>
  );
}
