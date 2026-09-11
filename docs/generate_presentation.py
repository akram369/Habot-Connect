# ==============================================================================
# Habot Connect FZCO — PowerPoint Presentation Generator
# Generates HabotConnect_Architecture.pptx (Exactly 15 Slides)
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# ==============================================================================

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

os.makedirs("docs", exist_ok=True)

prs = Presentation()
# Set widescreen 16:9 layout
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]

# Color Palette
COLOR_NAVY = RGBColor(26, 54, 93)      # Primary Deep Navy
COLOR_SLATE = RGBColor(43, 108, 176)   # Secondary Slate Blue
COLOR_DARK = RGBColor(45, 55, 72)      # Charcoal Body Text
COLOR_MUTED = RGBColor(113, 128, 150)  # Cool Grey Subtitle
COLOR_BG_CARD = RGBColor(247, 250, 252)# Off-white Card
COLOR_BORDER = RGBColor(226, 232, 240) # Subtle Card Border
COLOR_RED = RGBColor(197, 48, 48)      # Alert Red
COLOR_GREEN = RGBColor(40, 167, 69)    # Success Green
COLOR_WHITE = RGBColor(255, 255, 255)  # Pure White

def add_header(slide, title_text, category_text="HABOT CONNECT FZCO | HIRING PROJECT"):
    # Header background band
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_NAVY
    top_bar.line.color.rgb = COLOR_NAVY

    # Category Text
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.3))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = RGBColor(237, 137, 54) # Accent Orange

    # Title Text
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.7), Inches(0.65))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    # Footer note
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.35))
    tf_foot = footer_box.text_frame
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = "Shaik Akram | Junior Cloud & DevOps Engineer | +91 6302806015 | akramshaik1512@gmail.com"
    p_foot.font.size = Pt(9)
    p_foot.font.color.rgb = COLOR_MUTED

def add_card(slide, left, top, width, height, title, points, accent_color=COLOR_SLATE):
    # Background Card Box
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_BG_CARD
    card.line.color.rgb = COLOR_BORDER
    card.line.width = Pt(1)

    # Accent top border
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.08))
    accent.fill.solid()
    accent.fill.fore_color.rgb = accent_color
    accent.line.color.rgb = accent_color

    # Card Title
    t_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.45))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(14)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY

    # Card Points
    c_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.6), width - Inches(0.4), height - Inches(0.75))
    tf_c = c_box.text_frame
    tf_c.word_wrap = True

    for i, pt in enumerate(points):
        p = tf_c.add_paragraph() if i > 0 else tf_c.paragraphs[0]
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

# ==============================================================================
# SLIDE 1: Title Slide
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = COLOR_NAVY
bg1.line.color.rgb = COLOR_NAVY

# Decorative accent bar
bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.8), Inches(1.5), Inches(0.1))
bar1.fill.solid()
bar1.fill.fore_color.rgb = RGBColor(237, 137, 54) # Orange accent
bar1.line.color.rgb = RGBColor(237, 137, 54)

tbox1 = s1.shapes.add_textbox(Inches(1.2), Inches(2.1), Inches(11.0), Inches(2.5))
tf1 = tbox1.text_frame
tf1.word_wrap = True
p1_1 = tf1.paragraphs[0]
p1_1.text = "Habot Connect FZCO — Deployment & Automation Blueprint"
p1_1.font.size = Pt(30)
p1_1.font.bold = True
p1_1.font.color.rgb = COLOR_WHITE

p1_2 = tf1.add_paragraph()
p1_2.text = "Staging Restoration, Poka-Yoke Automated Build Gates & Deterministic DCYN Data Pipelines"
p1_2.font.size = Pt(17)
p1_2.font.color.rgb = RGBColor(226, 232, 240)
p1_2.space_before = Pt(10)

# Bio card on title slide
bio_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.5), Inches(10.9), Inches(1.8))
bio_box.fill.solid()
bio_box.fill.fore_color.rgb = RGBColor(30, 64, 110)
bio_box.line.color.rgb = RGBColor(43, 108, 176)

