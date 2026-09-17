import pypdf
import re
import html
import json

reader = pypdf.PdfReader('Antellay_Terms_Conditions.pdf')

doc_metadata = [
    {
        "id": "terms",
        "title": "Terms & Conditions",
        "subtitle": "User Agreement, Platform Governance & Operational Standards",
        "icon": "fa-file-contract",
        "start": 1,
        "end": 7,
        "summary": [
            {
                "icon": "fa-satellite",
                "title": "Space Tech & AI Purpose",
                "desc": "Platform provides software, telemetry analysis, orbital visualizations, and AI models for the space economy."
            },
            {
                "icon": "fa-shield-halved",
                "title": "No Sole Critical Reliance",
                "desc": "Information is for analytical and decision-support; not certified as sole emergency/flight control without enterprise SLA."
            },
            {
                "icon": "fa-copyright",
                "title": "Proprietary SpaceOS",
                "desc": "All SpaceOS software, models, and branding belong to ANTELLAY Labs. Third-party data remains with respective owners."
            },
            {
                "icon": "fa-scale-balanced",
                "title": "Governing Jurisdiction",
                "desc": "Governed by the laws of India, with exclusive judicial jurisdiction vested in the competent courts of Jaipur, Rajasthan."
            }
        ]
    },
    {
        "id": "privacy",
        "title": "Privacy Policy",
        "subtitle": "Data Protection Practices, Personal Information Handling & User Rights",
        "icon": "fa-user-shield",
        "start": 8,
        "end": 14,
        "summary": [
            {
                "icon": "fa-ban",
                "title": "Zero Data Selling",
                "desc": "We never sell, rent, or monetize your personal or organization data to data brokers or third parties."
            },
            {
                "icon": "fa-globe",
                "title": "Space Data Separation",
                "desc": "Orbital coordinates, space weather, and satellite telemetry do not constitute personal information."
            },
            {
                "icon": "fa-lock",
                "title": "Bank-Grade Encryption",
                "desc": "Technical safeguards, encrypted data transmission, authentication tokens, and strict access control."
            },
            {
                "icon": "fa-user-check",
                "title": "Full User Rights",
                "desc": "Comprehensive rights to access, review, correct, export, or request deletion of your personal data."
            }
        ]
    },
    {
        "id": "cookies",
        "title": "Cookie Policy",
        "subtitle": "Browser Technologies, Session Management & Tracking Preferences",
        "icon": "fa-cookie-bite",
        "start": 15,
        "end": 18,
        "summary": [
            {
                "icon": "fa-key",
                "title": "Essential Cookies",
                "desc": "Required for authentication, secure login sessions, and basic platform navigation."
            },
            {
                "icon": "fa-sliders",
                "title": "Functional Choices",
                "desc": "Used to remember user preferences, interface themes, and display settings."
            },
            {
                "icon": "fa-chart-pie",
                "title": "Anonymous Analytics",
                "desc": "Aggregated diagnostic information to identify performance bottlenecks and improve features."
            },
            {
                "icon": "fa-toggle-on",
                "title": "Browser Controls",
                "desc": "Users can modify, block, or delete stored cookies via browser privacy settings anytime."
            }
        ]
    },
    {
        "id": "disclaimer",
        "title": "General Disclaimer",
        "subtitle": "Space, Satellite, Orbital Tracking & Near-Real-Time Data Limitations",
        "icon": "fa-triangle-exclamation",
        "start": 19,
        "end": 24,
        "summary": [
            {
                "icon": "fa-clock",
                "title": "Near-Real-Time Data",
                "desc": "Live satellite positions may experience provider delays, calculation revisions, and network latency."
            },
            {
                "icon": "fa-satellite-dish",
                "title": "Third-Party Feeds",
                "desc": "Orbital elements originate from authorized public and third-party catalogs without ownership claims."
            },
            {
                "icon": "fa-triangle-exclamation",
                "title": "Independent Validation",
                "desc": "Do not rely exclusively on outputs for mission-critical flight, safety, or navigational decisions."
            },
            {
                "icon": "fa-chart-line",
                "title": "No Financial Advice",
                "desc": "Space economy growth figures and research data do not constitute investment or financial solicitations."
            }
        ]
    },
    {
        "id": "ai-spaceos",
        "title": "AI & SpaceOS Disclaimer",
        "subtitle": "Predictive Models, Machine Learning Outputs & Simulation Boundaries",
        "icon": "fa-brain",
        "start": 36,
        "end": 42,
        "summary": [
            {
                "icon": "fa-microchip",
                "title": "AI-Driven Models",
                "desc": "Predictive analytics and simulations are algorithmic outputs designed to assist human decisions."
            },
            {
                "icon": "fa-user-gear",
                "title": "Mandatory Human Oversight",
                "desc": "Consequential space mission actions require professional engineering validation and human review."
            },
            {
                "icon": "fa-network-wired",
                "title": "No Autonomous Flight Control",
                "desc": "Software interfaces do not imply unmonitored autonomous commanding of external spacecraft."
            },
            {
                "icon": "fa-flask",
                "title": "Simulation & Synthetic Data",
                "desc": "Simulated trajectories and synthetic models represent hypothetical scenarios unless specified."
            }
        ]
    },
    {
        "id": "acceptable-use",
        "title": "Acceptable Use Policy",
        "subtitle": "Operational Security Standards, Rules of Engagement & Infrastructure Defense",
        "icon": "fa-shield-halved",
        "start": 43,
        "end": 50,
        "summary": [
            {
                "icon": "fa-check",
                "title": "Permitted Research",
                "desc": "Authorized space research, educational analysis, software exploration, and legitimate API integrations."
            },
            {
                "icon": "fa-ban",
                "title": "Strictly Prohibited",
                "desc": "Attacking systems, unauthorized scraping, penetration tests, jamming, or interfering with satellites."
            },
            {
                "icon": "fa-shield-virus",
                "title": "Cybersecurity Safeguards",
                "desc": "No malware deployment, credential sharing, denial-of-service, or bypassing access controls."
            },
            {
                "icon": "fa-gavel",
                "title": "Strict Enforcement",
                "desc": "Immediate suspension, access revocation, and reporting to legal authorities for malicious acts."
            }
        ]
    },
    {
        "id": "data-api",
        "title": "Data & API Policy",
        "subtitle": "Data Ingestion, Sourcing Standards, Rate Limits & Integration Rights",
        "icon": "fa-database",
        "start": 28,
        "end": 35,
        "summary": [
            {
                "icon": "fa-cloud-arrow-down",
                "title": "Multisource Ingestion",
                "desc": "Data normalized from public catalogs, government APIs, research datasets, and proprietary calculations."
            },
            {
                "icon": "fa-gauge-high",
                "title": "API Quotas & Rate Limits",
                "desc": "Enforced request quotas and concurrency limits to maintain high-availability infrastructure."
            },
            {
                "icon": "fa-share-nodes",
                "title": "Redistribution Rules",
                "desc": "Commercial redistribution or reselling of proprietary datasets requires explicit written licensing."
            },
            {
                "icon": "fa-award",
                "title": "Source Attribution",
                "desc": "Preserve all original third-party licensing and source attribution headers when using data."
            }
        ]
    },
    {
        "id": "security",
        "title": "Security & Responsible Disclosure",
        "subtitle": "Vulnerability Reporting Protocols, Good-Faith Research & Infrastructure Defense",
        "icon": "fa-lock",
        "start": 94,
        "end": 102,
        "summary": [
            {
                "icon": "fa-envelope-open-text",
                "title": "Report Channel",
                "desc": "Direct vulnerability reports to space@antellay.com with proof of concept and impact assessment."
            },
            {
                "icon": "fa-handshake",
                "title": "Good-Faith Protection",
                "desc": "We support responsible researchers acting in good faith without service disruption or data theft."
            },
            {
                "icon": "fa-user-lock",
                "title": "Privacy Preservation",
                "desc": "Never access, modify, or download customer data during authorized security evaluations."
            },
            {
                "icon": "fa-timeline",
                "title": "Coordinated Remediation",
                "desc": "Prompt acknowledgment, structured verification, rapid patching, and coordinated disclosure."
            }
        ]
    },
    {
        "id": "refunds",
        "title": "Refund & Cancellation Policy",
        "subtitle": "Commercial Subscriptions, Billing Inquiries & Transaction Terms",
        "icon": "fa-receipt",
        "start": 118,
        "end": 125,
        "summary": [
            {
                "icon": "fa-calendar-xmark",
                "title": "Subscription Cancellation",
                "desc": "Cancel enterprise or SaaS subscriptions at any time effective at the end of the billing period."
            },
            {
                "icon": "fa-rotate-left",
                "title": "Refund Evaluation",
                "desc": "Refunds considered for duplicate transactions, technical billing errors, or material delivery failure."
            },
            {
                "icon": "fa-code-branch",
                "title": "Custom Development",
                "desc": "Milestone payments and delivered engineering work are non-refundable as stated in SOWs."
            },
            {
                "icon": "fa-headset",
                "title": "Billing Assistance",
                "desc": "Contact billing team directly at space@antellay.com with invoice details for fast resolution."
            }
        ]
    },
    {
        "id": "notice",
        "title": "Legal Notice & Operator",
        "subtitle": "Website Operator, Corporate Identity & Official Contact Channels",
        "icon": "fa-landmark",
        "start": 25,
        "end": 27,
        "summary": [
            {
                "icon": "fa-building",
                "title": "Operating Entity",
                "desc": "ANTELLAY Space is operated by ANTELLAY Labs, registered in Jaipur, Rajasthan, India."
            },
            {
                "icon": "fa-envelope",
                "title": "Official Contact",
                "desc": "Email: space@antellay.com & space.antellay@gmail.com | Phone: +91 97846 26443."
            },
            {
                "icon": "fa-shield",
                "title": "Brand Protection",
                "desc": "All logos, trademarks, and SpaceOS technology represent protected intellectual property."
            },
            {
                "icon": "fa-gavel",
                "title": "Legal Jurisdiction",
                "desc": "Governed by the laws of India, subject to courts having jurisdiction in Jaipur, Rajasthan."
            }
        ]
    }
]

