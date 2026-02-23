"use client";

import { Loader2 } from "lucide-react";

interface ProgressStep {
    label: string;
    status: 'pending' | 'active' | 'complete';
}

interface ProgressIndicatorProps {
    steps: ProgressStep[];
    currentStep?: number;
}

export default function ProgressIndicator({ steps, currentStep }: ProgressIndicatorProps) {
    return (
        <div className="flex items-center gap-3 p-4 bg-slate-800/50 rounded-lg border border-slate-700">
            {steps.map((step, index) => {
                const isActive = currentStep !== undefined ? index === currentStep : step.status === 'active';
                const isComplete = currentStep !== undefined ? index < currentStep : step.status === 'complete';

                return (
                    <div key={index} className="flex items-center gap-2">
                        <div className="flex items-center gap-2">
                            {isActive && <Loader2 className="w-4 h-4 animate-spin text-indigo-400" />}
                            {isComplete && (
                                <svg className="w-4 h-4 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                            )}
                            {!isActive && !isComplete && (
                                <div className="w-4 h-4 rounded-full border-2 border-slate-600" />
                            )}
                            <span className={`text-sm ${isActive ? 'text-indigo-400 font-medium' :
                                    isComplete ? 'text-green-400' :
                                        'text-slate-400'
                                }`}>
                                {step.label}
                            </span>
                        </div>
                        {index < steps.length - 1 && (
                            <div className={`w-8 h-0.5 ${isComplete ? 'bg-green-400' : 'bg-slate-700'}`} />
                        )}
                    </div>
                );
            })}
        </div>
    );
}
