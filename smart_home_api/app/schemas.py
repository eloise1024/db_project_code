from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

class RelationType(str, Enum):
    admin = "admin"
    member = "member"

# User schemas
class UserBase(BaseModel):
    name: str
    number: str = Field(..., max_length=11)

class UserCreate(UserBase):
    user_id: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    number: Optional[str] = None

class User(UserBase):
    user_id: str
    register_time: date
    
    class Config:
        from_attributes = True

# Home schemas
class HomeBase(BaseModel):
    area_sqm: float
    address: str

class HomeCreate(HomeBase):
    home_id: str

class HomeUpdate(BaseModel):
    area_sqm: Optional[float] = None
    address: Optional[str] = None

class Home(HomeBase):
    home_id: str
    
    class Config:
        from_attributes = True

# User-Home Relation schemas
class UserHomeRelationBase(BaseModel):
    relation: RelationType

class UserHomeRelationCreate(UserHomeRelationBase):
    user_id: str
    home_id: str

class UserHomeRelationUpdate(BaseModel):
    relation: Optional[RelationType] = None

class UserHomeRelation(UserHomeRelationBase):
    user_id: str
    home_id: str
    
    class Config:
        from_attributes = True

# Device schemas
class DeviceBase(BaseModel):
    device_type: str
    name: str
    room_name: str

class DeviceCreate(DeviceBase):
    device_id: str
    home_id: str

class DeviceUpdate(BaseModel):
    device_type: Optional[str] = None
    name: Optional[str] = None
    room_name: Optional[str] = None

class Device(DeviceBase):
    device_id: str
    home_id: str
    install_time: date
    
    class Config:
        from_attributes = True

# Device Usage Log schemas
class DeviceUsageLogBase(BaseModel):
    start_time: datetime
    duration_seconds: float

class DeviceUsageLogCreate(DeviceUsageLogBase):
    usage_id: str
    device_id: str

class DeviceUsageLogUpdate(BaseModel):
    start_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None

class DeviceUsageLog(DeviceUsageLogBase):
    usage_id: str
    device_id: str
    
    class Config:
        from_attributes = True

# Device Feedback schemas
class DeviceFeedbackBase(BaseModel):
    problem_description: str
    resolved: bool = False

class DeviceFeedbackCreate(DeviceFeedbackBase):
    feedback_id: str
    device_id: str
    user_id: str

class DeviceFeedbackUpdate(BaseModel):
    problem_description: Optional[str] = None
    resolved: Optional[bool] = None

class DeviceFeedback(DeviceFeedbackBase):
    feedback_id: str
    device_id: str
    user_id: str
    submit_time: datetime
    
    class Config:
        from_attributes = True

# Security Event schemas
class SecurityEventBase(BaseModel):
    event_time: datetime

class SecurityEventCreate(SecurityEventBase):
    event_id: str
    home_id: str
    device_id: str

class SecurityEventUpdate(BaseModel):
    event_time: Optional[datetime] = None

class SecurityEvent(SecurityEventBase):
    event_id: str
    home_id: str
    device_id: str
    
    class Config:
        from_attributes = True

# Analytics schemas
class UsageStats(BaseModel):
    total_duration: float
    period: str
    device_id: str
    device_name: str

class TimeSlotUsage(BaseModel):
    time_slot: str
    usage_count: int
    total_duration: float

class DeviceCorrelation(BaseModel):
    device1: str
    device2: str
    correlation_probability: float

class AreaUsageCorrelation(BaseModel):
    area_sqm: float
    avg_daily_usage: float
    device_type: str

class AlertDistribution(BaseModel):
    device_type: str
    count: int
    percentage: float

class FeedbackDistribution(BaseModel):
    device_type: str
    total_feedback: int
    resolved_count: int
    unresolved_count: int
    resolved_percentage: float

# Response schemas for complex queries
class UserHomesResponse(BaseModel):
    user: User
    homes: List[Home]
    relations: List[UserHomeRelation]

class HomeUsersResponse(BaseModel):
    home: Home
    users: List[User]
    relations: List[UserHomeRelation]

class ChartData(BaseModel):
    labels: List[str]
    data: List[float]
    chart_type: str
    title: str

class CorrelationChartData(BaseModel):
    nodes: List[Dict[str, Any]]
    links: List[Dict[str, Any]]
    title: str