def determine_tag(title):
    t = title.lower()
    if any(k in t for k in ["prohibit", "unlawful", "hack", "abuse"]):
        return ("PROHIBITED ACTIVITIES", "tag-danger")
    if any(k in t for k in ["permit", "purpose", "scope", "about"]):
        return ("PLATFORM SCOPE", "tag-success")
    if any(k in t for k in ["disclaim", "limitation", "warning", "guarantee", "critical", "reliance"]):
        return ("IMPORTANT NOTICE", "tag-warning")
    if any(k in t for k in ["privacy", "data", "security", "cookie", "storage"]):
        return ("DATA & SECURITY", "tag-info")
    if any(k in t for k in ["govern", "law", "jurisdiction", "regulatory", "compliance"]):
        return ("LEGAL COMPLIANCE", "tag-legal")
    if any(k in t for k in ["ai", "spaceos", "model", "simulation"]):
        return ("AI & SPACEOS", "tag-ai")
    if any(k in t for k in ["intellectual", "property", "copyright", "trademark"]):
        return ("INTELLECTUAL PROPERTY", "tag-ip")
    if any(k in t for k in ["contact", "operator", "notice"]):
        return ("OFFICIAL CONTACT", "tag-contact")
    return ("POLICY CLAUSE", "tag-neutral")

