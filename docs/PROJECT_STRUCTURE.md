# Project Structure

This document explains the reorganized project structure following Python packaging best practices.

## Directory Structure

```
markdown2pdf_resume_builder/
├── 📁 src/                                 # Source code
│   └── 📁 markdown2pdf_resume_builder/     # Main package
│       ├── __init__.py                     # Package initialization & exports
│       ├── __main__.py                     # Module entry point (python -m ...)
│       ├── cli.py                          # Command-line interface
│       └── resume_builder.py               # Core resume building logic
├── 📁 tests/                               # Test suite
│   ├── conftest.py                         # Pytest configuration & fixtures
│   ├── test_resume_builder.py              # Core functionality tests
│   └── test_cli.py                         # CLI tests
├── 📁 examples/                            # Example files & demos
│   ├── example_usage.sh                    # Usage demonstration script
│   └── resume_vibhor_janey_updated_aug_2025.md  # Sample resume
├── 📁 scripts/                             # Utility scripts
│   ├── main_legacy.py                      # Legacy main.py (backward compatibility)
│   └── resume_builder_reportlab.py         # Alternative implementation
├── 📁 docs/                                # Documentation
│   ├── API.md                              # API documentation
│   └── CONTRIBUTING.md                     # Contribution guidelines
├── 📁 output/                              # Generated PDF files (gitignored)
├── 📄 pyproject.toml                       # Project configuration & dependencies
├── 📄 Makefile                             # Development automation
├── 📄 main.py                              # Legacy entry point (with deprecation warning)
├── 📄 README.md                            # Project overview & usage
├── 📄 LICENSE                              # License file
├── 📄 CHANGELOG.md                         # Version history
├── 📄 .gitignore                           # Git ignore rules
└── 📄 requirements.txt                     # Fallback requirements (for pip)
```

## Key Components

### Source Code (`src/`)

**Why `src/` layout?**
- Prevents accidental imports during development
- Forces proper installation for testing
- Clear separation between source and other files
- Industry standard for Python packages

**Package Structure:**
- `__init__.py`: Package exports and metadata
- `__main__.py`: Enables `python -m package_name`
- `cli.py`: Command-line interface with Click
- `resume_builder.py`: Core PDF generation logic

### Tests (`tests/`)

**Framework:** pytest with comprehensive fixtures
- `conftest.py`: Shared test configuration and fixtures
- `test_*.py`: Individual test modules
- **Coverage:** Configured for >90% coverage requirement

### Examples (`examples/`)

**Purpose:** Demonstrations and sample files
- Working example scripts
- Sample resume markdown files
- Usage demonstrations

### Scripts (`scripts/`)

**Purpose:** Utility and legacy scripts
- Development utilities
- Alternative implementations
- Backward compatibility support

### Documentation (`docs/`)

**Comprehensive docs:**
- API reference with examples
- Contributing guidelines
- Architecture explanations

## Installation Methods

### 1. Development Installation
```bash
# Clone repository
git clone <repository-url>
cd markdown2pdf_resume_builder

# Install in development mode
pip install -e .

# Or using make
make install
```

### 2. User Installation (when published)
```bash
pip install markdown2pdf-resume-builder
```

## Usage Methods

### 1. As Installed Command
```bash
# After installation
resume-builder resume.md --one-page
markdown2pdf-resume-builder resume.md --header-color="#2C5F41"
```

### 2. As Python Module
```bash
# Without installation (development)
python -m markdown2pdf_resume_builder resume.md --one-page
```

### 3. Programmatic Usage
```python
from markdown2pdf_resume_builder import ResumeBuilder

builder = ResumeBuilder(one_page=True)
pdf_path = builder.generate_pdf("resume.md")
```

### 4. Legacy Support
```bash
# Backward compatibility (with deprecation warning)
python main.py resume.md --one-page
```

## Development Workflow

### Quick Start
```bash
make setup-dev     # Set up development environment
make test          # Run tests
make run-example   # Test with sample file
```

### Code Quality
```bash
make format        # Format code with Black
make lint          # Run linting checks
make test-cov      # Test with coverage
make check-all     # Run all checks
```

### Building & Distribution
```bash
make clean         # Clean build artifacts
make build         # Build distribution packages
```

## Configuration Files

### `pyproject.toml`
**Modern Python project configuration:**
- Project metadata and dependencies
- Build system configuration (Hatchling)
- Tool configurations (Black, pytest, mypy)
- Entry points for console scripts

### `Makefile`
**Development automation:**
- Common development tasks
- Testing and quality checks
- Build and release processes

### `.gitignore`
**Comprehensive ignore rules:**
- Python artifacts (`__pycache__`, `.pyc`)
- Virtual environments
- Build/distribution files
- IDE files
- Generated outputs

## Entry Points

### 1. Console Scripts (Recommended)
```toml
[project.scripts]
resume-builder = "markdown2pdf_resume_builder.cli:main"
markdown2pdf-resume-builder = "markdown2pdf_resume_builder.cli:main"
```

### 2. Module Entry Point
```python
# src/markdown2pdf_resume_builder/__main__.py
if __name__ == "__main__":
    from .cli import main
    main()
```

### 3. Legacy Entry Point
```python
# main.py (with deprecation warning)
import warnings
warnings.warn("Use 'python -m markdown2pdf_resume_builder' instead")
```

## Benefits of This Structure

### ✅ **Professional Standards**
- Follows Python packaging best practices
- Uses modern build tools (pyproject.toml)
- Clear separation of concerns

### ✅ **Development Experience**
- Easy testing and debugging
- Automated quality checks
- Comprehensive documentation

### ✅ **Distribution Ready**
- Proper package structure for PyPI
- Multiple installation methods
- Backward compatibility

### ✅ **Maintainability**
- Clear code organization
- Comprehensive test suite
- Development automation

### ✅ **User Experience**
- Multiple usage patterns
- Clear documentation
- Professional installation

## Migration from Old Structure

**Old → New:**
- `main.py` → `src/markdown2pdf_resume_builder/cli.py`
- Core logic → `src/markdown2pdf_resume_builder/resume_builder.py`
- Examples → `examples/`
- Alternative code → `scripts/`

**Backward Compatibility:**
- Legacy `main.py` still works (with warning)
- Same CLI interface
- Same API for programmatic usage

This structure positions the project as a professional, maintainable Python package ready for distribution and long-term development.
