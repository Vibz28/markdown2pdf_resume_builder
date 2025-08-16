"""Markdown to PDF Resume Builder.

A professional, ATS-friendly resume builder that converts Markdown files to beautifully 
formatted PDFs with dynamic sizing, interactive features, and template-style formatting.
"""

__version__ = "1.0.0"
__author__ = "Vibhor Janey"
__email__ = "vibhor.janey@gmail.com"

from .resume_builder import ResumeBuilder
from .cli import main

__all__ = ["ResumeBuilder", "main"]
