# AGENTS.md: LLM wiki of European Parliament debates

You maintain an Obsidian wiki (`vault/`) built from European Parliament plenary debates on migration, one source file per debate:

* `debate_ceuta.json`: *The recent hybrid attacks and instrumentalisation of migrants in Ceuta and the need for a coordinated response to protect the EU's external borders*, 15 September 2026, added first;
* `debate_return_regulation.json`: *Common system for the return of third-country nationals staying illegally in the Union (Return Regulation)*, 16 June 2026, added in step 9.

Follow these rules exactly. When a case is not covered, stop and ask the user. Don't invent a convention.

## 1. Files

| Path | Role | You may |
|---|---|---|
| `debate_*.json` | the sources: one debate per file, extracted from the dataset | read only |
| `fallacy_detection_codebook.md` | fallacy codebook, used in step 8 only | read only |
| `to_markdown.py` | the converter that wrote the step-2 notes | run only when asked |
| `vault/` | the wiki | read and write |

Vault folders:

| Folder | Notes | Created by |
|---|---|---|
| `speeches/` | one note per intervention | converter |
| `debates/` | one note per debate | converter |
| `people/` | speakers; people mentioned in speeches | converter; you, for people mentioned |
| `groups/` | the 9 EP political groups | converter |
| `parties/` | national parties of the speakers | converter |
| `countries/` | speakers' countries; countries mentioned | converter; you, for countries mentioned |
| `entities/` | organisations, places, laws and agreements, events | you |
| `topics/` | the topics of section 5 | you |
| `fallacies/` | one note per code of the fallacy codebook | you, in step 8 |

`index.md` lists all notes. `log.md` records what you did.

## 2. What you must not change

* The text of a speech, in the original language.
* The step-2 frontmatter fields, and the header line `Speaker: … · Group: … · Party: …`.
* Anything in the `debate_*.json` files.
* Don't create, rename or delete group or party notes. All of them exist.
* Don't infer a speaker's group, party or country from the text: the data gives them.
* Don't write backlinks. Obsidian computes them.

## 3. Naming rules

Every entity has one note, and every link uses that note's file name. Other spellings go in the note's `aliases` and in the link's display text:

* `[[Frontex]]`
* `[[Morocco|Marruecos]]`
* `[[PPE|EPP Group]]`

Never write a link to a name that is not a file name in the vault: an unresolved link is an error. If the entity has no note, create the note first (section 4).

**People.**
* File name = `full_name` from the data, in Latin script. Aliases = the transcript names, e.g. `Loucas Fourlas` with alias `Λουκάς Φουρλάς`, or `Emil Radev` with alias `Емил Радев`.
* For people mentioned but not in the data: the usual full name in English, in Latin script (e.g. `Pedro Sánchez`), with `role` in the frontmatter.

**The chair.**
* "President", "Presidente", "Le Président", "Madam President", "Mr President" addressed to the chair mean the person chairing at that moment, not the President of the Parliament.
* The `## Chair` section of each debate note says who chairs from the start, and from which `order` another chair takes over. For a speech, the chair is the last one listed before its `order`.
* Ceuta debate: Antonella Sberna up to `order` 219, Younous Omarjee from `order` 220. Return Regulation debate: Javi López.
* When a speaker names another president ("President von der Leyen", "President Metsola"), link that person.

**EP political groups.** File names and aliases:

| File name | Aliases |
|---|---|
| `PPE` | Group of the European People's Party (Christian Democrats), EPP, EPP Group, European People's Party, Partido Popular Europeo |
| `S&D` | Group of the Progressive Alliance of Socialists and Democrats in the European Parliament, Socialists and Democrats, S&D Group |
| `PfE` | Patriots for Europe, Patriots |
| `ECR` | European Conservatives and Reformists, ECR Group |
| `Renew` | Renew Europe |
| `Verts-ALE` | The Greens/European Free Alliance, Greens/EFA, Verts/ALE, the Greens |
| `The Left` | The Left - GUE/NGL, GUE/NGL, The Left group |
| `ESN` | Europe of Sovereign Nations, Sovereignists |
| `NI` | Non-attached Members, non-inscrits |

Don't confuse a group with a national party:
* `PPE` (*Partido Popular Europeo*) is the EP group;
* `PP` is the Spanish national party, `PP (ESP)`.

