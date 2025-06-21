# Project Setup Toolkit

AI-driven toolkit for setting up new software projects with templates and best practices.

## 🎯 Overview

This toolkit provides a comprehensive set of templates and AI-powered tools to quickly set up professional software projects. Instead of hardcoded logic, it uses intelligent template filling to adapt to any project type.

## ✨ Features

- **AI-Driven Setup**: Templates filled intelligently based on project analysis
- **Comprehensive Coverage**: README, CLAUDE.md, licenses, gitignore, and more
- **Git Integration**: Automatic commits at each setup step
- **Flexible Templates**: Easy to modify templates without changing code
- **Project Types**: Supports web apps, CLIs, libraries, APIs, and more

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/dragoonbuster/project-setup-toolkit.git
cd project-setup-toolkit

# Start a new project
./start_project.py
```

## 📦 Available Tools

| Tool | Purpose |
|------|---------|
| `start_project.py` | Master orchestrator - runs all tools in sequence |
| `setup_structure.py` | Creates organized directory structure |
| `setup_license.py` | Helps select and generate appropriate license |
| `setup_gitignore.py` | Creates comprehensive .gitignore file |
| `setup_readme.py` | Generates professional README.md |
| `setup_claude_md.py` | Creates AI assistant guidelines |
| `setup_env.py` | Generates .env.example template |
| `create_feature_prompt.py` | Creates detailed feature implementation prompts |
| `generate_commit.py` | Generates semantic commit messages |
| `setup_contributing.py` | Creates contribution guidelines |

## 📁 Project Structure

```
project-setup-toolkit/
├── *_template.md          # Templates for various files
├── setup_*.py            # Individual setup tools
├── create_*.py           # Generation tools
├── start_project.py      # Master orchestrator
├── PROJECT_SETUP_PLAN.md # Implementation plan
└── README.md            # This file
```

## 💻 How It Works

1. **Templates**: Markdown files with placeholders for customization
2. **Tools**: Simple Python scripts that provide AI instructions
3. **AI Processing**: Claude analyzes projects and fills templates intelligently
4. **Git Integration**: Each step creates appropriate commits

### Example Workflow

```bash
# 1. Start new project
./start_project.py

# 2. Claude will:
#    - Create directory structure
#    - Add license
#    - Generate .gitignore
#    - Create README.md
#    - Set up CLAUDE.md
#    - Make commits at each step

# 3. Project is ready for development!
```

## 🛠️ Individual Tool Usage

Each tool can be used independently:

```bash
# Just create a README
./setup_readme.py

# Just set up .gitignore
./setup_gitignore.py

# Create a feature implementation prompt
./create_feature_prompt.py
```

## 📝 Templates

Templates use `{{PLACEHOLDER}}` syntax and are designed to be:
- Easy to read and modify
- Comprehensive in coverage
- Flexible for different project types

## 🤝 Contributing

We welcome contributions! See our contributing guidelines (run `./setup_contributing.py` to generate).

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with AI-first philosophy
- Inspired by modern development practices
- Designed for developer happiness

---

Made with ❤️ by dragoonbuster