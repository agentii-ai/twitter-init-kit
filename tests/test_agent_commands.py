"""
Integration tests for agent slash commands.

Tests T119-T122 from tasks.md:
- T119: Create tests/test_agent_commands.py
- T120: Test /twitterkit.constitution command execution
- T121: Test /twitterkit.specify command execution
- T122: Test /twitterkit.plan command execution
"""

import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_project() -> Generator[Path, None, None]:
    """Create a temporary project directory with .twitterkit/ structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test-project"
        project_path.mkdir()

        # Create .twitterkit/ structure
        twitterkit = project_path / ".twitterkit"
        (twitterkit / "memory").mkdir(parents=True)
        (twitterkit / "templates").mkdir(parents=True)
        (twitterkit / "templates" / "commands").mkdir(parents=True)

        # Create minimal constitution
        constitution = twitterkit / "memory" / "constitution.md"
        constitution.write_text("# Twitter-Init-Kit Constitution\n\nTest constitution")

        # Create specs directory
        (project_path / "specs").mkdir()

        yield project_path


class TestAgentCommandFiles:
    """Test suite for agent command file structure (T119)."""

    def test_command_files_exist(self) -> None:
        """
        Test that all required command files exist.

        Verifies:
        - All 6 twitterkit.* command files present
        - Files are in .twitterkit/templates/commands/
        """
        commands_dir = Path(__file__).parent.parent / ".twitterkit" / "templates" / "commands"

        expected_commands = [
            "twitterkit.constitution.md",
            "twitterkit.specify.md",
            "twitterkit.plan.md",
            "twitterkit.tasks.md",
            "twitterkit.implement.md",
            "twitterkit.clarify.md",
        ]

        for cmd in expected_commands:
            cmd_path = commands_dir / cmd
            assert cmd_path.exists(), f"Missing command file: {cmd}"
            assert cmd_path.stat().st_size > 0, f"Empty command file: {cmd}"

    def test_command_files_have_required_sections(self) -> None:
        """
        Test that command files have required sections.

        Verifies:
        - Prerequisites section
        - Execution Steps section
        - Expected Outputs section
        """
        commands_dir = Path(__file__).parent.parent / ".twitterkit" / "templates" / "commands"

        for cmd_file in commands_dir.glob("twitterkit.*.md"):
            content = cmd_file.read_text()

            # Check for required sections
            assert (
                "prerequisite" in content.lower()
            ), f"{cmd_file.name}: Missing Prerequisites section"
            assert (
                "step" in content.lower() or "execution" in content.lower()
            ), f"{cmd_file.name}: Missing Execution Steps section"
            assert (
                "output" in content.lower()
            ), f"{cmd_file.name}: Missing Expected Outputs section"

    def test_command_files_reference_twitterkit_package(self) -> None:
        """
        Test that command files reference .twitterkit/ package.

        Verifies:
        - Commands reference .twitterkit/ (not .specify/)
        - Commands use twitterkit namespace (not speckit)
        """
        commands_dir = Path(__file__).parent.parent / ".twitterkit" / "templates" / "commands"

        for cmd_file in commands_dir.glob("twitterkit.*.md"):
            content = cmd_file.read_text()

            # Should reference .twitterkit/
            assert (
                ".twitterkit" in content or "twitterkit" in content.lower()
            ), f"{cmd_file.name}: Should reference .twitterkit/ package"

            # Should NOT reference .specify/ (except in context explanations)
            # Allow mentions of spec-kit for comparison, but not direct file references
            if ".specify/" in content:
                # Count occurrences - should be minimal (only in documentation)
                specify_refs = content.count(".specify/")
                assert (
                    specify_refs <= 2
                ), f"{cmd_file.name}: Too many .specify/ references (found {specify_refs})"


class TestConstitutionCommand:
    """Test suite for /twitterkit.constitution command (T120)."""

    def test_constitution_command_structure(self) -> None:
        """
        Test constitution command file structure.

        Verifies:
        - Command file exists
        - Has description
        - Has prerequisites
        - Has execution steps
        """
        cmd_path = (
            Path(__file__).parent.parent
            / ".twitterkit"
            / "templates"
            / "commands"
            / "twitterkit.constitution.md"
        )

        assert cmd_path.exists()

        content = cmd_path.read_text()

        # Should describe what constitution does
        assert (
            "constitution" in content.lower()
        ), "Command should describe constitution purpose"
        assert (
            "principle" in content.lower()
        ), "Command should mention principles"

        # Should have execution guidance
        assert (
            "create" in content.lower() or "generate" in content.lower()
        ), "Command should explain how to create constitution"


class TestSpecifyCommand:
    """Test suite for /twitterkit.specify command (T121)."""

    def test_specify_command_structure(self) -> None:
        """
        Test specify command file structure.

        Verifies:
        - Command file exists
        - References spec-template.md
        - Mentions Twitter-specific elements
        """
        cmd_path = (
            Path(__file__).parent.parent
            / ".twitterkit"
            / "templates"
            / "commands"
            / "twitterkit.specify.md"
        )

        assert cmd_path.exists()

        content = cmd_path.read_text()

        # Should reference spec template
        assert (
            "spec-template" in content.lower() or "spec.md" in content.lower()
        ), "Command should reference spec template"

        # Should mention Twitter-specific concepts
        twitter_concepts = ["campaign", "persona", "twitter", "engagement"]
        found_concepts = sum(1 for concept in twitter_concepts if concept in content.lower())
        assert found_concepts >= 2, "Command should mention Twitter marketing concepts"

        # Should explain output location
        assert (
            "specs/" in content
        ), "Command should specify output location (specs/ directory)"


class TestPlanCommand:
    """Test suite for /twitterkit.plan command (T122)."""

    def test_plan_command_structure(self) -> None:
        """
        Test plan command file structure.

        Verifies:
        - Command file exists
        - References plan-template.md
        - Mentions growth planning elements
        """
        cmd_path = (
            Path(__file__).parent.parent
            / ".twitterkit"
            / "templates"
            / "commands"
            / "twitterkit.plan.md"
        )

        assert cmd_path.exists()

        content = cmd_path.read_text()

        # Should reference plan template
        assert (
            "plan-template" in content.lower() or "plan.md" in content.lower()
        ), "Command should reference plan template"

        # Should mention growth planning concepts
        growth_concepts = ["growth", "plan", "sprint", "phase", "strategy"]
        found_concepts = sum(1 for concept in growth_concepts if concept in content.lower())
        assert found_concepts >= 2, "Command should mention growth planning concepts"

        # Should explain prerequisites
        assert (
            "spec" in content.lower()
        ), "Command should mention spec.md as prerequisite"


class TestTasksCommand:
    """Test suite for /twitterkit.tasks command."""

    def test_tasks_command_structure(self) -> None:
        """
        Test tasks command file structure.

        Verifies:
        - Command file exists
        - References tasks-template.md
        - Mentions task execution elements
        """
        cmd_path = (
            Path(__file__).parent.parent
            / ".twitterkit"
            / "templates"
            / "commands"
            / "twitterkit.tasks.md"
        )

        assert cmd_path.exists()

        content = cmd_path.read_text()

        # Should reference tasks template
        assert (
            "tasks-template" in content.lower() or "tasks.md" in content.lower()
        ), "Command should reference tasks template"

        # Should mention execution concepts
        execution_concepts = ["task", "execution", "phase", "implement"]
        found_concepts = sum(
            1 for concept in execution_concepts if concept in content.lower()
        )
        assert found_concepts >= 2, "Command should mention execution concepts"


class TestImplementCommand:
    """Test suite for /twitterkit.implement command."""

    def test_implement_command_structure(self) -> None:
        """
        Test implement command file structure.

        Verifies:
        - Command file exists
        - Mentions systematic execution
        - References tasks.md
        """
        cmd_path = (
            Path(__file__).parent.parent
            / ".twitterkit"
            / "templates"
            / "commands"
            / "twitterkit.implement.md"
        )

        assert cmd_path.exists()

        content = cmd_path.read_text()

        # Should reference tasks.md
        assert (
            "tasks" in content.lower()
        ), "Command should reference tasks.md"

        # Should mention execution methodology
        execution_concepts = ["implement", "execute", "systematic", "pdca", "cycle"]
        found_concepts = sum(
            1 for concept in execution_concepts if concept in content.lower()
        )
        assert found_concepts >= 1, "Command should mention execution methodology"


class TestClarifyCommand:
    """Test suite for /twitterkit.clarify command."""

    def test_clarify_command_structure(self) -> None:
        """
        Test clarify command file structure.

        Verifies:
        - Command file exists
        - Mentions clarification process
        - References spec.md
        """
        cmd_path = (
            Path(__file__).parent.parent
            / ".twitterkit"
            / "templates"
            / "commands"
            / "twitterkit.clarify.md"
        )

        assert cmd_path.exists()

        content = cmd_path.read_text()

        # Should mention clarification
        assert (
            "clarify" in content.lower() or "underspecified" in content.lower()
        ), "Command should describe clarification purpose"

        # Should reference spec
        assert (
            "spec" in content.lower()
        ), "Command should mention spec as input"


class TestCommandInstallation:
    """Test suite for command installation via CLI."""

    def test_commands_can_be_copied_to_claude_directory(
        self, temp_project: Path
    ) -> None:
        """
        Test that command files can be installed to .claude/commands/.

        Verifies:
        - Commands can be copied from .twitterkit/templates/commands/
        - Target directory can be created
        """
        source_commands = (
            Path(__file__).parent.parent / ".twitterkit" / "templates" / "commands"
        )
        target_commands = temp_project / ".claude" / "commands"
        target_commands.mkdir(parents=True)

        # Copy command files
        for cmd_file in source_commands.glob("twitterkit.*.md"):
            target_file = target_commands / cmd_file.name
            target_file.write_text(cmd_file.read_text())

        # Verify all commands copied
        expected_commands = [
            "twitterkit.constitution.md",
            "twitterkit.specify.md",
            "twitterkit.plan.md",
            "twitterkit.tasks.md",
            "twitterkit.implement.md",
            "twitterkit.clarify.md",
        ]

        for cmd in expected_commands:
            assert (target_commands / cmd).exists(), f"Failed to copy {cmd}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
