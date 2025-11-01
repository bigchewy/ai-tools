# Claude Context: Daily Signal Plugin

## Plugin Overview

The daily-signal plugin provides morning and evening check-in rituals powered by six expert psychologist personas. Each persona specializes in different aspects of mental resilience, emotional processing, and adaptive living. The plugin integrates with Asana for task management and supports personalized user profiles.

## Architecture

### Core Components

1. **Commands** (`commands/`)
   - `morning-signal.md`: Main morning check-in flow with advisor selection
   - `evening-signal.md`: Evening reflection and integration
   - Additional check-in variations

2. **Resources** (`resources/`)
   - 6 advisor persona files (185 lines each)
   - `CLAUDE.md`: Selection guide for choosing the right advisor
   - `profile-template.md`: Template for user profiles

3. **Configuration** (`.claude-plugin/`)
   - `plugin.json`: Plugin metadata

### File Organization

```
daily-signal/
├── commands/           # Slash commands
│   ├── morning-signal.md
│   └── evening-signal.md
├── resources/          # Advisor personas and templates
│   ├── v_brene_brown.md
│   ├── v_diana_chapman.md
│   ├── v_jim_loehr.md
│   ├── v_marsha_linehan.md
│   ├── v_martin_seligman.md
│   ├── v_steven_hayes.md
│   ├── CLAUDE.md       # Selection guide
│   └── profile-template.md
└── .claude-plugin/
    └── plugin.json
```

## Production-Ready Patterns

This plugin demonstrates best practices for Claude Code plugin development. Study these patterns for new plugins.

### 1. Progressive Disclosure (Information Architecture)

**Structure:**
- Main command: 200 lines
- References 6 advisor files: ~185 lines each
- Selection guide: 199 lines
- Exactly one level deep - no nested references

**Implementation in morning-signal.md:8-9:**
```markdown
1. Read `daily-signal/resources/v_diana_chapman.md`
2. Read `daily-signal/resources/CLAUDE.md` for selection criteria
```

**Why it works:**
- Claude sees overview immediately
- Detailed context loads only when needed
- Prevents overwhelming single-file size
- Maintains manageable token usage

### 2. State Management Pattern

**Problem solved:** Prevents Claude from racing ahead or batching multiple questions in multi-step flows.

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

**Why it works:**
- Explicit FORBIDDEN/REQUIRED language is unambiguous
- State tracking creates clear mental model
- Enforces proper conversational pacing
- Prevents batching that ruins user experience

### 3. File Cascade Pattern (Configuration Fallback)

**Problem solved:** Gracefully handle optional user profiles with predictable fallback behavior.

**Implementation (morning-signal.md:116-120):**
```markdown
1. `virtual_board/profile/main_profile.md` (if using Virtual Board system)
2. `profile/main_profile.md` (vault root)
3. `daily-signal-profile.md` (vault root)
4. If none exist, use `daily-signal/resources/profile-template.md`
```

**Why it works:**
- Supports multiple user workflows
- Fails gracefully with template fallback
- No blocking errors from missing files
- Clear priority order

### 4. Explicit Error Handling

**Implementation (morning-signal.md:197-199):**
```markdown
### Error Handling
- If workspace not found: Use mcp__asana__asana_list_workspaces first
- If task creation fails: Note in check-in file but don't block session completion
- Always document what was attempted for reproducibility
```

**Why it works:**
- Documents failure paths explicitly
- Provides recovery procedures
- Never blocks critical user flows
- Enables debugging and reproducibility

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

**Why it works:**
- Fully qualified MCP names (`mcp__server__tool`)
- Explicit parameter documentation
- Clear example format
- Documented error paths

### 6. Reusable Resource Template

**All 6 advisor persona files follow identical structure:**

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

**Why it works:**
- Consistent structure aids comprehension
- Claude knows where to find specific information
- Easy to add new advisors
- Predictable token usage per advisor

**Reference implementation:** `daily-signal/resources/v_diana_chapman.md`

### 7. Output File Conventions

**Implementation pattern:**
```markdown
Check-ins are saved to:
- Morning: `domains/check_ins/morning/YYYY-MM-DD.md`
- Evening: `domains/check_ins/evening/YYYY-MM-DD.md`
```

**Why it works:**
- Domain-based organization
- ISO date format (sortable, unambiguous)
- Predictable paths for automation
- Easy to parse programmatically

## Advisor Selection System

### The Six Advisors

1. **v_Brené_Brown** - Vulnerability & Courage
   - Best for: Emotional awareness, difficult conversations, perfectionism
   - Signature: "What story am I telling myself—and is it even true?"

2. **v_Diana_Chapman** - Conscious Leadership
   - Best for: Reactivity patterns, trust issues, decision paralysis
   - Signature: "Where are you on the line right now?"

3. **v_Jim_Loehr** - Energy Management
   - Best for: Burnout, guilt about rest, sustainable habits
   - Signature: "What activities give you energy versus drain it?"

4. **v_Steven_Hayes** - Acceptance & Commitment Therapy
   - Best for: Lost purpose, fighting limitations, identity transitions
   - Signature: "What would you do today if your symptoms weren't the enemy?"

5. **v_Marsha_Linehan** - Distress Tolerance (DBT)
   - Best for: Emotional overwhelm, crisis moments, managing unfairness
   - Signature: "What reality are you refusing to accept that's causing additional suffering?"

