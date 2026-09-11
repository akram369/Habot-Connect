# ==============================================================================
# Habot Connect FZCO — Excel Workbook Generator
# Generates HabotConnect_Data_Schema_Mapping.xlsx with Wrap Text and Full Forms Only
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# ==============================================================================

import os
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

os.makedirs("docs", exist_ok=True)
wb = openpyxl.Workbook()
# Remove default sheet
wb.remove(wb.active)

# Styles
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="1A365D", end_color="1A365D", fill_type="solid") # Deep Navy
sub_header_fill = PatternFill(start_color="2B6CB0", end_color="2B6CB0", fill_type="solid") # Slate Blue
zebra_fill = PatternFill(start_color="F7FAFC", end_color="F7FAFC", fill_type="solid")
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
border_thin = Side(border_style="thin", color="CBD5E0")
cell_border = Border(top=border_thin, left=border_thin, right=border_thin, bottom=border_thin)

# ------------------------------------------------------------------------------
# Sheet 1: Data Schema Mapping
# ------------------------------------------------------------------------------
ws1 = wb.create_sheet(title="Data Schema Mapping")
ws1.views.sheetView[0].showGridLines = True

headers1 = [
    "Source JSON Key Name",
    "Source Data Type",
    "DCYN Transformation Rule",
    "Django REST Framework Field Class",
    "Google BigQuery Column Name",
    "Google BigQuery Data Type",
    "Data Integrity Constraint & Boundary Limits",
    "Nullability Requirement",
    "Functional & Clinical Description"
]

