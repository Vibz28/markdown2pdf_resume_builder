#!/usr/bin/env python3
"""
Alternative Resume Builder using ReportLab for better cross-platform compatibility
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional, Tuple, List, Dict

import click
import markdown2
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, black, blue
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


class ReportLabResumeBuilder:
    """Resume builder using ReportLab for PDF generation."""
    
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
        lines = content.strip().split('\n')
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
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)      # Italic
        text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)  # Code
        
        # Handle links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<link href="\2">\1</link>', text)
        
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
    
    def generate_pdf(self, markdown_file: str, output_filename: Optional[str] = None) -> str:
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
        
        return str(output_path)


@click.command()
@click.argument('markdown_file', type=click.Path(exists=True))
@click.option('--one-page', '-1', is_flag=True, help='Generate a one-page resume with compressed formatting')
@click.option('--output', '-o', help='Output filename (without extension)')
@click.option('--output-dir', default='output', help='Output directory (default: output)')
@click.option('--open-pdf', is_flag=True, help='Open the generated PDF after creation')
def main(markdown_file: str, one_page: bool, output: Optional[str], output_dir: str, open_pdf: bool):
    """
    Convert a Markdown resume to a professionally formatted PDF using ReportLab.
    
    MARKDOWN_FILE: Path to the input markdown resume file
    """
    try:
        # Create resume builder
        builder = ReportLabResumeBuilder(one_page=one_page, output_dir=output_dir)
        
        # Generate PDF
        click.echo(f"Converting {markdown_file} to PDF using ReportLab...")
        pdf_path = builder.generate_pdf(markdown_file, output)
        
        # Success message
        mode = "one-page" if one_page else "multi-page"
        click.echo(f"✅ Successfully generated {mode} resume: {pdf_path}")
        
        # Open PDF if requested
        if open_pdf:
            import subprocess
            import platform
            
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", pdf_path])
            elif platform.system() == "Windows":
                subprocess.run(["start", pdf_path], shell=True)
            else:  # Linux
                subprocess.run(["xdg-open", pdf_path])
        
        # File size info
        pdf_size = os.path.getsize(pdf_path)
        click.echo(f"   Size: {pdf_size / 1024:.1f} KB")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
