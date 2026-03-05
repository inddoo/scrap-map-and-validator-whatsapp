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

