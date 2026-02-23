import { useState, useEffect } from 'react';

export interface Message {
    role: 'user' | 'assistant' | 'system';
    content: string;
}

export interface Conversation {
    id: string;
    title: string;
    messages: Message[];
    createdAt: number;
    updatedAt: number;
}

const STORAGE_KEY = 'chat_history';

export function useChatHistory(): {
    conversations: Conversation[];
    currentConversationId: string | null;
    currentConversation: Conversation | null;
    createNewConversation: () => string;
    deleteConversation: (id: string) => void;
    updateConversation: (id: string, messages: Message[]) => void;
    setCurrentConversationId: (id: string | null) => void;
} {
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);

    // Load conversations from localStorage on mount
    useEffect(() => {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            try {
                const parsed = JSON.parse(stored);
                setConversations(parsed);
                // Set the most recent conversation as current
                if (parsed.length > 0) {
                    setCurrentConversationId(parsed[0].id);
                }
            } catch (e) {
                console.error('Failed to parse chat history:', e);
            }
        }
    }, []);

    // Save conversations to localStorage whenever they change
    useEffect(() => {
        if (conversations.length > 0) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
        }
    }, [conversations]);

    const createNewConversation = () => {
        const newConv: Conversation = {
            id: Date.now().toString(),
            title: 'New Chat',
            messages: [
                {
                    role: 'assistant',
                    content: 'Hello! I am your AI Analyst. You can ask me questions or click the attachment icon to upload a feedback CSV.'
                }
            ],
            createdAt: Date.now(),
            updatedAt: Date.now()
        };
        setConversations(prev => [newConv, ...prev]);
        setCurrentConversationId(newConv.id);
        return newConv.id;
    };

    const deleteConversation = (id: string) => {
        setConversations(prev => prev.filter(c => c.id !== id));
        if (currentConversationId === id) {
            const remaining = conversations.filter(c => c.id !== id);
            setCurrentConversationId(remaining.length > 0 ? remaining[0].id : null);
        }
    };

    const updateConversation = (id: string, messages: Message[]) => {
        setConversations(prev => prev.map(conv => {
            if (conv.id === id) {
                // Auto-generate title from first user message if still "New Chat"
                let title = conv.title;
                if (title === 'New Chat' && messages.length > 1) {
                    const firstUserMsg = messages.find(m => m.role === 'user');
                    if (firstUserMsg) {
                        title = firstUserMsg.content.slice(0, 50) + (firstUserMsg.content.length > 50 ? '...' : '');
                    }
                }
                return {
                    ...conv,
                    messages,
                    title,
                    updatedAt: Date.now()
                };
            }
            return conv;
        }));
    };

    const getCurrentConversation = (): Conversation | null => {
        return conversations.find(c => c.id === currentConversationId) || null;
    };

    return {
        conversations,
        currentConversationId,
        currentConversation: getCurrentConversation(),
        createNewConversation,
        deleteConversation,
        updateConversation,
        setCurrentConversationId
    };
}
