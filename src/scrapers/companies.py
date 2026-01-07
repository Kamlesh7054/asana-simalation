import random

# Real B2B SaaS company name patterns
COMPANY_PREFIXES = [
    "Stream", "Data", "Cloud", "Sync", "Flow", "Pulse", "Wave", "Grid",
    "Stack", "Link", "Nexus", "Prism", "Quantum", "Vertex", "Zenith"
]

COMPANY_SUFFIXES = [
    "Flow", "Core", "Base", "Sync", "Works", "Labs", "Tech", "Systems",
    "Solutions", "Platform", "Hub", "Space", "Forge", "Dynamics"
]

def generate_company_name() -> str:
    """Generate realistic B2B SaaS company name"""
    prefix = random.choice(COMPANY_PREFIXES)
    suffix = random.choice(COMPANY_SUFFIXES)
    return f"{prefix}{suffix}"

def generate_domain(company_name: str) -> str:
    """Generate company domain"""
    return company_name.lower().replace(" ", "") + ".com"