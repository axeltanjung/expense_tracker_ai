export default function GlassCard({ children }) {
  return (
    <div className="bg-[#0f1324] border border-white/10 rounded-2xl shadow-2xl backdrop-blur-xl p-6 text-[var(--text-main)]">
      {children}
    </div>
  )
}
