from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas.resume_schemas import ResumeRequest, SummaryRequest
from services.generate_resume import generate_resume as generate_resume_service
from services.generate_summary import generate_summary as generate_summary_service
from app.models.user import User
from app.models.template import Template
from app.utils.thumbnail_generator import generate_pdf_thumbnail
import tempfile
from app.core.security import get_current_user
from app.core.database import get_db
import time
from typing import Optional, List
import os

from pathlib import Path


router = APIRouter()


# Generate Resume

@router.post("/generate-resume")
async def generate_resume(
    request: Request,
    data: ResumeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):

    template = db.query(Template).filter(Template.id==data.template_id).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    relative_pdf_path, pdf_dir = generate_resume_service(
        job_description= data.job_description or "",
        user_data=data.dict(),
        template_path=template.folder_path.lstrip("/"),
        user_id=current_user.id,
    )

    thumbnail_path = generate_pdf_thumbnail(
        pdf_path=relative_pdf_path,
        output_dir=pdf_dir
    )

    template = Template(name=f"{current_user.firstname} {int(time.time())}", description="description", folder_path=relative_pdf_path, thumbnail_url=thumbnail_path, downloads=0, is_system=False, user_id=current_user.id)
    db.add(template)
    db.commit()
    db.refresh(template)

    return {
        "message": "Resume created successfully",
        "file": relative_pdf_path,
    }



# Serve Resume

@router.get("/view-resume/{pdf_path:path}")
def serve_resume(
        pdf_path: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

    BASE_TEMPLATES = Path(__file__).resolve().parents[2] / "app" / "templates"

    file_path = BASE_TEMPLATES / pdf_path

    print("FILE PATH ========== ", file_path)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File Not Found")

    # Get the template for this user and path
    template = db.query(Template).filter(
        Template.user_id == current_user.id,
        Template.folder_path == str(file_path)
    ).first()

    if template:
        print("lginah template +___+)_)()(*&*^^&^&^(**()))")
        template.downloads += 1
        db.commit()

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "inline"
        }
    )



# Dashboard

@router.get('/dashboard')
def dashboard(request: Request, 
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)
                ):

    templates = current_user.templates

    total_downloads = (
            db.query(func.coalesce(func.sum(Template.downloads), 0))
                .filter(Template.user_id == current_user.id)
                .scalar()
    )

    templates_data = [
            {
                "id": template.id,
                "name": template.name,
                "description": template.description,
                "path": template.folder_path,
                "thumbnail": template.thumbnail_url,
                "downloads": template.downloads
            }
            for template in templates
    ]



    return {
            "templates": templates_data,
            "total_templates": len(templates_data),
            "total_downloads": total_downloads
    }

# Generate Summary

@router.post("/generate-summary")
def generate_summary(data: SummaryRequest):

    data = {
        "experiences": data.experiences,
        "skills": data.skills,
    }
    
    summary_text = generate_summary_service(data)

    return { "summary": summary_text }




