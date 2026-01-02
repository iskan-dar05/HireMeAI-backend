from pydantic import BaseModel
from typing import Optional, List


class Experience(BaseModel):
    company: str
    position: str
    startDate: Optional[str]
    endDate: Optional[str]
    description: str

class Education(BaseModel):
    school: str
    degree: str
    field: str
    graduationDate: Optional[str]



class ResumeRequest(BaseModel):
    fullname: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    linkedin: Optional[str] = None
    job_description: Optional[str]
    template_id: int
    profession: Optional[str]
    summary: Optional[str]
    skills: Optional[str]
    experiences: List[Experience]
    education: List[Education]


class SummaryRequest(BaseModel):
    experiences: List[Experience]
    skills: Optional[List[str]] = []
