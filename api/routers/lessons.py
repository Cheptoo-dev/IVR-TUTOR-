from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

router = APIRouter()

# Enums
class LessonStatus(str, Enum):
    draft = "draft"
    active = "active"
    completed = "completed"
    archived = "archived"

class LessonType(str, Enum):
    audio = "audio"
    interactive = "interactive"
    quiz = "quiz"
    exercise = "exercise"

# Pydantic models
class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: str
    lesson_type: LessonType
    duration_minutes: Optional[int] = None

class LessonCreate(LessonBase):
    pass

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    lesson_type: Optional[LessonType] = None
    duration_minutes: Optional[int] = None
    status: Optional[LessonStatus] = None

class Lesson(LessonBase):
    id: str
    status: LessonStatus
    created_at: datetime
    updated_at: datetime

class LessonProgress(BaseModel):
    lesson_id: str
    student_id: str
    progress_percentage: float
    completed_at: Optional[datetime] = None
    score: Optional[float] = None

@router.get("/")
async def lessons_root():
    """Lessons API root endpoint"""
    return {"message": "Lessons API is running", "version": "1.0.0"}

@router.get("/lessons", response_model=List[Lesson])
async def get_lessons(
    status: Optional[LessonStatus] = None,
    lesson_type: Optional[LessonType] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Get list of lessons with optional filtering"""
    # TODO: Implement actual database query
    sample_lessons = [
        Lesson(
            id="lesson_001",
            title="Introduction to Mathematics",
            description="Basic math concepts for beginners",
            content="Welcome to mathematics! Today we'll learn about numbers...",
            lesson_type=LessonType.interactive,
            duration_minutes=30,
            status=LessonStatus.active,
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        Lesson(
            id="lesson_002",
            title="English Grammar Basics",
            description="Fundamental grammar rules",
            content="Let's explore the building blocks of English grammar...",
            lesson_type=LessonType.audio,
            duration_minutes=25,
            status=LessonStatus.active,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ]
    
    # Apply filters (simplified)
    filtered_lessons = sample_lessons
    if status:
        filtered_lessons = [l for l in filtered_lessons if l.status == status]
    if lesson_type:
        filtered_lessons = [l for l in filtered_lessons if l.lesson_type == lesson_type]
    
    return filtered_lessons[skip:skip+limit]

@router.get("/lessons/{lesson_id}", response_model=Lesson)
async def get_lesson(lesson_id: str):
    """Get a specific lesson by ID"""
    # TODO: Implement actual database lookup
    if lesson_id == "lesson_001":
        return Lesson(
            id=lesson_id,
            title="Introduction to Mathematics",
            description="Basic math concepts for beginners",
            content="Welcome to mathematics! Today we'll learn about numbers...",
            lesson_type=LessonType.interactive,
            duration_minutes=30,
            status=LessonStatus.active,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    raise HTTPException(status_code=404, detail="Lesson not found")

@router.post("/lessons", response_model=Lesson)
async def create_lesson(lesson: LessonCreate):
    """Create a new lesson"""
    # TODO: Implement actual database creation
    new_lesson = Lesson(
        id=f"lesson_{hash(lesson.title) % 10000}",
        **lesson.dict(),
        status=LessonStatus.draft,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    return new_lesson

@router.put("/lessons/{lesson_id}", response_model=Lesson)
async def update_lesson(lesson_id: str, lesson_update: LessonUpdate):
    """Update an existing lesson"""
    # TODO: Implement actual database update
    existing_lesson = await get_lesson(lesson_id)  # This will raise 404 if not found
    
    # Update fields that are provided
    update_data = lesson_update.dict(exclude_unset=True)
    updated_lesson = existing_lesson.copy(update=update_data)
    updated_lesson.updated_at = datetime.now()
    
    return updated_lesson

@router.delete("/lessons/{lesson_id}")
async def delete_lesson(lesson_id: str):
    """Delete a lesson"""
    # TODO: Implement actual database deletion
    # First check if lesson exists
    await get_lesson(lesson_id)  # This will raise 404 if not found
    return {"message": f"Lesson {lesson_id} deleted successfully"}

@router.get("/lessons/{lesson_id}/progress", response_model=List[LessonProgress])
async def get_lesson_progress(lesson_id: str):
    """Get progress for all students on a specific lesson"""
    # TODO: Implement actual progress tracking
    return [
        LessonProgress(
            lesson_id=lesson_id,
            student_id="student_001",
            progress_percentage=75.0,
            score=85.5
        )
    ]

@router.post("/lessons/{lesson_id}/start")
async def start_lesson(lesson_id: str, student_id: str):
    """Start a lesson for a student"""
    # TODO: Implement lesson start logic
    return {
        "lesson_id": lesson_id,
        "student_id": student_id,
        "status": "started",
        "message": "Lesson started successfully"
    }