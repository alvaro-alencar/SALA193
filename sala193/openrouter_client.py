"""OpenRouter HTTP client for structured SALA193 character decisions.

Uses Python's standard library for network requests. Never writes API keys,
prompts or response payloads to diagnostic output.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from sala193.models import ActionType


ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterError(RuntimeError):
    """A configuration, transport, provider or structured output error."""


def action_schema() -> dict:
    """Simple strict JSON schema, compatible with supported OpenRouter providers."""
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "actor": {"type": "string"},
            "target": {"type": ["string", "null"]},
            "action_type": {"type": "string", "enum": [a.value for a in ActionType]},
            "visible_intention": {"type": "string"},
            "hidden_intention": {"type": "string"},
            "intensity": {"type": "number"},
            "risk": {"type": "number"},
            "emotional_tone": {"type": "string"},
            "dialogue": {"type": "string"},
        },
        "required": [
            "actor", "target", "action_type", "visible_intention",
            "hidden_intention", "intensity", "risk", "emotional_tone", "dialogue",
        ],
    }


@dataclass
class OpenRouterClient:
    model: str
    api_key: str | None = None
    timeout_seconds: float = 45.0
    max_tokens: int = 400

    def __post_init__(self) -> None:
        self.api_key = self.api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise OpenRouterError(
                "OPENROUTER_API_KEY não configurada. Veja docs/openrouter.md."
            )
        if not self.model or not self.model.strip():
            raise OpenRouterError("Defina OPENROUTER_MODEL ou --model.")
        if self.max_tokens < 100 or self.timeout_seconds <= 0:
            raise OpenRouterError("max_tokens deve ser >= 100 e timeout deve ser positivo.")

    def complete_json(self, prompt: str) -> dict:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Você interpreta uma pessoa comum num RPG de convivência. "
                        "Responda EXCLUSIVAMENTE com um objeto JSON válido conforme o schema. "
                        "Todos os textos de ação e diálogo devem estar em português brasileiro. "
                        "Não mencione países, estados-nação, história ou inspirações ocultas. "
                        "O diálogo deve ser uma fala humana curta, natural e específica."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "sala193_action",
                    "strict": True,
                    "schema": action_schema(),
                },
            },
            "provider": {"require_parameters": True},
            "temperature": 0.8,
            "max_tokens": self.max_tokens,
        }
        request = Request(
            ENDPOINT,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-Title": "SALA193",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                answer = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            # Do not echo provider response or headers; avoid exposing secrets.
            raise OpenRouterError(
                f"OpenRouter retornou HTTP {exc.code}. Confira chave, créditos, "
                "modelo e suporte a JSON Schema."
            ) from None
        except (URLError, TimeoutError, OSError) as exc:
            raise OpenRouterError("Falha de conexão ou timeout ao consultar OpenRouter.") from exc
        except (UnicodeError, ValueError) as exc:
            raise OpenRouterError("OpenRouter retornou uma resposta HTTP inválida.") from exc

        try:
            message = answer["choices"][0]["message"]
            if message.get("refusal"):
                raise OpenRouterError("O modelo recusou gerar a ação.")
            content = message["content"]
            if not isinstance(content, str):
                raise ValueError("Conteúdo não textual")
            parsed = json.loads(content)
            if not isinstance(parsed, dict):
                raise ValueError("Objeto JSON esperado")
            return parsed
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise OpenRouterError(
                "O modelo não retornou um objeto JSON válido. "
                "Verifique se o modelo selecionado suporta structured outputs."
            ) from exc
