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

  if (mode === "exit") {
    if (stage === "at_gate") return scene.exit || scene.entry;
    if (stage === "exited") return scene.lot_after || scene.lot_before || scene.exit;
    return scene.exit || scene.lot_before || scene.entry;
  }

  switch (stage) {
    case "at_gate":
    case "opening":
      return scene.entry || scene.lot_before;
    case "moving_in":
      return scene.lot_before || scene.entry;
    case "searching":
    case "parked":
      return scene.lot_after || scene.lot_before || scene.entry;
    default:
      return scene.entry || scene.lot_after || scene.lot_before || scene.exit;
  }
}

export function SceneMedia({ scenes, sceneId, stage, mode }: Props) {
  const scene = (sceneId && scenes[sceneId]) || null;
  const primaryImg = scene ? pickImage(scene, stage, mode) : null;
  const beforeImg = scene?.lot_before || null;
  const afterImg = scene?.lot_after || null;

  return (
    <div className="rounded-2xl bg-linear-to-b from-slate-900 to-slate-950/60 p-4 shadow-xl shadow-black/40 ring-1 ring-white/5">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
          Image to Models
        </p>
        <span className="text-[11px] text-slate-500">
          {sceneId ? `Scene ${sceneId}` : "Idle"}
        </span>
      </div>

      <div className="flex flex-col gap-3">
        <div className="relative overflow-hidden rounded-xl border border-slate-800 bg-slate-900/60 shadow-inner shadow-black/50 ring-1 ring-white/5">
          <div className="relative aspect-video bg-slate-800/60">
            {primaryImg ? (
              <Image
                src={primaryImg.replace(/^\.\//, "/")}
                alt={`Scene ${sceneId || ""} media`}
                fill
                className="object-cover"
                sizes="100vw"
                unoptimized
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

        <div className="grid grid-cols-2 gap-3">
          <div className="overflow-hidden rounded-lg border border-slate-800 bg-slate-900/60 shadow-inner shadow-black/40 ring-1 ring-white/5">
            <div className="relative aspect-video bg-slate-800/60">
              {beforeImg ? (
                <Image
                  src={beforeImg.replace(/^\.\//, "/")}
                  alt={`Scene ${sceneId || ""} before`}
                  fill
                  className="object-cover"
                  sizes="50vw"
                  unoptimized
                />
              ) : (
                <div className="flex h-full items-center justify-center text-xs text-slate-500">
                  No before image
                </div>
              )}
            </div>
            <div className="px-3 py-2 text-xs uppercase tracking-wide text-slate-300">
              Before
            </div>
          </div>

          <div className="overflow-hidden rounded-lg border border-slate-800 bg-slate-900/60 shadow-inner shadow-black/40 ring-1 ring-white/5">
            <div className="relative aspect-video bg-slate-800/60">
              {afterImg ? (
                <Image
                  src={afterImg.replace(/^\.\//, "/")}
                  alt={`Scene ${sceneId || ""} after`}
                  fill
                  className="object-cover"
                  sizes="50vw"
                  unoptimized
                />
              ) : (
                <div className="flex h-full items-center justify-center text-xs text-slate-500">
                  No after image
                </div>
              )}
            </div>
            <div className="px-3 py-2 text-xs uppercase tracking-wide text-slate-300">
              After
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
