---
title: CrewAI Repository Setup
description: Generates a complete, production-ready GitHub repository structure for developing CrewAI-based AI agents
domain: productivity
variables:
  required:
    - project_name: Name of the repository/project
  optional:
    - python_version: Python version to target (default: 3.10+)
    - include_docker: Include Docker configuration (default: true)
    - include_examples: Include example agent implementations (default: true)
tags: [crewai, repository-setup, ai-agents, python, development, boilerplate]
---

## Description
This prompt creates a comprehensive GitHub repository for CrewAI agent development with everything needed from initial setup through production deployment. It generates project structure, configuration files, boilerplate code, examples, documentation, and production-ready features following Python best practices.

Use this when starting a new CrewAI project to avoid manual setup of development environment, testing infrastructure, and deployment configurations. The output is enterprise-ready but maintains simplicity for quick onboarding.

## Example
```
project_name = "my-crewai-agents"
python_version = "3.11"
include_docker = true
include_examples = true
```

## Prompt
```text
Create a complete, production-ready GitHub repository for developing CrewAI-based AI agents with the following specifications:

PROJECT: {project_name}
PYTHON VERSION: {python_version}
DOCKER: {include_docker}
EXAMPLES: {include_examples}

# Repository Structure Requirements

## Core Structure
- Standard Python project layout with src/, tests/, docs/, examples/ directories
- Logical organization for agents, tools, tasks, and configurations
- Clear separation between source code, tests, and documentation

## Development Environment
- Docker and docker-compose configuration for consistent local development
- Virtual environment setup with modern Python packaging (pyproject.toml)
- Comprehensive requirements.txt with CrewAI and common dependencies
- .env.example showing all required environment variables
- .gitignore optimized for Python/AI projects with IDE-specific exclusions

## Code Quality & Testing
- Pre-commit hooks configuration for automated code quality checks
- Pytest configuration with coverage reporting
- Linting setup (black, isort, flake8, mypy)
- GitHub Actions workflow for CI/CD (testing, linting, building)
- Makefile with common commands (install, test, lint, format, run, clean)

## Boilerplate Code
- Base agent class that other agents can inherit from with common functionality
- Tools directory with example tools and a tools registry pattern
- Configuration management system supporting multiple environments (dev, staging, prod)
- Main orchestration file demonstrating crew and agent setup
- Utility modules for common operations (logging, error handling, API calls)

## Examples & Documentation
- README.md with project overview, installation steps, quick start, and structure explanation
- Getting started guide in docs/ with step-by-step instructions
- Agent development best practices guide
- Tool creation tutorial with examples
- At least three working examples:
  - Simple single-agent workflow
  - Multi-agent collaborative crew
  - Custom tool implementation
- API documentation template
- Troubleshooting guide with common issues and solutions

## Production Features
- Structured logging configuration with different levels for dev/prod
- Error handling patterns and custom exception classes
- Environment-specific configurations (database, API endpoints, resource limits)
- Health check implementation (if deployed as a service)
- Security best practices (API key management, input validation, rate limiting)
- Performance monitoring hooks (metrics collection, instrumentation points)
- Resource management configurations (memory limits, timeout settings)

# Output Requirements

Provide each major file as a separate code block or artifact with:
- Clear filename and path as the header
- Complete, runnable code (no placeholders or TODOs)
- Inline comments explaining key decisions
- Proper formatting and style consistency

Organize outputs in logical groups:
1. Repository root files (README, requirements, .gitignore, etc.)
2. Configuration files (Docker, pytest, pre-commit, etc.)
3. Source code structure (base classes, utilities)
4. Example implementations
5. Documentation files

# Constraints
- Use Python {python_version} syntax and features
- Follow PEP 8 and modern Python conventions
- Keep dependencies minimal but sufficient
- Make it easy to extend without modifying core files
- Ensure all examples are fully functional and can run immediately
- Include helpful comments but avoid over-documentation

# Success Criteria
A developer should be able to:
1. Clone the repository
2. Run a single setup command
3. Execute example agents within 5 minutes
4. Understand the architecture from documentation
5. Create their first custom agent within 30 minutes
6. Deploy to production with confidence using provided configurations
```