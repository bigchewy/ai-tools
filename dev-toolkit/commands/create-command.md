# Create Command - Interactive Command Generator

## Purpose

Generate new slash commands for ai-tools plugins following established patterns and best practices. This command guides you through the creation process, validates inputs, and creates properly structured command files.

## Prerequisites

**CRITICAL:** This command MUST be run from within the ai-tools repository directory.

**Repository Path Detection:**
- Use the current working directory as repo_root
- Validate we're in ai-tools by checking for `.claude-plugin/marketplace.json`
- All paths in validation script should be relative to repo_root

**Important Note:** Every plugin MUST have `.claude-plugin/plugin.json` for commands to be discovered by Claude Code. The validation script will check for this and offer to create it if missing.

## Pre-Execution Reading Protocol

Before starting, MUST read:
1. `dev-toolkit/resources/TEMPLATES.md` - Review all available command templates
2. Scan available plugins by listing directories in ai-tools root
3. Get current working directory to use as repo_root

---

## Conversation Flow Control

### CRITICAL EXECUTION CONSTRAINTS
**CONVERSATION STATE TRACKING**: Track which section you're in (1-8 total sections)
**CURRENT SECTION**: [Discovery | Plugin | Name | Purpose | Type | Integration | Resources | Generation]

### MANDATORY CONVERSATION FLOW

1. **DISCOVERY**: List available plugins
   - **STOP HERE. Show plugin list and wait for user input.**

2. **PLUGIN SELECTION**: Get target plugin name
   - **STOP HERE. Wait for the user's plugin selection before continuing.**

3. **NAME INPUT**: Get command name
   - **STOP HERE. Wait for the user's command name before continuing.**

4. **PURPOSE DEFINITION**: Get command purpose
   - **STOP HERE. Wait for the user's purpose description before continuing.**

5. **TYPE SELECTION**: Determine command type/template
   - **STOP HERE. Wait for the user's template selection before continuing.**

6. **INTEGRATION CHECK**: Identify external integrations needed
   - **STOP HERE. Wait for the user's response before continuing.**

7. **RESOURCE PLANNING**: Determine if resource files needed
   - **STOP HERE. Wait for the user's response before continuing.**

8. **GENERATION**: Validate, generate, and save files
   - **STOP HERE. Show validation results and wait for confirmation before creating files.**

### ENFORCEMENT RULES
- **FORBIDDEN**: Asking multiple questions in one response (except when showing options)
- **FORBIDDEN**: Moving to next section without user response
- **FORBIDDEN**: Generating files without explicit user confirmation
- **REQUIRED**: Each response must end with: "Please provide your input, and I'll continue with the next step."
- **REQUIRED**: Use validation script before file creation
- **REQUIRED**: Track current section number throughout conversation

---

## Execution Protocol

### Section 1: Discovery - List Available Plugins

**Actions:**
1. List all directories in ai-tools root (excluding hidden dirs and files)
2. For each plugin, show: name and brief description from its README.md (first paragraph only)
3. Present numbered list to user

**Output Format:**
```
Available plugins in your ai-tools repository:

1. daily-signal - [Brief description]
2. asana-toolkit - [Brief description]
3. weekly-reviews - [Brief description]
4. dev-toolkit - [Brief description]

Which plugin should this command be added to? (Enter plugin name or number)
```

**STOP HERE. Wait for user's plugin selection before continuing.**

---

### Section 2: Plugin Selection - Validate Target Plugin

**Actions:**
1. Capture user's plugin selection (name or number)
2. Get current working directory to use as repo_root:
   ```bash
   pwd
   ```
3. Validate plugin exists using validation script:
   ```bash
   python3 dev-toolkit/resources/create_command_script.py \
     "$(pwd)" \
     "[plugin-name]" \
     "temp-validation" \
     --validate-only
   ```
4. Parse JSON output to check:
   - plugin_exists is true
   - plugin_json_exists is true (CRITICAL for command discovery)
5. If plugin.json is missing, offer to create it:
   ```bash
   python3 dev-toolkit/resources/create_command_script.py \
     "$(pwd)" \
     "[plugin-name]" \
     "temp" \
     --create-plugin-json
   ```

**Error Handling:**
- If plugin not found: Ask if user wants to create new plugin (yes/no)
- If creating new plugin: Will need to create plugin directory structure and update marketplace.json
- If plugin.json missing: Explain it's REQUIRED and offer to create it
- If user declines plugin.json creation: Warn commands won't work but allow proceeding
- If user declines: Return to Section 1

