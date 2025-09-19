from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Student(Base):
    """Student model - tracks learners using the system"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(15), unique=True, index=True)
    name = Column(String(100), nullable=True)
    preferred_language = Column(String(10), default="en")  # en, sw, etc
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    total_lessons_completed = Column(Integer, default=0)
    total_quiz_score = Column(Float, default=0.0)  # Average score
    is_active = Column(Boolean, default=True)
    
    # Relationships
    sessions = relationship("CallSession", back_populates="student")
    progress = relationship("LessonProgress", back_populates="student")
    sms_logs = relationship("SMSLog", back_populates="student")

class CallSession(Base):
    """Track individual call sessions"""
    __tablename__ = "call_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    phone_number = Column(String(15))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    menu_path = Column(JSON, default=list)  # Track navigation: ["main", "math", "addition"]
    lessons_accessed = Column(JSON, default=list)  # List of lesson IDs
    quiz_results = Column(JSON, default=dict)  # {"lesson_1": {"score": 80, "attempts": 2}}
    session_status = Column(String(20), default="active")  # active, completed, abandoned
    
    # Relationships
    student = relationship("Student", back_populates="sessions")

class Lesson(Base):
    """Lesson content and metadata"""
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    subject = Column(String(50))  # math, english, science
    level = Column(String(20))    # beginner, intermediate, advanced
    language = Column(String(10)) # en, sw, etc
    description = Column(Text, nullable=True)
    
    # Content can be either audio file or text-to-speech script
    content_type = Column(String(20), default="tts")  # "audio_file" or "tts"
    content_path = Column(String(500))  # S3 URL for audio or TTS script text
    duration_seconds = Column(Integer, default=60)
    
    # Quiz questions stored as JSON
    quiz_questions = Column(JSON, default=list)
    # Example: [{"question": "What is 2+2?", "options": ["3", "4", "5"], "correct": 1}]
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)  # For sequencing lessons
    
    # Relationships
    progress_records = relationship("LessonProgress", back_populates="lesson")

class LessonProgress(Base):
    """Track student progress through lessons"""
    __tablename__ = "lesson_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    session_id = Column(String(100))  # Link to call session
    
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    quiz_score = Column(Integer, nullable=True)  # Percentage score (0-100)
    quiz_answers = Column(JSON, default=list)  # Student's answers
    attempts = Column(Integer, default=1)
    time_spent_seconds = Column(Integer, default=0)
    status = Column(String(20), default="in_progress")  # in_progress, completed, failed
    
    # Relationships
    student = relationship("Student", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress_records")

class SMSLog(Base):
    """Log all SMS communications"""
    __tablename__ = "sms_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    phone_number = Column(String(15))
    message = Column(Text)
    message_type = Column(String(50))  # progress, reminder, welcome, quiz_result
    sent_at = Column(DateTime, default=datetime.utcnow)
    delivery_status = Column(String(20), default="sent")  # sent, delivered, failed
    cost = Column(String(10), nullable=True)  # Cost from Africa's Talking
    
    # Relationships
    student = relationship("Student", back_populates="sms_logs")

class SystemSettings(Base):
    """Store system configuration"""
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True)
    value = Column(Text)
    description = Column(String(500), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Example system settings that could be stored:
# - daily_reminder_time: "09:00"
# - max_attempts_per_quiz: "3"
# - default_language: "en"
# - welcome_message_template: "Welcome to IVR Tutor, {name}!"
