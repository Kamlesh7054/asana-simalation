# Asana RL Environment - Seed Data Generator

A Python-based data generation tool that creates realistic seed data for reinforcement learning environments simulating enterprise Asana workspaces.

## 📋 Overview

This project generates a complete Asana workspace simulation for a B2B SaaS company with: 
- **7,500 employees** across 85 teams
- **550+ projects** spanning engineering, marketing, operations, and product
- **33,000+ tasks** with realistic metadata, due dates, and completion status
- **37,000+ comments** and activity streams
- Research-backed distributions matching real-world enterprise patterns

The generated data serves as training ground for AI agents learning to navigate and use project management tools. 

---

## 🎯 Key Features

- ✅ **Realistic Data**:  Names from US Census, job titles from LinkedIn taxonomy
- ✅ **Research-Based**: Completion rates, workload distributions based on industry studies
- ✅ **Temporal Consistency**: All timestamps logically ordered (tasks completed after creation, etc.)
- ✅ **Relational Integrity**: 100% valid foreign keys, no orphaned records
- ✅ **Edge Cases**: Includes overdue tasks, inactive users, archived projects
- ✅ **Configurable Scale**: Adjust employee count, team size, project volume

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Kamlesh7054/asana-seed-data. git
cd asana-seed-data

# 2. Install dependencies
pip install -r requirements. txt

# 3. (Optional) Set up OpenAI API key for enhanced content generation
cp .env
# Edit .env and add:  OPENAI_API_KEY=sk-your-key-here
```

### Generate Database

```bash
# Run the generator
python src/main.py

# Output will be created at: output/asana_simulation. sqlite
```

**Generation time:** ~5-10 minutes (7,500 users) without LLM, ~30-45 minutes with LLM enabled. 

---

## 📁 Project Structure

```
asana-seed-data/
├── src/
│   ├── main.py                 # Entry point - orchestrates generation
│   ├── config.py               # Configuration (employee count, date ranges)
│   ├── database.py             # SQLite database utilities
│   ├── generators/             # Data generation modules
│   │   ├── organizations.py    # Company/org generation
│   │   ├── teams.py            # Team creation
│   │   ├── users.py            # User/employee generation
│   │   ├── projects.py         # Project generation
│   │   ├── tasks.py            # Task generation
│   │   └── comments. py         # Comment/activity generation
│   ├── scrapers/               # External data sources
│   │   ├── names.py            # Census-based names
│   │   └── companies.py        # Company name patterns
│   └── utils/                  # Helper functions
│       ├── id_generator.py     # UUID generation
│       ├── date_utils.py       # Date/time utilities
│       └── llm_utils.py        # OpenAI API integration
├── schema.sql                  # Complete database schema (DDL)
├── validation_queries.sql      # SQL queries to validate output
├── requirements.txt            # Python dependencies
├── .env                        # Environment variable template
└── output/                     # Generated database (created on first run)
```

---

## ⚙️ Configuration

### Adjust Generation Parameters

Edit `src/config.py` to customize the dataset:

```python
# Organization sizing
TARGET_EMPLOYEE_COUNT = 7500    # Total users (500-10000)
NUM_TEAMS = 85                  # Number of teams
NUM_PROJECTS_PER_TEAM = 8       # Projects per team
TASKS_PER_PROJECT_RANGE = (20, 100)  # Min/max tasks per project

# Simulation dates
COMPANY_FOUNDING_DATE = "2019-01-15"
SIMULATION_CURRENT_DATE = "2026-01-07"

# Department distribution (percentages, must sum to 1.0)
DEPT_DISTRIBUTION = {
    "Engineering": 0.42,
    "Sales & Marketing": 0.28,
    "Operations": 0.18,
    "Product & Design": 0.12
}
```

**Recommendations:**
- **Quick testing:** `TARGET_EMPLOYEE_COUNT = 500` (~2 minutes)
- **Full dataset:** `TARGET_EMPLOYEE_COUNT = 7500` (~10 minutes)

### Enable LLM for Better Content Quality

For more realistic task/project names, add your OpenAI API key:

1. Get key from https://platform.openai.com/api-keys
2. Create `.env` file: `cp .env.example .env`
3. Add key:  `OPENAI_API_KEY=sk-proj-your-key-here`

**Without LLM:** Uses template-based generation (generic names like "Task 570")  
**With LLM:** Generates specific names ("Implement OAuth2 authentication", "Q1 Brand Refresh Campaign")

---

## 📊 Validate Generated Data

After generation, verify data quality:

```bash
# Run validation queries
sqlite3 output/asana_simulation.sqlite < validation_queries.sql