def parse_document_sections(start_p, end_p):
    raw_pages = []
    for p in range(start_p - 1, end_p):
        txt = reader.pages[p].extract_text(extraction_mode='layout') or ''
        raw_pages.append(txt)
    
    full_text = "\n\n".join(raw_pages)
    full_text = full_text.replace('\ufffd', '"')
    
    # Isolate section headings
    full_text = re.sub(r'(\n|^)\s*(\d+\.\s+[A-Za-z0-9\s&,–\-\(\)\/]+?)\s*(?=\n)', r'\n\n===SEC===\2\n\n', full_text)
    
    parts = full_text.split('===SEC===')
    intro_part = parts[0]
    sec_parts = parts[1:]
    
    # Clean intro lines
    intro_lines = [l.strip() for l in intro_part.split('\n') if l.strip()]
    cleaned_intro = []
    for l in intro_lines:
        if any(x in l.lower() for x in ["terms & conditions", "privacy policy", "cookie policy", "disclaimer", "legal notice", "data & api", "ai & spaceos", "acceptable use", "refund & cancellation"]):
            continue
        if "last updated: 15 september 2026" in l.lower():
            continue
        if "building the ai operating system for the space economy" in l.lower():
            continue
        cleaned_intro.append(l)
        
    intro_html = ""
    if cleaned_intro:
        intro_p = re.sub(r'\s+', ' ', " ".join(cleaned_intro)).strip()
        intro_html = f'<div class="legal-intro-banner"><i class="fa-solid fa-circle-info"></i> <p>{html.escape(intro_p)}</p></div>'
        
    sections = []
    for sp in sec_parts:
        lines = [l.strip() for l in sp.split('\n') if l.strip()]
        if not lines:
            continue
        sec_header = lines[0]
        content_lines = lines[1:]
        
        m = re.match(r'^(\d+)\.\s+(.+)$', sec_header)
        if m:
            sec_num = m.group(1)
            sec_title = m.group(2).strip()
        else:
            sec_num = "•"
            sec_title = sec_header
            
        tag_text, tag_class = determine_tag(sec_title)
        
        # Now process paragraphs and lists inside this section
        body_parts = []
        raw_content = "\n".join(content_lines)
        
        # Split into subsections if any: "2.1 Permitted Use"
        raw_content = re.sub(r'(\n|^)\s*(\d+\.\d+\s+[A-Za-z0-9\s&,–\-\(\)\/]+?)\s*(?=\n)', r'\n\n===SUB===\2\n\n', raw_content)
        
        blocks = [b.strip() for b in re.split(r'\n\s*\n', raw_content) if b.strip()]
        
        for block in blocks:
            if block.startswith('===SUB==='):
                sub_txt = block.replace('===SUB===', '').strip()
                sub_lines = [sl.strip() for sl in sub_txt.split('\n') if sl.strip()]
                sub_heading = sub_lines[0]
                sm = re.match(r'^(\d+\.\d+)\s+(.+)$', sub_heading)
                if sm:
                    body_parts.append(f'<h4 class="subsec-heading"><span class="subsec-num">{sm.group(1)}</span> {html.escape(sm.group(2))}</h4>')
                else:
                    body_parts.append(f'<h4 class="subsec-heading">{html.escape(sub_heading)}</h4>')
                # Process remaining lines in sub block if any
                block = "\n".join(sub_lines[1:])
                if not block.strip():
                    continue
                    
            b_lines = [l.strip() for l in block.split('\n') if l.strip()]
            
            # Check if this block has bullet items
            has_bullets = any(l.startswith('●') or l.startswith('•') or l.startswith('- ') or l.startswith('* ') for l in b_lines)
            if has_bullets:
                intro = []
                bullets = []
                current_b = []
                for bl in b_lines:
                    if bl.startswith('●') or bl.startswith('•') or bl.startswith('- ') or bl.startswith('* '):
                        if current_b:
                            bullets.append(" ".join(current_b))
                            current_b = []
                        current_b.append(re.sub(r'^[●•\-\*]\s*', '', bl))
                    elif current_b:
                        current_b.append(bl)
                    else:
                        intro.append(bl)
                if current_b:
                    bullets.append(" ".join(current_b))
                    
                if intro:
                    intro_txt = re.sub(r'\s+', ' ', " ".join(intro)).strip()
                    body_parts.append(f'<p class="list-lead">{html.escape(intro_txt)}</p>')
                    
                if bullets:
                    body_parts.append('<ul class="legal-list">')
                    for item in bullets:
                        item_clean = re.sub(r'\s+', ' ', item).strip()
                        body_parts.append(f'  <li><span class="bullet-dot"></span><span>{html.escape(item_clean)}</span></li>')
                    body_parts.append('</ul>')
                continue
                
            # Check if this block is Contact details
            clean_b = re.sub(r'\s+', ' ', block).strip()
            if ("email:" in clean_b.lower() or "phone:" in clean_b.lower()) and "antellay" in clean_b.lower():
                body_parts.append('<div class="legal-contact-card">')
                body_parts.append('  <div class="contact-entity"><i class="fa-solid fa-building"></i> <strong>ANTELLAY Space</strong> (Operated by ANTELLAY Labs)</div>')
                body_parts.append('  <div class="contact-location"><i class="fa-solid fa-location-dot"></i> Jaipur, Rajasthan, India</div>')
                body_parts.append('  <div class="contact-grid">')
                body_parts.append('    <a href="mailto:space@antellay.com" class="contact-pill"><i class="fa-solid fa-envelope"></i> space@antellay.com</a>')
                body_parts.append('    <a href="tel:+919784626443" class="contact-pill"><i class="fa-solid fa-phone"></i> +91 97846 26443</a>')
                body_parts.append('  </div>')
                body_parts.append('</div>')
                continue
                
            # Check if Governing Law
            if "governing law" in sec_title.lower() or "jaipur, rajasthan" in clean_b.lower():
                body_parts.append(f'<p>{html.escape(clean_b)}</p>')
                body_parts.append('<div class="law-jurisdiction-box"><div class="jurisdiction-icon"><img src="https://flagcdn.com/w40/in.png" width="22" alt="India"></div><div><strong>Jurisdiction: Jaipur, Rajasthan, India</strong><p>Applicable Law: Laws of the Republic of India. Subject to the competent courts in Jaipur.</p></div></div>')
                continue
                
            # Normal paragraph
            body_parts.append(f'<p>{html.escape(clean_b)}</p>')
            
        sections.append({
            "num": sec_num,
            "title": sec_title,
            "tag": tag_text,
            "tag_class": tag_class,
            "html": "\n".join(body_parts)
        })
        
    return intro_html, sections

# Generate all documents structured HTML
all_docs_html = []
all_tabs_html = []

