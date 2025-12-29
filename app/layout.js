import "./globals.css"

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-800">
        {children}
      </body>
    </html>
  )
}

<div className="sticky top-0 z-50 bg-white border-b shadow-sm">
  <div className="max-w-7xl mx-auto flex justify-between items-center p-4">
    <div className="font-bold text-xl">💸 Finance AI</div>
    <div className="flex items-center gap-4 text-sm">
      <span className="text-gray-500">Welcome, Axel</span>
      <button className="bg-black text-white px-4 py-2 rounded-xl">Upgrade</button>
    </div>
  </div>
</div>

