"""Test configuration for pytest."""

import pytest
from pathlib import Path

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "data"

@pytest.fixture
def sample_markdown():
    """Sample markdown content for testing."""
    return """# John Doe
**Senior Software Engineer**

[john.doe@email.com](mailto:john.doe@email.com) | (555) 123-4567 | [linkedin.com/in/johndoe](https://linkedin.com/in/johndoe) | San Francisco, CA

---

## EDUCATION

**University of California, Berkeley** — *B.S. Computer Science*  
Sep 2015 – May 2019 | Berkeley, CA

## WORK EXPERIENCE

**Tech Corp**  
**Senior Software Engineer**  
*Jan 2020 – present | San Francisco, CA*

- Led development of microservices architecture serving 10M+ users
- Improved system performance by 40% through optimization

## SKILLS

**Programming Languages:** Python, JavaScript, Java, Go
**Frameworks:** Django, React, Spring Boot

## PROJECTS

**[Project Alpha — Full Stack Web App](https://github.com/johndoe/alpha)**  
- Built scalable web application with React frontend and Django backend
- Deployed on AWS with CI/CD pipeline

## COURSES

**Advanced Machine Learning** — Stanford Online  
Jan 2023
"""

@pytest.fixture
def temp_markdown_file(tmp_path, sample_markdown):
    """Create a temporary markdown file for testing."""
    file_path = tmp_path / "test_resume.md"
    file_path.write_text(sample_markdown)
    return str(file_path)
