"""Command-line interface for the Markdown to PDF Resume Builder."""

import os
import sys
from typing import Optional

import click

from .resume_builder import ResumeBuilder, open_pdf


@click.command()
@click.argument('markdown_file', type=click.Path(exists=True))
@click.option('--one-page', '-1', is_flag=True, help='Generate a one-page resume with compressed formatting')
@click.option('--output', '-o', help='Output filename (without extension)')
@click.option('--output-dir', default='output', help='Output directory (default: output)')
@click.option('--open-pdf', 'open_pdf_flag', is_flag=True, help='Open the generated PDF after creation')
@click.option('--header-color', default='#4A6741', help='Header background color (default: #4A6741)')
@click.option('--font-scheme', default='modern', help='Font scheme (default: modern)')
def main(markdown_file: str, one_page: bool, output: Optional[str], output_dir: str, 
         open_pdf_flag: bool, header_color: str, font_scheme: str):
    """
    Convert a Markdown resume to a professionally formatted PDF.
    
    MARKDOWN_FILE: Path to the input markdown resume file
    """
    try:
        # Create resume builder
        builder = ResumeBuilder(
            one_page=one_page, 
            output_dir=output_dir,
            header_color=header_color,
            font_scheme=font_scheme
        )
        
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
