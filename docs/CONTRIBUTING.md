# Contributing to Markdown2PDF Resume Builder

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites
- Python 3.10 or higher
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vibz28/markdown2pdf_resume_builder.git
   cd markdown2pdf_resume_builder
   ```

2. **Set up development environment**
   ```bash
   make setup-dev
   ```
   
   Or manually:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   pre-commit install
   ```

3. **Verify installation**
   ```bash
   make test
   make run-example
   ```

## Project Structure

```
markdown2pdf_resume_builder/
├── src/markdown2pdf_resume_builder/    # Main package
│   ├── __init__.py                     # Package initialization
│   ├── __main__.py                     # Module entry point
│   ├── cli.py                          # Command-line interface
│   └── resume_builder.py               # Core functionality
├── tests/                              # Test suite
├── examples/                           # Example files
├── scripts/                            # Utility scripts
├── docs/                              # Documentation
├── pyproject.toml                     # Project configuration
└── Makefile                           # Development commands
```

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run checks**
   ```bash
   make check-all  # Runs formatting, linting, and tests
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

### Code Style

- Use [Black](https://black.readthedocs.io/) for code formatting
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes

### Testing

- Write tests for all new functionality
- Ensure tests pass before submitting PR
- Aim for good test coverage (>90%)

```bash
make test        # Run tests
make test-cov    # Run tests with coverage
```

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions/changes
- `refactor:` for code refactoring
- `style:` for formatting changes

## Submitting Changes

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request**
   - Use a clear, descriptive title
   - Include a detailed description of changes
   - Reference any related issues

3. **Code Review Process**
   - Address any feedback from maintainers
   - Ensure all checks pass
   - Squash commits if requested

## Reporting Issues

When reporting bugs or requesting features:

1. **Check existing issues** to avoid duplicates
2. **Use issue templates** when available
3. **Provide detailed information**:
   - OS and Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and logs

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update examples if functionality changes

## Release Process

Maintainers handle releases:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release tag
4. Publish to PyPI

## Questions?

- Open an issue for questions about contributing
- Join discussions in existing issues
- Contact maintainers directly if needed

Thank you for contributing! 🎉
