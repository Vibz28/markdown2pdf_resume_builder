# Markdown to PDF Resume Builder

A professional resume builder that converts Markdown files to beautifully formatted PDFs with dynamic sizing, interactive features, and ATS (Applicant Tracking System) friendly formatting.

## Features

✅ **Dynamic PDF Generation**: Convert Markdown resumes to professional PDFs  
✅ **One-Page Mode**: Automatically compress content to fit a single page  
✅ **Multi-Page Mode**: Full formatting with optimal spacing and readability  
✅ **Interactive PDFs**: Preserves hyperlinks for email, LinkedIn, and other URLs  
✅ **ATS-Friendly**: Optimized for resume parsing systems like Workday and Greenhouse  
✅ **Professional Styling**: Clean, modern typography with excellent readability  
✅ **LLM-Readable**: Generated PDFs are easily parseable by AI systems  
✅ **Cross-Platform**: Works on macOS, Windows, and Linux  

## Installation

### Prerequisites
- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip

### Quick Start

1. **Clone the repository** (or download the files):
```bash
git clone https://github.com/Vibz28/markdown2pdf_resume_builder.git
cd markdown2pdf_resume_builder
```

2. **Install dependencies using uv** (recommended):
```bash
uv sync
```

   Or with pip:
```bash
pip install -r requirements.txt
```

3. **Build your resume**:
```bash
# Generate a multi-page resume
uv run python main.py your_resume.md
# OR with pip: python main.py your_resume.md

# Generate a one-page resume
uv run python main.py --one-page your_resume.md

# Specify custom output and auto-open
uv run python main.py --one-page --output my_resume --output-dir pdfs --open-pdf your_resume.md
```

4. **Try the example** (uses the included sample resume):
```bash
# Run the example script
./example_usage.sh

# Or manually test with the sample
uv run python main.py [YOUR_RESUME_FILE].md
uv run python main.py --one-page [YOUR_RESUME_FILE].md
```

## Usage

### Command Line Interface

```bash
uv run python main.py [OPTIONS] MARKDOWN_FILE
```

**Options:**
- `--one-page, -1`: Generate a one-page resume with compressed formatting
- `--output, -o TEXT`: Output filename (without extension)
- `--output-dir TEXT`: Output directory (default: output)
- `--open-pdf`: Open the generated PDF after creation
- `--help`: Show help message

### Examples

```bash
# Basic conversion
uv run python main.py resume.md

# One-page version
uv run python main.py --one-page resume.md

# Custom output location and auto-open
uv run python main.py --one-page --output john_doe_resume --output-dir resumes --open-pdf resume.md
```

## Markdown Format

Your resume should follow a structured Markdown format. Here's the recommended structure based on the included sample:

```markdown
# Your Name
**Your Title/Position**

[email@example.com](mailto:email@example.com) | (123) 456-7890 | [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile) | City, State

---

## WORK EXPERIENCE

**Company Name**  
**Job Title**  
*Date Range | Location*

- Achievement or responsibility with **bold** keywords
- Another achievement with metrics and results
- Technical accomplishments with specific technologies

## EDUCATION

**University Name** — *Degree*  
Date Range | Location

## SKILLS

**Category:** Skill 1, Skill 2, Skill 3, etc.

## PROJECTS

**Project Name — Technology Stack**  
- Description of the project and achievements
```

### Supported Markdown Features

- **Headers** (H1-H4): Used for name, sections, companies, and positions
- **Bold/Italic**: For emphasis and highlighting
- **Links**: Email, LinkedIn, GitHub, portfolio links (preserved as clickable)
- **Lists**: Bullet points for achievements and skills
- **Code**: Inline code for technical terms and technologies
- **Tables**: For structured data (if needed)
- **Horizontal Rules**: Section separators

## Output Files

The tool generates:
- **PDF**: Your professionally formatted resume
- **HTML**: Debug version for review and customization
- **Organized structure**: Files saved in the specified output directory

