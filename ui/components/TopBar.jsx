export default function Topbar() {
  return (
    <div className="ml-20 p-6 flex justify-between items-center">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      <div className="flex gap-4 items-center">
        <input placeholder="Search..." className="bg-white/5 px-4 py-2 rounded-xl text-sm outline-none"/>
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-violet-500 to-indigo-500"/>
      </div>
    </div>
  )
}
