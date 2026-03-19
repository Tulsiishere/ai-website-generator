from backend.website_generator.components import (
    hero_section,
    about_section,
    services_section,
    gallery_section,
    contact_section,
)
from backend.website_generator.css import generate_css
from backend.website_generator.models import WebsiteBlueprint


def build_website(blueprint: WebsiteBlueprint) -> str:
    sections_html = ""
    c = blueprint.content

    for section in [s.lower() for s in blueprint.sections]:
        if section == "hero":
            sections_html += hero_section(
                title=c.hero_title,
                subtitle=c.hero_subtitle or "",
                cta=c.cta_text or "Get in touch",
            )
        elif section == "about":
            sections_html += about_section(c.about_text)

        elif section == "services":
            sections_html += services_section(c.services or [])

        elif section == "gallery":
            captions = [item.caption for item in c.gallery_items] if c.gallery_items else []
            sections_html += gallery_section(captions)

        elif section == "contact":
            ci = c.contact_info
            sections_html += contact_section(
                email=ci.email if ci else "",
                phone=ci.phone if ci else "",
                address=ci.address if ci else "",
            )
        else:
            # Smart fallback: render services list if available, else generic
            sections_html += f"""
            <section style="padding:60px 40px;text-align:center;">
                <h2 style="font-size:1.8rem;margin-bottom:16px;">{section.title()}</h2>
                <p style="color:#6b7280;">Coming soon — check back for updates.</p>
            </section>
            """

    css = generate_css(
        blueprint.color_scheme.primary,
        blueprint.color_scheme.accent,
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{blueprint.website_type.title()} — {c.hero_title}</title>
    <style>{css}</style>
</head>
<body>
    {sections_html}
</body>
</html>"""