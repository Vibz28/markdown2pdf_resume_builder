#!/bin/bash
# Example usage script for the Markdown to PDF Resume Builder

echo "🎯 Markdown to PDF Resume Builder - Example Usage"
echo "=================================================="
echo

# Set the resume file
RESUME_FILE="[YOUR_RESUME_FILE].md"

if [ ! -f "$RESUME_FILE" ]; then
    echo "❌ Resume file not found: $RESUME_FILE"
    echo "Please ensure your markdown resume file exists."
    exit 1
fi

echo "📄 Using resume file: $RESUME_FILE"
echo

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Please run 'uv sync' first."
    exit 1
fi

PYTHON_CMD=".venv/bin/python"

echo "1️⃣  Generating multi-page resume..."
$PYTHON_CMD main.py "$RESUME_FILE"
echo

echo "2️⃣  Generating one-page resume..."
$PYTHON_CMD main.py --one-page "$RESUME_FILE"
echo

echo "3️⃣  Generating custom output with auto-open..."
$PYTHON_CMD main.py --one-page --output "my_resume_custom" --open-pdf "$RESUME_FILE"
echo

echo "✅ Done! Check the 'output' directory for your PDFs."
echo
echo "📂 Generated files:"
ls -la output/*.pdf 2>/dev/null || echo "No PDF files found in output directory"
echo

echo "💡 Usage tips:"
echo "   • Use --one-page for single-page resumes"
echo "   • Use --output to specify custom filename"
echo "   • Use --open-pdf to automatically open the PDF"
echo "   • Check output directory for both PDF and HTML files"
