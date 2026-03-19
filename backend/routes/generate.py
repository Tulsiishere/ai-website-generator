import os
import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse

from backend.ai_engine import generate_blueprint
from backend.website_generator.builder import build_website
from backend.website_generator.models import PromptRequest
from backend.database import save_site, get_all_sites

router = APIRouter()

GENERATED_FOLDER = "backend/generated_sites"
os.makedirs(GENERATED_FOLDER, exist_ok=True)


@router.post("/generate")
async def generate_site(request: PromptRequest):
    try:
        blueprint = generate_blueprint(request.prompt)
        html = build_website(blueprint)

        site_id = str(uuid.uuid4())
        file_path = os.path.join(GENERATED_FOLDER, f"{site_id}.html")

        # Save HTML
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        # Save to MongoDB
        await save_site(
            site_id = site_id,
            prompt = request.prompt,
            blueprint = blueprint.model_dump(),
        )

        return JSONResponse(
            content={
                "status": "success",
                "site_id": site_id,
                "preview_url": f"/preview/{site_id}",
                "download_url": f"/download/{site_id}",
            }
        )

    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to generate website: {str(e)}")

@router.get("/preview/{site_id}")
def preview_site(site_id: str):
    file_path = os.path.join(GENERATED_FOLDER, f"{site_id}.html")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Site not found")

    return FileResponse(file_path, media_type="text/html")

@router.get("/download/{site_id}")
def download_site(site_id: str):
    file_path = os.path.join(GENERATED_FOLDER, f"{site_id}.html")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Site not found")

    return FileResponse(file_path, media_type="text/html", filename=f"{site_id}.html")

@router.get("/sites")
async def list_sites():
    sites = await get_all_sites()
    return JSONResponse(content={"sites": sites})