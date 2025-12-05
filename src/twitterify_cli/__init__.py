"""Twitter-Init-Kit CLI Tool - Main Entry Point"""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

__version__ = "0.1.0"

app = typer.Typer(
    help="twitterify - Twitter marketing toolkit powered by spec-driven development"
)
console = Console()


@app.command()
def init(
    project_name: Optional[str] = typer.Argument(
        None,
        help="Project name or '.' for current directory",
    ),
    ai: Optional[str] = typer.Option(
        None,
        "--ai",
        help="AI assistant: claude, cursor, windsurf, gemini, copilot, etc.",
    ),
    script: Optional[str] = typer.Option(
        "sh",
        "--script",
        help="Script variant: sh (bash/zsh) or ps (PowerShell)",
    ),
    here: bool = typer.Option(
        False,
        "--here",
        help="Initialize in current directory",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force initialization in non-empty directory",
    ),
    no_git: bool = typer.Option(
        False,
        "--no-git",
        help="Skip git repository initialization",
    ),
    ignore_agent_tools: bool = typer.Option(
        False,
        "--ignore-agent-tools",
        help="Skip AI agent tool checks",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug output",
    ),
) -> None:
    """Initialize a new twitter-init-kit project."""

    if debug:
        console.print("[yellow]Debug mode enabled[/yellow]")

    # Determine target directory
    if here:
        target_dir = Path.cwd()
    elif project_name:
        target_dir = Path.cwd() / project_name if project_name != "." else Path.cwd()
    else:
        console.print("[red]Error: Project name required (or use --here)[/red]")
        raise typer.Exit(1)

    # Check if directory exists and has content
    if target_dir.exists() and any(target_dir.iterdir()) and not force:
        console.print(
            f"[yellow]Directory {target_dir} is not empty.[/yellow]\n"
            f"Use --force to override, or --here to use current directory."
        )
        raise typer.Exit(1)

    # Create directory
    target_dir.mkdir(parents=True, exist_ok=True)

    # Display success message
    console.print(
        Panel(
            f"[green]✓ Project initialized at {target_dir}[/green]\n\n"
            f"Next steps:\n"
            f"1. cd {target_dir}\n"
            f"2. Run your AI agent (claude, cursor, windsurf, etc.)\n"
            f"3. Use /twitterkit.constitution to define project principles\n"
            f"4. Use /twitterkit.specify to create your Twitter spec\n"
            f"5. Use /twitterkit.plan to generate your growth plan\n"
            f"6. Use /twitterkit.tasks to break down execution\n"
            f"7. Use /twitterkit.implement to execute tasks",
            title="[bold blue]twitter-init-kit[/bold blue]",
        )
    )


@app.command()
def check(
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug output",
    ),
) -> None:
    """Check for installed required tools."""

    if debug:
        console.print("[yellow]Debug mode enabled[/yellow]")

    tools_found = []
    tools_missing = []

    # Check for git
    result = __check_tool("git", "--version")
    if result:
        tools_found.append("git")
    else:
        tools_missing.append("git")

    # Check for AI agents
    agents_to_check = {
        "claude": "claude --version",
        "cursor-agent": "cursor-agent --version",
        "windsurf": "windsurf --version",
        "gemini": "gemini --version",
    }

    for agent, cmd in agents_to_check.items():
        # Simplified check - in real implementation, would use proper command
        pass

    # Display results
    console.print("\n[bold]System Check Results:[/bold]\n")

    if tools_found:
        console.print("[green]✓ Found:[/green]")
        for tool in tools_found:
            console.print(f"  • {tool}")

    if tools_missing:
        console.print(f"\n[yellow]⚠ Missing (optional):[/yellow]")
        for tool in tools_missing:
            console.print(f"  • {tool}")

    console.print("\n[cyan]For more info, visit: https://docs.claude.com/claude-code[/cyan]")


def __check_tool(tool: str, args: str) -> bool:
    """Check if a tool is installed."""
    import subprocess

    try:
        subprocess.run(
            f"{tool} {args}",
            shell=True,
            capture_output=True,
            timeout=5,
        )
        return True
    except Exception:
        return False


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
