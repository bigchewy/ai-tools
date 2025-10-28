# asana-toolkit Plugin

Asana task management and analytics tools for Claude Code.

## Agents

### `asana-data-collector`
Collects comprehensive task data from Asana for any specified time period.

**Usage:**
```
Use the asana-data-collector agent to pull task data for the last 7 days
```

**Provides:**
- Total tasks completed, created, and overdue
- Daily distribution patterns
- Time-of-day completion patterns
- Project breakdown
- Planned vs emergent task ratio

### `asana-task-creator`
Converts weekly review insights and commitments into properly structured Asana tasks.

### `asana-weekly-data`
Collects Asana task data and provides basic statistical analysis for reviews.

## Requirements

This plugin requires the Asana MCP server. Configure in your Claude Code settings:

```json
{
  "mcpServers": {
    "asana": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-asana"],
      "env": {
        "ASANA_ACCESS_TOKEN": "your-access-token"
      }
    }
  }
}
```

Get your Asana access token at: https://app.asana.com/0/my-apps

## Tips

- Use `asana-data-collector` for deep analysis of any time period
- Use `asana-weekly-data` for quick weekly review stats
- Combine with `weekly-reviews` plugin for comprehensive weekly reviews
