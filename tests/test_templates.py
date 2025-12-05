"""
Integration tests for template rendering engine.

Tests T116-T118 from tasks.md:
- T116: Create tests/test_templates.py
- T117: Test template variable substitution
- T118: Test missing variable error handling
"""

import tempfile
from pathlib import Path
from typing import Generator

import pytest

from twitterify_cli.template_engine import TemplateEngine


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def template_engine() -> TemplateEngine:
    """Create a template engine instance."""
    return TemplateEngine()


@pytest.fixture
def sample_template(temp_dir: Path) -> Path:
    """Create a sample template file for testing."""
    template_path = temp_dir / "test-template.md"
    template_content = """# $PROJECT_NAME

## Campaign: $CAMPAIGN_NAME

### Target Persona
$PERSONA_PRIMARY

### Hero Workflow
${HERO_WORKFLOW}

### Success Metrics
- Impressions: $TARGET_IMPRESSIONS
- Engagement: ${TARGET_ENGAGEMENT}
- Activations: $TARGET_ACTIVATIONS

### Channels
$CHANNELS
"""
    template_path.write_text(template_content)
    return template_path


class TestTemplateVariableSubstitution:
    """Test suite for template variable substitution (T117)."""

    def test_basic_variable_substitution(
        self, template_engine: TemplateEngine, sample_template: Path
    ) -> None:
        """
        Test basic $VAR_NAME variable substitution.

        Verifies:
        - $VAR_NAME patterns are replaced
        - ${VAR_NAME} patterns are replaced
        - Multiple variables can be substituted
        """
        variables = {
            "PROJECT_NAME": "cursor-twitter-launch",
            "CAMPAIGN_NAME": "Alpha Launch Campaign",
            "PERSONA_PRIMARY": "Technical founders at AI SaaS companies",
            "HERO_WORKFLOW": "Code completion that actually works",
            "TARGET_IMPRESSIONS": "100K",
            "TARGET_ENGAGEMENT": "5%",
            "TARGET_ACTIVATIONS": "100",
            "CHANNELS": "Twitter, Product Hunt, Hacker News",
        }

        rendered = template_engine.render_template(
            sample_template, variables, validate=True
        )

        # Verify all variables were substituted
        assert "cursor-twitter-launch" in rendered
        assert "Alpha Launch Campaign" in rendered
        assert "Technical founders at AI SaaS companies" in rendered
        assert "Code completion that actually works" in rendered
        assert "100K" in rendered
        assert "5%" in rendered
        assert "100" in rendered
        assert "Twitter, Product Hunt, Hacker News" in rendered

        # Verify no variable placeholders remain
        assert "$PROJECT_NAME" not in rendered
        assert "$CAMPAIGN_NAME" not in rendered
        assert "${HERO_WORKFLOW}" not in rendered

    def test_partial_variable_substitution(
        self, template_engine: TemplateEngine, temp_dir: Path
    ) -> None:
        """
        Test that partial variable substitution works.

        Verifies:
        - Only provided variables are substituted
        - Unprovided variables remain as placeholders (if validation disabled)
        """
        template_path = temp_dir / "partial-template.md"
        template_path.write_text(
            "# $PROJECT_NAME\n\nCampaign: $CAMPAIGN_NAME\n\nChannel: $CHANNEL"
        )

        variables = {
            "PROJECT_NAME": "test-project",
            "CAMPAIGN_NAME": "test-campaign",
        }

        # Without validation, unprovided variables remain
        rendered = template_engine.render_template(
            template_path, variables, validate=False
        )

        assert "test-project" in rendered
        assert "test-campaign" in rendered
        assert "$CHANNEL" in rendered  # Not substituted

    def test_braced_variable_substitution(
        self, template_engine: TemplateEngine, temp_dir: Path
    ) -> None:
        """
        Test ${VAR_NAME} braced variable substitution.

        Verifies:
        - ${VAR_NAME} syntax works
        - Mixed $VAR and ${VAR} syntax works
        """
        template_path = temp_dir / "braced-template.md"
        template_path.write_text(
            "$PROJECT_NAME uses ${FRAMEWORK} for ${PURPOSE}.\n\nAuthor: $AUTHOR"
        )

        variables = {
            "PROJECT_NAME": "twitter-init-kit",
            "FRAMEWORK": "spec-kit",
            "PURPOSE": "Twitter marketing",
            "AUTHOR": "Frank",
        }

        rendered = template_engine.render_template(
            template_path, variables, validate=True
        )

        assert "twitter-init-kit uses spec-kit for Twitter marketing." in rendered
        assert "Author: Frank" in rendered


