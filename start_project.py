#!/usr/bin/env python3
"""
Project Starter - Master Orchestrator
Coordinates all setup tools to create a complete project foundation.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT_STARTER_PROMPT = """
Please set up a new project by running through these steps:

1. **Project Structure** (setup_structure.py)
   - Ask about project type and create directory structure
   - Initialize git repository
   - Create initial commit

2. **License Selection** (setup_license.py)  
   - Help choose appropriate license
   - Generate LICENSE file
   - Commit with message: "chore: add LICENSE"

3. **Git Ignore** (setup_gitignore.py)
   - Analyze project type and generate .gitignore
   - Commit with message: "chore: add comprehensive .gitignore"

4. **Environment Setup** (setup_env.py)
   - Create .env.example with discovered variables
   - Commit with message: "chore: add environment variable template"

5. **README Creation** (setup_readme.py)
   - Generate comprehensive README.md
   - Commit with message: "docs: add comprehensive README"

6. **CLAUDE.md Setup** (setup_claude_md.py)
   - Create AI assistant guidelines
   - Commit with message: "docs: add AI assistant guidelines (CLAUDE.md)"

7. **Initial Feature Prompt** (create_feature_prompt.py)
   - Ask if user wants to create first feature prompt
   - If yes, generate feature implementation plan

8. **Final Setup**
   - Create any additional configuration files
   - Set up pre-commit hooks if desired
   - Initialize package manager if needed
   - Final commit with message: "chore: complete initial project setup"

For each step:
- Run the tool's prompt
- Execute the necessary actions
- Make a git commit
- Move to the next step

The goal is a fully configured project ready for development with:
- Clear structure and documentation
- Proper licensing and gitignore
- AI-friendly guidelines
- Version control history
"""

def main():
    print("🚀 Project Starter - Master Orchestrator")
    print("=" * 50)
    print("\nThis tool coordinates all setup tools to create a complete project.")
    print("\nTo start a new project, provide this prompt to Claude:\n")
    print(PROJECT_STARTER_PROMPT)
    print("\n" + "=" * 50)
    print("\nTools that will be used:")
    
    tools = [
        ("📁", "setup_structure.py", "Create project structure"),
        ("⚖️", "setup_license.py", "Select and add license"),
        ("🚫", "setup_gitignore.py", "Generate .gitignore"),
        ("🔐", "setup_env.py", "Create environment template"),
        ("📘", "setup_readme.py", "Generate README.md"),
        ("🤖", "setup_claude_md.py", "Create CLAUDE.md"),
        ("🚀", "create_feature_prompt.py", "Optional: First feature")
    ]
    
    for emoji, tool, desc in tools:
        print(f"{emoji} {tool:<25} - {desc}")
    
    print("\n" + "=" * 50)
    print("Ready to create a professional project foundation!")
    
    return 0

if __name__ == "__main__":
    exit(main())