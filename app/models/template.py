from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True)
    description = Column(String)
    folder_path = Column(String)
    thumbnail_url = Column(String)
    downloads = Column(Integer, default=0)

    # 🔥 FIX HERE
    user_id = Column(String, ForeignKey("users.id"), nullable=True)

    is_system = Column(Boolean, default=False)

    user = relationship("User", back_populates="templates")
