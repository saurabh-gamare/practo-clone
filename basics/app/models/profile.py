from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    # use unique=True as its one to one relationship
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    profile_pic = Column(String(255))
    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    mobile = Column(String(10), unique=True)
    email = Column(String(50), unique=True)
    address = Column(String(100))
    speciality = Column(String(50))
    degree = Column(String(50))

    user = relationship("User", back_populates="profile")