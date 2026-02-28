import { NextResponse } from "next/server";

const BACKEND_URL = process.env.AI_ENGINE_URL || "http://127.0.0.1:8000";
export async function POST(request: Request) {
    try {
        const body = await request.json();

        const res = await fetch(`${BACKEND_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            return NextResponse.json(errorData, { status: res.status });
        }

        const data = await res.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error("Chat Proxy Error:", error);
        return NextResponse.json({ error: "Failed to connect to AI Engine" }, { status: 500 });
    }
}
