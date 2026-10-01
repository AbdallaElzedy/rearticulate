# Rearticulate

A skill for Claude Code that rewrites your request into a structured prompt, shows you the rewrite, and then carries it out in the same turn.

Prompting guidance tends to live in documentation you read once and half remember. This packages it as something that runs. Type `/rearticulate fix the login bug` and the skill works out what a careful colleague would need to know before starting, writes that into a prompt with a stated role, the reason the task matters, the files it should treat as data rather than as instructions, and criteria it can check afterwards. Then it executes against that prompt.

The second half earns its place. A rewritten prompt you have to paste somewhere else is friction. This one is addressed to Claude itself, so the block on screen becomes the instruction set for the rest of the turn.

## Why the target model matters

Prompting advice is measured on particular models, and the measurements disagree with each other.

Opus 5 checks its own work, so instructing it to verify tends to buy a second pass that costs tokens and changes little. Sonnet 5 reads instructions literally and does not stretch them to neighbouring cases, so a rule meant to apply widely needs its scope written out. Fable 5 can decline a request that asks it to narrate its own reasoning. Opus 4.8 reaches for subagents less readily than its successors, so a prompt that wants delegation has to say so.

A skill that flattened those differences would hand the same prompt to each model. This one keeps a profile per family and chooses between them.

| Profile | Covers | Representative adjustment |
|---|---|---|
| `fable-5-1` | Fable 5.1, Mythos 5.1 | Asks for progress text between tool calls, and strips anti-formatting blocks inherited from older prompts |
| `fable-5` | Fable 5, Mythos 5 | Leaves out show-your-reasoning instructions, which can trigger a refusal category on this family |
| `opus-5` | Opus 5 | Omits the verification section and states response length outright |
| `sonnet-5` | Sonnet 5 | Spells out instruction scope, and drops sampling parameters that return a 400 |
| `opus-4-8` | Opus 4.8 | Encourages delegation, and notes the larger output budget at higher effort |
| `legacy-4x` | Opus 4.7, 4.6, 4.5, Sonnet 4.6, 4.5, Haiku 4.5, Mythos Preview | Applies the guide's inline notes, names the closest page, and records that the fit is by analogy |

The skill separates the model running the session from the model a prompt is written for. Those are usually the same, and differ when you are authoring a prompt for something else to consume.

A model mentioned in passing does not switch profiles. "Fix the test that Sonnet 5 wrote yesterday" keeps the session model as the target. "Rewrite this prompt for Sonnet 5" switches it.

## Installing

Clone into your personal skills directory:

```bash
git clone https://github.com/AbdallaElzedy/rearticulate.git ~/.claude/skills/rearticulate
```

On Windows PowerShell:

```powershell
git clone https://github.com/AbdallaElzedy/rearticulate.git "$env:USERPROFILE\.claude\skills\rearticulate"
```

To scope it to one repository instead, clone into that repository's `.claude/skills/` directory. Claude Code picks the skill up next session and `/rearticulate` becomes available. There is nothing to configure.

## Using it

```
/rearticulate fix the login bug
/rearticulate --model opus-5 write a system prompt for our support bot
/rearticulate --dry-run migrate the probe suite to the new CLI
```

Two flags are read from anywhere in the request and removed before the rewrite.

| Flag | Effect |
|---|---|
| `--model <alias>` | Writes the prompt for the named model rather than the session model. Takes `fable-5-1`, `fable-5`, `opus-5`, `sonnet-5`, `opus-4-8`, the 4.x names, and their `claude-` forms. |
| `--dry-run` | Stops after showing the prompt, with grafted blocks printed in full so you can take them elsewhere. Replying "run it" executes the prompt already shown. |

Phrasing works too. "Just rewrite the prompt" or "show me the prompt" reads as a dry run, while a prohibition inside the task itself, such as "build it but hold off on the tests", stays part of the task.

On screen you get one fenced block holding the prompt, then up to three short lines: the target model and how it was resolved, the assumptions that were made, and the wording that was changed. Anything inferred, stripped, or substituted gets recorded there, which is the part worth reading before you let it run.

## What a run does

