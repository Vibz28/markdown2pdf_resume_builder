# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-08-15

### Added
- Initial release of Markdown to PDF Resume Builder
- ReportLab-based PDF generation for cross-platform compatibility
- Dynamic font sizing and margins for one-page vs multi-page layouts
- Interactive PDF support with preserved hyperlinks
- ATS-friendly formatting optimized for resume parsing systems
- Command-line interface with Click framework
- Support for standard Markdown features (headers, lists, links, bold/italic, code)
- Professional styling with configurable themes
- Automatic output directory creation
- Cross-platform PDF opening functionality
- Sample resume template (Vibhor Janey's resume)
- Comprehensive documentation and examples
- Example usage script for demonstration
- uv package manager support with pyproject.toml configuration
- Alternative implementations for different PDF engines

### Features
- **One-page mode**: Compressed formatting to fit content on a single page
- **Multi-page mode**: Optimal spacing for readability and professional appearance
- **Interactive links**: Email, LinkedIn, and web links preserved in PDF
- **Professional typography**: Clean, modern design with excellent readability
- **ATS compatibility**: Optimized for Applicant Tracking Systems
- **LLM-friendly**: Generated PDFs are easily parseable by AI systems
- **Cross-platform**: Works on macOS, Windows, and Linux

### Technical Details
- Built with Python 3.10+ support
- Uses ReportLab for reliable PDF generation
- Click for command-line interface
- Markdown2 for enhanced Markdown processing
- Comprehensive error handling and user feedback
- Modular design for easy extension and customization
