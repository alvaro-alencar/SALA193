# SALA193

SALA193 é um experimento narrativo e computacional: um ambiente simulado onde 193 agentes de IA convivem como personagens autônomos, cada um com personalidade, memória, interesses, traumas e relações próprias.

A camada histórica existe como DNA psicológico dos personagens, não como explicação direta. O leitor/espectador não deve perceber que está vendo uma transposição de relações entre países. Deve ver uma série de convivência: cenas, alianças, conflitos, afetos, disputas, conversas e consequências.

## Premissa

Em vez de narrar a História como mapa, tratado ou linha do tempo, SALA193 transforma organismos políticos em personagens humanos. A simulação não chama os personagens por nomes de países. Eles têm nomes próprios, biografias próprias e conflitos próprios.

O narrador principal é João: uma personificação literária do Brasil, mas sem dizer isso ao leitor. João não sabe que carrega essa dimensão. Ele apenas observa, sente, tenta conciliar, erra, improvisa, se envolve e conta o que viu.

## Objetivo

Criar uma engine mínima para:

1. definir fichas de personagens;
2. simular interações entre agentes;
3. manter memória e reputação;
4. gerar logs estruturados;
5. converter acontecimentos em cenas narrativas;
6. permitir ciclos longos de convivência emergente.

## Princípio narrativo

A simulação não deve produzir relatórios geopolíticos. Deve produzir dramaturgia.

Errado:

> Samuel representa os Estados Unidos e tenta aumentar sua influência.

Certo:

> Samuel chega ao bar sorrindo demais, oferece pagar a conta de todo mundo e, antes da meia-noite, metade da mesa já está devendo favor a ele.

## Regra de ouro

Os personagens nunca sabem que são países. O leitor também não precisa saber. A camada histórica é o organismo oculto da ficção.

## Status

Projeto em fundação.

Primeira etapa: requisitos, especificações e arquitetura mínima da simulação.

## Estrutura prevista

```text
SALA193/
  docs/
    requirements.md
    specs.md
    character_model.md
    simulation_loop.md
    narrative_rules.md
  sala193/
    __init__.py
    models.py
    engine.py
    memory.py
    narrator.py
  examples/
    characters/
      joao.yaml
      samuel.yaml
    scenarios/
      first_room.yaml
  tests/
```

## Licença

A definir.
