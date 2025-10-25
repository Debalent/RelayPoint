-- Initialize PostgreSQL database for development
-- This script runs when the container is first created

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "hstore";

-- Create test data (optional)
-- Uncomment and modify as needed for your development environment

/*
-- Create test users
INSERT INTO users (id, email, hashed_password, full_name, is_active, is_superuser)
VALUES 
    (uuid_generate_v4(), 'admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Admin User', true, true),
    (uuid_generate_v4(), 'user@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Regular User', true, false);
*/

-- Add any other initialization SQL here