tf_bio = bio_box.text_frame
tf_bio.word_wrap = True
p_b1 = tf_bio.paragraphs[0]
p_b1.text = "Candidate Name: SHAIK AKRAM"
p_b1.font.size = Pt(15)
p_b1.font.bold = True
p_b1.font.color.rgb = COLOR_WHITE

p_b2 = tf_bio.add_paragraph()
p_b2.text = "Position: Junior Cloud & DevOps Engineer (GCP / Django / React) | Full Time 100% Remote"
p_b2.font.size = Pt(12)
p_b2.font.color.rgb = RGBColor(237, 137, 54)
p_b2.space_before = Pt(4)

p_b3 = tf_bio.add_paragraph()
p_b3.text = "Contact: +91 6302806015 | akramshaik1512@gmail.com | LinkedIn: /in/shaik-akram08/ | GitHub: akram369"
p_b3.font.size = Pt(11)
p_b3.font.color.rgb = COLOR_WHITE
p_b3.space_before = Pt(4)

p_b4 = tf_bio.add_paragraph()
p_b4.text = "Submission Date: 11-September-2026 | Submission Link: https://forms.gle/qaTCAxi3YA8MCN196"
p_b4.font.size = Pt(10)
p_b4.font.color.rgb = RGBColor(203, 213, 224)
p_b4.space_before = Pt(3)

# ==============================================================================
# SLIDE 2: Staging Incident & Problem Statement
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Critical Staging Scenario: Incident Breakdown & Root Cause Analysis")
add_card(s2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2),
    "1. Incident Anatomy: What Failed in Staging",
    [
        "A junior developer pushed an emergency hotfix directly bypassing standard code review and staging verification gates.",
        "Unencrypted GCP service account credentials and raw API secrets were embedded directly in application source code.",
        "An unvalidated schema modification altered student onboarding payload keys, severing downstream BigQuery analytics ingestion.",
        "Failure to enforce pre-commit linters allowed malformed formatting, untyped inputs, and circular dependencies into staging.",
        "Absence of a 'Fail-Closed' posture allowed the defective container image to deploy successfully despite critical security flaws."
    ],
    COLOR_RED
)
add_card(s2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2),
    "2. Three Mandated Engineering Remediation Pillars",
    [
        "Task 1: Secure Infrastructure as Code (IaC) — Provisioning D0 Raw Landing (GCS) and D1 Staged/Enforced (BigQuery) using modular Terraform.",
        "Enforcing Customer-Managed Encryption Keys (CMEK), Uniform Bucket-Level Access, and strict Row-Level Security (RLS) policies.",
        "Task 2: Poka-Yoke Automated CI/CD Build Gate — Designing an uncompromising Fail-Closed GitHub Actions pipeline.",
        "Automated gates halt and quarantine any build with secret leakage, style non-conformance, or vulnerable dependencies.",
        "Task 3: Schema Deconstruction & DCYN Library — Converting human subjective inputs into deterministic binary (Yes/No) truths.",
        "Implementing zero-judgment Django REST Framework serializers matching Pub/Sub and BigQuery schemas exactly."
    ],
    COLOR_SLATE
)

# ==============================================================================
# SLIDE 3: HabotConnect Values & Leadership Principles Alignment
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "HabotConnect Culture: Values & Leadership Principles Alignment")
add_card(s3, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.2),
    "1. Poka-Yoke (Mistake-Proofing)",
    [
        "Golden Rule: Never rely on 'human memory' or 'good intentions' to prevent production bugs.",
        "Automated build gates act as hard physical interlocks—mechanically preventing bad code from proceeding.",
        "Deterministic linters and type checkers eliminate 100% of stylistic debates.",
        "Every schema boundary is validated mathematically with zero tolerance for fuzziness."
    ],
    COLOR_NAVY
)
add_card(s3, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.2),
    "2. Absolute Structural Discipline",
    [
        "Quiet Management: Engineers operate autonomously with extreme ownership and zero micromanagement.",
        "Strict adherence to naming conventions, full forms only, and complete absence of placeholders.",
        "Least Privilege access control: every service account possesses strictly the minimal required permissions.",
        "Immutable audit trails: every raw payload is hashed with SHA-256 before transformation."
    ],
    COLOR_SLATE
)
add_card(s3, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.2),
    "3. Fail-Closed Security Posture",
    [
        "Default Deny: In any ambiguous, erroneous, or unexpected state, the system halts immediately.",
        "If parental consent is missing, ingestion halts with an HTTP 400 Bad Request.",
        "If a secret token pattern is matched, GitHub Actions aborts packaging and isolates the commit.",
        "Row-Level Security returns 0 rows to unauthorized actors rather than leaking records."
    ],
    RGBColor(49, 151, 149) # Teal
)

