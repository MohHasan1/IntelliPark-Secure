import Image from "next/image";
import { GateStage, SceneConfig } from "../types";

type Props = {
  scenes: Record<string, SceneConfig>;
  sceneId: string | null;
  stage: GateStage;
  mode: "entry" | "exit";
};

function pickImage(scene: SceneConfig, stage: GateStage, mode: "entry" | "exit") {
  if (!scene) return null;

  // Map gate stage to best-guess media; fallback order ensures something shows.
  if (mode === "exit") {
    if (stage === "at_gate") return scene.exit || scene.entry || scene.lot_after || scene.lot_before;
    if (stage === "exited") return scene.lot_after || scene.lot_before || scene.exit || scene.entry;
    return scene.exit || scene.lot_after || scene.lot_before || scene.entry;
  }

  switch (stage) {
    case "at_gate":
    case "opening":
      return scene.entry || scene.lot_before || scene.lot_after || scene.exit;
    case "moving_in":
      return scene.lot_before || scene.entry || scene.lot_after || scene.exit;
    case "searching":
      return scene.lot_after || scene.lot_before || scene.entry || scene.exit;
    case "parked":
      return scene.lot_after || scene.lot_before || scene.entry || scene.exit;
    default:
      return scene.entry || scene.lot_after || scene.lot_before || scene.exit;
  }
}

export function SceneMedia({ scenes, sceneId, stage, mode }: Props) {
  const scene = (sceneId && scenes[sceneId]) || null;
  const img = scene ? pickImage(scene, stage, mode) : null;

  return (
    <div className="rounded-2xl bg-gradient-to-b from-slate-900 to-slate-950/60 p-4 shadow-xl shadow-black/40 ring-1 ring-white/5">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
          Scene Media
        </p>
        <span className="text-[11px] text-slate-500">
          {sceneId ? `Scene ${sceneId}` : "Idle"}
        </span>
      </div>

      <div className="relative overflow-hidden rounded-xl border border-slate-800 bg-slate-900/60 shadow-inner shadow-black/50 ring-1 ring-white/5">
        <div className="relative aspect-video bg-slate-800/60">
          {img ? (
            <Image
              src={img.replace(/^\.\//, "/")}
              alt={`Scene ${sceneId || ""} media`}
              fill
              className="object-cover"
            />
          ) : (
            <div className="flex h-full items-center justify-center text-xs text-slate-500">
              No media
            </div>
          )}
        </div>
        <div className="flex items-center justify-between px-3 py-2 text-sm text-slate-100">
          <span className="font-semibold capitalize">{stage}</span>
          <span
            className={`rounded-full px-2 py-1 text-[11px] uppercase tracking-wide ${
              mode === "exit"
                ? "bg-red-500/15 text-red-100 ring-1 ring-red-500/30"
                : "bg-emerald-500/15 text-emerald-100 ring-1 ring-emerald-500/30"
            }`}
          >
            {mode}
          </span>
        </div>
      </div>
    </div>
  );
}
