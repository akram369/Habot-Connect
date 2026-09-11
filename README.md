# Habot Connect FZCO — Deployment & Automation Blueprint
## Junior Cloud & DevOps Engineer (GCP / Django / React) Hiring Project

**Candidate**: Shaik Akram  
**Contact**: +91 6302806015 | akramshaik1512@gmail.com  
**Profiles**: [LinkedIn](https://www.linkedin.com/in/shaik-akram08/) | [GitHub](https://github.com/akram369)  
**Company**: Habot Connect FZCO (Dubai, UAE | 100% Remote)  
**Submission Form**: [Google Form Submission Link](https://forms.gle/qaTCAxi3YA8MCN196)  
**Submission Deadline**: 13-September-2026  

---

## Executive Summary & Incident Context

HabotConnect is building a digital platform connecting parents of neurodivergent children with accredited Learning Support Assistants (LSAs). To scale this platform securely, our backend Django REST Framework (DRF) and frontend React applications deploy via automated pipelines to Google Cloud Platform (GCP).

### The Critical Staging Incident
A junior developer pushed an unreviewed hotfix into the staging environment:
1. **Security Guideline Bypass**: Leaked unencrypted GCP service account credentials and raw API secrets into application source code.
2. **Schema Mismatch**: Introduced an unvalidated schema change on student onboarding forms, severing downstream BigQuery analytics pipelines.
3. **Pipeline Permissiveness**: The absence of strict "Fail-Closed" gates allowed the defective code to build and deploy.

### Remediation Blueprint
This repository delivers the production-ready automation and data blueprint designed to restore system integrity, enforce automated mistake-proofing (**Poka-Yoke**), and guarantee zero data loss across pipelines.

---

## Repository Structure & Deliverables Manifest

```
d:/Habot Connect/
├── README.md                                  # Master documentation with candidate credentials
├── pytest.ini                                 # Pytest runner configuration with pythonpath & settings
├── pyproject.toml                             # Python tooling specifications (Black, isort, pytest)
├── .flake8                                    # Strict Flake8 linter configuration (max-line-length = 100)
├── .gitleaks.toml                             # Static secret scanner regex and allowlist rules
├── docs/
│   ├── architectural_blueprint.md             # In-depth architectural & data pipeline documentation
│   ├── fail_closed_demonstration.md           # Log demonstration of the Fail-Closed build gate
│   ├── generate_excel_mapping.py              # Script generating wrapped-text Excel workbook
│   ├── generate_presentation.py               # Script generating 15-slide PowerPoint deck
│   ├── HabotConnect_Architecture.pptx         # 15-slide executive presentation file
│   └── HabotConnect_Data_Schema_Mapping.xlsx  # Multi-sheet workbook (Wrap Text & Full Forms Only)
├── terraform/
│   ├── versions.tf                            # Terraform core & Google Cloud provider locking
│   ├── variables.tf                           # Variables with strict types and descriptions
│   ├── main.tf                                # GCS D0 Landing, BigQuery D1 Staged, KMS & RLS
│   ├── outputs.tf                             # Output attributes (URIs, dataset IDs, SA emails)
│   ├── terraform.tfvars                       # Staging environment variable assignments
│   └── rls_policies.sql                       # BigQuery Row-Level Security DDL scripts
├── .github/
│   └── workflows/
│       └── poka_yoke_build_gate.yml           # Fail-closed multi-stage GitHub Actions pipeline
├── backend/
│   ├── manage.py                              # Django management script
│   ├── requirements.txt                       # Locked backend Python dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py                        # Hardened settings (fail-closed secret key loading)
│   │   ├── urls.py                            # Core URL routing
│   │   └── wsgi.py                            # WSGI entrypoint
│   └── onboarding/
│       ├── __init__.py
│       ├── apps.py                            # App configuration
│       ├── dcyn_library.py                    # Deterministic Clean Yes/No logic library
│       ├── models.py                          # StudentOnboardingProfile database model
│       ├── serializers.py                     # DRF ModelSerializer with zero-judgment limits
│       ├── views.py                           # Secure ingestion endpoint & streaming sink
│       ├── urls.py                            # App endpoint routing
│       └── tests/
│           ├── __init__.py
│           ├── test_dcyn_library.py           # Unit tests for DCYN binary transformations
│           ├── test_serializers.py            # Unit tests for strict mathematical boundaries
│           └── test_poka_yoke_gate.py         # Tests asserting secret leakage prevention
└── tests/
    ├── sample_valid_payload.json              # Valid student onboarding JSON payload
    ├── sample_invalid_payload_schema.json     # Payload violating strict age & boundary limits
    └── sample_insecure_payload_secret.json    # Payload simulating unencrypted secret leak
```

---

## Detailed Task Breakdown

### Task 1: Terraform Secure Staging Provisioning (IaC)
- **File**: [`terraform/main.tf`](file:///d:/Habot%20Connect/terraform/main.tf)
- **Google Cloud Storage (D0 Raw Landing Bucket)**:
  - Uniform Bucket-Level Access enabled (`uniform_bucket_level_access = true`).
  - Public Access Prevention hard-enforced (`public_access_prevention = "enforced"`).
  - Object Versioning enabled.
  - Customer-Managed Encryption Keys (CMEK) via Google Cloud KMS Keyring.
  - Automated Lifecycle Rules: 30-day Nearline transition, 60-day Coldline transition, 90-day permanent deletion, 14-day non-current version purge.
  - Immutable access audit logging to dedicated audit bucket.
- **Google BigQuery Dataset (D1 Staged/Enforced)**:
  - Dataset ID: `habotconnect_d1_staged_enforced` in `me-central1` (Dubai).
  - Default table expiration: 180 days.
  - Dedicated CMEK encryption.
- **BigQuery Table Partitioning & Clustering**:
  - Table `student_onboarding_staged` partitioned by day on `ingestion_timestamp`.
  - Clustered on `assigned_learning_support_assistant_identifier` and `regional_jurisdiction`.
- **Row-Level Security (RLS) Policies**:
  - `lsa_assigned_students_isolation`: Restricts LSAs to rows where `assigned_learning_support_assistant_identifier = SESSION_USER()`.
  - `regional_coordinator_district_isolation`: Restricts regional coordinators by municipal district.
  - `compliance_officer_full_audit`: Grants full visibility to legal/compliance auditors (`FILTER USING (TRUE)`).
- **Least Privilege IAM Conditions**:
  - Ingestion Service Account: Restricted to `roles/storage.objectCreator` on raw onboarding prefix.
  - Analytics Service Account: Restricted to `roles/storage.objectViewer` and `roles/bigquery.dataEditor`.

### Task 2: Poka-Yoke Automated CI/CD Build Gate
- **File**: [`.github/workflows/poka_yoke_build_gate.yml`](file:///d:/Habot%20Connect/.github/workflows/poka_yoke_build_gate.yml)
- **Fail-Closed Gate Hierarchy**:
  1. **Gate 1: Static Secret Detection**: Gitleaks Action scans commit history. Halts immediately on exposed keys.
  2. **Gate 2: Code Quality & Formatting**: Black (`--check`), isort (`--check-only`), and Flake8 (`--max-line-length=100`).
  3. **Gate 3: SAST & Dependency Auditing**: Bandit (`-ll -ii`) and `pip-audit`.
  4. **Gate 4: IaC Syntax & Security**: `terraform fmt -check`, `terraform validate`, and `tfsec`.
  5. **Gate 5: Automated Unit Tests**: Pytest running DCYN logic and DRF serializer boundaries.
  6. **Gate 6: Quarantine Incident Handler**: Triggered conditionally upon any failure (`if: failure()`). Tags commit as quarantined, blocks container registry pushes, and dispatches an incident alert.

### Task 3: Schema Mapping and DCYN Validation Library
- **Files**:
  - [`backend/onboarding/dcyn_library.py`](file:///d:/Habot%20Connect/backend/onboarding/dcyn_library.py)
  - [`backend/onboarding/serializers.py`](file:///d:/Habot%20Connect/backend/onboarding/serializers.py)
  - [`backend/onboarding/models.py`](file:///d:/Habot%20Connect/backend/onboarding/models.py)
- **DCYN Logic Library**:
  - Evaluates affirmative inputs (`True`, `1`, `"yes"`, `"true"`) strictly to `True`.
  - Evaluates negative inputs (`False`, `0`, `"no"`, `"false"`) strictly to `False`.
  - Rejects ambiguous inputs (`"maybe"`, `"sometimes"`, `"unknown"`, `"n/a"`) with `DCYNValidationError`.
  - Enforces 10 standardized clinical/operational special needs indicators.
- **Zero-Judgment Field Boundaries**:
  - Student Age: Strictly between 3.00 and 18.00 years old. Underage (<3) or overage (>18) applicants are rejected.
  - Parent & Emergency Phone: Strict International E.164 format (`^\+[1-9]\d{6,14}$`).
  - Emergency Contact: Cross-field validated to ensure distinct persona and telephone from primary parent.
  - Parental Consent Legal Gate: `dcyn_parental_data_processing_consent_granted` must evaluate to `True`.
  - Streaming Helper Methods: `to_bigquery_row()` and `to_pubsub_message()`.

---

## Submission Artifacts

### 1. PowerPoint Presentation (15 Slides)
- **File**: [`docs/HabotConnect_Architecture.pptx`](file:///d:/Habot%20Connect/docs/HabotConnect_Architecture.pptx)
- **Slide Count**: Exactly 15 slides.
- **Contents**: Title & Candidate Bio, Staging Incident Root Cause, HabotConnect Values Alignment, End-to-End System Blueprint, GCS D0 Security, BigQuery D1 Schema & Partitioning, Row-Level Security Architecture, IAM Least Privilege Matrix, Poka-Yoke Build Gate Philosophy, Tooling Breakdown, Fail-Closed Demonstration Log, DCYN Logic Library, DRF Serializer Limits, Verification Results, and Executive Conclusion.

### 2. Multi-Worksheet Data Schema Workbook (Excel)
- **File**: [`docs/HabotConnect_Data_Schema_Mapping.xlsx`](file:///d:/Habot%20Connect/docs/HabotConnect_Data_Schema_Mapping.xlsx)
- **Formatting Standards**:
  - **Wrap Text Enabled**: 100% of cells across all worksheets have text wrapping enabled for full visibility.
  - **Full Forms Only**: Zero slang, zero abbreviations, and zero placeholders used.
- **Worksheets**:
  1. `Data Schema Mapping`: Comprehensive 24-attribute mapping from source JSON keys to DRF fields and BigQuery columns.
  2. `DCYN Binary Logic Library`: Catalog of 10 binary questions, truth criteria, rejection rules, and operational rationale.
  3. `Security & IAM Matrix`: Role-Based Access Control matrix mapping GCP roles, resources, and IAM Conditions.
  4. `Poka-Yoke Pipeline Gates`: Full specification of inspection stages, tools, fail-closed triggers, and quarantine actions.

---

## Verification & Local Testing Commands

All test suites and linters pass with 100% compliance:

```bash
# 1. Execute full Pytest unit test suite (58 tests)
python -m pytest

# 2. Run Flake8 structural discipline linter (0 errors, 0 warnings)
flake8 backend/ --config=.flake8

# 3. Execute Bandit Static Application Security Testing (0 high/medium issues)
bandit -r backend/ -ll -ii

# 4. Regenerate Excel Schema Mapping Workbook
python docs/generate_excel_mapping.py

# 5. Regenerate 15-Slide Presentation
python docs/generate_presentation.py
```

---

## Candidate Statement

I hereby submit this completed hiring project for the **Junior Cloud & DevOps Engineer** role at **Habot Connect FZCO**. The architecture and code blocks have been engineered with absolute structural discipline, radical accountability, and zero human judgment in validation boundaries. I look forward to presenting this deployment blueprint during the video call presentation phase.

**Shaik Akram**  
*Junior Cloud & DevOps Engineer*  
*Phone*: +91 6302806015  
*Email*: akramshaik1512@gmail.com  
*LinkedIn*: [linkedin.com/in/shaik-akram08/](https://www.linkedin.com/in/shaik-akram08/)  
*GitHub*: [github.com/akram369](https://github.com/akram369)  
