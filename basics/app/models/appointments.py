from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum as SAEnum
from sqlalchemy.orm import relationship

from database import Base


class AppmtStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    RESCHEDULED = 'rescheduled'


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    appmt_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    status = Column(SAEnum(AppmtStatus, name='appmt_status', create_type=True), default='PENDING', nullable=False)

    # Many to one relationship (Foreign Key)
    # foreign_keys are used as the 2 ForeignKey columns has relationship with same model(user)
    patient = relationship("User", back_populates="appmt_patient", foreign_keys=[patient_id])
    doctor = relationship("User", back_populates="appmt_doctor", foreign_keys=[doctor_id])
