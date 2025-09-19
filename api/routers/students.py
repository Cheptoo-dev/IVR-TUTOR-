from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

router = APIRouter()

# Enums
class StudentStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    graduated = "graduated"

# Pydantic models
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone_number: str
    grade_level: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    grade_level: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    status: Optional[StudentStatus] = None

class Student(StudentBase):
    id: str
    status: StudentStatus
    enrollment_date: datetime
    last_activity: Optional[datetime] = None
    total_lessons_completed: int = 0

class StudentProgress(BaseModel):
    student_id: str
    total_lessons: int
    completed_lessons: int
    in_progress_lessons: int
    average_score: Optional[float] = None
    last_lesson_date: Optional[datetime] = None

class StudentActivity(BaseModel):
    id: str
    student_id: str
    activity_type: str  # "lesson", "quiz", "call", "sms"
    description: str
    timestamp: datetime
    result: Optional[str] = None

@router.get("/")
async def students_root():
    """Students API root endpoint"""
    return {"message": "Students API is running", "version": "1.0.0"}

@router.get("/students", response_model=List[Student])
async def get_students(
    status: Optional[StudentStatus] = None,
    grade_level: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Get list of students with optional filtering"""
    # TODO: Implement actual database query
    sample_students = [
        Student(
            id="student_001",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
            grade_level="Grade 8",
            guardian_name="Jane Doe",
            guardian_phone="+1234567891",
            status=StudentStatus.active,
            enrollment_date=datetime.now(),
            last_activity=datetime.now(),
            total_lessons_completed=15
        ),
        Student(
            id="student_002",
            first_name="Mary",
            last_name="Smith",
            email="mary.smith@example.com",
            phone_number="+1234567892",
            grade_level="Grade 7",
            guardian_name="Robert Smith",
            guardian_phone="+1234567893",
            status=StudentStatus.active,
            enrollment_date=datetime.now(),
            last_activity=datetime.now(),
            total_lessons_completed=22
        )
    ]
    
    # Apply filters (simplified)
    filtered_students = sample_students
    if status:
        filtered_students = [s for s in filtered_students if s.status == status]
    if grade_level:
        filtered_students = [s for s in filtered_students if s.grade_level == grade_level]
    if search:
        search_lower = search.lower()
        filtered_students = [
            s for s in filtered_students 
            if search_lower in s.first_name.lower() or search_lower in s.last_name.lower()
        ]
    
    return filtered_students[skip:skip+limit]

@router.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: str):
    """Get a specific student by ID"""
    # TODO: Implement actual database lookup
    if student_id == "student_001":
        return Student(
            id=student_id,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
            grade_level="Grade 8",
            guardian_name="Jane Doe",
            guardian_phone="+1234567891",
            status=StudentStatus.active,
            enrollment_date=datetime.now(),
            last_activity=datetime.now(),
            total_lessons_completed=15
        )
    raise HTTPException(status_code=404, detail="Student not found")

@router.post("/students", response_model=Student)
async def create_student(student: StudentCreate):
    """Create a new student"""
    # TODO: Implement actual database creation
    new_student = Student(
        id=f"student_{hash(student.phone_number) % 10000}",
        **student.dict(),
        status=StudentStatus.active,
        enrollment_date=datetime.now(),
        total_lessons_completed=0
    )
    return new_student

@router.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: str, student_update: StudentUpdate):
    """Update an existing student"""
    # TODO: Implement actual database update
    existing_student = await get_student(student_id)  # This will raise 404 if not found
    
    # Update fields that are provided
    update_data = student_update.dict(exclude_unset=True)
    updated_student = existing_student.copy(update=update_data)
    
    return updated_student

@router.delete("/students/{student_id}")
async def delete_student(student_id: str):
    """Delete a student"""
    # TODO: Implement actual database deletion
    # First check if student exists
    await get_student(student_id)  # This will raise 404 if not found
    return {"message": f"Student {student_id} deleted successfully"}

@router.get("/students/{student_id}/progress", response_model=StudentProgress)
async def get_student_progress(student_id: str):
    """Get progress summary for a specific student"""
    # TODO: Implement actual progress calculation
    await get_student(student_id)  # Verify student exists
    
    return StudentProgress(
        student_id=student_id,
        total_lessons=50,
        completed_lessons=15,
        in_progress_lessons=3,
        average_score=78.5,
        last_lesson_date=datetime.now()
    )

@router.get("/students/{student_id}/activity", response_model=List[StudentActivity])
async def get_student_activity(student_id: str, limit: int = Query(20, ge=1, le=100)):
    """Get recent activity for a specific student"""
    # TODO: Implement actual activity tracking
    await get_student(student_id)  # Verify student exists
    
    return [
        StudentActivity(
            id="activity_001",
            student_id=student_id,
            activity_type="lesson",
            description="Completed Math Lesson 5",
            timestamp=datetime.now(),
            result="Score: 85%"
        ),
        StudentActivity(
            id="activity_002",
            student_id=student_id,
            activity_type="call",
            description="Received reminder call for homework",
            timestamp=datetime.now(),
            result="Call answered"
        )
    ][:limit]

@router.post("/students/{student_id}/enroll-lesson")
async def enroll_student_in_lesson(student_id: str, lesson_id: str):
    """Enroll a student in a specific lesson"""
    # TODO: Implement actual enrollment logic
    await get_student(student_id)  # Verify student exists
    
    return {
        "student_id": student_id,
        "lesson_id": lesson_id,
        "status": "enrolled",
        "message": "Student successfully enrolled in lesson"
    }