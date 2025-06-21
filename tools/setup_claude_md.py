#!/usr/bin/env python3
"""
CLAUDE.md Setup Tool
Provides instructions for Claude AI to generate a project-specific CLAUDE.md file.
"""

from pathlib import Path

CLAUDE_PROMPT = """
Please analyze the current project directory and create a comprehensive CLAUDE.md file by:

1. Reading the CLAUDE_template.md file
2. Analyzing the project structure, files, and code patterns
3. Detecting:
   - Project name and purpose
   - Technology stack and frameworks
   - File naming conventions
   - Code style patterns
   - Essential commands from package.json/Makefile/etc
   - Testing framework
   - Build/deployment setup
   - Git workflow patterns

4. Filling in ALL template placeholders with project-specific values
5. Saving the result as CLAUDE.md in the project root

Make sure to:
- Be specific rather than generic
- Detect actual patterns from the codebase
- Include all detected commands and scripts
- Set up comprehensive guidelines for future development
- Preserve the template structure while customizing content

The goal is a CLAUDE.md that helps AI assistants understand and work with this specific project effectively.
"""

def main():
    template_path = Path(__file__).parent.parent / "templates" / "CLAUDE_template.md"
    
    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        return 1
    
    print("🤖 CLAUDE.md Generator")
    print("=" * 50)
    print("\nTo generate CLAUDE.md for your project, provide this prompt to Claude:\n")
    print(CLAUDE_PROMPT)
    print("\nTemplate location:", template_path)
    print("\n" + "=" * 50)
    print("This tool provides instructions for AI-assisted CLAUDE.md generation.")
    
    return 0

if __name__ == "__main__":
    exit(main())