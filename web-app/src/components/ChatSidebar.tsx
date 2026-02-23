"use client";

import { Trash2, MessageSquare, Plus } from "lucide-react";
import { Conversation } from "@/hooks/useChatHistory";

interface ChatSidebarProps {
    conversations: Conversation[];
    currentConversationId: string | null;
    onSelectConversation: (id: string) => void;
    onNewConversation: () => void;
    onDeleteConversation: (id: string) => void;
}

export default function ChatSidebar({
    conversations,
    currentConversationId,
    onSelectConversation,
    onNewConversation,
    onDeleteConversation
}: ChatSidebarProps) {
    return (
        <div className="w-64 bg-slate-900 border-r border-slate-700 flex flex-col h-full">
            {/* Header */}
            <div className="p-4 border-b border-slate-700">
                <button
                    onClick={onNewConversation}
                    className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors"
                >
                    <Plus className="w-4 h-4" />
                    <span className="font-medium">New Chat</span>
                </button>
            </div>

            {/* Conversation List */}
            <div className="flex-1 overflow-y-auto p-2">
                {conversations.length === 0 ? (
                    <div className="text-center text-slate-400 text-sm mt-8">
                        No conversations yet
                    </div>
                ) : (
                    conversations.map((conv) => (
                        <div
                            key={conv.id}
                            className={`group relative flex items-center gap-2 p-3 rounded-lg mb-1 cursor-pointer transition-colors ${currentConversationId === conv.id
                                ? "bg-slate-800 text-white"
                                : "text-slate-300 hover:bg-slate-800/50"
                                }`}
                            onClick={() => onSelectConversation(conv.id)}
                        >
                            <MessageSquare className="w-4 h-4 flex-shrink-0" />
                            <span className="flex-1 text-sm truncate">{conv.title}</span>
                            <button
                                onClick={(e) => {
                                    e.stopPropagation();
                                    onDeleteConversation(conv.id);
                                }}
                                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-600/20 rounded transition-opacity"
                            >
                                <Trash2 className="w-3 h-3 text-red-400" />
                            </button>
                        </div>
                    ))
                )}
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-slate-700 text-xs text-slate-400">
                {conversations.length} conversation{conversations.length !== 1 ? 's' : ''}
            </div>
        </div>
    );
}
