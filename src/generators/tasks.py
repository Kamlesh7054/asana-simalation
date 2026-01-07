from utils.id_generator import generate_id
from utils.date_utils import generate_due_date_realistic, generate_completion_time, random_date_between
from utils. llm_utils import generate_with_llm
from config import TASKS_PER_PROJECT_RANGE, SIMULATION_CURRENT_DATE
from datetime import datetime
import random
import numpy as np

# Fallback templates when LLM is unavailable or fails
TASK_NAME_TEMPLATES = {
    "Engineering": [
        "Implement {} feature",
        "Fix bug in {}",
        "Add unit tests for {}",
        "Refactor {} module",
        "Optimize {} performance",
        "Deploy {} to production",
        "Review PR for {}",
        "Update {} documentation",
        "Debug {} issue",
        "Migrate {} to new architecture",
        "Add error handling for {}",
        "Improve {} security",
        "Scale {} infrastructure",
        "Investigate {} performance bottleneck",
        "Configure {} monitoring",
        "Integrate {} service"
    ],
    "Sales & Marketing": [
        "Write blog post about {}",
        "Create {} campaign",
        "Design {} graphics",
        "Update {} landing page",
        "Schedule {} webinar",
        "Draft {} email",
        "Analyze {} metrics",
        "Optimize {} conversion",
        "Create {} presentation",
        "Plan {} strategy",
        "Research {} competitors",
        "Launch {} initiative",
        "Prepare {} demo",
        "Track {} performance"
    ],
    "Operations": [
        "Process {} requests",
        "Review {} policy",
        "Update {} procedures",
        "Prepare {} report",
        "Schedule {} meeting",
        "Audit {} systems",
        "Streamline {} workflow",
        "Implement {} tool",
        "Train team on {}",
        "Evaluate {} vendors",
        "Document {} process",
        "Coordinate {} logistics"
    ],
    "Product & Design": [
        "Design {} mockups",
        "Conduct {} user research",
        "Update {} wireframes",
        "Create {} prototype",
        "Test {} with users",
        "Iterate on {} design",
        "Gather feedback on {}",
        "Define {} requirements",
        "Sketch {} concepts",
        "Validate {} hypothesis",
        "Refine {} user flow",
        "Build {} interactive prototype"
    ]
}

TASK_COMPONENTS = {
    "Engineering": [
        "authentication", "payment API", "user dashboard", "database schema",
        "notification system", "search functionality", "caching layer", "API endpoints",
        "user profile", "admin panel", "reporting module", "email service",
        "file upload", "data migration", "integration tests", "CI/CD pipeline",
        "error logging", "session management", "data validation", "security audit"
    ],
    "Sales & Marketing": [
        "Q1 campaign", "product launch", "SEO strategy", "social media presence",
        "email newsletter", "case study", "webinar series", "landing page",
        "ad campaign", "content calendar", "lead magnet", "sales deck",
        "customer testimonials", "brand guidelines", "market research", "competitor analysis"
    ],
    "Operations": [
        "onboarding", "quarterly review", "budget planning", "compliance audit",
        "vendor contracts", "employee handbook", "IT security", "office setup",
        "payroll", "benefits enrollment", "performance reviews", "team building",
        "expense tracking", "resource allocation", "policy updates", "training program"
    ],
    "Product & Design": [
        "checkout flow", "mobile app", "homepage redesign", "user profile page",
        "settings page", "navigation menu", "dashboard layout", "onboarding flow",
        "search interface", "notification center", "error states", "loading states",
        "empty states", "confirmation dialogs", "filter controls", "accessibility features"
    ]
}

def generate_task_name(project_name: str, department:  str, use_llm: bool = True) -> str:
    """Generate realistic task name with LLM and fallback"""
    # Try LLM first (50% of the time if enabled)
    if use_llm and random.random() < 0.5:
        try:
            prompt = f"""Generate a realistic task name for project "{project_name}" in {department} department. 
Engineering examples: "Implement OAuth2 authentication", "Fix memory leak in user service", "Add unit tests for API endpoints"
Marketing examples: "Write blog post about Q1 features", "Design email campaign graphics", "Update landing page copy"
Operations examples: "Review expense policy", "Prepare Q1 budget report", "Update onboarding procedures"
Product examples: "Design checkout flow mockups", "Conduct user research on mobile app", "Create homepage prototype"
Return only the task name, no explanation or quotes."""
            
            name = generate_with_llm(prompt, temperature=0.9)
            # Validate LLM output
            if name and len(name) > 5 and len(name) < 150:
                # Clean up the response
                name = name.strip().strip('"').strip("'")
                return name
        except Exception as e:
            print(f"   ⚠️  LLM generation failed: {e}")
    
    # Fallback to templates
    templates = TASK_NAME_TEMPLATES.get(department, TASK_NAME_TEMPLATES["Engineering"])
    components = TASK_COMPONENTS.get(department, TASK_COMPONENTS["Engineering"])
    
    # Select random template and component
    template = random.choice(templates)
    component = random.choice(components)
    
    # Add variation with version numbers or dates (30% of the time)
    if random.random() < 0.3:
        variation = random.choice([
            f"{component} v{random.randint(1, 5)}",
            f"{component} Q{random.randint(1, 4)}",
            f"{component} Phase {random.randint(1, 3)}",
            component
        ])
    else:
        variation = component
    
    return template.format(variation)

