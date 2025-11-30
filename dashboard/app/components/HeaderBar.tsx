type Props = {
  apiBase: string;
  loading: boolean;
  onRefresh: () => void;
};

export function HeaderBar({ apiBase, loading, onRefresh }: Props) {
  return (
    <header className="flex items-center justify-between gap-4">
      <div>
        <p className="text-sm uppercase tracking-[0.3em] text-sky-300/80">
          ParkVision Control
        </p>
        <h1 className="text-3xl font-semibold text-sky-50">Live Lot Dashboard</h1>
      </div>
      <div className="flex items-center gap-3">
        <button
          onClick={onRefresh}
          className="rounded-full bg-gradient-to-r from-sky-400 to-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 shadow-lg shadow-sky-500/40 transition hover:from-sky-300 hover:to-cyan-400"
        >
          {loading ? "Refreshing..." : "Refresh"}
        </button>
        <div className="text-xs text-slate-400">
          API: {apiBase.replace("http://", "").replace("https://", "")}
        </div>
      </div>
    </header>
  );
}
