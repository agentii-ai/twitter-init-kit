---
description: Generate a custom checklist for the current feature based on user requirements.
---

## Checklist Purpose: "Unit Tests for English"

**CRITICAL CONCEPT**: Checklists are **UNIT TESTS FOR REQUIREMENTS WRITING** - they validate the quality, clarity, and completeness of requirements in a given domain.

**NOT for verification/testing**:
- ❌ NOT "Verify the button clicks correctly"
- ❌ NOT "Test error handling works"
- ❌ NOT "Confirm the API returns 200"
- ❌ NOT checking if code/implementation matches the spec

**FOR requirements quality validation**:
- ✅ "Are visual hierarchy requirements defined for all card types?" (completeness)
- ✅ "Is 'prominent display' quantified with specific sizing/positioning?" (clarity)
- ✅ "Are hover state requirements consistent across all interactive elements?" (consistency)
- ✅ "Are accessibility requirements defined for keyboard navigation?" (coverage)
- ✅ "Does the spec define what happens when logo image fails to load?" (edge cases)

**Metaphor**: If your spec is code written in English, the checklist is its unit test suite.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Execution Steps

1. **Check Prerequisites**: Run `.twitterkit/scripts/{SCRIPT}/check-prerequisites.sh --json` from repo root and parse JSON for FEATURE_DIR. Abort if plan.md is missing.

2. **Process User Input**: Extract from `$ARGUMENTS`:
   - Checklist type/focus area (e.g., "ux", "api", "security", "performance")
   - Depth level: "comprehensive" (40-60 items) or "focused" (15-25 items)
   - Explicit must-have topics
   - File name preference

3. **Load Artifacts**: Read spec.md, plan.md, and constitution.md. Note requirement IDs if present.

4. **Generate Checklist Items**: Each item must be a **question testing requirements quality**:
   - **Completeness**: "Are [X] requirements specified for [scenario]?"
   - **Clarity**: "Is [vague term] quantified with measurable criteria?"
   - **Consistency**: "Are requirements consistent between [A] and [B]?"
   - **Measurability**: "Can [requirement] be objectively measured?"
   - **Coverage**: "Are [edge cases] addressed in requirements?"
   - **Traceability**: Reference existing IDs like `[Spec §X.Y]`

   **🚫 ABSOLUTELY PROHIBITED**:
   - ❌ Any item starting with "Verify", "Test", "Confirm", "Check" + implementation behavior
   - ❌ References to code execution, user actions, system behavior
   - ❌ "Displays correctly", "works properly", "functions as expected"
   - ❌ "Click", "navigate", "render", "load", "execute"

   **✅ REQUIRED PATTERNS**:
   - ✅ "Are [requirement type] defined/specified/documented for [scenario]?"
   - ✅ "Is [vague term] quantified/clarified with specific criteria?"
   - ✅ "Are requirements consistent between [section A] and [section B]?"
   - ✅ "Does the spec define [missing aspect]?"

5. **Create Checklist File**: Write to `FEATURE_DIR/checklists/<name>.md` using template from `.twitterkit/templates/checklist-template.md`.

6. **Report**: Output full path, item count, and summary of focus areas selected.

## Example Checklist Types & Sample Items

**UX Requirements Quality:** `ux.md`
- "Are visual hierarchy requirements defined with measurable criteria?"
- "Is the number and positioning of UI elements explicitly specified?"
- "Are interaction state requirements (hover, focus, active) consistently defined?"
- "Are accessibility requirements specified for all interactive elements?"

**API Requirements Quality:** `api.md`
- "Are error response formats specified for all failure scenarios?"
- "Are rate limiting requirements quantified with specific thresholds?"
- "Are authentication requirements consistent across all endpoints?"

**Performance Requirements Quality:** `performance.md`
- "Are performance requirements quantified with specific metrics?"
- "Are performance targets defined for all critical user journeys?"
- "Can performance requirements be objectively measured?"

**Security Requirements Quality:** `security.md`
- "Are authentication requirements specified for all protected resources?"
- "Are data protection requirements defined for sensitive information?"
- "Is the threat model documented and requirements aligned to it?"

## Anti-Examples: What NOT To Do

**❌ WRONG - These test implementation, not requirements:**
```markdown
- [ ] CHK001 - Verify landing page displays 3 episode cards
- [ ] CHK002 - Test hover states work correctly on desktop
- [ ] CHK003 - Confirm logo click navigates to home page
```

**✅ CORRECT - These test requirements quality:**
```markdown
- [ ] CHK001 - Are the number and layout of featured episodes explicitly specified?
- [ ] CHK002 - Are hover state requirements consistently defined for all interactive elements?
- [ ] CHK003 - Are navigation requirements clear for all clickable brand elements?
- [ ] CHK004 - Is the selection criteria for related episodes documented?
```

## Context

$ARGUMENTS
