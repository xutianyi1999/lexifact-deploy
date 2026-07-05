#!/usr/bin/env python3

import subprocess
import re
import sys
import os
from pathlib import Path

try:
    import typer
    import dotenv
    from rich.console import Console
except ImportError:
    print("Missing dependencies. Install them:")
    print("  pip install typer rich python-dotenv")
    sys.exit(1)

app = typer.Typer()
console = Console()
ROOT = Path(__file__).resolve().parent.parent
COMPOSE = ROOT / "docker-compose.yml"

if not COMPOSE.exists():
    console.print(f"[red]{COMPOSE} not found. Run from project root.[/red]")
    sys.exit(1)

COMPOSE_TEXT = COMPOSE.read_text()


def _detected_required_vars() -> list[str]:
    return re.findall(r"\$\{(\w+):\?", COMPOSE_TEXT)


def compose(*args: str):
    result = subprocess.run(["docker", "compose", "-f", str(COMPOSE), *args])
    if result.returncode != 0:
        raise typer.Exit(abs(result.returncode) or 1)


def _check_all() -> bool:
    ok = True

    result = subprocess.run(["docker", "info"], capture_output=True, text=True)
    if result.returncode != 0:
        console.print(f"  [red]✗ Docker daemon[/red]  — {result.stderr.strip()}")
        ok = False
    else:
        console.print("  [green]✓ Docker daemon[/green]")

    missing = [v for v in _detected_required_vars() if not os.environ.get(v)]
    if missing:
        for v in missing:
            console.print(f"  [red]✗ {v}[/red]")
        ok = False
    else:
        console.print("  [green]✓ Environment variables[/green]")

    return ok


def get_var_doc(name: str) -> str:
    m = re.search(rf"\${{{re.escape(name)}:\?(.+?)}}", COMPOSE_TEXT)
    return m.group(1) if m else ""


@app.command()
def up():
    """Start all services (docker compose up -d)."""
    env_path = ROOT / ".env"
    if env_path.exists():
        dotenv.load_dotenv(env_path)
    else:
        console.print(
            "[yellow].env not found — env vars from environment only[/yellow]"
        )

    console.print("[bold]Preflight checks[/bold]")
    if not _check_all():
        console.print("\n[red]Preflight failed. Fix issues above and try again.[/red]")
        raise typer.Exit(1)

    compose("pull")
    compose("up", "-d")


@app.command()
def down():
    """Stop and remove containers (docker compose down)."""
    compose("down")


@app.command()
def ps():
    """List container status (docker compose ps)."""
    compose("ps")


@app.command()
def logs(
    service: str = typer.Argument(None, help="Service name"),
    tail: int = typer.Option(50, help="Number of lines to show"),
    follow: bool = typer.Option(False, "-f", "--follow", help="Follow log output"),
):
    """View service logs (docker compose logs)."""
    cmd = ["logs", f"--tail={tail}"]
    if follow:
        cmd.append("-f")
    if service:
        cmd.append(service)
    compose(*cmd)


@app.command()
def pull():
    """Pull latest images from registry."""
    compose("pull")


@app.command()
def check():
    """Run preflight checks (Docker, env vars)."""
    env_path = ROOT / ".env"
    if env_path.exists():
        dotenv.load_dotenv(env_path)

    console.print("[bold]Preflight checks[/bold]")
    if not _check_all():
        console.print("\n[red]Some checks failed. Fix issues above.[/red]")
        raise typer.Exit(1)
    console.print("\n[green]All checks passed.[/green]")


@app.command()
def init():
    """Create ~/.lexifact/ data directory and .env template."""
    data_dir = Path.home() / ".lexifact"
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        console.print(f"[red]Cannot create {data_dir}. Check permissions.[/red]")
        raise typer.Exit(1)
    console.print(f"[green]Created {data_dir}[/green]")

    env_path = ROOT / ".env"
    if env_path.exists():
        console.print(f"[yellow]{env_path} already exists, skipping.[/yellow]")
        return

    try:
        with env_path.open("w") as f:
            f.write("# LexiFact environment variables\n")
            f.write("# Fill in the values below.\n\n")
            for var in _detected_required_vars():
                doc = get_var_doc(var) or "Required"
                f.write(f"# {doc}\n{var}=\n\n")
    except OSError:
        console.print(f"[red]Failed to write {env_path}. Check permissions.[/red]")
        raise typer.Exit(1)

    console.print(f"[green]Created {env_path}. Edit it with your values.[/green]")


def main():
    app()


if __name__ == "__main__":
    main()
