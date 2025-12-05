# Contributing to Twitter-Init-Kit

Thank you for your interest in contributing to twitter-init-kit! This document provides guidelines for contributing to the project.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Submitting Changes](#submitting-changes)
6. [Creating Kit Variants](#creating-kit-variants)

---

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) before contributing.

---

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:

- **Clear title and description**
- **Steps to reproduce** the bug
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, twitterify version)
- **Screenshots or logs** if applicable

**Example**:
```
Title: twitterify init fails with --ai claude on macOS

Description:
When running `twitterify init test-project --ai claude`, the command fails with:
FileNotFoundError: .claude/commands/ directory not found

Steps to reproduce:
1. Install twitterify via uv: `uv tool install twitterify-cli`
2. Run: `twitterify init test-project --ai claude`
3. Error occurs

Expected: .claude/commands/ directory should be created
Actual: Command fails with FileNotFoundError

Environment:
- macOS 14.1
- Python 3.11.5
- twitterify 0.1.0
```

### Suggesting Enhancements

Have an idea for a new feature or improvement? Open an issue with:

- **Clear use case**: What problem does this solve?
- **Proposed solution**: How would it work?
- **Alternatives considered**: Other approaches you've thought about
- **Impact**: Who would benefit from this?

### Improving Documentation

Documentation improvements are always welcome:

- Fix typos or grammatical errors
- Clarify confusing instructions
- Add examples or use cases
- Improve quickstart guide
- Add case studies to refs/

### Adding Case Studies

Help us build evidence-based templates by contributing case studies:

1. Research a successful AI SaaS Twitter strategy (2023-2025)
2. Document key metrics, tactics, and principles
3. Add to `refs/0_overview.md` or create `refs/5_more/[company]-case-study.md`
4. Cite sources and provide screenshots/links
5. Extract actionable principles

**Example format**:
```markdown
## [Company Name] - [Strategy Focus]

**Background**: [Brief company description]

**Twitter Strategy**:
- [Key tactic 1]
- [Key tactic 2]
- [Key tactic 3]

**Metrics**:
- Followers: [count]
- Engagement rate: [percentage]
- Activation: [percentage]

**Principles**:
1. [Principle 1]: [Evidence]
2. [Principle 2]: [Evidence]

**Sources**: [Links to public sources]
```

### Creating Kit Variants

The most impactful contribution is creating new kit variants (pm-kit, pd-kit, sales-kit):

1. Follow the [Kit Variant Creation Guide](./refs/6_variant_creation_guide.md)
2. Share your progress in the spec-kit community
3. Document your adaptation process
4. Submit your variant as a sister project

---

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- `uv` or `pip` or `pipx`

### Local Installation

```bash
# Clone repository
git clone https://github.com/yourusername/twitter-init-kit.git
cd twitter-init-kit

# Install development dependencies
uv sync

# Or create virtual environment manually
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_init.py

# Run with coverage
pytest --cov=twitterify_cli tests/

# Run with verbose output
pytest -v
```

### Running Linters

```bash
# Run ruff (linter)
ruff check .

# Fix auto-fixable issues
ruff check . --fix

# Run mypy (type checker)
mypy src/twitterify_cli

# Run black (formatter)
black src/ tests/

# Check formatting without changes
black src/ tests/ --check
```

### Testing CLI Locally

```bash
# Install CLI locally
uv tool install -e .

# Test commands
twitterify --help
twitterify check
twitterify init test-project --ai claude

# Uninstall
uv tool uninstall twitterify-cli
```

---

## Coding Standards

### Python Style Guide

Follow **PEP 8** style guidelines:

- Use **4 spaces** for indentation (not tabs)
- Maximum line length: **88 characters** (Black default)
- Use **snake_case** for functions and variables
- Use **PascalCase** for classes
- Add **type hints** to all functions
- Add **docstrings** to all public functions

**Good Example**:
```python
def render_template(
    self, template_path: Path, variables: Dict[str, str], validate: bool = True
) -> str:
    """
    Render template with variable substitution.

    Args:
        template_path: Path to template file
        variables: Dictionary of variable names to values
        validate: Whether to validate all variables are provided

    Returns:
        Rendered template content

    Raises:
        FileNotFoundError: If template file doesn't exist
        ValueError: If required variables are missing (when validate=True)
    """
    # Implementation...
```

### Markdown Style Guide

- Use **ATX-style headings** (`# Heading` not `Heading\n=======`)
- Add **blank lines** before and after headings
- Use **fenced code blocks** with language specified
- Keep lines under **120 characters** (soft limit)
- Use **consistent list formatting** (either `-` or `*`, not mixed)

### Git Commit Messages

Follow **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic changes)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(cli): add --debug flag for verbose output

Add optional --debug flag to all CLI commands to enable verbose
logging for troubleshooting.

Closes #42

---

fix(templates): handle missing variables gracefully

Template engine now provides clear error messages when required
variables are missing instead of silently failing.

Fixes #37

---

docs(quickstart): add troubleshooting section

