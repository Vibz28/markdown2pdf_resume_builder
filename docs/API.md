# API Documentation

This document provides detailed API documentation for the Markdown2PDF Resume Builder.

## Core Classes

### ResumeBuilder

The main class for converting Markdown resumes to PDF.

```python
from markdown2pdf_resume_builder import ResumeBuilder

builder = ResumeBuilder(
    one_page=False,
    output_dir="output",
    header_color="#4A6741",
    font_scheme="modern"
)
```

#### Constructor Parameters

- **one_page** (`bool`, default: `False`): Enable one-page compression mode
- **output_dir** (`str`, default: `"output"`): Directory for generated PDFs
- **header_color** (`str`, default: `"#4A6741"`): Header background color (hex)
- **font_scheme** (`str`, default: `"modern"`): Font styling scheme

#### Methods

##### `generate_pdf(markdown_file: str, output_filename: Optional[str] = None) -> str`

Generate a PDF from a markdown file.

**Parameters:**
- `markdown_file`: Path to the input markdown file
- `output_filename`: Optional custom output filename

**Returns:**
- Path to the generated PDF file

**Raises:**
- `FileNotFoundError`: If the markdown file doesn't exist

**Example:**
```python
pdf_path = builder.generate_pdf("resume.md", "my_resume.pdf")
print(f"Generated: {pdf_path}")
```

#### Private Methods

These methods are used internally but documented for reference:

##### `_estimate_content_length(content: str) -> int`

Estimate total content length for dynamic sizing.

##### `_get_dynamic_sizing(content_length: int) -> Dict[str, float]`

Calculate dynamic font sizes based on content length.

##### `_create_styles(content_length: int) -> Dict[str, ParagraphStyle]`

Create ReportLab paragraph styles for the resume.

##### `_parse_markdown_content(content: str) -> List[Dict]`

Parse markdown content into structured data.

##### `_clean_text(text: str) -> str`

Clean markdown formatting for ReportLab rendering.

##### `_reorder_sections(sections: List[Dict]) -> List[Dict]`

Reorder sections to: Education → Experience → Skills → Projects → Courses.

##### `_create_header_table(name: str, title: str, contact_lines: List[str]) -> Table`

Create the colored header table.

##### `_build_pdf_content(sections: List[Dict]) -> List`

Build the complete PDF content structure.

##### `_format_entry(entry: List[Tuple[str, str]]) -> List`

Format individual resume entries (jobs, education, etc.).

## Utility Functions

### `open_pdf(pdf_path: str)`

Open a PDF file using the system's default application.

**Parameters:**
- `pdf_path`: Path to the PDF file to open

**Example:**
```python
from markdown2pdf_resume_builder.resume_builder import open_pdf
open_pdf("resume.pdf")
```

## Command Line Interface

### `main()`

Main CLI entry point. Can be used programmatically:

```python
from markdown2pdf_resume_builder.cli import main
from click.testing import CliRunner

runner = CliRunner()
result = runner.invoke(main, ['resume.md', '--one-page'])
```

## Styling Configuration

### Font Sizing

The system uses dynamic font sizing based on content length:

- **Multi-page mode**: Fixed sizes (11pt base, 20pt name, 14pt sections)
- **One-page mode**: Scaled sizes (8.5pt-6.8pt base, depending on content)

### Color Schemes

Default colors:
- Header background: `#4A6741` (customizable)
- Header text: White
- Section headers: Dark gray with light background
- Body text: Black
- Links: Blue with underline

### Section Icons

- 🎓 Education
- 💼 Work Experience  
- 🛠 Skills
- 📂 Projects
- 📚 Courses

## Error Handling

The library provides comprehensive error handling:

- **File not found**: Clear error message with file path
- **Invalid markdown**: Graceful parsing with fallbacks
- **PDF generation errors**: Detailed error reporting
- **Style errors**: Safe defaults with warnings

## Examples

### Basic Usage

```python
from markdown2pdf_resume_builder import ResumeBuilder

# Create builder
builder = ResumeBuilder()

# Generate PDF
pdf_path = builder.generate_pdf("resume.md")
print(f"PDF generated: {pdf_path}")
```

### One-Page Resume

```python
builder = ResumeBuilder(one_page=True)
pdf_path = builder.generate_pdf("resume.md")
```

### Custom Styling

```python
builder = ResumeBuilder(
    header_color="#2C5F41",
    output_dir="pdfs",
    font_scheme="modern"
)
pdf_path = builder.generate_pdf("resume.md", "custom_resume.pdf")
```

### Batch Processing

```python
import glob
from pathlib import Path

builder = ResumeBuilder(output_dir="batch_output")

for markdown_file in glob.glob("resumes/*.md"):
    try:
        pdf_path = builder.generate_pdf(markdown_file)
        print(f"✅ {markdown_file} → {pdf_path}")
    except Exception as e:
        print(f"❌ {markdown_file}: {e}")
```

## Type Hints

The library uses comprehensive type hints for better IDE support:

```python
from typing import Optional, List, Dict, Tuple
from pathlib import Path
from reportlab.platypus import Paragraph, Table
```

All public methods include proper type annotations for parameters and return values.
