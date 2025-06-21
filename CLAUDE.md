# CLAUDE.md - AI Assistant Guidelines

> **IMPORTANT**: Always read `docs/PROJECT_SETUP_PLAN.md` and `docs/PROJECT_REVIEW_PLAN.md` at the start of each new context window for current implementation status and next steps.

## Project Overview
**Project Name**: project-setup-toolkit  
**Purpose**: AI-driven toolkit for setting up new software projects with templates and best practices  
**Tech Stack**: Python, Git, GitHub CLI, Markdown Templates  
**Primary Language**: Python  
**Status**: Development

## Claude Behavior Guidelines

### Communication Style
- Be concise and direct - avoid unnecessary explanations
- Only provide code explanations when explicitly asked
- Use file references with pattern: `filename.ext:line_number`
- Avoid emojis unless specifically requested
- Keep responses under 4 lines unless detail is requested

### Task Management
- **ALWAYS** use TodoWrite for multi-step tasks (3+ steps)
- Mark tasks as `in_progress` BEFORE starting work
- Only have ONE task `in_progress` at a time
- Mark tasks `completed` IMMEDIATELY after finishing
- Break complex features into specific, actionable items

### Tool Usage Priority
1. **Search/Navigation**: Use Task tool for open-ended searches
2. **File Reading**: Use Read for specific files, Glob for patterns
3. **Code Changes**: Prefer Edit/MultiEdit over Write for existing files
4. **Testing**: Always verify changes with tests after implementation
5. **Validation**: Run lint/typecheck commands after code changes

## Project Structure

### Directory Layout
```
project-setup-toolkit/
├── templates/           # Template files (*.md)
│   ├── CLAUDE_template.md     # AI assistant guidelines
│   ├── README_template.md     # Project documentation
│   ├── FEATURE_PROMPT_template.md  # Feature implementation
│   └── [other templates]     # Additional templates
├── tools/              # Setup and generation tools
│   ├── setup_*.py     # Project setup tools
│   ├── create_*.py    # Content generation tools
│   └── generate_*.py  # Automated generators
├── docs/               # Documentation
├── examples/           # Example outputs
└── [root files]        # README.md, LICENSE, etc.
```

### File Naming Conventions
- **Templates**: UPPERCASE_template.md (e.g., `CLAUDE_template.md`)
- **Tools**: lowercase_action.py (e.g., `setup_readme.py`)
- **Tests**: test_*.py
- **Documentation**: lowercase.md
- **Config**: lowercase-config.ext

## Development Workflow

### Essential Commands
```bash
# Install dependencies (none currently)
# This is a pure Python project with standard library only

# Start development
python start_project.py

# Run tests (ALWAYS run after changes)
python -m pytest tests/ (when implemented)

# Type checking (MUST pass before considering task complete)
python -m mypy tools/ (when configured)

# Linting (MUST pass before considering task complete)
python -m ruff check . (when configured)

# Format code
python -m black . (when configured)

# Build for production
# Not applicable - this is a toolkit
```