for idx, doc in enumerate(doc_metadata):
    active_class = "active" if idx == 0 else ""
    aria_selected = "true" if idx == 0 else "false"
    display_style = "block" if idx == 0 else "none"
    
    intro_html, sections = parse_document_sections(doc["start"], doc["end"])
    
    # Tab button
    all_tabs_html.append(f'''
    <button class="policy-tab-btn {active_class}" data-target="{doc['id']}" role="tab" aria-selected="{aria_selected}">
      <div class="tab-icon"><i class="fa-solid {doc['icon']}"></i></div>
      <div class="tab-text">
        <span class="tab-title">{html.escape(doc['title'])}</span>
        <span class="tab-sub">{html.escape(doc['subtitle'])}</span>
      </div>
      <i class="fa-solid fa-chevron-right tab-arrow"></i>
    </button>''')
    
    # Document Header & Summary Cards
    summary_cards_html = []
    for sc in doc["summary"]:
        summary_cards_html.append(f'''
        <div class="exec-card">
          <div class="exec-card-icon"><i class="fa-solid {sc['icon']}"></i></div>
          <div class="exec-card-content">
            <h5>{html.escape(sc['title'])}</h5>
            <p>{html.escape(sc['desc'])}</p>
          </div>
        </div>''')
        
    summary_grid = "\n".join(summary_cards_html)
    
    # Table of Contents chips for in-page navigation
    toc_chips = []
    for sec in sections:
        toc_chips.append(f'<a href="#{doc["id"]}-sec-{sec["num"]}" class="toc-chip"><span class="chip-num">{sec["num"]}</span> {html.escape(sec["title"])}</a>')
    toc_bar_html = "\n".join(toc_chips)
    
    # Section Cards
    cards_html = []
    for sec in sections:
        cards_html.append(f'''
        <section class="legal-card" id="{doc['id']}-sec-{sec['num']}">
          <header class="legal-card-header">
            <div class="header-left">
              <span class="sec-badge">{sec['num']}</span>
              <h3 class="card-title">{html.escape(sec['title'])}</h3>
            </div>
            <span class="sec-tag {sec['tag_class']}">{sec['tag']}</span>
          </header>
          <div class="legal-card-body">
            {sec['html']}
          </div>
        </section>''')
        
    sections_rendered = "\n".join(cards_html)
    
    all_docs_html.append(f'''
    <article class="legal-panel {active_class}" id="panel-{doc['id']}" role="tabpanel" style="display: {display_style};">
      <div class="doc-header-banner">
        <div class="doc-header-top">
          <span class="doc-badge"><i class="fa-solid fa-satellite"></i> OFFICIAL GOVERNANCE DOCUMENT</span>
          <span class="doc-version-badge"><i class="fa-solid fa-code-commit"></i> Version 2.4</span>
        </div>
        <h2>{html.escape(doc['title'])}</h2>
        <p class="doc-lead">{html.escape(doc['subtitle'])}</p>
        
        <div class="doc-meta-strip">
          <span class="doc-meta-pill"><i class="fa-regular fa-calendar-check"></i> Last Updated: 15 September 2026</span>
          <span class="doc-meta-pill"><i class="fa-solid fa-building-shield"></i> Operated by ANTELLAY Labs</span>
          <span class="doc-meta-pill"><i class="fa-solid fa-scale-balanced"></i> Law of India &bull; Jaipur Jurisdiction</span>
        </div>
      </div>

      <!-- Executive Highlights Grid -->
      <div class="exec-summary-wrap">
        <div class="exec-header">
          <h4><i class="fa-solid fa-bolt"></i> Key Highlights at a Glance</h4>
          <span class="exec-note">Executive summary of core principles</span>
        </div>
        <div class="exec-grid">
          {summary_grid}
        </div>
      </div>

      <!-- Table of Contents Navigator -->
      <div class="doc-toc-wrapper">
        <div class="toc-header">
          <i class="fa-solid fa-list-ol"></i> In-Document Navigator ({len(sections)} Sections)
        </div>
        <div class="toc-chips-scroll">
          {toc_bar_html}
        </div>
      </div>

      {intro_html}

      <div class="doc-sections-container">
        {sections_rendered}
      </div>
    </article>''')

tabs_combined = "\n".join(all_tabs_html)
docs_combined = "\n".join(all_docs_html)