**National parties.**
* File name = `<label> (<ISO 3166 alpha-3 country code>)`, with `/` replaced by `-`. E.g. `PS (FRA)`, `PS (PRT)`, `PS (SVK)`, `TB-LNNK (LVA)`.
* The same label in two countries is two parties.
* `Independiente`, `Independent`, `Ind.` and `Sans parti` are not parties: no note, no link.

**Countries.**
* File name = the English short name (`Spain`, `Morocco`).
* Aliases = the ISO alpha-3 code and the names used in the speeches (`ESP`, `España`, `Espagne`; `MAR`, `Marruecos`, `Maroc`).

**Other entities.** Use the name the organisation or law uses for itself in English. Use these names when they appear:

| File name | Aliases (examples) |
|---|---|
| `Frontex` | European Border and Coast Guard Agency |
| `European Commission` | the Commission, Comisión Europea |
| `Council of the European Union` | the Council, Consejo |
| `Pact on Migration and Asylum` | the Pact, el Pacto, le pacte |
| `Schengen Borders Code` | Código de Fronteras Schengen |
| `Schengen Area` | Schengen |
| `Ceuta` | Θέουτα, Сеута |
| `Melilla` | |
| `Government of Spain` | the Spanish government, Gobierno de España |

## 4. Entity extraction

For each speech note, read the original text (any language) and extract the entities that are **named** in it:

| Type | Folder | Examples |
|---|---|---|
| person | `people/` | Pedro Sánchez, Ursula von der Leyen |
| country | `countries/` | Morocco, Belarus, Russia |
| organisation | `entities/` | Frontex, European Commission, Government of Spain |
| place | `entities/` | Ceuta, Melilla, Lampedusa |
| law or agreement | `entities/` | Pact on Migration and Asylum, Schengen Borders Code |
| event | `entities/` | e.g. a named earlier crisis |

Don't extract:
* salutations: "Madam President, Commissioner, colleagues" are not mentions;
* generic words: migrants, the borders, Europe used as a general idea;
* the speaker's own group or party when it appears only in the speaker label.

Before creating a note:
1. Search the file names and the `aliases` in `people/`, `countries/`, `entities/`, `groups/` and `parties/`.
2. If one matches, link it, and add the new spelling to its `aliases` if it's not there.
3. If nothing matches, create the note with this template, then link it:

```markdown
---
type: person | country | organisation | place | law | event
aliases: []
---
# <File name>

<One sentence saying what this is.>
```

## 5. Topics

Closed list. File names are exact. Don't create other topic notes: write proposals in `topics_proposed.md`, at the workshop root, with one example speech each.

| Topic note | What it covers |
|---|---|
| `Instrumentalisation of migration` | migrants used by a state as a means of pressure; hybrid attacks |
| `External border protection` | controls, fences, surveillance, Frontex, border management |
| `EU-Morocco relations` | Morocco's role, cooperation, agreements, pressure on Morocco |
| `Schengen and internal border controls` | free movement, reintroduced internal border controls |
| `Solidarity between Member States` | burden sharing, help to Spain, relocation |
| `Pact on Migration and Asylum` | the Pact, its implementation, its crisis rules |
| `Returns` | return of people with no right to stay, return agreements |
| `Migrant smuggling` | smugglers, trafficking networks |
| `Humanitarian situation and victims` | deaths, injuries, reception conditions, unaccompanied minors, rights of migrants |
| `Regularisation of migrants` | Spain's regularisation scheme, pull factors |
| `Sovereignty of Ceuta and Melilla` | "Ceuta is Spain", territorial integrity |
| `Responsibility of the Spanish government` | criticism or defence of how the Spanish government handled the events |
| `Return hubs` | return centres in third countries, e.g. the Italian centre in Albania |
| `Detention of migrants` | detention before return, including families and children |
| `Majorities in Parliament` | who votes with whom, e.g. the PPE and the groups to its right |

The last three topics were added with the Return Regulation debate (step 9).

A speech gets a topic only if it says something about it, not if it merely uses a word.

## 6. What to add to each speech note

Add these fields to the frontmatter, as plain values without links:

```yaml
position: supports | opposes | mixed | not_stated
topics: [External border protection, EU-Morocco relations]
```

Append these sections after the text:

