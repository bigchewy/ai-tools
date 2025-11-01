# Claude Context: AI Tools Project

## ⚠️ CRITICAL: Command Creation Protocol

**When creating new commands, ALWAYS use `/create-command` from the dev-toolkit plugin.**

This is the standardized, canonical way to create commands in this repository. It ensures consistency, applies all proven patterns, and maintains quality standards.

**DO NOT manually create command files unless the user explicitly requests it.**

See "Development Workflow → CRITICAL: Creating New Commands" section below for complete documentation.

---

## Project Overview

This is a monorepo containing Claude Code plugins for productivity, self-awareness, and task management. The project follows the Claude Code plugin marketplace structure and contains multiple plugins that work with Claude Code's command and agent systems.

**Key Development Tool:** The `dev-toolkit` plugin provides `/create-command` for standardized command creation.

## Current Plugins

1. **dev-toolkit**: Development tools for creating commands and managing plugins (CRITICAL: Use this for creating new commands)
2. **daily-signal**: Morning and evening check-in rituals with expert psychologist personas
3. **asana-toolkit**: Asana task management with data collection and task creation agents
4. **weekly-reviews**: Weekly review automation with Google Docs integration

## Project Architecture

### Plugin Structure
Each plugin follows this structure:
```
plugin-name/
├── commands/           # Slash commands (.md files)
├── agents/            # Specialized agents (.md files)
├── resources/         # Templates and supporting files
└── plugin.json        # Plugin metadata
```

### Marketplace Structure
- `.claude-plugin/marketplace.json` - Defines the marketplace and all available plugins
- Plugins are referenced by ID (e.g., `eric-productivity-tools`)
- Each plugin entry specifies location, name, description, and entry point

## Dev-Toolkit: The Command Creation System

The `dev-toolkit` plugin is the **mandatory tool for creating new commands** in this repository. It provides standardized, validated, pattern-based command generation.

### Core Components

1. **`/create-command`** - Interactive command generator
   - Located: `dev-toolkit/commands/create-command.md`
   - Guides you through 8-step workflow
   - Validates plugin and command names
   - Generates files following all proven patterns
   - Prevents common errors through validation

2. **`TEMPLATES.md`** - Template library with 4 command types
   - Located: `dev-toolkit/resources/TEMPLATES.md`
   - Simple Single-Step Command
   - Multi-Step Interactive Command (with state management)
   - Command with MCP Integration
   - Command with External Resource References
   - Each template includes when to use it, structure, and examples

3. **`create_command_script.py`** - Validation utility
   - Located: `dev-toolkit/resources/create_command_script.py`
   - Validates plugin existence
   - Enforces kebab-case naming
   - Detects file conflicts
   - Creates directories safely
   - Returns JSON for programmatic use

### Design Philosophy

The dev-toolkit enforces:
1. **Pattern-Based Generation** - All 7 proven patterns from daily-signal automatically applied
2. **Validation First** - Check everything before file operations
3. **Interactive Guidance** - One question at a time, clear examples
4. **Extensibility** - Easy to add new templates and validation rules

### When to Use Each Template

**Simple Single-Step:** One clear task, no user interaction
- Example: Generate a daily summary

**Multi-Step Interactive:** Sequential user input, information gathering
- Example: daily-signal morning check-in
- Implements: State tracking, FORBIDDEN/REQUIRED rules

**MCP Integration:** External service calls (Asana, Google Docs)
- Example: Creating Asana tasks
- Implements: Fully qualified names, error handling, workspace discovery

**External Resource References:** Loading files, templates, configuration
- Example: Loading advisor profiles
- Implements: Progressive disclosure, file cascade, one-level-deep references

### Quality Guarantees

Every command created with `/create-command`:
- ✓ Under 500 lines
- ✓ Follows kebab-case naming
- ✓ Implements relevant patterns
- ✓ Includes error handling
- ✓ Has proper directory structure
- ✓ Validated before creation
- ✓ Matches template best practices

## Working Patterns from daily-signal Plugin

The daily-signal plugin demonstrates production-ready patterns. Use these as templates.

### 1. Progressive Disclosure (Information Architecture)

**What it looks like:**
- Main command: `daily-signal/commands/morning-signal.md` (200 lines)
- References 6 advisor files: `daily-signal/resources/v_diana_chapman.md` (~185 lines each)
- Selection guide: `daily-signal/resources/CLAUDE.md` (199 lines)
- Exactly one level deep - no nested references

**Explicit file references in morning-signal.md:8-9:**
```markdown
1. Read `daily-signal/resources/v_diana_chapman.md`
2. Read `daily-signal/resources/CLAUDE.md` for selection criteria
```

### 2. State Management Pattern

**Problem solved:** Prevents Claude from racing ahead or batching multiple questions.

