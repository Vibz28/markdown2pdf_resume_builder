"""Tests for the ResumeBuilder class."""

import os
from pathlib import Path

import pytest

from markdown2pdf_resume_builder.resume_builder import ResumeBuilder


class TestResumeBuilder:
    """Test cases for the ResumeBuilder class."""
    
    def test_init_default_params(self):
        """Test ResumeBuilder initialization with default parameters."""
        builder = ResumeBuilder()
        assert builder.one_page is False
        assert builder.output_dir.name == "output"
        assert builder.font_scheme == "modern"
    
    def test_init_custom_params(self):
        """Test ResumeBuilder initialization with custom parameters."""
        builder = ResumeBuilder(
            one_page=True, 
            output_dir="custom_output",
            header_color="#FF0000",
            font_scheme="classic"
        )
        assert builder.one_page is True
        assert builder.output_dir.name == "custom_output"
        assert builder.font_scheme == "classic"
    
    def test_estimate_content_length(self, sample_markdown):
        """Test content length estimation."""
        builder = ResumeBuilder()
        length = builder._estimate_content_length(sample_markdown)
        assert length > 0
        assert isinstance(length, int)
    
    def test_get_dynamic_sizing_one_page(self):
        """Test dynamic sizing for one-page mode."""
        builder = ResumeBuilder(one_page=True)
        
        # Test different content lengths
        short_content_sizing = builder._get_dynamic_sizing(1000)
        long_content_sizing = builder._get_dynamic_sizing(4000)
        
        # Longer content should have smaller fonts
        assert long_content_sizing['base_size'] < short_content_sizing['base_size']
        assert long_content_sizing['name_size'] < short_content_sizing['name_size']
    
    def test_get_dynamic_sizing_multi_page(self):
        """Test dynamic sizing for multi-page mode."""
        builder = ResumeBuilder(one_page=False)
        sizing = builder._get_dynamic_sizing(5000)  # Content length shouldn't matter
        
        assert sizing['base_size'] == 11
        assert sizing['name_size'] == 20
        assert sizing['section_size'] == 14
        assert sizing['small_size'] == 9
    
    def test_parse_markdown_content(self, sample_markdown):
        """Test markdown content parsing."""
        builder = ResumeBuilder()
        sections = builder._parse_markdown_content(sample_markdown)
        
        assert len(sections) > 0
        
        # Should have name section
        name_sections = [s for s in sections if s['type'] == 'name']
        assert len(name_sections) == 1
        assert name_sections[0]['title'] == "John Doe"
        
        # Should have regular sections
        regular_sections = [s for s in sections if s['type'] == 'section']
        section_titles = [s['title'] for s in regular_sections]
        assert "EDUCATION" in section_titles
        assert "WORK EXPERIENCE" in section_titles
        assert "SKILLS" in section_titles
        assert "PROJECTS" in section_titles
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        builder = ResumeBuilder()
        
        # Test link processing
        text_with_link = "[Google](https://google.com)"
        cleaned = builder._clean_text(text_with_link)
        assert '<link href="https://google.com" color="blue"><u>Google</u></link>' in cleaned
        
        # Test bold formatting
        text_with_bold = "**Bold Text**"
        cleaned = builder._clean_text(text_with_bold)
        assert "<b>Bold Text</b>" in cleaned
        
        # Test italic formatting
        text_with_italic = "*Italic Text*"
        cleaned = builder._clean_text(text_with_italic)
        assert "<i>Italic Text</i>" in cleaned
    
    def test_reorder_sections(self, sample_markdown):
        """Test section reordering functionality."""
        builder = ResumeBuilder()
        sections = builder._parse_markdown_content(sample_markdown)
        reordered = builder._reorder_sections(sections)
        
        # Find section titles in order
        section_titles = []
        for section in reordered:
            if section['type'] == 'section':
                section_titles.append(section['title'].lower())
        
        # Education should come before experience
        education_idx = None
        experience_idx = None
        for i, title in enumerate(section_titles):
            if 'education' in title:
                education_idx = i
            elif 'experience' in title or 'work' in title:
                experience_idx = i
        
        if education_idx is not None and experience_idx is not None:
            assert education_idx < experience_idx
    
    def test_generate_pdf(self, temp_markdown_file, tmp_path):
        """Test PDF generation."""
        builder = ResumeBuilder(output_dir=str(tmp_path))
        
        # Generate PDF
        pdf_path = builder.generate_pdf(temp_markdown_file)
        
        # Check that PDF was created
        assert os.path.exists(pdf_path)
        assert pdf_path.endswith('.pdf')
        
        # Check file size is reasonable
        file_size = os.path.getsize(pdf_path)
        assert file_size > 1000  # Should be at least 1KB
    
    def test_generate_pdf_one_page(self, temp_markdown_file, tmp_path):
        """Test one-page PDF generation."""
        builder = ResumeBuilder(one_page=True, output_dir=str(tmp_path))
        
        # Generate PDF
        pdf_path = builder.generate_pdf(temp_markdown_file, "one_page_test.pdf")
        
        # Check that PDF was created
        assert os.path.exists(pdf_path)
        assert "one_page_test.pdf" in pdf_path
    
    def test_generate_pdf_file_not_found(self):
        """Test PDF generation with non-existent file."""
        builder = ResumeBuilder()
        
        with pytest.raises(FileNotFoundError):
            builder.generate_pdf("non_existent_file.md")
