from pydantic import BaseModel




class TemplateOut(BaseModel):
    id: int
    name: str
    description: str
    folder_path: str
    thumbnail_url: str

    class Config:
        orm_mode = True
