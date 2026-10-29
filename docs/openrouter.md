# SALA193 + OpenRouter

## Criar a chave

Acesse https://openrouter.ai/settings/keys e crie uma chave com limite de gastos.
Não cole a chave em mensagens, issues, commits ou arquivos públicos.

## Configuração

Na raiz do projeto, usando Windows PowerShell:

~~~powershell
Copy-Item .env.example .env
notepad .env
~~~

Linux/macOS:

~~~bash
cp .env.example .env
nano .env
~~~

Preencha o arquivo local .env:

~~~dotenv
OPENROUTER_API_KEY=cole_sua_chave_localmente
OPENROUTER_MODEL=openai/gpt-4o-mini
~~~

O arquivo .env está no .gitignore. Nunca faça commit da chave.
Em hospedagem, configure OPENROUTER_API_KEY nos segredos do servidor.

## Instalação

~~~bash
pip install -e ".[dev]"
~~~

## Testar com João e Samuel

~~~bash
sala193 run examples/scenarios/first_room.yaml --turns 2 --adapter openrouter
~~~

Serão até quatro chamadas à API (dois personagens × dois turnos).
Para selecionar outro modelo:

~~~bash
sala193 run examples/scenarios/first_room.yaml --turns 2 --adapter openrouter --model openai/gpt-4o-mini
~~~

Os arquivos gerados são:
- logs/latest/events.jsonl (eventos estruturados)
- logs/latest/drama_log.md (resumo)
- logs/latest/scene_joao.md (narração com as falas)

## Falhas da API

Por padrão a execução é interrompida se a IA falhar, sem fingir que uma ação por regras veio do modelo.

Para permitir uma decisão determinística substituta com aviso:

~~~bash
sala193 run examples/scenarios/first_room.yaml --turns 2 --adapter openrouter --fallback-rules
~~~

## Custos e privacidade

- Cada personagem ativo faz uma chamada por turno.
- 193 personagens × 10 turnos podem resultar em até 1.930 chamadas se todos estiverem ativos.
- Inicie com dois personagens e um ou dois turnos. A CLI limita execuções individuais a 20 turnos.
- Use modelos e endpoints compatíveis com JSON Schema structured outputs.
- As fichas enviadas para tomada de decisão não revelam o país de inspiração nem as memórias privadas dos demais personagens.
- A memória atualmente dura uma execução; persistência entre sessões está planejada.
- Defina limites de gasto na chave e monitore o painel do OpenRouter.

## Referências

https://openrouter.ai/docs/api/reference/overview
https://openrouter.ai/docs/guides/features/structured-outputs


## Executar no GitHub (sem instalar nada localmente)

1. Abra Settings → Secrets and variables → Actions no repositório.
2. Clique em New repository secret.
3. Use exatamente o nome OPENROUTER_API_KEY e cole sua chave.
4. Abra Actions → SALA193 - Simular com IA → Run workflow.
5. Escolha 1 ou 2 turnos e um modelo compatível com JSON Schema.
6. Depois da execução, baixe o artifact sala193-cenas, que contém a cena e os registros.

Links diretos:
- https://github.com/alvaro-alencar/SALA193/settings/secrets/actions
- https://github.com/alvaro-alencar/SALA193/actions/workflows/simulate.yml

O segredo não é revelado no repositório público. Não escreva a chave em variáveis públicas, inputs do workflow, mensagens ou código.
O workflow não roda sozinho: apenas quando acionado manualmente.
