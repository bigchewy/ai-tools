# Command Templates

This file provides templates for different types of commands based on proven patterns from the ai-tools repository.

## Table of Contents
1. [Simple Single-Step Command](#simple-single-step-command)
2. [Multi-Step Interactive Command](#multi-step-interactive-command)
3. [Command with MCP Integration](#command-with-mcp-integration)
4. [Command with External Resource References](#command-with-external-resource-references)

---

## Simple Single-Step Command

**Use when:** Command has one clear task with no user interaction needed.

**Structure:**
```markdown
# [Command Name]

## Purpose
[1-2 sentence description of what this command does]

## Execution Instructions

[Clear, specific instructions for Claude to follow]

### Output Format
[Specify exactly what the output should look like]

### File Creation
[If applicable, specify where files should be saved]
```

**Example:** A command that generates a daily summary.

---

## Multi-Step Interactive Command

**Use when:** Command requires gathering information from user before execution.

**Based on:** daily-signal/commands/morning-signal.md (Pattern #2: State Management)

**Structure:**
```markdown
# [Command Name]

## Conversation Flow Control

### CRITICAL EXECUTION CONSTRAINTS
**CONVERSATION STATE TRACKING**: Track which section you're in (X total sections)
**CURRENT SECTION**: [Section1 | Section2 | Section3 | ...]

### MANDATORY CONVERSATION FLOW
1. **SECTION 1**: [Description]
   - **STOP HERE. Wait for the user's response before continuing.**

2. **SECTION 2**: [Description]
   - **STOP HERE. Wait for the user's response before continuing.**

3. **SECTION 3**: [Description]
   - **STOP HERE. Wait for the user's response before continuing.**

[Continue for all sections...]

### ENFORCEMENT RULES
- **FORBIDDEN**: Asking multiple questions in one response (except when explicitly allowed)
- **FORBIDDEN**: Moving to next section without user response
- **REQUIRED**: Each response must end with: "Please share your thoughts, and I'll continue with the next section."
- **REQUIRED**: Track current section number throughout conversation

---

## Execution Protocol

### Step 1: [First Step Name]
[Detailed instructions]

### Step 2: [Second Step Name]
[Detailed instructions]

[Continue for all steps...]

---

## Error Handling

### Common Issues
- **Issue 1**: [Description]
  - Solution: [How to handle]
- **Issue 2**: [Description]
  - Solution: [How to handle]

### Validation
- Check [condition] before proceeding
- Verify [requirement] is met
```

**Example:** daily-signal morning check-in with 9 sequential steps.

---

## Command with MCP Integration

**Use when:** Command needs to interact with external services (Asana, Google Docs, etc.)

**Based on:** daily-signal/commands/morning-signal.md (Pattern #5: MCP Integration)

**Structure:**
```markdown
# [Command Name]

## Purpose
[Description including which MCP server is used]

## Pre-Requisites
- MCP server `[server-name]` must be configured
- Required MCP tools: `mcp__[server]__[tool1]`, `mcp__[server]__[tool2]`

## Execution Instructions

[Main command instructions]

---

## MCP Integration Protocol

### Tool 1: [Tool Name]
**When to use:** [Description]

**Implementation:**
```
Use mcp__[server]__[tool] with:
- parameter1: [description]
- parameter2: [description]
- parameter3: [description]
```

**Example:**
```
Use mcp__asana__asana_create_task with:
- workspace: Use the user's default workspace
- assignee: "me"
- name: "[Task title format]"
- notes: [Description format]
- due_on: [Date format]
```

### Error Handling
- **If [condition]**: Use mcp__[server]__[fallback_tool] first
- **If [tool] fails**: [Describe fallback behavior]
- **Always**: Document what was attempted for reproducibility

---

## Output Documentation

After successful execution:
1. [What to save/output]
2. [Where to save it]
3. [What confirmation to provide]
```

**Example:** daily-signal creates Asana tasks after morning check-in.

---

## Command with External Resource References

**Use when:** Command needs to reference external files, templates, or documentation.

**Based on:** daily-signal/commands/morning-signal.md (Pattern #1: Progressive Disclosure)

**Structure:**
```markdown
# [Command Name]

## Purpose
[Description]

## Pre-Execution Reading Protocol

Before executing this command, MUST read:
1. `[plugin]/resources/[file1].md` - [Purpose]
2. `[plugin]/resources/[file2].md` - [Purpose]
3. `[plugin]/resources/[file3].md` - [Purpose]

**File Loading Rules:**
- Read files in order listed above
- Only load additional resources when explicitly needed
- Keep references one level deep (no nested reference chains)

---

## Resource Selection

[If applicable, describe how to choose which resource to use]

**Decision Criteria:**
- Use [resource1] when: [condition]
- Use [resource2] when: [condition]
- Use [resource3] when: [condition]

---

## Execution Instructions

[Main command logic, referencing loaded resources]

### Resource Application
1. Apply [resource1] by [description]
2. Integrate [resource2] through [description]
3. Reference [resource3] for [description]

---

## Configuration Cascade

[If applicable, show fallback paths for optional configuration]

Read configuration from (in order of preference):
1. `[path1]/[file].md` ([description])
2. `[path2]/[file].md` ([description])
3. `[path3]/[file].md` ([description])
4. If none exist, use `[plugin]/resources/[template].md`
```

**Example:** daily-signal loads advisor profiles and user configuration.

---

## Best Practice Checklist

When creating any command, ensure:

### Core Quality
- [ ] Under 500 lines total
- [ ] One-level-deep references (no nested chains)
- [ ] Consistent terminology throughout
- [ ] Concrete examples included
- [ ] Specific descriptions with key terms

### State Management (if multi-step)
- [ ] Explicit section tracking
- [ ] STOP markers after each user interaction
- [ ] FORBIDDEN behaviors clearly stated
- [ ] REQUIRED behaviors clearly stated

### Error Handling
- [ ] All error conditions documented
- [ ] Fallback behaviors specified
- [ ] Recovery paths described
- [ ] Validation steps included

### File Operations
- [ ] Output paths clearly specified
- [ ] File naming conventions documented
- [ ] Directory creation handled
- [ ] Conflict resolution addressed

### MCP Integration (if applicable)
- [ ] Fully qualified tool names (mcp__server__tool)
- [ ] All parameters documented
- [ ] Error recovery specified
- [ ] Workspace/config discovery documented
