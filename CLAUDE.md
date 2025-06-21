# CLAUDE.md - AI Assistant Guidelines

> **IMPORTANT**: Always read `PROJECT_SETUP_PLAN.md` at the start of each new context window for current implementation status and next steps.

## Project Overview
**Project Name**: {{PROJECT_NAME}}  
**Purpose**: {{PROJECT_DESCRIPTION}}  
**Tech Stack**: {{TECH_STACK}}  
**Primary Language**: {{PRIMARY_LANGUAGE}}  
**Status**: {{PROJECT_STATUS}}

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
{{PROJECT_NAME}}/
├── {{SOURCE_DIR}}/              # Source code
│   ├── {{COMPONENTS_DIR}}/     # {{COMPONENTS_DESC}}
│   ├── {{SERVICES_DIR}}/       # {{SERVICES_DESC}}  
│   ├── {{UTILS_DIR}}/          # {{UTILS_DESC}}
│   └── {{TESTS_DIR}}/          # {{TESTS_DESC}}
├── {{DOCS_DIR}}/               # Documentation
├── {{CONFIG_DIR}}/             # Configuration files
└── {{SCRIPTS_DIR}}/            # Build/deploy scripts
```

### File Naming Conventions
- **Components**: {{COMPONENT_NAMING}} (e.g., {{COMPONENT_EXAMPLE}})
- **Utilities**: {{UTILITY_NAMING}} (e.g., {{UTILITY_EXAMPLE}})
- **Tests**: {{TEST_NAMING}}
- **Styles**: {{STYLE_NAMING}}
- **Config**: {{CONFIG_NAMING}}

## Development Workflow

### Essential Commands
```bash
# Install dependencies
{{INSTALL_CMD}}

# Start development
{{DEV_CMD}}

# Run tests (ALWAYS run after changes)
{{TEST_CMD}}

# Type checking (MUST pass before considering task complete)
{{TYPECHECK_CMD}}

# Linting (MUST pass before considering task complete)
{{LINT_CMD}}

# Format code
{{FORMAT_CMD}}

# Build for production
{{BUILD_CMD}}
```

### Git Workflow
- **Branch naming**: {{BRANCH_NAMING}}
- **Commit style**: {{COMMIT_STYLE}}
- **Never commit**: {{IGNORE_FILES}}
- **Always test**: Run tests before marking any task as complete

## Code Standards

### Style Guidelines
- **Indentation**: {{INDENTATION}} spaces
- **Line length**: {{LINE_LENGTH}} characters
- **Quotes**: {{QUOTE_STYLE}} (be consistent)
- **Semicolons**: {{SEMICOLONS}}
- **Trailing commas**: {{TRAILING_COMMAS}}

### Best Practices
- Check existing patterns before implementing new features
- Use existing utilities and components when available
- Follow established error handling patterns
- Maintain consistent import ordering
- Add types/interfaces for all data structures
- Make commits frequently and before each new change. 

## Architecture Decisions

### Database/Persistence
- **Database Type**: {{DATABASE_TYPE}}
- **ORM/Query Builder**: {{ORM_CHOICE}}
- **Migration Tool**: {{MIGRATION_TOOL}}
- **Schema Location**: {{SCHEMA_LOCATION}}

### State Management
- **Library**: {{STATE_LIBRARY}}
- **Pattern**: {{STATE_PATTERN}}
- **Conventions**: {{STATE_CONVENTIONS}}

### API Communication
- **Base URL**: {{API_BASE_URL}}
- **Auth Method**: {{AUTH_METHOD}}
- **Error Format**: {{ERROR_FORMAT}}
- **Request Library**: {{REQUEST_LIBRARY}}

### Testing Strategy
- **Framework**: {{TEST_FRAMEWORK}}
- **Coverage Target**: {{COVERAGE_TARGET}}%
- **Test Location**: {{TEST_LOCATION}}
- **Naming**: {{TEST_FILE_PATTERN}}

## Error Handling

### Expected Behaviors
- Validate inputs before processing
- Provide meaningful error messages
- Log errors appropriately (never log sensitive data)
- Gracefully degrade functionality
- Show user-friendly error states

### Common Issues
{{COMMON_ISSUES}}

## Performance Considerations
- **Bundle size limits**: {{BUNDLE_SIZE_LIMIT}}
- **Load time targets**: {{LOAD_TIME_TARGET}}
- **Optimization strategies**: {{OPTIMIZATION_STRATEGIES}}
- **Performance monitoring**: {{PERF_MONITORING}}

## Security Requirements
- Input validation on all user data
- XSS prevention through proper escaping
- CSRF protection enabled
- Secure headers configured
- No secrets in code (use environment variables)

## Accessibility Standards
- WCAG 2.1 AA compliance
- Keyboard navigation for all features
- Screen reader compatible
- Proper ARIA labels
- Color contrast ratios met

## Dependencies

### Core Dependencies
```json
{
  "dependencies": {
{{CORE_DEPENDENCIES}}
  }
}
```

### Development Dependencies
```json
{
  "devDependencies": {
{{DEV_DEPENDENCIES}}
  }
}
```

## Environment Variables
```bash
# Required variables
{{REQUIRED_ENV_VARS}}

# Optional variables
{{OPTIONAL_ENV_VARS}}
```

## Deployment

### Build Process
1. Run tests: `npm test`
2. Type check: `npm run typecheck`
3. Lint: `npm run lint`
4. Build: `npm run build`
5. Deploy: [Deployment command/process]

### Environments
- **Development**: {{DEV_ENV}}
- **Staging**: {{STAGING_ENV}}
- **Production**: {{PROD_ENV}}

## Troubleshooting

### Common Problems
1. **Problem**: [Description]
   **Solution**: [How to fix]

2. **Problem**: [Description]
   **Solution**: [How to fix]

### Debug Commands
```bash
# Check node version
node --version

# Clear cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json && npm install
```

## Project-Specific Notes
<!-- Important context about this specific project -->

## Common Patterns
{{COMMON_PATTERNS}}

## Monitoring & Logging
- **Logging Library**: {{LOGGING_LIBRARY}}
- **Log Levels**: {{LOG_LEVELS}}
- **Error Tracking**: {{ERROR_TRACKING}}
- **Analytics**: {{ANALYTICS_TOOLS}}

## Resources
- **Documentation**: {{DOCS_LINK}}
- **Design System**: {{DESIGN_SYSTEM_LINK}}
- **API Docs**: {{API_DOCS_LINK}}
- **CI/CD**: {{CICD_LINK}}

---
*Last updated: {{LAST_UPDATED}}*
*Template Version: 2.1*