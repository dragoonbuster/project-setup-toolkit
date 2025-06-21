#!/usr/bin/env python3
"""
README.md Setup Tool
Provides instructions for Claude AI to generate a project-specific README.md file.
"""

from pathlib import Path

README_PROMPT = """
Please create a comprehensive README.md file for this project by:

1. Reading the README_template.md file
2. Analyzing the project to determine:
   - Project name, purpose, and description
   - Key features and benefits
   - Technology stack and dependencies
   - Installation and setup steps
   - Usage examples from the codebase
   - Available scripts and commands
   - Project structure
   - Testing approach
   - Deployment options
   - Contributing guidelines

3. Auto-generating appropriate badges for:
   - Version, language, license
   - Build status, test coverage
   - Any relevant metrics

4. Filling in ALL template placeholders with project-specific content
5. Saving the result as README.md

Make sure to:
- Write compelling, clear documentation
- Include real examples from the codebase
- Detect and document all available commands
- Create a professional, complete README
- Add screenshots/diagrams placeholders where appropriate

The goal is a README that helps users understand, install, and use the project effectively.
"""

def main():
    template_path = Path(__file__).parent / "README_template.md"
    
    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        return 1
    
    print("📘 README.md Generator")
    print("=" * 50)
    print("\nTo generate README.md for your project, provide this prompt to Claude:\n")
    print(README_PROMPT)
    print("\nTemplate location:", template_path)
    print("\n" + "=" * 50)
    print("This tool provides instructions for AI-assisted README.md generation.")
    
    return 0

if __name__ == "__main__":
    exit(main())