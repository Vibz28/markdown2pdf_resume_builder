# Markdown to PDF Resume Builder

A professional, ATS-friendly resume builder that converts Markdown files to beautifully formatted PDFs with dynamic sizing, interactive features, and template-style formatting.

## ✨ Key Features

### **🎨 Template-Style Formatting**
- **Colored Header Banner**: Professional header with customizable background color (default: #4A6741)
- **Section Icons**: Automatic icons for Education 🎓, Experience 💼, Skills 🛠, Projects 📂, Courses 📚
- **Styled Section Headers**: Bordered headers with background colors for visual hierarchy
- **White Text on Header**: Name, title, and contact info in white text on colored background

### **🔗 Enhanced Hyperlink Support**
- **Visual Links**: Hyperlinks are blue and underlined for clear visibility
- **Clickable PDFs**: All links preserved and functional in PDF output
- **Project Title Links**: Support for `**[Project Name](URL)**` format with proper styling
- **Contact Links**: Email and LinkedIn links automatically detected and styled

### **📄 Intelligent Layout**
- **Dynamic Font Sizing**: Automatically adjusts font size (6.8pt-8.5pt) based on content length
- **One-Page Optimization**: Aggressive compression algorithm for single-page resumes
- **Section Reordering**: Automatically orders sections as Education → Experience → Skills → Projects → Courses
- **Content-Aware Margins**: Adaptive margins (0.3" for one-page, 0.75" for multi-page)

### **🛠 Customization Options**
- **Header Colors**: Customize header background with `--header-color` flag
- **Font Schemes**: Choose font styling with `--font-scheme` flag  
- **Output Control**: Flexible output directory and filename options
- **Debug-Friendly**: Comprehensive error handling and validation

## 🚀 Quick Start

### Installation
```bash
# Clone and set up
git clone <repository-url>
cd markdown2pdf_resume_builder

# Install dependencies using uv
uv sync

# Or install manually
pip install reportlab markdown2 click
```

### Basic Usage
```bash
# Clean white header (default)
python main.py resume.md --one-page

# Colored header for branding
python main.py resume.md --header-color="#2C5F41"

# Open PDF automatically after generation
python main.py resume.md --one-page --open-pdf
```

### Advanced Options
```bash
# Full customization
python main.py resume.md \
    --one-page \
    --header-color="white" \
    --font-scheme="modern" \
    --output-dir="pdfs" \
    --output="my_resume" \
    --open-pdf
```

## 📝 Markdown Format

### Header Section (Name & Contact)
```markdown
# Your Name
**Your Professional Title**

[your.email@domain.com](mailto:your.email@domain.com) | (123) 456-7890 | [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile) | City, State
```

### Sections
```markdown
## EDUCATION

**University Name** — *Degree Title*  
Sep 2021 – Dec 2022 | City, State

## WORK EXPERIENCE

**Company Name**  
**Job Title**  
*Jan 2023 – present | City, State*

- Achievement or responsibility with specific metrics
- Another bullet point describing your impact

## SKILLS

**Category:** Technology, Tool, Framework, Language
**Programming Languages:** Python (NumPy, Pandas), R, Java, JavaScript

## PROJECTS

**[Project Name — Technology Stack](https://link-to-project.com)**  
- Description of the project and achievements
- Technical accomplishments with specific technologies

**Another Project — Technology Stack**  
- Description without link (also supported)

## COURSES

**Course Name** — Provider  
Month Year
```

## 🎯 Template Features

### Visual Hierarchy
- **Header Banner**: Colored background with white text for name, title, and contact
- **Section Headers**: Icons + bordered backgrounds for clear section separation
- **Content Styling**: Bold job titles, italic dates/locations, justified body text
- **Professional Colors**: Configurable header color with complementary text colors

### Link Handling
- **Visible Links**: Blue color + underline for immediate recognition
- **Preserved Functionality**: All hyperlinks remain clickable in PDF
- **Smart Processing**: Handles various link formats including project titles

### Dynamic Sizing
- **Content Analysis**: Calculates optimal font sizes based on total content length
- **One-Page Algorithm**: Scales fonts from 8.5pt to 6.8pt for content compression
- **Margin Adjustment**: Reduces margins for one-page mode (0.3" vs 0.75")

## 🔧 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--one-page` | Compress to single page | Multi-page |
| `--header-color` | Header background color | `white` |
| `--font-scheme` | Font styling scheme | `modern` |
| `--output-dir` | Output directory | `output` |
| `--output` | Custom filename | Auto-generated |
| `--open-pdf` | Open PDF after creation | No |

## 📊 Output Information

The tool provides detailed output including:
- **File Size**: Generated PDF size in KB
- **Mode**: One-page vs multi-page confirmation  
- **Path**: Full path to generated PDF
- **Success/Error**: Clear status messages

## 🐛 Bug Fixes & Improvements

### Recent Updates
- ✅ **Semicolon Bug**: Fixed regex patterns that added unwanted semicolons to job titles
- ✅ **Link Visibility**: Added blue color and underline to make hyperlinks clearly visible
- ✅ **Section Ordering**: Automatic reordering regardless of markdown file structure
- ✅ **Template Styling**: Professional header banner and section formatting
- ✅ **Enhanced Error Handling**: Better validation and user feedback

## 🛡 Error Handling

- **File Validation**: Checks for markdown file existence
- **Content Analysis**: Validates markdown structure
- **PDF Generation**: Comprehensive error reporting
- **Cross-Platform**: Works on macOS, Windows, and Linux

## 📁 Project Structure

```
markdown2pdf_resume_builder/
├── main.py                     # Main resume builder (template-style)
├── resume_builder_reportlab.py # Alternative ReportLab-only version
├── pyproject.toml             # Project configuration
├── example_usage_improved.sh  # Demo script with all features
├── output/                    # Generated PDFs
└── README.md                  # This file
```

## 🎉 Success Stories

✅ **Professional Output**: Generates ATS-friendly PDFs that pass applicant tracking systems  
✅ **Template Compliance**: Matches professional resume templates with colored headers  
✅ **Interactive Features**: Clickable links work perfectly in PDF viewers  
✅ **Space Optimization**: Intelligent one-page compression for concise resumes  

---

**Ready to create your professional resume?** Start with `python main.py your_resume.md --one-page` and customize from there! 🚀