**Output Format:**
```
✓ Plugin '[plugin-name]' found.

Now, what should we name this command?

Command names must follow kebab-case convention:
- Lowercase letters, numbers, and hyphens only
- Cannot start or end with hyphen
- No consecutive hyphens
- Examples: morning-signal, create-task, weekly-review

Enter command name:
```

**STOP HERE. Wait for user's command name before continuing.**

---

### Section 3: Name Input - Validate Command Name

**Actions:**
1. Capture user's command name
2. Validate command name using validation script:
   ```bash
   python3 dev-toolkit/resources/create_command_script.py \
     "$(pwd)" \
     "[plugin-name]" \
     "[command-name]" \
     --validate-only
   ```
3. Parse JSON output to check:
   - command_name_valid is true
   - command_already_exists is false
   - plugin_json_exists is true (should already be confirmed in Section 2)

**Error Handling:**
- If name invalid: Show specific validation error and ask for new name (loop back to start of Section 3)
- If command exists: Ask if user wants to overwrite (yes/no)
  - If no: Return to start of Section 3
  - If yes: Continue but flag for overwrite in Section 8

**Output Format:**
```
✓ Command name '[command-name]' is valid and available.

Next, describe the purpose of this command in 1-2 sentences.

What should this command do?
```

**STOP HERE. Wait for user's purpose description before continuing.**

---

### Section 4: Purpose Definition - Capture Command Purpose

**Actions:**
1. Capture user's purpose description (1-2 sentences)
2. Store for use in command file generation

**Output Format:**
```
Got it. This command will: [purpose description]

Now, let's determine which template to use. Review these options:

1. Simple Single-Step Command
   - Best for: One clear task, no user interaction needed
   - Example: Generate a daily summary

2. Multi-Step Interactive Command
   - Best for: Gathering information from user before execution
   - Example: Morning check-in with multiple questions
   - Implements state management pattern

3. Command with MCP Integration
   - Best for: Interacting with external services (Asana, Google Docs, etc.)
   - Example: Creating Asana tasks automatically
   - Requires MCP server configuration

4. Command with External Resource References
   - Best for: Loading external files, templates, or documentation
   - Example: Loading advisor profiles or configuration files
   - Implements progressive disclosure pattern

Which template best fits your command? (Enter number 1-4)
```

**STOP HERE. Wait for user's template selection before continuing.**

---

### Section 5: Type Selection - Choose Command Template

**Actions:**
1. Capture user's template selection (1-4)
2. Load appropriate template structure from TEMPLATES.md
3. Store template choice for generation phase

**Output Format:**
```
✓ Using template: [Template Name]

Does this command need to integrate with external services?

Examples of integrations:
- MCP servers (Asana, Google Docs, Slack, etc.)
- File system operations (reading/writing specific file formats)
- API calls to external services
- Database operations

Enter integration details, or type "none" if no external integrations needed:
```

**STOP HERE. Wait for user's response about integrations before continuing.**

---

### Section 6: Integration Check - Identify External Dependencies

**Actions:**
1. Capture integration requirements
2. If MCP integration mentioned:
   - Note which MCP server(s)
   - Flag need for MCP integration documentation
3. If file operations mentioned:
   - Note file paths and formats
4. Store integration details for generation phase

**Output Format (if integrations specified):**
```
✓ Noted integrations: [integration details]

Will this command need additional resource files?

Resource files can include:
- Templates (markdown, JSON, etc.)
- Reference documentation
- Configuration files
- Example files
- Helper scripts

Enter "yes" if you need resource files, or "no" to skip:
```

**Output Format (if no integrations):**
```
✓ No external integrations needed.

Will this command need additional resource files?

Resource files can include:
- Templates (markdown, JSON, etc.)
- Reference documentation
- Configuration files
- Example files

Enter "yes" if you need resource files, or "no" to skip:
```

**STOP HERE. Wait for user's response about resource files before continuing.**

---

### Section 7: Resource Planning - Plan Resource Files

**Actions:**
1. Capture resource file requirements (yes/no)
2. If yes:
   - Ask what types of resources needed
   - Note resource directory will be created at `[plugin]/resources/[command-name]/`
3. If no:
   - Proceed without resource directory
