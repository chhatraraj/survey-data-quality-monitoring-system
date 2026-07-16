-- =====================================================
-- Survey Quality Monitoring System
-- Database Schema v1.0
-- PostgreSQL + PostGIS
-- =====================================================

-- =====================================================
-- Enable PostgreSQL Extensions
-- =====================================================

CREATE EXTENSION IF NOT EXISTS postgis;

-- =====================================================
-- TABLE: projects
-- Description:
-- Stores survey project information.
-- =====================================================

CREATE TABLE projects (

    project_id BIGSERIAL PRIMARY KEY,

    project_code VARCHAR(50) NOT NULL UNIQUE,

    project_name VARCHAR(255) NOT NULL,

    client_name VARCHAR(255) NOT NULL,

    description TEXT,

    target_interviews INTEGER NOT NULL
        CHECK (target_interviews >= 0),

    start_date DATE NOT NULL,

    end_date DATE,

    status VARCHAR(20) NOT NULL
        DEFAULT 'Planning',

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    is_deleted BOOLEAN NOT NULL
        DEFAULT FALSE,

    deleted_at TIMESTAMPTZ,

    deleted_by VARCHAR(100)
);
-- =====================================================
-- TABLE: survey_forms
-- Description:
-- Stores KoboToolbox survey forms associated with
-- survey projects.
-- =====================================================

CREATE TABLE survey_forms (

    form_id BIGSERIAL PRIMARY KEY,

    project_id BIGINT NOT NULL,

    form_code VARCHAR(50) NOT NULL UNIQUE,

    form_name VARCHAR(255) NOT NULL,

    kobo_form_id VARCHAR(255),

    version INTEGER NOT NULL
        DEFAULT 1
        CHECK (version >= 1),

    status VARCHAR(20) NOT NULL
        DEFAULT 'Active',

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_form_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
);

-- =====================================================
-- TABLE: enumerators
-- Description:
-- Stores field enumerator information.
-- =====================================================

CREATE TABLE enumerators (

    enumerator_id BIGSERIAL PRIMARY KEY,

    project_id BIGINT NOT NULL,

    employee_code VARCHAR(50) UNIQUE,

    name VARCHAR(150) NOT NULL,

    phone VARCHAR(20),

    district VARCHAR(100),

    province VARCHAR(100),

    status VARCHAR(20)
        DEFAULT 'Active',

    joined_at DATE,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_enumerator_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
);
-- =====================================================
-- TABLE: survey_responses
-- Description:
-- Stores every completed interview imported from
-- KoboToolbox or CSV.
-- =====================================================

CREATE TABLE survey_responses (

    response_id BIGSERIAL PRIMARY KEY,

    project_id BIGINT NOT NULL,

    form_id BIGINT NOT NULL,

    enumerator_id BIGINT NOT NULL,

    submission_time TIMESTAMPTZ NOT NULL,

    interview_duration_seconds INTEGER
        CHECK (interview_duration_seconds >= 0),

    latitude DOUBLE PRECISION,

    longitude DOUBLE PRECISION,

    location GEOGRAPHY(POINT,4326),

    household_id VARCHAR(100),

    respondent_age INTEGER
        CHECK (
            respondent_age IS NULL
            OR respondent_age BETWEEN 0 AND 120
        ),

    district VARCHAR(100),

    device_id VARCHAR(255),

    raw_data JSONB,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

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
-- Description:
-- Stores spatial boundaries (survey areas)
-- for each project.
-- =====================================================

CREATE TABLE geofences (

    geofence_id BIGSERIAL PRIMARY KEY,

    project_id BIGINT NOT NULL,

    geofence_name VARCHAR(255) NOT NULL,

    description TEXT,

    area GEOGRAPHY(POLYGON, 4326) NOT NULL,

    is_active BOOLEAN NOT NULL
        DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_geofence_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
);

-- =====================================================
-- Database Comments
-- =====================================================

COMMENT ON TABLE projects IS
'Stores survey project information.';

COMMENT ON TABLE enumerators IS
'Stores field enumerators assigned to survey projects.';

COMMENT ON TABLE survey_responses IS
'Stores completed survey interviews imported from KoboToolbox or CSV files.';

COMMENT ON TABLE geofences IS
'Stores survey boundaries used for spatial validation and geofencing.';

-- =====================================================
-- TABLE: quality_checks
-- Description:
-- Stores rule-based validation results for each survey
-- response.
-- =====================================================

CREATE TABLE quality_checks (

    quality_check_id BIGSERIAL PRIMARY KEY,

    response_id BIGINT NOT NULL,

    rule_name VARCHAR(150) NOT NULL,

    severity VARCHAR(20) NOT NULL,

    status VARCHAR(20) NOT NULL
        DEFAULT 'Open',

    message TEXT,

    checked_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_quality_response
        FOREIGN KEY (response_id)
        REFERENCES survey_responses(response_id)
        ON DELETE CASCADE
);

-- =====================================================
-- TABLE: anomaly_scores
-- Description:
-- Stores machine learning anomaly detection results.
-- One response can have multiple algorithm outputs.
-- =====================================================

CREATE TABLE anomaly_scores (

    anomaly_score_id BIGSERIAL PRIMARY KEY,

    response_id BIGINT NOT NULL,

    algorithm VARCHAR(100) NOT NULL,

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
-- Description:
-- Stores alerts generated from rule engine,
-- statistical analysis, or machine learning.
-- =====================================================

CREATE TABLE alerts (

    alert_id BIGSERIAL PRIMARY KEY,

    response_id BIGINT,

    alert_type VARCHAR(100) NOT NULL,

    priority VARCHAR(20) NOT NULL,

    status VARCHAR(20) NOT NULL
        DEFAULT 'Open',

    message TEXT NOT NULL,

    source VARCHAR(50) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

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
-- Description:
-- Stores daily project KPIs for reporting.
-- =====================================================

CREATE TABLE daily_progress (

    daily_progress_id BIGSERIAL PRIMARY KEY,

    project_id BIGINT NOT NULL,

    progress_date DATE NOT NULL,

    interviews_completed INTEGER NOT NULL,

    daily_target INTEGER NOT NULL,

    completion_percentage DOUBLE PRECISION NOT NULL,

    active_enumerators INTEGER NOT NULL,

    created_at TIMESTAMPTZ
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_progress_project
        FOREIGN KEY(project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
);