def generate_task_description(task_name: str, use_llm: bool = True) -> str:
    """Generate task description with varied detail"""
    detail_level = random.random()
    
    # 20% no description
    if detail_level < 0.2:
        return ""
    
    # Try LLM for 50% of tasks with descriptions
    if use_llm and random.random() < 0.5:
        try:
            if detail_level < 0.7:
                # Brief description
                prompt = f"Write a brief 1-2 sentence task description for: {task_name}. No preamble."
            else:
                # Detailed description
                prompt = f"Write a detailed task description with 2-3 acceptance criteria bullet points for: {task_name}. Format with bullet points.  No preamble."
            
            description = generate_with_llm(prompt, temperature=0.7)
            if description and len(description) > 10:
                return description.strip()
        except Exception as e:
            print(f"   ⚠️  LLM description failed: {e}")
    
    # Fallback to template descriptions
    if detail_level < 0.7:
        # Brief
        return f"Complete the task: {task_name}.  Coordinate with team members as needed."
    else:
        # Detailed
        return f"""Complete the task: {task_name}

Acceptance Criteria:
• Implementation matches requirements
• All tests passing
• Documentation updated
• Code review completed"""

def generate_tasks(projects: list[dict], sections: list[dict], users: list[dict], use_llm: bool = True) -> list[dict]:
    """Generate tasks for all projects"""
    tasks = []
    
    # Group sections by project
    sections_by_project = {}
    for section in sections:
        pid = section["project_id"]
        if pid not in sections_by_project:
            sections_by_project[pid] = []
        sections_by_project[pid].append(section)
    
    # Group users by department
    users_by_dept = {}
    for user in users:
        dept = user["department"]
        if dept not in users_by_dept:
            users_by_dept[dept] = []
        users_by_dept[dept].append(user)
    
    print(f"   Generating tasks for {len(projects)} projects...")
    
    for idx, project in enumerate(projects):
        if idx % 10 == 0:
            print(f"   Progress: {idx}/{len(projects)} projects processed")
        
        project_id = project["project_id"]
        project_sections = sections_by_project.get(project_id, [])
        
        if not project_sections:
            continue
        
        # Number of tasks
        num_tasks = random. randint(*TASKS_PER_PROJECT_RANGE)
        
        # Get department and team users
        department = get_department_from_project(project, users)
        team_users = users_by_dept.get(department, [])
        
        # Fallback to all users if no team users found
        if not team_users: 
            team_users = users
        
        if not team_users:
            print(f"   ⚠️  No users available for project {project['name']}")
            continue

        for _ in range(num_tasks):
            # Created date within project lifetime
            created_at = random_date_between(project["created_at"], SIMULATION_CURRENT_DATE)
            
            # Section assignment (distribute across sections)
            section = random.choice(project_sections)
            
            # Assignee (85% assigned, Pareto distribution)
            assignee_id = None
            if team_users and random.random() < 0.85:
                assignee_ids = [u["user_id"] for u in team_users]
                if len(assignee_ids) == 1:
                    assignee_id = assignee_ids[0]
                else: 
                    assignee_id = np.random.choice(
                        assignee_ids,
                        p=generate_pareto_weights(len(assignee_ids))
                    )
            
            # Due date
            due_date = generate_due_date_realistic(created_at)
            
            # Completion status
            task_age_days = (datetime.fromisoformat(SIMULATION_CURRENT_DATE) - datetime.fromisoformat(created_at)).days
            
            # Completion probability:  older tasks more likely complete
            if project["project_type"] == "sprint":  
                base_completion_rate = 0.75
            elif project["project_type"] == "ongoing":
                base_completion_rate = 0.45
            else:
                base_completion_rate = 0.65
            
            # Age factor: older = more likely done
            age_factor = min(1.0, max(0, task_age_days) / 30)
            completion_prob = base_completion_rate * (0.5 + 0.5 * age_factor)
            
            completed = random. random() < completion_prob
            
            if completed:
                completed_at = generate_completion_time(created_at)
                completed_by = assignee_id
            else: 
                completed_at = None
                completed_by = None
            
            # Priority
            priority = random.choices(
                ["low", "medium", "high", "urgent"],
                weights=[0.20, 0.50, 0.20, 0.10]
            )[0]
            
            # Generate content
            if use_llm:
                task_name = generate_task_name(project["name"], department)
                task_description = generate_task_description(task_name)
            else:
                task_name = f"Task {random.randint(1, 1000)}"
                task_description = f"Description for {project['name']}"
            
            # Creator
            created_by = random.choice(team_users)["user_id"]
            
            tasks.append({
                "task_id": generate_id(),
                "project_id": project_id,
                "section_id": section["section_id"],
                "parent_task_id": None,  # Top-level task
                "name":  task_name,
                "description": task_description,
                "assignee_id": assignee_id,
                "due_date": due_date,
                "start_date": None,
                "created_at": created_at,
                "created_by":  created_by,
                "completed": completed,
                "completed_at": completed_at,
                "completed_by": completed_by,
                "priority": priority,
                "num_likes": random.randint(0, 5) if random.random() < 0.3 else 0,
                "num_subtasks":  0,
                "num_comments": 0
            })
    
    print(f"   ✓ Generated {len(tasks)} tasks total")
    return tasks

def get_department_from_project(project: dict, users: list) -> str:
    """Get department from project owner"""
    owner_id = project.get("owner_id")
    if owner_id:
        owner = next((u for u in users if u["user_id"] == owner_id), None)
        if owner:
            return owner["department"]
    
    # Fallback to Engineering if no owner found
    return "Engineering"

def generate_pareto_weights(n: int) -> np.ndarray:
    """Generate Pareto distribution (80/20 rule)"""
    if n <= 0:
        return np.array([])
    if n == 1:
        return np. array([1.0])
    
    weights = np.array([1.0 / (i + 1) ** 1.5 for i in range(n)])
    return weights / weights.sum()