4. Store resource plan for generation phase

**Output Format (if yes):**
```
✓ Resource directory will be created at: [plugin]/resources/[command-name]/

What types of resource files do you need?
(Describe the files you want to create, e.g., "template.md", "config-example.json")

Enter resource files needed, or "done" when finished listing:
```

**Output Format (if no):**
```
✓ No resource files needed.

Ready to generate your command! Here's what will be created:

Plugin: [plugin-name]
Command: /[command-name]
Purpose: [purpose]
Template: [template-name]
Integrations: [integration details or "none"]
Resources: [resource details or "none"]

Command file will be created at:
[plugin]/commands/[command-name].md

[If resources] Resource directory will be created at:
[plugin]/resources/[command-name]/

Proceed with generation? (yes/no)
```

**STOP HERE. Wait for user's final confirmation before continuing.**

---

### Section 8: Generation - Create Command Files

**CRITICAL: DO NOT proceed with file creation without explicit user confirmation.**

**Actions:**

1. **Run Final Validation:**
   ```bash
   python3 dev-toolkit/resources/create_command_script.py \
     "$(pwd)" \
     "[plugin-name]" \
     "[command-name]" \
     --validate-only
   ```

2. **Parse Validation Results:**
   - Check all validation flags
   - Confirm plugin_json_exists is true (CRITICAL)
   - If any validation fails, show error and STOP
   - If validation passes, proceed

3. **Generate Command Content:**
   - Use selected template from TEMPLATES.md
   - Fill in:
     - Command name
     - Purpose
     - Integration details
     - Resource references
   - Follow template structure exactly
   - Add error handling section
   - Add best practice checklist at end

4. **Create Command File:**
   ```bash
   # Write generated content to file
   # Path: [plugin]/commands/[command-name].md
   ```

5. **Create Resource Directory (if needed):**
   ```bash
   python3 -c "
   from pathlib import Path
   Path('[plugin]/resources/[command-name]').mkdir(parents=True, exist_ok=True)
   "
   ```

6. **Update Plugin README:**
   - Read current README.md
   - Add new command to commands list
   - Preserve existing formatting
   - Write updated README.md

7. **Create Summary Document:**
   - Create `[plugin]/resources/[command-name]/README.md` if resources created
   - Document what was created and how to use

**Error Handling:**
- If file creation fails: Report specific error, preserve what was created, provide manual steps
- If README update fails: Report error, command still created, provide manual README update instructions
- If validation fails: Report validation errors, do not create any files, provide fix suggestions

**Output Format (on success):**
```
✓ Command created successfully!

Files created:
- [plugin]/commands/[command-name].md

[If resources]
- [plugin]/resources/[command-name]/ (directory)

[If README updated]
- [plugin]/README.md (updated)

Next steps:
1. Review the generated command file at: [path]
2. Customize the template as needed for your specific use case
3. If using MCP integration, ensure your MCP servers are configured
4. Test the command with: /[command-name]

[If in git repo]
Don't forget to commit these changes:
git add [plugin]/
git commit -m "Add /[command-name] command to [plugin]"
```

**Output Format (on error):**
```
✗ Error creating command: [error message]

Validation results:
[Show validation JSON]

Suggested fixes:
[List specific actions user should take]

Would you like to try again? (yes/no)
```

---

## Error Handling Reference

### Validation Errors

**Plugin not found:**
- Message: "Plugin directory not found: [path]"
- Fix: Create plugin directory or check spelling
- Recovery: Offer to create new plugin

**Invalid command name:**
- Message: "Command name must be lowercase letters, numbers, and hyphens only (kebab-case)"
- Fix: Provide valid example names
- Recovery: Ask for new name

**Command already exists:**
- Message: "WARNING: Command file already exists: [path]"
- Fix: Choose different name or confirm overwrite
- Recovery: Return to name input or proceed with overwrite

**Missing plugin.json:**
- Message: "WARNING: Missing required file: .claude-plugin/plugin.json"
- Fix: This file is CRITICAL for command discovery. Commands will NOT work without it.
- Recovery: Offer to create with --create-plugin-json flag
- Command: `python3 dev-toolkit/resources/create_command_script.py "$(pwd)" "[plugin-name]" "temp" --create-plugin-json`

**Validation script error:**
- Message: "Failed to run validation: [error]"
- Fix: Check Python is available, check script permissions
- Recovery: Show manual validation steps

