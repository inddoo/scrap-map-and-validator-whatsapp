"""
API request/response schemas
"""
from pydantic import BaseModel
from typing import List, Optional, Dict


class ScrapeRequest(BaseModel):
    """Request schema for scraping operations"""
    query: str


class WAValidationRequest(BaseModel):
    """Request schema for WhatsApp validation"""
    phone_numbers: List[str]


class WAValidationResult(BaseModel):
    """Result schema for single WhatsApp validation"""
    phone: str
    clean_phone: str
    has_whatsapp: bool
    is_business: bool
    business_name: Optional[str] = ""
    status: str


class WAValidationResponse(BaseModel):
    """Response schema for WhatsApp validation"""
    success: bool
    results: List[WAValidationResult]
    summary: dict


class WASendMessageRequest(BaseModel):
    """Request schema for sending single message"""
    phone: str
    message: str
    delay: Optional[int] = 5


class WASendBulkRequest(BaseModel):
    """Request schema for sending bulk messages"""
    phone_numbers: List[str]
    message: str
    min_delay: Optional[int] = 5
    max_delay: Optional[int] = 10
    stop_on_error: Optional[bool] = False


class WASendPersonalizedRequest(BaseModel):
    """Request schema for sending personalized messages"""
    contacts: List[Dict]  # [{'phone': '628xxx', 'name': 'John', ...}]
    message_template: str  # "Halo {name}, ..."
    min_delay: Optional[int] = 5
    max_delay: Optional[int] = 10


class WASendResult(BaseModel):
    """Result schema for message sending"""
    phone: str
    message_sent: bool
    status: str
    error: Optional[str] = None


class WASendResponse(BaseModel):
    """Response schema for message sending"""
    success: bool
    results: List[Dict]
    summary: Dict



class AIGenerateMessageRequest(BaseModel):
    """Request schema for AI message generation"""
    template: str  # Template or instruction for message
    csv_data: List[Dict]  # CSV data rows
    context: Optional[str] = None  # Additional context


class AIGenerateMessageResponse(BaseModel):
    """Response schema for AI message generation"""
    success: bool
    messages: List[Dict]  # [{'phone': '628xxx', 'name': 'John', 'message': '...'}]


class AIAutoResponderRequest(BaseModel):
    """Request schema for AI auto responder"""
    incoming_message: str
    sender_phone: str
    sender_data: Dict  # Data from CSV
    response_prompt: str  # Instructions for response
    conversation_history: Optional[List[Dict]] = None


class AIAutoResponderResponse(BaseModel):
    """Response schema for AI auto responder"""
    success: bool
    response_message: str


class WASendAIPersonalizedRequest(BaseModel):
    """Request schema for sending AI-generated personalized messages"""
    csv_data: List[Dict]  # Full CSV data with phone and other fields
    message_template: str  # Template or AI instruction
    use_ai: bool = True  # Whether to use AI generation
    context: Optional[str] = None  # Additional context for AI
    min_delay: Optional[int] = 5
    max_delay: Optional[int] = 10
    auto_responder_enabled: Optional[bool] = False
    auto_responder_prompt: Optional[str] = None


class AutoResponderStartRequest(BaseModel):
    """Request schema for starting auto responder"""
    response_prompt: Optional[str] = None
    check_interval: Optional[int] = 1  # Check every N seconds (default: 1 for instant reply)


class AutoResponderUpdateRequest(BaseModel):
    """Request schema for updating auto responder prompt"""
    response_prompt: str


class AutoResponderStatusResponse(BaseModel):
    """Response schema for auto responder status"""
    success: bool
    is_running: bool
    response_prompt: Optional[str] = None
    check_interval: Optional[int] = None
    monitored_chats: Optional[int] = None
    total_processed: Optional[int] = None
