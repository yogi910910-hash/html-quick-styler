# ============================================================
# HTML Quick-Styler
# AI-Powered HTML Page Generator with IBM Granite 3.3 2B
# ============================================================
# Run this file in Google Colab step by step
# ============================================================

# ============================================================
# CELL 1: Install Dependencies
# ============================================================
# !pip install gradio transformers torch accelerate huggingface_hub

# ============================================================
# CELL 2: Imports
# ============================================================
import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import re

# ============================================================
# CELL 3: Load IBM Granite Model
# ============================================================
MODEL_ID = "ibm-granite/granite-3.3-2b-instruct"

print("Loading IBM Granite 3.3 2B model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)
print("✅ Model loaded successfully!")

# ============================================================
# CELL 4: Color Palette Generator
# ============================================================
class ColorPaletteGenerator:
    """Generates cohesive color palettes for different design styles."""

    PALETTES = {
        "modern": {
            "primary": "#6366F1",
            "secondary": "#8B5CF6",
            "accent": "#06B6D4",
            "background": "#0F172A",
            "surface": "#1E293B",
            "text_primary": "#F8FAFC",
            "text_secondary": "#94A3B8",
            "border": "#334155"
        },
        "vibrant": {
            "primary": "#FF6B6B",
            "secondary": "#4ECDC4",
            "accent": "#FFE66D",
            "background": "#1A1A2E",
            "surface": "#16213E",
            "text_primary": "#FFFFFF",
            "text_secondary": "#B0B0C3",
            "border": "#2D2D44"
        },
        "ocean": {
            "primary": "#0077B6",
            "secondary": "#00B4D8",
            "accent": "#90E0EF",
            "background": "#03045E",
            "surface": "#023E8A",
            "text_primary": "#CAF0F8",
            "text_secondary": "#90E0EF",
            "border": "#0077B6"
        },
        "forest": {
            "primary": "#2D6A4F",
            "secondary": "#52B788",
            "accent": "#B7E4C7",
            "background": "#081C15",
            "surface": "#1B4332",
            "text_primary": "#D8F3DC",
            "text_secondary": "#95D5B2",
            "border": "#2D6A4F"
        },
        "sunset": {
            "primary": "#F77F00",
            "secondary": "#FCBF49",
            "accent": "#EAE2B7",
            "background": "#1A0000",
            "surface": "#2D0A00",
            "text_primary": "#FFF3E0",
            "text_secondary": "#FFCC80",
            "border": "#BF360C"
        },
        "luxury": {
            "primary": "#C9A84C",
            "secondary": "#B8860B",
            "accent": "#FFD700",
            "background": "#0D0D0D",
            "surface": "#1A1A1A",
            "text_primary": "#F5F5DC",
            "text_secondary": "#D4AF37",
            "border": "#3D3D00"
        },
        "creative": {
            "primary": "#E040FB",
            "secondary": "#7C4DFF",
            "accent": "#00E5FF",
            "background": "#12005E",
            "surface": "#1A0070",
            "text_primary": "#EDE7F6",
            "text_secondary": "#CE93D8",
            "border": "#4A148C"
        },
        "minimal": {
            "primary": "#212121",
            "secondary": "#424242",
            "accent": "#757575",
            "background": "#FAFAFA",
            "surface": "#FFFFFF",
            "text_primary": "#212121",
            "text_secondary": "#757575",
            "border": "#E0E0E0"
        }
    }

    @classmethod
    def get_palette(cls, style: str) -> dict:
        return cls.PALETTES.get(style.lower(), cls.PALETTES["modern"])

    @classmethod
    def get_all_palettes(cls) -> dict:
        return cls.PALETTES

    @classmethod
    def generate_palette_preview_html(cls) -> str:
        html = "<div style='display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;padding:16px'>"
        for name, colors in cls.PALETTES.items():
            swatches = "".join(
                f"<div style='width:28px;height:28px;border-radius:50%;background:{v};border:2px solid #ffffff33' title='{k}'></div>"
                for k, v in colors.items()
            )
            html += f"""
            <div style='background:{colors["surface"]};border:1px solid {colors["border"]};border-radius:12px;padding:16px;box-shadow:0 4px 12px rgba(0,0,0,0.3)'>
              <div style='font-size:16px;font-weight:700;color:{colors["text_primary"]};margin-bottom:8px;text-transform:capitalize'>{name}</div>
              <div style='display:flex;gap:6px;flex-wrap:wrap'>{swatches}</div>
              <div style='font-size:11px;color:{colors["text_secondary"]};margin-top:8px'>Primary: {colors["primary"]}</div>
            </div>"""
        html += "</div>"
        return html


# ============================================================
# CELL 5: HTML Page Builder
# ============================================================
class HTMLPageBuilder:
    """Builds semantic HTML sections based on user descriptions."""

    SECTION_KEYWORDS = {
        "hero":         ["hero", "banner", "welcome", "landing", "header", "intro"],
        "features":     ["feature", "benefit", "service", "capability", "offer"],
        "about":        ["about", "mission", "vision", "team", "story", "company"],
        "portfolio":    ["portfolio", "work", "project", "gallery", "showcase"],
        "testimonials": ["testimonial", "review", "feedback", "client", "quote"],
        "pricing":      ["pricing", "plan", "cost", "subscription", "tier"],
        "contact":      ["contact", "reach", "form", "email", "message", "inquiry"],
        "footer":       ["footer", "link", "social", "copyright"]
    }

    def detect_sections(self, description: str) -> list[str]:
        desc_lower = description.lower()
        sections = []
        for section, keywords in self.SECTION_KEYWORDS.items():
            if any(kw in desc_lower for kw in keywords):
                sections.append(section)
        if not sections:
            sections = ["hero", "features", "contact", "footer"]
        if "footer" not in sections:
            sections.append("footer")
        return sections

    def generate_meta_tags(self, title: str, description: str) -> str:
        return f"""
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description[:160]}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description[:200]}">
    <meta name="twitter:card" content="summary_large_image">
    <title>{title}</title>"""

    def build_hero(self, title: str, palette: dict) -> str:
        return f"""
  <section id="hero" class="hero-section">
    <div class="container">
      <div class="hero-badge">✨ Welcome</div>
      <h1 class="hero-title">{title}</h1>
      <p class="hero-subtitle">Transform your vision into reality with cutting-edge technology and professional design.</p>
      <div class="hero-cta">
        <a href="#contact" class="btn btn-primary">Get Started</a>
        <a href="#about" class="btn btn-secondary">Learn More</a>
      </div>
    </div>
  </section>"""

    def build_features(self, palette: dict) -> str:
        items = [
            ("⚡", "Lightning Fast", "Optimized for peak performance with modern architecture."),
            ("🎨", "Beautiful Design", "Stunning, modern aesthetics that captivate your audience."),
            ("📱", "Fully Responsive", "Perfect on every device, from mobile to desktop."),
            ("🔒", "Secure & Reliable", "Enterprise-grade security protecting your data 24/7."),
            ("🚀", "Easy to Deploy", "One-click deployment to any cloud platform."),
            ("💡", "Smart Insights", "AI-powered analytics to drive smarter decisions.")
        ]
        cards = "".join(f"""
      <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <h3>{name}</h3>
        <p>{desc}</p>
      </div>""" for icon, name, desc in items)
        return f"""
  <section id="features" class="features-section">
    <div class="container">
      <div class="section-header">
        <h2>Why Choose Us</h2>
        <p>Everything you need to build something extraordinary</p>
      </div>
      <div class="features-grid">{cards}
      </div>
    </div>
  </section>"""

    def build_about(self, palette: dict) -> str:
        return """
  <section id="about" class="about-section">
    <div class="container about-grid">
      <div class="about-visual">
        <div class="about-card">
          <div class="stat"><span class="stat-num">500+</span><span class="stat-label">Projects</span></div>
          <div class="stat"><span class="stat-num">99%</span><span class="stat-label">Satisfaction</span></div>
          <div class="stat"><span class="stat-num">5yr</span><span class="stat-label">Experience</span></div>
        </div>
      </div>
      <div class="about-content">
        <div class="section-tag">About Us</div>
        <h2>We Build Digital Experiences</h2>
        <p>We are a passionate team of designers and developers dedicated to crafting exceptional digital experiences. Our mission is to empower businesses with beautiful, functional web solutions.</p>
        <p>With over 5 years of experience and 500+ successful projects, we bring expertise and creativity to every engagement.</p>
        <a href="#contact" class="btn btn-primary">Work With Us</a>
      </div>
    </div>
  </section>"""

    def build_portfolio(self, palette: dict) -> str:
        items = [
            ("E-Commerce Platform", "Web Design"), ("Brand Identity", "Branding"),
            ("Mobile App UI", "UI/UX"), ("Corporate Website", "Development"),
            ("Dashboard Analytics", "Data Viz"), ("Marketing Campaign", "Strategy")
        ]
        cards = "".join(f"""
      <div class="portfolio-card">
        <div class="portfolio-img" style="background:linear-gradient(135deg,{palette['primary']}44,{palette['secondary']}44)">
          <span style="font-size:2.5rem">🖼️</span>
        </div>
        <div class="portfolio-info">
          <h4>{name}</h4><span class="tag">{cat}</span>
        </div>
      </div>""" for name, cat in items)
        return f"""
  <section id="portfolio" class="portfolio-section">
    <div class="container">
      <div class="section-header">
        <h2>Our Work</h2>
        <p>A showcase of our finest projects</p>
      </div>
      <div class="portfolio-grid">{cards}
      </div>
    </div>
  </section>"""

    def build_testimonials(self, palette: dict) -> str:
        items = [
            ("Sarah Chen", "CEO, TechCorp", "🌟🌟🌟🌟🌟",
             "Absolutely phenomenal work! The team delivered beyond our expectations. Our website traffic doubled after the redesign."),
            ("Marcus Reed", "Founder, StartupX", "🌟🌟🌟🌟🌟",
             "Professional, creative, and incredibly responsive. I couldn't be happier with the final product."),
            ("Aisha Patel", "CMO, BrandLab", "🌟🌟🌟🌟🌟",
             "A game-changer for our digital presence. The modern design significantly improved our conversion rates.")
        ]
        cards = "".join(f"""
      <div class="testimonial-card">
        <div class="stars">{stars}</div>
        <p>"{text}"</p>
        <div class="testimonial-author">
          <div class="author-avatar">{name[0]}</div>
          <div><strong>{name}</strong><br><small>{role}</small></div>
        </div>
      </div>""" for name, role, stars, text in items)
        return f"""
  <section id="testimonials" class="testimonials-section">
    <div class="container">
      <div class="section-header">
        <h2>What Our Clients Say</h2>
        <p>Real words from real people</p>
      </div>
      <div class="testimonials-grid">{cards}
      </div>
    </div>
  </section>"""

    def build_pricing(self, palette: dict) -> str:
        plans = [
            ("Starter", "$9", "/mo", ["5 Pages", "Basic SEO", "Email Support", "1 Domain"], False),
            ("Pro", "$29", "/mo", ["Unlimited Pages", "Advanced SEO", "Priority Support", "5 Domains", "Analytics"], True),
            ("Enterprise", "$99", "/mo", ["Custom Solutions", "Dedicated Manager", "24/7 Support", "Unlimited Domains", "Custom Integrations"], False)
        ]
        cards = "".join(f"""
      <div class="pricing-card {'featured' if featured else ''}">
        {'<div class="popular-badge">Most Popular</div>' if featured else ''}
        <h3>{name}</h3>
        <div class="price">{price}<span>{period}</span></div>
        <ul>{''.join(f'<li>✓ {f}</li>' for f in features)}</ul>
        <a href="#contact" class="btn {'btn-primary' if featured else 'btn-secondary'}">Get Started</a>
      </div>""" for name, price, period, features, featured in plans)
        return f"""
  <section id="pricing" class="pricing-section">
    <div class="container">
      <div class="section-header">
        <h2>Simple Pricing</h2>
        <p>Choose the plan that fits your needs</p>
      </div>
      <div class="pricing-grid">{cards}
      </div>
    </div>
  </section>"""

    def build_contact(self, palette: dict) -> str:
        return """
  <section id="contact" class="contact-section">
    <div class="container">
      <div class="section-header">
        <h2>Get In Touch</h2>
        <p>We'd love to hear from you</p>
      </div>
      <div class="contact-grid">
        <div class="contact-info">
          <div class="contact-item"><span>📧</span><div><strong>Email</strong><p>hello@yoursite.com</p></div></div>
          <div class="contact-item"><span>📞</span><div><strong>Phone</strong><p>+1 (555) 123-4567</p></div></div>
          <div class="contact-item"><span>📍</span><div><strong>Location</strong><p>San Francisco, CA</p></div></div>
        </div>
        <form class="contact-form" onsubmit="event.preventDefault(); alert('Message sent!')">
          <input type="text" placeholder="Your Name" required>
          <input type="email" placeholder="Your Email" required>
          <input type="text" placeholder="Subject">
          <textarea rows="5" placeholder="Your Message" required></textarea>
          <button type="submit" class="btn btn-primary">Send Message</button>
        </form>
      </div>
    </div>
  </section>"""

    def build_footer(self, title: str, palette: dict) -> str:
        return f"""
  <footer class="footer">
    <div class="container footer-grid">
      <div class="footer-brand">
        <h3>{title}</h3>
        <p>Building beautiful web experiences for forward-thinking businesses.</p>
        <div class="social-links">
          <a href="#">🐦</a><a href="#">💼</a><a href="#">📷</a><a href="#">🐙</a>
        </div>
      </div>
      <div class="footer-links">
        <h4>Quick Links</h4>
        <ul>
          <li><a href="#hero">Home</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#features">Features</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </div>
      <div class="footer-links">
        <h4>Legal</h4>
        <ul>
          <li><a href="#">Privacy Policy</a></li>
          <li><a href="#">Terms of Service</a></li>
          <li><a href="#">Cookie Policy</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2025 {title}. All rights reserved. | Built with HTML Quick-Styler 🚀</p>
    </div>
  </footer>"""


# ============================================================
# CELL 6: CSS Generator
# ============================================================
def generate_css(palette: dict) -> str:
    p = palette
    return f"""
  :root {{
    --primary:    {p['primary']};
    --secondary:  {p['secondary']};
    --accent:     {p['accent']};
    --bg:         {p['background']};
    --surface:    {p['surface']};
    --text:       {p['text_primary']};
    --muted:      {p['text_secondary']};
    --border:     {p['border']};
  }}
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; }}
  body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}

  /* ---- Navbar ---- */
  nav {{ position: sticky; top: 0; z-index: 1000; background: rgba(15,23,42,0.85); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); padding: 1rem 0; }}
  .nav-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 2rem; display: flex; justify-content: space-between; align-items: center; }}
  .nav-logo {{ font-size: 1.4rem; font-weight: 800; color: var(--primary); text-decoration: none; }}
  .nav-links {{ display: flex; gap: 2rem; list-style: none; }}
  .nav-links a {{ color: var(--muted); text-decoration: none; font-size: 0.95rem; transition: color .3s; }}
  .nav-links a:hover {{ color: var(--text); }}
  .nav-cta {{ background: var(--primary); color: #fff; padding: .5rem 1.2rem; border-radius: 8px; text-decoration: none; font-size: .9rem; font-weight: 600; }}

  /* ---- Containers & Sections ---- */
  .container {{ max-width: 1200px; margin: 0 auto; padding: 0 2rem; }}
  section {{ padding: 5rem 0; }}
  .section-header {{ text-align: center; margin-bottom: 3rem; }}
  .section-header h2 {{ font-size: clamp(1.8rem, 4vw, 2.5rem); font-weight: 800; margin-bottom: 0.75rem; }}
  .section-header p {{ color: var(--muted); font-size: 1.1rem; }}
  .section-tag {{ display: inline-block; background: {p['primary']}22; color: var(--primary); padding: .3rem .9rem; border-radius: 999px; font-size: .85rem; font-weight: 600; margin-bottom: 1rem; }}

  /* ---- Buttons ---- */
  .btn {{ display: inline-block; padding: .75rem 1.75rem; border-radius: 10px; font-weight: 700; font-size: .95rem; text-decoration: none; cursor: pointer; border: none; transition: transform .2s, box-shadow .2s; }}
  .btn-primary {{ background: var(--primary); color: #fff; }}
  .btn-primary:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px {p['primary']}44; }}
  .btn-secondary {{ background: transparent; color: var(--text); border: 2px solid var(--border); }}
  .btn-secondary:hover {{ border-color: var(--primary); color: var(--primary); }}

  /* ---- Hero ---- */
  .hero-section {{ min-height: 90vh; display: flex; align-items: center; background: radial-gradient(ellipse at 50% 0%, {p['primary']}22 0%, transparent 70%); text-align: center; }}
  .hero-badge {{ display: inline-block; background: {p['accent']}22; color: var(--accent); border: 1px solid {p['accent']}44; padding: .4rem 1rem; border-radius: 999px; font-size: .85rem; font-weight: 600; margin-bottom: 1.5rem; }}
  .hero-title {{ font-size: clamp(2.5rem, 6vw, 4rem); font-weight: 900; line-height: 1.1; margin-bottom: 1.25rem; background: linear-gradient(135deg, var(--text), var(--primary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
  .hero-subtitle {{ color: var(--muted); font-size: 1.25rem; max-width: 600px; margin: 0 auto 2rem; }}
  .hero-cta {{ display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }}

  /* ---- Features ---- */
  .features-section {{ background: var(--surface); }}
  .features-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }}
  .feature-card {{ background: var(--bg); border: 1px solid var(--border); border-radius: 16px; padding: 2rem; transition: transform .3s, border-color .3s; }}
  .feature-card:hover {{ transform: translateY(-6px); border-color: var(--primary); }}
  .feature-icon {{ font-size: 2.2rem; margin-bottom: 1rem; }}
  .feature-card h3 {{ font-size: 1.1rem; font-weight: 700; margin-bottom: .5rem; }}
  .feature-card p {{ color: var(--muted); font-size: .95rem; }}

  /* ---- About ---- */
  .about-grid {{ display: grid; grid-template-columns: 1fr 1.5fr; gap: 4rem; align-items: center; }}
  .about-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 20px; padding: 2.5rem; display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; text-align: center; }}
  .stat-num {{ display: block; font-size: 2rem; font-weight: 900; color: var(--primary); }}
  .stat-label {{ font-size: .85rem; color: var(--muted); }}
  .about-content h2 {{ font-size: clamp(1.8rem, 3vw, 2.2rem); font-weight: 800; margin-bottom: 1rem; }}
  .about-content p {{ color: var(--muted); margin-bottom: 1rem; }}

  /* ---- Portfolio ---- */
  .portfolio-section {{ background: var(--surface); }}
  .portfolio-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }}
  .portfolio-card {{ background: var(--bg); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; transition: transform .3s; }}
  .portfolio-card:hover {{ transform: translateY(-6px); }}
  .portfolio-img {{ height: 200px; display: flex; align-items: center; justify-content: center; }}
  .portfolio-info {{ padding: 1.25rem; display: flex; justify-content: space-between; align-items: center; }}
  .portfolio-info h4 {{ font-size: 1rem; font-weight: 700; }}
  .tag {{ font-size: .75rem; background: {p['primary']}22; color: var(--primary); padding: .3rem .7rem; border-radius: 999px; }}

  /* ---- Testimonials ---- */
  .testimonials-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }}
  .testimonial-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 2rem; }}
  .stars {{ font-size: 1.1rem; margin-bottom: .75rem; }}
  .testimonial-card p {{ color: var(--muted); font-style: italic; margin-bottom: 1.25rem; }}
  .testimonial-author {{ display: flex; align-items: center; gap: 1rem; }}
  .author-avatar {{ width: 44px; height: 44px; border-radius: 50%; background: var(--primary); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.1rem; }}

  /* ---- Pricing ---- */
  .pricing-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1.5rem; align-items: start; }}
  .pricing-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 20px; padding: 2.5rem; position: relative; }}
  .pricing-card.featured {{ border-color: var(--primary); background: linear-gradient(180deg, {p['primary']}11 0%, var(--surface) 100%); }}
  .popular-badge {{ position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: var(--primary); color: #fff; padding: .3rem .9rem; border-radius: 999px; font-size: .8rem; font-weight: 700; white-space: nowrap; }}
  .pricing-card h3 {{ font-size: 1.2rem; font-weight: 700; margin-bottom: .5rem; }}
  .price {{ font-size: 2.5rem; font-weight: 900; color: var(--primary); margin-bottom: 1.5rem; }}
  .price span {{ font-size: 1rem; font-weight: 400; color: var(--muted); }}
  .pricing-card ul {{ list-style: none; margin-bottom: 2rem; }}
  .pricing-card li {{ padding: .5rem 0; color: var(--muted); border-bottom: 1px solid var(--border); font-size: .95rem; }}
  .pricing-card .btn {{ width: 100%; text-align: center; }}

  /* ---- Contact ---- */
  .contact-section {{ background: var(--surface); }}
  .contact-grid {{ display: grid; grid-template-columns: 1fr 1.5fr; gap: 3rem; align-items: start; }}
  .contact-item {{ display: flex; gap: 1rem; align-items: flex-start; margin-bottom: 1.5rem; font-size: 1.5rem; }}
  .contact-item p {{ color: var(--muted); font-size: .95rem; margin: 0; }}
  .contact-form {{ display: flex; flex-direction: column; gap: 1rem; }}
  .contact-form input, .contact-form textarea {{ background: var(--bg); border: 1px solid var(--border); border-radius: 10px; padding: .85rem 1.1rem; color: var(--text); font-size: .95rem; font-family: inherit; transition: border-color .3s; }}
  .contact-form input:focus, .contact-form textarea:focus {{ outline: none; border-color: var(--primary); }}
  .contact-form textarea {{ resize: vertical; min-height: 120px; }}
  .contact-form .btn {{ align-self: flex-start; }}

  /* ---- Footer ---- */
  .footer {{ background: var(--bg); border-top: 1px solid var(--border); padding: 4rem 0 0; }}
  .footer-grid {{ display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 3rem; padding-bottom: 3rem; }}
  .footer-brand h3 {{ font-size: 1.3rem; font-weight: 800; color: var(--primary); margin-bottom: .75rem; }}
  .footer-brand p {{ color: var(--muted); font-size: .95rem; margin-bottom: 1.5rem; }}
  .social-links {{ display: flex; gap: .75rem; font-size: 1.5rem; }}
  .social-links a {{ text-decoration: none; transition: transform .2s; }}
  .social-links a:hover {{ transform: scale(1.2); }}
  .footer-links h4 {{ font-size: 1rem; font-weight: 700; margin-bottom: 1rem; }}
  .footer-links ul {{ list-style: none; }}
  .footer-links li {{ margin-bottom: .6rem; }}
  .footer-links a {{ color: var(--muted); text-decoration: none; font-size: .9rem; transition: color .3s; }}
  .footer-links a:hover {{ color: var(--text); }}
  .footer-bottom {{ border-top: 1px solid var(--border); padding: 1.5rem 2rem; text-align: center; color: var(--muted); font-size: .875rem; }}

  /* ---- Responsive ---- */
  @media (max-width: 768px) {{
    .about-grid, .contact-grid, .footer-grid {{ grid-template-columns: 1fr; }}
    .nav-links {{ display: none; }}
    .hero-cta {{ flex-direction: column; align-items: center; }}
  }}"""


# ============================================================
# CELL 7: AI-powered generation with IBM Granite
# ============================================================
def ai_enhance_content(title: str, description: str, section: str) -> str:
    """Use IBM Granite to generate enhanced content for a section."""
    prompt = f"""Generate a compelling, professional {section} section headline and tagline for a website.
Website: {title}
Description: {description}
Respond with ONLY a JSON object: {{"headline": "...", "tagline": "..."}}"""
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs, max_new_tokens=80,
                temperature=0.7, do_sample=True, pad_token_id=tokenizer.eos_token_id
            )
        generated = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
        match = re.search(r'\{.*?\}', generated, re.DOTALL)
        if match:
            import json
            data = json.loads(match.group())
            return data.get("headline", title)
    except Exception:
        pass
    return title