# ==============================================================================
# SLIDE 4: End-to-End System Architecture Blueprint
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "End-to-End System Architecture: Secure Data Ingestion Pipeline")
add_card(s4, Inches(0.8), Inches(1.5), Inches(2.7), Inches(5.2),
    "Step 1: Frontend & Edge",
    [
        "React SPA Onboarding Portal.",
        "Client-side validation of student demographic data.",
        "HTTPS TLS 1.3 Transport Encryption.",
        "Parent and LSA persona role token authentication.",
        "Submits atomic JSON onboarding payload to API."
    ],
    COLOR_NAVY
)
add_card(s4, Inches(3.8), Inches(1.5), Inches(2.7), Inches(5.2),
    "Step 2: DRF Ingestion API",
    [
        "Django REST Framework Ingestion Service.",
        "Poka-Yoke Fail-Closed Secret Key Loading.",
        "DCYN Logic Library binary deconstruction.",
        "Zero-judgment boundary & age limit validation.",
        "Computes SHA-256 payload audit digest."
    ],
    COLOR_SLATE
)
add_card(s4, Inches(6.8), Inches(1.5), Inches(2.7), Inches(5.2),
    "Step 3: Pub/Sub & D0 Storage",
    [
        "Google Cloud Pub/Sub topic 'student-onboarding-raw'.",
        "At-least-once streaming guarantee.",
        "D0 Raw Landing Bucket (GCS).",
        "CMEK Cloud KMS encryption.",
        "Uniform bucket-level access & audit logging.",
        "Lifecycle: 30d Nearline, 90d deletion."
    ],
    RGBColor(49, 151, 149)
)
add_card(s4, Inches(9.8), Inches(1.5), Inches(2.7), Inches(5.2),
    "Step 4: D1 BigQuery Warehouse",
    [
        "BigQuery D1 Staged/Enforced dataset.",
        "Day-level partitioning on ingestion timestamp.",
        "Clustered on assigned LSA & jurisdiction.",
        "Row-Level Security (RLS) enforcement.",
        "Downstream analytics for LSA matching."
    ],
    COLOR_NAVY
)

# ==============================================================================
# SLIDE 5: Task 1: Terraform IaC — D0 Raw Landing Bucket Security
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "Task 1: Terraform IaC — D0 Raw Landing Google Cloud Storage Security")
add_card(s5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2),
    "1. Bucket Hardening & Protection Controls",
    [
        "Resource Identifier: habotconnect-d0-raw-landing-staging-xxxx.",
        "Uniform Bucket-Level Access: Enabled (disables legacy POSIX ACLs, enforces IAM).",
        "Public Access Prevention: Enforced (hard blocks any public internet visibility).",
        "Object Versioning: Enabled (protects against accidental deletion or overwrite).",
        "Customer-Managed Encryption Keys (CMEK): Cloud KMS Keyring integration.",
        "Immutable Audit Logging: All access and storage events streamed to dedicated audit bucket.",
        "Automated Rotation: Cloud KMS CryptoKey rotates automatically every 90 days."
    ],
    COLOR_NAVY
)
add_card(s5, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2),
    "2. Mistake-Proofing Retention Lifecycle Rules",
    [
        "Rule 1 (Nearline Transition): Objects older than 30 days automatically move to Nearline storage (saving 50% on storage costs).",
        "Rule 2 (Coldline Transition): Objects older than 60 days move to Coldline storage.",
        "Rule 3 (Data Retention Expiration): Live raw objects permanently deleted after 90 days (complies with UAE data minimization mandate).",
        "Rule 4 (Non-Current Version Expiration): Superseded object versions automatically deleted after 14 days.",
        "Zero-Waste Architecture: Eliminates manual janitor scripts and human operational oversight."
    ],
    COLOR_SLATE
)

