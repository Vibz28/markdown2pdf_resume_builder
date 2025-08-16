#!/usr/bin/env python3
"""
Legacy entry point for backward compatibility.

For new usage, prefer:
    python -m markdown2pdf_resume_builder
    or
    resume-builder (if installed)
"""

import sys
import warnings
from pathlib import Path

# Add src to path for development
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

try:
    from markdown2pdf_resume_builder.cli import main
except ImportError as e:
    print(f"Error importing package: {e}")
    print("Make sure the package is installed or you're running from the correct directory.")
    sys.exit(1)

if __name__ == "__main__":
    warnings.warn(
        "Using main.py directly is deprecated. "
        "Use 'python -m markdown2pdf_resume_builder' or install the package.",
        DeprecationWarning,
        stacklevel=2
    )
    main()