legal_page_complete = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Legal & Compliance Center | ANTELLAY Space</title>
  <meta name="description" content="Official Legal Terms, Privacy Policy, SpaceOS Disclaimers, API Terms, Security, and Compliance Policies for ANTELLAY Space operated by ANTELLAY Labs.">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" href="/favicon.png">
  <link rel="shortcut icon" href="/favicon.ico">
  <link rel="apple-touch-icon" href="/favicon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="css/style.css">
  <style>
    :root {{
      --legal-bg: #030712;
      --legal-card-bg: rgba(11, 19, 36, 0.72);
      --legal-card-border: rgba(148, 163, 184, 0.12);
      --legal-card-border-hover: rgba(232, 106, 40, 0.35);
      --legal-accent: #E86A28;
      --legal-accent-bright: #FF7A29;
      --legal-accent-glow: rgba(232, 106, 40, 0.28);
      --legal-text: #F1F5F9;
      --legal-muted: #94A3B8;
      --legal-dim: #525E70;
      --legal-cyan: #00F0FF;
      --legal-green: #00E676;
      --legal-red: #FF3366;
    }}

    body.legal-page {{
      background-color: var(--legal-bg);
      color: var(--legal-text);
      font-family: 'Inter', sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    /* Reading Progress Line */
    #reading-progress {{
      position: fixed;
      top: 0;
      left: 0;
      height: 3px;
      background: linear-gradient(90deg, #E86A28, #FF7A29, #00F0FF);
      z-index: 9999;
      width: 0%;
      transition: width 0.1s ease;
    }}

    /* Legal Hero */
    .legal-hero {{
      position: relative;
      padding: 130px 24px 45px;
      text-align: center;
      background: radial-gradient(circle at 50% 15%, rgba(232, 106, 40, 0.14) 0%, transparent 65%);
      border-bottom: 1px solid var(--legal-card-border);
      overflow: hidden;
    }}

    .legal-hero-inner {{
      max-width: 900px;
      margin: 0 auto;
      position: relative;
      z-index: 2;
    }}

    .legal-kicker {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 20px;
      background: rgba(232, 106, 40, 0.12);
      border: 1px solid rgba(232, 106, 40, 0.35);
      color: var(--legal-accent-bright);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-bottom: 18px;
    }}

    .legal-hero h1 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: clamp(28px, 4.5vw, 44px);
      font-weight: 700;
      letter-spacing: 0.5px;
      margin: 0 0 16px;
      color: #FFFFFF;
    }}

    .legal-hero h1 span {{
      color: var(--legal-accent-bright);
    }}

    .legal-hero p {{
      color: var(--legal-muted);
      font-size: 15px;
      line-height: 1.65;
      margin: 0 auto 26px;
      max-width: 660px;
    }}

    .legal-actions-bar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      align-items: center;
      gap: 12px;
      margin-top: 10px;
    }}

    .legal-action-btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 9px 18px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-decoration: none;
      letter-spacing: 0.4px;
      transition: all 0.25s ease;
      cursor: pointer;
    }}

    .legal-action-btn.primary {{
      background: var(--legal-accent);
      color: #FFFFFF;
      border: 1px solid var(--legal-accent-bright);
      box-shadow: 0 0 20px var(--legal-accent-glow);
    }}

    .legal-action-btn.primary:hover {{
      background: var(--legal-accent-bright);
      transform: translateY(-1px);
      box-shadow: 0 0 25px rgba(255, 122, 41, 0.45);
    }}

    .legal-action-btn.secondary {{
      background: rgba(15, 23, 42, 0.7);
      color: #E2E8F0;
      border: 1px solid var(--legal-card-border);
    }}

    .legal-action-btn.secondary:hover {{
      background: rgba(30, 41, 59, 0.9);
      border-color: rgba(255, 255, 255, 0.25);
      color: #FFFFFF;
    }}

    .legal-search-box {{
      max-width: 500px;
      margin: 22px auto 0;
      position: relative;
    }}

    .legal-search-box input {{
      width: 100%;
      background: rgba(10, 16, 28, 0.85);
      border: 1px solid var(--legal-card-border);
      border-radius: 8px;
      padding: 12px 16px 12px 42px;
      color: #FFFFFF;
      font-size: 13px;
      outline: none;
      transition: all 0.25s ease;
      box-sizing: border-box;
    }}

    .legal-search-box input:focus {{
      border-color: var(--legal-accent-bright);
      box-shadow: 0 0 15px var(--legal-accent-glow);
      background: rgba(15, 23, 42, 0.95);
    }}

    .legal-search-box i {{
      position: absolute;
      left: 15px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--legal-muted);
      font-size: 14px;
    }}

    /* Main Container */
    .legal-shell {{
      max-width: 1320px;
      margin: 0 auto;
      padding: 36px 24px 80px;
      display: grid;
      grid-template-columns: 310px 1fr;
      gap: 32px;
      position: relative;
      flex: 1;
    }}

    @media (max-width: 990px) {{
      .legal-shell {{
        grid-template-columns: 1fr;
        padding-top: 20px;
      }}
    }}

    /* Sidebar Navigation */
    .legal-sidebar {{
      position: sticky;
      top: 90px;
      max-height: calc(100vh - 110px);
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 5px;
      background: rgba(8, 14, 26, 0.8);
      border: 1px solid var(--legal-card-border);
      border-radius: 12px;
      padding: 14px;
      backdrop-filter: blur(14px);
    }}

    .legal-sidebar::-webkit-scrollbar {{
      width: 4px;
    }}
    .legal-sidebar::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.15);
      border-radius: 4px;
    }}

    .legal-sidebar-header {{
      padding: 6px 10px 12px;
      border-bottom: 1px solid var(--legal-card-border);
      margin-bottom: 6px;
    }}

    .legal-sidebar-header h3 {{
      margin: 0 0 4px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: #FFFFFF;
    }}

    .legal-sidebar-header p {{
      margin: 0;
      font-size: 11px;
      color: var(--legal-muted);
    }}

    .policy-tab-btn {{
      display: flex;
      align-items: center;
      gap: 12px;
      width: 100%;
      padding: 10px 12px;
      border-radius: 8px;
      background: transparent;
      border: 1px solid transparent;
      color: #94A3B8;
      text-align: left;
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: inherit;
    }}

    .policy-tab-btn:hover {{
      background: rgba(255, 255, 255, 0.04);
      color: #FFFFFF;
      border-color: rgba(255, 255, 255, 0.08);
    }}

    .policy-tab-btn.active {{
      background: rgba(232, 106, 40, 0.14);
      border-color: rgba(232, 106, 40, 0.4);
      color: #FFFFFF;
      box-shadow: 0 0 16px rgba(232, 106, 40, 0.2);
    }}

    .tab-icon {{
      width: 30px;
      height: 30px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.05);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      color: var(--legal-accent-bright);
      flex-shrink: 0;
    }}

    .policy-tab-btn.active .tab-icon {{
      background: var(--legal-accent);
      color: #FFFFFF;
    }}

    .tab-text {{
      flex: 1;
      min-width: 0;
    }}

    .tab-title {{
      display: block;
      font-size: 12px;
      font-weight: 600;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .tab-sub {{
      display: block;
      font-size: 10px;
      color: var(--legal-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .tab-arrow {{
      font-size: 10px;
      opacity: 0;
      transition: opacity 0.2s ease;
    }}

    .policy-tab-btn.active .tab-arrow {{
      opacity: 1;
      color: var(--legal-accent-bright);
    }}

    /* Main Panels Container */
    .legal-content-container {{
      min-width: 0;
    }}

    .legal-panel {{
      display: none;
      animation: fadeInPanel 0.25s ease-out;
    }}

    .legal-panel.active {{
      display: block;
    }}

    @keyframes fadeInPanel {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Document Header Banner */
    .doc-header-banner {{
      background: linear-gradient(180deg, rgba(17, 28, 52, 0.6) 0%, rgba(9, 15, 28, 0.8) 100%);
      border: 1px solid var(--legal-card-border);
      border-radius: 14px;
      padding: 30px 32px;
      margin-bottom: 24px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }}

    .doc-header-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 12px;
    }}

    .doc-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 700;
      color: var(--legal-accent-bright);
      background: rgba(232, 106, 40, 0.12);
      border: 1px solid rgba(232, 106, 40, 0.35);
      padding: 4px 10px;
      border-radius: 4px;
      letter-spacing: 1px;
    }}

    .doc-version-badge {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--legal-muted);
      background: rgba(255, 255, 255, 0.05);
      padding: 3px 8px;
      border-radius: 4px;
      border: 1px solid var(--legal-card-border);
    }}

    .doc-header-banner h2 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: clamp(24px, 3.2vw, 34px);
      font-weight: 700;
      color: #FFFFFF;
      margin: 0 0 8px;
    }}

    .doc-lead {{
      font-size: 15px;
      color: var(--legal-muted);
      line-height: 1.6;
      margin: 0 0 20px;
    }}

    .doc-meta-strip {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      padding-top: 16px;
      border-top: 1px solid var(--legal-card-border);
    }}

    .doc-meta-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      color: #CBD5E1;
      background: rgba(255, 255, 255, 0.03);
      padding: 4px 10px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.06);
    }}

    .doc-meta-pill i {{
      color: var(--legal-accent-bright);
    }}

    /* Executive Highlights Grid */
    .exec-summary-wrap {{
      background: rgba(10, 17, 30, 0.85);
      border: 1px solid rgba(232, 106, 40, 0.25);
      border-radius: 12px;
      padding: 22px 26px;
      margin-bottom: 24px;
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35);
    }}

    .exec-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--legal-card-border);
    }}

    .exec-header h4 {{
      margin: 0;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.8px;
      color: #FFFFFF;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .exec-header h4 i {{
      color: var(--legal-accent-bright);
    }}

    .exec-note {{
      font-size: 11px;
      color: var(--legal-muted);
    }}

    .exec-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
    }}

    .exec-card {{
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid rgba(148, 163, 184, 0.1);
      border-radius: 8px;
      padding: 14px;
      display: flex;
      gap: 12px;
      transition: border-color 0.2s ease, transform 0.2s ease;
    }}

    .exec-card:hover {{
      border-color: rgba(232, 106, 40, 0.4);
      transform: translateY(-2px);
    }}

    .exec-card-icon {{
      width: 32px;
      height: 32px;
      border-radius: 6px;
      background: rgba(232, 106, 40, 0.12);
      border: 1px solid rgba(232, 106, 40, 0.25);
      color: var(--legal-accent-bright);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      flex-shrink: 0;
    }}

    .exec-card-content h5 {{
      margin: 0 0 4px;
      font-size: 12px;
      font-weight: 600;
      color: #FFFFFF;
    }}

    .exec-card-content p {{
      margin: 0;
      font-size: 11px;
      line-height: 1.5;
      color: var(--legal-muted);
    }}

    /* Table of Contents Navigator */
    .doc-toc-wrapper {{
      background: rgba(8, 14, 25, 0.7);
      border: 1px solid var(--legal-card-border);
      border-radius: 10px;
      padding: 14px 18px;
      margin-bottom: 26px;
    }}

    .toc-header {{
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.8px;
      color: var(--legal-muted);
      text-transform: uppercase;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .toc-chips-scroll {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      max-height: 110px;
      overflow-y: auto;
      padding-right: 4px;
    }}

    .toc-chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 9px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.07);
      color: #94A3B8;
      font-size: 11px;
      text-decoration: none;
      transition: all 0.2s ease;
      white-space: nowrap;
    }}

    .toc-chip:hover {{
      background: rgba(232, 106, 40, 0.15);
      border-color: rgba(232, 106, 40, 0.4);
      color: #FFFFFF;
    }}

    .chip-num {{
      font-family: 'JetBrains Mono', monospace;
      color: var(--legal-accent-bright);
      font-weight: 600;
      font-size: 10px;
    }}

    /* Legal Intro Banner */
    .legal-intro-banner {{
      display: flex;
      align-items: flex-start;
      gap: 14px;
      padding: 16px 20px;
      border-radius: 8px;
      background: rgba(0, 240, 255, 0.05);
      border-left: 3px solid var(--legal-cyan);
      margin-bottom: 24px;
    }}

    .legal-intro-banner i {{
      color: var(--legal-cyan);
      font-size: 18px;
      margin-top: 2px;
      flex-shrink: 0;
    }}

    .legal-intro-banner p {{
      margin: 0;
      font-size: 13px;
      line-height: 1.6;
      color: #E2E8F0;
    }}

    /* Section Cards */
    .doc-sections-container {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}

    .legal-card {{
      background: var(--legal-card-bg);
      border: 1px solid var(--legal-card-border);
      border-radius: 12px;
      overflow: hidden;
      transition: border-color 0.25s ease, box-shadow 0.25s ease;
      scroll-margin-top: 100px;
    }}

    .legal-card:hover {{
      border-color: var(--legal-card-border-hover);
      box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4);
    }}

    .legal-card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      padding: 16px 22px;
      background: rgba(15, 23, 42, 0.4);
      border-bottom: 1px solid var(--legal-card-border);
    }}

    .header-left {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .sec-badge {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 28px;
      height: 28px;
      border-radius: 6px;
      background: rgba(232, 106, 40, 0.15);
      border: 1px solid rgba(232, 106, 40, 0.35);
      color: var(--legal-accent-bright);
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      flex-shrink: 0;
    }}

    .card-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 16px;
      font-weight: 700;
      color: #FFFFFF;
      margin: 0;
      letter-spacing: 0.3px;
    }}

    .sec-tag {{
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 4px;
      letter-spacing: 0.6px;
      text-transform: uppercase;
    }}

    .sec-tag.tag-neutral {{
      background: rgba(255, 255, 255, 0.05);
      color: var(--legal-muted);
      border: 1px solid var(--legal-card-border);
    }}

    .sec-tag.tag-success {{
      background: rgba(0, 230, 118, 0.12);
      color: var(--legal-green);
      border: 1px solid rgba(0, 230, 118, 0.3);
    }}

    .sec-tag.tag-warning {{
      background: rgba(255, 193, 7, 0.12);
      color: #FFC107;
      border: 1px solid rgba(255, 193, 7, 0.3);
    }}

    .sec-tag.tag-danger {{
      background: rgba(255, 51, 102, 0.12);
      color: var(--legal-red);
      border: 1px solid rgba(255, 51, 102, 0.3);
    }}

    .sec-tag.tag-info {{
      background: rgba(0, 240, 255, 0.1);
      color: var(--legal-cyan);
      border: 1px solid rgba(0, 240, 255, 0.25);
    }}

    .sec-tag.tag-legal {{
      background: rgba(168, 85, 247, 0.12);
      color: #C084FC;
      border: 1px solid rgba(168, 85, 247, 0.3);
    }}

    .sec-tag.tag-ai {{
      background: rgba(232, 106, 40, 0.15);
      color: var(--legal-accent-bright);
      border: 1px solid rgba(232, 106, 40, 0.35);
    }}

    .sec-tag.tag-ip {{
      background: rgba(59, 130, 246, 0.12);
      color: #60A5FA;
      border: 1px solid rgba(59, 130, 246, 0.3);
    }}

    .sec-tag.tag-contact {{
      background: rgba(16, 185, 129, 0.12);
      color: #34D399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    .legal-card-body {{
      padding: 22px 24px;
      font-size: 14px;
      line-height: 1.75;
      color: #CBD5E1;
    }}

    .legal-card-body p {{
      margin: 0 0 14px;
    }}

    .legal-card-body p:last-child {{
      margin-bottom: 0;
    }}

    .list-lead {{
      color: #FFFFFF;
      font-weight: 500;
      margin-bottom: 10px !important;
    }}

    .subsec-heading {{
      font-size: 14px;
      font-weight: 600;
      color: #FFFFFF;
      margin: 20px 0 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .subsec-num {{
      color: var(--legal-accent-bright);
      font-family: 'JetBrains Mono', monospace;
    }}

    /* Clean Styled List */
    .legal-list {{
      list-style-type: none;
      margin: 10px 0 18px;
      padding: 0;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .legal-list li {{
      display: flex;
      align-items: baseline;
      gap: 10px;
      line-height: 1.6;
      background: rgba(255, 255, 255, 0.02);
      padding: 8px 12px;
      border-radius: 6px;
      border-left: 2px solid rgba(232, 106, 40, 0.4);
    }}

    .bullet-dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--legal-accent-bright);
      flex-shrink: 0;
      position: relative;
      top: -2px;
    }}

    /* Contact Card in Policy */
    .legal-contact-card {{
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(232, 106, 40, 0.3);
      border-radius: 10px;
      padding: 18px 20px;
      margin-top: 14px;
    }}

    .contact-entity {{
      font-size: 14px;
      color: #FFFFFF;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .contact-entity i {{
      color: var(--legal-accent-bright);
    }}

    .contact-location {{
      font-size: 12px;
      color: var(--legal-muted);
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .contact-grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .contact-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 6px;
      background: rgba(232, 106, 40, 0.12);
      border: 1px solid rgba(232, 106, 40, 0.3);
      color: #FFFFFF;
      font-size: 12px;
      font-weight: 500;
      text-decoration: none;
      transition: all 0.2s ease;
    }}

    .contact-pill:hover {{
      background: var(--legal-accent);
      border-color: var(--legal-accent-bright);
      transform: translateY(-1px);
    }}

    /* Law & Jurisdiction Box */
    .law-jurisdiction-box {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid rgba(148, 163, 184, 0.15);
      border-radius: 8px;
      padding: 12px 16px;
      margin-top: 12px;
    }}

    .jurisdiction-icon {{
      flex-shrink: 0;
    }}

    .law-jurisdiction-box strong {{
      display: block;
      font-size: 13px;
      color: #FFFFFF;
      margin-bottom: 2px;
    }}

    .law-jurisdiction-box p {{
      margin: 0 !important;
      font-size: 12px;
      color: var(--legal-muted);
    }}

    /* Footer Legal Links Styling */
    .footer-legal-bar {{
      width: 100%;
      display: flex;
      justify-content: center;
      margin: 18px 0 8px;
      position: relative;
      z-index: 2;
    }}

    .footer-legal-links {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      align-items: center;
      gap: 8px;
    }}

    .legal-btn {{
      display: inline-flex;
      align-items: center;
      padding: 5px 12px;
      border-radius: 20px;
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid rgba(148, 163, 184, 0.16);
      color: #94A3B8;
      font-size: 11px;
      font-weight: 500;
      text-decoration: none;
      letter-spacing: 0.4px;
      transition: all 0.25s ease;
      backdrop-filter: blur(8px);
    }}

    .legal-btn:hover {{
      color: #FFFFFF;
      background: rgba(232, 106, 40, 0.16);
      border-color: rgba(232, 106, 40, 0.5);
      box-shadow: 0 0 14px rgba(232, 106, 40, 0.25);
      transform: translateY(-1px);
    }}
  </style>
