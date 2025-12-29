"use client"
import { useState } from "react"
import GlassCard from "@/components/GlassCard"
import { api } from "@/lib/api"

export default function Advisor() {
  const [q,setQ] = useState("")
  const [a,setA] = useState(null)

  const ask = ()=>{
    api.post("/advisor/ask",{q}).then(r=>setA(r.data))
  }

  return (
    <div className="ml-0 md:ml-20 max-w-4xl mx-auto p-10 space-y-6">
      <h1 className="text-3xl font-bold">AI Financial Advisor</h1>

      <GlassCard>
        <textarea
          value={q}
          onChange={e=>setQ(e.target.value)}
          placeholder="Ask about savings, spending, FIRE, risk..."
          className="w-full bg-white/5 p-3 rounded-xl h-32"
        />
        <button onClick={ask} className="mt-3 bg-violet-600 px-5 py-2 rounded-xl">
          Ask AI
        </button>
      </GlassCard>

      {a && (
        <GlassCard>
          <p className="text-[var(--text-soft)]">Answer</p>
          <p className="mt-2">{a.answer}</p>
        </GlassCard>
      )}
    </div>
  )
}