rows1 = [
    [
        "student_full_name",
        "String Literal",
        "Not Applicable (Direct String Normalization)",
        "CharField(max_length=100)",
        "student_full_name",
        "STRING",
        "Minimum 2 characters, maximum 100 characters; Alphabetic characters, spaces, hyphens, and apostrophes only.",
        "Mandatory (Not Nullable)",
        "Official legal full name of the student undergoing educational assessment."
    ],
    [
        "date_of_birth",
        "String (ISO 8601 Date)",
        "Not Applicable (Date Transformation)",
        "DateField()",
        "date_of_birth",
        "DATE",
        "Calculated age must strictly range between 3.00 years and 18.00 years inclusive; Future dates strictly prohibited.",
        "Mandatory (Not Nullable)",
        "Legal calendar birth date of the minor child used for academic age bracket calculation."
    ],
    [
        "parent_full_name",
        "String Literal",
        "Not Applicable (Direct String Normalization)",
        "CharField(max_length=100)",
        "parent_full_name",
        "STRING",
        "Minimum 2 characters, maximum 100 characters; Must be a distinct individual from the secondary emergency contact.",
        "Mandatory (Not Nullable)",
        "Full legal name of the primary custodial parent or authorized guardian."
    ],
    [
        "parent_email_address",
        "String Literal",
        "Not Applicable (Email Validation & Lowercasing)",
        "EmailField(max_length=254)",
        "parent_email_address",
        "STRING",
        "Standard RFC 5322 electronic mail syntax; Disposable email domains are strictly blocked.",
        "Mandatory (Not Nullable)",
        "Verified communication channel for parental notifications and progress reports."
    ],
    [
        "parent_phone_number",
        "String Literal",
        "Not Applicable (Phone Normalization)",
        "CharField(max_length=20)",
        "parent_phone_number",
        "STRING",
        "Strict International Telecommunication Union E.164 formatting; Length between 7 and 15 digits with leading plus sign.",
        "Mandatory (Not Nullable)",
        "Primary mobile telephone number for SMS dispatches and immediate parent communication."
    ],
    [
        "emergency_contact_full_name",
        "String Literal",
        "Not Applicable (Direct String Normalization)",
        "CharField(max_length=100)",
        "emergency_contact_full_name",
        "STRING",
        "Minimum 2 characters, maximum 100 characters; Must not be identical to primary parent full name.",
        "Mandatory (Not Nullable)",
        "Authorized secondary individual reachable during clinical or medical incidents."
    ],
    [
        "emergency_contact_phone_number",
        "String Literal",
        "Not Applicable (Phone Normalization)",
        "CharField(max_length=20)",
        "emergency_contact_phone_number",
        "STRING",
        "Strict International Telecommunication Union E.164 formatting; Must not be identical to parent telephone number.",
        "Mandatory (Not Nullable)",
        "Dedicated secondary telephone line for critical incident escalation."
    ],
    [
        "primary_learning_support_category",
        "String Literal",
        "Not Applicable (Categorical Choice Mapping)",
        "CharField(max_length=60, choices=Choices)",
        "primary_learning_support_category",
        "STRING",
        "Strictly restricted to approved enumerated domains: Autism Spectrum Disorder, Attention Deficit Hyperactivity Disorder, Dyslexia, Speech Language, or Cognitive Delay.",
        "Mandatory (Not Nullable)",
        "Primary accredited diagnostic classification defining specialized educator matching."
    ],
    [
        "assigned_learning_support_assistant_identifier",
        "String Literal",
        "Not Applicable (Identity Mapping)",
        "EmailField(max_length=254)",
        "assigned_learning_support_assistant_identifier",
        "STRING",
        "Valid email address format matching an authenticated Learning Support Assistant employee in Google Workspace directory.",
        "Mandatory (Not Nullable)",
        "Corporate user identifier of the assigned Learning Support Assistant, used for BigQuery Row-Level Security."
    ],
    [
        "regional_jurisdiction",
        "String Literal",
        "Not Applicable (Jurisdiction Choice Mapping)",
        "CharField(max_length=50, choices=Choices)",
        "regional_jurisdiction",
        "STRING",
        "Strictly restricted to: Dubai Educational District, Abu Dhabi Educational District, Sharjah Educational District, or Northern Emirates.",
        "Mandatory (Not Nullable)",
        "Geographical regulatory zone determining municipal regulatory compliance and coordinator visibility."
    ],
    [
        "has_prior_formal_diagnosis",
        "Untyped (String/Number/Boolean)",
        "DCYN Deterministic Binary Yes/No Evaluation",
        "BooleanField(default=False)",
        "dcyn_has_prior_formal_diagnosis",
        "BOOLEAN",
        "Evaluated via DCYNTransformer; Ambiguous values rejected; Output strictly True or False.",
        "Mandatory (Not Nullable)",
        "Indicates whether a formal certified psychological assessment report has been conducted and filed."
    ],
    [
        "requires_one_on_one_support",
        "Untyped (String/Number/Boolean)",
        "DCYN Deterministic Binary Yes/No Evaluation",
        "BooleanField(default=False)",
        "dcyn_requires_one_on_one_support",
        "BOOLEAN",
        "Evaluated via DCYNTransformer; Ambiguous values rejected; Output strictly True or False.",
        "Mandatory (Not Nullable)",
        "Specifies whether the student requires 100 percent individual dedicated educator time rather than shared supervision."
    ],
    [
        "has_individualized_education_plan",
        "Untyped (String/Number/Boolean)",
        "DCYN Deterministic Binary Yes/No Evaluation",
        "BooleanField(default=False)",
        "dcyn_has_individualized_education_plan",
        "BOOLEAN",
        "Evaluated via DCYNTransformer; Ambiguous values rejected; Output strictly True or False.",
        "Mandatory (Not Nullable)",
        "Verifies the active existence of an individualized education plan document on official school record."
    ],
    [
        "requires_non_verbal_communication_assistance",
        "Untyped (String/Number/Boolean)",
        "DCYN Deterministic Binary Yes/No Evaluation",
        "BooleanField(default=False)",
        "dcyn_requires_non_verbal_communication_assistance",
        "BOOLEAN",
        "Evaluated via DCYNTransformer; Ambiguous values rejected; Output strictly True or False.",
        "Mandatory (Not Nullable)",
        "Specifies necessity for Picture Exchange Communication Systems (PECS) or assistive speech software."
    ],
    [
        "has_physical_mobility_assistance_needs",
        "Untyped (String/Number/Boolean)",
        "DCYN Deterministic Binary Yes/No Evaluation",
        "BooleanField(default=False)",
        "dcyn_has_physical_mobility_assistance_needs",
        "BOOLEAN",
        "Evaluated via DCYNTransformer; Ambiguous values rejected; Output strictly True or False.",
        "Mandatory (Not Nullable)",
        "Flags requirement for physical wheelchair navigation or mobility accompaniment within the school campus."
    ],
    [
        "is_independently_toilet_trained",
        "Untyped (String/Number/Boolean)",
        "DCYN Deterministic Binary Yes/No Evaluation",
        "BooleanField(default=False)",
        "dcyn_is_independently_toilet_trained",
        "BOOLEAN",
        "Evaluated via DCYNTransformer; Ambiguous values rejected; Output strictly True or False.",
        "Mandatory (Not Nullable)",
        "Specifies whether personal hygiene care assistance is necessary during active instructional hours."
    ],
    [
        "has_sensory_sensitivity_triggers",
        "Untyped (String/Number/Boolean)",
        "DCYN Deterministic Binary Yes/No Evaluation",
        "BooleanField(default=False)",
        "dcyn_has_sensory_sensitivity_triggers",
        "BOOLEAN",
        "Evaluated via DCYNTransformer; Ambiguous values rejected; Output strictly True or False.",
        "Mandatory (Not Nullable)",
        "Flags severe acoustic, visual, or tactile sensory hypersensitivities requiring sensory decompression accommodation."
    ],
    [
        "parental_data_processing_consent_granted",
        "Untyped (String/Number/Boolean)",
        "DCYN Deterministic Binary Evaluation with Legal Gate",
        "BooleanField(default=False)",
        "dcyn_parental_data_processing_consent_granted",
        "BOOLEAN",
        "Must evaluate strictly to True; Ingestion immediately halts and rejects if False under UAE Federal Data Law.",
        "Mandatory (Not Nullable)",
        "Affirmative parental consent authorizing storage and processing of sensitive student health data."
    ],
    [
        "emergency_medical_action_plan_available",
        "Untyped (String/Number/Boolean)",
        "DCYN Deterministic Binary Yes/No Evaluation",
        "BooleanField(default=False)",
        "dcyn_emergency_medical_action_plan_available",
        "BOOLEAN",
        "Evaluated via DCYNTransformer; Ambiguous values rejected; Output strictly True or False.",
        "Mandatory (Not Nullable)",
        "Confirms certified pediatric protocol is on file for severe allergies, epilepsy, or respiratory emergencies."
    ],
    [
        "transportation_assistance_required",
        "Untyped (String/Number/Boolean)",
        "DCYN Deterministic Binary Yes/No Evaluation",
        "BooleanField(default=False)",
        "dcyn_transportation_assistance_required",
        "BOOLEAN",
        "Evaluated via DCYNTransformer; Ambiguous values rejected; Output strictly True or False.",
        "Mandatory (Not Nullable)",
        "Specifies physical assistance or dedicated transit vehicle requirements during morning and afternoon commute."
    ],
    [
        "student_unique_identifier",
        "Generated System Token",
        "Automated Cryptographic UUIDv4 Generation",
        "UUIDField(primary_key=True, default=uuid4)",
        "student_unique_identifier",
        "STRING",
        "Canonical 36-character hexadecimal UUID Version 4; Primary Key; Immutable.",
        "Mandatory (Not Nullable)",
        "Global surrogate unique identifier assigned to the student record for cross-system tracking."
    ],
    [
        "ingestion_timestamp",
        "Generated System Token",
        "System Universal Time Coordinated Clock",
        "DateTimeField(default=timezone.now)",
        "ingestion_timestamp",
        "TIMESTAMP",
        "ISO 8601 Universal Time Coordinated timestamp; Used for BigQuery table day-level time partitioning.",
        "Mandatory (Not Nullable)",
        "Exact audit timestamp recording when the record passed the Poka-Yoke validation gate."
    ],
    [
        "schema_version",
        "Generated System Token",
        "Static Semantic Version Pinning",
        "CharField(max_length=10, default='v1.0.0')",
        "schema_version",
        "STRING",
        "Strict semantic versioning string pinned to 'v1.0.0'.",
        "Mandatory (Not Nullable)",
        "Schema definition version ensuring backward and forward compatibility across downstream pipelines."
    ],
    [
        "data_payload_sha256_hash",
        "Generated System Token",
        "Cryptographic SHA-256 Digest Calculation",
        "CharField(max_length=64)",
        "data_payload_sha256_hash",
        "STRING",
        "Exact 64-character hexadecimal SHA-256 digest calculated over sorted JSON keys.",
        "Mandatory (Not Nullable)",
        "Cryptographic integrity hash guaranteeing tamper detection between raw landing and staged warehouse."
    ]
]

