-- schema.sql

-- Organizations/Workspaces
CREATE TABLE organizations (
    org_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    org_type TEXT CHECK(org_type IN ('workspace', 'organization')) DEFAULT 'organization'
);

-- Teams
CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    department TEXT NOT NULL, -- Engineering, Marketing, Sales, Operations, Product
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- Users
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    job_title TEXT,
    department TEXT,
    profile_photo_url TEXT,
    created_at TIMESTAMP NOT NULL,
    last_active TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- Team Memberships
CREATE TABLE team_memberships (
    membership_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT CHECK(role IN ('member', 'admin', 'owner')) DEFAULT 'member',
    joined_at TIMESTAMP NOT NULL,
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(team_id, user_id)
);

-- Projects
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    project_type TEXT, -- sprint, ongoing, campaign, initiative
    status TEXT CHECK(status IN ('active', 'archived', 'on_hold')) DEFAULT 'active',
    owner_id TEXT,
    start_date DATE,
    due_date DATE,
    created_at TIMESTAMP NOT NULL,
    archived_at TIMESTAMP,
    color TEXT, -- Asana uses colors for projects
    privacy TEXT CHECK(privacy IN ('public', 'private')) DEFAULT 'public',
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

-- Sections (columns within projects)
CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    position INTEGER NOT NULL, -- order within project
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Tasks
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT,
    parent_task_id TEXT, -- NULL for top-level tasks, non-NULL for subtasks
    name TEXT NOT NULL,
    description TEXT,
    assignee_id TEXT,
    due_date DATE,
    start_date DATE,
    created_at TIMESTAMP NOT NULL,
    created_by TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    completed_by TEXT,
    priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
    num_likes INTEGER DEFAULT 0,
    num_subtasks INTEGER DEFAULT 0,
    num_comments INTEGER DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id),
    FOREIGN KEY (completed_by) REFERENCES users(user_id)
);

-- Comments/Stories
CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    comment_text TEXT NOT NULL,
    comment_type TEXT CHECK(comment_type IN ('comment', 'system')) DEFAULT 'comment',
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Custom Field Definitions
CREATE TABLE custom_field_definitions (
    field_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    field_name TEXT NOT NULL,
    field_type TEXT CHECK(field_type IN ('text', 'number', 'dropdown', 'date', 'checkbox')) NOT NULL,
    description TEXT,
    options TEXT, -- JSON array for dropdown options
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Custom Field Values
CREATE TABLE custom_field_values (
    value_id TEXT PRIMARY KEY,
    field_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    value TEXT, -- Stores value as text, can be parsed based on field_type
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    UNIQUE(field_id, task_id)
);

-- Tags
CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- Task-Tag Association
CREATE TABLE task_tags (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    added_at TIMESTAMP NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

-- Attachments
CREATE TABLE attachments (
    attachment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT, -- pdf, png, doc, etc.
    file_size INTEGER, -- in bytes
    url TEXT,
    uploaded_by TEXT NOT NULL,
    uploaded_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
);

-- Indexes for common queries
CREATE INDEX idx_users_org ON users(org_id);
CREATE INDEX idx_teams_org ON teams(org_id);
CREATE INDEX idx_projects_team ON projects(team_id);
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_assignee ON tasks(assignee_id);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_comments_task ON comments(task_id);