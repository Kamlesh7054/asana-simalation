import uuid

def generate_id() -> str:
    """Generate UUID similar to Asana's GID format"""
    return str(uuid. uuid4())