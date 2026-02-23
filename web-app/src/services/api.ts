import axios from "axios";

// Use relative path for internal API routes
const API_URL = "/api";

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

export interface FeedbackItem {
    source: string;
    content: string;
    rating?: number;
    metadata?: any;
}

export const ingestFeedback = async (items: FeedbackItem[]) => {
    const response = await api.post("/ingest", { items });
    return response.data;
};

export const chatWithAgent = async (question: string) => {
    const response = await api.post("/chat", { question });
    return response.data;
};


