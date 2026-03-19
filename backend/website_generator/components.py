import html
from typing import List


def hero_section(title: str, subtitle: str = "", cta: str = "Get in touch") -> str:
    safe_title = html.escape(title)
    safe_subtitle = html.escape(subtitle)
    safe_cta = html.escape(cta)
    return f"""
    <section class="hero">
        <h1>{safe_title}</h1>
        {"<p class='hero-sub'>" + safe_subtitle + "</p>" if subtitle else ""}
        <a href="#contact" class="cta-btn">{safe_cta}</a>
    </section>
    """


def about_section(text: str) -> str:
    safe_text = html.escape(text)
    return f"""
    <section class="about">
        <h2>About Us</h2>
        <p>{safe_text}</p>
    </section>
    """


def services_section(services: List[str]) -> str:
    items = "".join(
        f'<div class="service-card"><span class="service-icon">✦</span><p>{html.escape(s)}</p></div>'
        for s in services
    )
    return f"""
    <section class="services">
        <h2>What We Offer</h2>
        <div class="services-grid">{items}</div>
    </section>
    """


def gallery_section(captions: List[str] = None) -> str:
    captions = captions or ["Our Work", "Portfolio", "Projects"]
    items = "".join(
        f'<div class="img-box"><span>{html.escape(c)}</span></div>'
        for c in captions
    )
    return f"""
    <section class="gallery">
        <h2>Gallery</h2>
        <div class="gallery-grid">{items}</div>
    </section>
    """


def contact_section(email: str = "", phone: str = "", address: str = "") -> str:
    info = ""
    if email:
        info += f'<p>✉ {html.escape(email)}</p>'
    if phone:
        info += f'<p>✆ {html.escape(phone)}</p>'
    if address:
        info += f'<p>⚑ {html.escape(address)}</p>'

    return f"""
    <section class="contact" id="contact">
        <h2>Get In Touch</h2>
        <div class="contact-info">{info}</div>
        <form>
            <input type="text" placeholder="Your Name" />
            <input type="email" placeholder="Your Email" />
            <textarea placeholder="Your Message"></textarea>
            <button type="submit">Send Message</button>
        </form>
    </section>
    """