from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class Template(Base):
	__tablename__ = "templates"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True)
	description = Column(String)
	folder_path = Column(String)
	thumbnail_url = Column(String)
	downloads=Column(Integer)

	user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
	user = relationship("User", back_populates="templates")
	is_system = Column(Boolean, default=False)