6. **v_Martin_Seligman** - Learned Optimism
   - Best for: Catastrophic thinking, learned helplessness, negative self-talk
   - Signature: "How are you explaining this setback to yourself—and is that explanation accurate?"

### Selection Protocol

1. **Diana Chapman always triages first** (morning-signal.md:7-16)
2. She asks 3-4 rapid assessment questions
3. Based on responses, consults `resources/CLAUDE.md` decision tree
4. Selects most appropriate advisor
5. That advisor conducts the full session

This two-stage design (triage → specialist) ensures optimal advisor matching.

## Integration Points

### User Profile System

The plugin supports multiple profile locations with fallback:

1. Virtual Board system: `virtual_board/profile/main_profile.md`
2. Vault root: `profile/main_profile.md`
3. Plugin-specific: `daily-signal-profile.md`
4. Template fallback: `resources/profile-template.md`

### Asana Integration

After completing morning check-in:
- Creates task: "Micro-Practices for Today - [DATE]"
- Includes all 5 micro-practices as bulleted list
- Adds adventure walk question
- Assigns to user with today's due date

Uses MCP tool: `mcp__asana__asana_create_task`

### Enneagram Integration

If `profile/enneagram_patterns.md` exists:
- Advisors read type-specific compulsion patterns
- Apply type-aware interventions
- Watch for quadrant-specific flags

## Session Flow

### Morning Check-In (9 Sections)

1. **Triage**: Diana asks assessment questions → advisor selection
2. **Breathing**: Coherence breathing (4s in, 7s out)
3. **Head**: Mental space check
4. **Heart**: Emotional check
5. **Body**: Physical sensations
6. **Spirit**: Compassionate observer perspective
7. **Integration**: Tailored question based on patterns
8. **Score**: 1-10 daily rating
9. **Closing**: Micro-practices + adventure walk prompt

### State Management

- Track current section explicitly
- ONE question per response (except triage)
- Wait for user response before advancing
- Maintain same advisor throughout session
- Save file only after completing all sections

## Quality Checklist

This plugin meets all best practice standards:

### Core Quality ✓
- [x] Under 500 lines per file
- [x] One-level-deep references
- [x] Consistent terminology ("advisor", "quadrant")
- [x] Concrete examples in advisor profiles
- [x] Specific selection criteria with triggers

### Information Architecture ✓
- [x] Progressive disclosure (selection criteria → full profiles)
- [x] Domain-specific organization (6 advisors by approach)
- [x] Table of contents in CLAUDE.md

### Error Handling ✓
- [x] Explicit error paths for Asana integration
- [x] Configuration cascade for profiles
- [x] Graceful degradation (task failure doesn't block session)

### State Management ✓
- [x] Context quarantine (dedicated sessions per advisor)
- [x] Context offloading (profile loaded once)
- [x] Explicit flow control (FORBIDDEN/REQUIRED rules)

### MCP Integration ✓
- [x] Fully qualified names
- [x] Documented parameters
- [x] Error recovery procedures

## Development Guidelines

### Adding New Advisors

1. Create `resources/v_[name].md` following template structure (see pattern #6)
2. Add to advisor list in `resources/CLAUDE.md`
3. Update decision tree with selection criteria
4. Include example dialogue and synergies with existing advisors
5. Document "when NOT to use" section
6. Test with actual morning check-in flow

### Modifying Commands

1. Maintain state management pattern
2. Keep file references one level deep
3. Document error handling explicitly
4. Update this CLAUDE.md with any new patterns

### Testing

Use plugin reload cycle:
```bash
/plugin uninstall daily-signal
/plugin install /path/to/daily-signal
```

Test edge cases:
- Missing profile files (should fall back to template)
- Asana integration failure (should note but not block)
- All 6 advisors (verify personality consistency)

## Common Issues

### Issue: Claude batches multiple questions
**Solution:** Review state management rules in morning-signal.md:57-62

### Issue: Wrong advisor selected
**Solution:** Check triage questions and CLAUDE.md decision tree alignment

### Issue: Profile not found
**Solution:** Verify file cascade order (morning-signal.md:116-120)

### Issue: Asana task creation fails
**Solution:** Check error handling (morning-signal.md:197-199)

## Token Usage

Approximate token counts:
- Morning command: ~2,000 tokens
- Single advisor file: ~2,300 tokens
- Selection guide: ~2,500 tokens
- Typical session: ~7,000 tokens total

This is optimized through progressive disclosure—Claude only reads what's needed for each session.

## Future Enhancements

Potential additions:
- Evening check-in command expansion
- Additional advisor personas
- Integration with other MCP servers (Google Docs, etc.)
- Automated weekly pattern analysis
- Custom advisor creation workflow

## Reference Files

Key files to study:
- **Command example:** `commands/morning-signal.md`
- **Advisor template:** `resources/v_diana_chapman.md`
- **Selection logic:** `resources/CLAUDE.md`
- **Profile template:** `resources/profile-template.md`

## Related Documentation

- Main project: `/CLAUDE.md` (root-level context)
- Plugin marketplace: `/.claude-plugin/marketplace.json`
- Plugin metadata: `.claude-plugin/plugin.json`
