import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.api.player import router as player_router
from backend.api.team import router as team_router
from backend.api.venue import router as venue_router
from backend.api.analytics import router as analytics_router
from backend.api.prediction import router as prediction_router
from backend.api.comparison import router as comparison_router

app = FastAPI(
    title="CricketIQ AI API",
    description="Backend API for CricketIQ AI Sports Analytics Platform",
    version="2.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(player_router)
app.include_router(team_router)
app.include_router(venue_router)
app.include_router(analytics_router)
app.include_router(prediction_router)
app.include_router(comparison_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "platform": "CricketIQ AI",
        "version": "2.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
