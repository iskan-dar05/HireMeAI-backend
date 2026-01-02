import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


sys.path.append(str(BASE_DIR))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.template import Template
from app.models.user import User


SYSTEM_TEMPLATES = [
    {
        "name": "Modern Resume",
        "description": "Modern professional resume template",
        "folder_path": "/system/template1",
        "thumbnail_url": "/system/template1/thumbnail.png",
        "downloads": 0,
        "is_system": True,
        "user_id": None,
    },
    {
        "name": "Classic Resume",
        "description": "Classic clean resume template",
        "folder_path": "/system/template2",
        "thumbnail_url": "/system/template2/thumbnail.png",
        "downloads": 0,
        "is_system": True,
        "user_id": None,
    },
    {
        "name": "Minimal Resume",
        "description": "Minimalist resume with clean layout",
        "folder_path": "system/template3",
        "thumbnail_url": "/system/template3/thumbnail.png",
        "downloads": 0,
        "is_system": True,
        "user_id": None,
    },
    {
        "name": "Creative Resume",
        "description": "Creative resume for designers",
        "folder_path": "/system/template4",
        "thumbnail_url": "/system/template4/thumbnail.png",
        "downloads": 0,
        "is_system": True,
        "user_id": None,
    },
    {
        "name": "Professional Resume",
        "description": "Professional corporate resume",
        "folder_path": "/system/template5",
        "thumbnail_url": "/system/template5/thumbnail.png",
        "downloads": 0,
        "is_system": True,
        "user_id": None,
    },
    {
        "name": "Elegant Resume",
        "description": "Elegant resume with modern typography",
        "folder_path": "/system/template6",
        "thumbnail_url": "/system/template6/thumbnail.png",
        "downloads": 0,
        "is_system": True,
        "user_id": None,
    },
    {
        "name": "Technical Resume",
        "description": "Resume optimized for developers and engineers",
        "folder_path": "/system/template7",
        "thumbnail_url": "/system/template7/thumbnail.png",
        "downloads": 0,
        "is_system": True,
        "user_id": None,
    },
    {
        "name": "Academic Resume",
        "description": "Academic CV for researchers and students",
        "folder_path": "/system/template8",
        "thumbnail_url": "/system/template8/thumbnail.png",
        "downloads": 0,
        "is_system": True,
        "user_id": None,
    },
    {
        "name": "Simple Resume",
        "description": "Simple and clean resume layout",
        "folder_path": "/system/template9",
        "thumbnail_url": "/system/template9/thumbnail.png",
        "downloads": 0,
        "is_system": True,
        "user_id": None,
    },
    {
        "name": "Bold Resume",
        "description": "Bold resume with strong visual impact",
        "folder_path": "/system/template10",
        "thumbnail_url": "/system/template10/thumbnail.png",
        "downloads": 0,
        "is_system": True,
        "user_id": None,
    },
]

def seed_templates():
    db: Session = SessionLocal()

    for data in SYSTEM_TEMPLATES:
        exists = db.query(Template).filter(
            Template.name == data["name"]
        ).first()

        if exists:
            print(f"⚠️ Template '{data['name']}' already exists")
            continue

        template = Template(**data)
        db.add(template)
        print(f"✅ Inserted template: {data['name']}")

    db.commit()
    db.close()

if __name__ == "__main__":
    seed_templates()
