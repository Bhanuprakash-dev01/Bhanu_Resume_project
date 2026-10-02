import { AgentDashboard } from "@/components/AgentDashboard";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-100 p-6">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.2em] text-blue-600">Operations AI</p>
            <h1 className="text-3xl font-bold text-slate-900">Delivery Support Resolution Agent</h1>
          </div>
          <div className="rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm text-slate-600 shadow-sm">
            4 active workflows · 2 pending approvals
          </div>
        </header>

        <AgentDashboard />
      </div>
    </main>
  );
}
