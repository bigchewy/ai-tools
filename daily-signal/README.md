# Daily Signal Plugin

Morning and evening check-in rituals for self-awareness and personal growth, powered by six expert psychologist personas.

## Overview

The daily-signal plugin provides structured daily check-ins that help you:
- Track mental, emotional, physical, and spiritual states
- Process complex emotions with evidence-based frameworks
- Build self-awareness through consistent reflection
- Integrate insights into actionable daily practices
- Maintain continuity through automated journaling

Each session is guided by one of six psychological experts, selected based on your current needs.

## The Six Advisors

1. **v_Brené_Brown** - Vulnerability & Courage
   - Best for emotional awareness, difficult conversations, perfectionism
   - "What story am I telling myself—and is it even true?"

2. **v_Diana_Chapman** - Conscious Leadership
   - Best for reactivity patterns, trust issues, decision paralysis
   - "Where are you on the line right now?"

3. **v_Jim_Loehr** - Energy Management
   - Best for burnout, guilt about rest, sustainable habits
   - "What activities give you energy versus drain it?"

4. **v_Steven_Hayes** - Acceptance & Commitment Therapy
   - Best for lost purpose, fighting limitations, identity transitions
   - "What would you do today if your symptoms weren't the enemy?"

5. **v_Marsha_Linehan** - Distress Tolerance (DBT)
   - Best for emotional overwhelm, crisis moments, managing unfairness
   - "What reality are you refusing to accept that's causing additional suffering?"

6. **v_Martin_Seligman** - Learned Optimism
   - Best for catastrophic thinking, learned helplessness, negative self-talk
   - "How are you explaining this setback to yourself—and is that explanation accurate?"

## Commands

### `/morning-signal`
Comprehensive morning reflection with automatic advisor selection:
1. Diana Chapman triages with 3-4 quick questions
2. System selects the most appropriate advisor based on your responses
3. Chosen advisor guides you through the Hoffman Quadrinity check:
   - 🧠 **Head** - What am I thinking?
   - ❤️ **Heart** - What am I feeling emotionally?
   - 🚶 **Body** - What sensations are present in my body?
   - ✨ **Spirit** - What does my Spiritual Self want me to know?
4. Integration question tailored to patterns
5. Daily score (1-10)
6. Five micro-practices for the day
7. Adventure walk question for reflection

**Output:** Saves to `domains/check_ins/morning/YYYY-MM-DD.md`

### `/morning-signal-hoffman-only`
Streamlined Hoffman Quadrinity check-in guided only by Diana Chapman, focusing on the four quadrants without advisor selection.

### `/evening-signal`
Evening reflection and integration practice for winding down the day.

**Output:** Saves to `domains/check_ins/evening/YYYY-MM-DD.md`

## Installation

### Option 1: Install as Part of AI Tools Monorepo

If you're using the full ai-tools repository:

```bash
cd "/path/to/your/claude-workspace"
git clone https://github.com/bigchewy/ai-tools.git
```

Then in Claude Code:
```
/plugin install ./ai-tools/.claude-plugin/marketplace.json
```

### Option 2: Install Daily Signal as Standalone Plugin

To install just the daily-signal plugin in another repository or folder:

#### Step 1: Copy the Plugin Files

```bash
# Navigate to your target directory
cd /path/to/your/project

# Create the plugin directory
mkdir -p daily-signal

# Copy the plugin files
cp -r /path/to/ai-tools/daily-signal/* daily-signal/
```

Or clone and extract just this plugin:

```bash
# Clone the repository
git clone https://github.com/bigchewy/ai-tools.git temp-ai-tools

# Copy just the daily-signal folder
cp -r temp-ai-tools/daily-signal ./daily-signal

# Remove the temp clone
rm -rf temp-ai-tools
```

#### Step 2: Create Plugin Configuration

Create `.claude-plugin/plugin.json` in the `daily-signal` directory (this should already exist if you copied the files):

```json
{
  "name": "daily-signal",
  "version": "1.0.0",
  "description": "Morning and evening check-in rituals with expert psychologist personas",
  "author": "Eric W Page",
  "commands": {
    "morning-signal": "commands/morning-signal.md",
    "morning-signal-hoffman-only": "commands/morning-signal-hoffman-only.md",
    "evening-signal": "commands/evening-signal.md"
  }
}
```

#### Step 3: Install in Claude Code

```
/plugin install ./daily-signal
```

Or if you want to install from a marketplace file:

Create `.claude-plugin/marketplace.json`:

```json
{
  "name": "Daily Signal",
  "plugins": [
    {
      "id": "daily-signal",
      "location": "daily-signal",
      "name": "Daily Signal",
      "description": "Morning and evening check-in rituals",
      "main": "commands/morning-signal.md"
    }
  ]
}
```

Then:
```
/plugin install ./.claude-plugin/marketplace.json
```

#### Step 4: Verify Installation

```
/plugin list
```

You should see `daily-signal` in the list.

### Option 3: Install from GitHub Directly

If you want to keep the plugin updated with the source:

```bash
cd /path/to/your/project
git submodule add https://github.com/bigchewy/ai-tools.git external/ai-tools
ln -s external/ai-tools/daily-signal daily-signal
```

Then install as above.

## Configuration

### User Profile (Optional but Recommended)

The plugin looks for your personal profile in this order:
1. `virtual_board/profile/main_profile.md` (if using Virtual Board system)
2. `profile/main_profile.md` (vault root)
3. `daily-signal-profile.md` (vault root)
4. `daily-signal/resources/profile-template.md` (fallback template)

To create your profile:

