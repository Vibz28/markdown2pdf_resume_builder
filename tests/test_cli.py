"""Tests for the CLI module."""

from click.testing import CliRunner

from markdown2pdf_resume_builder.cli import main


def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert "Convert a Markdown resume" in result.output


def test_cli_basic_usage(temp_markdown_file):
    """Test basic CLI usage."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        result = runner.invoke(main, [temp_markdown_file])
        assert result.exit_code == 0
        assert "Successfully generated" in result.output


def test_cli_one_page_flag(temp_markdown_file):
    """Test CLI with one-page flag."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        result = runner.invoke(main, [temp_markdown_file, '--one-page'])
        assert result.exit_code == 0
        assert "one-page" in result.output


def test_cli_custom_header_color(temp_markdown_file):
    """Test CLI with custom header color."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        result = runner.invoke(main, [temp_markdown_file, '--header-color', '#FF0000'])
        assert result.exit_code == 0
        assert "Successfully generated" in result.output


def test_cli_nonexistent_file():
    """Test CLI with non-existent file."""
    runner = CliRunner()
    result = runner.invoke(main, ['nonexistent.md'])
    assert result.exit_code == 2  # Click's exit code for bad parameter
