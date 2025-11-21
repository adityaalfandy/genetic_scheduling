from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import jadwal_routes, data_routes
import os

app = FastAPI(
    title="Genetic Algorithm Scheduling System",
    description="Sistem Penjadwalan Mata Kuliah dengan Algoritma Genetika",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="app/static")

# Static files
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routes
app.include_router(jadwal_routes.router)
app.include_router(data_routes.router)

@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()
    print("Database initialized successfully")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve frontend"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Genetic Scheduling API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)