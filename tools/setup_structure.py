#!/usr/bin/env python3
"""
Project Structure Generator
Provides instructions for Claude AI to create project directory structures.
"""

from pathlib import Path

STRUCTURE_PROMPT = """
Please create a project directory structure by:

1. Reading the STRUCTURE_template.md file
2. Asking the user about:
   - Project type (web app, CLI tool, library, API, etc)
   - Primary language and framework
   - Testing preferences
   - Documentation needs
   - Deployment targets

3. Generating an appropriate structure including:
   - Source code organization
   - Test directory layout
   - Configuration file placement
   - Documentation structure
   - Build/deployment directories
   - Asset/resource directories

4. Creating the actual directories and initial files:
   - Empty __init__.py files for Python packages
   - .gitkeep files for empty directories
   - Initial main/index files
   - Basic configuration files
   - Initial test files

5. Generating a structure.md documenting:
   - Directory purposes
   - File organization rules
   - Naming conventions
   - Where different types of code belong

Make sure to:
- Follow language/framework best practices
- Include all necessary configuration files
- Create a logical, scalable structure
- Add README files in key directories
- Consider deployment and build needs

The goal is a well-organized project structure that scales with growth.
"""

def main():
    template_path = Path(__file__).parent.parent / "templates" / "STRUCTURE_template.md"
    
    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        return 1
    
    print("📁 Project Structure Generator")
    print("=" * 50)
    print("\nTo generate project structure, provide this prompt to Claude:\n")
    print(STRUCTURE_PROMPT)
    print("\nTemplate location:", template_path)
    print("\n" + "=" * 50)
    print("This tool helps create organized project directory structures.")
    
    return 0

if __name__ == "__main__":
    exit(main())