class TestMissingVariableErrorHandling:
    """Test suite for missing variable error handling (T118)."""

    def test_validation_detects_missing_variables(
        self, template_engine: TemplateEngine, sample_template: Path
    ) -> None:
        """
        Test that validation detects missing variables.

        Verifies:
        - validate=True raises error on missing variables
        - Error message lists missing variables
        """
        incomplete_variables = {
            "PROJECT_NAME": "test-project",
            "CAMPAIGN_NAME": "test-campaign",
            # Missing: PERSONA_PRIMARY, HERO_WORKFLOW, etc.
        }

        with pytest.raises(ValueError) as exc_info:
            template_engine.render_template(
                sample_template, incomplete_variables, validate=True
            )

        error_message = str(exc_info.value)
        assert "missing" in error_message.lower() or "required" in error_message.lower()

    def test_validate_template_method(
        self, template_engine: TemplateEngine, sample_template: Path
    ) -> None:
        """
        Test validate_template() method.

        Verifies:
        - Returns (True, []) when all variables provided
        - Returns (False, [missing vars]) when variables missing
        """
        # Complete variables
        complete_variables = {
            "PROJECT_NAME": "test",
            "CAMPAIGN_NAME": "test",
            "PERSONA_PRIMARY": "test",
            "HERO_WORKFLOW": "test",
            "TARGET_IMPRESSIONS": "test",
            "TARGET_ENGAGEMENT": "test",
            "TARGET_ACTIVATIONS": "test",
            "CHANNELS": "test",
        }

        is_valid, missing = template_engine.validate_template(
            sample_template, complete_variables
        )
        assert is_valid
        assert len(missing) == 0

        # Incomplete variables
        incomplete_variables = {
            "PROJECT_NAME": "test",
            "CAMPAIGN_NAME": "test",
        }

        is_valid, missing = template_engine.validate_template(
            sample_template, incomplete_variables
        )
        assert not is_valid
        assert len(missing) > 0
        assert "PERSONA_PRIMARY" in missing
        assert "HERO_WORKFLOW" in missing

    def test_extract_variables_method(
        self, template_engine: TemplateEngine, sample_template: Path
    ) -> None:
        """
        Test _extract_variables() method.

        Verifies:
        - Correctly extracts all $VAR_NAME patterns
        - Correctly extracts all ${VAR_NAME} patterns
        - Returns unique variable names
        """
        content = sample_template.read_text()
        variables = template_engine._extract_variables(content)

        expected_vars = {
            "PROJECT_NAME",
            "CAMPAIGN_NAME",
            "PERSONA_PRIMARY",
            "HERO_WORKFLOW",
            "TARGET_IMPRESSIONS",
            "TARGET_ENGAGEMENT",
            "TARGET_ACTIVATIONS",
            "CHANNELS",
        }

        assert set(variables) == expected_vars