```bash
# Copy the template
cp daily-signal/resources/profile-template.md profile/main_profile.md

# Edit with your information
# Include: name, values, Enneagram type, current context
```

### File Storage

The plugin saves check-ins to:
- Morning: `domains/check_ins/morning/YYYY-MM-DD.md`
- Evening: `domains/check_ins/evening/YYYY-MM-DD.md`

Create these directories:

```bash
mkdir -p domains/check_ins/morning
mkdir -p domains/check_ins/evening
```

### Asana Integration (Optional)

If you have the Asana MCP server installed, the morning check-in will automatically create a task with your daily micro-practices.

Requirements:
- Asana MCP server configured
- Default workspace set in Asana
- Tasks will be titled: "Micro-Practices for Today - YYYY-MM-DD"

To disable Asana integration, the plugin gracefully handles missing MCP servers.

## Usage

### Basic Morning Check-In

```
/morning-signal
```

Follow the prompts:
1. Answer Diana's triage questions honestly
2. Complete the coherence breathing exercise (4s in, 7s out)
3. Respond to each quadrant question (Head, Heart, Body, Spirit)
4. Reflect on the integration question
5. Provide your daily score (1-10)
6. Review suggested micro-practices

**Time commitment:** 10-15 minutes

### Quick Hoffman Check

```
/morning-signal-hoffman-only
```

Diana Chapman guides you through just the four quadrants without advisor selection.

**Time commitment:** 5-7 minutes

### Evening Reflection

```
/evening-signal
```

Reflect on the day and practice gratitude.

**Time commitment:** 5-10 minutes

## Advanced Features

### Enneagram Integration

If your profile includes your Enneagram type, advisors will:
- Watch for type-specific compulsion patterns
- Offer type-aware interventions
- Reference your growth and stress patterns

Add to your profile:
```markdown
## Enneagram Type
Type: [Your type]
Wing: [Your wing]
```

Then create `profile/enneagram_patterns.md` with your patterns.

### Recent Pattern Review

Advisors automatically review your recent check-ins (past 3-7 days) to:
- Identify recurring themes
- Track energy and emotional patterns
- Notice breakthroughs or stuck points
- Tailor questions to your current journey

### Seven States Framework

If you use the Seven States framework, create `profile/seven_states_framework.md` and advisors will incorporate state tracking into sessions.

## Tips

- **Consistency matters**: Daily check-ins build self-awareness over time
- **Be honest**: The advisors adapt to your actual state, not your ideal state
- **One section at a time**: The system enforces pacing to prevent overwhelm
- **Review past check-ins**: Look for patterns across weeks and months
- **Trust the triage**: Diana's assessment usually selects the right advisor
- **Try different advisors**: Over time, use all six to build diverse skills

## Customization

### Adding Your Own Advisor

1. Create `daily-signal/resources/v_your_advisor.md`
2. Follow the structure in `v_diana_chapman.md`:
   - Archetype & Voice
   - Domains of Mastery
   - Challenge Prompts
   - Example Dialogue
   - Morning Check-In Protocol
3. Add selection criteria to `resources/CLAUDE.md`
4. Test with `/morning-signal`

### Modifying Questions

Edit the command files in `daily-signal/commands/`:
- `morning-signal.md` - Main morning flow
- `evening-signal.md` - Evening flow

Follow the state management patterns to maintain proper pacing.

## Troubleshooting

### "Profile not found" Warning

**Solution:** Create a profile using the template:
```bash
cp daily-signal/resources/profile-template.md profile/main_profile.md
```

### Asana Task Creation Fails

**Solution:** The session continues without blocking. Check:
- Asana MCP server is installed and configured
- Default workspace is set in Asana settings
- Network connection is active

### Advisor Asks Multiple Questions at Once

**Solution:** Report this as a bug. The state management rules should prevent batching. Try:
```
/plugin uninstall daily-signal
/plugin install ./daily-signal
```

### Check-In File Not Saved

**Solution:** Ensure directories exist:
```bash
mkdir -p domains/check_ins/morning domains/check_ins/evening
```

## Development

For developers wanting to understand or modify this plugin:

1. **Read CLAUDE.md** in this directory for architectural patterns
2. **Study `commands/morning-signal.md`** for state management implementation
3. **Review `resources/CLAUDE.md`** for advisor selection logic
4. **Examine `resources/v_diana_chapman.md`** for advisor template structure

### Testing Changes

```bash
# Uninstall current version
/plugin uninstall daily-signal

# Make your changes to files

# Reinstall
/plugin install ./daily-signal

# Test
/morning-signal
```

## Credits

### Frameworks
- **Hoffman Quadrinity Process**: Four-centered awareness (Head, Heart, Body, Spirit)
- **Conscious Leadership**: Diana Chapman, Jim Dethmer, Kaley Warner Klemp
- **The Gifts of Imperfection**: Brené Brown
- **The Power of Full Engagement**: Jim Loehr, Tony Schwartz
- **Acceptance and Commitment Therapy**: Steven Hayes
- **Dialectical Behavior Therapy**: Marsha Linehan
- **Learned Optimism**: Martin Seligman

### Plugin Development
- Author: Eric W Page (@bigchewy)
- License: MIT
- Repository: https://github.com/bigchewy/ai-tools

## Support

- **Issues**: https://github.com/bigchewy/ai-tools/issues
- **Discussions**: https://github.com/bigchewy/ai-tools/discussions
- **Documentation**: See CLAUDE.md in this directory for technical details

## License

MIT License - See LICENSE file in repository root.

---

**Version:** 1.0.0
**Last Updated:** 2024-11-01
