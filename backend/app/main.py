import asyncio
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.database import close_database, get_database
from app.services.energy_simulator import simulator


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_database()
    await db.users.create_index("email", unique=True)
    yield
    await close_database()


app = FastAPI(
    title="Smart Energy AI API",
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
app.include_router(api_router, prefix="/api/v1")


class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, data: dict):
        dead = []
        for ws in self.active:
            try:
                await ws.send_json(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name}


@app.websocket("/ws/energy")
async def websocket_energy(websocket: WebSocket):
    """Real-time simulated energy stream for dashboard."""
    await manager.connect(websocket)
    try:
        while True:
            live = simulator.generate_live_reading()
            agg = simulator.aggregate_usage(live["power_kw"])
            appliances = simulator.estimate_appliances(live["power_kw"])
            payload = {"live": live, "appliances": appliances, **agg}
            await websocket.send_json(payload)
            await asyncio.sleep(settings.simulation_interval_seconds)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# MQTT placeholder — enable when broker is available
async def mqtt_listener_placeholder():
    if not settings.mqtt_enabled:
        return
    # Future: aiomqtt subscribe to settings.mqtt_topic_energy
    pass
