const workflowStages = [
  "Triage",
  "Retrieval",
  "Investigation",
  "Validation",
  "Response",
];

const sources = [
  { doc: "Delivery Delay Policy", section: "Support Procedures", excerpt: "Delayed arrivals over 48 hours may qualify for refund or replacement." },
  { doc: "Refund Eligibility", section: "Eligibility Rules", excerpt: "Refunds above $200 require review and approval." },
  { doc: "Customer Communication Rules", section: "Disclosure Rules", excerpt: "Only claim actions after tool confirmation." },
];

export function AgentDashboard() {
  return (
    <div className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-800">Conversation</h2>
          <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700">Status: Active</span>
        </div>

        <div className="space-y-4">
          <div className="rounded-xl bg-slate-100 p-3 text-sm text-slate-700">
            User: “My package has been delayed for over 48 hours. I need a refund.
          </div>
          <div className="rounded-xl bg-blue-50 p-3 text-sm text-blue-800">
            Agent: I checked the order metadata and carrier update. The shipment is delayed and policy review indicates a high-value refund may require human approval.
          </div>
        </div>

        <div className="mt-6 flex gap-3">
          <input
            className="flex-1 rounded-lg border border-slate-300 bg-slate-50 p-3 text-sm outline-none focus:border-blue-500"
            placeholder="Type a support request..."
          />
          <button className="rounded-lg bg-blue-600 px-4 py-3 text-sm font-medium text-white hover:bg-blue-700">
            Run workflow
          </button>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-lg font-semibold text-slate-800">Workflow Panel</h2>
        <div className="space-y-3">
          {workflowStages.map((stage, index) => (
            <div
              key={stage}
              className={`flex items-center justify-between rounded-xl border px-3 py-2 ${
                index === 4 ? "border-blue-200 bg-blue-50 text-blue-700" : "border-slate-200 bg-slate-50 text-slate-700"
              }`}
            >
              <span className="font-medium">{stage}</span>
              <span className="text-xs">{index === 4 ? "Current" : "Complete"}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
        <h2 className="mb-4 text-lg font-semibold text-slate-800">Sources Panel</h2>
        <div className="space-y-3">
          {sources.map((source) => (
            <div key={source.doc} className="rounded-xl border border-slate-200 bg-slate-50 p-3">
              <div className="flex items-center justify-between text-sm">
                <span className="font-semibold text-slate-800">{source.doc}</span>
                <span className="text-slate-500">{source.section}</span>
              </div>
              <p className="mt-2 text-sm text-slate-600">{source.excerpt}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
        <h2 className="mb-4 text-lg font-semibold text-slate-800">Human Approval Panel</h2>
        <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
          <div className="text-sm text-amber-800">
            <p className="font-semibold">Proposed action: Request refund</p>
            <p className="mt-2">Reason: The order is delayed over 48 hours and the refund exceeds the threshold requiring review.</p>
            <p className="mt-2">Evidence: Carrier indicates weather delay; policy says refund may be eligible after 48 hours.</p>
            <p className="mt-2">Confidence: 0.88</p>
          </div>
          <div className="mt-4 flex gap-3">
            <button className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white">Approve</button>
            <button className="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white">Reject</button>
            <button className="rounded-lg bg-slate-200 px-4 py-2 text-sm font-medium text-slate-700">Modify</button>
          </div>
        </div>
      </div>
    </div>
  );
}
