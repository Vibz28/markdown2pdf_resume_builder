# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.2] - 2025-08-15

### 🚀 Critical One-Page Optimization & Layout Fixes

### Fixed
- **One-Page Functionality Restored**
  - Fixed dynamic font sizing precision loss (removed integer conversion)
  - Enhanced scaling algorithm with more aggressive size reduction for dense content
  - Added additional content length thresholds (4000, 4500, 5000+ characters)
  - Now properly fits content on single page regardless of density

- **Header Space Optimization**
  - Significantly reduced header padding and spacing for one-page resumes
  - Minimized top/bottom padding in header table (2px top, 4px bottom for one-page)
  - Reduced spacer after header from 6px to 3px for one-page layouts
  - Eliminated excessive whitespace without compromising readability

- **Typography Hierarchy Correction**
  - **Job Titles:** Now smaller than company names (base_size - 1)
  - **Company Names:** Proper base font size for prominence
  - **Section Headers:** Appropriately sized (base_size + 2) with underlines
  - Fixed size relationships for better visual hierarchy

### Enhanced
- **Dynamic Sizing Algorithm**
  - More granular content length thresholds for better scaling
  - Improved base font sizes starting from 9.5pt for better readability
  - Enhanced scale factors: 65% for very dense content (5000+ chars)
  - Maintains proportion across all text elements

- **Space Efficiency**
  - Reduced spacing between all elements in one-page mode
  - Conditional spacing based on one-page flag throughout styles
  - Optimized bullet point and paragraph spacing
  - Minimized wasted vertical space while maintaining readability

### Technical
- **Precision Improvements**
  - Removed integer conversion that was causing font size precision loss
  - Enhanced floating-point calculations for accurate scaling
  - Better proportional spacing calculations
- **Layout Optimization**
  - Conditional styling based on one-page mode
  - Improved header table styling with minimal padding
  - Enhanced vertical space management

## [1.1.1] - 2025-08-15

### 🐛 Critical Fixes & Improvements

### Fixed
- **Job Title Formatting**
  - Fixed markdown parsing for combined bold+italic (`_**text**_`) job titles
  - Job titles now render properly as both bold and italicized
  - Removed underscore artifacts from final PDF output

- **Section Separators**
  - Completely removed horizontal rule separators (`---`) from PDF output
  - Enhanced content parsing to filter out separator lines during processing
  - Cleaner section transitions with typography-based hierarchy

- **One-Page Dynamic Sizing**
  - Fixed one-page resume formatting that was expanding to multiple pages
  - Restored proper integration between content analysis and dynamic font sizing
  - Enhanced scaling algorithm to ensure content fits on single page

### Enhanced
- **Markdown Processing**
  - Improved regex patterns for handling complex markdown combinations
  - Better precedence handling for nested formatting (bold+italic)
  - Support for both `_**text**_` and `**_text_**` patterns

- **Content Analysis**
  - Enhanced content length estimation for more accurate dynamic sizing
  - Improved font scaling algorithm for dense content
  - Better proportion calculations for spacing and padding

### Technical
- Added comprehensive test coverage for new markdown parsing features
- Enhanced test suite with horizontal rule filtering validation
- Improved code documentation for markdown processing methods

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
