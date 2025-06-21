# CI/CD Pipeline Configuration

## GitHub Actions Workflow
```yaml
name: {{WORKFLOW_NAME}}

on:
  {{TRIGGERS}}

jobs:
  {{JOBS}}
```

## Test Job
```yaml
test:
  runs-on: {{RUNNER_OS}}
  steps:
    {{TEST_STEPS}}
```

## Build Job  
```yaml
build:
  runs-on: {{RUNNER_OS}}
  needs: test
  steps:
    {{BUILD_STEPS}}
```

## Deploy Job
```yaml
deploy:
  runs-on: {{RUNNER_OS}}
  needs: build
  if: github.ref == 'refs/heads/main'
  steps:
    {{DEPLOY_STEPS}}
```

## Environment Variables
```yaml
env:
  {{CI_ENV_VARS}}
```

## Secrets Required
{{REQUIRED_SECRETS}}

## Branch Protection Rules
{{BRANCH_PROTECTION}}

## Additional Workflows
{{ADDITIONAL_WORKFLOWS}}