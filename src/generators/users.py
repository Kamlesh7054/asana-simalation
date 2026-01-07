from utils.id_generator import generate_id
from utils.date_utils import random_date_between
from scrapers.names import generate_realistic_name
from config import TARGET_EMPLOYEE_COUNT, COMPANY_FOUNDING_DATE, SIMULATION_CURRENT_DATE, DEPT_DISTRIBUTION
import random
from datetime import datetime, timedelta

JOB_TITLES = {
    "Engineering": [
        "Software Engineer", "Senior Software Engineer", "Staff Engineer",
        "Engineering Manager", "Senior Engineering Manager", "Director of Engineering",
        "QA Engineer", "DevOps Engineer", "Security Engineer", "Data Engineer",
        "Principal Engineer", "VP of Engineering", "CTO"
    ],
    "Sales & Marketing": [
        "Marketing Manager", "Content Writer", "SEO Specialist", "Product Marketing Manager",
        "Sales Representative", "Account Executive", "Sales Manager", "CMO",
        "Customer Success Manager", "Growth Manager", "VP of Sales", "VP of Marketing",
        "Marketing Coordinator", "Sales Development Representative"
    ],
    "Operations": [
        "HR Manager", "Recruiter", "Finance Manager", "Accountant", "Legal Counsel",
        "IT Administrator", "Operations Manager", "Chief Financial Officer",
        "Senior Recruiter", "HR Business Partner", "Compliance Officer", "CFO", "COO"
    ],
    "Product & Design": [
        "Product Manager", "Senior Product Manager", "UX Designer", "UI Designer",
        "UX Researcher", "Product Designer", "VP of Product", "Design Lead",
        "Staff Product Manager", "Design Director", "Chief Product Officer"
    ]
}

def generate_users(org_id:   str, company_domain: str, teams: list, target_count: int = TARGET_EMPLOYEE_COUNT):
    """Generate users and team memberships"""
    users = []
    memberships = []
    email_counter = {}  # Track email usage to prevent duplicates
    
    # Group teams by department
    teams_by_dept = {}
    for team in teams:  
        dept = team["department"]
        if dept not in teams_by_dept:
            teams_by_dept[dept] = []
        teams_by_dept[dept]. append(team)
    
    print(f"   Generating {target_count} users across departments...")
    
    # Generate users distributed across departments
    for department, team_list in teams_by_dept.items():
        dept_percentage = DEPT_DISTRIBUTION[department]
        dept_user_count = int(target_count * dept_percentage)
        
        if not team_list:
            print(f"   ⚠️  No teams found for {department}")
            continue
        
        users_per_team = max(1, dept_user_count // len(team_list))
        
        print(f"   {department}: {dept_user_count} users across {len(team_list)} teams")
        
        for team in team_list: 
            for _ in range(users_per_team):
                first_name, last_name = generate_realistic_name()
                user_id = generate_id()
                
                # Generate unique email
                base_email = f"{first_name.lower()}.{last_name.lower()}@{company_domain}"
                
                # Check if email already exists
                if base_email in email_counter:
                    email_counter[base_email] += 1
                    email = f"{first_name.lower()}.{last_name.lower()}{email_counter[base_email]}@{company_domain}"
                else:
                    email_counter[base_email] = 0
                    email = base_email
                
                # Hiring date distribution
                hiring_date = random_date_between(
                    COMPANY_FOUNDING_DATE,
                    SIMULATION_CURRENT_DATE
                )
                
                # Last active:    90% within last week
                rand = random.random()
                now = datetime.fromisoformat(SIMULATION_CURRENT_DATE)
                if rand < 0.90:
                    last_active = now - timedelta(days=random.randint(0, 7))
                elif rand < 0.95:
                    last_active = now - timedelta(days=random.randint(8, 30))
                else:
                    last_active = now - timedelta(days=random.randint(31, 90))
                
                users.append({
                    "user_id": user_id,
                    "org_id": org_id,
                    "email": email,  # Use unique email
                    "first_name":   first_name,
                    "last_name": last_name,
                    "job_title":  random.choice(JOB_TITLES[department]),
                    "department":  department,
                    "profile_photo_url":  f"https://i.pravatar.cc/150?u={user_id}",
                    "created_at": hiring_date,
                    "last_active":  last_active.  isoformat(),
                    "is_active":  True
                })
                
                # Add team membership
                memberships.append({
                    "membership_id": generate_id(),
                    "team_id": team["team_id"],
                    "user_id": user_id,
                    "role": "member" if random.random() > 0.1 else "admin",
                    "joined_at": hiring_date
                })
    
    print(f"   ✓ Generated {len(users)} users")
    print(f"   ✓ Generated {len(memberships)} team memberships")
    
    return users, memberships