#!/usr/bin/env python3
"""
Feature Prompt Builder
Provides instructions for Claude AI to generate detailed feature implementation prompts.
"""

from pathlib import Path

FEATURE_PROMPT = """
Please create a detailed feature implementation prompt by:

1. Reading the FEATURE_PROMPT_template.md file
2. Gathering information about the requested feature:
   - Feature name and description
   - User story and acceptance criteria
   - Technical requirements
   - Affected components

3. Analyzing the current codebase to determine:
   - Existing patterns to follow
   - Files that need modification
   - New files to create
   - Dependencies to add
   - Testing approach

4. Filling in ALL template placeholders with specific details
5. Creating a step-by-step implementation plan
6. Saving the result as feature_[feature_name].md

Ask the user for:
- Feature name and description
- Priority and complexity
- Specific requirements
- Any constraints or considerations

Make sure to:
- Reference specific files and patterns from the codebase
- Include detailed technical specifications
- Provide clear acceptance criteria
- Define testing requirements
- Consider security and performance implications

The goal is a prompt that another AI can use to implement the feature correctly.
"""

def main():
    template_path = Path(__file__).parent / "FEATURE_PROMPT_template.md"
    
    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        return 1
    
    print("🚀 Feature Prompt Builder")
    print("=" * 50)
    print("\nTo generate a feature implementation prompt, provide this to Claude:\n")
    print(FEATURE_PROMPT)
    print("\nTemplate location:", template_path)
    print("\n" + "=" * 50)
    print("This tool helps create detailed prompts for feature implementation.")
    
    return 0

if __name__ == "__main__":
    exit(main())