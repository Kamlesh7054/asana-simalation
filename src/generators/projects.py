from utils.id_generator import generate_id
from utils.date_utils import random_date_between
from utils.llm_utils import generate_with_llm
from config import NUM_PROJECTS_PER_TEAM, SIMULATION_CURRENT_DATE
import random
from datetime import datetime, timedelta

PROJECT_COLORS = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "gray"]

def generate_project_name_llm(department: str, project_type: str, team_name: str) -> str:
    """Generate realistic project name using LLM"""
    prompt = f"""Generate a realistic project name for a {department} team called "{team_name}". 
Project type: {project_type}
Examples for Engineering: "Q1 2026 Sprint 3", "Payment Gateway Integration", "Mobile App Performance"
Examples for Marketing: "Product Launch Campaign Q1", "SEO Optimization Initiative", "Brand Refresh 2026"
Return only the project name, no explanation."""
    
    return generate_with_llm(prompt, temperature=0.9)

def generate_projects(teams: list[dict], users: list[dict], use_llm: bool = True) -> tuple[list[dict], list[dict]]:
    """Generate projects and sections"""
    projects = []
    sections = []
    
    PROJECT_NAMES = {
        "Engineering": ["Q1 Sprint", "Infrastructure Update", "Performance Optimization", "API Redesign", "Mobile Refactor"],
        "Sales & Marketing": ["Q1 Campaign", "Product Launch", "Lead Generation", "Brand Refresh", "Content Strategy"],
        "Operations": ["Process Improvement", "System Upgrade", "Team Training", "Policy Update", "Audit"],
        "Product & Design": ["Design System", "User Research", "Prototyping", "UX Audit", "Feature Design"]
    }
    
    for team in teams:
        department = team["department"]
        num_projects = random.randint(5, NUM_PROJECTS_PER_TEAM)
        
        for _ in range(num_projects):
            # Determine project type based on department
            if department == "Engineering":
                project_type = random.choices(
                    ["sprint", "ongoing", "initiative"],
                    weights=[0.6, 0.3, 0.1]
                )[0]
            elif department == "Sales & Marketing": 
                project_type = random.choices(
                    ["campaign", "ongoing"],
                    weights=[0.7, 0.3]
                )[0]
            else: 
                project_type = random.choice(["initiative", "ongoing"])
            
            # Generate name
            if use_llm:
                project_name = generate_project_name_llm(department, project_type, team["name"])
            else:
                base_name = random.choice(PROJECT_NAMES.get(department, ["Project"]))
                project_name = f"{base_name} {random.randint(1, 5)}"
            
            # Status
            status = random.choices(
                ["active", "archived", "on_hold"],
                weights=[0.85, 0.10, 0.05]
            )[0]
            
            # Dates
            created_at = random_date_between(team["created_at"], SIMULATION_CURRENT_DATE)
            created_dt = datetime.fromisoformat(created_at)
            
            if project_type == "sprint":
                start_date = created_dt.date().isoformat()
                due_date = (created_dt + timedelta(days=14)).date().isoformat()
            elif project_type == "campaign":
                start_date = created_dt.date().isoformat()
                due_date = (created_dt + timedelta(days=random.randint(28, 56))).date().isoformat()
            else:
                start_date = None
                due_date = None
            
            # Owner (random team member)
            team_members = [u["user_id"] for u in users if u["department"] == department]
            owner_id = random.choice(team_members) if team_members else None
            
            project_id = generate_id()
            
            # Generate description
            if use_llm:
                description = generate_with_llm(f"Write a 2-sentence project description for: {project_name}")
            else:
                description = f"Project for {department} team"
            
            projects.append({
                "project_id": project_id,
                "team_id": team["team_id"],
                "name": project_name,
                "description": description,
                "project_type": project_type,
                "status": status,
                "owner_id": owner_id,
                "start_date": start_date,
                "due_date": due_date,
                "created_at": created_at,
                "archived_at": None,
                "color": random.choice(PROJECT_COLORS),
                "privacy": "public"
            })
            
            # Generate sections
            if department == "Engineering":
                section_names = ["Backlog", "To Do", "In Progress", "Code Review", "Done"]
            elif department == "Sales & Marketing":
                section_names = ["Planning", "In Progress", "Review", "Completed"]
            else:
                section_names = ["To Do", "In Progress", "Done"]
            
            for position, section_name in enumerate(section_names):
                sections.append({
                    "section_id": generate_id(),
                    "project_id": project_id,
                    "name": section_name,
                    "position": position,
                    "created_at": created_at
                })
    
    return projects, sections