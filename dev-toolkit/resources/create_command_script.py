#!/usr/bin/env python3
"""
Command creation utility script for ai-tools plugins.

This script validates and creates command files following established patterns.
DO NOT modify this script - it implements proven validation logic.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime


def validate_plugin_exists(repo_root: str, plugin_name: str) -> tuple[bool, str]:
    """
    Validate that the plugin directory exists.

    Returns: (success: bool, message: str)
    """
    plugin_path = Path(repo_root) / plugin_name

    if not plugin_path.exists():
        return False, f"Plugin directory not found: {plugin_path}"

    if not plugin_path.is_dir():
        return False, f"Path exists but is not a directory: {plugin_path}"

    return True, f"Plugin directory found: {plugin_path}"


def validate_command_name(command_name: str) -> tuple[bool, str]:
    """
    Validate command name follows kebab-case convention.

    Returns: (success: bool, message: str)
    """
    # Check for empty
    if not command_name:
        return False, "Command name cannot be empty"

    # Check for valid characters (lowercase, numbers, hyphens only)
    if not all(c.islower() or c.isdigit() or c == '-' for c in command_name):
        return False, "Command name must be lowercase letters, numbers, and hyphens only (kebab-case)"

    # Check doesn't start or end with hyphen
    if command_name.startswith('-') or command_name.endswith('-'):
        return False, "Command name cannot start or end with a hyphen"

    # Check doesn't have consecutive hyphens
    if '--' in command_name:
        return False, "Command name cannot have consecutive hyphens"

    return True, "Command name is valid"


def check_command_exists(repo_root: str, plugin_name: str, command_name: str) -> tuple[bool, str]:
    """
    Check if command file already exists.

    Returns: (exists: bool, path: str)
    """
    command_path = Path(repo_root) / plugin_name / "commands" / f"{command_name}.md"
    return command_path.exists(), str(command_path)


def ensure_commands_directory(repo_root: str, plugin_name: str) -> tuple[bool, str]:
    """
    Ensure the commands directory exists, create if needed.

    Returns: (success: bool, message: str)
    """
    commands_dir = Path(repo_root) / plugin_name / "commands"

    try:
        commands_dir.mkdir(parents=True, exist_ok=True)
        return True, f"Commands directory ready: {commands_dir}"
    except Exception as e:
        return False, f"Failed to create commands directory: {e}"


def ensure_resources_directory(repo_root: str, plugin_name: str, command_name: str = None) -> tuple[bool, str]:
    """
    Ensure the resources directory exists, optionally for specific command.

    Returns: (success: bool, message: str)
    """
    if command_name:
        resources_dir = Path(repo_root) / plugin_name / "resources" / command_name
    else:
        resources_dir = Path(repo_root) / plugin_name / "resources"

    try:
        resources_dir.mkdir(parents=True, exist_ok=True)
        return True, f"Resources directory ready: {resources_dir}"
    except Exception as e:
        return False, f"Failed to create resources directory: {e}"


def check_plugin_json_exists(repo_root: str, plugin_name: str) -> tuple[bool, str, str]:
    """
    Check if .claude-plugin/plugin.json exists.

    CRITICAL: Without this file, commands will NOT be discovered by Claude Code.
    Every plugin MUST have .claude-plugin/plugin.json for commands to work.

    Returns: (exists: bool, path: str, message: str)
    """
    plugin_json_path = Path(repo_root) / plugin_name / ".claude-plugin" / "plugin.json"

    if plugin_json_path.exists():
        return True, str(plugin_json_path), f"Plugin config found: {plugin_json_path}"
    else:
        return False, str(plugin_json_path), f"WARNING: Missing required file: {plugin_json_path}"


def create_plugin_json(repo_root: str, plugin_name: str, description: str = None) -> tuple[bool, str]:
    """
    Create .claude-plugin/plugin.json file.

    This file is REQUIRED for Claude Code to discover the plugin's commands.

    Returns: (success: bool, message: str)
    """
    plugin_dir = Path(repo_root) / plugin_name / ".claude-plugin"
    plugin_json_path = plugin_dir / "plugin.json"

    # Create directory if needed
    try:
        plugin_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return False, f"Failed to create .claude-plugin directory: {e}"

    # Default description if not provided
    if not description:
        description = f"Commands and tools for {plugin_name}"

    # Create plugin.json content
    plugin_json = {
        "name": plugin_name,
        "version": "1.0.0",
        "description": description,
        "author": "Eric W Page",
        "repository": "https://github.com/bigchewy/ai-tools",
        "keywords": ["productivity", "tools"]
    }

    # Write file
    try:
        with open(plugin_json_path, 'w', encoding='utf-8') as f:
            json.dump(plugin_json, f, indent=2)
            f.write('\n')  # Add trailing newline
        return True, f"Plugin config created: {plugin_json_path}"
    except Exception as e:
        return False, f"Failed to create plugin.json: {e}"


def create_command_file(repo_root: str, plugin_name: str, command_name: str, content: str) -> tuple[bool, str]:
    """
    Create the command markdown file.

    Returns: (success: bool, message: str)
    """
    command_path = Path(repo_root) / plugin_name / "commands" / f"{command_name}.md"

    try:
        with open(command_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, f"Command file created: {command_path}"
    except Exception as e:
        return False, f"Failed to create command file: {e}"


def validate_all(repo_root: str, plugin_name: str, command_name: str) -> dict:
    """
    Run all validations and return structured results.

    Returns: {
        "plugin_exists": bool,
        "plugin_json_exists": bool,
        "plugin_json_path": str,
        "command_name_valid": bool,
        "command_already_exists": bool,
        "commands_dir_ready": bool,
        "messages": [str],
        "command_path": str
    }
    """
    results = {
        "plugin_exists": False,
        "plugin_json_exists": False,
        "plugin_json_path": "",
        "command_name_valid": False,
        "command_already_exists": False,
        "commands_dir_ready": False,
        "messages": [],
        "command_path": ""
    }

    # Validate plugin exists
    success, message = validate_plugin_exists(repo_root, plugin_name)
    results["plugin_exists"] = success
    results["messages"].append(message)

    if not success:
        return results

    # CRITICAL: Check for .claude-plugin/plugin.json
    # This file is REQUIRED for commands to be discovered by Claude Code
    exists, plugin_json_path, message = check_plugin_json_exists(repo_root, plugin_name)
    results["plugin_json_exists"] = exists
    results["plugin_json_path"] = plugin_json_path
    results["messages"].append(message)

    if not exists:
        results["messages"].append("CRITICAL: Commands will NOT work without .claude-plugin/plugin.json")
        results["messages"].append("Run with --create-plugin-json flag to create this file")

    # Validate command name
    success, message = validate_command_name(command_name)
    results["command_name_valid"] = success
    results["messages"].append(message)

    if not success:
        return results

    # Check if command already exists
    exists, path = check_command_exists(repo_root, plugin_name, command_name)
    results["command_already_exists"] = exists
    results["command_path"] = path

    if exists:
        results["messages"].append(f"WARNING: Command file already exists: {path}")
    else:
        results["messages"].append(f"Command file will be created at: {path}")

    # Ensure directories exist
    success, message = ensure_commands_directory(repo_root, plugin_name)
    results["commands_dir_ready"] = success
    results["messages"].append(message)

    return results


if __name__ == "__main__":
    # This script is designed to be called by Claude Code
    # It expects: repo_root plugin_name command_name [--validate-only] [--create-plugin-json]

    if len(sys.argv) < 4:
        print(json.dumps({
            "error": "Usage: create_command_script.py <repo_root> <plugin_name> <command_name> [--validate-only] [--create-plugin-json]"
        }))
        sys.exit(1)

    repo_root = sys.argv[1]
    plugin_name = sys.argv[2]
    command_name = sys.argv[3]
    validate_only = "--validate-only" in sys.argv
    create_plugin_json_flag = "--create-plugin-json" in sys.argv

    # Handle plugin.json creation if requested
    if create_plugin_json_flag:
        success, message = create_plugin_json(repo_root, plugin_name)
        result = {
            "success": success,
            "message": message,
            "plugin_json_created": success
        }
        print(json.dumps(result, indent=2))
        sys.exit(0 if success else 1)

    # Run validation
    results = validate_all(repo_root, plugin_name, command_name)

    # Print results as JSON for Claude to parse
    print(json.dumps(results, indent=2))

    # Exit with appropriate code
    if not results["plugin_exists"] or not results["command_name_valid"]:
        sys.exit(1)

    if results["command_already_exists"] and not validate_only:
        sys.exit(2)  # Special code for "file exists"

    # Exit code 3 if plugin.json is missing (warning, not blocking)
    if not results["plugin_json_exists"]:
        sys.exit(3)  # Special code for "missing plugin.json"

    sys.exit(0)
