#!/usr/bin/env python3
"""
Markdown to PDF Resume Builder

A tool to convert markdown resumes to professionally formatted PDFs with dynamic sizing,
interactive features, and ATS-friendly formatting.

This version automatically detects available PDF generation backends and uses the best one available.
"""

import os
import re
import sys
import subprocess
import platform
from pathlib import Path
from typing import Optional, Tuple, List, Dict

import click
import markdown2

# Try to import WeasyPrint, fallback to ReportLab if not available
try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
    print("✅ Using WeasyPrint for high-quality PDF generation")
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    print(f"⚠️  WeasyPrint not available. Using ReportLab fallback.")
    # Import ReportLab components
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import Color, black, blue
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


class WeasyPrintResumeBuilder:
    """Resume builder using WeasyPrint for high-quality PDF generation."""
    
    def __init__(self, one_page: bool = False, output_dir: str = "output"):
        self.one_page = one_page
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.font_config = FontConfiguration()
    
    def get_css_styles(self, one_page: bool = False) -> str:
        """Generate CSS styles based on page requirements."""
        
        # Base styles that work well for both single and multi-page
        base_font_size = "10pt" if one_page else "11pt"
        line_height = "1.2" if one_page else "1.3"
        margin = "0.4in" if one_page else "0.75in"
        section_spacing = "8pt" if one_page else "12pt"
        
        css = f"""
        @page {{
            size: letter;
            margin: {margin};
            @bottom-center {{
                content: "";
            }}
        }}
        
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: {base_font_size};
            line-height: {line_height};
            color: #2c3e50;
            margin: 0;
            padding: 0;
            background: white;
        }}
        
        /* Header styling */
        h1 {{
            font-size: {'18pt' if one_page else '22pt'};
            font-weight: bold;
            color: #1a252f;
            margin: 0 0 {'4pt' if one_page else '8pt'} 0;
            text-align: center;
            letter-spacing: 0.5pt;
        }}
        
        h1 + p {{
            text-align: center;
            font-size: {'9pt' if one_page else '10pt'};
            color: #34495e;
            margin: 0 0 {'8pt' if one_page else '12pt'} 0;
            font-weight: 500;
        }}
        
        /* Contact information */
        h1 + p + p {{
            text-align: center;
            font-size: {'8pt' if one_page else '9pt'};
            margin: 0 0 {'12pt' if one_page else '16pt'} 0;
        }}
        
        /* Section headers */
        h2 {{
            font-size: {'12pt' if one_page else '14pt'};
            font-weight: bold;
            color: #1a252f;
            margin: {section_spacing} 0 {'4pt' if one_page else '6pt'} 0;
            padding-bottom: 2pt;
            border-bottom: 1pt solid #3498db;
            text-transform: uppercase;
            letter-spacing: 0.5pt;
        }}
        
        /* Work experience entries */
        h3 {{
            font-size: {'10pt' if one_page else '11pt'};
            font-weight: bold;
            color: #2c3e50;
            margin: {'6pt' if one_page else '8pt'} 0 {'2pt' if one_page else '3pt'} 0;
        }}
        
        h4 {{
            font-size: {'9pt' if one_page else '10pt'};
            font-weight: bold;
            color: #7f8c8d;
            margin: 0 0 {'2pt' if one_page else '3pt'} 0;
            font-style: italic;
        }}
        
        /* Paragraph spacing */
        p {{
            margin: 0 0 {'4pt' if one_page else '6pt'} 0;
            text-align: justify;
        }}
        
        /* List styling */
        ul {{
            margin: {'2pt' if one_page else '4pt'} 0 {'6pt' if one_page else '8pt'} 0;
            padding-left: 16pt;
        }}
        
        li {{
            margin: 0 0 {'2pt' if one_page else '3pt'} 0;
            text-align: justify;
        }}
        
        /* Links */
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        /* Strong/bold text */
        strong, b {{
            font-weight: bold;
            color: #1a252f;
        }}
        
        /* Emphasis/italic text */
        em, i {{
            font-style: italic;
        }}
        
        /* Horizontal rule */
        hr {{
            border: none;
            height: 1pt;
            background-color: #bdc3c7;
            margin: {'8pt' if one_page else '12pt'} 0;
        }}
        
        /* Code styling for technical terms */
        code {{
            background-color: #f8f9fa;
            padding: 1pt 2pt;
            border-radius: 2pt;
            font-family: 'Courier New', monospace;
            font-size: {'8pt' if one_page else '9pt'};
            color: #e74c3c;
        }}
        
        /* Table styling if present */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: {'4pt' if one_page else '6pt'} 0;
        }}
        
        th, td {{
            padding: 2pt 4pt;
            text-align: left;
            border-bottom: 1pt solid #ecf0f1;
        }}
        
        th {{
            font-weight: bold;
            background-color: #f8f9fa;
        }}
        
        /* Page break control for one-page mode */
        .page-break {{
            page-break-before: {'avoid' if one_page else 'auto'};
        }}
        
        /* Ensure no orphans/widows for better readability */
        p, li {{
            orphans: 2;
            widows: 2;
        }}
        
        /* Special formatting for dates and locations */
        .date-location {{
            font-style: italic;
            color: #7f8c8d;
            font-size: {'8pt' if one_page else '9pt'};
        }}
        """
        
        return css
    
    def preprocess_markdown(self, content: str) -> str:
        """Preprocess markdown content for better PDF formatting."""
        
        # Enhance date/location formatting
        content = re.sub(
            r'\\*([^*]+)\\s*\\|\\s*([^*]+)\\*',
            r'<span class="date-location">\\1 | \\2</span>',
            content
        )
        
        # Enhance email links
        content = re.sub(
            r'\\[([^]]+@[^]]+)\\]\\(mailto:([^)]+)\\)',
            r'<a href="mailto:\\2">\\1</a>',
            content
        )
        
        # Enhance LinkedIn and other profile links
        content = re.sub(
            r'\\[([^]]+)\\]\\((https://[^)]+)\\)',
            r'<a href="\\2">\\1</a>',
            content
        )
        
        return content
    
    def convert_markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown content to HTML."""
        
        # Preprocess the markdown
        processed_content = self.preprocess_markdown(markdown_content)
        
        # Convert to HTML with useful extras
        html_content = markdown2.markdown(
            processed_content,
            extras=[
                'fenced-code-blocks',
                'tables',
                'break-on-newline',
                'link-patterns',
                'smarty-pants'
            ]
        )
        
        return html_content
    
    def create_full_html(self, html_content: str, css_styles: str) -> str:
        """Create the complete HTML document."""
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resume</title>
            <style>
                {css_styles}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
    
    def generate_pdf(self, markdown_file: str, output_filename: Optional[str] = None) -> Tuple[str, str]:
        """Generate PDF from markdown file."""
        
        # Read markdown file
        markdown_path = Path(markdown_file)
        if not markdown_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_file}")
        
        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert to HTML
        html_content = self.convert_markdown_to_html(markdown_content)
        
        # Get CSS styles
        css_styles = self.get_css_styles(self.one_page)
        
        # Create full HTML document
        full_html = self.create_full_html(html_content, css_styles)
        
        # Generate output filename
        if output_filename is None:
            base_name = markdown_path.stem
            suffix = "_one_page" if self.one_page else "_full"
            output_filename = f"{base_name}{suffix}.pdf"
        
        output_path = self.output_dir / output_filename
        
        # Create PDF
        html_doc = HTML(string=full_html)
        css_doc = CSS(string=css_styles, font_config=self.font_config)
        
        html_doc.write_pdf(
            output_path,
            stylesheets=[css_doc],
            font_config=self.font_config
        )
        
        # Also save HTML for debugging
        html_output_path = self.output_dir / f"{Path(output_filename).stem}.html"
        with open(html_output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        return str(output_path), str(html_output_path)


class ReportLabResumeBuilder:
    """Resume builder using ReportLab for cross-platform compatibility."""
    
    def __init__(self, one_page: bool = False, output_dir: str = "output"):
        self.one_page = one_page
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.styles = self._create_styles()
    
    def _create_styles(self) -> Dict[str, ParagraphStyle]:
        """Create custom paragraph styles for the resume."""
        styles = getSampleStyleSheet()
        
        # Adjust sizes based on one-page mode
        base_size = 9 if self.one_page else 11
        
        custom_styles = {
            'Name': ParagraphStyle(
                'Name',
                parent=styles['Heading1'],
                fontSize=16 if self.one_page else 20,
                spaceAfter=4 if self.one_page else 6,
                alignment=TA_CENTER,
                textColor=Color(0.1, 0.15, 0.2),
                fontName='Helvetica-Bold'
            ),
            'Title': ParagraphStyle(
                'Title',
                parent=styles['Normal'],
                fontSize=base_size,
                spaceAfter=4 if self.one_page else 6,
                alignment=TA_CENTER,
                textColor=Color(0.2, 0.3, 0.4),
                fontName='Helvetica-Bold'
            ),
            'Contact': ParagraphStyle(
                'Contact',
                parent=styles['Normal'],
                fontSize=base_size - 1,
                spaceAfter=8 if self.one_page else 12,
                alignment=TA_CENTER,
                textColor=Color(0.3, 0.3, 0.3)
            ),
            'SectionHeader': ParagraphStyle(
                'SectionHeader',
                parent=styles['Heading2'],
                fontSize=base_size + 2,
                spaceAfter=4 if self.one_page else 6,
                spaceBefore=8 if self.one_page else 12,
                textColor=Color(0.1, 0.15, 0.2),
                fontName='Helvetica-Bold'
            ),
            'JobTitle': ParagraphStyle(
                'JobTitle',
                parent=styles['Normal'],
                fontSize=base_size,
                spaceAfter=2,
                textColor=black,
                fontName='Helvetica-Bold'
            ),
            'Company': ParagraphStyle(
                'Company',
                parent=styles['Normal'],
                fontSize=base_size,
                spaceAfter=2,
                textColor=black,
                fontName='Helvetica-Bold'
            ),
            'DateLocation': ParagraphStyle(
                'DateLocation',
                parent=styles['Normal'],
                fontSize=base_size - 1,
                spaceAfter=4 if self.one_page else 6,
                textColor=Color(0.4, 0.4, 0.4),
                fontName='Helvetica-Oblique'
            ),
            'Body': ParagraphStyle(
                'Body',
                parent=styles['Normal'],
                fontSize=base_size,
                spaceAfter=3 if self.one_page else 4,
                alignment=TA_JUSTIFY,
                leftIndent=12,
                bulletIndent=12
            ),
            'Skills': ParagraphStyle(
                'Skills',
                parent=styles['Normal'],
                fontSize=base_size,
                spaceAfter=4 if self.one_page else 6,
                alignment=TA_JUSTIFY
            )
        }
        
        return custom_styles
    
    def _parse_markdown_content(self, content: str) -> List[Dict]:
        """Parse markdown content into structured data."""
        lines = content.strip().split('\\n')
        sections = []
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Header level 1 (Name)
            if line.startswith('# '):
                if current_section:
                    current_section['content'] = current_content
                    sections.append(current_section)
                current_section = {
                    'type': 'name',
                    'title': line[2:].strip(),
                    'content': []
                }
                current_content = []
            
            # Header level 2 (Sections)
            elif line.startswith('## '):
                if current_section:
                    current_section['content'] = current_content
                    sections.append(current_section)
                current_section = {
                    'type': 'section',
                    'title': line[3:].strip(),
                    'content': []
                }
                current_content = []
            
            # Regular content
            else:
                current_content.append(line)
        
        # Add the last section
        if current_section:
            current_section['content'] = current_content
            sections.append(current_section)
        
        return sections
    
    def _clean_text(self, text: str) -> str:
        """Clean markdown formatting for ReportLab."""
        # Remove markdown formatting but preserve structure
        text = re.sub(r'\\*\\*(.*?)\\*\\*', r'<b>\\1</b>', text)  # Bold
        text = re.sub(r'\\*(.*?)\\*', r'<i>\\1</i>', text)      # Italic
        text = re.sub(r'`(.*?)`', r'<font name="Courier">\\1</font>', text)  # Code
        
        # Handle links
        text = re.sub(r'\\[([^\\]]+)\\]\\(([^)]+)\\)', r'<link href="\\2">\\1</link>', text)
        
        return text
    
    def _build_pdf_content(self, sections: List[Dict]) -> List:
        """Build the PDF content from parsed sections."""
        story = []
        
        for section in sections:
            if section['type'] == 'name':
                # Name and title section
                story.append(Paragraph(section['title'], self.styles['Name']))
                
                # Look for title and contact info in content
                for line in section['content']:
                    if line.startswith('**') and line.endswith('**'):
                        # This is likely the title
                        title = line[2:-2]
                        story.append(Paragraph(title, self.styles['Title']))
                    elif '@' in line or 'linkedin' in line.lower():
                        # This is likely contact info
                        clean_line = self._clean_text(line)
                        story.append(Paragraph(clean_line, self.styles['Contact']))
                
                # Add separator
                story.append(Spacer(1, 8 if self.one_page else 12))
            
            elif section['type'] == 'section':
                # Section header
                story.append(Paragraph(section['title'], self.styles['SectionHeader']))
                
                # Process section content
                current_entry = []
                
                for line in section['content']:
                    if line.startswith('**') and not line.startswith('***'):
                        # Company or institution name
                        if current_entry:
                            story.extend(self._format_entry(current_entry))
                            current_entry = []
                        
                        company = line.strip('*')
                        current_entry.append(('company', company))
                    
                    elif line.startswith('*') and '|' in line:
                        # Date and location
                        date_loc = line.strip('*').strip()
                        current_entry.append(('date_location', date_loc))
                    
                    elif line.startswith('- '):
                        # Bullet point
                        bullet = line[2:]
                        current_entry.append(('bullet', bullet))
                    
                    elif line and not line.startswith('#'):
                        # Regular content
                        current_entry.append(('content', line))
                
                # Add the last entry
                if current_entry:
                    story.extend(self._format_entry(current_entry))
                
                story.append(Spacer(1, 6 if self.one_page else 10))
        
        return story
    
    def _format_entry(self, entry: List[Tuple[str, str]]) -> List:
        """Format a single entry (job, education, etc.)."""
        formatted = []
        
        for entry_type, content in entry:
            clean_content = self._clean_text(content)
            
            if entry_type == 'company':
                formatted.append(Paragraph(clean_content, self.styles['Company']))
            elif entry_type == 'date_location':
                formatted.append(Paragraph(clean_content, self.styles['DateLocation']))
            elif entry_type == 'bullet':
                formatted.append(Paragraph(f"• {clean_content}", self.styles['Body']))
            elif entry_type == 'content':
                if clean_content.startswith('**') and clean_content.endswith('**'):
                    # Job title
                    title = clean_content[2:-2]
                    formatted.append(Paragraph(title, self.styles['JobTitle']))
                else:
                    formatted.append(Paragraph(clean_content, self.styles['Skills']))
        
        if formatted:
            formatted.append(Spacer(1, 4 if self.one_page else 6))
        
        return [KeepTogether(formatted)]
    
    def generate_pdf(self, markdown_file: str, output_filename: Optional[str] = None) -> Tuple[str, str]:
        """Generate PDF from markdown file."""
        # Read markdown file
        markdown_path = Path(markdown_file)
        if not markdown_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_file}")
        
        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Parse content
        sections = self._parse_markdown_content(markdown_content)
        
        # Generate output filename
        if output_filename is None:
            base_name = markdown_path.stem
            suffix = "_one_page_rl" if self.one_page else "_full_rl"
            output_filename = f"{base_name}{suffix}.pdf"
        
        output_path = self.output_dir / output_filename
        
        # Set up PDF document
        margins = 0.4*inch if self.one_page else 0.75*inch
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            topMargin=margins,
            bottomMargin=margins,
            leftMargin=margins,
            rightMargin=margins
        )
        
        # Build PDF content
        story = self._build_pdf_content(sections)
        
        # Generate PDF
        doc.build(story)
        
        return str(output_path), ""


def open_pdf(pdf_path: str):
    """Open PDF file using the appropriate system command."""
    if platform.system() == "Darwin":  # macOS
        subprocess.run(["open", pdf_path])
    elif platform.system() == "Windows":
        subprocess.run(["start", pdf_path], shell=True)
    else:  # Linux
        subprocess.run(["xdg-open", pdf_path])


@click.command()
@click.argument('markdown_file', type=click.Path(exists=True))
@click.option('--one-page', '-1', is_flag=True, help='Generate a one-page resume with compressed formatting')
@click.option('--output', '-o', help='Output filename (without extension)')
@click.option('--output-dir', default='output', help='Output directory (default: output)')
@click.option('--open-pdf', is_flag=True, help='Open the generated PDF after creation')
@click.option('--engine', type=click.Choice(['auto', 'weasyprint', 'reportlab']), default='auto', help='PDF generation engine')
def main(markdown_file: str, one_page: bool, output: Optional[str], output_dir: str, open_pdf_flag: bool, engine: str):
    """
    Convert a Markdown resume to a professionally formatted PDF.
    
    MARKDOWN_FILE: Path to the input markdown resume file
    """
    try:
        # Determine which engine to use
        use_weasyprint = False
        if engine == 'weasyprint':
            if not WEASYPRINT_AVAILABLE:
                click.echo("❌ WeasyPrint not available. Install required system dependencies.", err=True)
                sys.exit(1)
            use_weasyprint = True
        elif engine == 'auto':
            use_weasyprint = WEASYPRINT_AVAILABLE
        # else use reportlab (engine == 'reportlab')
        
        # Create resume builder
        if use_weasyprint:
            builder = WeasyPrintResumeBuilder(one_page=one_page, output_dir=output_dir)
            engine_name = "WeasyPrint"
        else:
            builder = ReportLabResumeBuilder(one_page=one_page, output_dir=output_dir)
            engine_name = "ReportLab"
        
        # Generate PDF
        click.echo(f"Converting {markdown_file} to PDF using {engine_name}...")
        
        if use_weasyprint:
            pdf_path, html_path = builder.generate_pdf(markdown_file, output)
            if html_path:
                click.echo(f"   HTML: {html_path}")
        else:
            pdf_path, _ = builder.generate_pdf(markdown_file, output)
        
        # Success message
        mode = "one-page" if one_page else "multi-page"
        click.echo(f"✅ Successfully generated {mode} resume:")
        click.echo(f"   PDF: {pdf_path}")
        
        # Open PDF if requested
        if open_pdf_flag:
            open_pdf(pdf_path)
        
        # File size info
        pdf_size = os.path.getsize(pdf_path)
        click.echo(f"   Size: {pdf_size / 1024:.1f} KB")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