# ==============================================================================
# SLIDE 6: Task 1: Terraform IaC — D1 Staged BigQuery Dataset & Enforced Schema
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Task 1: Terraform IaC — D1 Staged Google BigQuery Warehouse & Schema")
add_card(s6, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2),
    "1. D1 Staged/Enforced Dataset Architecture",
    [
        "Dataset ID: habotconnect_d1_staged_enforced (Location: me-central1 Dubai).",
        "Default Table Expiration: 180 days (prevents staging data creep).",
        "CMEK Cloud KMS Encryption: Uses dedicated BigQuery CMEK CryptoKey.",
        "Access Control List: OWNER (Terraform Admin), WRITER (Analytics Pipeline Service Account), READER (LSA & Compliance Groups).",
        "Data Classification: Confidential Staged Enforced.",
        "Automated Provisioning: 100% reproducible via Terraform main.tf without manual GCP Console touches."
    ],
    COLOR_NAVY
)
add_card(s6, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2),
    "2. High-Performance Partitioning & Clustering",
    [
        "Target Table: student_onboarding_staged (24 strictly typed schema columns).",
        "Day-Level Time Partitioning: Partitioned by 'ingestion_timestamp' (reduces analytical scan costs by up to 95%).",
        "Multi-Column Clustering: Clustered on 'assigned_learning_support_assistant_identifier' and 'regional_jurisdiction'.",
        "Fast Lookup: Co-locates related student records, accelerating LSA matching dashboards.",
        "Tamper Detection: Every row contains the original payload's SHA-256 hash and schema version 'v1.0.0'."
    ],
    COLOR_SLATE
)

# ==============================================================================
# SLIDE 7: Row-Level Security (RLS) & Data Isolation Architecture
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Row-Level Security (RLS): Multi-Tenant Data Isolation in BigQuery")
add_card(s7, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.2),
    "Policy 1: LSA Student Isolation",
    [
        "Target: Learning Support Assistants.",
        "Predicate: assigned_learning_support_assistant_identifier = SESSION_USER().",
        "Behavior: When LSA Sarah logs in, BigQuery automatically filters rows matching 'sarah@habotconnect.internal'.",
        "Guarantees that LSAs can never inspect student records assigned to other educators.",
        "Zero code change in BI dashboards."
    ],
    COLOR_NAVY
)
add_card(s7, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.2),
    "Policy 2: Regional District Isolation",
    [
        "Target: Regional Educational Coordinators.",
        "Predicate: regional_jurisdiction IN (SELECT district FROM mapping WHERE email = SESSION_USER()).",
        "Behavior: Dubai coordinators only see Dubai students; Abu Dhabi coordinators only see Abu Dhabi students.",
        "Complies with municipal education data localization requirements."
    ],
    COLOR_SLATE
)
add_card(s7, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.2),
    "Policy 3: Compliance Full Audit",
    [
        "Target: Compliance Officers & Legal.",
        "Predicate: TRUE (Unfiltered Access).",
        "Behavior: Compliance group has full visibility across all regional jurisdictions.",
        "Required for statutory child welfare audits, legal inquiries, and quality assurance.",
        "Audited via Cloud Audit Logs."
    ],
    RGBColor(49, 151, 149)
)

