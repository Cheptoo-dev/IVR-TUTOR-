from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Import database and models
from .database import engine, get_db
from . import models

# Import routers
from .routers import voice, sms, students, lessons, dashboard

# Load environment variables
load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=os.getenv("APP_NAME", "IVR Tutor"),
    description="Inclusive Education Platform - Voice-First Learning",
    version=os.getenv("APP_VERSION", "1.0.0"),
    docs_url="/docs" if os.getenv("DEBUG", "True") == "True" else None,
    redoc_url="/redoc" if os.getenv("DEBUG", "True") == "True" else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories if they don't exist
os.makedirs("dashboard/static", exist_ok=True)
os.makedirs("dashboard/templates", exist_ok=True)

# Static files and templates (for simple dashboard)
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")
templates = Jinja2Templates(directory="dashboard/templates")

# Include routers
app.include_router(voice.router, prefix="/api/voice", tags=["Voice/IVR"])
app.include_router(sms.router, prefix="/api/sms", tags=["SMS"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(lessons.router, prefix="/api/lessons", tags=["Lessons"])
app.include_router(dashboard.router, prefix="", tags=["Dashboard"])

@app.get("/")
async def root():
    """API Health Check"""
    return {
        "message": "🎓 IVR Tutor API is running!",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Detailed health check including database"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "version": os.getenv("APP_VERSION", "1.0.0")
    }

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print("🚀 IVR Tutor API starting up...")
    print(f"📊 Database: {os.getenv('DATABASE_URL', 'sqlite:///./ivr_tutor.db')}")
    print(f"🌍 Environment: {os.getenv('AFRICASTALKING_ENVIRONMENT', 'sandbox')}")
    print("✅ Ready to receive calls!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("DEBUG", "True") == "True" else False
    ) 