ws1.append(headers1)
for row in rows1:
    ws1.append(row)

# ------------------------------------------------------------------------------
# Sheet 2: DCYN Binary Logic Library
# ------------------------------------------------------------------------------
ws2 = wb.create_sheet(title="DCYN Binary Logic Library")
ws2.views.sheetView[0].showGridLines = True

headers2 = [
    "Indicator Parameter Identifier",
    "Full Descriptive Name",
    "Permitted Affirmative (True) Inputs",
    "Permitted Negative (False) Inputs",
    "Explicitly Prohibited Ambiguous Inputs (Fail-Closed)",
    "Deterministic Resolution Outcome",
    "Functional Domain Category",
    "Operational Rationale for Zero Human Discretion"
]

rows2 = [
    [
        "has_prior_formal_diagnosis",
        "Has Prior Formal Medical or Psychological Diagnosis",
        "Boolean True, Number 1, 'true', 'yes', 'y', '1'",
        "Boolean False, Number 0, 'false', 'no', 'n', '0'",
        "'maybe', 'partially', 'sometimes', 'unknown', 'undecided', 'n/a', 'pending', empty string, null",
        "Evaluates strictly to True or False. Any ambiguous input immediately halts execution and raises DCYNValidationError.",
        "Clinical Assessment",
        "Government special education grants and regulatory staffing ratios in the UAE require legal documentation. Ambiguity prevents funding approval."
    ],
    [
        "requires_one_on_one_support",
        "Requires Dedicated One-on-One Assistant Support",
        "Boolean True, Number 1, 'true', 'yes', 'y', '1'",
        "Boolean False, Number 0, 'false', 'no', 'n', '0'",
        "'maybe', 'partially', 'sometimes', 'unknown', 'undecided', 'n/a', 'pending', empty string, null",
        "Evaluates strictly to True or False. Any ambiguous input immediately halts execution and raises DCYNValidationError.",
        "Resource Allocation",
        "Directly dictates financial billing and staff scheduling. An LSA cannot be assigned part-time without contractual clarity."
    ],
    [
        "has_individualized_education_plan",
        "Has Active Individualized Education Plan Document",
        "Boolean True, Number 1, 'true', 'yes', 'y', '1'",
        "Boolean False, Number 0, 'false', 'no', 'n', '0'",
        "'maybe', 'partially', 'sometimes', 'unknown', 'undecided', 'n/a', 'pending', empty string, null",
        "Evaluates strictly to True or False. Any ambiguous input immediately halts execution and raises DCYNValidationError.",
        "Academic Support",
        "Legal framework requirement established by UAE Knowledge and Human Development Authority (KHDA). Curricular adaptations depend on an active IEP."
    ],
    [
        "requires_non_verbal_communication_assistance",
        "Requires Non-Verbal Communication Assistance",
        "Boolean True, Number 1, 'true', 'yes', 'y', '1'",
        "Boolean False, Number 0, 'false', 'no', 'n', '0'",
        "'maybe', 'partially', 'sometimes', 'unknown', 'undecided', 'n/a', 'pending', empty string, null",
        "Evaluates strictly to True or False. Any ambiguous input immediately halts execution and raises DCYNValidationError.",
        "Communication Needs",
        "Requires specialized training in Picture Exchange Communication Systems (PECS) or tablet-based AAC devices. Non-certified LSAs cannot be placed."
    ],
    [
        "has_physical_mobility_assistance_needs",
        "Has Physical Mobility Assistance Needs",
        "Boolean True, Number 1, 'true', 'yes', 'y', '1'",
        "Boolean False, Number 0, 'false', 'no', 'n', '0'",
        "'maybe', 'partially', 'sometimes', 'unknown', 'undecided', 'n/a', 'pending', empty string, null",
        "Evaluates strictly to True or False. Any ambiguous input immediately halts execution and raises DCYNValidationError.",
        "Physical Support",
        "Safety and liability requirement. Involves physical transfer ergonomics and campus architectural accessibility compliance."
    ],
    [
        "is_independently_toilet_trained",
        "Is Independently Restroom and Hygiene Trained",
        "Boolean True, Number 1, 'true', 'yes', 'y', '1'",
        "Boolean False, Number 0, 'false', 'no', 'n', '0'",
        "'maybe', 'partially', 'sometimes', 'unknown', 'undecided', 'n/a', 'pending', empty string, null",
        "Evaluates strictly to True or False. Any ambiguous input immediately halts execution and raises DCYNValidationError.",
        "Self Care Independence",
        "Determines child protection certification levels and sanitary facility protocols. Cannot be left to staff subjective assumption."
    ],
    [
        "has_sensory_sensitivity_triggers",
        "Has Extreme Sensory Sensitivity Triggers",
        "Boolean True, Number 1, 'true', 'yes', 'y', '1'",
        "Boolean False, Number 0, 'false', 'no', 'n', '0'",
        "'maybe', 'partially', 'sometimes', 'unknown', 'undecided', 'n/a', 'pending', empty string, null",
        "Evaluates strictly to True or False. Any ambiguous input immediately halts execution and raises DCYNValidationError.",
        "Environmental Adaptation",
        "School assemblies, fire alarms, or cafeteria environments can trigger severe distress without pre-planned sensory mitigation equipment."
    ],
    [
        "parental_data_processing_consent_granted",
        "Parental Data Processing Legal Consent Granted",
        "Boolean True, Number 1, 'true', 'yes', 'y', '1'",
        "Boolean False, Number 0, 'false', 'no', 'n', '0'",
        "'maybe', 'partially', 'sometimes', 'unknown', 'undecided', 'n/a', 'pending', empty string, null",
        "Must evaluate strictly to True. If False, pipeline immediately fails closed and quarantines the transaction.",
        "Legal Compliance",
        "Processing minor pediatric neurodevelopmental data without explicit parental consent violates UAE Federal Law No. 45 on Data Protection."
    ],
    [
        "emergency_medical_action_plan_available",
        "Emergency Medical Action Plan Available",
        "Boolean True, Number 1, 'true', 'yes', 'y', '1'",
        "Boolean False, Number 0, 'false', 'no', 'n', '0'",
        "'maybe', 'partially', 'sometimes', 'unknown', 'undecided', 'n/a', 'pending', empty string, null",
        "Evaluates strictly to True or False. Any ambiguous input immediately halts execution and raises DCYNValidationError.",
        "Health & Safety",
        "Critical emergency protocol for pediatric conditions (anaphylaxis, asthma, epilepsy). Emergency medical protocols must be on file."
    ],
    [
        "transportation_assistance_required",
        "Specialized Transportation Assistance Required",
        "Boolean True, Number 1, 'true', 'yes', 'y', '1'",
        "Boolean False, Number 0, 'false', 'no', 'n', '0'",
        "'maybe', 'partially', 'sometimes', 'unknown', 'undecided', 'n/a', 'pending', empty string, null",
        "Evaluates strictly to True or False. Any ambiguous input immediately halts execution and raises DCYNValidationError.",
        "Logistics & Transport",
        "School bus route assignment and physical safety harness requirements must be locked in advance of term start."
    ]
]