# ==============================================================================
# SLIDE 8: Identity & Access Management (IAM) Least Privilege Matrix
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "Identity & Access Management: Least Privilege & IAM Conditions Matrix")
add_card(s8, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2),
    "1. Service Account Strict Separation",
    [
        "Ingestion Service Account (sa-data-ingestion-staging):",
        "  • Role: roles/storage.objectCreator only.",
        "  • IAM Condition: resource.name.startsWith('.../student_onboarding_raw/').",
        "  • Cannot read, list, modify, or delete existing landing objects.",
        "Analytics Pipeline Service Account (sa-analytics-pipeline-staging):",
        "  • Role: roles/storage.objectViewer (GCS) + roles/bigquery.dataEditor (BQ).",
        "  • Cannot alter dataset metadata or IAM policies.",
        "Complete segregation of duties: Ingestion cannot read; Analytics cannot write raw data."
    ],
    COLOR_NAVY
)
add_card(s8, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2),
    "2. Human Persona Access & KMS Key Governance",
    [
        "LSA & Coordinator Google Workspace Groups:",
        "  • Granted roles/bigquery.dataViewer on D1 Staged table.",
        "  • Filtered strictly by Row Access Policies (RLS).",
        "Cloud Storage & BigQuery Service Agents:",
        "  • Granted roles/cloudkms.cryptoKeyEncrypterDecrypter on respective CMEK keys.",
        "  • GCS and BigQuery use separate keys, isolating security blast radius.",
        "Zero Developer Access: Developers possess no raw credentials in code or production database consoles."
    ],
    COLOR_SLATE
)

# ==============================================================================
# SLIDE 9: Task 2: Poka-Yoke Automated CI/CD Build Gate Architecture
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "Task 2: Poka-Yoke Automated CI/CD Build Gate — Fail-Closed Philosophy")
add_card(s9, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2),
    "1. The Golden Rule of Mistake-Proofing",
    [
        "Poka-Yoke Concept: Design systems where it is structurally impossible to make a mistake.",
        "Fail-Closed Design: If an automated check detects any variance, the pipeline stops immediately.",
        "No 'Soft Warnings': Linters and security scanners are configured with zero-warning tolerance.",
        "Build Quarantine: Defective commits are tagged, blocked from artifact registries, and logged.",
        "Prevents the exact staging incident where unencrypted API keys bypassed security."
    ],
    COLOR_NAVY
)
add_card(s9, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2),
    "2. Six-Stage Sequential Quality Pipeline",
    [
        "Gate 1: Static Secret Detection (Gitleaks) — Halts immediately on exposed keys.",
        "Gate 2: Code Quality & Formatting (Black, isort, Flake8) — Enforces structural discipline.",
        "Gate 3: SAST & Dependency Audit (Bandit, pip-audit) — Blocks security vulnerabilities.",
        "Gate 4: IaC Syntax & Security (Terraform fmt, validate, tfsec) — Audits cloud resources.",
        "Gate 5: Automated Test Suite (Pytest, DCYN, Serializer limits) — Validates logic 100%.",
        "Gate 6: Fail-Closed Quarantine Handler — Triggered if: failure()."
    ],
    COLOR_SLATE
)

# ==============================================================================
# SLIDE 10: Build Gate Inspection Stages & Tooling
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "Poka-Yoke Build Gate: Tooling Breakdown & Inspection Specifications")
add_card(s10, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.2),
    "Gates 1 & 2: Secrets & Code Style",
    [
        "Gitleaks Action v2:",
        "  • Scans complete git commit diffs.",
        "  • Blocks GCP service account keys, JWTs, and API tokens.",
        "Black (line-length = 100):",
        "  • Enforces deterministic Python formatting.",
        "Flake8 & isort:",
        "  • Max line length 100 characters.",
        "  • Zero tolerance for unused or wildcard imports."
    ],
    COLOR_NAVY
)
add_card(s10, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.2),
    "Gates 3 & 4: SAST & Infrastructure",
    [
        "Bandit Security Scanner:",
        "  • AST-based analysis of backend code.",
        "  • Flags insecure deserialization, SQLi, and hardcoded secrets.",
        "pip-audit Dependency Auditor:",
        "  • Scans locked requirements.txt for CVEs.",
        "Terraform fmt & tfsec:",
        "  • Enforces canonical HCL formatting.",
        "  • Blocks unencrypted buckets or public ACLs."
    ],
    COLOR_SLATE
)
add_card(s10, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.2),
    "Gates 5 & 6: Tests & Quarantine",
    [
        "Pytest & Pytest-Django:",
        "  • 58 unit tests asserting 100% pass rate.",
        "  • Validates age limits, phone formats, and DCYN normalization.",
        "Quarantine Incident Handler:",
        "  • Triggered conditionally on any failure.",
        "  • Emits security alert, revokes CI token, and locks artifact promotion."
    ],
    RGBColor(49, 151, 149)
)

