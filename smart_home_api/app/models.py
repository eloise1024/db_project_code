from sqlalchemy import Column, String, Integer, Float, Text, Date, DateTime, Boolean, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    
    user_id = Column(String, primary_key=True)
    name = Column(String)
    number = Column(String(11))
    register_time = Column(Date, default=func.current_date())
    
    # Relationships
    user_home_relations = relationship("UserHomeRelation", back_populates="user")
    feedbacks = relationship("DeviceFeedback", back_populates="user")

class Home(Base):
    __tablename__ = "home"
    
    home_id = Column(String, primary_key=True)
    area_sqm = Column(Float)
    address = Column(Text)
    
    # Relationships
    user_home_relations = relationship("UserHomeRelation", back_populates="home")
    devices = relationship("Device", back_populates="home")
    security_events = relationship("SecurityEvent", back_populates="home")

class UserHomeRelation(Base):
    __tablename__ = "user_home_relation"
    
    user_id = Column(String, ForeignKey("user.user_id"), primary_key=True)
    home_id = Column(String, ForeignKey("home.home_id"), primary_key=True)
    relation = Column(String)
    
    __table_args__ = (
        CheckConstraint("relation IN ('admin', 'member')", name='relation_check'),
    )
    
    # Relationships
    user = relationship("User", back_populates="user_home_relations")
    home = relationship("Home", back_populates="user_home_relations")

class Device(Base):
    __tablename__ = "device"
    
    device_id = Column(String, primary_key=True)
    device_type = Column(String)
    name = Column(String)
    home_id = Column(String, ForeignKey("home.home_id"))
    room_name = Column(Text)
    install_time = Column(Date, default=func.current_date())
    
    # Relationships
    home = relationship("Home", back_populates="devices")
    usage_logs = relationship("DeviceUsageLog", back_populates="device")
    feedbacks = relationship("DeviceFeedback", back_populates="device")
    security_events = relationship("SecurityEvent", back_populates="device")

class DeviceUsageLog(Base):
    __tablename__ = "device_usage_log"
    
    usage_id = Column(String, primary_key=True)
    device_id = Column(String, ForeignKey("device.device_id"))
    start_time = Column(DateTime)
    duration_seconds = Column(Numeric(6,2))
    
    # Relationships
    device = relationship("Device", back_populates="usage_logs")

class DeviceFeedback(Base):
    __tablename__ = "device_feedback"
    
    feedback_id = Column(String, primary_key=True)
    device_id = Column(String, ForeignKey("device.device_id"))
    user_id = Column(String, ForeignKey("user.user_id"))
    submit_time = Column(DateTime, default=func.now())
    problem_description = Column(Text)
    resolved = Column(Boolean, default=False)
    
    # Relationships
    device = relationship("Device", back_populates="feedbacks")
    user = relationship("User", back_populates="feedbacks")

class SecurityEvent(Base):
    __tablename__ = "security_event"
    
    event_id = Column(String, primary_key=True)
    home_id = Column(String, ForeignKey("home.home_id"))
    event_time = Column(DateTime, default=func.now())
    device_id = Column(String, ForeignKey("device.device_id"))
    
    # Relationships
    home = relationship("Home", back_populates="security_events")
    device = relationship("Device", back_populates="security_events")

class Alert(Base):
    """警报表"""
    __tablename__ = "alerts"
    
    alert_id = Column(String, primary_key=True, index=True)
    home_id = Column(String, ForeignKey("homes.home_id"))
    device_id = Column(String, ForeignKey("devices.device_id"))
    alert_type = Column(String)  # 设备故障, 网络异常, 温度异常等
    message = Column(String)
    severity = Column(String, default="medium")  # low, medium, high
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime)
    resolved_at = Column(DateTime, nullable=True)

class Feedback(Base):
    """用户反馈表"""
    __tablename__ = "feedbacks"
    
    feedback_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    device_id = Column(String, ForeignKey("devices.device_id"))
    device_type = Column(String)
    feedback_type = Column(String)  # bug, suggestion, complaint等
    content = Column(String)
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime)
    resolved_at = Column(DateTime, nullable=True)

class UsageRecord(Base):
    """设备使用记录表"""
    __tablename__ = "usage_records"
    
    record_id = Column(String, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.device_id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer)
    created_at = Column(DateTime)