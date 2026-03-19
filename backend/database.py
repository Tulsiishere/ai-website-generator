import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URI)
db = client["ai_website_builder"]
sites_collection = db["generated_sites"]


async def save_site(site_id: str, prompt: str, blueprint: dict) -> None:
    document = {
        "site_id": site_id,
        "prompt": prompt,
        "blueprint": blueprint,
        "created_at": datetime.utcnow().isoformat(),
        "preview_url": f"/preview/{site_id}",
        "download_url": f"/download/{site_id}",
    }
    await sites_collection.insert_one(document)


async def get_site(site_id: str) -> dict | None:
    doc = await sites_collection.find_one({"site_id": site_id}, {"_id": 0})
    return _serialize(doc) if doc else None


async def get_all_sites(limit: int = 20) -> list:
    cursor = sites_collection.find({}, {"_id": 0}).sort("created_at", -1).limit(limit)
    docs = await cursor.to_list(length=limit)
    return [_serialize(doc) for doc in docs]


def _serialize(doc: dict) -> dict:
    """Convert any non-serializable types to strings."""
    return {
        k: v.isoformat() if isinstance(v, datetime) else str(v) if not isinstance(v, (str, int, float, bool, list, dict, type(None))) else v
        for k, v in doc.items()
    }