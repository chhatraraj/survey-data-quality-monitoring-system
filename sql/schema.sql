-- =====================================================
-- Survey Quality Monitoring System
-- Database Schema
-- Module: Projects
-- =====================================================

CREATE TABLE projects (
    project_id BIGSERIAL PRIMARY KEY,

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
        DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Module: Enumerators
-- =====================================================

CREATE TABLE enumerators (

    enumerator_id BIGSERIAL PRIMARY KEY,

    project_id BIGINT NOT NULL,

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