### File Creation Errors

**Permission denied:**
- Message: "Failed to create [file]: Permission denied"
- Fix: Check directory permissions
- Recovery: Provide manual file creation steps

**Directory creation failed:**
- Message: "Failed to create directory: [error]"
- Fix: Check parent directory exists and is writable
- Recovery: Show manual mkdir commands

**README update failed:**
- Message: "Command created but README update failed: [error]"
- Fix: Command is still usable, README needs manual update
- Recovery: Provide manual README update instructions

---

## Template Application Guide

### For Simple Single-Step Commands
- Use minimal structure
- Focus on clear execution instructions
- Specify output format explicitly
- Include file creation paths if applicable

### For Multi-Step Interactive Commands
- Implement full state tracking
- Add CRITICAL EXECUTION CONSTRAINTS section
- Add ENFORCEMENT RULES section
- Define each step with STOP marker
- Include section tracking

### For Commands with MCP Integration
- Document required MCP servers in prerequisites
- Use fully qualified tool names (mcp__server__tool)
- Document all parameters explicitly
- Include error handling for MCP failures
- Add fallback behaviors

### For Commands with Resource References
- List all resources in Pre-Execution Reading Protocol
- Use explicit file paths
- Keep references one level deep
- Add resource selection criteria if multiple options
- Include configuration cascade if applicable

---

## Best Practices Applied

This command implements:
- ✓ Pattern #2: State Management (8-section flow with explicit STOP markers)
- ✓ Pattern #4: Error Handling (comprehensive validation and recovery)
- ✓ Pattern #1: Progressive Disclosure (references TEMPLATES.md)
- ✓ Pattern #7: Output Conventions (kebab-case, structured paths)
- ✓ Validation Script (Python utility for file operations)
- ✓ Quality Checklist (ensures generated commands meet standards)

---

## Validation Script Reference

The validation script (`dev-toolkit/resources/create_command_script.py`) provides:
- Plugin existence checking
- **Plugin.json validation (CRITICAL for command discovery)**
- Command name validation (kebab-case)
- File conflict detection
- Directory creation (with error handling)
- Plugin.json creation (--create-plugin-json flag)
- JSON output for programmatic parsing

**Usage for validation:**
```bash
python3 dev-toolkit/resources/create_command_script.py \
  "$(pwd)" \
  "<plugin-name>" \
  "<command-name>" \
  [--validate-only]
```

**Usage for creating plugin.json:**
```bash
python3 dev-toolkit/resources/create_command_script.py \
  "$(pwd)" \
  "<plugin-name>" \
  "temp" \
  --create-plugin-json
```

**Output JSON:**
```json
{
  "plugin_exists": bool,
  "plugin_json_exists": bool,
  "plugin_json_path": str,
  "command_name_valid": bool,
  "command_already_exists": bool,
  "commands_dir_ready": bool,
  "messages": [str],
  "command_path": str
}
```

**Exit Codes:**
- 0: Success
- 1: Validation failure (plugin or name invalid)
- 2: File already exists
- 3: Plugin.json missing (warning, not blocking)

---

## Marketplace Setup

**IMPORTANT:** Marketplace configuration is done ONCE, not per-command.

### Initial Setup (First Time Only)

**For GitHub repositories (recommended for sharing):**
```bash
/plugin marketplace add https://github.com/bigchewy/ai-tools
```

**For local development:**
```bash
/plugin marketplace add file:///path/to/ai-tools
```

### After Setup

Once the marketplace is added, always install plugins by name:
```bash
/plugin install dev-toolkit@eric-productivity-tools
```

**Never use absolute paths repeatedly.** The marketplace URL is configured once, then you reference plugins by marketplace name (`@eric-productivity-tools`).

### Reloading After Changes

When you create new commands or modify plugins:
```bash
/plugin uninstall dev-toolkit
/plugin install dev-toolkit@eric-productivity-tools
```

Or restart Claude Code to reload all plugins.

---

## Notes

- This command creates the foundation. The user will need to customize the generated command for their specific needs.
- All generated commands follow the 7 proven patterns from daily-signal
- Generated commands include best practice checklists
- Validation ensures consistency across the plugin ecosystem
- User must confirm before any files are created
- **CRITICAL:** Every plugin MUST have `.claude-plugin/plugin.json` or commands won't be discovered
