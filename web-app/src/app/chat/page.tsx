"use client";

import { useState, useRef, useEffect } from "react";
import { useMutation } from "@tanstack/react-query";
import { chatWithAgent, ingestFeedback } from "@/services/api";
import { Send, User, Bot, Loader2, Paperclip, FileText } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { cn } from "@/lib/utils";
import Papa from "papaparse";
import { useChatHistory, Message } from "@/hooks/useChatHistory";
import ChatSidebar from "@/components/ChatSidebar";
import ProgressIndicator from "@/components/ProgressIndicator";

export default function ChatPage() {
    const [input, setInput] = useState("");
    const [uploadProgress, setUploadProgress] = useState<number | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const {
        conversations,
        currentConversationId,
        currentConversation,
        createNewConversation,
        deleteConversation,
        updateConversation,
        setCurrentConversationId
    } = useChatHistory();

    const messages = currentConversation?.messages || [];

    // Initialize first conversation if none exist
    useEffect(() => {
        if (conversations.length === 0) {
            createNewConversation();
        }
    }, []);

    // Update conversation when messages change
    useEffect(() => {
        if (currentConversationId && messages.length > 0) {
            updateConversation(currentConversationId, messages);
        }
    }, [messages.length]);

    const setMessages = (updater: (prev: Message[]) => Message[]) => {
        if (currentConversationId) {
            const newMessages = updater(messages);
            updateConversation(currentConversationId, newMessages);
        }
    };

    // Chat Mutation with retry logic
    const chatMutation = useMutation({
        mutationFn: chatWithAgent,
        retry: 2,
        retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 3000),
        onSuccess: (data) => {
            const responseText = data.answer || (data.messages ? data.messages[data.messages.length - 1].content : "No response content");
            setMessages((prev) => [...prev, { role: "assistant", content: responseText }]);
        },
        onError: (error: any) => {
            const errorMessage = error?.response?.status === 500
                ? "The AI Engine is currently processing. Please try again in a moment."
                : "Sorry, I encountered an error connecting to the AI Engine.";
            setMessages((prev) => [...prev, { role: "assistant", content: errorMessage }]);
        }
    });

    // Upload Mutation with realistic progress
    const uploadMutation = useMutation({
        mutationFn: async (items: any[]) => {
            // Step 1: Parsing CSV (already done by frontend)
            setUploadProgress(0);
            await new Promise(resolve => setTimeout(resolve, 200));

            // Step 2: Uploading to backend
            setUploadProgress(1);
            const uploadPromise = ingestFeedback(items);

            // Step 3: Simulate RLM Analysis progress (backend is working)
            // Show this step while waiting for backend response
            await new Promise(resolve => setTimeout(resolve, 500));
            setUploadProgress(2);

            // Wait for backend to complete
            const result = await uploadPromise;

            // Step 4: Complete (Graph Storage done)
            setUploadProgress(3);
            await new Promise(resolve => setTimeout(resolve, 300));

            return result;
        },
        onSuccess: (_, variables) => {
            setMessages(prev => [...prev, {
                role: "system",
                content: `✅ RLM Analysis Complete! Processed **${variables.length}** feedback items with hierarchical understanding. Themes identified and stored in graph. You can now ask questions!`
            }]);
            setTimeout(() => setUploadProgress(null), 1000);
        },
        onError: () => {
            setMessages(prev => [...prev, { role: "system", content: "❌ Failed to upload file. Please check the format." }]);
            setUploadProgress(null);
        }
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg: Message = { role: "user", content: input };
        setMessages((prev) => [...prev, userMsg]);
        chatMutation.mutate(input);
        setInput("");
    };

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        setMessages(prev => [...prev, { role: "system", content: `📂 Uploading **${file.name}**...` }]);

        Papa.parse(file, {
            header: true,
            complete: (results) => {
                const items = results.data
                    .filter((row: any) => row.content)
                    .map((row: any) => ({
                        source: row.source || "csv-upload",
                        content: row.content,
                        rating: row.rating ? parseFloat(row.rating) : 3.0,
                        metadata: { ...row }
                    }));

                if (items.length > 0) {
                    uploadMutation.mutate(items);
                } else {
                    setMessages(prev => [...prev, { role: "system", content: "⚠️ No valid rows found. CSV must have a 'content' column." }]);
                }
            },
            error: () => {
                setMessages(prev => [...prev, { role: "system", content: "❌ Error parsing CSV file." }]);
            }
        });

        if (fileInputRef.current) fileInputRef.current.value = "";
    };

    const uploadSteps: Array<{ label: string; status: 'pending' | 'active' | 'complete' }> = [
        { label: "Parsing CSV", status: uploadProgress === 0 ? 'active' as const : uploadProgress && uploadProgress > 0 ? 'complete' as const : 'pending' as const },
        { label: "Uploading", status: uploadProgress === 1 ? 'active' as const : uploadProgress && uploadProgress > 1 ? 'complete' as const : 'pending' as const },
        { label: "RLM Analysis", status: uploadProgress === 2 ? 'active' as const : uploadProgress && uploadProgress > 2 ? 'complete' as const : 'pending' as const },
        { label: "Graph Storage", status: uploadProgress === 3 ? 'complete' as const : 'pending' as const }
    ];

    return (
        <div className="flex h-[calc(100vh-8rem)] bg-slate-950">
            {/* Sidebar */}
            <ChatSidebar
                conversations={conversations}
                currentConversationId={currentConversationId}
                onSelectConversation={setCurrentConversationId}
                onNewConversation={createNewConversation}
                onDeleteConversation={deleteConversation}
            />

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col">
                <header className="p-6 border-b border-slate-700">
                    <h1 className="text-2xl font-bold text-white">AI Analyst</h1>
                    <p className="text-sm text-slate-400">Chat with your data or upload new feedback.</p>
                </header>

                <div className="flex-1 overflow-y-auto p-6 space-y-4">
                    {messages.map((msg, idx) => (
                        <div key={idx} className={cn("flex gap-3", msg.role === "user" ? "flex-row-reverse" : "flex-row")}>
                            <div className={cn("flex h-8 w-8 shrink-0 items-center justify-center rounded-full",
                                msg.role === "user" ? "bg-indigo-600 text-white" :
                                    msg.role === "system" ? "bg-slate-500 text-white" : "bg-emerald-600 text-white")}>
                                {msg.role === "user" ? <User className="h-4 w-4" /> : msg.role === "system" ? <FileText className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                            </div>
                            <div className={cn("rounded-lg px-4 py-2 max-w-[80%]",
                                msg.role === "user" ? "bg-indigo-600 text-white" :
                                    msg.role === "system" ? "bg-slate-800 text-slate-300 italic border border-slate-700" : "bg-slate-800 text-slate-100")}>
                                <div className="prose prose-sm prose-invert max-w-none">
                                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                                </div>
                            </div>
                        </div>
                    ))}

                    {/* Upload Progress */}
                    {uploadProgress !== null && (
                        <ProgressIndicator steps={uploadSteps} currentStep={uploadProgress} />
                    )}

                    {/* Chat Loading */}
                    {chatMutation.isPending && (
                        <div className="flex gap-3">
                            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-600 text-white">
                                <Bot className="h-4 w-4" />
                            </div>
                            <div className="flex items-center gap-2 text-slate-400">
                                <Loader2 className="h-4 w-4 animate-spin" />
                                <span className="text-sm">Thinking...</span>
                            </div>
                        </div>
                    )}
                </div>

                <div className="p-6 border-t border-slate-700">
                    <form onSubmit={handleSubmit} className="flex gap-2">
                        <input
                            type="file"
                            accept=".csv"
                            ref={fileInputRef}
                            className="hidden"
                            onChange={handleFileUpload}
                        />
                        <button
                            type="button"
                            onClick={() => fileInputRef.current?.click()}
                            className="rounded-lg border border-slate-700 bg-slate-800 px-3 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors"
                            title="Upload CSV"
                            disabled={uploadMutation.isPending || chatMutation.isPending}
                        >
                            {uploadMutation.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Paperclip className="h-4 w-4" />}
                        </button>

                        <input
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Message AI or upload a CSV..."
                            className="flex-1 rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-white placeholder-slate-400 focus:border-indigo-500 focus:outline-none"
                            disabled={chatMutation.isPending}
                        />
                        <button
                            type="submit"
                            disabled={chatMutation.isPending || !input.trim()}
                            className="rounded-lg bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700 disabled:opacity-50 transition-colors"
                        >
                            <Send className="h-4 w-4" />
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}
