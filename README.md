# Workshop: build an LLM wiki from a European Parliament debate

In this workshop you turn one plenary debate of the European Parliament into a wiki you can explore in Obsidian. You work with an AI agent called OpenCode: you tell it what to do in plain English, and it reads and writes the files for you. You don't need to know how to code.

Over the steps you will:

* turn the debate's data into notes, one per speech;
* write the rules (`AGENTS.md`) that the agent follows to find people, organisations and topics in the speeches and to link them;
* check what the agent produced, and fix the rules;
* explore the graph of the debate;
* ask questions to a chatbot that answers from your wiki;
* look for fallacies in the speeches.

At each step you make a decision and you check the result. The agent does the typing; whether the result is right is up to you.

## What's in this folder

| File or folder | What it is |
|---|---|
| `README.md` | this guide |
| `debate.json` | the debate: every speech, with its speaker, in the original language |
| `to_markdown.py` | a script (a small program) that turns `debate.json` into notes |
| `to_markdown_prompt.txt` | the prompt that produced `to_markdown.py` |
| `AGENTS.md` | the rules for the agent; you complete it in step 3 |
| `fallacy_detection_codebook.md` | the definitions of the fallacies, for step 8 |
| `vault/` | your wiki, created in step 2 by `to_markdown.py`, then enriched step by step. In Obsidian a folder of notes is called a *vault* |

## Background

