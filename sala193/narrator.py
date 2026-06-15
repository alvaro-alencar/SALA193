from __future__ import annotations

from sala193.models import Character, SimulationEvent, SimulationLog


FORBIDDEN_STORY_TERMS = {
    "country",
    "nation",
    "government",
    "geopolitics",
    "border",
    "colony",
    "empire",
    "gdp",
    "sanction",
    "treaty",
    "military alliance",
    "world war",
    "united nations",
}


class Narrator:
    def __init__(self, characters: dict[str, Character]):
        self.characters = characters

    def drama_log(self, log: SimulationLog) -> str:
        lines = [f"# Drama log — {log.scenario_id}", ""]
        for event in log.events:
            actor = self._name(event.actor)
            target = self._name(event.target) if event.target else "ninguém"
            lines.append(f"- **Turno {event.turn}**: {actor} → {target}: {event.outcome}")
            if event.future_hooks:
                for hook in event.future_hooks:
                    lines.append(f"  - Gancho: {hook}")
        return "\n".join(lines).strip() + "\n"

    def scene(self, log: SimulationLog, pov: str = "joao") -> str:
        pov_character = self.characters.get(pov)
        narrator_name = pov_character.public_name if pov_character else "João"

        lines = [
            f"Meu nome é {narrator_name}.",
            "",
            "Tem noite que começa pequena e termina morando dentro da gente.",
            "",
        ]

        for event in log.events:
            lines.extend(self._event_to_scene_lines(event, narrator_name))
            lines.append("")

        lines.append("Eu não entendi tudo naquela hora. A gente quase nunca entende.")
        lines.append("Só percebi que, depois daquela noite, ninguém sentou do mesmo jeito na mesa.")

        prose = "\n".join(lines).strip() + "\n"
        self._guard_story_mode(prose)
        return prose

    def _event_to_scene_lines(self, event: SimulationEvent, narrator_name: str) -> list[str]:
        actor = self._name(event.actor)
        target = self._name(event.target) if event.target else None

        if event.action_type.value == "offer" and target:
            return [
                f"{actor} chegou sorrindo como quem já tinha decidido alguma coisa antes de entrar.",
                f"Nem esperou {target} terminar a frase. Puxou a carteira, pagou o que havia para pagar e ainda deixou o recibo bem no meio da mesa.",
                "Foi um gesto bonito, se a gente olhasse de longe.",
                "De perto, tinha peso.",
            ]

        if event.action_type.value == "talk":
            return [
                f"{actor} falou baixo, quase manso.",
                "Mas conversa mansa também empurra móveis dentro da cabeça da gente.",
                "Todo mundo respondeu com palavras simples. Ninguém disse o que queria dizer.",
            ]

        if event.action_type.value == "refuse" and target:
            return [
                f"{actor} recusou antes da proposta terminar de nascer.",
                f"{target} ficou parado, com aquela cara de quem não sabe se foi ofendido ou poupado.",
                "A mesa continuou igual. Só o ar mudou de dono.",
            ]

        if event.action_type.value == "threaten" and target:
            return [
                f"{actor} não levantou a voz.",
                "Esse foi o pior detalhe.",
                f"Olhou para {target} e deixou a frase cair devagar, pesada o bastante para ninguém fingir que não ouviu.",
            ]

        if event.action_type.value == "leave":
            return [
                f"{actor} riu, fez uma piada torta e foi saindo.",
                "Ninguém segurou.",
                "Às vezes a gente deixa a pessoa ir embora só para não admitir que queria uma resposta.",
            ]

        return [
            f"{actor} fez alguma coisa pequena por fora e grande por dentro.",
            event.outcome,
        ]

    def _name(self, character_id: str | None) -> str:
        if not character_id:
            return "alguém"
        character = self.characters.get(character_id)
        return character.public_name if character else character_id

    def _guard_story_mode(self, text: str) -> None:
        lowered = text.lower()
        leaked = sorted(term for term in FORBIDDEN_STORY_TERMS if term in lowered)
        if leaked:
            raise ValueError(f"story mode leaked forbidden terms: {', '.join(leaked)}")
