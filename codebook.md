# Fallacy codebook (step 8)

Six fallacy codes and one control code, taken from a draft codebook (v0.1). The draft came from an exploratory pass on speeches of this dataset: these are the codes that were both frequent and the clearest to identify.

## Rules

1. Code the reasoning, not the tone or the political position. Persuasion and strong opinions are not fallacies.
2. Every positive must cite an exact span, name the conclusion that the span is meant to support, and name the defect.
3. "None" is a valid and frequent answer.
4. Label from the text only. You don't know who the speaker is, or which group or country they belong to.

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

One block per speech:

```yaml
speech_id: "<speech_id>"
fallacies:
  - code: <CODE>
    span_original: "<exact words from the text>"
    span_en: "<your English translation>"
    conclusion: "<the conclusion the span supports>"
    defect: "<what is wrong with the reasoning>"
    strength: clear        # clear | borderline
```

When the speech has none: `fallacies: []`.
