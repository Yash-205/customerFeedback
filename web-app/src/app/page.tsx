import Link from "next/link";
import { ArrowRight, MessageSquare } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] text-center space-y-8">
      <div className="space-y-4 max-w-2xl">
        <h1 className="text-5xl font-extrabold tracking-tight sm:text-6xl bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-600">
          Customer Intelligence Engine
        </h1>
        <p className="text-xl text-slate-400">
          Turn scattered feedback into actionable insights. Chat with your data or upload CSVs directly to the AI Analyst.
        </p>
      </div>

      <div className="w-full max-w-sm mt-12">
        <Link href="/chat" className="block group rounded-2xl border bg-slate-900 border-slate-800 p-6 shadow-sm hover:shadow-md transition-all">
          <div className="h-12 w-12 rounded-lg bg-emerald-100 text-emerald-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform mx-auto">
            <MessageSquare className="h-6 w-6" />
          </div>
          <h3 className="text-lg font-semibold mb-2">AI Analyst & Upload</h3>
          <p className="text-slate-500 text-sm">Chat with the agent and upload new CSV feedback files in one place.</p>
        </Link>
      </div>

      <div className="mt-12">
        <Link href="/chat" className="inline-flex items-center gap-2 rounded-full bg-white px-6 py-3 text-slate-900 hover:bg-slate-200 transition-colors">
          Start Analysis <ArrowRight className="h-4 w-4" />
        </Link>
      </div>
    </div>
  );
}
