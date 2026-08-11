"""CLI integration tests."""
import pytest
from click.testing import CliRunner
from sensemaking_skills.cli import cli


@pytest.fixture
def runner():
    """Provide Click CLI test runner."""
    return CliRunner()


class TestCLIBasic:
    """Test basic CLI functionality."""

    def test_cli_version(self, runner):
        """Test --version flag."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.2.2" in result.output

    def test_cli_help(self, runner):
        """Test --help flag."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Sensemaking Skills" in result.output
        assert "analyze" in result.output
        assert "validate" in result.output
        assert "test" in result.output

    def test_analyze_help(self, runner):
        """Test analyze subcommand help."""
        result = runner.invoke(cli, ["analyze", "--help"])
        assert result.exit_code == 0
        assert "--repo" in result.output

    def test_validate_help(self, runner):
        """Test validate subcommand help."""
        result = runner.invoke(cli, ["validate", "--help"])
        assert result.exit_code == 0
        assert "--artifact" in result.output

    def test_test_help(self, runner):
        """Test test subcommand help."""
        result = runner.invoke(cli, ["test", "--help"])
        assert result.exit_code == 0
        assert "--repos" in result.output

    def test_analyze_without_repo(self, runner):
        """Test analyze without --repo returns error."""
        result = runner.invoke(cli, ["analyze"])
        assert result.exit_code != 0
        assert "Error" in result.output or "repo" in result.output.lower()

    def test_validate_without_artifact(self, runner):
        """Test validate without --artifact returns error."""
        result = runner.invoke(cli, ["validate"])
        assert result.exit_code != 0

    def test_validate_with_missing_artifact(self, runner):
        """Test validate with non-existent artifact returns error."""
        result = runner.invoke(cli, ["validate", "--artifact", "/nonexistent/path.md"])
        assert result.exit_code != 0
        assert "does not exist" in result.output.lower()
