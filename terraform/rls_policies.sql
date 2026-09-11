-- ==============================================================================
-- Habot Connect FZCO — Google BigQuery Row-Level Security (RLS) Policies
-- Dataset: habotconnect_d1_staged_enforced
-- Table: student_onboarding_staged
-- Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
-- Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Policy 1: Learning Support Assistant (LSA) Isolation Policy
-- Purpose: Restricts Learning Support Assistants so they can strictly query
--          rows where their authenticated identity matches the assigned LSA ID.
-- ------------------------------------------------------------------------------
CREATE OR REPLACE ROW ACCESS POLICY lsa_assigned_students_isolation
ON `habotconnect-staging-2026.habotconnect_d1_staged_enforced.student_onboarding_staged`
GRANT TO ('group:learning-support-assistants@habotconnect.internal')
FILTER USING (
    assigned_learning_support_assistant_identifier = SESSION_USER()
);

-- ------------------------------------------------------------------------------
-- Policy 2: Regional Educational Coordinator District Isolation Policy
-- Purpose: Restricts regional supervisors to their specific municipal jurisdiction
--          (for example: Dubai, Abu Dhabi, Sharjah).
-- ------------------------------------------------------------------------------
CREATE OR REPLACE ROW ACCESS POLICY regional_coordinator_district_isolation
ON `habotconnect-staging-2026.habotconnect_d1_staged_enforced.student_onboarding_staged`
GRANT TO ('group:regional-coordinators@habotconnect.internal')
FILTER USING (
    regional_jurisdiction IN (
        SELECT authorized_jurisdiction
        FROM `habotconnect-staging-2026.habotconnect_d1_staged_enforced.coordinator_jurisdiction_mapping`
        WHERE coordinator_email_address = SESSION_USER()
    )
);

-- ------------------------------------------------------------------------------
-- Policy 3: Compliance & Legal Audit Full Unconstrained Access
-- Purpose: Grants legal and medical compliance auditors complete visibility
--          for audit compliance, data subject access requests, and quality control.
-- ------------------------------------------------------------------------------
CREATE OR REPLACE ROW ACCESS POLICY compliance_officer_full_audit
ON `habotconnect-staging-2026.habotconnect_d1_staged_enforced.student_onboarding_staged`
GRANT TO ('group:compliance-officers@habotconnect.internal')
FILTER USING (
    TRUE
);

-- ------------------------------------------------------------------------------
-- Verification Query: Asserting Filter Isolation
-- When executed by an LSA (e.g. lsa.sarah@habotconnect.internal):
-- ------------------------------------------------------------------------------
-- SELECT
--     student_unique_identifier,
--     student_full_name,
--     assigned_learning_support_assistant_identifier,
--     regional_jurisdiction,
--     dcyn_requires_one_on_one_support
-- FROM
--     `habotconnect-staging-2026.habotconnect_d1_staged_enforced.student_onboarding_staged`;
-- Expected Result: Only records where assigned_learning_support_assistant_identifier = 'lsa.sarah@habotconnect.internal'
