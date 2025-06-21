#!/usr/bin/env python3
"""
Git Commit Message Generator
Provides instructions for Claude AI to generate semantic commit messages.
"""

from pathlib import Path

COMMIT_PROMPT = """
Please generate a semantic commit message by:

1. Reading the COMMIT_template.md file
2. Analyzing the git changes:
   - Run `git diff --staged` to see staged changes
   - Run `git status` to see file modifications
   - Understand what was changed and why

3. Determining:
   - Commit type (feat/fix/refactor/docs/style/test/chore)
   - Scope (affected component/module)
   - Short description (imperative mood, <50 chars)
   - Detailed description of changes
   - Breaking changes (if any)
   - Related issues (if any)

4. Following conventional commits format:
   - type(scope): short description
   - Blank line
   - Detailed description
   - Breaking changes section if needed
   - Closes/Fixes references if applicable

5. Filling the template with appropriate content

Make sure to:
- Use imperative mood ("add" not "added")
- Be specific about what changed
- Explain why the change was made
- Keep first line under 50 characters
- Wrap body at 72 characters

Output the complete commit message ready for use with git commit -m
"""

def main():
    template_path = Path(__file__).parent.parent / "templates" / "COMMIT_template.md"
    
    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        return 1
    
    print("📝 Git Commit Message Generator")
    print("=" * 50)
    print("\nTo generate a commit message, provide this prompt to Claude:\n")
    print(COMMIT_PROMPT)
    print("\nTemplate location:", template_path)
    print("\n" + "=" * 50)
    print("This tool helps create semantic commit messages from git changes.")
    
    return 0

if __name__ == "__main__":
    exit(main())