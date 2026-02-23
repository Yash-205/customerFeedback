from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import ingest, chat, health

app = FastAPI(title="Customer Intelligence Engine API")

# --- CORS Configuration ---
# Allow requests from your Next.js frontend (e.g., localhost:3000, Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to ["https://your-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routers ---
app.include_router(health.router, tags=["Health"])
app.include_router(ingest.router, tags=["Ingestion"])
app.include_router(chat.router, tags=["Chat"])