</head>
<body class="legal-page">

  <div id="reading-progress"></div>

  <!-- Header -->
  <header class="site-header">
    <a class="brand" href="index.html">
      <svg class="mark" viewBox="0 0 48 48" aria-hidden="true">
        <path d="M24 4 6 43l18-12 18 12L24 4Z" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>
        <path d="M24 15v16M17 35l7-4 7 4" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
      </svg>
      <span><span class="brand-name">ANTELLAY</span><span class="brand-sub">SPACE</span></span>
    </a>
    <nav class="nav" aria-label="Primary">
      <a href="architecture.html">Architecture</a>
      <a href="thesis.html">Thesis</a>
      <a href="news.html">News</a>
      <a href="product.html">Products</a>
      <a href="about.html">About Us</a>
      <a href="contact.html">Contact Us</a>
    </nav>
    <a class="contact" href="login.html">Login</a>
    <button class="menu-toggle" type="button" aria-label="Toggle navigation" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </header>

  <div class="mobile-menu" id="mobile-menu">
    <a href="architecture.html">Architecture</a>
    <a href="thesis.html">Thesis</a>
    <a href="news.html">News</a>
    <a href="product.html">Products</a>
    <a href="about.html">About Us</a>
    <a href="contact.html">Contact Us</a>
    <a href="login.html">Login</a>
  </div>

  <main>
    <!-- Hero -->
    <section class="legal-hero">
      <div class="legal-hero-inner">
        <div class="legal-kicker"><i class="fa-solid fa-scale-balanced"></i> Governance &amp; Compliance</div>
        <h1>Legal &amp; Regulatory <span>Framework</span></h1>
        <p>Comprehensive operational standards, terms of service, privacy practices, and compliance protocols governing the ANTELLAY Space technology platform and space economy operations.</p>
        
        <div class="legal-actions-bar">
          <button onclick="window.print()" class="legal-action-btn secondary">
            <i class="fa-solid fa-print"></i> Print Document
          </button>
          <a href="contact.html" class="legal-action-btn secondary">
            <i class="fa-solid fa-envelope"></i> Contact Legal Team
          </a>
        </div>

        <div class="legal-search-box">
          <i class="fa-solid fa-magnifying-glass"></i>
          <input type="text" id="legal-search" placeholder="Search clauses, terms, or policy keywords...">
        </div>
      </div>
    </section>

    <!-- Shell with Sidebar & Content -->
    <div class="legal-shell">
      <!-- Sidebar -->
      <aside class="legal-sidebar" role="tablist">
        <div class="legal-sidebar-header">
          <h3>Documentation Hub</h3>
          <p>Select a policy to review</p>
        </div>
        {tabs_combined}
      </aside>

      <!-- Main Panels -->
      <div class="legal-content-container">
        {docs_combined}
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer class="page" id="contact">
    <video class="footer-video" autoplay muted loop playsinline disablepictureinpicture src="assets/videos/WhatsApp Video 2026-08-11 at 12.12.58 PM.mp4"></video>
    <div class="footer-top">
      <div class="footer-center">
        <a class="brand" href="index.html">
          <svg class="mark" viewBox="0 0 48 48" aria-hidden="true"><path d="M24 4 6 43l18-12 18 12L24 4Z" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/><path d="M24 15v16M17 35l7-4 7 4" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>
          <span><span class="brand-name">ANTELLAY</span><span class="brand-sub">SPACE</span></span>
        </a>
        <div class="socials">
          <a href="https://www.linkedin.com/company/a-n-t-e-l-l-a-y-space/posts/?feedView=all" target="_blank" aria-label="LinkedIn">in</a>
          <a href="#" aria-label="Twitter">&#120143;</a>
          <a href="mailto:space.antellay@gmail.com" aria-label="Mail">&#9993;</a>
          <a href="https://www.instagram.com/antellay.tech?igsh=NDBoa3NoMjZ2Ynk3" target="_blank" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
        </div>
      </div>
      <a href="#hero" class="to-top" aria-label="Back to top">&#8593;</a>
    </div>

    <div class="footer-legal-bar">
      <div class="footer-legal-links">
        <a href="legal.html#terms" class="legal-btn">Terms &amp; Conditions</a>
        <a href="legal.html#privacy" class="legal-btn">Privacy Policy</a>
        <a href="legal.html#cookies" class="legal-btn">Cookie Policy</a>
        <a href="legal.html#disclaimer" class="legal-btn">Disclaimer</a>
        <a href="legal.html#ai-spaceos" class="legal-btn">AI &amp; SpaceOS</a>
        <a href="legal.html#security" class="legal-btn">Security</a>
        <a href="legal.html#data-api" class="legal-btn">Data &amp; API</a>
        <a href="legal.html#refunds" class="legal-btn">Refund Policy</a>
      </div>
    </div>

    <div class="copyright">
      &copy; 2026 <a href="https://antellay.in/" target="_blank" rel="noopener noreferrer" class="footer-link">ANTELLAY Labs</a>. All Rights Reserved. A <a href="https://celebso.com/" target="_blank" rel="noopener noreferrer" class="footer-link">Celebso Group</a> Company.
      <span class="india-flag-container">
        <img src="https://flagcdn.com/w40/in.png" srcset="https://flagcdn.com/w80/in.png 2x" width="20" alt="India" style="vertical-align: middle; border-radius: 2px;">
      </span>
    </div>
  </footer>

  <script>
    // Tab switching logic & Hash routing
    const tabs = document.querySelectorAll('.policy-tab-btn');
    const panels = document.querySelectorAll('.legal-panel');

    function activateTab(targetId) {{
      let matched = false;
      tabs.forEach(tab => {{
        const isTarget = tab.getAttribute('data-target') === targetId;
        tab.classList.toggle('active', isTarget);
        tab.setAttribute('aria-selected', isTarget ? 'true' : 'false');
        if (isTarget) matched = true;
      }});

      panels.forEach(panel => {{
        const isTarget = panel.id === `panel-${{targetId}}`;
        panel.classList.toggle('active', isTarget);
        panel.style.display = isTarget ? 'block' : 'none';
      }});

      if (!matched && tabs.length > 0) {{
        tabs[0].classList.add('active');
        tabs[0].setAttribute('aria-selected', 'true');
        panels[0].classList.add('active');
        panels[0].style.display = 'block';
      }}
    }}

    tabs.forEach(tab => {{
      tab.addEventListener('click', () => {{
        const target = tab.getAttribute('data-target');
        window.location.hash = target;
        activateTab(target);
        window.scrollTo({{ top: document.querySelector('.legal-content-container').offsetTop - 80, behavior: 'smooth' }});
      }});
    }});

    // Handle initial hash routing & deep-link scrolling
    function handleHash() {{
      const rawHash = window.location.hash.replace('#', '').trim();
      if (!rawHash) {{
        activateTab('terms');
        return;
      }}

      // Check if hash matches a full tab or a section like "terms-sec-3"
      if (rawHash.includes('-sec-')) {{
        const tabPrefix = rawHash.split('-sec-')[0];
        activateTab(tabPrefix);
        setTimeout(() => {{
          const secEl = document.getElementById(rawHash);
          if (secEl) {{
            secEl.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
          }}
        }}, 100);
      }} else {{
        activateTab(rawHash);
      }}
    }}

    window.addEventListener('hashchange', handleHash);
    window.addEventListener('DOMContentLoaded', handleHash);

    // Reading Progress Indicator
    window.addEventListener('scroll', () => {{
      const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = (winScroll / height) * 100;
      document.getElementById('reading-progress').style.width = scrolled + '%';
    }});

    // Live search within active document
    const searchInput = document.getElementById('legal-search');
    if (searchInput) {{
      searchInput.addEventListener('input', (e) => {{
        const query = e.target.value.toLowerCase().trim();
        const activePanel = document.querySelector('.legal-panel.active');
        if (!activePanel) return;

        const cards = activePanel.querySelectorAll('.legal-card');
        cards.forEach(card => {{
          if (!query) {{
            card.style.display = 'block';
          }} else {{
            const text = card.textContent.toLowerCase();
            card.style.display = text.includes(query) ? 'block' : 'none';
          }}
        }});
      }});
    }}

    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const mobileMenu = document.querySelector('#mobile-menu');
    if (menuToggle && mobileMenu) {{
      menuToggle.addEventListener('click', () => {{
        const isOpen = mobileMenu.classList.toggle('open');
        menuToggle.setAttribute('aria-expanded', String(isOpen));
      }});
      mobileMenu.querySelectorAll('a').forEach(link => {{
        link.addEventListener('click', () => {{
          mobileMenu.classList.remove('open');
          menuToggle.setAttribute('aria-expanded', 'false');
        }});
      }});
    }}
  </script>
</body>
</html>
'''

with open('legal.html', 'w', encoding='utf-8') as f:
    f.write(legal_page_complete)

print("Generated structured legal.html successfully!")
