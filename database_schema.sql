-- ====================================================================================
-- Web-Based Asset Risk Management System
-- MySQL Database Schema
--
-- Note: This schema is designed to align with the frontend HTML wireframes and
-- will be used with a Python backend when implemented.
-- ====================================================================================

-- Create a database (uncomment if needed)
-- CREATE DATABASE IF NOT EXISTS risksys_db;
-- USE risksys_db;

-- --------------------------------------------------------
-- 1. Users Table
-- Supports login and role-based access control (Admin / Read-Only).
-- --------------------------------------------------------
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL, -- To store hashed passwords
    full_name VARCHAR(100) NOT NULL,
    role ENUM('Admin', 'Read-Only') DEFAULT 'Read-Only',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- --------------------------------------------------------
-- 2. Assets Table
-- Captures IT, OT, and Infrastructure assets with ISO 27001 requirements.
-- --------------------------------------------------------
CREATE TABLE assets (
    asset_id INT AUTO_INCREMENT PRIMARY KEY,
    asset_name VARCHAR(150) NOT NULL,
    asset_description TEXT,
    asset_category ENUM('IT', 'OT', 'Infrastructure') NOT NULL,
    operational_status ENUM('Active', 'Maintenance', 'Retired') DEFAULT 'Active',
    
    -- ISO 27001 Information Classification
    classification ENUM('Public', 'Internal', 'Confidential', 'Restricted'),
    cia_confidentiality ENUM('Low', 'Medium', 'High'),
    cia_integrity ENUM('Low', 'Medium', 'High'),
    cia_availability ENUM('Low', 'Medium', 'High'),
    
    asset_owner VARCHAR(100) NOT NULL,
    location VARCHAR(150),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- --------------------------------------------------------
-- 3. Risks Table
-- Links to assets and calculates ratings based on Likelihood and Impact.
-- --------------------------------------------------------
CREATE TABLE risks (
    risk_id INT AUTO_INCREMENT PRIMARY KEY,
    asset_id INT NOT NULL,
    risk_description TEXT NOT NULL,
    
    likelihood INT NOT NULL CHECK (likelihood BETWEEN 1 AND 5),
    impact INT NOT NULL CHECK (impact BETWEEN 1 AND 5),
    risk_rating INT GENERATED ALWAYS AS (likelihood * impact) STORED,
    
    -- ISO 27001 Requirements
    risk_treatment ENUM('Modify', 'Retain', 'Avoid', 'Share') NOT NULL,
    
    review_date DATE,
    risk_status ENUM('Open', 'Mitigated', 'Closed') DEFAULT 'Open',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE
);

-- --------------------------------------------------------
-- 4. Risk Controls Table
-- Allows for multiple Annex A Controls (A.5, A.8, A.9, etc.) per risk.
-- --------------------------------------------------------
CREATE TABLE risk_controls (
    risk_control_id INT AUTO_INCREMENT PRIMARY KEY,
    risk_id INT NOT NULL,
    control_code VARCHAR(50) NOT NULL, -- e.g., 'A.5', 'A.8'
    FOREIGN KEY (risk_id) REFERENCES risks(risk_id) ON DELETE CASCADE
);

-- --------------------------------------------------------
-- 5. Mitigations Table
-- Action items meant to address or reduce identified risks.
-- --------------------------------------------------------
CREATE TABLE mitigations (
    mitigation_id INT AUTO_INCREMENT PRIMARY KEY,
    risk_id INT NOT NULL,
    action_description TEXT NOT NULL,
    assigned_to INT NOT NULL, -- Links to 'user_id' in users table
    
    target_date DATE,
    progress_status ENUM('Not Started', 'In Progress', 'Completed') DEFAULT 'Not Started',
    comments TEXT,
    
    -- ISO 27001 Evaluation
    effectiveness_review_date DATE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (risk_id) REFERENCES risks(risk_id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(user_id)
);

-- --------------------------------------------------------
-- 6. Audit Logs Table
-- Immutable system trail for actions (auditing & compliance).
-- --------------------------------------------------------
CREATE TABLE audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT, -- Can be NULL if the action wasn't tied to a specific user (e.g., system logic fallback)
    action_type ENUM('CREATE', 'UPDATE', 'DELETE', 'LOGIN') NOT NULL,
    entity_name VARCHAR(50) NOT NULL, -- e.g., 'Asset', 'Risk', 'Mitigation', 'User Session'
    entity_id VARCHAR(50), -- Variable depending on the entity primary key Type (INT disguised as VARCHAR for flexibility)
    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action_details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- --------------------------------------------------------
-- 7. Recommended Indexes (for reporting and filtering)
-- --------------------------------------------------------

-- Risk and asset lookups / filters
CREATE INDEX idx_risks_asset_status ON risks (asset_id, risk_status);

-- Mitigation lookups for reporting (by risk and overdue status)
CREATE INDEX idx_mitigations_risk_target_status
    ON mitigations (risk_id, target_date, progress_status);

-- Audit log filtering (user, type, date)
CREATE INDEX idx_audit_logs_user_type_date
    ON audit_logs (user_id, action_type, action_date);

-- ====================================================================================
-- Initial Seed Data (Optional for testing the application structure)
-- ====================================================================================

-- Insert sample users
INSERT INTO users (username, password_hash, full_name, role) VALUES 
('admin', 'hashed_pass_placeholder', 'Admin User', 'Admin'),
('viewer', 'hashed_pass_placeholder', 'Read-Only User', 'Read-Only');
