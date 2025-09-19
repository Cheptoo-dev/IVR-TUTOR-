from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

# Pydantic models
class DashboardStats(BaseModel):
    total_students: int
    active_lessons: int
    completed_lessons: int
    total_calls: int
    success_rate: float

class RecentActivity(BaseModel):
    id: str
    type: str  # "lesson", "call", "sms"
    description: str
    timestamp: datetime
    status: str

class DashboardData(BaseModel):
    stats: DashboardStats
    recent_activities: List[RecentActivity]

@router.get("/")
async def dashboard_root():
    """Dashboard API root endpoint"""
    return {"message": "Dashboard API is running", "version": "1.0.0"}

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get overall dashboard statistics"""
    # TODO: Implement actual stats calculation from database
    return DashboardStats(
        total_students=150,
        active_lessons=45,
        completed_lessons=230,
        total_calls=1250,
        success_rate=85.5
    )

@router.get("/recent-activity", response_model=List[RecentActivity])
async def get_recent_activity(limit: int = 10):
    """Get recent activity feed"""
    # TODO: Implement actual recent activity from database
    sample_activities = [
        RecentActivity(
            id="act_001",
            type="lesson",
            description="Student John completed Math Lesson 5",
            timestamp=datetime.now(),
            status="completed"
        ),
        RecentActivity(
            id="act_002",
            type="call",
            description="Automated call to remind about homework",
            timestamp=datetime.now(),
            status="successful"
        )
    ]
    return sample_activities[:limit]

@router.get("/overview", response_model=DashboardData)
async def get_dashboard_overview():
    """Get complete dashboard overview"""
    stats = await get_dashboard_stats()
    activities = await get_recent_activity(5)
    
    return DashboardData(
        stats=stats,
        recent_activities=activities
    )

@router.get("/performance/{time_period}")
async def get_performance_data(time_period: str):
    """Get performance data for specified time period (day, week, month)"""
    # TODO: Implement performance analytics
    if time_period not in ["day", "week", "month"]:
        raise HTTPException(status_code=400, detail="Invalid time period")
    
    return {
        "period": time_period,
        "metrics": {
            "lesson_completion_rate": 78.5,
            "call_success_rate": 85.2,
            "student_engagement": 92.1
        }
    }