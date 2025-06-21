#!/usr/bin/env python3
"""
Environment Variables Setup Tool
Provides instructions for Claude AI to generate .env.example files.
"""

from pathlib import Path

ENV_PROMPT = """
Please create a comprehensive .env.example file by:

1. Reading the ENV_template.md file
2. Analyzing the codebase to find:
   - Environment variable usage (process.env, os.environ, etc)
   - Configuration files that reference env vars
   - Database connection strings
   - API endpoints and keys
   - Feature flags
   - Debug/development settings

3. Creating a .env.example with:
   - All discovered environment variables
   - Descriptive comments for each variable
   - Example values (not real secrets)
   - Sensible defaults where appropriate
   - Required vs optional markings

4. Organizing variables by category:
   - Application settings
   - Database configuration
   - External services/APIs
   - Authentication
   - Feature flags
   - Logging/monitoring
   - Development settings

5. Saving as .env.example in project root

Make sure to:
- Include ALL environment variables found in code
- Provide clear descriptions
- Use placeholder values for secrets
- Mark required variables clearly
- Include type hints where helpful (string/number/boolean)
- Add security warnings for sensitive values

Example format:
# Database Configuration (Required)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

The goal is a template that helps developers configure the project correctly.
"""

def main():
    template_path = Path(__file__).parent / "ENV_template.md"
    
    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        return 1
    
    print("🔐 Environment Variables Setup Tool")
    print("=" * 50)
    print("\nTo generate .env.example, provide this prompt to Claude:\n")
    print(ENV_PROMPT)
    print("\nTemplate location:", template_path)
    print("\n" + "=" * 50)
    print("This tool helps create environment variable templates.")
    
    return 0

if __name__ == "__main__":
    exit(main())