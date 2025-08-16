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
from reportlab.platypus.flowables import HRFlowable

from .themes import get_theme
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


class ResumeBuilder:
    """Main class for building PDF resumes from Markdown files using ReportLab."""
    
    def __init__(self, one_page: bool = False, output_dir: str = "output", 
                 header_color: str = "white", font_scheme: str = "modern", theme: str = "light"):
        self.one_page = one_page
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.content_length = 0
        self.styles = None  # Will be created after content analysis
        self.theme = get_theme(theme)
        
        # Template styling options
        self.header_color_hex = header_color
        self.is_white_background = header_color.lower() == "white" or header_color == "#ffffff"
        if self.is_white_background:
            # Use theme background for header in white mode
            self.header_color = self.theme.get_color('card')
            self.header_text_color = self.theme.get_color('fg')
        else:
            self.header_color = Color(*[int(header_color.lstrip('#')[i:i+2], 16)/255.0 for i in (0, 2, 4)])
            self.header_text_color = white
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
        
        # More aggressive dynamic sizing for one-page based on content length
        # Target: make it fit on one page regardless of content density
        if content_length <= 2000:
            scale = 1.0
        elif content_length <= 2500:
            scale = 0.95
        elif content_length <= 3000:
            scale = 0.9
        elif content_length <= 3500:
            scale = 0.85
        elif content_length <= 4000:
            scale = 0.75
        elif content_length <= 4500:
            scale = 0.65
        elif content_length <= 5000:
            scale = 0.6
        else:
            scale = 0.55  # Very dense content
        
        return {
            'base_size': 9.5 * scale,
            'name_size': 16 * scale,
            'section_size': 11 * scale,
            'small_size': 8 * scale
        }
    
    def create_styles(self):
        """Create paragraph styles based on content length and one-page settings."""
        base_styles = getSampleStyleSheet()
        
        # Use dynamic sizing for one-page resumes, standard sizing for multi-page
        if self.one_page:
            # Get dynamic sizing based on content length
            sizing = self._get_dynamic_sizing(self.content_length)
            font_size = sizing['base_size']
            title_size = sizing['section_size']
            name_size = sizing['name_size']
            spacing = max(1, int(sizing['base_size'] * 0.2))  # Reduced spacing
        else:
            # Standard multi-page sizing
            if self.content_length > 5000:
                font_size = 9
                title_size = 12
                name_size = 16
                spacing = 2
                # font_size = 9
                # title_size = 14
                # name_size = 18
                # spacing = 3
            elif self.content_length > 3000:
                font_size = 9
                title_size = 14
                name_size = 18
                spacing = 3
                # font_size = 10
                # title_size = 16
                # name_size = 20
                # spacing = 4
            else:
                font_size = 11
                title_size = 18
                name_size = 22
                spacing = 6

        # Theme-based font selection (matching HTML template)
        font_family = self.theme.fonts['primary']
        if self.font_scheme == "serif":
            font_family = "Times-Roman"
        elif self.font_scheme == "sans":
            font_family = "Helvetica"  # Clean, modern font like Inter
        
        self.styles = {
            'Name': ParagraphStyle(
                'Name',
                parent=base_styles['Heading1'],
                fontSize=name_size+1,
                fontName=f'{font_family}-Bold',
                textColor=self.header_text_color,
                alignment=1,  # Center
                spaceAfter=0,  # Reduced header spacing
                spaceBefore=0,
            ),
            'Title': ParagraphStyle(
                'Title',
                parent=base_styles['Normal'],
                fontSize=title_size+1,  # Slightly larger
                fontName=font_family,
                textColor=self.theme.get_color('muted'),  # Muted color like HTML
                alignment=1,  # Center
                spaceAfter=2 if self.one_page else spacing,  # Reduced header spacing
                spaceBefore=0,
            ),
            'Contact': ParagraphStyle(
                'Contact',
                parent=base_styles['Normal'],
                fontSize=font_size+2,
                fontName=font_family,
                textColor=self.theme.get_color('fg'),
                alignment=1,  # Center
                spaceAfter=1 if self.one_page else 2,  # Reduced header spacing
                spaceBefore=0,
            ),
            'SectionHeader': ParagraphStyle(
                'SectionHeader',
                parent=base_styles['Heading2'],
                fontSize=font_size-1,  # Smaller, uppercase-style headers
                fontName=f'{font_family}-Bold',
                textColor=self.theme.get_color('muted'),  # Muted like HTML
                spaceAfter=spacing,
                spaceBefore=spacing,
                leftIndent=0,
            ),
            'JobTitle': ParagraphStyle(
                'JobTitle',
                parent=base_styles['Normal'],
                fontSize=font_size,  # Same as company for balance
                fontName=f'{font_family}-Bold',
                textColor=self.theme.get_color('fg'),
                spaceAfter=1,
                spaceBefore=spacing-2 if spacing > 2 else 0,
            ),
            'Company': ParagraphStyle(
                'Company',
                parent=base_styles['Normal'],
                fontSize=font_size,  # Base size for company
                fontName=f'{font_family}-Bold',
                textColor=self.theme.get_color('fg'),
                spaceAfter=1,
                spaceBefore=0,
            ),
            'DateLocation': ParagraphStyle(
                'DateLocation',
                parent=base_styles['Normal'],
                fontSize=font_size-1.5,  # Smaller for dates
                fontName=font_family,
                textColor=self.theme.get_color('muted'),  # Muted color
                spaceAfter=spacing-2 if spacing > 2 else 1,
                spaceBefore=0,
            ),
            'Body': ParagraphStyle(
                'Body',
                parent=base_styles['Normal'],
                fontSize=font_size,
                fontName=font_family,
                textColor=self.theme.get_color('fg'),
                spaceAfter=1 if self.one_page else 2,
                spaceBefore=0,
                leftIndent=12,
            ),
            'Skills': ParagraphStyle(
                'Skills',
                parent=base_styles['Normal'],
                fontSize=font_size-0.5,  # Slightly smaller for skills
                fontName=font_family,
                textColor=self.theme.get_color('fg'),
                spaceAfter=1 if self.one_page else 2,
                spaceBefore=0,
            ),
        }
    
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
            
            # Skip horizontal rules/separators
            if line.startswith('---') or line == '---':
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
        # Use theme-aware link color
        link_color = "cyan" if self.theme.name == "dark" else "blue"
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', rf'<link href="\2" color="{link_color}"><u>\1</u></link>', text)
        
        # Handle bold+italic combination first: _**text**_ or **_text_**
        text = re.sub(r'_\*\*([^*]+)\*\*_', r'<b><i>\1</i></b>', text)  # _**text**_ -> bold+italic
        text = re.sub(r'\*\*_([^_]+)_\*\*', r'<b><i>\1</i></b>', text)  # **_text_** -> bold+italic
        
        # Then handle remaining markdown formatting
        text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)  # Bold
        text = re.sub(r'_([^_]+)_', r'<i>\1</i>', text)        # Italic (underscores)
        text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)      # Italic (asterisks)
        text = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', text)  # Code
        
        return text
    
    def _reorder_sections(self, sections: List[Dict]) -> List[Dict]:
        """Reorder sections to: Experience, Education, Skills, Projects, Courses."""
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
        for section_key in ['experience', 'education', 'projects', 'skills', 'courses']:
            if section_key in section_map:
                reordered.append(section_map[section_key])
        
        # Add any other sections at the end
        reordered.extend(other_sections)
        
        return reordered
    
    def _create_header_table(self, name: str, title: str, contact_lines: List[str]) -> Table:
        """Create the header table with clean styling."""
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
        
        # Create table with appropriate width (not full margin width)
        table = Table(header_data, colWidths=[6.5*inch])
        
        # Apply styling based on background color choice with minimal padding
        if self.is_white_background:
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),   # Reduced padding
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),  # Reduced padding
                ('TOPPADDING', (0, 0), (-1, -1), 2),    # Minimal top padding
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4 if self.one_page else 8),  # Reduced bottom padding
            ]))
        else:
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), self.header_color),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
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
                
                # Add separator with minimal spacing for one-page
                story.append(Spacer(1, 3 if self.one_page else 15))
            
            elif section['type'] == 'section':
                # Clean section header without icons or boxes
                section_title = section['title'].upper()  # Uppercase for professional look
                
                story.append(Paragraph(section_title, self.styles['SectionHeader']))
                
                # Special handling for skills section to use chip-like formatting
                if 'skill' in section['title'].lower():
                    story.extend(self._format_skills_section(section['content']))
                elif 'education' in section['title'].lower():
                    # Special handling for education section - horizontal layout
                    story.extend(self._format_education_section(section['content']))
                else:
                    # Process section content normally
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
    
    def _format_skills_section(self, content: List[str]) -> List:
        """Format skills section with chip-like styling."""
        formatted = []
        current_category = None
        
        for line in content:
            clean_line = self._clean_text(line)
            if clean_line.startswith('**') and clean_line.endswith('**'):
                # Category header
                category = clean_line[2:-2]  # Remove ** markers
                if current_category:
                    formatted.append(Spacer(1, 4))  # Space between categories
                
                # Create category header with muted styling
                cat_style = ParagraphStyle(
                    'SkillCategory',
                    parent=self.styles['Skills'],
                    fontSize=self.styles['Skills'].fontSize - 1,
                    fontName=f"{self.theme.fonts['primary']}-Bold",
                    textColor=self.theme.get_color('muted'),
                    spaceAfter=2,
                    spaceBefore=0,
                )
                formatted.append(Paragraph(category, cat_style))
                current_category = category
            else:
                # Skills list - keep original comma formatting from markdown
                formatted.append(Paragraph(clean_line, self.styles['Skills']))
                
        return formatted
    
    def _format_education_section(self, content: List[str]) -> List:
        """Format education section with horizontal layout for institutions."""
        formatted = []
        education_entries = []
        current_entry = []
        
        # Parse education entries
        for line in content:
            clean_line = self._clean_text(line)
            if clean_line.startswith('**') and clean_line.endswith('**'):
                # Institution name with degree - this is a new entry
                if current_entry:
                    education_entries.append(current_entry)
                    current_entry = []
                current_entry.append(('institution_degree', clean_line))
            elif clean_line and not clean_line.startswith('#') and not clean_line.startswith('**'):
                # Date and location info
                current_entry.append(('date_location', clean_line))
        
        # Add the last entry
        if current_entry:
            education_entries.append(current_entry)
        
        # Create side-by-side layout for education entries
        if education_entries and len(education_entries) >= 2:
            # Extract data for both entries
            left_institution_degree = ""
            left_date_location = ""
            right_institution_degree = ""
            right_date_location = ""
            
            # Process left entry (first education item)
            for entry_type, content_item in education_entries[0]:
                if entry_type == 'institution_degree':
                    left_institution_degree = str(content_item)
                elif entry_type == 'date_location':
                    left_date_location = str(content_item)
            
            # Process right entry (second education item)
            for entry_type, content_item in education_entries[1]:
                if entry_type == 'institution_degree':
                    right_institution_degree = str(content_item)
                elif entry_type == 'date_location':
                    right_date_location = str(content_item)
            
            # Create table data with institution/degree row and date/location row
            table_data = [
                [
                    Paragraph(left_institution_degree, self.styles['Company']),
                    Paragraph(right_institution_degree, self.styles['Company'])
                ],
                [
                    Paragraph(left_date_location, self.styles['DateLocation']),
                    Paragraph(right_date_location, self.styles['DateLocation'])
                ]
            ]
            
            # Create table with equal column widths for side-by-side display
            from reportlab.lib.units import inch
            
            education_table = Table(table_data, colWidths=[3.2*inch, 3.2*inch])
            education_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Left align all content
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [None, None])  # No backgrounds
            ]))
            
            formatted.append(education_table)
            
        else:
            # Fallback for single entry or more than two entries
            for entry in education_entries:
                for entry_type, content_item in entry:
                    if entry_type == 'institution_degree':
                        formatted.append(Paragraph(str(content_item), self.styles['Company']))
                    elif entry_type == 'date_location':
                        formatted.append(Paragraph(str(content_item), self.styles['DateLocation']))
                formatted.append(Spacer(1, 4))
        
        return formatted
                
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
        self.create_styles()
        
        # Parse content
        sections = self._parse_markdown_content(markdown_content)
        
        # Generate output filename
        if output_filename is None:
            base_name = markdown_path.stem
            suffix = "_one_page" if self.one_page else "_full"
            output_filename = f"{base_name}{suffix}.pdf"
        
        output_path = self.output_dir / output_filename
        
        # Set up PDF document with theme-aware styling
        margins = 0.3*inch if self.one_page else 0.75*inch
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            topMargin=margins,
            bottomMargin=margins,
            leftMargin=margins,
            rightMargin=margins
        )
        
        # Build PDF content with theme support
        story = self._build_pdf_content(sections)
        
        # Apply theme background if dark mode
        def apply_theme_background(canvas, doc):
            if self.theme.name == 'dark':
                canvas.setFillColor(self.theme.get_color('bg'))
                canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
        
        # Generate PDF with theme support
        if self.theme.name == 'dark':
            doc.build(story, onFirstPage=apply_theme_background, onLaterPages=apply_theme_background)
        else:
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
