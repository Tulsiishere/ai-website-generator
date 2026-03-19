# AI Website Generator

An AI-powered web application that generates fully functional, styled websites from natural language prompts. Built with FastAPI, Google Gemini, and MongoDB.

**Live Demo:** [https://ai-website-generator-3yh7.onrender.com](https://ai-website-generator-3yh7.onrender.com)

---

## What It Does

A user types a business description like _"Bakery in Bandra, Mumbai selling artisan breads"_ and the system:

1. Sends the prompt to Google Gemini to generate a structured website blueprint (JSON)
2. Validates the blueprint using Pydantic
3. Builds a complete HTML/CSS website using a modular component system
4. Saves the project to MongoDB
5. Returns a live preview URL and a downloadable HTML file

---

## Architecture

```
User Prompt
    │
    ▼
FastAPI Backend (/generate)
    │
    ├── ai_engine.py        → Sends prompt to Gemini, returns WebsiteBlueprint (JSON)
    │
    ├── website_generator/
    │   ├── models.py       → Pydantic schema validation
    │   ├── builder.py      → Assembles HTML from components
    │   ├── components.py   → Reusable section components (hero, about, services...)
    │   └── css.py          → Dynamic CSS generation with responsive breakpoints
    │
    ├── database.py         → MongoDB persistence via Motor (async)
    │
    └── routes/
        └── generate.py     → API route handlers
```

---

## Tech Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| Backend | FastAPI (Python) | Async support, automatic docs, fast development |
| AI Model | Google Gemini 2.0 Flash | Free tier, structured JSON output, reliable |
| Database | MongoDB + Motor | Flexible schema for dynamic blueprints, async driver |
| Frontend | Vanilla HTML/CSS/JS | No framework overhead, fast load, simple to deploy |
| Hosting | Render | Free tier, auto-deploy from GitHub, Python native |

---

## Project Structure

```
ai_website_builder/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── ai_engine.py             # Gemini API integration + JSON parsing
│   ├── database.py              # MongoDB connection and queries
│   ├── routes/
│   │   ├── __init__.py
│   │   └── generate.py          # API route handlers
│   └── website_generator/
│       ├── models.py            # Pydantic data models
│       ├── builder.py           # HTML assembly engine
│       ├── components.py        # Reusable HTML components
│       └── css.py               # Dynamic CSS + responsive breakpoints
├── frontend/
│   └── index.html               # Single-page UI (form + preview iframe)
├── .env                         # Environment variables (not committed)
├── render.yaml                  # Render deployment config
├── requirements.txt
└── README.md
```

---

## API Endpoints

### `POST /generate`
Generates a website from a natural language prompt.

**Request:**
```json
{
  "prompt": "Bakery in Mumbai selling artisan breads and custom cakes"
}
```

**Response:**
```json
{
  "status": "success",
  "site_id": "a1b2c3d4-...",
  "preview_url": "/preview/a1b2c3d4-...",
  "download_url": "/download/a1b2c3d4-..."
}
```

---

### `GET /preview/{site_id}`
Returns the fully rendered HTML website for in-browser preview.

---

### `GET /download/{site_id}`
Downloads the generated website as an HTML file.

---

### `GET /sites`
Returns a list of all previously generated sites stored in MongoDB.

**Response:**
```json
{
  "sites": [
    {
      "site_id": "a1b2c3d4-...",
      "prompt": "Bakery in Mumbai",
      "created_at": "2026-03-17T14:08:35",
      "preview_url": "/preview/a1b2c3d4-...",
      "download_url": "/download/a1b2c3d4-..."
    }
  ]
}
```

---

## AI Pipeline

```
User Prompt
    │
    ▼
System Prompt + User Input → Gemini 2.0 Flash
    │
    ▼
Structured JSON Response (WebsiteBlueprint)
    │
    ├── website_type  (e.g. "bakery")
    ├── theme         (e.g. "warm and modern")
    ├── sections      (e.g. ["hero", "about", "services", "gallery", "contact"])
    ├── color_scheme  (hex codes)
    └── content
        ├── hero_title
        ├── hero_subtitle
        ├── about_text
        ├── services      (list)
        ├── gallery_items (list with captions)
        ├── contact_info  (email, phone, address)
        └── cta_text
    │
    ▼
Pydantic Validation (WebsiteBlueprint model)
    │
    ▼
Component Builder → Full HTML + CSS Website
    │
    ▼
Saved to MongoDB + File System
    │
    ▼
Preview URL + Download URL returned to user
```

---

## Model Selection Rationale

### Why Google Gemini over GPT-4 / Claude?

| Factor | Gemini 2.0 Flash | GPT-4 | Claude |
|--------|-----------------|-------|--------|
| Free tier | Generous | Limited | Limited |
| JSON mode | Native support | Yes | Yes |
| Response schema | Supported | No | No |
| Speed | Very fast | Moderate | Moderate |
| Cost at scale | Low | High | High |

Gemini's `response_schema` parameter enables **constrained decoding** — the model is forced to generate tokens that structurally match the defined JSON schema. This eliminates malformed JSON entirely, which is the most common failure point when using LLMs for structured output generation.

### Why FastAPI over Flask?

- Native async support — critical for non-blocking MongoDB queries via Motor
- Automatic Swagger UI at `/docs` — made development and testing significantly faster
- Built-in Pydantic integration for request/response validation
- Better performance under concurrent load

### Why MongoDB over PostgreSQL?

The core data — a `WebsiteBlueprint` — is a deeply nested, variable-length JSON document. Different website types produce different content structures. MongoDB's document model stores this naturally without requiring schema migrations. PostgreSQL would require flattening or serializing the JSON, adding unnecessary complexity for this use case.

---

## Local Setup

```bash
# Clone the repo
git clone https://github.com/Tulsiishere/ai-website-generator.git
cd ai-website-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your GEMINI_API_KEY and MONGO_URI

# Run the server
uvicorn backend.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key from [ai.google.dev](https://ai.google.dev) |
| `MONGO_URI` | MongoDB connection string (local or Atlas) |

---

## Features

- Natural language prompt → complete website in under 10 seconds
- Modular component system (hero, about, services, gallery, contact)
- AI-generated content: headlines, taglines, about text, service names, contact info
- Dynamic color scheme from hex codes
- Fully responsive design (desktop, tablet, mobile)
- Live preview in browser iframe
- One-click HTML download
- All projects saved to MongoDB with timestamps
- Clean REST API with automatic Swagger documentation

---

## Author

**Tulsi Pandey**  
Data Science Student | Aspiring GenAI Developer  