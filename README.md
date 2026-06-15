# SALA193

SALA193 é um experimento narrativo e computacional: um ambiente simulado onde 193 agentes de IA convivem como personagens autônomos, cada um com personalidade, memória, interesses, traumas e relações próprias.

A camada histórica existe como DNA psicológico dos personagens, não como explicação direta. O leitor/espectador não deve perceber que está vendo uma transposição de relações entre países. Deve ver uma série de convivência: cenas, alianças, conflitos, afetos, disputas, conversas e consequências.

## Premissa

Em vez de narrar a História como mapa, tratado ou linha do tempo, SALA193 transforma organismos políticos em personagens humanos. A simulação não chama os personagens por nomes de países. Eles têm nomes próprios, biografias próprias e conflitos próprios.

O narrador principal é João: uma personificação literária do Brasil, mas sem dizer isso ao leitor. João não sabe que carrega essa dimensão. Ele apenas observa, sente, tenta conciliar, erra, improvisa, se envolve e conta o que viu.

## A ideia em uma frase

SALA193 é uma mesa de RPG social onde personagens são controlados por agentes, consequências são arbitradas por um mestre e os acontecimentos viram cena literária.

## Arquitetura atual

```text
Ficha do personagem
        ↓
AgentAdapter escolhe ação
        ↓
GameMaster resolve consequência
        ↓
Rules executam teste dramático
        ↓
Memória e relações mudam
        ↓
Narrator escreve cena
```

## Princípio narrativo

A simulação não deve produzir relatórios geopolíticos. Deve produzir dramaturgia.

Errado:

> Samuel representa os Estados Unidos e tenta aumentar sua influência.

Certo:

> Samuel chega ao bar sorrindo demais, oferece pagar a conta de todo mundo e, antes da meia-noite, metade da mesa já está devendo favor a ele.

## Regra de ouro

Os personagens nunca sabem que são países. O leitor também não precisa saber. A camada histórica é o organismo oculto da ficção.

## Rodando localmente

```bash
git clone https://github.com/alvaro-alencar/SALA193.git
cd SALA193
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell
pip install -e .[dev]
pytest
sala193 run examples/scenarios/first_room.yaml --turns 4 --adapter rules
```

## Estrutura

```text
SALA193/
  docs/
    requirements.md
    specs.md
    character_model.md
    simulation_loop.md
    narrative_rules.md
    rpg_architecture.md
    quickstart.md
  sala193/
    __init__.py
    models.py
    actions.py
    agents.py
    rules.py
    gamemaster.py
    engine.py
    memory.py
    narrator.py
    cli.py
  examples/
    characters/
      joao.yaml
      samuel.yaml
    scenarios/
      first_room.yaml
  tests/
```

## Status

MVP em evolução.

O projeto já possui:

- fichas YAML;
- engine de turnos;
- adapter determinístico;
- Game Master;
- teste dramático determinístico;
- memória e relações;
- narrador em story mode;
- CLI básica;
- testes iniciais.

Próximo passo: adicionar `LLMAgentAdapter` para que personagens proponham ações por IA mantendo saída estruturada.

## Licença

A definir.
