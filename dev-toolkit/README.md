# dev-toolkit Plugin

Development tools for creating and managing ai-tools plugins, commands, and agents.

## Commands

### `/create-command`
Interactive command generator that guides you through creating new slash commands for your plugins.

**Features:**
- Validates plugin and command names
- Offers multiple templates (simple, multi-step, MCP integration, resource references)
- Generates properly structured command files following best practices
- Creates resource directories when needed
- Updates plugin README automatically
- Implements all 7 proven patterns from daily-signal

**When to use:**
- Creating a new slash command for any plugin
- Want to follow established patterns and best practices
- Need guidance on command structure and state management
- Building commands that integrate with MCP servers

**Workflow:**
1. Lists available plugins in your repository
2. Validates plugin selection
3. Validates command name (kebab-case)
4. Captures command purpose
5. Guides template selection (4 options)
6. Identifies external integrations
7. Plans resource files
8. Generates and validates all files

**Example usage:**
```
/create-command
```

Then follow the interactive prompts to create your command.

## Resources

### TEMPLATES.md
Comprehensive template library showing 4 command patterns:
1. **Simple Single-Step Command** - For straightforward one-task commands
2. **Multi-Step Interactive Command** - For information-gathering workflows
3. **Command with MCP Integration** - For external service integration
4. **Command with External Resource References** - For commands that load resources

Each template includes:
- When to use it
- Complete structure
- Working examples from daily-signal
- Best practice checklist

### create_command_script.py
Python utility script for validation and file operations:
- Plugin existence checking
- Command name validation (kebab-case enforcement)
- File conflict detection
- Directory creation with error handling
- JSON output for programmatic parsing

**Usage:**
```bash
python3 dev-toolkit/resources/create_command_script.py \
  "<repo-root>" \
  "<plugin-name>" \
  "<command-name>" \
  [--validate-only]
```

## Design Philosophy

The dev-toolkit follows these principles:

### 1. Pattern-Based Generation
All generated commands follow the 7 proven patterns from daily-signal:
1. Progressive Disclosure (one-level references)
2. State Management (explicit flow control)
3. File Cascade (configuration fallbacks)
4. Error Handling (documented recovery paths)
5. MCP Integration (fully qualified names)
6. Resource Templates (consistent structure)
7. Output Conventions (predictable paths)

### 2. Validation First
Every command creation goes through validation before file operations:
- Plugin exists
- Command name is valid kebab-case
- No file conflicts
- Directories can be created
- User confirms before changes

### 3. Interactive Guidance
The `/create-command` workflow uses state management to:
- Ask one question at a time
- Provide clear examples and options
- Prevent user errors through validation
- Allow user to confirm before file creation

### 4. Extensibility
Template library is designed for future expansion:
- Add new templates by updating TEMPLATES.md
- Validation script can be enhanced with new checks
- Command generator can support new plugin types

## Best Practices Implemented

### Core Quality ✓
- [x] Under 500 lines per command file
- [x] One-level-deep references (TEMPLATES.md)
- [x] Consistent terminology throughout
- [x] Concrete examples in templates
- [x] Specific descriptions with key terms

### State Management ✓
- [x] 8-section flow with explicit tracking
- [x] STOP markers after each user interaction
- [x] FORBIDDEN behaviors clearly stated
- [x] REQUIRED behaviors enforced

### Error Handling ✓
- [x] All validation errors documented
- [x] Fallback behaviors specified
- [x] Recovery paths described
- [x] Validation steps executed before file operations

### Code & Scripts ✓
- [x] Python validation script with error handling
- [x] All constants documented (exit codes, JSON structure)
- [x] Clear separation: validation vs file creation
- [x] JSON output for programmatic use

## Installation

This plugin is part of the ai-tools marketplace:

```bash
/plugin install dev-toolkit@eric-productivity-tools
```

## Usage Tips

### Creating Your First Command

1. Run `/create-command`
2. Select your target plugin
3. Choose a descriptive kebab-case name (e.g., `weekly-report`, `create-task`)
4. Describe what the command does in 1-2 sentences
5. Select the appropriate template:
   - **Simple** for quick one-step operations
   - **Multi-Step** for gathering user input
   - **MCP Integration** for external services
   - **Resource References** for loading files
6. Specify any integrations needed
7. Confirm resource file requirements
8. Review and confirm generation

### Customizing Generated Commands

Generated commands are starting points:
- Review the generated .md file
- Customize sections for your specific needs
- Add domain-specific logic
- Enhance error handling for your use case
- Add examples relevant to your domain

### Template Selection Guide

**Choose Simple Single-Step when:**
- Command has one clear task
- No user input required during execution
- Minimal error handling needed
- Example: Generate a daily summary

**Choose Multi-Step Interactive when:**
- Need to gather information from user
- Multiple questions in sequence
- User should review before final action
- Example: Morning check-in, project setup

**Choose MCP Integration when:**
- Calling external services (Asana, Google Docs, etc.)
- Need error handling for API failures
- Workspace/configuration discovery required
- Example: Create Asana task, send Slack message

**Choose Resource References when:**
- Loading external files, templates, configs
- Multiple resource options to choose from
- Configuration cascade needed
- Example: Load advisor profiles, apply templates

## Future Enhancements

Planned additions to dev-toolkit:

- `/create-agent` - Generate agent definitions
- `/create-plugin` - Scaffold new plugin structure
- `/validate-plugin` - Check plugin follows best practices
- `/export-plugin` - Package plugin for distribution
- Template versioning and updates
- Command testing framework

## Contributing

When adding new templates or features:
1. Follow the existing pattern structure
2. Add validation logic to script if needed
3. Update TEMPLATES.md with new patterns
4. Test with multiple command types
5. Document in this README

## References

This plugin implements patterns documented in:
- `Claude.md` - Project context and best practices
- `daily-signal/` - Reference implementation
- Claude Code docs - Official skill best practices

## Author

Eric W Page (@bigchewy)

Part of the eric-productivity-tools marketplace.
