type Props = {
  isFull: boolean;
};

export function FullLotBanner({ isFull }: Props) {
  if (!isFull) return null;
  return (
    <div className="rounded-xl border border-amber-500/40 bg-amber-500/10 px-4 py-3 text-sm text-amber-100">
      Parking lot is full. No empty spots available.
    </div>
  );
}
