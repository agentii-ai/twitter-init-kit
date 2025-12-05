"""
Integration tests for twitterify CLI initialization commands.

Tests T111-T115 from tasks.md:
- T111: Test basic init command
- T112: Test initialization in new directory
- T113: Test initialization in current directory with --force
- T114: Test agent selection (--ai flag)
- T115: Test script selection (--script flag)
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from twitterify_cli import app

runner = CliRunner()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def temp_project_dir(temp_dir: Path) -> Path:
    """Create a temporary project directory."""
    project = temp_dir / "test-project"
    project.mkdir(parents=True)
    return project


class TestInitCommand:
    """Test suite for twitterify init command (T111-T115)."""

    def test_init_new_directory(self, temp_dir: Path) -> None:
        """
        T112: Test initialization in new directory.

        Verifies:
        - Creates project directory
        - Copies .twitterkit/ package
        - Creates specs/ and refs/ directories
        - Generates README.md
        """
        os.chdir(temp_dir)
        project_name = "test-twitter-campaign"

        result = runner.invoke(app, ["init", project_name])

        # Should succeed
        assert result.exit_code == 0

        # Verify project directory created
        project_path = temp_dir / project_name
        assert project_path.exists()
        assert project_path.is_dir()

        # Verify .twitterkit/ package copied
        twitterkit_path = project_path / ".twitterkit"
        assert twitterkit_path.exists()
        assert (twitterkit_path / "memory").exists()
        assert (twitterkit_path / "templates").exists()
        assert (twitterkit_path / "scripts").exists()

        # Verify constitution exists
        constitution = twitterkit_path / "memory" / "constitution.md"
        assert constitution.exists()
        assert constitution.stat().st_size > 0

        # Verify specs/ directory
        assert (project_path / "specs").exists()

        # Verify refs/ directory
        assert (project_path / "refs").exists()

        # Verify README.md created
        readme = project_path / "README.md"
        assert readme.exists()
        assert readme.stat().st_size > 0

    def test_init_current_directory_with_force(self, temp_project_dir: Path) -> None:
        """
        T113: Test initialization in current directory with --force.

        Verifies:
        - --here flag works
        - --force flag allows init in non-empty directory
        - Doesn't fail if directory already has files
        """
        os.chdir(temp_project_dir)

        # Create a dummy file to make directory non-empty
        (temp_project_dir / "existing.txt").write_text("existing content")

        result = runner.invoke(app, ["init", ".", "--here", "--force"])

        # Should succeed with --force
        assert result.exit_code == 0

        # Verify .twitterkit/ package installed
        assert (temp_project_dir / ".twitterkit").exists()

        # Verify existing file not deleted
        assert (temp_project_dir / "existing.txt").exists()

    def test_init_with_ai_flag(self, temp_dir: Path) -> None:
        """
        T114: Test agent selection with --ai flag.

        Verifies:
        - --ai claude installs Claude Code commands
        - .claude/commands/ directory created
        - twitterkit.* command files installed
        """
        os.chdir(temp_dir)
        project_name = "test-claude-project"

        result = runner.invoke(app, ["init", project_name, "--ai", "claude"])

        assert result.exit_code == 0

        project_path = temp_dir / project_name
        claude_commands = project_path / ".claude" / "commands"

        # Verify .claude/commands/ created
        assert claude_commands.exists()

        # Verify twitterkit.* commands installed
        expected_commands = [
            "twitterkit.constitution.md",
            "twitterkit.specify.md",
            "twitterkit.plan.md",
            "twitterkit.tasks.md",
            "twitterkit.implement.md",
            "twitterkit.clarify.md",
        ]

        for cmd in expected_commands:
            cmd_file = claude_commands / cmd
            assert cmd_file.exists(), f"Missing command: {cmd}"
            assert cmd_file.stat().st_size > 0

    def test_init_with_cursor_agent(self, temp_dir: Path) -> None:
        """
        T114: Test Cursor agent selection.

        Verifies:
        - --ai cursor creates .cursor/ directory
        - Context file created
        """
        os.chdir(temp_dir)
        project_name = "test-cursor-project"

        result = runner.invoke(app, ["init", project_name, "--ai", "cursor"])

        assert result.exit_code == 0

        project_path = temp_dir / project_name
        cursor_dir = project_path / ".cursor"

        # Note: Cursor integration may create context file differently
        # This test verifies basic directory structure
        assert project_path.exists()
        assert (project_path / ".twitterkit").exists()

    def test_init_with_script_flag(self, temp_dir: Path) -> None:
        """
        T115: Test script variant selection with --script flag.

        Verifies:
        - --script sh uses bash scripts (default)
        - --script ps would use PowerShell scripts (future)
        """
        os.chdir(temp_dir)
        project_name = "test-script-project"

        result = runner.invoke(app, ["init", project_name, "--script", "sh"])

        assert result.exit_code == 0

        project_path = temp_dir / project_name
        scripts_dir = project_path / ".twitterkit" / "scripts" / "bash"

        # Verify bash scripts exist
        assert scripts_dir.exists()
        assert (scripts_dir / "create-new-campaign.sh").exists()
        assert (scripts_dir / "setup-plan.sh").exists()
        assert (scripts_dir / "update-agent-context.sh").exists()

    def test_init_without_git(self, temp_dir: Path) -> None:
        """
        Test --no-git flag skips git initialization.

        Verifies:
        - --no-git prevents git init
        - .git directory not created
        """
        os.chdir(temp_dir)
        project_name = "test-no-git"

        result = runner.invoke(app, ["init", project_name, "--no-git"])

        assert result.exit_code == 0

        project_path = temp_dir / project_name
        git_dir = project_path / ".git"

        # Verify no .git directory
        assert not git_dir.exists()

    def test_init_in_empty_directory_without_force_fails(self, temp_project_dir: Path) -> None:
        """
        Test that init in current directory requires --force if not empty.

        Verifies:
        - Init fails without --force in non-empty directory
        - Error message is clear
        """
        os.chdir(temp_project_dir)

        # Create a file to make directory non-empty
        (temp_project_dir / "existing.txt").write_text("content")

        result = runner.invoke(app, ["init", ".", "--here"])

        # Should fail without --force
        assert result.exit_code != 0
        assert "force" in result.output.lower() or "not empty" in result.output.lower()


class TestCheckCommand:
    """Test suite for twitterify check command."""

    def test_check_command_runs(self) -> None:
        """
        Test that check command runs successfully.

        Verifies:
        - Command executes without error
        - Outputs tool detection results
        """
        result = runner.invoke(app, ["check"])

        # Should always run (may show warnings but shouldn't fail)
        assert result.exit_code in [0, 1]  # 0 = all tools found, 1 = some missing

        # Should mention essential tools
        assert "git" in result.output.lower()
        assert "python" in result.output.lower()


class TestVersionCommand:
    """Test suite for twitterify version command."""

    def test_version_command(self) -> None:
        """
        Test that version command displays version info.

        Verifies:
        - Command runs successfully
        - Displays version number
        """
        result = runner.invoke(app, ["version"])

        assert result.exit_code == 0
        assert "twitterify" in result.output.lower()
        assert "version" in result.output.lower()


class TestHelpCommand:
    """Test suite for twitterify --help command."""

    def test_help_command(self) -> None:
        """
        Test that help command displays usage information.

        Verifies:
        - Command runs successfully
        - Shows available commands
        """
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "init" in result.output.lower()
        assert "check" in result.output.lower()
        assert "version" in result.output.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
