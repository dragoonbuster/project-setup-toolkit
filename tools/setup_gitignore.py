#!/usr/bin/env python3
"""
.gitignore Generator
Provides instructions for Claude AI to generate project-specific .gitignore files.
"""

from pathlib import Path

GITIGNORE_PROMPT = """
Please create a comprehensive .gitignore file by:

1. Reading the GITIGNORE_template.md file
2. Analyzing the project to detect:
   - Programming languages used
   - Frameworks and tools
   - Build systems
   - IDE/editor preferences
   - Operating systems

3. Including appropriate ignore patterns for:
   - Language-specific files (compiled output, caches)
   - Dependency directories (node_modules, venv, etc)
   - Build artifacts
   - IDE configuration files
   - OS-specific files
   - Log files
   - Environment files with secrets
   - Test coverage reports
   - Temporary files

4. Organizing patterns by category as shown in template
5. Adding project-specific patterns based on codebase analysis
6. Saving as .gitignore in project root

Make sure to:
- Include comprehensive patterns for detected tech stack
- Add security-critical patterns (keys, secrets, .env)
- Comment sections for clarity
- Include both general and specific patterns
- Consider CI/CD artifacts

The goal is a .gitignore that prevents accidental commits of unwanted files.
"""

def main():
    template_path = Path(__file__).parent.parent / "templates" / "GITIGNORE_template.md"
    
    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        return 1
    
    print("🚫 .gitignore Generator")
    print("=" * 50)
    print("\nTo generate .gitignore for your project, provide this prompt to Claude:\n")
    print(GITIGNORE_PROMPT)
    print("\nTemplate location:", template_path)
    print("\n" + "=" * 50)
    print("This tool helps create comprehensive .gitignore files.")
    
    return 0

if __name__ == "__main__":
    exit(main())