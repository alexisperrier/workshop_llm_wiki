# AGENTS.md: LLM wiki of the Ceuta debate

<!--This file tells the agent how to build and maintain the wiki. Some parts are already written. Fill in the parts marked **TODO** in step 3, then revise them after the checks of step 4. Keep your first version as `AGENTS.v1.md` before you revise it.

Write the rules as instructions to the agent: short, exact, with examples. The agent follows what is written, not what you meant.-->

You maintain an Obsidian wiki (`vault/`) built from one European Parliament plenary debate (`debate.json`): *The recent hybrid attacks and instrumentalisation of migrants in Ceuta and the need for a coordinated response to protect the EU's external borders*, 15 September 2026.

When a case is not covered by these rules, stop and ask the user. Don't invent a convention.

## 1. Files

| Path | Role | You may |
|---|---|---|
| `debate.json` | the source: one debate, extracted from the dataset | read only |
| `codebook.md` | fallacy codebook, used in step 8 only | read only |
| `to_markdown.py` | the converter that wrote the step-2 notes | run only when asked |
| `vault/` | the wiki | read and write |

Vault folders: `speeches/`, `debates/`, `people/`, `groups/`, `parties/`, `countries/`, `entities/`, `topics/`, `fallacies/`, plus `index.md`.

> **TODO**: for each folder, say what goes in it, and whether the converter or the agent creates its notes.

## 2. What you must not change

* The text of a speech, in the original language.
* Anything in `debate.json`.
* Don't write backlinks. Obsidian computes them.

> **TODO**: what else must the agent never change or create? Think of the step-2 fields and links, and of the group and party notes. Can the agent deduce a speaker's group from the text?

## 3. Naming rules

Every entity has one note, and every link uses that note's file name. Other spellings go in the note's `aliases` and in the link's display text, e.g. `[[PPE|EPP Group]]`.

Never write a link to a name that is not a file name in the vault: an unresolved link is an error.

**EP political groups.**

| File name | Aliases |
|---|---|
| `PPE` | Group of the European People's Party (Christian Democrats), EPP, EPP Group, European People's Party, Partido Popular Europeo |
| `S&D` | **TODO** |
| `PfE` | **TODO** |
| `ECR` | **TODO** |
| `Renew` | **TODO** |
| `Verts-ALE` | **TODO** |
| `The Left` | **TODO** |
| `ESN` | **TODO** |
| `NI` | **TODO** |

> **TODO**: write the rule for each of these, with an example from the debate.
>
> * **People:** which name is the file name, and which names go in `aliases`? What about people written in Greek or Cyrillic? What about people mentioned in a speech but not in the data?
> * **The chair:** who is "Madam President" or "Mr President"? The chair changes during the debate. Look for `PRÉSIDENCE` in `debate.json`.
> * **National parties:** `PS` is three different parties in this debate. How do you name them? What about `Independiente` or `Sans parti`?
> * **Countries:** which language for the file name? Which aliases?
> * **Other entities:** e.g. Frontex, the Pact on Migration and Asylum, Ceuta. Which name, which aliases?
> * **Group vs party:** how does the agent tell `PPE` (the EP group) from `PP` (the Spanish party)?

## 4. Entity extraction

The agent reads the original text of each speech, in any language.

> **TODO**:
>
> * Which types of entities does the agent extract (people, organisations, countries, places, laws, events…), and in which folder does each type go?
> * What does it NOT extract? Think of the "Madam President, Commissioner…" at the start of every speech, and of generic words like "migrants".
> * Write the procedure the agent follows before creating a note, so that it doesn't create duplicates.
> * Write the template of a new entity note (frontmatter fields, first line).

## 5. Topics

> **TODO**: read 5 speeches first. Then write a closed list of 8–12 topics, each with an exact file name and a one-line definition of what it covers.
>
> The agent must not create other topics. Where does it write its proposals for new ones?
>
> When does a speech get a topic: when it mentions a word, or when it says something about it?

| Topic note | What it covers |
|---|---|
| | |

## 6. What to add to each speech note

> **TODO**:
>
> * Which fields does the agent add to the frontmatter (as plain values, for filtering in Obsidian)?
> * Which sections does it append after the text, and in which order? Give the template.
> * Write the question of the debate that the speaker's position answers, and the allowed values (supports / opposes / mixed / not stated).
> * The dataset has no English translation. How should the agent quote the original text and mark its own translations?
> * What is different for blue-card questions and answers, for the chair's interventions, and for the written statements?

## 7. Workflow

> **TODO**:
>
> * In which order, and in batches of how many notes, does the agent work?
> * What does it check before each batch?
> * What does it report after each batch, and where (the chat, a `log.md` file)?

## 8. Lint

> **TODO**: what does the agent check when you ask for a lint? Does it fix things directly, or report first? How does it merge two notes about the same entity?

## 9. Synthesis pages

> **TODO**: what does the agent write on the topic notes, the group notes, the debate note and `index.md`? Which rule prevents claims that no speech supports?

## 10. Query mode (step 7)

> **TODO**: how does the agent answer a question about the debate? Where does it start, what may it use, how does it cite, and what does it say when the answer is not in the vault? May it modify files?
