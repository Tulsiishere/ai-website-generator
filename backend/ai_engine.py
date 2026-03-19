import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError

from backend.website_generator.models import WebsiteBlueprint

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_key_here")

MODEL_NAME = "gemini-2.5-flash"

_client = genai.Client(api_key=GEMINI_API_KEY)

# ==============================
# Response Schema for structured output
# ==============================

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "website_type": {"type": "string"},
        "theme": {"type": "string"},
        "sections": {
            "type": "array",
            "items": {"type": "string"}
        },
        "color_scheme": {
            "type": "object",
            "properties": {
                "primary": {"type": "string"},
                "accent": {"type": "string"}
            },
            "required": ["primary", "accent"]
        },
        "content": {
            "type": "object",
            "properties": {
                "hero_title":    {"type": "string"},
                "hero_subtitle": {"type": "string"},
                "about_text":    {"type": "string"},
                "services":      {"type": "array", "items": {"type": "string"}},
                "gallery_items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"caption": {"type": "string"}},
                        "required": ["caption"]
                    }
                },
                "contact_info": {
                    "type": "object",
                    "properties": {
                        "email":   {"type": "string"},
                        "phone":   {"type": "string"},
                        "address": {"type": "string"}
                    },
                    "required": ["email", "phone", "address"]
                },
                "cta_text": {"type": "string"}
            },
            "required": [
                "hero_title", "hero_subtitle", "about_text",
                "services", "gallery_items", "contact_info", "cta_text"
            ]
        }
    },
    "required": [
        "website_type", "theme", "sections", "color_scheme", "content"
    ]
}

# ==============================
# System Prompt
# ==============================

SYSTEM_PROMPT = """You are an expert web designer. Return ONLY a valid JSON object with this EXACT structure — no deviations:

{
  "website_type": "bakery",
  "theme": "warm and modern",
  "sections": ["hero", "about", "services", "gallery", "contact"],
  "color_scheme": {
    "primary": "#7c3aed",
    "accent": "#f59e0b"
  },
  "content": {
    "hero_title": "Fresh Baked Every Morning",
    "hero_subtitle": "Artisan breads and pastries made with love in Mumbai.",
    "about_text": "2-3 sentences about the business.",
    "services": ["Custom Cakes", "Sourdough Bread", "Catering"],
    "gallery_items": [
      {"caption": "Our signature sourdough"},
      {"caption": "Custom wedding cakes"},
      {"caption": "Daily fresh pastries"}
    ],
    "contact_info": {
      "email": "hello@bakery.com",
      "phone": "+91 98765 43210",
      "address": "123 Baker Street, Bandra, Mumbai"
    },
    "cta_text": "Order Now"
  }
}

Replace all values with real, specific content for the business described. Keep all keys exactly as shown."""

# ==============================
# JSON cleaning
# ==============================

def clean_json_string(text: str) -> str:
    text = text.strip()
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                text = part
                break
    text = re.sub(r",\s*([}\]])", r"\1", text)  # trailing commas
    return text.strip()


def extract_json(text: str) -> dict | None:
    start = text.find("{")
    if start == -1:
        return None

    # Try direct parse first
    end = text.rfind("}")
    if end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    # Response was truncated — attempt to repair by closing open braces/brackets
    fragment = text[start:]
    open_braces = fragment.count("{") - fragment.count("}")
    open_brackets = fragment.count("[") - fragment.count("]")

    # Close any open string first (odd number of unescaped quotes = open string)
    in_string = False
    escaped = False
    for ch in fragment:
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string

    repaired = fragment
    if in_string:
        repaired += '"'          # close open string
    repaired += "]" * open_brackets  # close open arrays
    repaired += "}" * open_braces    # close open objects

    try:
        return json.loads(repaired)
    except json.JSONDecodeError:
        return None

def normalize_response(data: dict) -> dict:
    """
    If Gemini returns a flat dict instead of nested blueprint,
    auto-wrap content fields into the correct structure.
    """
    content_fields = {
        "hero_title", "hero_subtitle", "about_text",
        "services", "gallery_items", "contact_info", "cta_text"
    }
    top_level_fields = {"website_type", "theme", "sections", "color_scheme", "content"}

    # If already correct structure, return as-is
    if all(f in data for f in ["website_type", "theme", "content"]):
        return data

    # Flat response — rebuild the structure
    content = {k: data[k] for k in content_fields if k in data}
    blueprint = {k: data[k] for k in top_level_fields - {"content"} if k in data}
    blueprint["content"] = content

    # Patch missing top-level fields with sensible defaults
    if "website_type" not in blueprint:
        blueprint["website_type"] = "business"
    if "theme" not in blueprint:
        blueprint["theme"] = "modern"
    if "sections" not in blueprint:
        blueprint["sections"] = ["hero", "about", "services", "gallery", "contact"]
    if "color_scheme" not in blueprint:
        blueprint["color_scheme"] = {"primary": "#111827", "accent": "#f59e0b"}

    return blueprint
# ==============================
# Generate Blueprint
# ==============================

def generate_blueprint(user_prompt: str) -> WebsiteBlueprint:
    prompt = f"{SYSTEM_PROMPT}\n\nBusiness description: {user_prompt}"

    # --- Attempt 1: structured output via response_schema ---
    try:
        response = _client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=2000,
                response_mime_type="application/json",
                response_schema=RESPONSE_SCHEMA,
            ),
        )

        if response.text:
            data = normalize_response(json.loads(response.text))
            return WebsiteBlueprint.model_validate(data)

    except (json.JSONDecodeError, ValidationError, Exception):
        pass  # fall through to attempt 2

    # --- Attempt 2: plain JSON mode, manual cleaning ---
    try:
        retry_response = _client.models.generate_content(
            model=MODEL_NAME,
            contents=(
                "Return ONLY a valid JSON object. No markdown. No explanation.\n\n"
                + prompt
            ),
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=2000,
                response_mime_type="application/json",
            ),
        )

        raw = retry_response.text or ""
        print("=== RAW GEMINI RESPONSE ===")
        print(repr(raw))
        print("=== END ===")
        cleaned = clean_json_string(raw)

        try:
            data = normalize_response(json.loads(cleaned))
        except json.JSONDecodeError:
            data = extract_json(cleaned)
            if data is None:
                raise ValueError("Could not extract valid JSON from Gemini response")

        return WebsiteBlueprint.model_validate(normalize_response(data))

    except ValidationError as e:
        raise ValueError(f"Blueprint schema mismatch: {e}") from e
    except Exception as e:
        raise ValueError(f"Gemini failed to return valid JSON: {e}") from e