## Styling and Customization

### Two Format Modes

1. **Multi-Page Mode** (default):
   - 11pt base font size
   - 0.75" margins
   - Optimal spacing for readability
   - Suitable for detailed resumes

2. **One-Page Mode** (`--one-page`):
   - 10pt base font size
   - 0.4" margins
   - Compressed spacing
   - Automatic content fitting

### Font and Design Features

- **Professional Typography**: Georgia serif font for excellent readability
- **Color Scheme**: Professional blues and grays
- **Section Headers**: Bold, uppercase headers with subtle underlines
- **Responsive Links**: Interactive hyperlinks preserved in PDF
- **Clean Layout**: Optimized white space and visual hierarchy

## Output Quality & Features

### PDF Quality
- **Professional Typography**: Clean, readable fonts optimized for both screen and print
- **Consistent Formatting**: Proper spacing, alignment, and visual hierarchy
- **Compact File Size**: Optimized PDFs typically under 10KB for fast loading
- **Print-Ready**: High-quality output suitable for printing and digital sharing

### ATS Compatibility Features
- **Text-Based Content**: All text remains selectable and searchable
- **Logical Structure**: Proper heading hierarchy and content flow
- **Standard Fonts**: Uses widely-supported fonts for maximum compatibility
- **Clean Layout**: No complex graphics or elements that confuse parsers
- **Consistent Formatting**: Standardized spacing and structure

### Interactive Elements
- **Clickable Links**: Email, LinkedIn, GitHub, and portfolio links preserved
- **Phone Numbers**: Properly formatted and accessible
- **Professional URLs**: Clean, working hyperlinks in the PDF

### Customization Options
- **Dynamic Sizing**: Automatic font and margin adjustment for one-page format
- **Flexible Output**: Choose between compressed and expanded layouts
- **Custom Filenames**: Specify your preferred output names
- **Multiple Formats**: Support for various resume sections and structures

## ATS and LLM Compatibility

The generated PDFs are optimized for:

- **ATS Systems**: Clean text structure, proper heading hierarchy, standard fonts
- **Resume Parsers**: Logical content flow, consistent formatting, accessible text
- **LLM Processing**: Well-structured content that's easily parseable by AI
- **Human Readers**: Professional appearance with excellent readability

## Development

### Project Structure

```
markdown2pdf_resume_builder/
├── main.py                          # Main resume builder script (ReportLab-based)
├── resume_builder_reportlab.py      # Alternative ReportLab implementation
├── pyproject.toml                   # Project configuration and dependencies
├── README.md                        # This file
├── LICENSE                          # Apache 2.0 license
└── example_usage.sh                 # Example usage script
```

### Available Scripts

- **main.py**: Primary script using ReportLab (cross-platform compatible)
- **resume_builder_reportlab.py**: Alternative ReportLab implementation
- **example_usage.sh**: Demonstration script showing various usage patterns

### Dependencies

- **markdown2**: Enhanced Markdown processing
- **weasyprint**: High-quality PDF generation
- **reportlab**: PDF manipulation capabilities
- **click**: Command-line interface framework

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test them
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## Troubleshooting

### Common Issues

1. **Font errors**: Ensure you have standard system fonts installed
2. **PDF generation fails**: Check that all dependencies are properly installed
3. **One-page doesn't fit**: Consider reducing content or using multi-page mode
4. **Links not working**: Verify markdown link syntax is correct

### System-Specific Notes

- **macOS**: May require additional font packages for optimal rendering
- **Windows**: Ensure proper Python and dependency installation
- **Linux**: May need additional system libraries for WeasyPrint

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Author

**Vibhor Janey**
- Email: vibhor.janey@gmail.com
- LinkedIn: [linkedin.com/in/vibhorjaney](https://linkedin.com/in/vibhorjaney)

---

*Built with ❤️ to help create professional resumes that stand out to both humans and ATS systems.*