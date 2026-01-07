-- validation_queries.sql
-- Query to validate the generated data

.headers on
.mode column

SELECT '=== DATABASE SUMMARY ===' as Info;
SELECT '';

SELECT 'Organizations' as Entity, COUNT(*) as Count FROM organizations
UNION ALL
SELECT 'Teams', COUNT(*) FROM teams
UNION ALL
SELECT 'Users', COUNT(*) FROM users
UNION ALL
SELECT 'Projects', COUNT(*) FROM projects
UNION ALL
SELECT 'Tasks', COUNT(*) FROM tasks
UNION ALL
SELECT 'Comments', COUNT(*) FROM comments;

SELECT '';
SELECT '=== DEPARTMENT DISTRIBUTION ===' as Info;
SELECT '';

SELECT department, COUNT(*) as user_count 
FROM users 
GROUP BY department 
ORDER BY user_count DESC;

SELECT '';
SELECT '=== SAMPLE TASKS ===' as Info;
SELECT '';

SELECT 
    t.name as task_name, 
    p.name as project_name,
    t.priority, 
    t.completed, 
    t.due_date 
FROM tasks t
JOIN projects p ON t.project_id = p.project_id
LIMIT 15;

SELECT '';
SELECT '=== TASK NAME VARIETY CHECK ===' as Info;
SELECT '';

SELECT name, COUNT(*) as occurrences 
FROM tasks 
GROUP BY name 
ORDER BY occurrences DESC 
LIMIT 10;

SELECT '';
SELECT '=== COMPLETION RATE BY PROJECT TYPE ===' as Info;
SELECT '';

SELECT 
    p.project_type,
    COUNT(*) as total_tasks,
    SUM(CASE WHEN t.completed = 1 THEN 1 ELSE 0 END) as completed_tasks,
    ROUND(CAST(SUM(CASE WHEN t.completed = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as completion_percentage
FROM tasks t
JOIN projects p ON t. project_id = p.project_id
GROUP BY p.project_type;

SELECT '';
SELECT '=== DUE DATE DISTRIBUTION ===' as Info;
SELECT '';

SELECT 
    COUNT(*) as total_tasks,
    SUM(CASE WHEN due_date IS NULL THEN 1 ELSE 0 END) as no_due_date,
    SUM(CASE WHEN due_date IS NOT NULL THEN 1 ELSE 0 END) as has_due_date,
    ROUND(CAST(SUM(CASE WHEN due_date IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as pct_no_due_date
FROM tasks;

SELECT '';
SELECT '=== SAMPLE USERS ===' as Info;
SELECT '';

SELECT first_name, last_name, job_title, department 
FROM users 
LIMIT 10;