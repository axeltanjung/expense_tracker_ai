"use client"
import Sidebar from "@/components/Sidebar"
import Topbar from "@/components/TopBar"
import GlassCard from "@/components/GlassCard"
import SwipeLayer from "@/components/SwipeLayer"
import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { LineChart, Line, XAxis, YAxis, Tooltip, BarChart, Bar } from "recharts"

export default function Home() {  
  const USER_ID = "ac6fce9e-aeb2-44c2-be90-20e40e9f4c3e"
  const [spend, setSpend] = useState(null)
  const [risk, setRisk] = useState([])
  const [whatif, setWhatIf] = useState(null)
  const [extra, setExtra] = useState(0)
  const [scenarios, setScenarios] = useState([])
  const [fire, setFire] = useState(null)
  const [newAmt, setNewAmt] = useState("")
  const [newMerchant, setNewMerchant] = useState("")
  const [saving, setSaving] = useState(false)

  useEffect(()=>{
    api.get(`/insights/fire?user_id=${USER_ID}`).then(r=>setFire(r.data))
  },[])

  const saveScenario = () => {
    api.post("/insights/scenario", {
      user_id: USER_ID,
      name: `Scenario ${scenarios.length+1}`,
      extra_monthly_cost: extra
    }).then(()=> loadScenarios())
  }

  const loadScenarios = () =>
    api.get(`/insights/scenario?user_id=${USER_ID}`)
      .then(r => setScenarios(r.data))

  const runSim = (v) => {
    setExtra(v)
    api.post("/insights/whatif", {
      user_id: "ac6fce9e-aeb2-44c2-be90-20e40e9f4c3e",
      extra_monthly_cost: v
    }).then(r => setWhatIf(r.data))
  }

  const addExpense = () => {
    setSaving(true)
    api.post("/txn", {
      user_id: USER_ID,
      amount: Number(newAmt),
      merchant: newMerchant,
      direction: "out"
    }).then(()=>{
      setSaving(false)
      setNewAmt("")
      setNewMerchant("")
      window.location.reload() // simple re-sync
    })
  }
 
  const [behavior, setBehavior] = useState([])
  useEffect(()=>{
    api.get(`/insights/behavior?user_id=${USER_ID}`).then(r=>setBehavior(r.data))
  },[])

  const uploadReceipt = (file) => {
    const f = new FormData()
    f.append("file", file)
    api.post("/txn/ocr", f).then(r=>{
      setNewMerchant(r.data.merchant)
      setNewAmt(r.data.amount)
    })
  }

  const startVoice = ()=>{
    const rec = new window.webkitSpeechRecognition()
    rec.lang="id-ID"
    rec.onresult=e=>{
      const t = e.results[0][0].transcript
      const m = t.match(/(\d+)/)
      if(m) setNewAmt(Number(m[1]))
      setNewMerchant(t.replace(m[1],""))
    }
    rec.start()
  }

  useEffect(() => {
    const USER_ID = "ac6fce9e-aeb2-44c2-be90-20e40e9f4c3e";
    api.get(`/insights/spend?user_id=${USER_ID}`).then(r => setSpend(r.data))
    api.get(`/insights/risk?user_id=${USER_ID}`).then(r => setRisk(r.data))
  }, [])

  if (!spend) return <div className="p-10">Loading...</div>

  return (
  <>
    <SwipeLayer />
    <Sidebar />

    <div className="ml-20 min-h-screen">
      <Topbar />

      <div className="max-w-7xl mx-auto p-8 space-y-8">

        {/* HERO */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold text-[var(--text-main)]">Your Financial Cockpit</h1>
            <p className="text-[var(--text-soft)]">AI-powered spending & decision intelligence</p>
          </div>
          <span className="bg-violet-600 px-4 py-2 rounded-xl text-sm shadow-lg">LIVE</span>
        </div>

        {/* KPI */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <GlassCard>
            <p className="text-xs text-[var(--text-soft)]">7D SPEND</p>
            <p className="text-3xl font-bold mt-2">Rp {spend.spend_7d.toLocaleString()}</p>
          </GlassCard>
          <GlassCard>
            <p className="text-xs text-[var(--text-soft)]">30D SPEND</p>
            <p className="text-3xl font-bold mt-2">Rp {spend.spend_30d.toLocaleString()}</p>
          </GlassCard>
          <GlassCard>
            <p className="text-xs text-[var(--text-soft)]">90D SPEND</p>
            <p className="text-3xl font-bold mt-2">Rp {spend.spend_90d.toLocaleString()}</p>
          </GlassCard>
        </div>

        {/* GRID */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

          {/* LEFT */}
          <div className="space-y-6">
            <GlassCard>
              <p className="mb-2 text-sm text-[var(--text-soft)]">Cashflow</p>
              <div className="h-40 bg-gradient-to-br from-indigo-500/40 to-purple-600/20 rounded-xl"/>
            </GlassCard>

            <GlassCard>
              <h3 className="font-semibold mb-2">Quick Add Expense</h3>
              <input value={newMerchant} onChange={e=>setNewMerchant(e.target.value)} placeholder="Merchant" className="bg-white/5 rounded-xl p-2 w-full mb-2"/>
              <input value={newAmt} onChange={e=>setNewAmt(e.target.value)} placeholder="Amount" className="bg-white/5 rounded-xl p-2 w-full mb-3"/>
              <button onClick={addExpense} className="w-full bg-violet-600 hover:bg-violet-500 transition py-2 rounded-xl">Add Expense</button>
            </GlassCard>
          </div>

          {/* CENTER */}
          <div className="space-y-6">
            <GlassCard>
              <h3 className="font-semibold mb-2">What-If Simulator</h3>
              <input type="range" min="0" max="5000000" step="50000" value={extra} onChange={e=>runSim(Number(e.target.value))} className="w-full"/>
              {whatif && (
                <div className="mt-3 text-sm space-y-1">
                  <p>Projected Net: {Math.round(whatif.projected_net_30d).toLocaleString()}</p>
                  <p>Runway: {whatif.runway_days} days</p>
                  <p className={whatif.risk==="SAFE"?"text-green-400":"text-red-400"}>{whatif.risk}</p>
                </div>
              )}
            </GlassCard>

            {fire && (
              <GlassCard>
                <p className="text-sm text-[var(--text-soft)]">FIRE Projection</p>
                <p className="text-2xl font-bold mt-1">{fire.months_to_fire} months</p>
              </GlassCard>
            )}
          </div>

          {/* RIGHT */}
          <div className="space-y-4">
            {behavior.map((b,i)=>(
              <div key={i} className="bg-yellow-500/10 border border-yellow-500/30 p-4 rounded-xl">
                <p className="text-xs uppercase text-yellow-400">Behavior</p>
                <p className="font-semibold">{b.flag_type}</p>
                <p className="text-sm text-[var(--text-soft)]">{b.message}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* FLOATING */}
      <div className="fixed bottom-6 right-6 bg-violet-600 px-6 py-3 rounded-full shadow-xl flex gap-4 z-50">
        <button onClick={startVoice}>🎙</button>
        <label>
          📸
          <input hidden type="file" onChange={e=>uploadReceipt(e.target.files[0])}/>
        </label>
      </div>
    </div>
  </>
)

}

const KPI = ({title,value}) => (
  <div className="bg-white rounded-2xl p-6 shadow-lg border">
    <p className="text-xs uppercase tracking-wider text-[var(--text-soft)]">{title}</p>
    <p className="text-3xl font-bold mt-1">Rp {Math.round(value).toLocaleString()}</p>
  </div>
)
