import os
from dotenv import load_dotenv

load_dotenv()

# Database
DB_PATH = "output/asana_simulation.sqlite"

# Organization sizing (5000-10000 employees)
TARGET_EMPLOYEE_COUNT = 7500
NUM_TEAMS = 85  # Average 88 people per team
NUM_PROJECTS_PER_TEAM = 8  # Mix of active and archived
TASKS_PER_PROJECT_RANGE = (20, 100)

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = "gpt-4o-mini"  # Cost-effective for generation
LLM_TEMPERATURE = 0.8  # Variety in output

# Date Configuration
COMPANY_FOUNDING_DATE = "2019-01-15"
SIMULATION_CURRENT_DATE = "2026-01-07"

# Department Distribution (percentages)
DEPT_DISTRIBUTION = {
    "Engineering": 0.42,
    "Sales & Marketing": 0.28,
    "Operations": 0.18,
    "Product & Design": 0.12
}