"""
API request/response schemas
"""
from pydantic import BaseModel
from typing import List, Optional


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
