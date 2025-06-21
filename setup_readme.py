#!/usr/bin/env python3
"""
README.md Setup Tool
Interactive tool to generate comprehensive README.md files for projects.
"""

import os
import re
import json
import subprocess
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import urllib.parse

class ReadmeGenerator:
    def __init__(self):
        self.template_path = Path(__file__).parent / "README_template.md"
        self.placeholders = {}
        self.project_root = Path.cwd()
        self.detected_info = {}
        
    def detect_project_info(self) -> Dict[str, str]:
        """Auto-detect project information from existing files."""
        detected = {}
        
        # Get project name from directory
        detected['project_name'] = self.project_root.name
        
        # Check for package.json (Node.js)
        package_json = self.project_root / "package.json"
        if package_json.exists():
            with open(package_json) as f:
                pkg = json.load(f)
                detected['project_name'] = pkg.get('name', detected['project_name'])
                detected['version'] = pkg.get('version', '0.1.0')
                detected['description'] = pkg.get('description', '')
                detected['author'] = pkg.get('author', '')
                detected['license'] = pkg.get('license', 'MIT')
                detected['homepage'] = pkg.get('homepage', '')
                
                # Detect scripts
                scripts = pkg.get('scripts', {})
                detected['scripts'] = scripts
                detected['has_tests'] = any('test' in s for s in scripts.keys())
                detected['has_build'] = any('build' in s for s in scripts.keys())
                
                # Detect dependencies
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                detected['dependencies'] = deps
                
                # Framework detection
                if 'react' in deps:
                    detected['framework'] = 'React'
                    detected['language'] = 'JavaScript/TypeScript'
                elif 'vue' in deps:
                    detected['framework'] = 'Vue'
                    detected['language'] = 'JavaScript/TypeScript'
                elif 'express' in deps:
                    detected['framework'] = 'Express'
                    detected['language'] = 'Node.js'
                elif '@angular/core' in deps:
                    detected['framework'] = 'Angular'
                    detected['language'] = 'TypeScript'
                    
        # Check for Python files
        elif (self.project_root / "setup.py").exists() or (self.project_root / "pyproject.toml").exists():
            detected['language'] = 'Python'
            if (self.project_root / "requirements.txt").exists():
                detected['has_requirements'] = True
                
        # Check for Cargo.toml (Rust)
        elif (self.project_root / "Cargo.toml").exists():
            detected['language'] = 'Rust'
            
        # Check for go.mod (Go)
        elif (self.project_root / "go.mod").exists():
            detected['language'] = 'Go'
            
        # Git detection
        try:
            # Get remote URL
            remote = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], 
                                           stderr=subprocess.DEVNULL).decode().strip()
            detected['repo_url'] = remote
            
            # Parse GitHub/GitLab URL
            if 'github.com' in remote:
                match = re.search(r'github\.com[:/]([^/]+)/([^/.]+)', remote)
                if match:
                    detected['github_user'] = match.group(1)
                    detected['github_repo'] = match.group(2).replace('.git', '')
                    
            # Get current branch
            branch = subprocess.check_output(['git', 'branch', '--show-current'],
                                           stderr=subprocess.DEVNULL).decode().strip()
            detected['default_branch'] = branch or 'main'
            
            # Check for existing tags
            try:
                tags = subprocess.check_output(['git', 'tag'], 
                                             stderr=subprocess.DEVNULL).decode().strip()
                detected['has_releases'] = bool(tags)
            except:
                detected['has_releases'] = False
                
        except:
            pass
            
        # Check for CI/CD files
        if (self.project_root / ".github/workflows").exists():
            detected['ci_platform'] = 'GitHub Actions'
        elif (self.project_root / ".gitlab-ci.yml").exists():
            detected['ci_platform'] = 'GitLab CI'
        elif (self.project_root / ".travis.yml").exists():
            detected['ci_platform'] = 'Travis CI'
            
        # Check for Docker
        if (self.project_root / "Dockerfile").exists():
            detected['has_docker'] = True
            
        # Check for existing docs
        if (self.project_root / "docs").exists():
            detected['has_docs'] = True
            
        return detected
    
    def generate_badges(self, info: Dict[str, str]) -> str:
        """Generate shield.io badges based on project info."""
        badges = []
        
        # Version badge
        if info.get('version'):
            badges.append(f"![Version](https://img.shields.io/badge/version-{info['version']}-blue.svg)")
        
        # Language badge
        if info.get('language'):
            lang = urllib.parse.quote(info['language'])
            badges.append(f"![Language](https://img.shields.io/badge/language-{lang}-brightgreen.svg)")
        
        # License badge
        if info.get('license'):
            badges.append(f"![License](https://img.shields.io/badge/license-{info['license']}-green.svg)")
        
        # GitHub specific badges
        if info.get('github_user') and info.get('github_repo'):
            user = info['github_user']
            repo = info['github_repo']
            
            # Stars
            badges.append(f"![GitHub stars](https://img.shields.io/github/stars/{user}/{repo}.svg)")
            
            # Issues
            badges.append(f"![GitHub issues](https://img.shields.io/github/issues/{user}/{repo}.svg)")
            
            # Build status (if CI detected)
            if info.get('ci_platform') == 'GitHub Actions':
                badges.append(f"![Build Status](https://github.com/{user}/{repo}/workflows/CI/badge.svg)")
        
        # Test coverage (placeholder)
        if info.get('has_tests'):
            badges.append("![Coverage](https://img.shields.io/badge/coverage-80%25-yellowgreen.svg)")
        
        return '\n'.join(badges) if badges else "![Status](https://img.shields.io/badge/status-active-success.svg)"
    
    def get_directory_structure(self, max_depth: int = 3) -> str:
        """Generate a tree view of the project structure."""
        def create_tree(path: Path, prefix: str = "", depth: int = 0) -> List[str]:
            if depth > max_depth:
                return []
                
            # Skip common directories
            skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 
                        'dist', 'build', '.next', 'coverage', '.pytest_cache'}
            
            if path.name in skip_dirs:
                return []
                
            items = []
            
            try:
                children = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
                # Filter hidden files and limit number of items shown
                children = [c for c in children if not c.name.startswith('.')][:15]
                
                for i, child in enumerate(children):
                    is_last = i == len(children) - 1
                    current = "└── " if is_last else "├── "
                    
                    if child.is_dir():
                        items.append(f"{prefix}{current}{child.name}/")
                        if depth < max_depth:
                            extension = "    " if is_last else "│   "
                            items.extend(create_tree(child, prefix + extension, depth + 1))
                    else:
                        # Add file size for context
                        size = child.stat().st_size
                        if size < 1024:
                            size_str = f" ({size}B)"
                        elif size < 1024 * 1024:
                            size_str = f" ({size//1024}KB)"
                        else:
                            size_str = f" ({size//1024//1024}MB)"
                        
                        items.append(f"{prefix}{current}{child.name}")
                        
            except PermissionError:
                pass
                
            return items
        
        tree_lines = [f"{self.project_root.name}/"]
        tree_lines.extend(create_tree(self.project_root))
        
        return '\n'.join(tree_lines[:50])  # Limit total lines
    
    def gather_project_info(self) -> None:
        """Gather project information through interactive prompts."""
        self.detected_info = self.detect_project_info()
        
        print("📘 README.md Generator")
        print("=" * 50)
        print("I'll help you create a comprehensive README for your project.")
        print("Press Enter to accept auto-detected values.\n")
        
        # Basic Information
        print("📋 Basic Information")
        self.placeholders['PROJECT_NAME'] = input(
            f"Project name [{self.detected_info.get('project_name', 'my-project')}]: "
        ) or self.detected_info.get('project_name', 'my-project')
        
        self.placeholders['PROJECT_TAGLINE'] = input(
            "Project tagline (one-liner): "
        ) or f"A {self.detected_info.get('language', 'software')} project"
        
        desc = self.detected_info.get('description', '')
        self.placeholders['PROJECT_DESCRIPTION'] = input(
            f"Project description [{desc[:50] + '...' if len(desc) > 50 else desc}]: "
        ) or desc or "A comprehensive description of what this project does and its main purpose."
        
        # Badges
        print("\n🏷️ Badges")
        auto_badges = self.generate_badges(self.detected_info)
        print("Auto-generated badges preview:")
        print(auto_badges[:200] + "..." if len(auto_badges) > 200 else auto_badges)
        use_auto = input("\nUse auto-generated badges? (Y/n): ").lower() != 'n'
        
        if use_auto:
            self.placeholders['BADGES'] = auto_badges
        else:
            self.placeholders['BADGES'] = input("Custom badges (markdown): ") or ""
        
        # Motivation
        print("\n💡 Project Motivation")
        self.placeholders['PROJECT_MOTIVATION'] = input(
            "Why was this project created? (problem it solves): "
        ) or "This project was created to solve specific challenges in the domain."
        
        # Key Benefits
        print("\n✅ Key Benefits (enter empty line to finish)")
        benefits = []
        while True:
            benefit = input(f"Benefit {len(benefits) + 1}: ")
            if not benefit:
                break
            benefits.append(f"- {benefit}")
        
        self.placeholders['KEY_BENEFITS'] = '\n'.join(benefits) if benefits else "- Efficient and reliable\n- Easy to use\n- Well documented"
        
        # Features
        print("\n✨ Features (enter empty line to finish)")
        features = []
        while True:
            feature = input(f"Feature {len(features) + 1}: ")
            if not feature:
                break
            features.append(f"- **{feature.split()[0]}**: {' '.join(feature.split()[1:])}" if len(feature.split()) > 1 else f"- {feature}")
        
        self.placeholders['FEATURES_LIST'] = '\n'.join(features) if features else "- **Core Feature**: Main functionality\n- **Another Feature**: Additional capability"
        
        # Demo Section
        print("\n🚀 Demo")
        has_demo = input("Do you have a live demo? (y/N): ").lower() == 'y'
        if has_demo:
            demo_url = input("Demo URL: ")
            demo_screenshot = input("Screenshot URL (optional): ")
            demo_section = f"[Live Demo]({demo_url})"
            if demo_screenshot:
                demo_section += f"\n\n![Demo Screenshot]({demo_screenshot})"
        else:
            demo_section = "Coming soon..."
        self.placeholders['DEMO_SECTION'] = demo_section
        
        # Prerequisites
        print("\n📦 Prerequisites")
        prereqs = []
        
        if self.detected_info.get('language') == 'JavaScript/TypeScript' or 'node' in self.detected_info.get('language', '').lower():
            prereqs.append("- Node.js (v14 or higher)")
            prereqs.append("- npm or yarn")
        elif self.detected_info.get('language') == 'Python':
            prereqs.append("- Python 3.8 or higher")
            prereqs.append("- pip")
        elif self.detected_info.get('language') == 'Rust':
            prereqs.append("- Rust 1.56 or higher")
            prereqs.append("- Cargo")
        elif self.detected_info.get('language') == 'Go':
            prereqs.append("- Go 1.16 or higher")
        
        custom_prereq = input("Additional prerequisites (comma-separated): ")
        if custom_prereq:
            prereqs.extend([f"- {p.strip()}" for p in custom_prereq.split(',')])
        
        self.placeholders['PREREQUISITES'] = '\n'.join(prereqs) if prereqs else "- No special prerequisites"
        
        # Repository URL
        self.placeholders['REPO_URL'] = input(
            f"Repository URL [{self.detected_info.get('repo_url', 'https://github.com/user/repo')}]: "
        ) or self.detected_info.get('repo_url', 'https://github.com/user/repo')
        
        # Installation
        print("\n🔧 Installation")
        scripts = self.detected_info.get('scripts', {})
        
        if 'npm' in str(self.detected_info):
            self.placeholders['INSTALL_COMMAND'] = "npm install"
        elif self.detected_info.get('has_requirements'):
            self.placeholders['INSTALL_COMMAND'] = "pip install -r requirements.txt"
        else:
            self.placeholders['INSTALL_COMMAND'] = input("Install command: ") or "# Install dependencies"
        
        # Environment setup
        has_env = (self.project_root / ".env.example").exists() or input("\nDoes your project use environment variables? (y/N): ").lower() == 'y'
        
        if has_env:
            self.placeholders['ENV_SETUP_COMMAND'] = "cp .env.example .env"
            
            print("\nList environment variables (empty line to finish):")
            env_vars = []
            while True:
                var = input("Variable name: ")
                if not var:
                    break
                desc = input(f"  {var} description: ")
                env_vars.append(f"   # {var}: {desc}")
            
            self.placeholders['ENV_VARIABLES'] = '\n'.join(env_vars) if env_vars else "   # See .env.example for required variables"
        else:
            self.placeholders['ENV_SETUP_COMMAND'] = "# No environment setup needed"
            self.placeholders['ENV_VARIABLES'] = "# No environment variables required"
        
        # Usage
        print("\n💻 Usage")
        
        # Quick start command
        if 'start' in scripts:
            quick_start = "npm start"
        elif 'dev' in scripts:
            quick_start = "npm run dev"
        elif self.detected_info.get('language') == 'Python':
            quick_start = "python main.py"
        else:
            quick_start = input("Quick start command: ") or "./start.sh"
        
        self.placeholders['QUICK_START_COMMAND'] = quick_start
        
        # Basic example
        print("\nProvide a basic usage example (use ``` for code blocks):")
        print("(Enter 'DONE' on a new line when finished)")
        example_lines = []
        while True:
            line = input()
            if line == 'DONE':
                break
            example_lines.append(line)
        
        self.placeholders['BASIC_EXAMPLE'] = '\n'.join(example_lines) if example_lines else """```javascript
// Example usage
const myModule = require('my-module');
const result = myModule.doSomething();
console.log(result);
```"""
        
        # Advanced usage
        self.placeholders['ADVANCED_USAGE'] = "See the [documentation](docs/) for advanced usage examples."
        
        # Configuration
        print("\n⚙️ Configuration")
        self.placeholders['CONFIGURATION_DETAILS'] = input(
            "Configuration details (or press Enter for default): "
        ) or "Configuration can be done through environment variables or config files. See `.env.example` for available options."
        
        # API Reference
        print("\n📚 API Reference")
        has_api = input("Does your project have an API? (y/N): ").lower() == 'y'
        
        if has_api:
            api_type = input("API type (REST/GraphQL/Library): ") or "REST"
            if api_type.upper() == "REST":
                self.placeholders['API_REFERENCE'] = "### REST API Endpoints\n\nSee [API Documentation](docs/api.md) for detailed endpoint information."
            elif api_type.upper() == "GRAPHQL":
                self.placeholders['API_REFERENCE'] = "### GraphQL Schema\n\nSee [GraphQL Documentation](docs/graphql.md) for schema details."
            else:
                self.placeholders['API_REFERENCE'] = "### API Methods\n\nSee [API Documentation](docs/api.md) for detailed method documentation."
        else:
            self.placeholders['API_REFERENCE'] = "Not applicable for this project."
        
        # Development
        print("\n🛠️ Development")
        
        # Project structure
        print("\nGenerating project structure...")
        self.placeholders['PROJECT_STRUCTURE'] = self.get_directory_structure()
        
        # Dev setup
        dev_commands = []
        if scripts.get('dev'):
            dev_commands.append("npm run dev")
        elif scripts.get('watch'):
            dev_commands.append("npm run watch")
        
        additional_dev = input("\nAdditional dev setup commands (semicolon-separated): ")
        if additional_dev:
            dev_commands.extend(additional_dev.split(';'))
        
        self.placeholders['DEV_SETUP_COMMANDS'] = '\n'.join(dev_commands) if dev_commands else "# Start development server\nnpm run dev"
        
        # Code style
        self.placeholders['CODE_STYLE_GUIDE'] = input(
            "Code style guide (or Enter for default): "
        ) or "This project follows standard code style guidelines. Run `npm run lint` to check code style."
        
        # Available scripts
        if scripts:
            script_list = []
            for name, cmd in scripts.items():
                script_list.append(f"- `npm run {name}`: {cmd}")
            self.placeholders['AVAILABLE_SCRIPTS'] = '\n'.join(script_list)
        else:
            self.placeholders['AVAILABLE_SCRIPTS'] = "- `start`: Start the application\n- `test`: Run tests\n- `build`: Build for production"
        
        # Testing
        print("\n🧪 Testing")
        
        test_cmd = "npm test" if scripts.get('test') else input("Test command: ") or "npm test"
        self.placeholders['TEST_COMMAND'] = test_cmd
        
        coverage_cmd = "npm run coverage" if scripts.get('coverage') else "npm test -- --coverage"
        self.placeholders['COVERAGE_COMMAND'] = coverage_cmd
        
        self.placeholders['TESTING_STRATEGY'] = input(
            "Testing strategy (or Enter for default): "
        ) or "This project uses unit tests and integration tests. Tests are located in the `__tests__` directory."
        
        # Deployment
        print("\n📦 Deployment")
        
        build_cmd = "npm run build" if scripts.get('build') else input("Build command: ") or "npm run build"
        self.placeholders['BUILD_COMMAND'] = build_cmd
        
        # Deployment options
        deployment_options = []
        print("\nDeployment platforms (enter empty line to finish):")
        while True:
            platform = input("Platform: ")
            if not platform:
                break
            deployment_options.append(f"- **{platform}**: See [deployment/{platform.lower()}.md](docs/deployment/{platform.lower()}.md)")
        
        self.placeholders['DEPLOYMENT_OPTIONS'] = '\n'.join(deployment_options) if deployment_options else "- **Vercel**: `vercel deploy`\n- **Heroku**: `git push heroku main`\n- **Docker**: `docker-compose up -d`"
        
        self.placeholders['PRODUCTION_ENV_VARS'] = "See `.env.production.example` for production environment variables."
        
        # Development process
        self.placeholders['DEVELOPMENT_PROCESS'] = "1. Create a feature branch\n2. Make your changes\n3. Write/update tests\n4. Ensure all tests pass\n5. Submit a pull request"
        
        # License
        print("\n📄 License")
        self.placeholders['LICENSE_TYPE'] = input(
            f"License [{self.detected_info.get('license', 'MIT')}]: "
        ) or self.detected_info.get('license', 'MIT')
        
        # Author
        self.placeholders['AUTHOR'] = input(
            f"Author [{self.detected_info.get('author', 'Your Name')}]: "
        ) or self.detected_info.get('author', 'Your Name')
        
        # Support
        print("\n📞 Support")
        support_lines = []
        
        if self.detected_info.get('github_user') and self.detected_info.get('github_repo'):
            support_lines.append(f"- 🐛 [Report bugs]({self.repo_url}/issues)")
            support_lines.append(f"- 💡 [Request features]({self.repo_url}/issues)")
        
        email = input("Support email (optional): ")
        if email:
            support_lines.append(f"- 📧 Email: {email}")
        
        self.placeholders['SUPPORT_SECTION'] = '\n'.join(support_lines) if support_lines else "- Create an issue in the repository\n- Contact the maintainers"
        
        # Acknowledgments
        print("\n🙏 Acknowledgments")
        acks = []
        print("Add acknowledgments (empty line to finish):")
        while True:
            ack = input("Acknowledgment: ")
            if not ack:
                break
            acks.append(f"- {ack}")
        
        self.placeholders['ACKNOWLEDGMENTS'] = '\n'.join(acks) if acks else "- Thanks to all contributors\n- Inspired by similar projects in the community"
        
        # Roadmap
        print("\n🗺️ Roadmap")
        roadmap_items = []
        print("Add roadmap items (empty line to finish):")
        while True:
            item = input("Roadmap item: ")
            if not item:
                break
            roadmap_items.append(f"- [ ] {item}")
        
        self.placeholders['ROADMAP'] = '\n'.join(roadmap_items) if roadmap_items else "- [ ] Add more features\n- [ ] Improve documentation\n- [ ] Enhance performance"
        
        # Status
        self.placeholders['PROJECT_STATUS'] = f"Project is: __{input('Project status (active/maintained/deprecated) [active]: ') or 'active'}__"
        
        # Made with
        self.placeholders['MADE_WITH'] = "❤️"
    
    def generate_readme(self) -> str:
        """Generate the final README.md content."""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found at {self.template_path}")
        
        content = self.template_path.read_text()
        
        # Replace all placeholders
        for key, value in self.placeholders.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
        
        return content
    
    def save_readme(self, output_path: Optional[Path] = None) -> None:
        """Save the generated README.md file."""
        if output_path is None:
            output_path = self.project_root / "README.md"
        
        content = self.generate_readme()
        
        # Backup existing file
        if output_path.exists():
            backup_path = output_path.with_suffix('.md.backup')
            print(f"\n⚠️  Backing up existing README.md to {backup_path}")
            output_path.rename(backup_path)
        
        output_path.write_text(content)
        print(f"\n✅ Successfully created {output_path}")
        
        # Additional files to create
        print("\n📋 Next steps:")
        print("1. Review and customize the generated README.md")
        print("2. Add screenshots to enhance the demo section")
        print("3. Create a LICENSE file if you haven't already")
        print("4. Set up CONTRIBUTING.md for contribution guidelines")
        print("5. Add .env.example if your project uses environment variables")

def main():
    """Main entry point."""
    generator = ReadmeGenerator()
    
    try:
        generator.gather_project_info()
        generator.save_readme()
    except KeyboardInterrupt:
        print("\n\n❌ README generation cancelled")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())