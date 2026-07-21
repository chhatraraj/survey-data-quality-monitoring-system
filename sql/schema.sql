-- =====================================================
-- Survey Quality Monitoring System
-- Database Schema v1.3
-- PostgreSQL + PostGIS
-- =====================================================

-- =====================================================
-- Enable PostgreSQL Extensions
-- =====================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS postgis;


-- =====================================================
-- PostgreSQL Enum Types
-- Must match src/utils/enums.py exactly
-- =====================================================

CREATE TYPE projectstatus AS ENUM (
    'Planning',
    'Active',
    'Completed',
    'Paused',
    'Cancelled'
);

CREATE TYPE enumeratorstatus AS ENUM (
    'Active',
    'Inactive',
    'Training',
    'Suspended'
);

CREATE TYPE severitylevel AS ENUM (
    'Low',
    'Medium',
    'High',
    'Critical'
);

CREATE TYPE alertpriority AS ENUM (
    'Low',
    'Medium',
    'High',
    'Critical'
);

CREATE TYPE alertstatus AS ENUM (
    'Open',
    'Investigating',
    'Resolved',
    'Closed'
);

CREATE TYPE alerttype AS ENUM (
    'Missing GPS',
    'Duplicate Household',
    'Speeder',
    'Project Delay',
    'Inactive Enumerator',
    'Outside Geofence',
    'ML Anomaly',
    'Duplicate Device'
);

CREATE TYPE mlalgorithm AS ENUM (
    'Isolation Forest',
    'Local Outlier Factor',
    'ECOD',
    'COPOD',
    'KNN'
);


-- =====================================================
-- TABLE: projects
-- Description: Stores survey project information.
-- =====================================================

CREATE TABLE projects (
    project_id BIGSERIAL PRIMARY KEY,
    project_code VARCHAR(50) NOT NULL UNIQUE,
    project_name VARCHAR(255) NOT NULL UNIQUE,
    client_name VARCHAR(255) NOT NULL,
    description TEXT,
    target_interviews INTEGER NOT NULL CHECK (target_interviews >= 0),
    start_date DATE NOT NULL,
    end_date DATE,
    status projectstatus NOT NULL DEFAULT 'Planning',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMPTZ,
    deleted_by VARCHAR(100)
);

-- =====================================================
-- TABLE: survey_forms
-- Description: Stores survey forms associated with projects.
-- =====================================================

CREATE TABLE survey_forms (
    form_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL,
    form_name VARCHAR(255) NOT NULL,
    form_version VARCHAR(50),
    kobo_form_id VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_form_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
);

-- =====================================================
-- TABLE: enumerators
-- Description: Stores field enumerator information.
-- =====================================================

CREATE TABLE enumerators (
    enumerator_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL,
    employee_code VARCHAR(50) UNIQUE,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    district VARCHAR(100),
    province VARCHAR(100),
    status enumeratorstatus NOT NULL DEFAULT 'Active',
    joined_at DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_enumerator_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
);

-- =====================================================
-- TABLE: survey_responses
-- Description: Stores completed interview records.
-- =====================================================