# ============================================================
# CELL 8: Full Page Assembly
# ============================================================
def generate_page(page_title: str, description: str, color_style: str, use_ai: bool) -> str:
    palette = ColorPaletteGenerator.get_palette(color_style)
    builder = HTMLPageBuilder()
    sections = builder.detect_sections(description)
    css = generate_css(palette)

    title = ai_enhance_content(page_title, description, "hero") if use_ai else page_title
    meta = builder.generate_meta_tags(title, description)

    section_html = ""
    section_map = {
        "hero":         lambda: builder.build_hero(title, palette),
        "features":     lambda: builder.build_features(palette),
        "about":        lambda: builder.build_about(palette),
        "portfolio":    lambda: builder.build_portfolio(palette),
        "testimonials": lambda: builder.build_testimonials(palette),
        "pricing":      lambda: builder.build_pricing(palette),
        "contact":      lambda: builder.build_contact(palette),
        "footer":       lambda: builder.build_footer(title, palette),
    }
    nav_items = [s for s in sections if s != "footer"]
    nav_links = "".join(f'<li><a href="#{s}">{s.capitalize()}</a></li>' for s in nav_items)
    navbar = f"""
<nav>
  <div class="nav-inner">
    <a class="nav-logo" href="#">{title}</a>
    <ul class="nav-links">{nav_links}</ul>
    <a class="nav-cta" href="#contact">Get Started</a>
  </div>
</nav>"""
    for sec in sections:
        if sec in section_map:
            section_html += section_map[sec]()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>{meta}