Add common issues and solutions to quickstart guide based on
beta user feedback.
```

### Testing Standards

- Write tests for **all new features**
- Maintain **80%+ code coverage**
- Use **descriptive test names** (`test_init_creates_twitterkit_directory`)
- Use **fixtures** for common setup
- Test **edge cases** and error conditions

**Test Structure**:
```python
def test_feature_name_should_do_something() -> None:
    """
    Test that feature does something specific.

    Verifies:
    - Condition 1 is met
    - Condition 2 is met
    - Edge case is handled
    """
    # Arrange
    input_data = create_test_data()

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected_value
    assert condition_is_met()
```

---

## Submitting Changes

### Pull Request Process

1. **Fork the repository** and create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following coding standards

3. **Write tests** for your changes

4. **Run tests and linters** to ensure everything passes
   ```bash
   pytest
   ruff check .
   mypy src/
   black src/ tests/ --check
   ```

5. **Commit your changes** with descriptive commit messages

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request** on GitHub with:
   - **Clear title** describing the change
   - **Description** explaining what and why
   - **Link to related issues** (Fixes #123, Closes #456)
   - **Testing notes** explaining how you tested
   - **Screenshots** if UI/output changes

### Pull Request Template

```markdown
## Description
[What does this PR do? Why is this change needed?]

## Related Issues
Fixes #[issue number]

## Changes Made
- [Change 1]
- [Change 2]
- [Change 3]

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Tested manually (describe steps)
- [ ] Linters pass (ruff, mypy, black)

## Documentation
- [ ] README updated (if needed)
- [ ] Quickstart guide updated (if needed)
- [ ] Code comments added (if needed)
- [ ] Type hints added

## AI Assistance Disclosure
[If you used AI assistance (Copilot, ChatGPT, Claude, etc.), disclose it here]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Commits follow Conventional Commits format
- [ ] No breaking changes (or documented if necessary)
- [ ] Self-reviewed the code
```

### Review Process

- **Maintainers will review** your PR within 3-5 business days
- **Address feedback** by pushing new commits to your branch
- **Be patient and respectful** during the review process
- **PR will be merged** once approved by a maintainer

---

## AI Contributions

> [!IMPORTANT]
>
> If you are using **any kind of AI assistance** to contribute to twitter-init-kit,
> it must be disclosed in the pull request or issue.

We welcome and encourage the use of AI tools! Many contributions have been enhanced with AI assistance. However, **you must disclose AI use** in PRs/issues, along with the extent (e.g., documentation vs. code generation).

If your PR responses or comments are AI-generated, disclose that as well.

**Example disclosures**:
- "This PR was written primarily by GitHub Copilot."
- "I consulted ChatGPT to understand the codebase but the solution was fully authored manually."

**Trivial exceptions**: Small typo fixes don't need disclosure.

### What We're Looking For

AI-assisted contributions should include:

- **Clear disclosure of AI use**
- **Human understanding and testing** - You've tested changes and understand them
- **Clear rationale** - You can explain why the change is needed
- **Concrete evidence** - Test cases or examples demonstrating improvement
- **Your own analysis** - Your thoughts on the developer experience

### What We'll Close

We'll close contributions that appear to be:

- Untested changes submitted without verification
- Generic suggestions not addressing specific needs
- Bulk submissions without human review

---

## Creating Kit Variants

Creating a new kit variant (pm-kit, pd-kit, sales-kit) is a major contribution! Follow these steps:

### 1. Research & Planning (Week 1)

- Define your domain (product management, design, sales, etc.)
- Identify target users
- Map spec-kit concepts to your domain
- Collect 5-10 case studies as evidence base

**Deliverable**: `refs/domain_mapping.md` and `refs/0_overview.md`

### 2. Fork & Rename (Week 1)

```bash
# Fork twitter-init-kit
git clone https://github.com/yourusername/twitter-init-kit.git yourkit
cd yourkit

# Rename package directory
mv .twitterkit .yourkit

# Update pyproject.toml
# Change: name = "twitterify-cli" → name = "yourkit-cli"
# Change: twitterify = "twitterify_cli:main" → yourcommand = "yourkit_cli:main"

# Rename Python package
mv src/twitterify_cli src/yourkit_cli

# Search and replace
find . -type f -exec sed -i 's/twitterify/yourcommand/g' {} +
find . -type f -exec sed -i 's/twitterkit/yourkit/g' {} +
```

### 3. Adapt Templates (Week 2-3)

Transform each template for your domain:

- `constitution.md` - Replace Twitter principles with domain principles
- `spec-template.md` - Replace campaign objectives with domain goals
- `plan-template.md` - Replace growth plan with domain execution plan
- `tasks-template.md` - Replace marketing tasks with domain tasks

**See**: [refs/6_variant_creation_guide.md](./refs/6_variant_creation_guide.md) for detailed instructions

### 4. Test & Document (Week 4)

- Create integration tests
- Test multi-kit coexistence with spec-kit and twitter-kit
- Write quickstart guide for your kit
- Update README

### 5. Share with Community

- Announce in spec-kit Discord/Slack
- Tweet about your kit variant
- Submit to awesome-spec-kit list
- Help others create variants

---

## Questions?

- **General questions**: Open a GitHub Discussion
- **Bug reports**: Open a GitHub Issue
- **Security issues**: Email frank@agentii.ai
- **Kit variant help**: Tag @yourhandle on Twitter

---

Thank you for contributing to twitter-init-kit! Your contributions help the entire community build better Twitter marketing strategies.
