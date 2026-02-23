import Link from 'next/link';
import { MessageSquare, BrainCircuit } from 'lucide-react';

export default function Navbar() {
    return (
        <nav className="border-b bg-slate-950">
            <div className="container mx-auto px-4 flex h-16 items-center justify-between">
                <Link href="/" className="flex items-center space-x-2 font-bold text-xl text-white">
                    <BrainCircuit className="h-6 w-6 text-indigo-600" />
                    <span>AI Engine</span>
                </Link>
                <div className="flex items-center space-x-6 text-sm font-medium">
                    <Link href="/chat" className="flex items-center gap-2 text-slate-600 hover:text-indigo-600 transition-colors">
                        <MessageSquare className="h-4 w-4" /> AI Analyst
                    </Link>
                </div>
            </div>
        </nav>
    );
}