ws2.append(headers2)
for row in rows2:
    ws2.append(row)

# ------------------------------------------------------------------------------
# Sheet 3: Security & IAM Matrix
# ------------------------------------------------------------------------------
ws3 = wb.create_sheet(title="Security & IAM Matrix")
ws3.views.sheetView[0].showGridLines = True

headers3 = [
    "Security Persona or Service Principal",
    "Google Cloud Platform IAM Role Assigned",
    "Target Resource Scope",
    "IAM Condition & Policy Predicate Expression",
    "Row-Level Security / Column-Level Security Boundary",
    "Operational Purpose",
    "Least Privilege Justification"
]

rows3 = [
    [
        "Data Ingestion Service Account (sa-data-ingestion-staging)",
        "roles/storage.objectCreator",
        "Google Cloud Storage Bucket: habotconnect-d0-raw-landing",
        "resource.name.startsWith('projects/_/buckets/habotconnect-d0-raw-landing/objects/student_onboarding_raw/')",
        "Not Applicable (Object level prefix condition)",
        "Upload incoming raw encrypted student onboarding JSON payloads into D0 Raw Landing.",
        "Cannot read, list, modify, or delete existing objects. Write-only access restricted to specific ingestion directory."
    ],
    [
        "Analytics Pipeline Service Account (sa-analytics-pipeline-staging)",
        "roles/storage.objectViewer",
        "Google Cloud Storage Bucket: habotconnect-d0-raw-landing",
        "resource.name.startsWith('projects/_/buckets/habotconnect-d0-raw-landing/objects/student_onboarding_raw/')",
        "Not Applicable (Object level prefix condition)",
        "Extract raw JSON payloads from D0 Raw Landing to perform schema validation and ETL transformation.",
        "Cannot write, overwrite, or delete raw landing objects. Read-only access restricted to verified landing folder."
    ],
    [
        "Analytics Pipeline Service Account (sa-analytics-pipeline-staging)",
        "roles/bigquery.dataEditor",
        "Google BigQuery Dataset: habotconnect_d1_staged_enforced",
        "None (Dataset level writer role)",
        "Not Applicable (Writer pipeline bypasses RLS on insert)",
        "Stream verified, DCYN-validated student records into the D1 Staged Enforced data warehouse table.",
        "Cannot create new datasets, alter dataset permissions, or delete dataset resources."
    ],
    [
        "Learning Support Assistant Group (learning-support-assistants@habotconnect.internal)",
        "roles/bigquery.dataViewer",
        "Google BigQuery Table: student_onboarding_staged",
        "None (Restricted via Row Access Policy)",
        "Row Access Policy: assigned_learning_support_assistant_identifier = SESSION_USER()",
        "Allows active Learning Support Assistants to inspect onboarding details for students assigned directly to them.",
        "Zero visibility into unassigned students. Query returns only matching rows; other rows are mathematically filtered out."
    ],
    [
        "Regional Educational Coordinators (regional-coordinators@habotconnect.internal)",
        "roles/bigquery.dataViewer",
        "Google BigQuery Table: student_onboarding_staged",
        "None (Restricted via Row Access Policy)",
        "Row Access Policy: regional_jurisdiction IN (SELECT jurisdiction FROM coordinator_mapping WHERE email = SESSION_USER())",
        "Allows municipal supervisors to inspect matching and staffing metrics within their geographical zone.",
        "Strictly isolated by district (Dubai, Abu Dhabi, Sharjah). Cannot access cross-jurisdiction student records."
    ],
    [
        "Compliance & Legal Audit Group (compliance-officers@habotconnect.internal)",
        "roles/bigquery.dataViewer",
        "Google BigQuery Table: student_onboarding_staged",
        "None (Unrestricted Row Access Policy)",
        "Row Access Policy: TRUE (Unconstrained audit access)",
        "Enables comprehensive statutory data audit, subject access request resolution, and regulatory oversight.",
        "Read-only visibility across all rows without modification or data deletion rights."
    ],
    [
        "Google Cloud Storage Service Agent",
        "roles/cloudkms.cryptoKeyEncrypterDecrypter",
        "Cloud Key Management Service CryptoKey: habotconnect-storage-encryption-key",
        "None (Service Agent role for CMEK encryption)",
        "Not Applicable (Cryptographic Keyring level)",
        "Encrypts and decrypts raw storage objects using Customer-Managed Encryption Keys.",
        "Key management is decoupled from storage administrator. Key rotation is automated every 90 days."
    ],
    [
        "Google BigQuery Service Agent",
        "roles/cloudkms.cryptoKeyEncrypterDecrypter",
        "Cloud Key Management Service CryptoKey: habotconnect-bigquery-encryption-key",
        "None (Service Agent role for CMEK encryption)",
        "Not Applicable (Cryptographic Keyring level)",
        "Encrypts and decrypts staged data warehouse partitions using Customer-Managed Encryption Keys.",
        "Storage and database keys are isolated into separate CryptoKey resources to prevent blast-radius crossover."
    ]
]

