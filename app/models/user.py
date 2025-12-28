from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base
from sqlalchemy.orm import relationship



class User(Base):
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True, index=True)
	firstname = Column(String, nullable=True)
	lastname = Column(String, nullable=True)
	email = Column(String, unique=True, index=True, nullable=False)
	hashed_password = Column(String, nullable=False)
	templates = relationship(
		"Template",
		back_populates="user",
		cascade="all, delete-orphan"
	)
	is_active = Column(Boolean, default=False) ## Email Verified


