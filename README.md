# Eric's Productivity Tools for Claude Code

A collection of Claude Code plugins for productivity, self-awareness, and task management.

## Available Plugins

### 🌅 daily-signal
Morning and evening check-in rituals for self-awareness and personal growth.

**Commands:**
- `/morning-signal` - General morning reflection
- `/morning-signal-hoffman-only` - Hoffman Quadrinity check-in with Diana Chapman
- `/evening-signal` - Evening reflection and gratitude practice

**Features:**
- Guided check-ins by expert psychologists (Diana Chapman, Brené Brown, etc.)
- Automatic file creation with date stamps
- Integration with personal profile system
- Enneagram-aware prompts

### 📊 asana-toolkit
Asana task management and analytics tools.

**Agents:**
- `asana-data-collector` - Collect and analyze task data for any date range
- `asana-task-creator` - Convert insights into properly structured Asana tasks
- `asana-weekly-data` - Weekly task statistics and patterns

**Requirements:**
- Asana MCP server configured
- Asana workspace access

### 📝 weekly-reviews
Weekly review automation and documentation.

**Commands:**
- `/friday-check-in` - Structured weekly review process

**Agents:**
- `weekly-doc-creator` - Generate structured Google Docs for weekly reviews

## Installation

### 1. Add the marketplace

```bash
/plugin marketplace add https://github.com/bigchewy/Eric-tools
```

Or for local development:

```bash
/plugin marketplace add /path/to/Eric-tools
```

### 2. Browse and install plugins

```bash
/plugin
```

Then select "Browse Plugins" and choose which plugins to install.

Or install directly:

```bash
/plugin install daily-signal@eric-productivity-tools
/plugin install asana-toolkit@eric-productivity-tools
/plugin install weekly-reviews@eric-productivity-tools
```

## Configuration

### daily-signal

The daily-signal plugin looks for your personal profile in this order:
1. `virtual_board/profile/main_profile.md` (if using Virtual Board system)
2. `profile/main_profile.md` (vault root)
3. `daily-signal-profile.md` (vault root)

If none exist, create a profile based on the template in `daily-signal/resources/profile-template.md`.

### asana-toolkit

Requires the Asana MCP server. Configure in your Claude Code settings:

```json
{
  "mcpServers": {
    "asana": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-asana"],
      "env": {
        "ASANA_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

## Development

### Project Structure

```
Eric-tools/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace definition
├── daily-signal/              # Daily check-in plugin
├── asana-toolkit/             # Asana integration plugin
├── weekly-reviews/            # Weekly review plugin
└── README.md
```

### Testing Changes

1. Make changes to plugin files
2. Reinstall the plugin:
   ```
   /plugin uninstall plugin-name
   /plugin install plugin-name@eric-productivity-tools
   ```

### Contributing

This is a personal toolkit, but if you find it useful and want to suggest improvements, please open an issue or pull request.

## License

MIT License - See LICENSE file for details.

## Author

Eric W Page
GitHub: [@bigchewy](https://github.com/bigchewy)
