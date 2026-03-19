import re


def sanitize_color(color: str, fallback: str) -> str:
    if not color:
        return fallback
    color = color.strip()
    # Already valid hex
    if re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", color):
        return color
    # Check expanded COLOR_MAP
    normalized = normalize_color(color)
    if normalized != color:
        return normalized
    # CSS named colors (safe subset)
    css_named = {
        "black", "white", "gray", "grey", "red", "blue", "green",
        "orange", "yellow", "purple", "brown", "navy", "teal",
        "gold", "silver", "coral", "crimson", "indigo", "violet"
    }
    lower = color.lower().replace(" ", "")
    if lower in css_named:
        return lower
    return fallback


COLOR_MAP = {
    # Grays
    "charcoal": "#1f2937", "charcoal gray": "#1f2937", "charcoal grey": "#1f2937",
    "dark gray": "#374151", "light gray": "#f3f4f6", "slate gray": "#64748b",
    # Blues
    "navy blue": "#1e3a8a", "sky blue": "#0ea5e9", "royal blue": "#2563eb",
    "midnight blue": "#1e1b4b", "steel blue": "#3b82f6",
    # Reds / Pinks
    "burnt orange": "#c2410c", "rust": "#b45309", "rose": "#f43f5e",
    "hot pink": "#ec4899",
    # Greens
    "forest green": "#166534", "emerald": "#10b981", "olive": "#4d7c0f",
    # Yellows / Golds
    "soft gold": "#d4af37", "golden": "#f59e0b", "amber": "#d97706",
    # Neutrals
    "off white": "#fafaf9", "cream": "#fffbeb", "beige": "#f5f0e8",
    "warm white": "#fefce8",
    # Dark
    "dark": "#111827", "dark navy": "#0f172a", "almost black": "#0a0a0a",
}


def normalize_color(color: str) -> str:
    return COLOR_MAP.get(color.strip(), COLOR_MAP.get(color.strip().lower(), color))


