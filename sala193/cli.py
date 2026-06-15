from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from sala193.agents import get_agent_adapter
from sala193.engine import SimulationEngine
from sala193.models import Character, Scenario, SimulationLog
from sala193.narrator import Narrator

app = typer.Typer(help="SALA193 simulation CLI")
console = Console()


@app.command()
def validate(character_file: Path) -> None:
    """Validate a character YAML file."""
    character = Character.from_yaml(character_file)
    console.print(Panel.fit(f"{character.public_name} validado com sucesso.", title="SALA193"))


@app.command()
def run(
    scenario_file: Path,
    characters_dir: Path = typer.Option(Path("examples/characters"), help="Directory containing character YAML files."),
    turns: int = typer.Option(5, help="Number of turns to simulate."),
    output_dir: Path = typer.Option(Path("logs/latest"), help="Directory to write logs."),
    adapter: str = typer.Option("rules", help="Agent adapter: rules or passive."),
) -> None:
    """Run a simulation scenario."""
    scenario = Scenario.from_yaml(scenario_file)
    characters = load_characters(characters_dir, scenario)
    agent_adapter = get_agent_adapter(adapter)

    engine = SimulationEngine(characters=characters, scenario=scenario, agent_adapter=agent_adapter)
    log = engine.run(turns=turns)

    output_dir.mkdir(parents=True, exist_ok=True)
    events_path = output_dir / "events.jsonl"
    drama_path = output_dir / "drama_log.md"
    scene_path = output_dir / f"scene_{scenario.pov}.md"

    narrator = Narrator(engine.characters)
    events_path.write_text(log.as_jsonl() + "\n", encoding="utf-8")
    drama_path.write_text(narrator.drama_log(log), encoding="utf-8")
    scene_path.write_text(narrator.scene(log, pov=scenario.pov), encoding="utf-8")

    console.print(Panel.fit(
        f"Simulação concluída com adapter '{agent_adapter.name}'.\n"
        f"Eventos: {events_path}\nDrama log: {drama_path}\nCena: {scene_path}",
        title="SALA193",
    ))


@app.command()
def scene(
    events_file: Path,
    characters_dir: Path = typer.Option(Path("examples/characters"), help="Directory containing character YAML files."),
    pov: str = typer.Option("joao", help="Point-of-view character id."),
) -> None:
    """Generate a scene from an events JSONL file."""
    characters = {character.id: character for character in load_all_characters(characters_dir)}
    events = []
    for line in events_file.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))

    log = SimulationLog(scenario_id="from_file", events=events)
    narrator = Narrator(characters)
    console.print(narrator.scene(log, pov=pov))


@app.command()
def inspect(
    scenario_file: Path,
    characters_dir: Path = typer.Option(Path("examples/characters"), help="Directory containing character YAML files."),
) -> None:
    """Print the hidden table setup for writers' room use."""
    scenario = Scenario.from_yaml(scenario_file)
    characters = load_characters(characters_dir, scenario)
    lines = [f"Cenário: {scenario.title}", "", "Personagens carregados:"]
    for character in characters:
        lines.append(
            f"- {character.public_name} ({character.id}) | inspiração privada: {character.private_inspiration or 'não definida'} | "
            f"âncora: {character.ordinary_life_anchor}"
        )
    console.print("\n".join(lines))


def load_characters(characters_dir: Path, scenario: Scenario) -> list[Character]:
    all_characters = {character.id: character for character in load_all_characters(characters_dir)}
    needed = {participant for frame in scenario.frames for participant in frame.participants}
    missing = sorted(needed - set(all_characters))
    if missing:
        raise typer.BadParameter(f"Missing character files for: {', '.join(missing)}")
    return [all_characters[character_id] for character_id in sorted(needed)]


def load_all_characters(characters_dir: Path) -> list[Character]:
    if not characters_dir.exists():
        raise typer.BadParameter(f"Characters directory not found: {characters_dir}")
    return [Character.from_yaml(path) for path in sorted(characters_dir.glob("*.yaml"))]


if __name__ == "__main__":
    app()
