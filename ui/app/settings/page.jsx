"use client"
import GlassCard from "@/components/GlassCard"

export default function Settings() {
  return (
    <div className="ml-0 md:ml-20 max-w-4xl mx-auto p-10 space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>

      <GlassCard>
        <label className="flex justify-between items-center">
          <span>Enable AI Spending Guard</span>
          <input type="checkbox" className="accent-violet-500"/>
        </label>
      </GlassCard>

      <GlassCard>
        <label className="flex justify-between items-center">
          <span>Auto Categorize Transactions</span>
          <input type="checkbox" className="accent-violet-500"/>
        </label>
      </GlassCard>
    </div>
  )
}
