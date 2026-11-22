#!/usr/bin/env python3
"""Convert debate.json into the notes of the Obsidian vault (step 2).

Usage:
    python3 to_markdown.py               # writes the notes into vault/
    python3 to_markdown.py --overwrite   # rebuild: replaces the notes this script owns

vault/ exists from the start, empty, so that it can be opened in Obsidian before step 2.
The vault is built in steps: this script adds the six folders below (step 2).
The agent adds entities/, topics/ and index.md (step 4), then fallacies/ (step 8).

Notes written (all from the structured data, no LLM):
    speeches/   one note per intervention (spoken, blue-card question or answer, chair, written statement)
    debates/    the debate note, with the ordered list of interventions
    people/     one note per speaker
    groups/     one note per EP political group
    parties/    one note per national party
    countries/  one note per speaker's country

Naming rules (same as AGENTS.md):
    people      full name from the MEP database, Latin script; transcript spellings go in aliases
    groups      EP label, "/" replaced by "-"                      e.g. PPE, Verts-ALE
    parties     "<label> (<ISO alpha-3 country code>)", "/" -> "-"  e.g. PS (FRA), TB-LNNK (LVA)
    countries   English short name, ISO code as alias               e.g. Spain (ESP)
    speeches    "<order> <speaker>" plus the kind when not a speech e.g. 227 Diego Solier (question)

Standard library only. Python 3.8 or later.
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

CONVERTER_FOLDERS = ["speeches", "debates", "people", "groups", "parties", "countries"]

# Labels that mean "no national party".
NOT_A_PARTY = {"independent", "independiente", "independente", "indépendant", "ind.", "sans parti", "parteilos"}

# How the chair is named in the transcript, in the languages of the Parliament.
CHAIR_WORDS = {
    "president", "presidente", "presidenta", "le président", "la présidente", "präsident", "präsidentin",
    "przewodniczący", "przewodnicząca", "priekšsēdētājs", "priekšsēdētāja", "voorzitter", "puhemies",
    "elnök", "πρόεδρος", "председател", "predsjednik", "predsjednica", "předseda", "předsedající",
    "predsedajúci", "predsedajúca", "pirmininkas", "pirmininkė", "talman", "formand", "eesistuja",
    "președinte", "președintele", "predsedujoči", "predsedujoča", "presidentti", "president-in-office",
}

FORBIDDEN_IN_FILE_NAMES = '\\/:*?"<>|#^[]'


def safe_name(name):
    """Make a string usable as an Obsidian file name and link target."""
    for ch in FORBIDDEN_IN_FILE_NAMES:
        name = name.replace(ch, "-")
    return " ".join(name.split()).strip(" .")


def yaml_value(value):
    """JSON is valid YAML: it quotes and escapes strings and lists safely."""
    return json.dumps(value, ensure_ascii=False)


def frontmatter(fields):
    lines = ["---"]
    for key, value in fields.items():
        if value is None or value == [] or value == "":
            continue
        lines.append(f"{key}: {yaml_value(value)}")
    lines.append("---")
    return "\n".join(lines)


def link(target, text=None):
    if text and text != target:
        return f"[[{target}|{text}]]"
    return f"[[{target}]]"


def is_chair(iv):
    name = (iv.get("speaker_name_in_transcript") or "").strip(" .").lower()
    return name in CHAIR_WORDS


def kind_of(iv):
    if iv["activity_type"] == "PLENARY_DEBATE_WRITTEN_STATEMENT":
        return "written"
    if iv["activity_type"] != "PLENARY_DEBATE_SPEECH":
        return "procedural"
    if iv["statement_type"] == "question":
        return "question"
    if iv["statement_type"] == "answer":
        return "answer"
    if is_chair(iv):
        return "chair"
    return "speech"


def person_name(iv):
    speaker = iv.get("speaker") or {}
    return speaker.get("full_name") or iv.get("speaker_name_in_transcript")


def group_file(group):
    return safe_name(group["label"])


def party_file(party, country):
    if party is None or party["label"].strip().lower() in NOT_A_PARTY:
        return None
    code = country["code"] if country else "XXX"
    return safe_name(f"{party['label']} ({code})")


def country_file(country):
    return safe_name(country["name"]) if country else None


def time_of(timestamp):
    return timestamp[11:19] if timestamp else None


def write(path, text, written):
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    written[path.parent.name] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source", default="debate.json", help="debate file (default: debate.json)")
    parser.add_argument("--vault", default="vault", help="vault folder (default: vault)")
    parser.add_argument("--overwrite", action="store_true",
                        help="replace existing notes in the folders this script writes (loses any enrichment)")
    args = parser.parse_args()

    source = Path(args.source)
    vault = Path(args.vault)
    data = json.loads(source.read_text(encoding="utf-8"))
    debate = data["debate"]
    sitting = data["sitting"]
    interventions = sorted(debate["interventions"], key=lambda iv: iv["order"])

    existing = [p for folder in CONVERTER_FOLDERS for p in (vault / folder).glob("*.md")]
    if existing and not args.overwrite:
        sys.exit(f"{len(existing)} notes already exist in {vault}/. "
                 "Run with --overwrite to rebuild them (this replaces any enrichment in those notes).")
    for folder in CONVERTER_FOLDERS:
        (vault / folder).mkdir(parents=True, exist_ok=True)
    if args.overwrite:
        for p in existing:
            p.unlink()

    debate_note = safe_name(debate["title"].replace(" (debate)", ""))
    written = defaultdict(int)

    # Collect people, groups, parties and countries from the speakers.
    people = {}
    groups = {}
    parties = {}
    countries = {}
    for iv in interventions:
        if kind_of(iv) == "procedural":
            continue
        speaker = iv.get("speaker") or {}
        name = safe_name(person_name(iv))
        person = people.setdefault(name, {
            "speaker": speaker, "aliases": set(), "roles": set(), "kinds": defaultdict(int),
        })
        transcript_name = iv.get("speaker_name_in_transcript")
        if transcript_name and transcript_name != speaker.get("full_name") and not is_chair(iv):
            person["aliases"].add(transcript_name)
        kind = kind_of(iv)
        person["kinds"][kind] += 1
        if kind == "chair":
            person["roles"].add("chair of the sitting")
        elif not speaker.get("political_group") and iv.get("speaker_role_in_transcript"):
            person["roles"].add(iv["speaker_role_in_transcript"])
        group = speaker.get("political_group")
        country = speaker.get("nationality")
        party = speaker.get("national_party")
        if group:
            groups[group_file(group)] = group
        if country:
            countries[country_file(country)] = country
        pfile = party_file(party, country)
        if pfile:
            entry = parties.setdefault(pfile, {"party": party, "country": country, "groups": set()})
            if group:
                entry["groups"].add(group_file(group))

    # File name of each intervention note.
    note_of = {}
    for iv in interventions:
        kind = kind_of(iv)
        if kind == "procedural":
            continue
        suffix = "" if kind == "speech" else f" ({kind})"
        note_of[iv["order"]] = safe_name(f"{iv['order']} {person_name(iv)}{suffix}")

    # Blue cards: a question is put to the author of the last speech before it; an answer replies to the last question.
    asked_about = {}
    replies_to = {}
    last_speech = None
    last_question = None
    for iv in interventions:
        kind = kind_of(iv)
        if kind == "speech":
            last_speech = iv
        elif kind == "question":
            last_question = iv
            if last_speech:
                asked_about[iv["order"]] = last_speech
        elif kind == "answer" and last_question:
            replies_to[iv["order"]] = last_question

    # Who chairs when: the chair at the start, then each "PRÉSIDENCE: ..." line.
    chair_changes = [iv for iv in interventions if iv["activity_type"] == "MEETING_NAME_CHAIR"]

    # Speech notes.
    for iv in interventions:
        kind = kind_of(iv)
        if kind == "procedural":
            continue
        speaker = iv.get("speaker") or {}
        group = speaker.get("political_group")
        country = speaker.get("nationality")
        pfile = party_file(speaker.get("national_party"), country)
        name = safe_name(person_name(iv))
        languages = sorted({p["lang"] for p in iv.get("paragraphs", []) if p.get("lang")}) or [iv["text_source"]]

        fields = {
            "type": "intervention",
            "kind": kind,
            "speech_id": iv["speech_id"],
            "order": iv["order"],
            "debate_id": debate["id"],
            "date": sitting["date"],
            "start_time": time_of(iv.get("start_time")),
            "end_time": time_of(iv.get("end_time")),
            "speaker": name,
            "speaker_label": iv.get("speaker_label"),
            "group": group_file(group) if group else None,
            "party": pfile,
            "country": country_file(country),
            "on_behalf_of_group": iv.get("on_behalf_of_group"),
            "language": languages[0] if len(languages) == 1 else languages,
            "words": len(iv["text"].split()),
        }
        header = [f"Speaker: {link(name)}"]
        if group:
            header.append(f"Group: {link(group_file(group))}")
        if pfile:
            header.append(f"Party: {link(pfile)}")
        if country:
            header.append(f"Country: {link(country_file(country))}")
        if not group and iv.get("speaker_role_in_transcript"):
            header.append(f"Role: {iv['speaker_role_in_transcript']}")
        lines = [frontmatter(fields), "", " · ".join(header), f"Debate: {link(debate_note)}"]
        if iv["order"] in asked_about:
            target = asked_about[iv["order"]]
            lines.append(f"Blue-card question on: {link(note_of[target['order']])}")
        if iv["order"] in replies_to:
            lines.append(f"Replies to: {link(note_of[replies_to[iv['order']]['order']])}")
        if kind == "written":
            lines.append("Written statement (Rule 178): not spoken in the chamber.")
        lines += ["", f"# {note_of[iv['order']]}", ""]
        if iv.get("speaker_label"):
            lines += [f"> {iv['speaker_label']}", ""]
        lines += ["## Text", ""]
        lines += [p["text"] + "\n" for p in iv.get("paragraphs", [])] or [iv["text"]]
        write(vault / "speeches" / f"{note_of[iv['order']]}.md", "\n".join(lines), written)

    # Debate note.
    stats = debate.get("stats", {})
    lines = [frontmatter({
        "type": "debate",
        "debate_id": debate["id"],
        "date": sitting["date"],
        "title": debate["title"],
        "url": debate["url"],
        "sitting_url": sitting["url"],
        "interventions": stats.get("interventions"),
        "words": stats.get("words"),
        "aliases": [debate["title"]],
    }), "", f"# {debate_note}", "", f"Source: {debate['url']}", "", "## Interventions", ""]
    for iv in interventions:
        kind = kind_of(iv)
        if kind == "procedural":
            lines.append(f"- {iv['order']}. *{' '.join(iv['text'].split())}*")
            continue
        speaker = iv.get("speaker") or {}
        group = speaker.get("political_group")
        detail = group_file(group) if group else (iv.get("speaker_role_in_transcript") or "")
        if kind != "speech":
            detail = f"{detail}, {kind}" if detail else kind
        lines.append(f"- {iv['order']}. {link(note_of[iv['order']])} ({detail})")
    if chair_changes:
        lines += ["", "## Chair", ""]
        first_chair = next((iv for iv in interventions if kind_of(iv) == "chair"), None)
        if first_chair:
            lines.append(f"- From the start: {link(safe_name(person_name(first_chair)))}")
        for iv in chair_changes:
            announced = " ".join(iv["text"].split())
            chair = next((n for n in people if n.upper() in announced.upper()), None)
            lines.append(f"- From {iv['order']}: {link(chair) if chair else ''} *{announced}*")
    write(vault / "debates" / f"{debate_note}.md", "\n".join(lines), written)

    # People notes.
    for name, person in sorted(people.items()):
        speaker = person["speaker"]
        group = speaker.get("political_group")
        country = speaker.get("nationality")
        pfile = party_file(speaker.get("national_party"), country)
        fields = {
            "type": "person",
            "person_id": speaker.get("person_id"),
            "first_name": speaker.get("first_name"),
            "last_name": speaker.get("last_name"),
            "gender": speaker.get("gender"),
            "mep": bool(speaker.get("is_mep_on_date")),
            "group": group_file(group) if group else None,
            "party": pfile,
            "country": country_file(country),
            "roles": sorted(person["roles"]),
            "aliases": sorted(person["aliases"]),
        }
        header = []
        if group:
            header.append(f"Group: {link(group_file(group))}")
        if pfile:
            header.append(f"Party: {link(pfile)}")
        if country:
            header.append(f"Country: {link(country_file(country))}")
        counts = ", ".join(f"{k}: {n}" for k, n in sorted(person["kinds"].items()))
        lines = [frontmatter(fields), ""]
        if header:
            lines += [" · ".join(header), ""]
        lines += [f"# {name}", ""]
        if person["roles"]:
            lines += [f"Role in this debate: {', '.join(sorted(person['roles']))}.", ""]
        lines.append(f"Interventions in this debate: {counts}.")
        write(vault / "people" / f"{name}.md", "\n".join(lines), written)

    # Group notes.
    for gfile, group in sorted(groups.items()):
        aliases = [a for a in {group["label"], group["name"]} if a != gfile]
        lines = [frontmatter({
            "type": "group", "group_id": group["id"], "label": group["label"], "name": group["name"],
            "aliases": sorted(aliases),
        }), "", f"# {gfile}", "", f"{group['name']}: political group of the European Parliament."]
        write(vault / "groups" / f"{gfile}.md", "\n".join(lines), written)

    # Party notes.
    for pfile, entry in sorted(parties.items()):
        party, country = entry["party"], entry["country"]
        aliases = [a for a in {party["label"], party["name"]} if a and a != pfile]
        header = [f"Country: {link(country_file(country))}"] if country else []
        header += [f"Group: {link(g)}" for g in sorted(entry["groups"])]
        lines = [frontmatter({
            "type": "party", "party_id": party["id"], "label": party["label"], "name": party["name"],
            "country": country_file(country), "aliases": sorted(aliases),
        }), "", " · ".join(header), "", f"# {pfile}", "", f"National party: {party['name']}."]
        write(vault / "parties" / f"{pfile}.md", "\n".join(lines), written)

    # Country notes.
    for cfile, country in sorted(countries.items()):
        lines = [frontmatter({"type": "country", "code": country["code"], "aliases": [country["code"]]}),
                 "", f"# {cfile}"]
        write(vault / "countries" / f"{cfile}.md", "\n".join(lines), written)

    print(f"Notes written in {vault}/:")
    for folder in CONVERTER_FOLDERS:
        print(f"  {folder + '/':<12} {written[folder]}")
    kinds = defaultdict(int)
    for iv in interventions:
        kinds[kind_of(iv)] += 1
    print("Interventions: " + ", ".join(f"{n} {k}" for k, n in sorted(kinds.items())) +
          " (procedural lines appear in the debate note only)")


if __name__ == "__main__":
    main()
