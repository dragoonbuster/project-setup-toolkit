#!/usr/bin/env python3
"""
CI/CD Setup Tool
Provides instructions for Claude AI to generate CI/CD pipeline configurations.
"""

from pathlib import Path

CI_PROMPT = """
Please create appropriate CI/CD pipeline configuration by:

1. Reading the CI_template.md file
2. Analyzing the project to determine:
   - Programming language and framework
   - Test framework and commands
   - Build requirements
   - Deployment targets
   - Environment needs

3. Generating configuration for:
   - GitHub Actions (preferred)
   - GitLab CI (if needed)
   - Other platforms as requested

4. Including workflows for:
   - Automated testing on PR/push
   - Code quality checks (linting, formatting)
   - Security scanning
   - Build and artifact creation
   - Deployment to staging/production
   - Release automation

5. Creating appropriate:
   - Workflow files (.github/workflows/)
   - Environment configurations
   - Secret requirements documentation
   - Branch protection recommendations

Make sure to:
- Use best practices for the detected tech stack
- Include comprehensive test coverage
- Set up proper security scanning
- Configure appropriate triggers
- Document required secrets and permissions

The goal is a complete CI/CD setup that ensures code quality and reliable deployments.
"""

def main():
    template_path = Path(__file__).parent.parent / "templates" / "CI_template.md"
    
    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        return 1
    
    print("🔄 CI/CD Pipeline Generator")
    print("=" * 50)
    print("\nTo generate CI/CD configuration, provide this prompt to Claude:\n")
    print(CI_PROMPT)
    print("\nTemplate location:", template_path)
    print("\n" + "=" * 50)
    print("This tool helps create robust CI/CD pipelines.")
    
    return 0

if __name__ == "__main__":
    exit(main())