import Link from "next/link";

type NavItem = {
  href: string;
  label: string;
};

const navItems: NavItem[] = [
  { href: "/", label: "Overview" },
  { href: "/allowed", label: "Allowed Plates" },
  { href: "/find-car", label: "Find Car" },
];

export function Sidebar() {
  return (
    <aside className="hidden min-h-screen w-64 flex-col bg-linear-to-b from-slate-950 to-slate-900/80 px-5 py-6 text-slate-100 shadow-2xl shadow-black/50 ring-1 ring-white/5 lg:flex">
      <div className="mb-8">
        <div className="text-xs uppercase tracking-[0.3em] text-sky-300/80">
          IntelliPark
        </div>
        <div className="text-lg font-semibold text-sky-50">Control</div>
      </div>
      <nav className="flex flex-col gap-2">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="rounded-xl px-3 py-2 text-sm font-semibold text-slate-100 transition hover:bg-slate-800/80 hover:text-sky-100"
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