<style>{css}
</style>
</head>
<body>
{navbar}
{section_html}
</body>
</html>"""


# ============================================================
# CELL 9: Gradio Interface
# ============================================================
def create_interface():
    palette_gen  = ColorPaletteGenerator()
    page_builder = HTMLPageBuilder()

    def on_generate(title, desc, style, use_ai, progress=gr.Progress()):
        if not title.strip():
            return "<p style='color:red'>Please enter a page title.</p>", ""
        progress(0.2, desc="Detecting sections...")
        sections = page_builder.detect_sections(desc)
        progress(0.5, desc="Generating HTML...")
        html = generate_page(title, desc, style, use_ai)
        progress(1.0, desc="Done!")
        sections_info = ", ".join(s.capitalize() for s in sections)
        summary = f"✅ Generated {len(sections)} sections: {sections_info}"
        return html, summary

    def save_html(html_code, filename):
        if not filename.strip():
            filename = "my_website"
        path = f"/content/{filename.replace(' ', '_')}.html"
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_code)
        return path, f"✅ Saved to {path}"

    with gr.Blocks(
        title="HTML Quick-Styler",
        theme=gr.themes.Base(primary_hue="violet", neutral_hue="slate"),
        css=".gradio-container {max-width: 1280px !important}"
    ) as demo:

        gr.Markdown("""
