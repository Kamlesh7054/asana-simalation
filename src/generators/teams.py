from utils.id_generator import generate_id
from utils.date_utils import random_date_between
from config import COMPANY_FOUNDING_DATE, SIMULATION_CURRENT_DATE, NUM_TEAMS, DEPT_DISTRIBUTION
import random

TEAM_TEMPLATES = {
    "Engineering": [
        "Backend Engineering", "Frontend Engineering", "Mobile iOS", "Mobile Android",
        "Platform Infrastructure", "DevOps", "QA & Testing", "Security Engineering",
        "Data Engineering", "Machine Learning", "API Services", "Cloud Infrastructure",
        "Site Reliability Engineering", "Core Platform", "Developer Tools", "Automation Engineering"
    ],
    "Sales & Marketing": [
        "Growth Marketing", "Content Marketing", "Product Marketing", "Brand & Creative",
        "Sales Development", "Enterprise Sales", "Customer Success", "Demand Generation",
        "Marketing Operations", "Sales Operations", "Field Marketing", "Digital Marketing",
        "Account Management", "Partnership Development"
    ],
    "Operations": [
        "Human Resources", "Finance & Accounting", "Legal & Compliance", "IT Support",
        "Facilities", "People Operations", "Business Operations", "Talent Acquisition",
        "Financial Planning & Analysis", "Corporate Development"
    ],
    "Product & Design": [
        "Product Management", "UX Research", "UI/UX Design", "Product Analytics",
        "Design Systems", "Product Strategy", "Visual Design", "Interaction Design"
    ]
}

def generate_teams(org_id: str, num_teams: int = NUM_TEAMS) -> list:
    """Generate teams distributed across departments"""
    teams = []
    
    # Calculate teams per department based on distribution
    dept_team_counts = {
        dept: max(1, int(num_teams * percentage))  # Ensure at least 1 team per department
        for dept, percentage in DEPT_DISTRIBUTION.items()
    }
    
    # Adjust for rounding errors - ensure we generate exactly num_teams
    total_assigned = sum(dept_team_counts.values())
    if total_assigned < num_teams:
        # Add remaining teams to Engineering (largest department)
        dept_team_counts["Engineering"] += (num_teams - total_assigned)
    elif total_assigned > num_teams: 
        # Remove excess teams from Engineering
        dept_team_counts["Engineering"] -= (total_assigned - num_teams)
    
    print(f"   Generating teams by department:")
    for dept, count in dept_team_counts.items():
        print(f"      {dept}: {count} teams")
    
    # Generate teams for each department
    for department, count in dept_team_counts.items():
        available_names = TEAM_TEMPLATES[department]. copy()
        
        # Shuffle for variety
        random.shuffle(available_names)
        
        for i in range(count):
            if available_names:
                name = available_names.pop(0)
            else:
                # Fallback naming when we run out of templates
                name = f"{department} Team {i - len(TEAM_TEMPLATES[department]) + 1}"
            
            # More varied descriptions
            descriptions = [
                f"{department} team focused on {name. lower()}",
                f"Responsible for {name.lower()} initiatives",
                f"Dedicated {department. lower()} team handling {name.lower()}",
                f"Cross-functional team specializing in {name.lower()}"
            ]
            
            # Create team with staggered creation dates (older departments first)
            # Operations and core engineering teams created earlier
            if department in ["Engineering", "Operations"]:
                # Created in first 2 years
                team_created_at = random_date_between(
                    COMPANY_FOUNDING_DATE,
                    increment_date(COMPANY_FOUNDING_DATE, 730)  # 2 years
                )
            elif department == "Sales & Marketing":
                # Created in years 1-4
                team_created_at = random_date_between(
                    increment_date(COMPANY_FOUNDING_DATE, 180),  # 6 months after founding
                    increment_date(COMPANY_FOUNDING_DATE, 1460)  # 4 years
                )
            else:  # Product & Design
                # Created in years 1-5
                team_created_at = random_date_between(
                    increment_date(COMPANY_FOUNDING_DATE, 90),  # 3 months after founding
                    increment_date(COMPANY_FOUNDING_DATE, 1825)  # 5 years
                )
            
            teams. append({
                "team_id": generate_id(),
                "org_id": org_id,
                "name": name,
                "description": random.choice(descriptions),
                "department": department,
                "created_at": team_created_at
            })
    
    print(f"   ✓ Generated {len(teams)} teams total")
    return teams


def increment_date(date_str: str, days: int) -> str:
    """Helper function to increment a date by specified days"""
    from datetime import datetime, timedelta
    
    date_obj = datetime.fromisoformat(date_str)
    new_date = date_obj + timedelta(days=days)
    
    # Don't exceed current simulation date
    current = datetime.fromisoformat(SIMULATION_CURRENT_DATE)
    if new_date > current: 
        return SIMULATION_CURRENT_DATE
    
    return new_date.isoformat()