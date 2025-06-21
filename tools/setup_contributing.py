#!/usr/bin/env python3
"""
Contributing Guide Generator
Provides instructions for Claude AI to create CONTRIBUTING.md files.
"""

from pathlib import Path

CONTRIBUTING_PROMPT = """
Please create a comprehensive CONTRIBUTING.md file by:

1. Reading the CONTRIBUTING_template.md file
2. Analyzing the project to understand:
   - Development workflow
   - Coding standards
   - Testing requirements
   - Git workflow
   - Review process

3. Creating guidelines for:
   - How to set up development environment
   - How to make changes
   - How to run tests
   - How to submit pull requests
   - How to report bugs
   - How to suggest features

4. Including:
   - Code style guidelines
   - Commit message format
   - PR template
   - Issue templates
   - Code of conduct basics

5. Making it welcoming and clear

Make sure to:
- Be encouraging to new contributors
- Provide specific examples
- Link to relevant documentation
- Include contact information
- Thank contributors

The goal is to make contributing as easy as possible.
"""

def main():
    template_path = Path(__file__).parent.parent / "templates" / "CONTRIBUTING_template.md"
    
    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        return 1
    
    print("🤝 Contributing Guide Generator")
    print("=" * 50)
    print("\nTo generate CONTRIBUTING.md, provide this prompt to Claude:\n")
    print(CONTRIBUTING_PROMPT)
    print("\nTemplate location:", template_path)
    print("\n" + "=" * 50)
    print("This tool helps create welcoming contribution guidelines.")
    
    return 0

if __name__ == "__main__":
    exit(main())