```markdown
## Summary
<2–3 sentences in English: what the speaker says, and to whom if it is a blue-card question or answer.>

## Position
- Question: <the question of this speech's debate, from the table below>
- Position: supports | opposes | mixed | not stated
- Justification: <one sentence>
- Quote: "<≤ 25 words, original language>" (translation by the agent: "<English>")

## Entities
- [[<File name>|<name as written in the speech>]]

## Topics
- [[<Topic note>]]
```

The question of each debate:

| Debate | Question |
|---|---|
| Ceuta (15 September 2026) | Should the EU respond to the events in Ceuta mainly by strengthening the protection of its external borders? |
| Return Regulation (16 June 2026) | Should Parliament adopt the Return Regulation in the version put to the vote? |

The summary, justification and translations are yours. Mark translations as "translation by the agent", because the dataset has no official translation.

* **Blue-card questions and answers:** the summary says who asks whom, and what. If the exchange doesn't address the question, the position is `not_stated`.
* **Chair interventions and procedural notes:** a one-line summary, no Position section, links only to entities named in them.
* **Written statements:** enrich them like speeches. They weren't spoken in the chamber.

## 7. Workflow

* Enrich notes in debate order (`order`), in batches of about 20. The user says which batch.
* Before a batch, list the existing notes and aliases in `people/`, `countries/`, `entities/` and `topics/`.
* Don't modify notes outside the batch, except to add aliases to entity notes.
* After a batch:
  * append to `vault/log.md`: date, debate, batch (first and last `order`), notes enriched, entity notes created, entity notes reused;
  * report the same in the chat.

## 8. Lint

When the user asks for a lint, report first and fix nothing. List:

1. unresolved links;
2. orphan notes;
3. entity notes that are the same entity (similar names or overlapping aliases);
4. topic links outside the list of section 5;
5. speech notes missing a section of section 6;
6. for 10 random speech notes, the entity links whose entity is not named in the text.

Fix only what the user approves. To merge duplicates:
* keep the canonical file name;
* move the other name to `aliases`;
* update every link;
* delete the duplicate note;
* append the changes to `log.md`.

## 9. Synthesis pages

When the user asks for the synthesis:

* **Each topic note:** add `## Positions by group`, with one short paragraph per group whose speakers addressed the topic, citing speeches from every debate that addressed it. Then add `## Speeches`, the list of speech notes linked to the topic, by debate.
* **Each group note:** add `## In the debates`, with one subsection per debate and the main points its speakers made.
* **Each debate note:** add `## Overview` (5 sentences) and `## Main lines of division`.
* **`index.md`:** every note, by folder, with a one-line description.

Every claim in a synthesis links to at least one speech note that supports it. Never write a claim without a link.

## 10. Query mode

When the user asks a question about the debates:

* Don't modify any file.
* Start from `index.md`, follow the links, and read the speech notes.
* Answer only from the vault. Cite the speech notes as `[[…]]`, and quote the original text with its translation.
* If the vault doesn't contain the answer, say "Not in the vault." Don't fill gaps from general knowledge.

## 11. Fallacy labelling (step 8)

Only when the user asks for it:

* Use only the codes of `fallacy_detection_codebook.md`, with its rules and its output format. "None" is a valid answer.
* Judge only the text of the speech (its `## Text` section). Ignore the speaker's name, group, party and country, and the other sections of the note (summary, position, entities, topics).
* Work in batches of about 20 notes, in debate order, as in section 7.
* Create the notes in `fallacies/` as the codebook says, the first time a code is used.
* Don't change anything else in the speech notes.

## 12. Adding a debate (step 9)

When the user has run `to_markdown.py` on a new debate file:

1. Read the new speech notes. Propose the question for the table of section 6, the topics to add to section 5 (with one example speech each) and any rule that doesn't fit this debate, such as the chair. Wait for the user's decision before changing this file.
2. Enrich the new speech notes as in sections 4 to 7, in batches of about 20. Many people, groups, parties and entities already have notes: link them, don't create new ones, and add new spellings to their `aliases`.
3. If the converter reported a person whose group changed, leave the person's note as it is: each speech note gives the group on the day of the speech.
4. Update the pages that already exist, as in section 9: the topic notes, the group notes, the entity notes and `index.md`. Add the new debate next to what is there; don't remove or rewrite what came from the earlier debates.
5. Run the lint of section 8, and report.