# ==============================================================================
# SLIDE 11: Demonstration of Fail-Closed Build Gate & Quarantine
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "Demonstration: Fail-Closed Pipeline Trigger on Insecure Commit")
add_card(s11, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2),
    "1. Insecure Commit Simulation",
    [
        "Developer commits test branch containing:",
        "  • Raw API Secret Key: 'AIzaSyD9876543210ABCDEFGHIJKLMN12345'.",
        "  • Formatting Violation: Line 102 exceeding 130 characters.",
        "  • Schema Mismatch: Student age set to 2 years old (under minimum threshold).",
        "GitHub Actions Pipeline triggers on 'git push'.",
        "Gate 1 (Gitleaks) executes regex scan against commit diff."
    ],
    COLOR_RED
)
add_card(s11, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2),
    "2. Automated Fail-Closed Execution Log",
    [
        "[Gitleaks] CRITICAL: Exposed GCP credential pattern detected!",
        "[Status] Process exited with exit code 1 (FAILED).",
        "[Pipeline] Halting downstream test and deploy jobs immediately.",
        "[Quarantine Handler] Commit tagged 'quarantined-security-violation'.",
        "[Audit] Deployment permanently blocked; Security lead notified.",
        "Result: The breach never reaches staging. System integrity 100% preserved."
    ],
    COLOR_NAVY
)

# ==============================================================================
# SLIDE 12: Task 3: DCYN Binary Logic Library Architecture
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
add_header(s12, "Task 3: DCYN Binary Logic Library — Deterministic Schema Deconstruction")
add_card(s12, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2),
    "1. Eliminating Human Subjective Interpretation",
    [
        "Problem: Free-text inputs ('maybe', 'sometimes', 'unknown') cause schema mismatches and break downstream analytics.",
        "Solution: Deterministic Clean Yes/No (DCYN) binary logic library.",
        "Strict Truth Mappings: True, 1, 'yes', 'y', 'true', '1' -> True.",
        "Strict False Mappings: False, 0, 'no', 'n', 'false', '0' -> False.",
        "Strict Rejections: 'maybe', 'partially', 'n/a', 'pending', empty string, or None -> raises DCYNValidationError.",
        "Zero Ambiguity: Mathematical certainty for matching LSAs with special needs students."
    ],
    COLOR_NAVY
)
add_card(s12, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2),
    "2. Ten Standardized DCYN Onboarding Questions",
    [
        "1. has_prior_formal_diagnosis (Clinical certified diagnosis).",
        "2. requires_one_on_one_support (100% dedicated LSA requirement).",
        "3. has_individualized_education_plan (Active IEP document on record).",
        "4. requires_non_verbal_communication_assistance (PECS / AAC tools).",
        "5. has_physical_mobility_assistance_needs (Wheelchair/mobility support).",
        "6. is_independently_toilet_trained (Personal hygiene independence).",
        "7. has_sensory_sensitivity_triggers (Acoustic/visual hypersensitivity).",
        "8. parental_data_processing_consent_granted (UAE Legal Gate - MUST BE TRUE).",
        "9. emergency_medical_action_plan_available (Pediatric emergency protocol).",
        "10. transportation_assistance_required (Special school bus transit needs)."
    ],
    COLOR_SLATE
)

