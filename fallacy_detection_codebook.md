# Fallacy codebook (step 8)

Six fallacy codes and one control code, taken from a draft codebook (v0.1). The draft came from an exploratory pass on speeches of this dataset: these are the codes that were both frequent and the clearest to identify.

## Rules

1. Code the reasoning, not the tone or the political position. Persuasion and strong opinions are not fallacies.
2. Every positive must cite an exact span, name the conclusion that the span is meant to support, and name the defect.
3. "None" is a valid and frequent answer.
4. Judge only the text of the speech (its `## Text` section). Ignore the speaker's name, group, party and country, even though the note shows them.

## Codes

| Code | What must be present |
|---|---|
| `AD_HOMINEM` | A claim or position is rejected **because of** an attack on the character, motives, identity or affiliation of a person or group, instead of on the argument. An insult alone, with no argument being rejected, is not enough. |
| `STRAW_MAN` | The speaker attributes to an identifiable opponent a position they did not hold, or an exaggerated version of it, **and then rebuts that version**. |
| `FALSE_DILEMMA` | Only two options are presented as exhaustive when obvious alternatives exist, **and** the choice is used to support a conclusion. |
| `SLIPPERY_SLOPE` | A measure is opposed because it will set off a chain of increasingly bad consequences, with the intermediate steps asserted rather than supported. |
| `FALSE_CAUSE` | A causal link is asserted from mere sequence or correlation, or a single cause is given for an outcome with several causes, and the conclusion depends on it. |
| `HASTY_GENERALIZATION` | A general claim is drawn **from one or a few cases cited in the text**. A sweeping claim with no cited case is not this code: use `UNSUPPORTED_ASSERTION`. |

## Control code

`UNSUPPORTED_ASSERTION`: a strong claim stated without support. It is **not counted as a fallacy**. It exists so that sweeping claims are not labelled `HASTY_GENERALIZATION` by default.

## Not coded

Rhetorical devices without a defect in the reasoning: rhetorical questions, repetition, lists of three, slogans, sarcasm, vivid imagery, and emotional tone next to an argument.

## Output format

In each speech note, add the codes found to the frontmatter, as plain values:

```yaml
fallacies: [STRAW_MAN, UNSUPPORTED_ASSERTION]
```

Then append this section after the text, with one item per instance:

```markdown
## Fallacies

- [[STRAW_MAN]] (clear | borderline)
  - Quote: "<exact words from the text>" (translation by the agent: "<English>")
  - Conclusion: <the conclusion the quote supports>
  - Defect: <what is wrong with the reasoning>
```

When the speech has none: `fallacies: []` in the frontmatter, and `None.` under `## Fallacies`.

## Fallacy notes

One note per code in `vault/fallacies/`, named after the code (`STRAW_MAN.md`), with the code's definition from this file. The note `UNSUPPORTED_ASSERTION.md` says that it is a control code, not a fallacy.
