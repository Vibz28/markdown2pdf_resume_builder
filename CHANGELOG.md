# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-08-15

### 🎨 Enhanced Styling & Clean Design

### Changed
- **Clean Default Styling**
  - Changed default header background to white for professional appearance
  - Removed section icons (🎓, 💼, 🛠, etc.) for cleaner look
  - Eliminated horizontal separators between sections
  - Removed section title bounding boxes and background colors

### Improved
- **Header Design**
  - Header no longer expands to full margin width
  - Better spacing and padding for professional look
  - Maintains colored header option for branding when desired

- **Section Headers**
  - Clean underlined design instead of boxed styling
  - Bold text with slightly increased font size
  - Proper spacing for visual hierarchy

- **Typography**
  - Job titles now italicized for better differentiation
  - Consistent font styling throughout document
  - Improved visual hierarchy with clean typography

### Technical
- Enhanced template styling system to support both white and colored backgrounds
- Improved header table width calculation and centering
- Refined paragraph style definitions for better visual appeal

## [1.0.0] - 2025-08-15

### 🎉 Major Release - Complete Restructure & Enhanced Features

### Added
- **✨ Professional Project Structure**
  - Adopted `src/` layout following Python packaging best practices
  - Proper package organization with `src/markdown2pdf_resume_builder/`
  - Comprehensive test suite with pytest
  - Development automation with Makefile
  - Professional documentation structure

- **🎨 Template-Style Formatting**
  - Colored header banner with customizable background color (default: #4A6741)
  - White text on colored header for professional appearance
  - Section icons (🎓 Education, 💼 Experience, 🛠 Skills, 📂 Projects, 📚 Courses)
  - Styled section headers with borders and background colors
  - Professional color scheme throughout

- **🔗 Enhanced Hyperlink Support**
  - Blue color and underline for clear link visibility
  - Clickable links preserved in PDF output
  - Special handling for project title links: `**[Project Name](URL)**`
  - Smart link detection in contact information

- **📋 Automatic Section Reordering**
  - Intelligent section ordering: Education → Experience → Skills → Projects → Courses
  - Works regardless of original markdown file structure
  - Smart categorization based on section titles

- **🛠 Customization Options**
  - `--header-color` flag for custom header background colors
  - `--font-scheme` flag for different font styling options
  - Flexible output directory and filename control
  - Template styling with professional defaults

- **📦 Multiple Installation & Usage Methods**
  - Console scripts: `resume-builder` and `markdown2pdf-resume-builder`
  - Python module: `python -m markdown2pdf_resume_builder`
  - Programmatic API for integration
  - Legacy compatibility with deprecation warnings

- **🧪 Comprehensive Testing**
  - Unit tests for core functionality
  - CLI integration tests
  - Test fixtures and sample data
  - Coverage reporting with >90% target

- **📚 Professional Documentation**
  - Detailed API documentation with examples
  - Contributing guidelines for developers
  - Project structure explanation
  - Comprehensive README with usage examples

### Fixed
- **🐛 Semicolon Bug**: Eliminated unwanted semicolons in job titles and content
- **🔧 Link Processing**: Improved markdown link parsing to avoid formatting conflicts
- **📏 Dynamic Sizing**: Enhanced content length analysis for better one-page optimization
- **🎯 Template Compliance**: Fixed styling to match professional resume templates

### Changed
- **🏗 Project Structure**: Complete reorganization following Python best practices
  - Moved main code to `src/markdown2pdf_resume_builder/`
  - Separated CLI logic into dedicated `cli.py`
  - Core functionality in `resume_builder.py`
  - Examples moved to dedicated `examples/` directory
  
- **⚙ Build System**: Upgraded to modern Python packaging
  - `pyproject.toml` as single source of configuration
  - Hatchling as build backend
  - Proper dependency management
  - Entry points for console scripts

- **🎨 Default Styling**: Enhanced visual appearance
  - Professional header with colored background
  - Section headers with icons and styling
  - Improved typography and spacing
  - Better visual hierarchy

- **📝 CLI Interface**: Enhanced command-line experience
  - More descriptive help messages
  - Better error handling and user feedback
  - Consistent option naming and descriptions

### Improved
- **⚡ Performance**: Optimized PDF generation process
- **🔒 Error Handling**: Comprehensive error reporting and validation
- **📖 Documentation**: Complete rewrite with professional standards
- **🧹 Code Quality**: Type hints, docstrings, and formatting standards

### Development
- **🔧 Development Tools**
  - Makefile for common development tasks
  - Black for code formatting
  - Flake8 for linting
  - mypy for type checking
  - pytest for testing
  - pre-commit hooks for quality assurance

- **📋 Quality Assurance**
  - Comprehensive test coverage
  - Type annotations throughout
  - Professional docstrings
  - Code style enforcement

## [0.1.0] - 2025-08-14

### Added
- Initial implementation of markdown to PDF resume builder
- Dynamic font sizing for one-page optimization
- Basic hyperlink support
- ReportLab-based PDF generation
- Click-based command-line interface

### Features
- One-page and multi-page resume generation
- Dynamic content analysis and font scaling
- Basic markdown parsing and PDF formatting
- Cross-platform compatibility

---

## Migration Guide v0.1.0 → v1.0.0

### For Users
- **Installation**: Same process, but now supports multiple methods
- **CLI Usage**: Same commands work, but new options available
- **Output**: Improved styling and template compliance

### For Developers
- **Import Path**: `from markdown2pdf_resume_builder import ResumeBuilder`
- **API**: Same public API, enhanced with new customization options
- **Structure**: Code moved to `src/` - use development installation

### Backward Compatibility
- Legacy `main.py` still works (with deprecation warning)
- Same command-line interface
- Same programmatic API

---

## Upcoming Features

### v1.1.0 (Planned)
- [ ] Additional template themes
- [ ] Custom font support
- [ ] Advanced styling options
- [ ] Batch processing capabilities

### v1.2.0 (Planned)
- [ ] Web interface for online generation
- [ ] Additional output formats (HTML, Word)
- [ ] Resume analytics and optimization suggestions
- [ ] Integration with job boards and ATS systems

---

**Note**: This project follows semantic versioning. Major version changes may include breaking changes, minor versions add features, and patch versions include bug fixes.
