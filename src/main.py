import sys
import os
from pathlib import Path

# Add src to path
sys. path.insert(0, str(Path(__file__).parent))

from database import Database
from config import DB_PATH, TARGET_EMPLOYEE_COUNT
from generators.organizations import generate_organization
from generators.teams import generate_teams
from generators. users import generate_users
from generators.projects import generate_projects
from generators.tasks import generate_tasks
from generators.comments import generate_comments

def main():
    print("=" * 60)
    print("ASANA RL ENVIRONMENT - SEED DATA GENERATOR")
    print("=" * 60)
    print()
    
    # Check for OpenAI API key and test connection
    print("🔑 Checking OpenAI API configuration...")
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key: 
        print("   ❌ OPENAI_API_KEY not found in environment variables")
        print("   ⚠️  LLM features will be DISABLED")
        print("   ℹ️  To enable LLM:  Set OPENAI_API_KEY in your . env file")
        print()
        use_llm = False
    else:
        # Show partial key for verification
        key_preview = f"{api_key[:10]}... {api_key[-4:]}" if len(api_key) > 14 else "***"
        print(f"   ✓ OpenAI API key found: {key_preview}")
        
        # Test API connection with a simple call
        try:
            from utils. llm_utils import generate_with_llm
            print("   🧪 Testing OpenAI API connection...")
            test_response = generate_with_llm("Say 'OK'", temperature=0.5)
            
            if test_response: 
                print(f"   ✓ API connection successful!  Response: '{test_response[: 50]}'")
                print("   ✓ LLM features ENABLED")
                use_llm = True
            else:
                print("   ⚠️  API returned empty response")
                print("   ⚠️  LLM features will be DISABLED (using templates only)")
                use_llm = False
        except Exception as e:
            print(f"   ❌ API connection failed: {str(e)[:100]}")
            print("   ⚠️  LLM features will be DISABLED (using templates only)")
            use_llm = False
    print()
    
    # Initialize database
    print("📦 Initializing database...")
    db = Database(DB_PATH)
    db.connect()
    db.initialize_schema()
    print()
    
    # Generate organization
    print("🏢 Generating organization...")
    org = generate_organization()
    db.insert_batch("organizations", [org])
    print(f"   Company: {org['name']}")
    print(f"   Domain: {org['domain']}")
    print()
    
    # Generate teams
    print("👥 Generating teams...")
    teams = generate_teams(org["org_id"])
    db.insert_batch("teams", teams)
    print(f"   ✓ Created {len(teams)} teams across departments")
    print()
    
    # Generate users and memberships
    print("🧑‍💼 Generating users and team memberships...")
    users, memberships = generate_users(org["org_id"], org["domain"], teams, TARGET_EMPLOYEE_COUNT)
    db.insert_batch("users", users)
    db.insert_batch("team_memberships", memberships)
    print(f"   ✓ Created {len(users)} users")
    print(f"   ✓ Created {len(memberships)} team memberships")
    print()
    
    # Generate projects and sections
    print("📁 Generating projects and sections...")
    if use_llm:
        print("   🤖 Using LLM for project name generation...")
    else:
        print("   📝 Using templates for project name generation...")
    
    projects, sections = generate_projects(teams, users, use_llm=use_llm)
    db.insert_batch("projects", projects)
    db.insert_batch("sections", sections)
    print(f"   ✓ Created {len(projects)} projects")
    print(f"   ✓ Created {len(sections)} sections")
    print()
    
    # Generate tasks
    print("✅ Generating tasks...")
    if use_llm:
        print("   🤖 Using LLM for task generation (this may take a while)...")
    else:
        print("   📝 Using templates for task generation...")
    
    tasks = generate_tasks(projects, sections, users, use_llm=use_llm)
    db.insert_batch("tasks", tasks)
    print(f"   ✓ Created {len(tasks)} tasks")
    print()
    
    # Generate comments
    print("💬 Generating comments...")
    comments = generate_comments(tasks, users)
    db.insert_batch("comments", comments)
    print(f"   ✓ Created {len(comments)} comments")
    print()
    
    # Summary
    print("=" * 60)
    print("✨ GENERATION COMPLETE")
    print("=" * 60)
    print(f"📊 Summary:")
    print(f"   Database:  {DB_PATH}")
    print(f"   Organization: {org['name']}")
    print(f"   Teams:  {len(teams)}")
    print(f"   Users: {len(users)}")
    print(f"   Projects: {len(projects)}")
    print(f"   Tasks: {len(tasks)}")
    print(f"   Comments: {len(comments)}")
    print()
    
    if use_llm:
        print("✓ Generated with LLM assistance for higher quality")
    else:
        print("⚠️  Generated with templates only")
        print("   For better quality, set OPENAI_API_KEY in .env file")
    print()
    
    db.close()
    
    print("🎉 All done! Database ready at:", DB_PATH)

if __name__ == "__main__": 
    main()