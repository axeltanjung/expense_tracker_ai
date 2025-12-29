"use client"
import { useRouter, usePathname } from "next/navigation"
import { useState } from "react"

const menu = [
  { icon: "🏠", label: "Dashboard", path: "/" },
  { icon: "📊", label: "Insights", path: "/insights" },
  { icon: "💳", label: "Transactions", path: "/transactions" },
  { icon: "🧠", label: "Advisor", path: "/advisor" },
  { icon: "⚙️", label: "Settings", path: "/settings" }
]

export default function Sidebar() {
  const router = useRouter()
  const pathname = usePathname()
  const [open, setOpen] = useState(false)

  const goto = p => { router.push(p); setOpen(false) }

  return (
    <>
      {/* MOBILE HAMBURGER */}
      <button
        aria-label="open-menu"
        onClick={() => setOpen(true)}
        className="md:hidden fixed top-5 left-5 z-50 bg-violet-600 p-2 rounded-xl"
      >
        ☰
      </button>
      
      {/* DESKTOP SIDEBAR */}
      <div className="hidden md:flex fixed left-0 top-0 h-full w-20 bg-black/40 backdrop-blur border-r border-white/10 flex-col items-center py-6 gap-6 z-40">
        <div className="w-10 h-10 bg-violet-600 rounded-xl flex items-center justify-center font-bold shadow-lg shadow-violet-600/40">AI</div>
        {menu.map(m => (
          <NavItem key={m.path} {...m} active={pathname === m.path} onClick={() => goto(m.path)} />
        ))}
      </div>

      {/* MOBILE DRAWER */}
      {open && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur z-50" onClick={() => setOpen(false)}>
          <div
            onClick={e=>e.stopPropagation()}
            className="absolute left-0 top-0 h-full w-64 bg-[#0f1324] p-6 space-y-4"
          >
            <div className="text-xl font-bold mb-6">Finance AI</div>
            {menu.map(m => (
              <button key={m.path} onClick={() => goto(m.path)}
                className={`w-full flex items-center gap-3 p-3 rounded-xl transition
                  ${pathname===m.path ? "bg-violet-600 text-white" : "hover:bg-white/5 text-[var(--text-soft)]"}`}>
                <span>{m.icon}</span> {m.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </>
  )
}

function NavItem({ icon, label, active, onClick }) {
  return (
    <button onClick={onClick}
      className={`w-12 h-12 rounded-xl flex items-center justify-center transition
        ${active ? "bg-violet-600 text-white shadow-lg shadow-violet-600/50" : "hover:bg-white/5 text-[var(--text-soft)]"}`}
      title={label}
    >
      {icon}
    </button>
  )
}
