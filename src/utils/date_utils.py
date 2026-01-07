from datetime import datetime, timedelta
import random
import numpy as np

def random_date_between(start_date: str, end_date: str) -> str:
    """Generate random date between two dates"""
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).isoformat()

def random_business_date(start_date: str, end_date: str) -> str:
    """Generate random date avoiding weekends (90% of the time)"""
    date_str = random_date_between(start_date, end_date)
    date_obj = datetime.fromisoformat(date_str)
    
    # 90% avoid weekends
    if random.random() < 0.9 and date_obj.weekday() >= 5:
        # Move to Friday
        days_back = date_obj.weekday() - 4
        date_obj -= timedelta(days=days_back)
    
    return date_obj.date().isoformat()

def generate_due_date_realistic(created_at: str) -> str | None:
    """
    Generate realistic due date based on research:
    - 25% no due date
    - 20% within 1 week
    - 35% within 1 month
    - 15% 1-3 months
    - 5% overdue
    """
    rand = random.random()
    created = datetime.fromisoformat(created_at)
    
    if rand < 0.25:
        return None  # No due date
    elif rand < 0.45:  # Within 1 week
        days = random.randint(1, 7)
    elif rand < 0.80:  # Within 1 month
        days = random.randint(8, 30)
    elif rand < 0.95:  # 1-3 months
        days = random.randint(31, 90)
    else:  # Overdue
        days = random.randint(-14, -1)
    
    due_date = created + timedelta(days=days)
    
    # Avoid weekends
    if due_date.weekday() >= 5 and random.random() < 0.9:
        due_date -= timedelta(days=due_date.weekday() - 4)
    
    return due_date.date().isoformat()

def generate_completion_time(created_at: str) -> str:
    """Generate realistic completion time using log-normal distribution"""
    created = datetime.fromisoformat(created_at)
    # Log-normal:  mean 5 days, std 3 days (cycle time research)
    days = np.random.lognormal(mean=1.6, sigma=0.6)
    days = max(0.1, min(days, 30))  # Clamp between 2 hours and 30 days
    completed = created + timedelta(days=days)
    return completed.isoformat()