from sqlalchemy import Column, String, Boolean
from app.core.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    # Clerk user ID (ex: user_2YkQ8vH8kX9ABC)
    id = Column(String, primary_key=True, index=True)

    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)

    is_active = Column(Boolean, default=True)

    templates = relationship(
        "Template",
        back_populates="user",
        cascade="all, delete-orphan"
    )
