import pypdf
import re
import html
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

reader = pypdf.PdfReader('Antellay_Terms_Conditions.pdf')

def extract_pages_clean(start_p, end_p):
    pages = []
    for p in range(start_p - 1, end_p):
        txt = reader.pages[p].extract_text(extraction_mode='layout') or ''
        pages.append(txt)
    full = "\n\n".join(pages)
    full = full.replace('\ufffd', '"')
    return full

def clean_bullets(text):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    intro = []
    bullets = []
    current_bullet = []
    
    for l in lines:
        if re.match(r'^[●•\-\*]\s*', l):
            if current_bullet:
                bullets.append(" ".join(current_bullet))
                current_bullet = []
            current_bullet.append(re.sub(r'^[●•\-\*]\s*', '', l))
        elif current_bullet:
            current_bullet.append(l)
        else:
            intro.append(l)
            
    if current_bullet:
        bullets.append(" ".join(current_bullet))
        
    return " ".join(intro).strip(), [b.strip() for b in bullets if b.strip()]

def build_terms_html():
    raw = extract_pages_clean(1, 7)
    # Match numbered sections 1 to 25
    matches = list(re.finditer(r'(\n|^)\s*(\d+)\.\s+([A-Za-z0-9\s&,–\-\(\)\/\']+?)\s*(?=\n)', raw))
    
    cards_html = []
    toc_chips = []
    toc_sidebar = []
    
    for i, m in enumerate(matches):
        sec_num = int(m.group(2))
        sec_title = m.group(3).strip()
        start_idx = m.end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(raw)
        sec_body_raw = raw[start_idx:end_idx].strip()
        
        anchor_id = f"terms-sec-{sec_num}"
        toc_chips.append(f'<a href="#{anchor_id}" class="toc-chip"><span class="chip-num">{sec_num:02d}</span> {html.escape(sec_title)}</a>')
        toc_sidebar.append(f'<a href="#{anchor_id}" class="toc-link"><span class="toc-num">{sec_num:02d}</span> <span>{html.escape(sec_title)}</span></a>')
        
        # Determine specific structure per section
        if sec_num == 1:
            tag_name, tag_class = "PLATFORM SCOPE", "tag-success"
            body = """
            <p class="clause-lead">ANTELLAY Space is a frontier space-technology initiative operated by <strong>ANTELLAY Labs</strong>, developing artificial intelligence, simulation systems, and software infrastructure for the global space economy.</p>
            <div class="highlight-feature-grid">
              <div class="h-card">
                <i class="fa-solid fa-satellite-dish"></i>
                <div class="h-text">
                  <h5>Telemetry & Sourcing</h5>
                  <p>Aggregates satellite, orbital, Earth observation, space-weather, and geospatial data from public catalogs and authorized providers.</p>
                </div>
              </div>
              <div class="h-card">
                <i class="fa-solid fa-microchip"></i>
                <div class="h-text">
                  <h5>SpaceOS Architecture</h5>
                  <p>Proprietary analytical engines, machine-learning models, and orbital visualization software developed by ANTELLAY Labs.</p>
                </div>
              </div>
            </div>
            <div class="callout-box info-box">
              <i class="fa-solid fa-circle-info"></i>
              <div>
                <strong>Non-Ownership of External Satellites</strong>
                <p>ANTELLAY Space does not necessarily own, operate, control, or maintain the physical spacecraft, sensors, ground stations, or external space infrastructure from which telemetry and data originate.</p>
              </div>
            </div>
            """

        elif sec_num == 2:
            tag_name, tag_class = "ACCEPTABLE USE", "tag-warning"
            body = """
            <p class="clause-lead">You agree to access and utilize the ANTELLAY Space Platform strictly within lawful parameters and under the operational boundaries specified below:</p>
            <div class="compare-container">
              <div class="compare-card permitted">
                <div class="compare-card-head">
                  <span class="badge-status perm"><i class="fa-solid fa-circle-check"></i> PERMITTED ACTIVITIES</span>
                  <h4>Authorized Platform Use</h4>
                </div>
                <ul class="structured-bullets perm-bullets">
                  <li><i class="fa-solid fa-check"></i> <span>Exploring satellite telemetry, orbital coordinates, and space domain visualizations.</span></li>
                  <li><i class="fa-solid fa-check"></i> <span>Academic research, scientific inquiry, technological exploration, and education.</span></li>
                  <li><i class="fa-solid fa-check"></i> <span>Evaluating ANTELLAY Space enterprise capabilities and upcoming SpaceOS features.</span></li>
                  <li><i class="fa-solid fa-check"></i> <span>Consuming authorized API feeds within agreed rate limits and quotas.</span></li>
                  <li><i class="fa-solid fa-check"></i> <span>Benchmarking mission parameters and simulation models in accordance with these Terms.</span></li>
                </ul>
              </div>
              <div class="compare-card prohibited">
                <div class="compare-card-head">
                  <span class="badge-status proh"><i class="fa-solid fa-circle-xmark"></i> STRICTLY FORBIDDEN</span>
                  <h4>Prohibited Operations</h4>
                </div>
                <ul class="structured-bullets proh-bullets">
                  <li><i class="fa-solid fa-xmark"></i> <span>Unlawful, malicious, fraudulent, or hazardous operations.</span></li>
                  <li><i class="fa-solid fa-xmark"></i> <span>Attempting unauthorized penetration, brute-force, or infrastructure exploitation.</span></li>
                  <li><i class="fa-solid fa-xmark"></i> <span>Automated scraping, excessive polling, or denial-of-service (DoS) attacks.</span></li>
                  <li><i class="fa-solid fa-xmark"></i> <span>Interfering with, jamming, or spoofing satellite communication or telemetry.</span></li>
                  <li><i class="fa-solid fa-xmark"></i> <span>Reverse engineering, decompiling, or disassembling SpaceOS proprietary algorithms.</span></li>
                  <li><i class="fa-solid fa-xmark"></i> <span>Misrepresenting ANTELLAY Space data, credentials, partnerships, or official capabilities.</span></li>
                </ul>
              </div>
            </div>
            """

        elif sec_num == 3:
            tag_name, tag_class = "DATA GOVERNANCE", "tag-info"
            body = """
            <p class="clause-lead">ANTELLAY Space displays and processes orbital mechanics, Two-Line Element sets (TLEs), satellite positions, space-weather metrics, and Earth observation imagery derived from third-party and public scientific feeds.</p>
            <div class="data-limitations-grid">
              <div class="limitation-item">
                <span class="lim-icon"><i class="fa-solid fa-clock-rotate-left"></i></span>
                <div>
                  <h6>Provider Latency</h6>
                  <p>Orbital data may experience ingestion latency, ground-station propagation delays, and calculation revisions.</p>
                </div>
              </div>
              <div class="limitation-item">
                <span class="lim-icon"><i class="fa-solid fa-arrows-rotate"></i></span>
                <div>
                  <h6>Periodic Recalculations</h6>
                  <p>Orbital perturbations and solar flux require periodic ephemeris recalculations which may cause positional shifts.</p>
                </div>
              </div>
              <div class="limitation-item">
                <span class="lim-icon"><i class="fa-solid fa-triangle-exclamation"></i></span>
                <div>
                  <h6>No Control Implied</h6>
                  <p>Displaying a satellite or object does not imply operational commanding or bilateral communication with that spacecraft.</p>
                </div>
              </div>
            </div>
            """

        elif sec_num == 4:
            tag_name, tag_class = "VERIFICATION", "tag-warning"
            body = """
            <p class="clause-lead">While reasonable engineering efforts are made to deliver reliable analytics, ANTELLAY Space does not warrant that all platform data will be continuous, error-free, or instantaneously updated.</p>
            <div class="callout-box warning-box">
              <i class="fa-solid fa-triangle-exclamation"></i>
              <div>
                <strong>Mandatory Independent Verification</strong>
                <p>Real-time telemetry may change without notice. You must independently cross-verify any mission-critical, scientific, safety, or financial data with primary sources before making operational commitments.</p>
              </div>
            </div>
            """

        elif sec_num == 5:
            tag_name, tag_class = "AI & SPACEOS", "tag-ai"
            body = """
            <p class="clause-lead">The platform integrates predictive models, machine learning algorithms, and synthetic orbital simulations branded as <strong>SpaceOS</strong>.</p>
            <div class="ai-governance-card">
              <div class="ai-gov-header">
                <i class="fa-solid fa-brain"></i>
                <div>
                  <h5>Algorithmic Decision-Support Boundaries</h5>
                  <p>AI outputs are analytical aids and must not replace certified aerospace engineering validation.</p>
                </div>
              </div>
              <ul class="structured-bullets">
                <li><i class="fa-solid fa-angle-right"></i> <span>Predictions and trajectory projections represent mathematical estimates based on historical datasets.</span></li>
                <li><i class="fa-solid fa-angle-right"></i> <span>Human flight controllers and engineers retain full responsibility for all downstream space mission decisions.</span></li>
                <li><i class="fa-solid fa-angle-right"></i> <span>ANTELLAY Space assumes no liability for orbital maneuvers executed on automated model predictions alone.</span></li>
              </ul>
            </div>
            """

        elif sec_num == 6:
            tag_name, tag_class = "MISSION CRITICAL", "tag-danger"
            body = """
            <div class="callout-box critical-box">
              <div class="critical-badge"><i class="fa-solid fa-shield-halved"></i> MISSION-CRITICAL DISCLAIMER</div>
              <h4>No Certified Sole Flight or Emergency System Reliance</h4>
              <p>Unless expressly agreed under a formal, executed enterprise Service Level Agreement (SLA), the ANTELLAY Space platform is <strong>NOT</strong> certified as a primary safety-critical, navigation-critical, defense-critical, aviation-critical, or life-support emergency system.</p>
              <div class="critical-rule">
                <i class="fa-solid fa-ban"></i>
                <p>Do NOT rely solely on this platform for operational decisions where system interruption, latency, or inaccurate data could result in death, personal injury, orbital collisions, spacecraft loss, environmental damage, or severe financial catastrophe.</p>
              </div>
            </div>
            """

        elif sec_num == 8:
            tag_name, tag_class = "INTELLECTUAL PROPERTY", "tag-ip"
            body = """
            <p class="clause-lead">All proprietary assets, source code, UI/UX designs, algorithmic architectures, and branding are protected under international copyright and intellectual property treaties.</p>
            <div class="ip-split-grid">
              <div class="ip-card proprietary">
                <h5><i class="fa-solid fa-copyright"></i> ANTELLAY Labs Ownership</h5>
                <p>The ANTELLAY Space name, logo, SpaceOS engine, orbital calculation code, custom models, documentation, and interface graphics belong exclusively to <strong>ANTELLAY Labs</strong>.</p>
              </div>
              <div class="ip-card thirdparty">
                <h5><i class="fa-solid fa-share-nodes"></i> Third-Party Sourced Data</h5>
                <p>Third-party satellite catalogs, NASA/ESA telemetry, and public ephemeris datasets remain the intellectual property of their respective creators and agencies.</p>
              </div>
            </div>
            """

        elif sec_num == 14:
            tag_name, tag_class = "WARRANTIES", "tag-neutral"
            body = """
            <p class="clause-lead">To the fullest extent permissible under applicable law, the Platform, APIs, and all SpaceOS services are provided on an <strong>"AS IS"</strong> and <strong>"AS AVAILABLE"</strong> basis without warranties of any kind.</p>
            <div class="warranty-exclusions-list">
              <div class="w-item"><i class="fa-solid fa-circle-xmark"></i> <span>No guarantee of uninterrupted or error-free platform uptime.</span></div>
              <div class="w-item"><i class="fa-solid fa-circle-xmark"></i> <span>No warranty regarding complete accuracy or timeliness of third-party satellite feeds.</span></div>
              <div class="w-item"><i class="fa-solid fa-circle-xmark"></i> <span>No implied warranty of merchantability or fitness for a particular commercial mission.</span></div>
              <div class="w-item"><i class="fa-solid fa-circle-xmark"></i> <span>No guarantee that simulation outputs will match unmodeled real-world space anomalies.</span></div>
            </div>
            """

        elif sec_num == 15:
            tag_name, tag_class = "LIABILITY", "tag-danger"
            body = """
            <p class="clause-lead">To the maximum extent permitted by applicable law, ANTELLAY Labs, ANTELLAY Space, and their officers, directors, contractors, and affiliates shall not be liable for:</p>
            <div class="liability-grid">
              <div class="l-card"><i class="fa-solid fa-arrow-trend-down"></i> <strong>Indirect or Consequential Damages</strong><p>Loss of revenue, anticipated profits, mission delays, or commercial goodwill.</p></div>
              <div class="l-card"><i class="fa-solid fa-database"></i> <strong>Telemetry & Data Loss</strong><p>Loss, corruption, or delays in satellite telemetry, sensor records, or orbital predictions.</p></div>
              <div class="l-card"><i class="fa-solid fa-satellite"></i> <strong>Spacecraft Operational Impact</strong><p>Damages arising from user reliance on analytical simulations or AI-generated advisories.</p></div>
            </div>
            """

        elif sec_num == 22:
            tag_name, tag_class = "GOVERNING LAW", "tag-legal"
            body = """
            <div class="jurisdiction-featured-card">
              <div class="j-header">
                <img src="https://flagcdn.com/w40/in.png" alt="India" width="32" height="22" class="flag-img">
                <div>
                  <span class="j-badge">EXCLUSIVE JUDICIAL FORUM</span>
                  <h4>Republic of India &bull; Jaipur Jurisdiction</h4>
                </div>
              </div>
              <div class="j-content">
                <p>These Terms and all matters arising out of or relating to the ANTELLAY Space platform shall be governed by, construed, and enforced in accordance with the <strong>laws of the Republic of India</strong>, without regard to conflict-of-laws principles.</p>
                <div class="j-court-box">
                  <i class="fa-solid fa-landmark"></i>
                  <div>
                    <strong>Exclusive Courts of Jaipur, Rajasthan</strong>
                    <p>Subject to applicable arbitration or mediation agreements, the competent courts located in <strong>Jaipur, Rajasthan, India</strong> shall have exclusive jurisdiction over all disputes.</p>
                  </div>
                </div>
              </div>
            </div>
            """

        elif sec_num == 25:
            tag_name, tag_class = "OFFICIAL CONTACT", "tag-contact"
            body = """
            <div class="official-contact-card">
              <div class="c-head">
                <div class="c-avatar"><i class="fa-solid fa-shield-halved"></i></div>
                <div>
                  <span class="c-sub">LEGAL & REGULATORY DESK</span>
                  <h4>ANTELLAY Space Governance</h4>
                  <p>Operated by <strong>ANTELLAY Labs</strong> &bull; Jaipur, Rajasthan, India</p>
                </div>
              </div>
              <div class="channels-grid">
                <a href="mailto:space@antellay.com" class="c-pill">
                  <i class="fa-solid fa-envelope"></i>
                  <div class="pill-info">
                    <span class="p-title">Official Legal Email</span>
                    <span class="p-val">space@antellay.com</span>
                  </div>
                </a>
                <a href="mailto:space.antellay@gmail.com" class="c-pill">
                  <i class="fa-solid fa-envelope-open-text"></i>
                  <div class="pill-info">
                    <span class="p-title">Direct Inquiries</span>
                    <span class="p-val">space.antellay@gmail.com</span>
                  </div>
                </a>
                <a href="tel:+919784626443" class="c-pill">
                  <i class="fa-solid fa-phone"></i>
                  <div class="pill-info">
                    <span class="p-title">Direct Telephone</span>
                    <span class="p-val">+91 97846 26443</span>
                  </div>
                </a>
              </div>
            </div>
            """

        else:
            # General clean structured parser
            intro_txt, bullets = clean_bullets(sec_body_raw)
            blocks = []
            if intro_txt:
                for p in intro_txt.split('\n\n'):
                    clean_p = re.sub(r'\s+', ' ', p).strip()
                    if clean_p:
                        blocks.append(f'<p class="clause-lead">{html.escape(clean_p)}</p>')
            if bullets:
                list_items = "".join([f'<li><i class="fa-solid fa-angle-right"></i> <span>{html.escape(re.sub(r"[;]+$", "", b))}</span></li>' for b in bullets])
                blocks.append(f'<ul class="structured-bullets default-bullets">{list_items}</ul>')
            body = "\n".join(blocks)
            
            t_lower = sec_title.lower()
            if "intellectual" in t_lower: tag_name, tag_class = "INTELLECTUAL PROPERTY", "tag-ip"
            elif "security" in t_lower: tag_name, tag_class = "SECURITY", "tag-info"
            elif "disclaimer" in t_lower or "financial" in t_lower: tag_name, tag_class = "DISCLAIMER", "tag-warning"
            elif "indemnif" in t_lower: tag_name, tag_class = "INDEMNITY", "tag-danger"
            elif "regulatory" in t_lower or "compliance" in t_lower: tag_name, tag_class = "COMPLIANCE", "tag-legal"
            elif "termination" in t_lower: tag_name, tag_class = "TERMINATION", "tag-neutral"
            elif "changes" in t_lower: tag_name, tag_class = "POLICY UPDATES", "tag-neutral"
            else: tag_name, tag_class = "OPERATIONAL STANDARD", "tag-neutral"

        cards_html.append(f"""
        <section class="legal-card" id="{anchor_id}">
          <header class="legal-card-header">
            <div class="header-left">
              <span class="sec-badge">{sec_num:02d}</span>
              <h3 class="card-title">{html.escape(sec_title)}</h3>
            </div>
            <div class="header-right">
              <span class="sec-tag {tag_class}">{tag_name}</span>
              <button class="copy-anchor-btn" onclick="copyClauseLink('{anchor_id}')" title="Copy link to clause">
                <i class="fa-regular fa-copy"></i>
              </button>
            </div>
          </header>
          <div class="legal-card-body">
            {body}
          </div>
        </section>
        """)
        
    return "\n".join(toc_chips), "\n".join(toc_sidebar), "\n".join(cards_html)