# 🚀 HTML Quick-Styler
### AI-Powered HTML Page Generator with IBM Granite 3.3 2B
""")

        with gr.Tabs():

            # ---------- TAB 1: Generate ----------
            with gr.TabItem("⚡ Generate Page"):
                with gr.Row():
                    with gr.Column(scale=1):
                        title_input  = gr.Textbox(label="Page Title", placeholder="My Awesome Website")
                        desc_input   = gr.Textbox(label="Description", lines=5,
                            placeholder="Hero section with welcome message, features list, about section, portfolio gallery, testimonials, pricing plans, contact form, and footer")
                        style_input  = gr.Dropdown(
                            choices=["modern","vibrant","ocean","forest","sunset","luxury","creative","minimal"],
                            value="modern", label="Color Style")
                        ai_toggle    = gr.Checkbox(label="Use IBM Granite AI Enhancement", value=True)
                        gen_btn      = gr.Button("🎨 Generate HTML", variant="primary", size="lg")
                        status_out   = gr.Textbox(label="Status", interactive=False)
                    with gr.Column(scale=2):
                        html_output  = gr.Code(language="html", label="Generated HTML", lines=30)
                        with gr.Row():
                            fname_input  = gr.Textbox(label="Filename", value="my_website", scale=3)
                            save_btn     = gr.Button("💾 Save", scale=1)
                        save_status  = gr.Textbox(label="Save Status", interactive=False)
                        save_path    = gr.File(label="Download HTML", visible=False)

                gen_btn.click(on_generate, [title_input, desc_input, style_input, ai_toggle],
                              [html_output, status_out])
                save_btn.click(save_html, [html_output, fname_input], [save_path, save_status])

            # ---------- TAB 2: Live Preview ----------
            with gr.TabItem("👁️ Live Preview"):
                preview_in  = gr.Code(language="html", label="Paste HTML here", lines=20)
                preview_btn = gr.Button("🔄 Refresh Preview", variant="primary")
                preview_out = gr.HTML(label="Preview")
                preview_btn.click(lambda x: x, [preview_in], [preview_out])
                gr.Markdown("*Paste your generated HTML and click Refresh Preview*")

            # ---------- TAB 3: Color Palettes ----------
            with gr.TabItem("🎨 Color Palettes"):
                gr.HTML(palette_gen.generate_palette_preview_html())

            # ---------- TAB 4: Templates ----------
            with gr.TabItem("📋 Quick Templates"):
                with gr.Row():
                    for label, ttl, desc, style in [
                        ("Portfolio", "Creative Portfolio", "Hero section with welcome message, portfolio gallery, about section, testimonials, contact form, footer", "modern"),
                        ("SaaS Landing", "SaaS Product", "Hero banner, features showcase, pricing plans, testimonials, call to action, footer", "vibrant"),
                        ("Corporate", "Corporate Site", "Hero section, company about, services features, team section, contact form, footer", "luxury"),
                    ]:
                        with gr.Column():
                            gr.Markdown(f"### {label}")
                            if gr.Button(f"Use {label} Template"):
                                pass  # handled below via JS in real deployment

            # ---------- TAB 5: Guide ----------
            with gr.TabItem("📖 Guide"):
                gr.Markdown("""
## How to Use HTML Quick-Styler

### Step 1: Describe Your Page
Enter your page title and describe the sections you want. Example:
> *"Hero section with welcome, features grid, about section, portfolio gallery, testimonials, pricing table, contact form, and footer"*

### Step 2: Choose Color Style
- **modern** – Indigo & purple, dark theme
- **vibrant** – Coral & teal, high energy
- **ocean** – Blues, calm and professional
- **forest** – Greens, natural feel
- **sunset** – Warm oranges, inviting
- **luxury** – Gold, premium feel
- **creative** – Purple & cyan, bold
- **minimal** – Grayscale, clean

### Step 3: Generate
Click **Generate HTML** to produce your page.

### Step 4: Preview & Download
- Paste generated code in **Live Preview** tab
- Click **Save** to download the HTML file

### Supported Sections
`hero` `features` `about` `portfolio` `testimonials` `pricing` `contact` `footer`
""")

    return demo


# ============================================================
# CELL 10: Launch
# ============================================================
demo = create_interface()
demo.launch(share=True, debug=True)