# ==============================================================================
# SLIDE 13: Task 3: Django REST Framework ModelSerializer & Validation Limits
# ==============================================================================
s13 = prs.slides.add_slide(blank_layout)
add_header(s13, "Task 3: DRF ModelSerializer — Zero-Judgment Mathematical Boundaries")
add_card(s13, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2),
    "1. Exact Field Boundary Validations",
    [
        "Student Full Name: 2 to 100 characters; regex '^[A-Za-z\\s\\'-]+$'; trimmed.",
        "Date of Birth: Exact age calculated in fractional years.",
        "  • Minimum Age Limit: Exactly 3.00 years old (early intervention).",
        "  • Maximum Age Limit: Exactly 18.00 years old (K-12 graduation limit).",
        "  • Underage (<3) or overage (>18) rejected with precise validation error.",
        "Parent & Emergency Phone: International E.164 regex '^\\+[1-9]\\d{6,14}$'.",
        "Disposable Email Blocking: Domains like 'mailinator.com' strictly prohibited."
    ],
    COLOR_NAVY
)
add_card(s13, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2),
    "2. Cross-Field Logic & Streaming Serialization",
    [
        "Emergency Contact Cross-Field Check: Emergency contact cannot be identical in name or phone number to the primary parent.",
        "Parental Consent Legal Gate: dcyn_parental_data_processing_consent_granted must be TRUE; halts ingestion if False.",
        "Audit Digest: Automatically calculates SHA-256 hash across sorted payload keys.",
        "to_bigquery_row(): Structures record into native types matching D1 Staged schema.",
        "to_pubsub_message(): Encodes payload as UTF-8 JSON for Cloud Pub/Sub topic."
    ],
    COLOR_SLATE
)

# ==============================================================================
# SLIDE 14: Verification Suite & Mathematical Proof
# ==============================================================================
s14 = prs.slides.add_slide(blank_layout)
add_header(s14, "Verification Suite: Mathematical Proof of System Reliability")
add_card(s14, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.2),
    "1. Unit Testing Results (Pytest)",
    [
        "58 Total Unit Tests Executed.",
        "58 Passed in 0.78 seconds (100% Success).",
        "DCYN logic testing: Truthy, Falsy, and all ambiguous rejections.",
        "Serializer limits: Exact age limits, E.164 phone formats, duplicate contact rejection.",
        "Security tests: Leaked secret payload rejection verified."
    ],
    COLOR_GREEN
)
add_card(s14, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.2),
    "2. Structural Linter (Flake8)",
    [
        "Flake8 Command: flake8 backend/ --config=.flake8.",
        "Result: 0 Errors, 0 Warnings.",
        "Enforces max line length = 100.",
        "Deterministic formatting via Black and isort.",
        "Zero unused imports or syntax warnings."
    ],
    COLOR_NAVY
)
add_card(s14, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.2),
    "3. Security SAST (Bandit)",
    [
        "Bandit Command: bandit -r backend/ -ll -ii.",
        "Result: 0 High/Medium Severity Issues.",
        "Zero hardcoded secrets detected.",
        "Zero SQL injection or insecure deserialization flaws.",
        "100% Fail-Closed verified."
    ],
    COLOR_SLATE
)

# ==============================================================================
# SLIDE 15: Executive Conclusion & Engineering Roadmap
# ==============================================================================
s15 = prs.slides.add_slide(blank_layout)
add_header(s15, "Executive Conclusion: Production Readiness & DevOps Roadmap")
add_card(s15, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2),
    "1. Delivered Solutions Summary",
    [
        "Complete Staging Restoration: Full resolution of the junior developer incident.",
        "Terraform IaC Blueprint: Automated GCS D0 Landing, BigQuery D1 Staged, CMEK, and RLS.",
        "Poka-Yoke CI/CD Build Gate: Fail-Closed GitHub Actions pipeline blocking secrets and lint errors.",
        "DCYN Logic Library: Zero-judgment binary normalization of special needs onboarding data.",
        "Full Documentation: 15-slide presentation, wrapped-text Excel schema mapping, and markdown blueprints."
    ],
    COLOR_NAVY
)
add_card(s15, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2),
    "2. Candidate Commitment & Readiness",
    [
        "Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com",
        "Demonstrated mastery of GCP IaC, DRF backend development, and Poka-Yoke automation.",
        "Thrives in HabotConnect's quiet management, detail-obsessed, 100% remote culture.",
        "Ready to present this blueprint to the CEO, Team Lead, and Engineering Panel.",
        "Thank you for the opportunity to participate in this hiring simulation!"
    ],
    COLOR_SLATE
)

output_presentation = "docs/HabotConnect_Architecture.pptx"
prs.save(output_presentation)
print(f"Successfully generated {output_presentation} with exactly {len(prs.slides)} slides.")
