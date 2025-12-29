"use client"
import { useEffect, useState } from "react"
import { api } from "@/lib/api"

export default function Transactions() {
  const USER_ID = "ac6fce9e-aeb2-44c2-be90-20e40e9f4c3e"
  const [rows, setRows] = useState([])

  useEffect(()=>{
    api.get(`/txn?user_id=${USER_ID}`).then(r=>setRows(r.data))
  },[])

  return (
    <div className="ml-0 md:ml-20 max-w-6xl mx-auto p-10">
      <h1 className="text-3xl font-bold mb-6">Transactions</h1>

      <table className="w-full text-sm rounded-xl overflow-hidden">
        <thead className="bg-white/5 text-[var(--text-soft)]">
          <tr>
            <th className="p-3">Date</th>
            <th>Merchant</th>
            <th>Amount</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(r=>(
            <tr key={r.id} className="border-b border-white/5">
              <td className="p-3">{r.datetime}</td>
              <td>{r.merchant}</td>
              <td className={r.direction==="out"?"text-red-400":"text-green-400"}>
                {r.amount.toLocaleString()}
              </td>
              <td>{r.direction}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
