#!/bin/bash

# Example usage script for the Markdown to PDF Resume Builder
# This script demonstrates all the features and improvements

echo "🚀 Markdown to PDF Resume Builder - Example Usage"
echo "=================================================="

# Set the Python path for the virtual environment
PYTHON_PATH="/Users/vibhorjaney/Library/CloudStorage/OneDrive-Personal/Resume Versions/markdown2pdf_resume_builder/.venv/bin/python"

echo ""
echo "📄 Generating resume with all improvements:"
echo "✅ Visible hyperlinks (blue color + underline)"
echo "✅ Fixed semicolon bug in job titles"  
echo "✅ Reordered sections: Education → Experience → Skills → Projects → Courses"
echo "✅ Template-style formatting with colored header"
echo ""

# Generate one-page resume with template styling
echo "🔸 Creating one-page resume with template styling..."
$PYTHON_PATH main.py resume_vibhor_janey_updated_aug_2025.md \
    --one-page \
    --header-color="#4A6741" \
    --font-scheme="modern"

echo ""

# Generate multi-page resume  
echo "🔸 Creating multi-page resume..."
$PYTHON_PATH main.py resume_vibhor_janey_updated_aug_2025.md \
    --header-color="#4A6741" \
    --font-scheme="modern"

echo ""

# Show available options
echo "🔸 Available customization options:"
echo "   --header-color: Change header background color (default: #4A6741)"
echo "   --font-scheme: Font styling scheme (default: modern)"
echo "   --one-page: Compress to one page with dynamic sizing"
echo "   --open-pdf: Automatically open PDF after generation"

echo ""
echo "📁 Output files generated in 'output/' directory:"
ls -la output/*.pdf 2>/dev/null | head -5

echo ""
echo "✨ All improvements implemented successfully!"
echo "   • Hyperlinks are now blue and underlined for visibility"
echo "   • Semicolon bug in job titles is fixed"
echo "   • Section order follows: Education → Experience → Skills → Projects → Courses"
echo "   • Template-style header with colored background and white text"
echo "   • Section headers have icons and styled backgrounds"
echo "   • Customizable colors and fonts via command-line flags"