# Or query directly
sqlite3 output/asana_simulation.sqlite
```

**Sample queries:**
```sql
-- Summary statistics
SELECT 'Users' as entity, COUNT(*) as count FROM users
UNION ALL
SELECT 'Teams', COUNT(*) FROM teams
UNION ALL
SELECT 'Projects', COUNT(*) FROM projects
UNION ALL
SELECT 'Tasks', COUNT(*) FROM tasks;

-- Completion rate by project type
SELECT project_type, 
       ROUND(100.0 * SUM(completed) / COUNT(*), 2) as completion_pct
FROM tasks t
JOIN projects p ON t.project_id = p.project_id
GROUP BY project_type;

-- Task name variety check
SELECT name, COUNT(*) as occurrences 
FROM tasks 
GROUP BY name 
ORDER BY occurrences DESC 
LIMIT 10;
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `openai` | ≥1.0.0 | LLM-based content generation (optional) |
| `python-dotenv` | ≥1.0.0 | Environment variable management |
| `faker` | ≥20.0.0 | Fallback name generation |
| `numpy` | ≥1.24.0 | Statistical distributions (Pareto, log-normal) |
| `pandas` | ≥2.0.0 | Data manipulation |
| `requests` | ≥2.31.0 | HTTP requests (future scraping features) |

Install all with:  `pip install -r requirements.txt`

---

## 🎓 Database Schema Highlights

### Core Tables

| Table | Records | Description |
|-------|---------|-------------|
| `organizations` | 1 | Top-level workspace |
| `teams` | 85 | Cross-functional teams (Engineering, Sales, etc.) |
| `users` | ~7,500 | Employees with realistic names, emails, job titles |
| `team_memberships` | ~7,500 | User-team associations |
| `projects` | ~550 | Sprint/campaign/initiative projects |
| `sections` | ~2,750 | Kanban columns ("To Do", "In Progress", "Done") |
| `tasks` | ~33,000 | Work items with due dates, assignees, priorities |
| `comments` | ~37,000 | User comments + system activity |

### Key Design Decisions

- **Email Uniqueness:** Handles duplicate names (john.smith2@company.com)
- **Task Hierarchy:** Self-referential `parent_task_id` for subtasks
- **Temporal Consistency:** All timestamps logically ordered (no time travel)
- **Pareto Distribution:** Top 20% of users own 50% of tasks (realistic workload)

Full schema:  See `schema.sql`

---

## 📈 Expected Output

### Actual Generated Data (Without LLM)

```
Organizations:  1
Teams: 85
Users: 7,488
Projects: 556
Tasks: 33,208
Comments: 37,283

Department Distribution:
  Engineering: 3,145 users (42.0%)
  Sales & Marketing: 2,093 users (27.9%)
  Operations: 1,350 users (18.0%)
  Product & Design: 900 users (12.0%)

Completion Rates:
  Sprint projects: 73.3%
  Campaign projects: 63.1%
  Ongoing projects: 44.3%

Due Dates:  25.1% have no due date (realistic backlog)
```

---

## 🐛 Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution:** Either add key to `.env` or run without LLM (uses templates).

### Issue: "UNIQUE constraint failed:  users.email"
**Solution:** Already fixed - uses collision resolution (john.smith2@).

### Issue: Database generation is slow
**Solution:** 
- Reduce `TARGET_EMPLOYEE_COUNT` in `config.py`
- Disable LLM (comment out `OPENAI_API_KEY` in `.env`)

### Issue: ModuleNotFoundError
**Solution:** Ensure all dependencies installed:  `pip install -r requirements.txt`

---

## 📚 Research & Methodology

Data generation based on:
- **Name distributions:** US Census Bureau data
- **Completion rates:** Asana "Anatomy of Work" Index 2024
- **Team structures:** LinkedIn Workforce Report, Radford Tech Survey
- **Task patterns:** Analysis of 500+ GitHub issues, Asana templates
- **Cycle times:** DORA State of DevOps Report (median 3-7 days)

Full methodology: See `DOCUMENTATION.md` (if included in repo)

---

## 📄 License

MIT License - See LICENSE file for details. 

---

## 👤 Author

**Kamlesh7054**  
GitHub: [@Kamlesh7054](https://github.com/Kamlesh7054)

---

## 🤝 Contributing

Contributions welcome!  Please: 
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub:  https://github.com/Kamlesh7054/asana-seed-data/issues
- Review validation queries in `validation_queries.sql`

---

**Generated with ❤️ for RL research in enterprise software automation**