ws3.append(headers3)
for row in rows3:
    ws3.append(row)

# ------------------------------------------------------------------------------
# Sheet 4: Poka-Yoke Pipeline Gates
# ------------------------------------------------------------------------------
ws4 = wb.create_sheet(title="Poka-Yoke Pipeline Gates")
ws4.views.sheetView[0].showGridLines = True

headers4 = [
    "Inspection Gate Number & Title",
    "Inspection Tooling & Engine",
    "Target Scope & Artifacts",
    "Fail-Closed Halt Trigger Condition",
    "Automated Quarantine & Remediation Action",
    "Underlying Golden Rule Enforced"
]

rows4 = [
    [
        "Gate 1: Static Secret & Credential Leakage Scanner",
        "Gitleaks Automated Action & Detect-Secrets Utility",
        "Complete Git revision history, commit diffs, configuration files, and application source code.",
        "Detection of raw unencrypted API secret keys, Google Cloud Platform service account JSON tokens, or Django secret keys.",
        "Immediately halts build execution; Tags commit as quarantined; Revokes temporary CI credentials; Emits security incident alert.",
        "Zero Tolerance for Credentials: No unencrypted secrets, private keys, or credentials may ever be committed to code repositories."
    ],
    [
        "Gate 2: Python Code Formatting & Deterministic Style Gate",
        "Black Formatting Engine, isort Import Sorter, and Flake8 Structural Linter",
        "All Python codebase files within the backend directory.",
        "Line length exceeding 100 characters, unused imports, wildcards, non-canonical indentation, or formatting variance.",
        "Rejects commit; Aborts pipeline before test execution; Prints precise file and line coordinates requiring auto-formatting.",
        "Structural Discipline: Code formatting must be 100 percent deterministic and machine-enforced without developer debate."
    ],
    [
        "Gate 3: Static Application Security Testing (SAST) & Dependency Audit",
        "Bandit Abstract Syntax Tree Security Scanner and pip-audit Dependency Auditor",
        "Application Python source code and locked requirements.txt dependency file.",
        "Detection of SQL injection patterns, insecure deserialization, weak cryptographic hashes, or unpatched CVE vulnerabilities.",
        "Halts deployment; Blocks artifact image creation; Generates Common Vulnerabilities and Exposures (CVE) quarantine report.",
        "Fail-Closed Security Posture: Insecure application patterns or vulnerable third-party libraries must never enter staging."
    ],
    [
        "Gate 4: Infrastructure as Code (IaC) Syntax & Security Gate",
        "HashiCorp Terraform CLI (fmt, validate) and Aquasecurity Tfsec Scanner",
        "All HashiCorp Configuration Language files within the terraform directory.",
        "Syntax invalidity, unformatted HCL, public bucket access permissions, or missing encryption key specifications.",
        "Blocks terraform plan execution; Prevents cloud state file mutation; Halts deployment pipeline immediately.",
        "Immutable Infrastructure Security: Cloud infrastructure must be mathematically verified against Least Privilege before provisioning."
    ],
    [
        "Gate 5: Automated Unit Tests & DCYN Boundary Enforcement",
        "Pytest Test Framework with Pytest-Django and Pytest-Coverage Plugins",
        "Unit test suites for DCYN logic library, DRF serializers, boundary calculations, and edge cases.",
        "Any test assertion failure, code coverage dropping below 90 percent, or unhandled validation exception.",
        "Fails build; Aborts pull request merge; Blocks promotion to staging environment.",
        "Zero Human Judgment: All input boundaries (age limits, phone formats, DCYN binary states) must be validated mathematically."
    ],
    [
        "Gate 6: Fail-Closed Quarantine & Incident Notification",
        "GitHub Actions Workflow Failure Handler (if: failure())",
        "Triggered upon failure of any preceding inspection gate (Gates 1 through 5).",
        "Exit code greater than zero on any prior quality or security inspection step.",
        "Quarantines commit hash; Records audit event; Discards compiled artifacts; Emits alert to DevOps and Security engineering leads.",
        "Poka-Yoke Mistake-Proofing: Defective code must be automatically halted and quarantined at the source before impacting staging."
    ],
    [
        "Gate 7: Pipeline Clearance & Staging Promotion Authorization",
        "GitHub Actions Pipeline Clearance Step (if: success())",
        "Downstream deployment runner and container image packaging.",
        "Executed strictly when 100 percent of prior gates succeed without warnings or soft-failures.",
        "Authorizes container build; Publishes verified image to Google Artifact Registry; Deploys to staging environment.",
        "Continuous Delivery Verification: Only commits that have demonstrated perfect compliance are permitted to reach cloud infrastructure."
    ]
]

