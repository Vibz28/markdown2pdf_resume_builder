"""Core resume builder functionality."""

import os
import re
import platform
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Tuple

import markdown2
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, black, blue, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


class ResumeBuilder:
    """Main class for building PDF resumes from Markdown files using ReportLab."""
    
    def __init__(self, one_page: bool = False, output_dir: str = "output", 
                 header_color: str = "#4A6741", font_scheme: str = "modern"):
        self.one_page = one_page
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.content_length = 0
        self.styles = None  # Will be created after content analysis
        
        # Template styling options
        self.header_color = Color(*[int(header_color.lstrip('#')[i:i+2], 16)/255.0 for i in (0, 2, 4)])
        self.font_scheme = font_scheme
    
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
                textColor=white,
                fontName='Helvetica-Bold'
            ),
            'Title': ParagraphStyle(
                'Title',
                parent=styles['Normal'],
                fontSize=base_size,
                spaceAfter=2 if self.one_page else 6,
                alignment=TA_CENTER,
                textColor=white,
                fontName='Helvetica-Oblique'
            ),
            'Contact': ParagraphStyle(
                'Contact',
                parent=styles['Normal'],
                fontSize=small_size,
                spaceAfter=4 if self.one_page else 12,
                alignment=TA_CENTER,
                textColor=white
            ),
            'SectionHeader': ParagraphStyle(
                'SectionHeader',
                parent=styles['Heading2'],
                fontSize=section_size,
                spaceAfter=2 if self.one_page else 6,
                spaceBefore=4 if self.one_page else 12,
                textColor=Color(0.1, 0.15, 0.2),
                fontName='Helvetica-Bold',
                borderWidth=1,
                borderColor=Color(0.7, 0.7, 0.7),
                backColor=Color(0.95, 0.95, 0.95)
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
        # Handle links first to avoid interference - make them visually distinct
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<link href="\2" color="blue"><u>\1</u></link>', text)
        
        # Remove markdown formatting but preserve structure
        # Fix: Be more careful with bold text to avoid adding semicolons
        text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)  # Bold
        text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)      # Italic (single asterisk, not bold)
        text = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', text)  # Code
        
        return text
    
    def _reorder_sections(self, sections: List[Dict]) -> List[Dict]:
        """Reorder sections to: Education, Experience, Skills, Projects, Courses."""
        name_section = None
        section_map = {}
        other_sections = []
        
        # Separate name section and categorize other sections
        for section in sections:
            if section['type'] == 'name':
                name_section = section
            elif section['type'] == 'section':
                title_lower = section['title'].lower()
                if 'education' in title_lower:
                    section_map['education'] = section
                elif 'experience' in title_lower or 'work' in title_lower:
                    section_map['experience'] = section
                elif 'skill' in title_lower:
                    section_map['skills'] = section
                elif 'project' in title_lower:
                    section_map['projects'] = section
                elif 'course' in title_lower:
                    section_map['courses'] = section
                else:
                    other_sections.append(section)
        
        # Build reordered list
        reordered = []
        if name_section:
            reordered.append(name_section)
        
        # Add sections in desired order
        for section_key in ['education', 'experience', 'skills', 'projects', 'courses']:
            if section_key in section_map:
                reordered.append(section_map[section_key])
        
        # Add any other sections at the end
        reordered.extend(other_sections)
        
        return reordered
    
    def _create_header_table(self, name: str, title: str, contact_lines: List[str]) -> Table:
        """Create the header table with colored background matching template."""
        # Process contact information into table cells
        contact_data = []
        for line in contact_lines:
            clean_line = self._clean_text(line)
            contact_data.append([Paragraph(clean_line, self.styles['Contact'])])
        
        # Create main header data
        header_data = [
            [Paragraph(name, self.styles['Name'])],
            [Paragraph(title, self.styles['Title'])]
        ]
        
        # Add contact rows
        header_data.extend(contact_data)
        
        # Create table
        table = Table(header_data, colWidths=[7.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.header_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return table
    
    def _build_pdf_content(self, sections: List[Dict]) -> List:
        """Build the PDF content from parsed sections."""
        # Reorder sections first
        sections = self._reorder_sections(sections)
        
        story = []
        
        for section in sections:
            if section['type'] == 'name':
                # Extract name, title, and contact info
                name = section['title']
                title = ""
                contact_lines = []
                
                for line in section['content']:
                    if line.startswith('**') and line.endswith('**'):
                        # This is likely the title
                        title = line[2:-2]
                    elif '@' in line or 'linkedin' in line.lower() or 'http' in line.lower() or '(' in line:
                        # This is likely contact info
                        contact_lines.append(line)
                
                # Create header table with colored background
                header_table = self._create_header_table(name, title, contact_lines)
                story.append(header_table)
                
                # Add separator
                story.append(Spacer(1, 6 if self.one_page else 15))
            
            elif section['type'] == 'section':
                # Section header with icon and styling
                section_title = f"🎓 {section['title']}" if 'education' in section['title'].lower() else \
                               f"💼 {section['title']}" if 'experience' in section['title'].lower() or 'work' in section['title'].lower() else \
                               f"🛠 {section['title']}" if 'skill' in section['title'].lower() else \
                               f"📂 {section['title']}" if 'project' in section['title'].lower() else \
                               f"📚 {section['title']}" if 'course' in section['title'].lower() else \
                               section['title']
                
                story.append(Paragraph(section_title, self.styles['SectionHeader']))
                
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
                if (clean_content.startswith('<b>') and clean_content.endswith('</b>') and 
                    '<link href=' in clean_content):
                    # Project title with link - remove the outer <b> tags since link already has styling
                    title = clean_content[3:-4]  # Remove <b> and </b> wrapper
                    formatted.append(Paragraph(title, self.styles['JobTitle']))
                elif clean_content.startswith('<b>') and clean_content.endswith('</b>'):
                    # Regular job/project title - remove <b> tags to avoid duplication with style
                    title = clean_content[3:-4]  # Remove <b> and </b>
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
