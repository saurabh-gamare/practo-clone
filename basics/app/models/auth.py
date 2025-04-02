from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SAEnum
from sqlalchemy.orm import relationship

from database import Base
from .appointments import Appointment


class Role(Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)
    role = Column(SAEnum(Role, name="role", create_type=True), nullable=False)

    # One to one relationship
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete")
    # Many to one (ForeignKey)
    appmt_patient = relationship("Appointment", back_populates="patient", foreign_keys=[Appointment.patient_id])
    appmt_doctor = relationship("Appointment", back_populates="doctor", foreign_keys=[Appointment.doctor_id])
