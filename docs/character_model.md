# Character Model — SALA193

## 1. Philosophy

A SALA193 character is not a symbol with a human mask. A character is a person whose biography, instincts and relationships carry a hidden civilizational structure.

The model should create people who can live inside scenes without explaining themselves.

The reader must not think: "this is a country".

The reader should think: "I know someone like this".

## 2. Public vs private layers

Each character has two layers.

### Public layer

Visible in story mode:

- name;
- age band;
- voice;
- habits;
- relationships;
- memories;
- current emotional state;
- desires;
- fears;
- contradictions.

### Private layer

Visible only in analysis mode:

- country inspiration;
- historical compression notes;
- archetypal design;
- forbidden direct references;
- symbolic traps to avoid.

## 3. Anti-allegory rule

Never make a character perform a national stereotype as a costume.

Bad:

> João plays football, dances samba and loves beaches because he is Brazil.

Better:

> João avoids ending conversations badly. He would rather leave with a joke than win with a wound.

The second version creates behavior, not decoration.

## 4. Character dimensions

### Identity

- `id`
- `public_name`
- `private_inspiration`
- `age_band`
- `social_position`
- `ordinary_life_anchor`

The ordinary life anchor is crucial. It keeps the character grounded in a realistic dimension.

Examples:

- bar owner;
- mechanic;
- teacher;
- nurse;
- debt collector;
- retired soldier;
- shopkeeper;
- musician;
- lawyer;
- delivery rider;
- landlord;
- tenant;
- union organizer;
- police officer;
- local celebrity.

### Temperament

Values from 0.0 to 1.0:

- openness;
- discipline;
- sociability;
- aggression;
- suspicion;
- ambition;
- patience;
- shame_sensitivity;
- risk_tolerance;
- loyalty;
- pride;
- mercy.

### Drives

- needs;
- fears;
- ambitions;
- addictions;
- recurring mistakes;
- forbidden desires.

### Wounds

Wounds are not exposition. They are behavior engines.

Examples:

- abandoned by a protector;
- humiliated in public;
- exploited by a mentor;
- betrayed by a sibling;
- survived scarcity;
- caused harm and cannot admit it;
- lives under inherited guilt.

### Resources

Values from 0.0 to 1.0:

- money;
- social_capital;
- coercive_power;
- institutional_access;
- cultural_influence;
- technical_skill;
- family_network;
- information;
- mobility;
- resilience.

### Moral boundaries

Values from 0.0 to 1.0 indicate likelihood of crossing a line under pressure.

- lie;
- betray;
- abandon;
- humiliate;
- exploit;
- threaten;
- injure;
- kill.

## 5. Relationship model

Every relationship is directional.

João's trust in Samuel may not equal Samuel's trust in João.

Dimensions:

- trust;
- fear;
- admiration;
- resentment;
- debt;
- intimacy;
- dependency;
- rivalry;
- attraction;
- guilt;
- protectiveness.

## 6. Memory model

Each memory entry should include:

- event id;
- summary;
- participants;
- emotional impact;
- interpretation;
- confidence;
- secrecy;
- tags.

Example:

```yaml
- event_id: e_0017
  summary: Samuel paid João's debt before João could refuse.
  participants: [joao, samuel]
  emotional_impact:
    gratitude: 0.42
    humiliation: 0.38
    suspicion: 0.21
  interpretation: "He helped me, but he made sure everyone saw."
  confidence: 0.86
  secrecy: public
  tags: [debt, favor, public_pressure]
```

## 7. João initial design

João is the first narrator candidate.

He must not be a caricature of Brazil.

He should be:

- observant;
- socially intelligent;
- allergic to final ruptures;
- capable of warmth and evasion;
- more improvisational than strategic;
- wounded by underestimation;
- seduced by recognition;
- ashamed of his own unfinishedness;
- able to survive chaos without fully solving it.

Possible ordinary anchor:

João runs or frequents a modest neighborhood bar, not as a metaphor for diplomacy, but because bars naturally generate scenes, conversations, debts, favors, gossip and conflict.

## 8. Samuel initial design

Samuel is not "the United States" inside the story.

He should be:

- energetic;
- productive;
- restless;
- persuasive;
- protective in a controlling way;
- allergic to weakness;
- generous when admired;
- dangerous when afraid;
- haunted by dependency;
- convinced that his help is usually necessary.

Possible ordinary anchor:

Samuel owns a growing logistics/security/business operation in the neighborhood. He is useful, rich, fast, admired and feared.

## 9. Naming policy

Names should feel ordinary in Portuguese narrative, but culturally plausible for each character's hidden inspiration.

Do not overcode names.

Bad:

- Uncle Sam
- João Brasil
- Ivan Russo
- Claire Révolution

Better:

- João
- Samuel
- Arthur
- Claire
- Ivan
- Liang
- Amara
- Mateo
- Hana
- Elias

## 10. Design test

A character is approved only if a scene with them works even when the reader has no idea about the hidden inspiration.
