"""Smart Energy AI — FastAPI application entry."""
import asyncio
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.database import close_db, connect_db, get_database
from app.core.security import decode_access_token
from app.services.energy_simulator import get_simulator


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title=get_settings().app_name,
    description="AI-Based Home Electricity Usage Prediction and Optimization",
    version="1.0.0",
    lifespan=lifespan,
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "docs": "/docs",
        "health": "ok",
    }


@app.get("/health")
async def health():
    try:
        db = get_database()
        await db.command("ping")
        db_ok = True
    except Exception:
        db_ok = False
    return {"status": "healthy" if db_ok else "degraded", "database": db_ok}


class ConnectionManager:
    def __init__(self):
        self.active: dict[str, list[WebSocket]] = {}

    async def connect(self, ws: WebSocket, user_id: str):
        await ws.accept()
        self.active.setdefault(user_id, []).append(ws)

    def disconnect(self, ws: WebSocket, user_id: str):
        if user_id in self.active:
            self.active[user_id] = [c for c in self.active[user_id] if c != ws]

    async def broadcast_user(self, user_id: str, data: dict):
        for ws in self.active.get(user_id, []):
            try:
                await ws.send_json(data)
            except Exception:
                pass


manager = ConnectionManager()


@app.websocket("/ws/energy")
async def websocket_energy(websocket: WebSocket, token: str = ""):
    """Real-time energy stream; pass ?token=JWT"""
    payload = decode_access_token(token) if token else None
    if not payload or "sub" not in payload:
        await websocket.close(code=4001)
        return

    user_id = payload["sub"]
    await manager.connect(websocket, user_id)
    sim = get_simulator(user_id)
    interval = settings.energy_sim_interval_seconds

    try:
        while True:
            reading = sim.next_reading()
            await websocket.send_json(reading)
            await manager.broadcast_user(user_id, reading)
            await asyncio.sleep(interval)
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