### Git Workflow
- **Branch naming**: feature/*, fix/*, refactor/*, docs/*
- **Commit style**: type(scope): description (conventional commits)
- **Never commit**: .env files, __pycache__, *.pyc, .DS_Store
- **Always test**: Verify tools work before marking tasks complete

## Code Standards

### Style Guidelines
- **Indentation**: 4 spaces
- **Line length**: 88 characters (Black default)
- **Quotes**: Double quotes (consistent with Black)
- **Semicolons**: Never (Python)
- **Trailing commas**: Yes (for multi-line)

### Best Practices
- Check existing patterns before implementing new features
- Use existing utilities and components when available
- Follow established error handling patterns
- Maintain consistent import ordering
- Add type hints for all function signatures
- Make commits frequently and before each new change
- Keep tools simple - just provide instructions for Claude
- Templates should be easy to read and modify

## Architecture Decisions

### Database/Persistence
- **Database Type**: None (file-based toolkit)
- **ORM/Query Builder**: N/A
- **Migration Tool**: N/A
- **Schema Location**: N/A

### State Management
- **Library**: N/A (stateless tools)
- **Pattern**: Simple function calls
- **Conventions**: Each tool is independent

### API Communication
- **Base URL**: N/A
- **Auth Method**: N/A
- **Error Format**: N/A
- **Request Library**: N/A

### Testing Strategy
- **Framework**: pytest (when implemented)
- **Coverage Target**: 80%
- **Test Location**: tests/ directory
- **Naming**: test_*.py

## Error Handling

### Expected Behaviors
- Validate file paths before processing
- Provide clear error messages when templates are missing
- Gracefully handle git command failures
- Show helpful usage instructions on errors
- Exit with appropriate status codes

### Common Issues
- **Template not found**: Ensure all templates are in templates/ directory
- **Git not initialized**: Tools require git repository for commits
- **GitHub CLI not authenticated**: Some tools require gh auth

## Performance Considerations
- **Bundle size limits**: N/A (Python toolkit)
- **Load time targets**: < 1s per tool execution
- **Optimization strategies**: Simple file operations, minimal dependencies
- **Performance monitoring**: None needed for CLI tools

## Security Requirements
- Input validation on all file paths
- No sensitive data in templates or tools
- Secure handling of git operations
- No network calls except GitHub CLI
- No secrets in code (templates use placeholders)

## Accessibility Standards
- Clear command-line help text
- Descriptive error messages
- Support for different terminal environments
- Unicode-safe file operations

## Dependencies

### Core Dependencies
```python
# Standard library only currently
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
```

### Development Dependencies
```python
# Future additions:
# pytest - for testing
# black - for code formatting
# ruff - for linting
# mypy - for type checking
```

## Environment Variables
```bash
# Required variables
# None currently

# Optional variables
# GITHUB_TOKEN - for enhanced GitHub CLI operations
```

## Deployment

### Build Process
1. No build needed - Python scripts
2. Ensure all templates are present
3. Verify tools are executable
4. Test with sample projects
5. Tag version for release

### Environments
- **Development**: Local development environment
- **Staging**: N/A
- **Production**: Distributed as toolkit files

## Troubleshooting

### Common Problems
1. **Problem**: Template not found error
   **Solution**: Ensure templates/ directory exists with all templates

2. **Problem**: Git commands fail
   **Solution**: Initialize git repository and configure user

3. **Problem**: GitHub CLI authentication
   **Solution**: Run `gh auth login` first

### Debug Commands
```bash
# Check Python version
python --version

# Check git configuration
git config --list

# Check GitHub CLI auth
gh auth status

# List available tools
ls tools/
```

## Project-Specific Notes

### Tool Architecture
- Each tool provides instructions for Claude rather than executing logic
- Templates use {{PLACEHOLDER}} syntax for AI-driven filling
- Tools are composable - work independently or together
- start_project.py orchestrates the full setup workflow

### Extension Pattern
1. Create new template file: NEW_THING_template.md
2. Create corresponding tool: setup_new_thing.py
3. Add to start_project.py orchestration
4. Update this CLAUDE.md documentation

## Common Patterns
- Read template file first, validate it exists
- Provide clear prompt for Claude to fill template
- Include template location in tool output
- Keep tools under 100 lines and simple
- Use consistent CLI help format
- Make all scripts executable with chmod +x

## Monitoring & Logging
- **Logging Library**: print() statements for simplicity
- **Log Levels**: None (simple CLI tools)
- **Error Tracking**: Exit codes and stderr
- **Analytics**: None

## Resources
- **Documentation**: docs/ directory (when created)
- **Design System**: N/A
- **API Docs**: N/A
- **CI/CD**: GitHub Actions (when configured)

---
*Last updated: 2025-01-21*
*Template Version: 2.1*