#!/usr/bin/env python3
"""
License Selector Tool
Provides instructions for Claude AI to help select and generate appropriate licenses.
"""

from pathlib import Path

LICENSE_PROMPT = """
Please help select and create an appropriate license by:

1. Reading the LICENSE_template.md file
2. Asking the user about:
   - Project type and purpose
   - Commercial vs open source intent
   - Desired permissions (can others sell it?)
   - Required attributions
   - Patent considerations
   - Copyleft preferences

3. Recommending the most appropriate license based on:
   - User's goals and constraints
   - Industry standards for similar projects
   - Compatibility with dependencies

4. Generating the LICENSE file with:
   - Full license text
   - Copyright year and holder name
   - Any custom modifications needed

5. Creating a brief license summary in README.md

Common recommendations:
- Libraries: MIT or Apache 2.0
- Applications: MIT, Apache 2.0, or GPL
- Documentation: CC BY 4.0
- Commercial: Proprietary license

Make sure to:
- Explain the implications of the chosen license
- Check compatibility with project dependencies
- Include the full legal text
- Update package.json/setup.py with license field

The goal is appropriate legal protection while meeting project goals.
"""

def main():
    template_path = Path(__file__).parent.parent / "templates" / "LICENSE_template.md"
    
    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        return 1
    
    print("⚖️  License Selector Tool")
    print("=" * 50)
    print("\nTo select and generate a license, provide this prompt to Claude:\n")
    print(LICENSE_PROMPT)
    print("\nTemplate location:", template_path)
    print("\n" + "=" * 50)
    print("This tool helps choose appropriate software licenses.")
    
    return 0

if __name__ == "__main__":
    exit(main())