def generate_css(primary: str, accent: str) -> str:
    primary_color = sanitize_color(primary, "#111827")
    accent_color = sanitize_color(accent, "#f59e0b")

    return f"""
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
        font-family: 'Segoe UI', Arial, sans-serif;
        background: #f9fafb;
        color: #1f2937;
        line-height: 1.6;
    }}

    /* ── Hero ── */
    .hero {{
        background: {primary_color};
        color: #ffffff;
        padding: 100px 40px;
        text-align: center;
    }}
    .hero h1 {{ font-size: 2.8rem; font-weight: 700; margin-bottom: 16px; }}
    .hero-sub {{ font-size: 1.2rem; opacity: 0.85; margin-bottom: 32px; }}
    .cta-btn {{
        display: inline-block;
        background: {accent_color};
        color: #fff;
        padding: 14px 32px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        transition: opacity 0.2s;
    }}
    .cta-btn:hover {{ opacity: 0.85; }}

    /* ── Nav ── */
    nav {{
        background: {primary_color};
        padding: 16px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
    }}
    nav .brand {{ color: #fff; font-size: 1.2rem; font-weight: 700; }}
    nav ul {{
        list-style: none;
        display: flex;
        gap: 24px;
        flex-wrap: wrap;
    }}
    nav ul li a {{
        color: rgba(255,255,255,0.85);
        text-decoration: none;
        font-size: 0.95rem;
        transition: color 0.2s;
    }}
    nav ul li a:hover {{ color: #fff; }}

    /* ── About ── */
    .about {{
        padding: 80px 40px;
        max-width: 800px;
        margin: auto;
        text-align: center;
    }}
    .about h2 {{ font-size: 2rem; color: {primary_color}; margin-bottom: 16px; }}
    .about p {{ font-size: 1.1rem; color: #4b5563; }}

    /* ── Services ── */
    .services {{
        background: #f3f4f6;
        padding: 80px 40px;
        text-align: center;
    }}
    .services h2 {{ font-size: 2rem; color: {primary_color}; margin-bottom: 40px; }}
    .services-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 24px;
        max-width: 900px;
        margin: auto;
    }}
    .service-card {{
        background: #fff;
        border-radius: 10px;
        padding: 28px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }}
    .service-icon {{
        font-size: 1.5rem;
        color: {accent_color};
        display: block;
        margin-bottom: 10px;
    }}
    .service-card p {{ font-weight: 600; color: #1f2937; }}

    /* ── Gallery ── */
    .gallery {{
        padding: 80px 40px;
        max-width: 1000px;
        margin: auto;
        text-align: center;
    }}
    .gallery h2 {{ font-size: 2rem; color: {primary_color}; margin-bottom: 40px; }}
    .gallery-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }}
    .img-box {{
        background: {accent_color};
        height: 180px;
        border-radius: 10px;
        display: flex;
        align-items: flex-end;
        padding: 12px;
        color: #fff;
        font-weight: 600;
        font-size: 0.9rem;
    }}

    /* ── Contact ── */
    .contact {{
        background: {primary_color};
        color: #fff;
        padding: 80px 40px;
        text-align: center;
    }}
    .contact h2 {{ font-size: 2rem; margin-bottom: 24px; }}
    .contact-info {{ margin-bottom: 32px; line-height: 2; opacity: 0.9; }}
    .contact form {{
        max-width: 560px;
        margin: auto;
        display: flex;
        flex-direction: column;
        gap: 14px;
    }}
    .contact form input,
    .contact form textarea {{
        width: 100%;
        padding: 14px 16px;
        border: none;
        border-radius: 6px;
        font-size: 1rem;
        background: rgba(255,255,255,0.12);
        color: #fff;
    }}
    .contact form input::placeholder,
    .contact form textarea::placeholder {{ color: rgba(255,255,255,0.6); }}
    .contact form textarea {{ height: 120px; resize: vertical; }}
    .contact form button {{
        background: {accent_color};
        color: #fff;
        border: none;
        padding: 14px;
        border-radius: 6px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
    }}

    /* ── Footer ── */
    footer {{
        background: #111827;
        color: rgba(255,255,255,0.5);
        text-align: center;
        padding: 24px 40px;
        font-size: 0.85rem;
    }}

    /* ════════════════════════════
       RESPONSIVE BREAKPOINTS
    ════════════════════════════ */

    /* Tablet — 768px and below */
    @media (max-width: 768px) {{
        .hero {{ padding: 70px 24px; }}
        .hero h1 {{ font-size: 2rem; }}
        .hero-sub {{ font-size: 1rem; }}

        .about {{ padding: 60px 24px; }}
        .about h2 {{ font-size: 1.6rem; }}

        .services {{ padding: 60px 24px; }}
        .services h2 {{ font-size: 1.6rem; }}
        .services-grid {{ grid-template-columns: repeat(2, 1fr); }}

        .gallery {{ padding: 60px 24px; }}
        .gallery h2 {{ font-size: 1.6rem; }}
        .gallery-grid {{ grid-template-columns: repeat(2, 1fr); }}

        .contact {{ padding: 60px 24px; }}
        .contact h2 {{ font-size: 1.6rem; }}

        nav {{ padding: 14px 24px; }}
    }}

    /* Mobile — 480px and below */
    @media (max-width: 480px) {{
        .hero {{ padding: 50px 16px; }}
        .hero h1 {{ font-size: 1.6rem; }}
        .hero-sub {{ font-size: 0.95rem; }}
        .cta-btn {{ padding: 12px 24px; font-size: 0.95rem; }}

        .about {{ padding: 40px 16px; }}
        .about p {{ font-size: 1rem; }}

        .services {{ padding: 40px 16px; }}
        .services-grid {{ grid-template-columns: 1fr; }}

        .gallery {{ padding: 40px 16px; }}
        .gallery-grid {{ grid-template-columns: 1fr; }}
        .img-box {{ height: 140px; }}

        .contact {{ padding: 40px 16px; }}
        .contact form input,
        .contact form textarea {{ padding: 12px; }}

        nav .brand {{ font-size: 1rem; }}
        nav ul {{ gap: 14px; }}
        nav ul li a {{ font-size: 0.85rem; }}
    }}
    """