-- Example SQL queries

-- Query 1: Get current database version
SELECT version();

-- Query 2: List all tables in the current schema
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- Query 3: Example users table query
-- SELECT id, username, email, created_at 
-- FROM users 
-- WHERE active = true 
-- ORDER BY created_at DESC 
-- LIMIT 10;