**Implementation (morning-signal.md:24-62):**
```markdown
### CRITICAL EXECUTION CONSTRAINTS
**CONVERSATION STATE TRACKING**: Track which section you're in (1-9 total sections)
**CURRENT SECTION**: [Triage | Breathing | Head | Heart | Body | Spirit | Integration | Score | Practices]

### ENFORCEMENT RULES
- **FORBIDDEN**: Asking multiple questions in one response
- **FORBIDDEN**: Moving to next section without user response
- **REQUIRED**: Each response must end with: "Please share your thoughts, and I'll continue with the next section."
```

### 3. File Cascade Pattern (Configuration Fallback)

**Problem solved:** Handle optional user profiles gracefully.

**Implementation (morning-signal.md:116-120):**
```markdown
1. `virtual_board/profile/main_profile.md` (if using Virtual Board system)
2. `profile/main_profile.md` (vault root)
3. `daily-signal-profile.md` (vault root)
4. If none exist, use `daily-signal/resources/profile-template.md`
```

### 4. Explicit Error Handling

**Implementation (morning-signal.md:197-199):**
```markdown
### Error Handling
- If workspace not found: Use mcp__asana__asana_list_workspaces first
- If task creation fails: Note in check-in file but don't block session completion
- Always document what was attempted for reproducibility
```

### 5. MCP Tool Integration Pattern

**Implementation (morning-signal.md:185-190):**
```markdown
Use mcp__asana__asana_create_task with:
- workspace: Use the user's default workspace
- assignee: "me"
- name: "Micro-Practices for Today - [YYYY-MM-DD]"
- notes: The formatted description above
- due_on: Today's date
```

**Key pattern:** Fully qualified MCP names (`mcp__server__tool`), explicit parameters, documented error paths.

### 6. Reusable Resource Template

**Advisor persona files** (all 6 follow identical structure):
```markdown
# v_[Name] – [Role Title]

## 1. Archetype & Voice
## 2. Domains of Mastery (table)
## 3. Challenge Prompts
## 4. Vibe Check
## 5. Favorite Frameworks & Tools
## 6. Blind Spots They Highlight
## 7. Engagement Template
## 8. Example Dialogue Snippet
## 9. Synergies with Other Advisors
## 10. When Not to Use [Name]
## 11. [Domain-specific frameworks]
## 16. Morning Check-In Protocol
```

**Location:** See `daily-signal/resources/v_diana_chapman.md` for reference implementation.

### 7. Output File Conventions

**From README.md:42-43:**
```markdown
Check-ins are saved to:
- Morning: `domains/check_ins/morning/YYYY-MM-DD.md`
- Evening: `domains/check_ins/evening/YYYY-MM-DD.md`
```

**Pattern:** Domain-based organization, ISO date format, predictable paths for automation.

---

## Plugin Development Patterns

