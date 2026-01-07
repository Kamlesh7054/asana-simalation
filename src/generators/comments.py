from utils.id_generator import generate_id
from utils.date_utils import random_date_between
from utils.llm_utils import generate_with_llm
from config import SIMULATION_CURRENT_DATE
import random

COMMENT_TEMPLATES = [
    "LGTM!  Approving.",
    "Can you provide more context on this?",
    "Blocked on {dependency}",
    "Updated the designs, please review",
    "This is ready for QA",
    "Moving to Done",
    "Great work on this! ",
    "Question: {question}",
    "Completed ahead of schedule",
    "Need help with {issue}"
]

def generate_comments(tasks: list[dict], users: list[dict]) -> list[dict]:
    """Generate comments for tasks"""
    comments = []
    
    for task in tasks: 
        # Not all tasks have comments
        if random.random() > 0.6:
            continue
        
        # Number of comments
        num_comments = random.choices([1, 2, 3, 4, 5], weights=[0.5, 0.25, 0.15, 0.07, 0.03])[0]
        
        for _ in range(num_comments):
            # Comment type
            is_system = random.random() < 0.2
            
            if is_system:
                comment_text = random.choice([
                    "Task moved to In Progress",
                    "Due date changed",
                    "Task assigned to user",
                    "Task completed",
                    "Attachment added"
                ])
                comment_type = "system"
            else:
                # User comment
                template = random.choice(COMMENT_TEMPLATES)
                if "{" in template:
                    # Fill in placeholder
                    comment_text = generate_with_llm(f"Complete this project comment: {template}")
                else:
                    comment_text = template
                comment_type = "comment"
            
            # Comment time:  between task creation and now
            created_at = random_date_between(task["created_at"], SIMULATION_CURRENT_DATE)
            
            # Commenter
            if task["assignee_id"] and random.random() < 0.6:
                user_id = task["assignee_id"]
            else:
                user_id = random.choice(users)["user_id"]
            
            comments.append({
                "comment_id": generate_id(),
                "task_id": task["task_id"],
                "user_id": user_id,
                "comment_text": comment_text,
                "comment_type": comment_type,
                "created_at": created_at
            })
        
        # Update task comment count
        task["num_comments"] = num_comments
    
    return comments