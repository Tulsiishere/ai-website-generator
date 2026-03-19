from typing import List
from typing import Optional
from pydantic import BaseModel


class ColorScheme(BaseModel):
    primary: str
    accent: str


class GalleryItem(BaseModel):
    caption: str

class ContactInfo(BaseModel):
    email: Optional[str] = ""
    phone: Optional[str] = ""
    address: Optional[str] = ""

class Content(BaseModel):
    hero_title: str
    hero_subtitle: Optional[str] = ""
    about_text: str
    services: Optional[List[str]] = []
    gallery_items: List[GalleryItem] = []
    contact_info: Optional[ContactInfo] = None
    cta_text: Optional[str] = "Get in touch"


class WebsiteBlueprint(BaseModel):
    website_type: str
    theme: str
    sections: List[str]
    color_scheme: ColorScheme
    content: Content

class PromptRequest(BaseModel):
    prompt: str