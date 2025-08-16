#!/usr/bin/env python3
"""
Markdown to PDF Resume Builder

A tool to convert markdown resumes to professionally formatted PDFs with dynamic sizing,
interactive features, and ATS-friendly formatting.

This version uses ReportLab for maximum compatibility across platforms.
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
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, black, blue
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


class ResumeBuilder:
    """Main class for building PDF resumes from Markdown files using ReportLab."""
    
    def __init__(self, one_page: bool = False, output_dir: str = "output"):
        self.one_page = one_page
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.content_length = 0
        self.styles = None  # Will be created after content analysis
    
    def _estimate_content_length(self, content: str) -> int:
        """Estimate the total content length for dynamic sizing."""
        # Count meaningful content (excluding markdown syntax)
        text_content = re.sub(r'[#*\-\[\]()]', '', content)
        text_content = re.sub(r'\s+', ' ', text_content)
        return len(text_content.strip())
    
    def _get_dynamic_sizing(self, content_length: int) -> Dict[str, float]:
        """Calculate dynamic font sizes based on content length."""
        if not self.one_page:
            return {
                'base_size': 11,
                'name_size': 20,
                'section_size': 14,
                'small_size': 9
            }
        
        # Dynamic sizing for one-page based on content length
        # Rough estimation: 2500 chars = comfortable, 3500+ = very tight
        if content_length <= 2000:
            scale = 1.0
        elif content_length <= 2500:
            scale = 0.95
        elif content_length <= 3000:
            scale = 0.9
        elif content_length <= 3500:
            scale = 0.85
        else:
            scale = 0.8
        
        return {
            'base_size': 8.5 * scale,
            'name_size': 14 * scale,
            'section_size': 10 * scale,
            'small_size': 7.5 * scale
        }
    
    def _create_styles(self, content_length: int) -> Dict[str, ParagraphStyle]:
        """Create custom paragraph styles for the resume."""
        styles = getSampleStyleSheet()
        
        # Get dynamic sizing based on content length
        sizing = self._get_dynamic_sizing(content_length)
        base_size = sizing['base_size']
        name_size = sizing['name_size']
        section_size = sizing['section_size']
        small_size = sizing['small_size']
        
        custom_styles = {
            'Name': ParagraphStyle(
                'Name',
                parent=styles['Heading1'],
                fontSize=name_size,
                spaceAfter=2 if self.one_page else 6,
                alignment=TA_CENTER,
                textColor=Color(0.1, 0.15, 0.2),
                fontName='Helvetica-Bold'
            ),
            'Title': ParagraphStyle(
                'Title',
                parent=styles['Normal'],
                fontSize=base_size,
                spaceAfter=2 if self.one_page else 6,
                alignment=TA_CENTER,
                textColor=Color(0.2, 0.3, 0.4),
                fontName='Helvetica-Bold'
            ),
            'Contact': ParagraphStyle(
                'Contact',
                parent=styles['Normal'],
                fontSize=small_size,
                spaceAfter=4 if self.one_page else 12,
                alignment=TA_CENTER,
                textColor=Color(0.3, 0.3, 0.3)
            ),
            'SectionHeader': ParagraphStyle(
                'SectionHeader',
                parent=styles['Heading2'],
                fontSize=section_size,
                spaceAfter=2 if self.one_page else 6,
                spaceBefore=4 if self.one_page else 12,
                textColor=Color(0.1, 0.15, 0.2),
                fontName='Helvetica-Bold'
            ),
            'JobTitle': ParagraphStyle(
                'JobTitle',
                parent=styles['Normal'],
                fontSize=base_size - 0.5,
                spaceAfter=1 if self.one_page else 2,
                textColor=black,
                fontName='Helvetica-Bold'
            ),
            'Company': ParagraphStyle(
                'Company',
                parent=styles['Normal'],
                fontSize=base_size,
                spaceAfter=1 if self.one_page else 2,
                textColor=black,
                fontName='Helvetica-Bold'
            ),
            'DateLocation': ParagraphStyle(
                'DateLocation',
                parent=styles['Normal'],
                fontSize=small_size,
                spaceAfter=2 if self.one_page else 6,
                textColor=Color(0.4, 0.4, 0.4),
                fontName='Helvetica-Oblique'
            ),
            'Body': ParagraphStyle(
                'Body',
                parent=styles['Normal'],
                fontSize=base_size - 0.5,
                spaceAfter=1.5 if self.one_page else 4,
                alignment=TA_JUSTIFY,
                leftIndent=10 if self.one_page else 12,
                bulletIndent=10 if self.one_page else 12,
                leading=(base_size - 0.5) * 1.2
            ),
            'Skills': ParagraphStyle(
                'Skills',
                parent=styles['Normal'],
                fontSize=base_size - 0.5,
                spaceAfter=2 if self.one_page else 6,
                alignment=TA_JUSTIFY,
                leading=(base_size - 0.5) * 1.2
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
        # Handle links first to avoid interference
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<link href="\2">\1</link>', text)
        
        # Remove markdown formatting but preserve structure
        # Fix: Be more careful with bold text to avoid adding semicolons
        text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)  # Bold
        text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)      # Italic (single asterisk, not bold)
        text = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', text)  # Code
        
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
                story.append(Spacer(1, 3 if self.one_page else 12))
            
            elif section['type'] == 'section':
                # Section header
                story.append(Paragraph(section['title'], self.styles['SectionHeader']))
                
                # Process section content
                current_entry = []
                
                for line in section['content']:
                    if line.startswith('**') and not line.startswith('***') and line.endswith('**'):
                        # Company or institution name
                        if current_entry:
                            story.extend(self._format_entry(current_entry))
                            current_entry = []
                        
                        company = line.strip('*')
                        current_entry.append(('company', company))
                    
                    elif line.startswith('*') and '|' in line and line.endswith('*'):
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
                
                story.append(Spacer(1, 2 if self.one_page else 10))
        
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
                # Check for project titles with links: **[Title](link)**
                if (clean_content.startswith('**') and clean_content.endswith('**') and 
                    '<link href=' in clean_content):
                    # Project title with link
                    title = clean_content[2:-2]  # Remove ** wrapper
                    formatted.append(Paragraph(title, self.styles['JobTitle']))
                elif clean_content.startswith('**') and clean_content.endswith('**'):
                    # Regular job/project title
                    title = clean_content[2:-2]
                    formatted.append(Paragraph(title, self.styles['JobTitle']))
                else:
                    formatted.append(Paragraph(clean_content, self.styles['Skills']))
        
        if formatted:
            formatted.append(Spacer(1, 2 if self.one_page else 6))
        
        return [KeepTogether(formatted)]
    
    def generate_pdf(self, markdown_file: str, output_filename: Optional[str] = None) -> str:
        """Generate PDF from markdown file."""
        # Read markdown file
        markdown_path = Path(markdown_file)
        if not markdown_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_file}")
        
        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Estimate content length for dynamic sizing
        self.content_length = self._estimate_content_length(markdown_content)
        
        # Create styles based on content analysis
        self.styles = self._create_styles(self.content_length)
        
        # Parse content
        sections = self._parse_markdown_content(markdown_content)
        
        # Generate output filename
        if output_filename is None:
            base_name = markdown_path.stem
            suffix = "_one_page" if self.one_page else "_full"
            output_filename = f"{base_name}{suffix}.pdf"
        
        output_path = self.output_dir / output_filename
        
        # Set up PDF document with more aggressive margins for one-page
        margins = 0.3*inch if self.one_page else 0.75*inch
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
@click.option('--open-pdf', 'open_pdf_flag', is_flag=True, help='Open the generated PDF after creation')
def main(markdown_file: str, one_page: bool, output: Optional[str], output_dir: str, open_pdf_flag: bool):
    """
    Convert a Markdown resume to a professionally formatted PDF.
    
    MARKDOWN_FILE: Path to the input markdown resume file
    """
    try:
        # Create resume builder
        builder = ResumeBuilder(one_page=one_page, output_dir=output_dir)
        
        # Generate PDF
        click.echo(f"Converting {markdown_file} to PDF...")
        pdf_path = builder.generate_pdf(markdown_file, output)
        
        # Success message
        mode = "one-page" if one_page else "multi-page"
        click.echo(f"✅ Successfully generated {mode} resume: {pdf_path}")
        
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