CREATE TABLE survey_responses (
    response_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL,
    form_id BIGINT NOT NULL,
    enumerator_id BIGINT NOT NULL,
    submission_time TIMESTAMPTZ NOT NULL,
    interview_duration_seconds INTEGER CHECK (interview_duration_seconds >= 0),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    location GEOGRAPHY(POINT, 4326),
    household_id VARCHAR(100),
    respondent_age INTEGER CHECK (
        respondent_age IS NULL OR respondent_age BETWEEN 0 AND 120
    ),
    district VARCHAR(100),
    device_id VARCHAR(255),
    raw_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_response_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_response_form
        FOREIGN KEY (form_id)
        REFERENCES survey_forms(form_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_response_enumerator
        FOREIGN KEY (enumerator_id)
        REFERENCES enumerators(enumerator_id)
        ON DELETE CASCADE
);

-- =====================================================
-- TABLE: geofences
-- Description: Stores spatial boundaries for geofencing.
-- =====================================================

CREATE TABLE geofences (
    geofence_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL,
    geofence_name VARCHAR(255) NOT NULL,
    description TEXT,
    area GEOGRAPHY(POLYGON, 4326) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_geofence_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
);

-- =====================================================
-- TABLE: quality_checks
-- Description: Stores rule-based validation results.
-- =====================================================

CREATE TABLE quality_checks (
    quality_check_id BIGSERIAL PRIMARY KEY,
    response_id BIGINT NOT NULL,
    rule_name VARCHAR(150) NOT NULL,
    severity severitylevel NOT NULL,
    message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_quality_response
        FOREIGN KEY (response_id)
        REFERENCES survey_responses(response_id)
        ON DELETE CASCADE
);

-- =====================================================
-- TABLE: anomaly_scores
-- Description: Stores ML anomaly detection outputs.
-- =====================================================

CREATE TABLE anomaly_scores (
    anomaly_score_id BIGSERIAL PRIMARY KEY,
    response_id BIGINT NOT NULL,
    algorithm mlalgorithm NOT NULL,
    anomaly_score DOUBLE PRECISION NOT NULL,
    prediction BOOLEAN NOT NULL,
    model_version VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_anomaly_response
        FOREIGN KEY (response_id)
        REFERENCES survey_responses(response_id)
        ON DELETE CASCADE
);

-- =====================================================
-- TABLE: alerts
-- Description: Stores system alerts generated by rules.
-- =====================================================

CREATE TABLE alerts (
    alert_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL,
    response_id BIGINT,
    alert_type alerttype NOT NULL,
    priority alertpriority NOT NULL,
    status alertstatus NOT NULL DEFAULT 'Open',
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMPTZ,
    CONSTRAINT fk_alert_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_alert_response
        FOREIGN KEY (response_id)
        REFERENCES survey_responses(response_id)
        ON DELETE SET NULL
);

-- =====================================================
-- TABLE: daily_progress
-- Description: Stores daily project reporting metrics.
-- =====================================================

CREATE TABLE daily_progress (
    daily_progress_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL,
    progress_date DATE NOT NULL,
    interviews_completed INTEGER NOT NULL,
    daily_target INTEGER NOT NULL,
    completion_percentage DOUBLE PRECISION NOT NULL,
    active_enumerators INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_progress_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
);

-- =====================================================
-- Performance Indexes (Foreign Keys)
-- =====================================================

CREATE INDEX idx_survey_forms_project ON survey_forms(project_id);
CREATE INDEX idx_enumerators_project ON enumerators(project_id);

CREATE INDEX idx_survey_responses_project ON survey_responses(project_id);
CREATE INDEX idx_survey_responses_form ON survey_responses(form_id);
CREATE INDEX idx_survey_responses_enumerator ON survey_responses(enumerator_id);

CREATE INDEX idx_geofences_project ON geofences(project_id);
CREATE INDEX idx_quality_checks_response ON quality_checks(response_id);
CREATE INDEX idx_anomaly_scores_response ON anomaly_scores(response_id);

CREATE INDEX idx_alerts_project ON alerts(project_id);
CREATE INDEX idx_alerts_response ON alerts(response_id);
CREATE INDEX idx_daily_progress_project ON daily_progress(project_id);

-- =====================================================
-- PostGIS Spatial Indexes
-- =====================================================

CREATE INDEX idx_survey_responses_location ON survey_responses USING GIST(location);
CREATE INDEX idx_geofences_area ON geofences USING GIST(area);

-- =====================================================
-- Database Comments
-- =====================================================

COMMENT ON TABLE projects IS 'Stores survey project information.';
COMMENT ON TABLE survey_forms IS 'Stores survey forms associated with projects.';
COMMENT ON TABLE enumerators IS 'Stores field enumerators assigned to survey projects.';
COMMENT ON TABLE survey_responses IS 'Stores completed survey interviews imported from KoboToolbox or CSV files.';
COMMENT ON TABLE geofences IS 'Stores survey boundaries used for spatial validation and geofencing.';
COMMENT ON TABLE quality_checks IS 'Stores rule-based validation results for each survey response.';
COMMENT ON TABLE anomaly_scores IS 'Stores machine learning anomaly detection outputs.';
COMMENT ON TABLE alerts IS 'Stores system alerts generated by rules or statistical analysis.';
COMMENT ON TABLE daily_progress IS 'Stores daily project KPIs for reporting.';