### Commands
- Stored as markdown files in `commands/` directory
- Use descriptive names (e.g., `morning-signal.md`)
- Include detailed prompts for Claude to follow
- Reference external resources using explicit paths (see Pattern #1 above)
- Implement state management for multi-step flows (see Pattern #2 above)

### Agents
- Stored as markdown files in `agents/` directory
- Define specialized roles with specific expertise
- Include clear instructions for data collection, analysis, or task creation
- May require MCP server integrations (see Pattern #5 above)

### Resources
- Templates, profiles, and reference materials
- Support both commands and agents
- Should follow consistent structure (see Pattern #6 above)
- Include error handling documentation (see Pattern #4 above)

## Skill Development Best Practices

### Core Principles

**Conciseness**: Keep skill files under 500 lines. Only include context Claude doesn't already possess. Challenge each piece of information—does it justify its token cost?

**Appropriate Freedom Levels**: Match specificity to task fragility:
- **High freedom** (text instructions): Multiple valid approaches exist
- **Medium freedom** (pseudocode): Preferred patterns with some variation
- **Low freedom** (specific scripts): Fragile operations requiring exact sequences

**Multi-Model Testing**: Verify skills work across Haiku, Sonnet, and Opus since effectiveness depends on the underlying model.

### Naming & Metadata

**Naming Conventions**: Use gerund form (verb + -ing) for clarity:
- Good: `processing-pdfs`, `analyzing-spreadsheets`, `creating-skills`
- Avoid: `helper`, `utils`, vague terms

**YAML Frontmatter Requirements** (for skills):
- `name`: Max 64 characters, lowercase letters/numbers/hyphens only
- `description`: Max 1024 characters, non-empty, no XML tags
- Write descriptions in third person
- Include what the skill does AND when to use it
- Be specific with key terms for proper skill discovery

### Information Architecture

**Progressive Disclosure**: Structure content like a table of contents:
- Main skill file provides overview
- Reference files load only when needed
- Keep references one level deep from main skill file

**Recommended Patterns**:
1. **High-level guide with references**: Basic content in main file, detailed materials in separate files (FORMS.md, REFERENCE.md, EXAMPLES.md)
2. **Domain-specific organization**: Separate reference files by domain (e.g., finance.md, sales.md) so Claude loads only relevant content
3. **Conditional details**: Show basics, link to advanced content conditionally

**For longer reference files** (100+ lines): Include table of contents so Claude sees full scope even during partial reads.

### Code & Scripts

**Error Handling**: Handle error conditions explicitly rather than punting to Claude. Document all constants with justifications.

**Utility Scripts**: Provide pre-made scripts for:
- More reliability than generated code
- Token savings
- Consistency across uses

Make clear whether Claude should execute or read scripts as reference.

**Validation Loops**: Use "plan-validate-execute" pattern:
- Create structured intermediate outputs
- Validate with scripts before applying changes
- Catches errors early and prevents irreversible mistakes

### Content Guidelines

**Avoid Time-Sensitive Information**: Use "old patterns" sections with details tags instead of conditional date statements.

**Consistent Terminology**: Choose one term and use it throughout (e.g., always "API endpoint," never mix with "URL").

**Template Patterns**: Provide strict templates for critical output formats; flexible guidance where adaptation helps.

**Examples Pattern**: Include concrete input/output pairs demonstrating desired style and detail level.

**Workflow Checklists**: For complex multi-step tasks, provide copyable checklists Claude can check off during progress.

### Testing & Iteration

**Build Evaluations First**: Create evaluations BEFORE extensive documentation. This ensures solving real problems, not imagined ones.

**Iterative Development with Claude**:
1. Complete task without skill; identify reusable patterns
2. Create the skill based on those patterns
3. Test with a fresh Claude session on similar tasks
4. Observe behavior for gaps
5. Refine based on observations

### Anti-Patterns to Avoid

- Windows-style paths (use forward slashes only)
- Offering too many approach options without a clear default
- Deeply nested file references (Claude may only partially read)
- Magic numbers without justification
- Assuming tools or packages are pre-installed
- Time-sensitive conditions in documentation

### Quality Checklist

**Core Quality**:
- [ ] Specific descriptions with key terms
- [ ] Under 500 lines
- [ ] One-level-deep references
- [ ] Consistent terminology
- [ ] Concrete examples

**Code & Scripts**:
- [ ] Explicit error handling
- [ ] Pre-made utility scripts where appropriate
- [ ] Validation steps
- [ ] Justified constants
- [ ] Clear documentation

**Testing**:
- [ ] Three+ evaluations created
- [ ] Tested with target models
- [ ] Real usage scenarios
- [ ] Feedback incorporated

## Development Workflow

### CRITICAL: Creating New Commands

**ALWAYS use `/create-command` from the dev-toolkit plugin when creating new commands.** This ensures consistency and adherence to all seven proven patterns.

**DO NOT manually create command files unless explicitly requested by the user.**

#### Why Use `/create-command`?

The dev-toolkit provides:
1. **Validated command structure** - Ensures kebab-case naming and file placement
2. **Pattern-based templates** - All 7 patterns from daily-signal automatically applied
3. **Template selection guidance** - Choose from 4 proven command types
4. **Automatic validation** - Checks for conflicts before creating files
5. **Consistency enforcement** - Every command follows the same quality standards

#### The Four Command Templates

Located in `dev-toolkit/resources/TEMPLATES.md`:

1. **Simple Single-Step Command**
   - Use when: One clear task, no user interaction needed
   - Example: Generate a daily summary

2. **Multi-Step Interactive Command** (Pattern #2: State Management)
   - Use when: Gathering information from user sequentially
   - Example: daily-signal morning check-in with 9 steps
   - Implements: FORBIDDEN/REQUIRED rules, explicit state tracking

3. **Command with MCP Integration** (Pattern #5: MCP Integration)
   - Use when: Interacting with external services (Asana, Google Docs)
   - Example: daily-signal creating Asana tasks
   - Implements: Fully qualified MCP names, error handling, workspace discovery

4. **Command with External Resource References** (Pattern #1: Progressive Disclosure)
   - Use when: Loading external files, templates, or configuration
   - Example: daily-signal loading advisor profiles
   - Implements: One-level-deep references, file cascade pattern

#### `/create-command` Workflow

1. Lists available plugins in repository
2. Validates plugin selection
3. Validates command name (enforces kebab-case)
4. Captures command purpose
5. Guides template selection (shows all 4 options with examples)
6. Identifies external integrations (MCP servers)
7. Plans resource files needed
8. Generates and validates all files
9. User confirms before creation

#### Manual Development (When Approved by User)

If user explicitly requests manual command creation:

1. **Review template library**: Read `dev-toolkit/resources/TEMPLATES.md` first
2. **Choose appropriate template**: Match your command type to one of the four templates
3. **Apply all relevant patterns**: Ensure you implement applicable patterns from the seven proven patterns
4. **Follow naming conventions**: Commands use kebab-case
5. **Validate structure**: Under 500 lines, one-level-deep references
6. **Test thoroughly**: Use plugin install/uninstall cycle
7. **Document**: Keep README.md in sync

### Standard Development Tasks

1. **Testing**: Use `/plugin uninstall` and `/plugin install` to reload changes
2. **Marketplace Updates**: Update `.claude-plugin/marketplace.json` when adding new plugins
3. **Documentation**: Keep README.md in sync with new features


## Repository Information

- GitHub: https://github.com/bigchewy/ai-tools
- Marketplace ID: eric-productivity-tools
- License: MIT
- Author: Eric W Page (@bigchewy)

## Working with This Project

### Creating Commands (MOST IMPORTANT)

**CRITICAL: Always use `/create-command` from dev-toolkit for creating new commands.**

This is the canonical, standardized way to create commands. It ensures:
- All 7 proven patterns are applied
- Consistent structure across all plugins
- Proper validation and error handling
- Template-based generation from working patterns

See the "Development Workflow" section above for complete `/create-command` documentation.

### Developing Other Plugin Components

When developing agents, resources, or modifying existing commands:

1. **For new commands**: Use `/create-command` (see above)
2. **For agents**: Follow patterns in existing agent files
3. **For resources**: Follow pattern #6 (Reusable Resource Template)
4. **For modifications**: Study the reference implementations below

### Reference Implementations

Study these files to understand working patterns:
- **Command creation tool:** `dev-toolkit/commands/create-command.md` - Shows how to guide command creation
- **Command templates:** `dev-toolkit/resources/TEMPLATES.md` - All four template types with examples
- **Command with state management:** `daily-signal/commands/morning-signal.md` - Multi-step interactive pattern
- **Persona resource template:** `daily-signal/resources/v_diana_chapman.md` - Reusable resource structure
- **Selection guide:** `daily-signal/resources/CLAUDE.md` - Decision tree and criteria
- **Profile template:** `daily-signal/resources/profile-template.md` - Configuration template

### Development Best Practices

1. **Use markdown format** for command/agent definitions
2. **Follow the established directory structure** - See Plugin Structure section above
3. **Apply proven patterns** when manually developing:
   - Progressive disclosure (Pattern #1)
   - State management for multi-step flows (Pattern #2)
   - File cascade for configuration (Pattern #3)
   - Explicit error handling (Pattern #4)
   - MCP tool integration (Pattern #5)
   - Reusable resource templates (Pattern #6)
   - Output file conventions (Pattern #7)
4. **Test thoroughly** using the plugin install/uninstall cycle
5. **Document new features** in README.md

## File Naming Conventions

- Commands: kebab-case (e.g., `morning-signal.md`)
- Agents: kebab-case (e.g., `asana-data-collector.md`)
- Resources: descriptive names (e.g., `profile-template.md`)
- Configuration: standard JSON (e.g., `plugin.json`, `marketplace.json`)

---

## How daily-signal Implements Best Practices

This section shows how the daily-signal plugin applies the best practices checklist:

### Core Quality ✓
- [x] **Under 500 lines**: Main command (200 lines), advisor files (~185 lines each)
- [x] **One-level-deep references**: Commands → resources, no nested references
- [x] **Consistent terminology**: "advisor" for persona, "quadrant" for Hoffman framework
- [x] **Concrete examples**: v_diana_chapman.md includes example dialogue (lines 62-69)
- [x] **Specific descriptions**: Each advisor has "When to Call On Them" table with triggers

### Information Architecture ✓
- [x] **Progressive disclosure**: Selection criteria in CLAUDE.md, full advisor details in separate files
- [x] **Domain-specific organization**: 6 advisor files by psychological approach
- [x] **Table of contents**: CLAUDE.md includes decision tree and detailed selection guide

### Error Handling ✓
- [x] **Explicit error paths**: Asana integration has documented fallback behavior
- [x] **Configuration cascade**: 4-level fallback for profile files
- [x] **Graceful degradation**: Task creation failure doesn't block session completion

### State Management ✓
- [x] **Context quarantine**: Each advisor invoked in dedicated session
- [x] **Context offloading**: Profile loaded once, then referenced
- [x] **Explicit flow control**: FORBIDDEN/REQUIRED rules prevent batching

### MCP Integration ✓
- [x] **Fully qualified names**: `mcp__asana__asana_create_task`
- [x] **Documented parameters**: All required fields specified
- [x] **Error recovery**: Workspace lookup fallback documented

This is what production-ready looks like. New plugins should match this quality bar.