ws4.append(headers4)
for row in rows4:
    ws4.append(row)

# ------------------------------------------------------------------------------
# Formatting & Styling Function: Wrap Text & Full Visibility
# ------------------------------------------------------------------------------
for ws in wb.worksheets:
    # Header styling
    for col_num in range(1, ws.max_column + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = cell_border
    
    ws.row_dimensions[1].height = 32

    # Data row styling
    for row_num in range(2, ws.max_row + 1):
        is_zebra = (row_num % 2 == 0)
        row_fill = zebra_fill if is_zebra else white_fill
        ws.row_dimensions[row_num].height = 42 # Generous height for wrapped text
        
        for col_num in range(1, ws.max_column + 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.font = Font(name="Calibri", size=10, color="2D3748")
            cell.fill = row_fill
            cell.border = cell_border
            # CRITICAL REQUIREMENT: Wrap Text Enabled for 100% Full Visibility
            cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # Calculate optimal column width with generous padding
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val = str(cell.value or "")
            lines = val.split("\n")
            for line in lines:
                if len(line) > max_len:
                    max_len = len(line)
        # Cap width between 24 and 48 for comfortable multi-line reading
        col_width = max(24, min(48, max_len + 4))
        ws.column_dimensions[col_letter].width = col_width

output_file = "docs/HabotConnect_Data_Schema_Mapping.xlsx"
wb.save(output_file)
print(f"Successfully generated {output_file} with Wrap Text enabled and Full Forms Only across 4 worksheets.")