See this [google doc](https://docs.google.com/document/d/1kyh_6LW9K6OEcO5lZqVCwW1l18DS5xxk5iCHgooDEIk/edit?tab=t.0)

### European Parliament plenary debates

* **MEPs.** The European Parliament has 720 Members (MEPs), elected in the 27 member states in June 2024 for the 10th parliamentary term (2024–2029).
* **Political groups.** MEPs sit by political group, not by country. The data uses the Parliament's own labels: `PPE`, `S&D`, `PfE`, `ECR`, `Renew`, `Verts/ALE`, `The Left`, `ESN`, and `NI` for non-attached Members. Each MEP is also a member of a national party.
* **Sittings.** The plenary meets in Strasbourg every month except August, for four days (Monday to Thursday), with additional sessions in Brussels. Each day is a *sitting*.
* **Debates.** Each sitting has an agenda of debates, votes and procedural items. Many debates open with statements by the Council (the minister of the country holding the rotating presidency, the "President-in-Office") and by the Commission. MEPs then speak, one speaker per group first. The President of Parliament or a Vice-President chairs, and the chair can change during a debate.
* **Blue cards.** During a speech, an MEP can raise a blue card to ask the speaker a question of up to 30 seconds, if the speaker agrees. The questioner may then add a short reaction. Blue cards are where MEPs from different groups address each other directly.
* **Languages.** MEPs speak in any of the EU's 24 official languages, with live interpretation. The official transcript, the *verbatim report of proceedings* (CRE, from the French *compte rendu in extenso*), keeps each speech in the language it was given in, without translation. A single debate is therefore written in many languages.

### The dataset

The data comes from the Parliament's public data service (its Open Data API). It was collected for this course by giving an AI coding agent a one-page description of what to build:

* repository: <https://github.com/SkatAI/eu-parliament-verbatim>
* the description given to the agent: [`docs/specs.md`](https://github.com/SkatAI/eu-parliament-verbatim/blob/main/docs/specs.md)
* the data: [`data/`](https://github.com/SkatAI/eu-parliament-verbatim/tree/main/data), 20 sitting days from 18 May to 8 October 2026, one file per day

The data has three levels:

| Level | Example |
|---|---|
| Sitting day | 15 September 2026 |
| Debate (agenda item) | the Ceuta debate |
| Intervention | a speech, a blue-card question or answer, a written statement |

`debate.json` holds one debate of that dataset.

### The debate

| | |
|---|---|
| Title | The recent hybrid attacks and instrumentalisation of migrants in Ceuta and the need for a coordinated response to protect the EU's external borders |
| Date | Tuesday 15 September 2026, 13:09–14:58 |
| Source page | https://www.europarl.europa.eu/doceo/document/CRE-10-2026-09-15-ITM-007_EN.html |
| Interventions | 74 spoken, by 52 MEPs, Commissioner Magnus Brunner, Council minister Thomas Byrne and the two successive chairs (Antonella Sberna, then Younous Omarjee). Plus 7 written statements, which were not spoken in the chamber |
| Languages | 12; Spanish, English, Italian and French are the most frequent |
| Political groups | all 9 |
| Blue cards | 9 question → answer exchanges, all between different groups |

### Key notions

**Wiki.** A set of pages that link to each other, with one page per subject. Wikipedia is the best known. 

**LLM wiki.** A wiki that an LLM writes and maintains from a set of sources, following rules that you write. The idea was described by Andrej Karpathy in April 2026 ([LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)). It has three parts:

* the **sources**, which the LLM reads but never changes (`debate.json`);
* the **wiki**, the pages the LLM writes (`vault/`);
* the **rules**, a file that sets the structure and the conventions (`AGENTS.md`).

A chatbot that searches documents goes back to the raw text for every question. An LLM wiki does the work once and keeps it as pages you can read, check and correct. The risk is that a mistake made while writing is kept and linked too. That's why you check.

**Graph.** A set of points (nodes) connected by lines (edges). In Obsidian each note is a node and each link is an edge.

**Obsidian.** A free note-taking app. It works on plain text files in a folder on your computer: there is no database, and other programs (like OpenCode) can read and write the same files. It shows links, backlinks, the metadata of each note (*properties*) and the graph.

**Markdown.** A way of writing formatted text in a plain text file: `# Title`, `**bold**`, `- list item`. Notes are markdown files (`.md`). A link to another note is written `[[Note name]]`, or `[[Note name|text shown]]`.

**YAML frontmatter.** A block of fields at the top of a note, between two `---` lines, one `field: value` per line. It holds data about the note (who speaks, which group, which language). Obsidian shows it as the note's properties.

```yaml
---
speaker: "Lena Düpont"
group: "PPE"
language: "de"
---
```

**JSON.** A text format for structured data, used by `debate.json`. It's made of named fields (`"title": "..."`) and lists (`[ ... ]`).

**AGENTS.md.** A file of instructions that OpenCode reads automatically every time you open this folder. It's how you give the agent rules that last for the whole project, instead of repeating them in every request.

## Setup

1. **Download this repository.** On GitHub, click *Code → Download ZIP*, then unzip it. Put the folder somewhere easy to find, e.g. your Documents.
2. **Install OpenCode.** Download the desktop app from <https://opencode.ai/download> and install it.
3. **Connect the model.** Follow your teacher's instructions to connect OpenCode to the model you'll use (in OpenCode, the `/connect` command). Or choose on of the free models that are made available in Opencode.
4. **Open the folder in OpenCode.** Open the unzipped folder as a project. OpenCode now reads `AGENTS.md` by itself.
5. **Install Obsidian.** Download it from <https://obsidian.md/download> and install it. You'll open the vault in step 2.
6. **Check Python.** The script needs Python 3, which is already installed on most computers. In OpenCode, type:

   > Check that python3 is installed on this computer, and tell me its version.

   If it isn't installed, ask OpenCode how to install it.

Note : installing python may take some time or face hurdles. If after a few minutes this is becoming a problem, just unzip the solution output file : vault_solution.zip . 

### Working with OpenCode

* You type a request in plain English. The agent reads files, runs commands and writes files, and tells you what it did.
* OpenCode has two agents, and the Tab key switches between them:
  * **Build** can change files;
  * **Plan** can only read and answer.

  Use Plan when you only want to look or ask (steps 1 and 7).
* A *session* is one conversation. A new session starts with no memory of the previous one, but `AGENTS.md` is always loaded.
* Read what the agent says it did. If something looks wrong, say so: "You created two notes. Merge them."

## Step 1. Explore the data

1. **Ask the agent to explain the data.** In OpenCode, with the **Plan** agent, type:

   > Explain the structure of debate.json in simple terms: what are its main parts, and what does one intervention contain? Show me the intervention with order 210 as an example.

2. **Compare with the official transcript.** Open the source page of the debate (link in the table above) and find the speech of Jeroen Lenaers. It should match intervention 210.
4. **Find the three levels** in what the agent showed you: sitting, debate, intervention. Which fields give the speaker's name, group, party and country? Which field gives the original language?

## Step 2. Turn the data into notes

> `to_markdown.py` turns `debate.json` into markdown notes. It was written by an AI agent from the prompt below. Read the prompt: it shows how precise you need to be to get what you want.
> The prompt that produced `to_markdown.py` is available in the file `to_markdown_prompt.txt`

1. Start by asking Opencode what the script `to_markdown.py` does ?

2. **Run the script.** In OpenCode, with the **Build** agent, type:

   > Run the  `to_markdown.py` script and tell me how many notes were written in each folder.
   > If python is not installed ask me if I want to install it 

   You should get:

   | Folder | Notes |
   |---|---|
   | `speeches/` | 81 (74 spoken interventions, 7 written statements) |
   | `debates/` | 1 |
   | `people/` | 63 |
   | `groups/` | 9 |
   | `parties/` | 46 |
   | `countries/` | 17 |


> At this point **do not trust that the markdown files were created**. Since the agent, opencode, has read this README file it knows what asnwer it should produce. Never trust, always check.

2. **Open the vault in Obsidian.** Choose *Open folder as vault* and select the `vault` folder inside this project. Open the graph view (Cmd+G on Mac, Ctrl+G on Windows) and take a screenshot: you will compare it with the enriched graph in step 6.
3. **Check the notes:**
   * Open 3 speech notes and compare them with the source page.
   * Open the note `Konstantinos Arvanitis`: what is in its `aliases`, and why?
   * Open `PS (FRA)`, `PS (PRT)` and `PS (SVK)`: why three notes and not one?
   * Open the debate note: when does the chair change?
4. **Discuss the script's choices.** The script made decisions for you:
   * the written statements(*) get notes, even though they were not spoken;
   * the chair's short interventions get notes too.

   Would you make the same choices? If not, ask OpenCode to change the script, then run it again with `--overwrite`.

  > (*) Note: the 7 written statements at the end of the debate. These are texts that MEPs submitted in writing instead of speaking. The verbatim report prints them after the debate, under the heading "Déclarations écrites (article 178)" (order 284 in debate.json), with authors such as Rihards Kols and Loucas Fourlas. Nobody said them in the chamber, so nobody heard them and no one could reply with a blue card. The script still gives each one a note in speeches/, like a spoken intervention, named for example 287 Loucas Fourlas (written) and marked kind: "written". That's why there are 81 speech notes and not 74.


## Step 3. Write the rules: AGENTS.md

This is the main design work. `AGENTS.md` already contains the parts that don't change. You complete the parts marked **TODO**.

1. **Read 5 speeches in Obsidian,** from different groups and in different languages. Note which people, organisations, places and laws they name, and what they talk about.
2. **Complete each TODO.** Write your decisions in plain English. You can edit `AGENTS.md` yourself in a plain text editor (TextEdit on Mac, Notepad on Windows), or tell OpenCode what to write:

   > In AGENTS.md, section 5, replace the TODO with this list of topics: … Keep my wording.

   The TODOs ask you to decide:
   * the other names of each political group (EPP, Greens/EFA, Patriots for Europe…);
   * how to name people, parties, countries and other entities;
   * who "Madam President" is (the chair changes during the debate);
   * which entities to extract, and which not to (e.g. the greeting "Madam President, Commissioner…" that opens every speech);
   * a closed list of 8–12 topics, with a one-line definition each;
   * what the agent adds to each speech note: summary, the speaker's position on the debate's question, links to entities and topics;
   * how the agent works in batches, checks its work, and answers questions.
3. **Save a copy of your first version.** Type:

   > Copy AGENTS.md to AGENTS.v1.md.

## Step 4. Enrich the notes and check

1. **Try your rules on 5 notes.** Type:

   > Following AGENTS.md, enrich the speech notes 210 to 214.

2. **Check these 5 notes against the text,** using this table:

   | Check | Yes / No | Example |
   |---|---|---|
   | Every linked entity is named in the speech | | |
   | No entity was missed | | |
   | No entity has two notes (e.g. `Frontex` and `FRONTEX`) | | |
   | Every link uses the note's file name | | |
   | Every topic is in your list | | |
   | The summary and position match the speech | | |

3. **Fix the rules.** Change `AGENTS.md` where the result was wrong, and write down what you changed and why. Then enrich all the notes, one batch at a time:

   > Following AGENTS.md, enrich the speech notes 207 to 226.

   Then do the same for 227 to 246, then 247 to 266, then 267 to 291. Check a few notes after each batch.

4. **Ask for a health check (a "lint").** Type:

   > Run the lint described in AGENTS.md. Report only, don't fix anything yet.

   Read the report, then ask for the fixes you agree with, e.g. "Merge the duplicate notes listed in point 3."

5. **Ask for the synthesis pages.** Type:

   > Write the synthesis pages described in AGENTS.md.

   These are the pages that summarise the positions by topic and by group. They are what make the vault a wiki and not only a set of linked notes. Check that every claim links to a speech that supports it.

## Step 5. Navigate the wiki in Obsidian

* Open a group note, e.g. `PfE`, and look at its **backlinks** (right sidebar): which speeches link to it?
* Open a topic note: which speeches, from which groups?
* Look at the **properties** of a speech note: speaker, group, position, topics.
* Optional: create a table of all speeches with their group and position, with the core plugin *Bases* (Obsidian help: <https://help.obsidian.md/bases>).

## Step 6. Explore the graph

1. **Open the graph view** (Cmd+G on Mac, Ctrl+G on Windows).
2. **Colour the notes by folder.** In the graph settings, open *Groups* and click *New group*. Write `path:speeches` and choose a colour. Do the same for `path:people`, `path:groups`, `path:parties`, `path:countries`, `path:entities` and `path:topics`. These colours remain distinct for colourblind readers:

   | Colour | Code | Colour | Code |
   |---|---|---|---|
   | orange | `#E69F00` | sky blue | `#56B4E9` |
   | green | `#009E73` | yellow | `#F0E442` |
   | blue | `#0072B2` | vermilion | `#D55E00` |
   | purple | `#CC79A7` | | |

3. **See what the LLM added.** Compare the graph with your screenshot from step 2.
4. **Open the local graph of a topic.** Open the topic note, click the *⋯* menu, then *Open local graph*, with depth 2. Which groups and MEPs connect to it?
5. **Answer one question from the graph, then check it in the notes.** For example:
   * Which entities are mentioned by one group only?
   * Which topics connect speakers from opposing groups?
   * Who replied to whom in the blue-card exchanges?

## Step 7. Ask questions to a chatbot

1. **Start a new session in OpenCode and choose the Plan agent,** which can't change files.
2. **Write 5 questions whose answers you know** from steps 5 and 6:
   * a factual question;
   * a comparison between groups;
   * a question about a blue-card exchange;
   * a question about a topic;
   * a question whose answer is not in the vault.
3. **Ask each one like this:**

   > Answer only from the notes in vault/, following the query rules in AGENTS.md: <your question>

4. **Score each answer:**

   | Question | Correct? | Cited notes exist and support the answer? | For the last question: did it say the answer isn't in the vault? |
   |---|---|---|---|
   | | | | |

## Step 8. Look for fallacies

`fallacy_detection_codebook.md` defines 6 fallacies: ad hominem, straw man, false dilemma, slippery slope, false cause, hasty generalisation. It also defines a control code for strong claims made without support, which is not a fallacy.

1. **Prepare the speeches without their authors.** Knowing the speaker or the group can bias the labels. In the workshop project (Build agent), type:

   > Create a folder named ceuta_blind next to this project folder (in its parent folder, not inside it). For each note in vault/speeches/, write a file <speech_id>.txt that contains only the text of the speech: no name, no group, no party, no country. Then copy fallacy_detection_codebook.md into ceuta_blind as AGENTS.md.

   The folder must be outside the project. Otherwise OpenCode would also load the project's `AGENTS.md`, which knows the speakers.

2. **Label the speeches.** Open the `ceuta_blind` folder as a new project in OpenCode, in a new session, and type:

   > Following AGENTS.md, label the fallacies in the first 20 files, in alphabetical order. Write the results in results.yaml.

3. **Compare with a classmate.** Two of you label the same 20 files, each in your own session. Then type:

   > Compare my results.yaml with my classmate's results_B.yaml. For each code, count the speeches labelled by both of us, by me only, and by my classmate only.

   Where you disagree, read the speech: who is right?

4. **Bring the labels into the wiki.** Back in the workshop project, type:

   > Read ../ceuta_blind/results.yaml. Find each speech in vault/speeches/ by its speech_id and add a "## Fallacies" section with the labels. Create one note per code in vault/fallacies/, with its definition from fallacy_detection_codebook.md, and link the labels to it.

5. **Look at the result in the graph:** fallacy notes, speeches, groups.

Be careful with what you conclude. With 3 to 12 speeches per group, no comparison between groups holds. An earlier test with one model, on 150 speeches of this dataset, found more fallacies in groups further from the centre. With one model, this can't be told apart from the model's own bias.

## What you hand in

* Your enriched vault (`vault/`) and your screenshot of the graph from step 2.
* `AGENTS.v1.md` and your final `AGENTS.md`, with what you changed between them and why.
* The step-4 checks, your 5 chatbot questions with their scores, and the fallacy comparison table.