def build_privacy_html():
    raw = extract_pages_clean(8, 14)
    matches = list(re.finditer(r'(\n|^)\s*(\d+)\.\s+([A-Za-z0-9\s&,–\-\(\)\/\']+?)\s*(?=\n)', raw))
    
    cards_html = []
    toc_chips = []
    toc_sidebar = []
    
    for i, m in enumerate(matches):
        sec_num = int(m.group(2))
        sec_title = m.group(3).strip()
        start_idx = m.end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(raw)
        sec_body_raw = raw[start_idx:end_idx].strip()
        
        anchor_id = f"privacy-sec-{sec_num}"
        toc_chips.append(f'<a href="#{anchor_id}" class="toc-chip"><span class="chip-num">{sec_num:02d}</span> {html.escape(sec_title)}</a>')
        toc_sidebar.append(f'<a href="#{anchor_id}" class="toc-link"><span class="toc-num">{sec_num:02d}</span> <span>{html.escape(sec_title)}</span></a>')
        
        if sec_num == 1:
            tag_name, tag_class = "PRIVACY SCOPE", "tag-success"
            body = """
            <p class="clause-lead">ANTELLAY Space, operated by <strong>ANTELLAY Labs</strong> ("we", "us", or "our"), is committed to safeguarding the privacy and personal data of every visitor, researcher, aerospace partner, and organization interacting with our platform.</p>
            <div class="scope-pillars-grid">
              <div class="pillar-card">
                <i class="fa-solid fa-user-shield"></i>
                <h6>Zero Data Brokerage</h6>
                <p>We never sell, rent, monetize, or trade your personal data to advertising networks or third-party brokers.</p>
              </div>
              <div class="pillar-card">
                <i class="fa-solid fa-lock"></i>
                <h6>Defense-Grade Encryption</h6>
                <p>Encrypted transmission (TLS 1.3), hashed tokens, and strict role-based access governance.</p>
              </div>
              <div class="pillar-card">
                <i class="fa-solid fa-scale-balanced"></i>
                <h6>DPDP & Global Standards</h6>
                <p>Structured to adhere to India's Digital Personal Data Protection (DPDP) Act and global privacy principles.</p>
              </div>
            </div>
            """

        elif sec_num == 2:
            tag_name, tag_class = "USER DATA", "tag-info"
            body = """
            <p class="clause-lead">Depending on your interactions with ANTELLAY Space, we may collect information you voluntarily provide across our communication channels and platform interfaces:</p>
            <div class="data-types-grid">
              <div class="dtype-card"><i class="fa-solid fa-id-card"></i> <strong>Full Name & Identity</strong><span>For formal communication and account provisioning.</span></div>
              <div class="dtype-card"><i class="fa-solid fa-envelope"></i> <strong>Work Email Address</strong><span>For responses, technical alerts, and security notifications.</span></div>
              <div class="dtype-card"><i class="fa-solid fa-phone"></i> <strong>Contact Phone</strong><span>For priority aerospace coordination and verification.</span></div>
              <div class="dtype-card"><i class="fa-solid fa-building"></i> <strong>Organization / Entity</strong><span>Aerospace agency, research university, or commercial entity name.</span></div>
              <div class="dtype-card"><i class="fa-solid fa-user-tie"></i> <strong>Professional Role</strong><span>Mission controller, aerospace engineer, researcher, or executive.</span></div>
              <div class="dtype-card"><i class="fa-solid fa-message"></i> <strong>Inquiry Content</strong><span>Information and telemetry questions contained in your submitted messages.</span></div>
            </div>
            <div class="callout-box warning-box" style="margin-top: 18px;">
              <i class="fa-solid fa-shield-cat"></i>
              <div>
                <strong>STRICT NOTICE: No Classified or Secret Data</strong>
                <p>Please do NOT submit classified, defense-restricted, proprietary flight keys, or confidential state secrets through public forms. All defense and classified space missions require dedicated, encrypted physical channels.</p>
              </div>
            </div>
            """

        elif sec_num == 3:
            tag_name, tag_class = "TECHNICAL TELEMETRY", "tag-info"
            body = """
            <p class="clause-lead">When you access our website or SpaceOS interfaces, certain technical telemetry is automatically collected by our security, hosting, and diagnostic providers:</p>
            <div class="telemetry-table-wrapper">
              <table class="styled-legal-table">
                <thead>
                  <tr>
                    <th>Data Category</th>
                    <th>Collected Attributes</th>
                    <th>Operational Purpose</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong><i class="fa-solid fa-network-wired"></i> Network Identifiers</strong></td>
                    <td>IP Address, Approximate Geolocation, Port Numbers</td>
                    <td>DDoS protection, rate limiting, and regional load-balancing.</td>
                  </tr>
                  <tr>
                    <td><strong><i class="fa-solid fa-laptop-code"></i> Client Architecture</strong></td>
                    <td>Browser Type, Version, Operating System, Screen Res</td>
                    <td>Optimizing WebGL / 3D orbital canvas rendering.</td>
                  </tr>
                  <tr>
                    <td><strong><i class="fa-solid fa-clock"></i> Access Records</strong></td>
                    <td>Timestamps, Pages Visited, Session Duration, Referrer</td>
                    <td>System performance diagnostics and bottleneck resolution.</td>
                  </tr>
                  <tr>
                    <td><strong><i class="fa-solid fa-bug"></i> Error Diagnostics</strong></td>
                    <td>HTTP status codes, WebGL shader crash logs, JS errors</td>
                    <td>Platform stability and mission interface debugging.</td>
                  </tr>
                </tbody>
              </table>
            </div>
            """

        elif sec_num == 4:
            tag_name, tag_class = "COOKIES", "tag-neutral"
            body = """
            <p class="clause-lead">ANTELLAY Space utilizes cookies, web storage (localStorage), and session tokens essential for platform operation and telemetry preferences:</p>
            <div class="cookie-types-grid">
              <div class="c-type-card essential">
                <span class="c-badge">STRICTLY NECESSARY</span>
                <h5>Essential Authentication</h5>
                <p>Maintains secure authentication sessions, CSRF token validation, and API gateway access control.</p>
              </div>
              <div class="c-type-card functional">
                <span class="c-badge">FUNCTIONAL</span>
                <h5>User Interface Preferences</h5>
                <p>Saves visual theme settings (Dark/Light), 3D orbital viewpoint presets, and telemetry unit choices.</p>
              </div>
              <div class="c-type-card analytics">
                <span class="c-badge">DIAGNOSTIC</span>
                <h5>Aggregated Performance</h5>
                <p>Measures aggregate API response latency and canvas frame rates to detect infrastructure lag.</p>
              </div>
            </div>
            """

        elif sec_num == 6:
            tag_name, tag_class = "SPACE DATA", "tag-success"
            body = """
            <div class="callout-box success-box">
              <div class="success-badge"><i class="fa-solid fa-satellite"></i> SPACE DATA DELIMITATION</div>
              <h4>Orbital Telemetry Does Not Constitute Personal Information</h4>
              <p>ANTELLAY Space displays satellite positions, TLEs, solar weather readings, geomagnetic metrics, and Earth observation imagery. <strong>Such space-related telemetry does not constitute personal data</strong> because it pertains solely to physical celestial objects and public spacecraft rather than identifiable human individuals.</p>
            </div>
            """

        elif sec_num == 8:
            tag_name, tag_class = "ZERO DATA SALE", "tag-success"
            body = """
            <div class="shield-guarantee-card">
              <div class="s-icon"><i class="fa-solid fa-shield-halved"></i></div>
              <div class="s-text">
                <h4>Ironclad Commitment: We Never Sell Your Data</h4>
                <p>ANTELLAY Space and ANTELLAY Labs do not sell, rent, or trade your personal or institutional information to data brokers, ad exchanges, or marketing affiliates.</p>
              </div>
            </div>
            <p class="clause-lead" style="margin-top: 18px;">Information is shared solely with strictly vetted infrastructure providers necessary to operate the platform:</p>
            <ul class="structured-bullets">
              <li><i class="fa-solid fa-check"></i> <strong>Cloud Hosting & Compute:</strong> Vetted cloud infrastructure providers (AWS, Google Cloud) under stringent data protection agreements.</li>
              <li><i class="fa-solid fa-check"></i> <strong>Security & DDoS Defense:</strong> Web application firewall and traffic scrubbing networks.</li>
              <li><i class="fa-solid fa-check"></i> <strong>Statutory Compliance:</strong> Government authorities or regulatory bodies only when compelled by valid, lawful legal process.</li>
            </ul>
            """

        elif sec_num == 10:
            tag_name, tag_class = "DATA SECURITY", "tag-info"
            body = """
            <p class="clause-lead">We deploy multi-layered defense-in-depth technical, administrative, and organizational safeguards to protect data integrity:</p>
            <div class="security-pillars-grid">
              <div class="sec-pillar">
                <i class="fa-solid fa-lock"></i>
                <h6>TLS 1.3 Encryption</h6>
                <p>All in-flight traffic is encrypted using modern cryptographic cipher suites.</p>
              </div>
              <div class="sec-pillar">
                <i class="fa-solid fa-key"></i>
                <h6>Tokenized Access</h6>
                <p>Least-privilege role-based access control (RBAC) across all administrative APIs.</p>
              </div>
              <div class="sec-pillar">
                <i class="fa-solid fa-shield-virus"></i>
                <h6>Vulnerability Auditing</h6>
                <p>Continuous dependency scanning and infrastructure security monitoring.</p>
              </div>
            </div>
            """

        elif sec_num == 12:
            tag_name, tag_class = "YOUR RIGHTS", "tag-success"
            body = """
            <p class="clause-lead">In accordance with applicable privacy laws and DPDP principles, you maintain full authority over your personal information:</p>
            <div class="rights-action-grid">
              <div class="r-card">
                <span class="r-num">01</span>
                <h5>Right of Access</h5>
                <p>Request an itemized copy of the personal information we hold regarding your account or inquiries.</p>
              </div>
              <div class="r-card">
                <span class="r-num">02</span>
                <h5>Right to Rectification</h5>
                <p>Request correction or updating of any inaccurate, incomplete, or outdated personal records.</p>
              </div>
              <div class="r-card">
                <span class="r-num">03</span>
                <h5>Right to Erasure</h5>
                <p>Request permanent deletion of your personal contact records, subject to legal retention obligations.</p>
              </div>
              <div class="r-card">
                <span class="r-num">04</span>
                <h5>Withdrawal of Consent</h5>
                <p>Revoke your prior consent for communication or non-essential telemetry processing anytime.</p>
              </div>
              <div class="r-card">
                <span class="r-num">05</span>
                <h5>Data Portability</h5>
                <p>Obtain your voluntary inquiry data in a structured, commonly used, machine-readable format.</p>
              </div>
              <div class="r-card">
                <span class="r-num">06</span>
                <h5>Grievance Redressal</h5>
                <p>Lodge a formal privacy inquiry or complaint directly with our designated Privacy Office in Jaipur.</p>
              </div>
            </div>
            """

        elif sec_num == 18:
            tag_name, tag_class = "GRIEVANCE DESK", "tag-contact"
            body = """
            <div class="official-contact-card privacy-desk">
              <div class="c-head">
                <div class="c-avatar"><i class="fa-solid fa-user-lock"></i></div>
                <div>
                  <span class="c-sub">DATA PROTECTION & GRIEVANCE OFFICER</span>
                  <h4>ANTELLAY Space Privacy Office</h4>
                  <p>Operated by <strong>ANTELLAY Labs</strong> &bull; Jaipur, Rajasthan, India</p>
                </div>
              </div>
              <div class="channels-grid">
                <a href="mailto:space@antellay.com" class="c-pill">
                  <i class="fa-solid fa-envelope"></i>
                  <div class="pill-info">
                    <span class="p-title">Data Protection Desk</span>
                    <span class="p-val">space@antellay.com</span>
                  </div>
                </a>
                <a href="mailto:space.antellay@gmail.com" class="c-pill">
                  <i class="fa-solid fa-envelope-open-text"></i>
                  <div class="pill-info">
                    <span class="p-title">Privacy Inquiries</span>
                    <span class="p-val">space.antellay@gmail.com</span>
                  </div>
                </a>
                <a href="tel:+919784626443" class="c-pill">
                  <i class="fa-solid fa-phone"></i>
                  <div class="pill-info">
                    <span class="p-title">Grievance Telephone</span>
                    <span class="p-val">+91 97846 26443</span>
                  </div>
                </a>
              </div>
            </div>
            """

        else:
            intro_txt, bullets = clean_bullets(sec_body_raw)
            blocks = []
            if intro_txt:
                for p in intro_txt.split('\n\n'):
                    clean_p = re.sub(r'\s+', ' ', p).strip()
                    if clean_p:
                        blocks.append(f'<p class="clause-lead">{html.escape(clean_p)}</p>')
            if bullets:
                list_items = "".join([f'<li><i class="fa-solid fa-angle-right"></i> <span>{html.escape(re.sub(r"[;]+$", "", b))}</span></li>' for b in bullets])
                blocks.append(f'<ul class="structured-bullets default-bullets">{list_items}</ul>')
            body = "\n".join(blocks)
            
            t_lower = sec_title.lower()
            if "retention" in t_lower: tag_name, tag_class = "RETENTION", "tag-neutral"
            elif "children" in t_lower: tag_name, tag_class = "CHILDREN PRIVACY", "tag-warning"
            elif "transfer" in t_lower: tag_name, tag_class = "TRANSFERS", "tag-info"
            elif "compliance" in t_lower: tag_name, tag_class = "LEGAL COMPLIANCE", "tag-legal"
            elif "changes" in t_lower: tag_name, tag_class = "POLICY UPDATES", "tag-neutral"
            else: tag_name, tag_class = "PRIVACY CLAUSE", "tag-neutral"

        cards_html.append(f"""
        <section class="legal-card" id="{anchor_id}">
          <header class="legal-card-header">
            <div class="header-left">
              <span class="sec-badge">{sec_num:02d}</span>
              <h3 class="card-title">{html.escape(sec_title)}</h3>
            </div>
            <div class="header-right">
              <span class="sec-tag {tag_class}">{tag_name}</span>
              <button class="copy-anchor-btn" onclick="copyClauseLink('{anchor_id}')" title="Copy link to clause">
                <i class="fa-regular fa-copy"></i>
              </button>
            </div>
          </header>
          <div class="legal-card-body">
            {body}
          </div>
        </section>
        """)
        
    return "\n".join(toc_chips), "\n".join(toc_sidebar), "\n".join(cards_html)

print("Terms and Privacy builders ready.")
