from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

router = APIRouter()

# Enums
class MessageStatus(str, Enum):
    pending = "pending"
    sent = "sent"
    delivered = "delivered"
    failed = "failed"
    read = "read"

class MessageType(str, Enum):
    reminder = "reminder"
    notification = "notification"
    welcome = "welcome"
    alert = "alert"
    custom = "custom"

# Pydantic models
class SMSBase(BaseModel):
    recipient_phone: str
    message: str
    message_type: MessageType = MessageType.custom

class SMSSend(SMSBase):
    scheduled_time: Optional[datetime] = None

class SMSBulk(BaseModel):
    recipient_phones: List[str]
    message: str
    message_type: MessageType = MessageType.custom
    scheduled_time: Optional[datetime] = None

class SMS(SMSBase):
    id: str
    status: MessageStatus
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    failed_reason: Optional[str] = None
    cost: Optional[float] = None

class SMSTemplate(BaseModel):
    id: str
    name: str
    content: str
    message_type: MessageType
    variables: List[str] = []  # List of variables that can be replaced like {student_name}

class SMSStats(BaseModel):
    total_sent: int
    total_delivered: int
    total_failed: int
    delivery_rate: float
    total_cost: float

class IncomingSMS(BaseModel):
    from_phone: str
    message: str
    received_at: datetime
    processed: bool = False

@router.get("/")
async def sms_root():
    """SMS API root endpoint"""
    return {"message": "SMS API is running", "version": "1.0.0"}

@router.post("/send", response_model=SMS)
async def send_sms(sms_data: SMSSend):
    """Send a single SMS message"""
    # TODO: Implement actual SMS sending logic (Twilio, etc.)
    new_sms = SMS(
        id=f"sms_{hash(sms_data.recipient_phone + sms_data.message) % 100000}",
        recipient_phone=sms_data.recipient_phone,
        message=sms_data.message,
        message_type=sms_data.message_type,
        status=MessageStatus.sent,
        sent_at=datetime.now(),
        cost=0.0075  # Example cost per SMS
    )
    
    # If scheduled, set status to pending
    if sms_data.scheduled_time and sms_data.scheduled_time > datetime.now():
        new_sms.status = MessageStatus.pending
        new_sms.sent_at = None
    
    return new_sms

@router.post("/send-bulk")
async def send_bulk_sms(bulk_data: SMSBulk):
    """Send SMS to multiple recipients"""
    # TODO: Implement actual bulk SMS sending logic
    sent_messages = []
    
    for phone in bulk_data.recipient_phones:
        sms = SMS(
            id=f"sms_{hash(phone + bulk_data.message) % 100000}",
            recipient_phone=phone,
            message=bulk_data.message,
            message_type=bulk_data.message_type,
            status=MessageStatus.sent,
            sent_at=datetime.now(),
            cost=0.0075
        )
        
        if bulk_data.scheduled_time and bulk_data.scheduled_time > datetime.now():
            sms.status = MessageStatus.pending
            sms.sent_at = None
            
        sent_messages.append(sms)
    
    return {
        "total_queued": len(sent_messages),
        "messages": sent_messages,
        "estimated_cost": len(sent_messages) * 0.0075
    }

@router.get("/messages", response_model=List[SMS])
async def get_messages(
    status: Optional[MessageStatus] = None,
    message_type: Optional[MessageType] = None,
    recipient_phone: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Get list of SMS messages with optional filtering"""
    # TODO: Implement actual database query
    sample_messages = [
        SMS(
            id="sms_001",
            recipient_phone="+1234567890",
            message="Reminder: You have a lesson tomorrow at 2 PM",
            message_type=MessageType.reminder,
            status=MessageStatus.delivered,
            sent_at=datetime.now(),
            delivered_at=datetime.now(),
            cost=0.0075
        ),
        SMS(
            id="sms_002",
            recipient_phone="+1234567891",
            message="Welcome to IVR Tutor! Your learning journey begins now.",
            message_type=MessageType.welcome,
            status=MessageStatus.sent,
            sent_at=datetime.now(),
            cost=0.0075
        )
    ]
    
    # Apply filters (simplified)
    filtered_messages = sample_messages
    if status:
        filtered_messages = [m for m in filtered_messages if m.status == status]
    if message_type:
        filtered_messages = [m for m in filtered_messages if m.message_type == message_type]
    if recipient_phone:
        filtered_messages = [m for m in filtered_messages if m.recipient_phone == recipient_phone]
    
    return filtered_messages[skip:skip+limit]

@router.get("/messages/{message_id}", response_model=SMS)
async def get_message(message_id: str):
    """Get a specific SMS message by ID"""
    # TODO: Implement actual database lookup
    if message_id == "sms_001":
        return SMS(
            id=message_id,
            recipient_phone="+1234567890",
            message="Reminder: You have a lesson tomorrow at 2 PM",
            message_type=MessageType.reminder,
            status=MessageStatus.delivered,
            sent_at=datetime.now(),
            delivered_at=datetime.now(),
            cost=0.0075
        )
    raise HTTPException(status_code=404, detail="SMS message not found")

@router.get("/templates", response_model=List[SMSTemplate])
async def get_sms_templates():
    """Get list of SMS templates"""
    # TODO: Implement actual database query
    return [
        SMSTemplate(
            id="template_001",
            name="Lesson Reminder",
            content="Hi {student_name}, don't forget your {subject} lesson at {time}!",
            message_type=MessageType.reminder,
            variables=["student_name", "subject", "time"]
        ),
        SMSTemplate(
            id="template_002",
            name="Welcome Message",
            content="Welcome to IVR Tutor, {student_name}! Ready to start learning?",
            message_type=MessageType.welcome,
            variables=["student_name"]
        )
    ]

@router.post("/templates", response_model=SMSTemplate)
async def create_sms_template(template: SMSTemplate):
    """Create a new SMS template"""
    # TODO: Implement actual database creation
    new_template = SMSTemplate(
        id=f"template_{hash(template.name) % 10000}",
        **template.dict()
    )
    return new_template

@router.get("/stats", response_model=SMSStats)
async def get_sms_stats():
    """Get SMS statistics"""
    # TODO: Implement actual stats calculation
    return SMSStats(
        total_sent=1250,
        total_delivered=1198,
        total_failed=52,
        delivery_rate=95.8,
        total_cost=9.375
    )

@router.post("/webhook")
async def sms_webhook(webhook_data: dict):
    """Handle SMS webhook (delivery receipts, incoming messages)"""
    # TODO: Implement webhook handling for SMS provider
    return {"status": "received", "message": "SMS webhook processed"}

@router.get("/incoming", response_model=List[IncomingSMS])
async def get_incoming_messages(limit: int = Query(50, ge=1, le=100)):
    """Get incoming SMS messages"""
    # TODO: Implement actual database query for incoming messages
    return [
        IncomingSMS(
            from_phone="+1234567890",
            message="HELP - I need assistance with my lesson",
            received_at=datetime.now(),
            processed=False
        )
    ][:limit]

@router.post("/send-to-student/{student_id}")
async def send_sms_to_student(student_id: str, message: str, message_type: MessageType = MessageType.custom):
    """Send SMS to a specific student"""
    # TODO: Look up student phone number and send SMS
    return {
        "student_id": student_id,
        "message": message,
        "status": "sent",
        "message_id": f"sms_{hash(student_id + message) % 100000}"
    }