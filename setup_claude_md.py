#!/usr/bin/env python3
"""
CLAUDE.md Setup Tool
Interacts with users to gather project information and generate a customized CLAUDE.md file.
"""

import os
import re
import json
import subprocess
from datetime import date
from pathlib import Path
from typing import Dict, Optional

class ClaudeMdSetup:
    def __init__(self):
        self.template_path = Path(__file__).parent / "CLAUDE.md"
        self.placeholders = {}
        self.project_root = Path.cwd()
        
    def detect_project_info(self) -> Dict[str, str]:
        """Auto-detect project information from existing files."""
        detected = {}
        
        # Check for package.json (Node.js)
        package_json = self.project_root / "package.json"
        if package_json.exists():
            with open(package_json) as f:
                pkg = json.load(f)
                detected['package_manager'] = 'npm'
                detected['project_name'] = pkg.get('name', '')
                detected['project_description'] = pkg.get('description', '')
                
                # Detect test framework
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                if 'jest' in deps:
                    detected['test_framework'] = 'Jest'
                elif 'vitest' in deps:
                    detected['test_framework'] = 'Vitest'
                elif 'mocha' in deps:
                    detected['test_framework'] = 'Mocha'
                    
                # Detect frontend framework
                if 'react' in deps:
                    detected['framework'] = 'React'
                elif 'vue' in deps:
                    detected['framework'] = 'Vue'
                elif 'svelte' in deps:
                    detected['framework'] = 'Svelte'
                elif '@angular/core' in deps:
                    detected['framework'] = 'Angular'
                    
        # Check for requirements.txt or pyproject.toml (Python)
        elif (self.project_root / "requirements.txt").exists() or (self.project_root / "pyproject.toml").exists():
            detected['package_manager'] = 'pip'
            detected['primary_language'] = 'Python'
            
            pyproject = self.project_root / "pyproject.toml"
            if pyproject.exists():
                # Basic TOML parsing for project name
                content = pyproject.read_text()
                match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    detected['project_name'] = match.group(1)
                    
        # Check for Cargo.toml (Rust)
        elif (self.project_root / "Cargo.toml").exists():
            detected['package_manager'] = 'cargo'
            detected['primary_language'] = 'Rust'
            
        # Check for go.mod (Go)
        elif (self.project_root / "go.mod").exists():
            detected['package_manager'] = 'go'
            detected['primary_language'] = 'Go'
            
        # Detect git info
        try:
            remote = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], 
                                           stderr=subprocess.DEVNULL).decode().strip()
            if 'github.com' in remote:
                detected['git_platform'] = 'GitHub'
            elif 'gitlab.com' in remote:
                detected['git_platform'] = 'GitLab'
        except:
            pass
            
        return detected
    
    def get_directory_structure(self) -> str:
        """Generate a tree view of the project structure."""
        def create_tree(path: Path, prefix: str = "", is_last: bool = True) -> str:
            if path.name in ['.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build']:
                return ""
                
            result = ""
            connector = "└── " if is_last else "├── "
            result += prefix + connector + path.name
            
            if path.is_dir():
                result += "/\n"
                children = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
                children = [c for c in children if not c.name.startswith('.')][:10]  # Limit depth
                
                for i, child in enumerate(children):
                    extension = "    " if is_last else "│   "
                    subtree = create_tree(child, prefix + extension, i == len(children) - 1)
                    if subtree:
                        result += subtree
            else:
                result += "\n"
                
            return result
            
        return self.project_root.name + "/\n" + "".join(
            create_tree(child, "", i == len(list(self.project_root.iterdir())) - 1)
            for i, child in enumerate(sorted(self.project_root.iterdir(), 
                                           key=lambda x: (not x.is_dir(), x.name)))
            if not child.name.startswith('.')
        )
    
    def gather_project_info(self) -> None:
        """Gather all project information through prompts."""
        detected = self.detect_project_info()
        
        print("🚀 CLAUDE.md Setup Tool")
        print("=" * 50)
        print("I'll help you create a comprehensive CLAUDE.md file for your project.")
        print("I've auto-detected some information. Press Enter to accept defaults.\n")
        
        # Basic Info
        self.placeholders['PROJECT_NAME'] = input(f"Project name [{detected.get('project_name', self.project_root.name)}]: ") or detected.get('project_name', self.project_root.name)
        self.placeholders['PROJECT_DESCRIPTION'] = input(f"Project description [{detected.get('project_description', '')}]: ") or detected.get('project_description', 'A software project')
        
        # Tech Stack
        print("\n📚 Technology Stack")
        framework = detected.get('framework', '')
        self.placeholders['TECH_STACK'] = input(f"Tech stack (e.g., React, Node.js, PostgreSQL) [{framework}]: ") or framework
        self.placeholders['PRIMARY_LANGUAGE'] = input(f"Primary language [{detected.get('primary_language', 'TypeScript')}]: ") or detected.get('primary_language', 'TypeScript')
        self.placeholders['PROJECT_STATUS'] = input("Project status (Development/Production/Maintenance) [Development]: ") or "Development"
        
        # Directory Structure
        print("\n📁 Directory Structure")
        print("Current structure detected:")
        print(self.get_directory_structure()[:500] + "..." if len(self.get_directory_structure()) > 500 else self.get_directory_structure())
        
        use_custom = input("\nUse custom directory structure? (y/N): ").lower() == 'y'
        if use_custom:
            self.placeholders['SOURCE_DIR'] = input("Source directory name [src]: ") or "src"
            self.placeholders['COMPONENTS_DIR'] = input("Components directory [components]: ") or "components"
            self.placeholders['SERVICES_DIR'] = input("Services directory [services]: ") or "services"
            self.placeholders['UTILS_DIR'] = input("Utils directory [utils]: ") or "utils"
            self.placeholders['TESTS_DIR'] = input("Tests directory [tests]: ") or "tests"
            self.placeholders['DOCS_DIR'] = input("Docs directory [docs]: ") or "docs"
            self.placeholders['CONFIG_DIR'] = input("Config directory [config]: ") or "config"
            self.placeholders['SCRIPTS_DIR'] = input("Scripts directory [scripts]: ") or "scripts"
            
            self.placeholders['COMPONENTS_DESC'] = input("Components description [UI components]: ") or "UI components"
            self.placeholders['SERVICES_DESC'] = input("Services description [Business logic]: ") or "Business logic"
            self.placeholders['UTILS_DESC'] = input("Utils description [Utilities]: ") or "Utilities"
            self.placeholders['TESTS_DESC'] = input("Tests description [Test files]: ") or "Test files"
        else:
            # Use defaults
            self.placeholders.update({
                'SOURCE_DIR': 'src',
                'COMPONENTS_DIR': 'components',
                'SERVICES_DIR': 'services',
                'UTILS_DIR': 'utils',
                'TESTS_DIR': 'tests',
                'DOCS_DIR': 'docs',
                'CONFIG_DIR': 'config',
                'SCRIPTS_DIR': 'scripts',
                'COMPONENTS_DESC': 'UI components',
                'SERVICES_DESC': 'Business logic',
                'UTILS_DESC': 'Utilities',
                'TESTS_DESC': 'Test files'
            })
        
        # File Naming
        print("\n📝 File Naming Conventions")
        lang = self.placeholders['PRIMARY_LANGUAGE'].lower()
        if 'typescript' in lang or 'javascript' in lang:
            self.placeholders['COMPONENT_NAMING'] = input("Component naming [PascalCase.tsx]: ") or "PascalCase.tsx"
            self.placeholders['COMPONENT_EXAMPLE'] = input("Component example [Button.tsx]: ") or "Button.tsx"
            self.placeholders['UTILITY_NAMING'] = input("Utility naming [camelCase.ts]: ") or "camelCase.ts"
            self.placeholders['UTILITY_EXAMPLE'] = input("Utility example [formatters.ts]: ") or "formatters.ts"
            self.placeholders['TEST_NAMING'] = input("Test naming [*.test.ts]: ") or "*.test.ts"
            self.placeholders['STYLE_NAMING'] = input("Style naming [*.module.css]: ") or "*.module.css"
        elif 'python' in lang:
            self.placeholders['COMPONENT_NAMING'] = input("Module naming [snake_case.py]: ") or "snake_case.py"
            self.placeholders['COMPONENT_EXAMPLE'] = input("Module example [user_service.py]: ") or "user_service.py"
            self.placeholders['UTILITY_NAMING'] = input("Utility naming [snake_case.py]: ") or "snake_case.py"
            self.placeholders['UTILITY_EXAMPLE'] = input("Utility example [helpers.py]: ") or "helpers.py"
            self.placeholders['TEST_NAMING'] = input("Test naming [test_*.py]: ") or "test_*.py"
            self.placeholders['STYLE_NAMING'] = "N/A"
        else:
            self.placeholders['COMPONENT_NAMING'] = input("Component naming: ") or "PascalCase"
            self.placeholders['COMPONENT_EXAMPLE'] = input("Component example: ") or "Component"
            self.placeholders['UTILITY_NAMING'] = input("Utility naming: ") or "camelCase"
            self.placeholders['UTILITY_EXAMPLE'] = input("Utility example: ") or "utility"
            self.placeholders['TEST_NAMING'] = input("Test naming: ") or "*.test.*"
            self.placeholders['STYLE_NAMING'] = input("Style naming: ") or "*.css"
            
        self.placeholders['CONFIG_NAMING'] = input("Config naming [kebab-case.json]: ") or "kebab-case.json"
        
        # Commands
        print("\n⚡ Essential Commands")
        pkg_mgr = detected.get('package_manager', 'npm')
        if pkg_mgr == 'npm':
            self.placeholders['INSTALL_CMD'] = "npm install"
            self.placeholders['DEV_CMD'] = input("Dev command [npm run dev]: ") or "npm run dev"
            self.placeholders['TEST_CMD'] = input("Test command [npm test]: ") or "npm test"
            self.placeholders['BUILD_CMD'] = input("Build command [npm run build]: ") or "npm run build"
            self.placeholders['LINT_CMD'] = input("Lint command [npm run lint]: ") or "npm run lint"
            self.placeholders['FORMAT_CMD'] = input("Format command [npm run format]: ") or "npm run format"
            self.placeholders['TYPECHECK_CMD'] = input("Type check command [npm run typecheck]: ") or "npm run typecheck"
        elif pkg_mgr == 'pip':
            self.placeholders['INSTALL_CMD'] = "pip install -r requirements.txt"
            self.placeholders['DEV_CMD'] = input("Dev command [python main.py]: ") or "python main.py"
            self.placeholders['TEST_CMD'] = input("Test command [pytest]: ") or "pytest"
            self.placeholders['BUILD_CMD'] = input("Build command [python setup.py build]: ") or "python setup.py build"
            self.placeholders['LINT_CMD'] = input("Lint command [ruff check]: ") or "ruff check"
            self.placeholders['FORMAT_CMD'] = input("Format command [black .]: ") or "black ."
            self.placeholders['TYPECHECK_CMD'] = input("Type check command [mypy .]: ") or "mypy ."
        else:
            self.placeholders['INSTALL_CMD'] = input("Install command: ") or f"{pkg_mgr} install"
            self.placeholders['DEV_CMD'] = input("Dev command: ") or f"{pkg_mgr} run dev"
            self.placeholders['TEST_CMD'] = input("Test command: ") or f"{pkg_mgr} test"
            self.placeholders['BUILD_CMD'] = input("Build command: ") or f"{pkg_mgr} build"
            self.placeholders['LINT_CMD'] = input("Lint command: ") or f"{pkg_mgr} lint"
            self.placeholders['FORMAT_CMD'] = input("Format command: ") or f"{pkg_mgr} format"
            self.placeholders['TYPECHECK_CMD'] = input("Type check command: ") or f"{pkg_mgr} typecheck"
        
        # Style Guidelines
        print("\n🎨 Code Style")
        self.placeholders['INDENTATION'] = input("Indentation spaces [2]: ") or "2"
        self.placeholders['LINE_LENGTH'] = input("Max line length [100]: ") or "100"
        self.placeholders['QUOTE_STYLE'] = input("Quote style (Single/Double) [Single]: ") or "Single"
        self.placeholders['SEMICOLONS'] = input("Semicolons (Always/Never) [Never]: ") or "Never"
        self.placeholders['TRAILING_COMMAS'] = input("Trailing commas (Yes/No) [Yes]: ") or "Yes"
        
        # Git Workflow
        print("\n🔀 Git Workflow")
        self.placeholders['BRANCH_NAMING'] = input("Branch naming [feature/*, fix/*, chore/*]: ") or "feature/*, fix/*, chore/*"
        self.placeholders['COMMIT_STYLE'] = input("Commit style [type(scope): description]: ") or "type(scope): description"
        self.placeholders['IGNORE_FILES'] = input("Never commit [.env, node_modules, dist]: ") or ".env files, node_modules, dist/build folders"
        
        # Architecture
        print("\n🏗️ Architecture")
        
        # State Management (for frontend)
        if any(fw in self.placeholders['TECH_STACK'].lower() for fw in ['react', 'vue', 'angular', 'svelte']):
            self.placeholders['STATE_LIBRARY'] = input("State management library [Context API]: ") or "Context API"
            self.placeholders['STATE_PATTERN'] = input("State pattern [Component State]: ") or "Component State"
            self.placeholders['STATE_CONVENTIONS'] = input("State conventions: ") or "Local state for components, Context for shared state"
        else:
            self.placeholders['STATE_LIBRARY'] = "N/A"
            self.placeholders['STATE_PATTERN'] = "N/A"
            self.placeholders['STATE_CONVENTIONS'] = "N/A"
        
        # Database
        has_db = input("\nDoes this project use a database? (y/N): ").lower() == 'y'
        if has_db:
            self.placeholders['DATABASE_TYPE'] = input("Database type [PostgreSQL]: ") or "PostgreSQL"
            self.placeholders['ORM_CHOICE'] = input("ORM/Query builder [Prisma]: ") or "Prisma"
            self.placeholders['MIGRATION_TOOL'] = input("Migration tool [Built-in ORM migrations]: ") or "Built-in ORM migrations"
            self.placeholders['SCHEMA_LOCATION'] = input("Schema location [prisma/schema.prisma]: ") or "prisma/schema.prisma"
        else:
            self.placeholders['DATABASE_TYPE'] = "None"
            self.placeholders['ORM_CHOICE'] = "N/A"
            self.placeholders['MIGRATION_TOOL'] = "N/A"
            self.placeholders['SCHEMA_LOCATION'] = "N/A"
        
        # API
        has_api = input("\nDoes this project communicate with APIs? (y/N): ").lower() == 'y'
        if has_api:
            self.placeholders['API_BASE_URL'] = input("API base URL env var [process.env.API_URL]: ") or "process.env.API_URL"
            self.placeholders['AUTH_METHOD'] = input("Auth method [JWT]: ") or "JWT"
            self.placeholders['ERROR_FORMAT'] = input("Error format [{ error: string, code: number }]: ") or "{ error: string, code: number }"
            self.placeholders['REQUEST_LIBRARY'] = input("Request library [fetch]: ") or "fetch"
        else:
            self.placeholders['API_BASE_URL'] = "N/A"
            self.placeholders['AUTH_METHOD'] = "N/A"
            self.placeholders['ERROR_FORMAT'] = "N/A"
            self.placeholders['REQUEST_LIBRARY'] = "N/A"
        
        # Testing
        print("\n🧪 Testing")
        self.placeholders['TEST_FRAMEWORK'] = input(f"Test framework [{detected.get('test_framework', 'Jest')}]: ") or detected.get('test_framework', 'Jest')
        self.placeholders['COVERAGE_TARGET'] = input("Coverage target % [80]: ") or "80"
        self.placeholders['TEST_LOCATION'] = input("Test location [Alongside code]: ") or "Alongside code"
        self.placeholders['TEST_FILE_PATTERN'] = input("Test file pattern [*.test.ts]: ") or "*.test.ts"
        
        # Performance
        print("\n⚡ Performance")
        self.placeholders['BUNDLE_SIZE_LIMIT'] = input("Bundle size limit [< 500KB]: ") or "< 500KB"
        self.placeholders['LOAD_TIME_TARGET'] = input("Load time target [< 3s]: ") or "< 3s"
        self.placeholders['OPTIMIZATION_STRATEGIES'] = input("Optimization strategies [Code splitting, lazy loading]: ") or "Code splitting, lazy loading"
        self.placeholders['PERF_MONITORING'] = input("Performance monitoring [Web Vitals]: ") or "Web Vitals"
        
        # Monitoring
        print("\n📊 Monitoring & Logging")
        self.placeholders['LOGGING_LIBRARY'] = input("Logging library [console]: ") or "console"
        self.placeholders['LOG_LEVELS'] = input("Log levels [error, warn, info, debug]: ") or "error, warn, info, debug"
        self.placeholders['ERROR_TRACKING'] = input("Error tracking [None]: ") or "None"
        self.placeholders['ANALYTICS_TOOLS'] = input("Analytics tools [None]: ") or "None"
        
        # Environment
        print("\n🌍 Environment Variables")
        self.placeholders['REQUIRED_ENV_VARS'] = input("Required env vars (comma-separated): ") or "NODE_ENV=development|production"
        self.placeholders['OPTIONAL_ENV_VARS'] = input("Optional env vars (comma-separated): ") or "DEBUG=true|false"
        
        # Deployment
        print("\n🚀 Deployment")
        self.placeholders['DEV_ENV'] = input("Development URL/details [http://localhost:3000]: ") or "http://localhost:3000"
        self.placeholders['STAGING_ENV'] = input("Staging URL/details [N/A]: ") or "N/A"
        self.placeholders['PROD_ENV'] = input("Production URL/details [N/A]: ") or "N/A"
        
        # Resources
        print("\n📚 Resources")
        self.placeholders['DOCS_LINK'] = input("Documentation link [N/A]: ") or "N/A"
        self.placeholders['DESIGN_SYSTEM_LINK'] = input("Design system link [N/A]: ") or "N/A"
        self.placeholders['API_DOCS_LINK'] = input("API docs link [N/A]: ") or "N/A"
        self.placeholders['CICD_LINK'] = input("CI/CD link [N/A]: ") or "N/A"
        
        # Common patterns and issues
        print("\n💡 Additional Information")
        self.placeholders['COMMON_PATTERNS'] = input("Common patterns (optional): ") or "- Follow existing component patterns\n- Use custom hooks for shared logic\n- Implement proper error boundaries"
        self.placeholders['COMMON_ISSUES'] = input("Known issues/gotchas (optional): ") or "- None currently documented"
        
        # Dependencies - simplified
        self.placeholders['CORE_DEPENDENCIES'] = '    // Core dependencies listed in package.json'
        self.placeholders['DEV_DEPENDENCIES'] = '    // Dev dependencies listed in package.json'
        
        # Metadata
        self.placeholders['LAST_UPDATED'] = date.today().isoformat()
    
    def generate_claude_md(self) -> str:
        """Generate the final CLAUDE.md content."""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found at {self.template_path}")
            
        content = self.template_path.read_text()
        
        # Replace all placeholders
        for key, value in self.placeholders.items():
            # Handle multiline values properly
            if '\n' in str(value):
                value = value.replace('\n', '\n')
            content = content.replace(f"{{{{{key}}}}}", str(value))
        
        return content
    
    def save_claude_md(self, output_path: Optional[Path] = None) -> None:
        """Save the generated CLAUDE.md file."""
        if output_path is None:
            output_path = self.project_root / "CLAUDE.md"
            
        content = self.generate_claude_md()
        
        # Backup existing file if present
        if output_path.exists():
            backup_path = output_path.with_suffix('.md.backup')
            print(f"\n⚠️  Backing up existing CLAUDE.md to {backup_path}")
            output_path.rename(backup_path)
        
        output_path.write_text(content)
        print(f"\n✅ Successfully created {output_path}")
        print("\n📋 Next steps:")
        print("1. Review the generated CLAUDE.md file")
        print("2. Update any placeholder values that need more detail")
        print("3. Add project-specific notes in the 'Project-Specific Notes' section")
        print("4. Commit the file to your repository")

def main():
    """Main entry point."""
    setup = ClaudeMdSetup()
    
    try:
        setup.gather_project_info()
        setup.save_claude_md()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())