| Step | Work |
|---|---|
| 1 | Resolves the session model and the target model, picks a request type, reads the files the request names, and flags steps with outside effects |
| 2 | Lists what a colleague with little context would ask, answers from the repository and the conversation, and settles routine ambiguity with a recorded assumption |
| 3 | Fills the template in fixed tag order with the sections that request type calls for |
| 4 | Converts phrasing current models handle poorly, including suggestion wording where action is wanted, capitalised emphasis, prohibitions with no reason attached, and prefill constructs |
| 5 | Prints the prompt and the assumption lines, with no preamble |
| 6 | Executes, batching independent tool calls, reading files before making claims about them, and pausing at the steps flagged in step 1 |
| 7 | Runs the checks it wrote, confirms the files touched are the ones the task named, and closes with a recap that reads on its own |

Steps 1 through 4 happen in thinking. Step 5 onward is what reaches you.

Questions are treated differently from instructions. "Can you suggest improvements to this file" with no other signal produces an assessment rather than edits, which is the behaviour the underlying guidance asks for.

## Repository layout

| Path | Lines | Contents |
|---|---|---|
| `SKILL.md` | 130 | The procedure, the model delta table, and the rules that stay in force for the session |
| `references/technique-catalog.md` | 3610 | The rules from the main guide, with the quote, the situation each applies to, and the step that uses it |
| `references/snippet-library.md` | 1303 | Sample prompts reproduced as published, with notes on which profiles should receive them |
| `references/models/` | 5181 | One file per profile: identity facts, behavioural entries, what to add, and what to take out |
| `references/model-notes.md` | 233 | The router. Aliases, the baseline chain between models, and cross-model API facts |
| `references/request-taxonomy.md` | 326 | Request types, the signals that select one, and the conversion list for weak phrasing |
| `templates/rearticulated-prompt.md` | 370 | Tag order, per-tag rules, model overlays, and the default blocks |
| `examples/rearticulations.md` | 877 | Nine worked rewrites, from a one-line bug fix through a long migration |

About 12,000 lines in total, of which `SKILL.md` is 130 by design. Claude Code holds an invoked skill in context and carries part of it through compaction, so the procedure lives in the short file while the detail waits in the references until a run reaches for it. The references are opened on stated triggers rather than up front.

Rule identifiers run through the whole set. `BP-nnn` points at the main guide in reading order, and `F51-`, `F5-`, `O5-`, `S5-` and `O48-` point at the model pages. If you want to know why the skill does something, follow the identifier to the quoted source.

## Where the guidance comes from

Six pages of Anthropic's documentation, captured on 8 September 2026.

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)
- [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
- [Prompting Claude Opus 4.8](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8)

Quoted blocks keep the published wording and punctuation. A few of them therefore read differently from this documentation, which is deliberate: a snippet that gets pasted into a prompt should match the text that was measured, not a tidied version of it.

Model behaviour moves between releases. The capture date above is the moment these notes describe, so check the current pages before leaning on a specific claim about a specific model.

## Scope and known gaps

Worth knowing before you rely on it.

The build ran two rounds of adversarial review out of three. The first raised 144 findings and the second brought that to roughly 50, with structural checks passing. A repair pass then applied 42 edits that a third round would have re-examined, so those particular fixes rest on one reading rather than an independent one. If you find something wrong in that neighbourhood, that is the likeliest reason.

The worked examples use generic subjects: a login bug, a report renderer, three business documents, a spoken summary, a probe migration, and three prompt-authoring requests. They were genericized from the environment the skill was built in, so a few file paths and tool names read as placeholders because that is what they are.

On behaviour that touches your machine: the skill reads files and edits the workspace without stopping to ask, and holds back on steps with outside reach. Pushing code, writing to shared systems, deleting, and sending messages belong to the second group and wait for you.

The procedure assumes Claude Code. The prompt-authoring path produces prompts for the API, while the skill itself leans on Claude Code features, among them skill loading, `${CLAUDE_SKILL_DIR}` substitution, and the permission model.

## Changing it

The parts most worth editing are the request taxonomy, where a row describes a kind of request and what it needs, and the examples, which the skill pattern-matches against when a row does not fit. Both are plain Markdown.

If you add a rule, give it an identifier and a source, because the audit trail is the reason the catalog is useful rather than merely long. If you add a snippet, record which profiles should receive it and which should not, since a snippet measured on one model is not evidence about another.

Issues and pull requests are welcome, particularly from anyone who has run it against a model the profiles cover thinly.