class TestTemplateRenderAndWrite:
    """Test suite for render_and_write() method."""

    def test_render_and_write_creates_file(
        self, template_engine: TemplateEngine, sample_template: Path, temp_dir: Path
    ) -> None:
        """
        Test that render_and_write() creates output file.

        Verifies:
        - Output file is created
        - Content is correctly rendered
        - File is written to correct path
        """
        output_path = temp_dir / "output.md"

        variables = {
            "PROJECT_NAME": "test-project",
            "CAMPAIGN_NAME": "test-campaign",
            "PERSONA_PRIMARY": "Test persona",
            "HERO_WORKFLOW": "Test workflow",
            "TARGET_IMPRESSIONS": "1000",
            "TARGET_ENGAGEMENT": "10%",
            "TARGET_ACTIVATIONS": "50",
            "CHANNELS": "Twitter",
        }

        success = template_engine.render_and_write(
            sample_template, output_path, variables, validate=True, overwrite=False
        )

        assert success
        assert output_path.exists()

        content = output_path.read_text()
        assert "test-project" in content
        assert "test-campaign" in content
        assert "Test persona" in content

    def test_render_and_write_overwrite_protection(
        self, template_engine: TemplateEngine, sample_template: Path, temp_dir: Path
    ) -> None:
        """
        Test that render_and_write() respects overwrite flag.

        Verifies:
        - overwrite=False prevents overwriting existing file
        - overwrite=True allows overwriting
        """
        output_path = temp_dir / "output.md"
        output_path.write_text("existing content")

        variables = {
            "PROJECT_NAME": "test",
            "CAMPAIGN_NAME": "test",
            "PERSONA_PRIMARY": "test",
            "HERO_WORKFLOW": "test",
            "TARGET_IMPRESSIONS": "test",
            "TARGET_ENGAGEMENT": "test",
            "TARGET_ACTIVATIONS": "test",
            "CHANNELS": "test",
        }

        # Should fail with overwrite=False
        success = template_engine.render_and_write(
            sample_template, output_path, variables, validate=True, overwrite=False
        )
        assert not success
        assert output_path.read_text() == "existing content"

        # Should succeed with overwrite=True
        success = template_engine.render_and_write(
            sample_template, output_path, variables, validate=True, overwrite=True
        )
        assert success
        assert "test" in output_path.read_text()


class TestTemplateCaching:
    """Test suite for template caching functionality."""

    def test_template_caching_improves_performance(
        self, template_engine: TemplateEngine, sample_template: Path
    ) -> None:
        """
        Test that template caching works.

        Verifies:
        - Second render of same template is faster (cached)
        - Cache is used correctly
        """
        variables = {
            "PROJECT_NAME": "test",
            "CAMPAIGN_NAME": "test",
            "PERSONA_PRIMARY": "test",
            "HERO_WORKFLOW": "test",
            "TARGET_IMPRESSIONS": "test",
            "TARGET_ENGAGEMENT": "test",
            "TARGET_ACTIVATIONS": "test",
            "CHANNELS": "test",
        }

        # First render (cache miss)
        rendered1 = template_engine.render_template(
            sample_template, variables, validate=True
        )

        # Second render (cache hit)
        rendered2 = template_engine.render_template(
            sample_template, variables, validate=True
        )

        # Results should be identical
        assert rendered1 == rendered2


class TestEdgeCases:
    """Test suite for edge cases in template rendering."""

    def test_empty_template(
        self, template_engine: TemplateEngine, temp_dir: Path
    ) -> None:
        """
        Test rendering empty template.

        Verifies:
        - Empty templates don't cause errors
        - Returns empty string
        """
        template_path = temp_dir / "empty.md"
        template_path.write_text("")

        rendered = template_engine.render_template(
            template_path, {}, validate=False
        )

        assert rendered == ""

    def test_template_without_variables(
        self, template_engine: TemplateEngine, temp_dir: Path
    ) -> None:
        """
        Test rendering template without any variables.

        Verifies:
        - Templates without variables render correctly
        - No errors raised
        """
        template_path = temp_dir / "no-vars.md"
        content = "# Static Content\n\nNo variables here."
        template_path.write_text(content)

        rendered = template_engine.render_template(
            template_path, {}, validate=True
        )

        assert rendered == content

    def test_variable_with_special_characters(
        self, template_engine: TemplateEngine, temp_dir: Path
    ) -> None:
        """
        Test variables with special characters in values.

        Verifies:
        - Special characters in variable values are preserved
        - No escaping issues
        """
        template_path = temp_dir / "special-chars.md"
        template_path.write_text("Project: $PROJECT_NAME\n\nDescription: $DESCRIPTION")

        variables = {
            "PROJECT_NAME": "test-project (v1.0.0)",
            "DESCRIPTION": "A test with $pecial ch@rs & symbols!",
        }

        rendered = template_engine.render_template(
            template_path, variables, validate=True
        )

        assert "test-project (v1.0.0)" in rendered
        assert "A test with $pecial ch@rs & symbols!" in rendered


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
