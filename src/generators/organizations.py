from datetime import datetime, timedelta
import random
from utils.id_generator import generate_id
from scrapers.companies import generate_company_name, generate_domain
from config import COMPANY_FOUNDING_DATE

def generate_organization() -> dict:
    """Generate single organization"""
    company_name = generate_company_name()
    
    return {
        "org_id": generate_id(),
        "name": company_name,
        "domain": generate_domain(company_name),
        "created_at":  COMPANY_FOUNDING_DATE,
        "org_type": "organization"
    }