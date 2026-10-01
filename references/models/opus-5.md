# Claude Opus 5

Source page: Prompting Claude Opus 5, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 (snapshot 2026-09-08). The page's own description is the authoritative list of what it covers: "response verbosity, agentic narration, task scoping, subagent delegation, self-correction, and output artifacts when thinking is disabled" (O5-01). Guide rules that name Opus 5 come from Prompting best practices, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (snapshot 2026-09-08), and are listed at the end of section 3 with their BP IDs.

How to read this file. Everything on the page is measured on Claude Opus 5; a rule here is applied to another model only by analogy, and the Target model item of the assumptions says so. The cross-model technique catalog (`references/technique-catalog.md`) applies first; this file only adds or overrides (O5-03). Profile IDs `O5-nn` are the page's rules in page order. Section 4 and 5 govern the content of a rearticulated prompt whose target model is Opus 5; section 6 governs the skill's own behaviour when Opus 5 is the model running the skill. Those two dimensions are resolved separately in SKILL.md Step 1a.

## Identity and API facts

- Profile: `opus-5`. Aliases: opus-5, opus5, claude-opus-5. API string: `claude-opus-5` (BP-085; the guide's SDK samples pin this string and `max_tokens` explicitly, BP-059).
- Covered set: inside the guide's eleven current models (BP-002); the guide's model table row is BP-017.
- Baseline: `opus-4-8`. Page basis: "It performs well out of the box on existing Claude Opus 4.8 prompts." (O5-05). Inherited from the Opus 4.8 profile unless a section of this page covers the same topic: code review coverage language (o48_review_coverage, o48_review_concrete_bar), frontend and design variety (frontend_aesthetics_short, o48_propose_directions, o48_aefrm_concrete_spec), literal instruction following and explicit scope (o48_explicit_scope), and the effort-sweep advice. Superseded by this page: verification, subagent delegation, response verbosity, agentic narration, self-correction, thinking-disabled behaviour. When a borrowed snippet is grafted, the Target model item records "text measured on Prompting Claude Opus 4.8".
- Thinking: on by default when the `thinking` parameter is omitted (O5-60, BP-218). It can be disabled only at effort `high` or below (O5-06, O5-60, BP-219); the page does not print the disable syntax and routes it to the migration guide. Preferred setting when cost matters: thinking on at `low` effort, which "performs better than thinking disabled at similar cost" (O5-62, BP-227). With thinking disabled two artifacts can appear: tool calls written as text, and internal XML tags in the visible response (O5-61, O5-63, O5-65).
- `budget_tokens`: not accepted; the guide states a 400 on Claude 4.7 and later (BP-189). Convert to adaptive thinking plus `output_config.effort` and record the change.
- Sampling parameters (`temperature`, `top_p`, `top_k`): not printed on this page. The Opus 4.8 page routes "sampling parameters" to the Opus 4.7 to Opus 5 migration guide (O48-05, O48-06), so the skill flags any sampling parameter in a raw request for Opus 5 as "check against the Opus 4.7 to Opus 5 migration guide" in the Target model item rather than asserting a value.
- Context window: 1M tokens as both default and maximum; "instruction following, tool calling, and reasoning stay consistent throughout the window" (O5-22).
- Tokenizer: not printed on this page; do not assert a scaling factor.
- Effort: default `high` (O5-14). Levels the page names: `low`, `medium`, `high`, `xhigh` (it does not name `max`; do not recommend it from this profile). `low` and `medium` "produce strong quality at a fraction of the tokens and latency" and are the primary cost and latency control (O5-13, O5-15); `xhigh` is for demanding coding and agentic work (O5-16); review accuracy holds at lower effort (O5-11). Effort carried from a prior model is unverified until an effort sweep is re-run (O5-17). Effort controls thinking volume, not visible response length (O5-28, BP-095). An effort level is never carried from another profile; re-derive it here.
- `max_tokens` headroom: not printed on this page; the guide's samples pin `max_tokens` explicitly (BP-059). Fall back to the guide.
- Refusal and safeguard notes: not printed on this page. "Refusal stop details" are among the Opus 4.7 to Opus 5 migration changes (O48-05); cite that guide rather than asserting behaviour.

### Harness and environment notes

These facts reach a rearticulated prompt only through the taxonomy rows for harness authoring and prompt authoring for another model; in an interactive session the skill informs the user and does not try to set them from inside a prompt.

- Deterministic subagent caps in Claude Code and the Claude Agent SDK: environment variables `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` and `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, and the SDK option `max_budget_usd` (O5-52). They require Claude Code 2.1.217 or later; a pinned SDK must be updated before it points at Opus 5 (O5-53). Reference: Cap subagent depth, concurrency, and spend, https://code.claude.com/docs/en/agent-sdk/subagents#cap-subagent-depth-concurrency-and-spend (O5-55).
- Claude Code adds its own delegation instruction on Opus 5 only under the `claude_code` system prompt preset; a custom or omitted system prompt needs o5_delegation_guidance added by the author (O5-54). The interactive Claude Code CLI uses the preset, so in-session the instruction is already present.
- Thinking-disabled artifacts (O5-61): a tool call written into user-facing text completes the turn without running and the leaked text stays in agentic history (O5-63), most often on tool-heavy workloads such as search (O5-64); `<thinking>` or other internal tags can appear in visible output (O5-65). Mitigation order: keep thinking on at lower effort (O5-62); if thinking must stay off, graft o5_thinking_disabled_mitigation as one block (O5-67, O5-68).
- Multi-agent coordination is a strength: writer-verifier patterns work and agents rarely overwrite each other (O5-25); cap delegation for cost-sensitive workloads (O5-26).

## Behavioural deltas

One entry per page rule, in page order, grouped by the page's section headings; the guide rules that name Opus 5 follow at the end. Sample prompts are quoted in part here and stored verbatim in `references/snippet-library.md` under the snippet ID given.

Page section: Prompting Claude Opus 5 (introduction)

### O5-01 Page provenance and the six tuning areas
- Kind: fact
- Rule: Record this page's URL and snapshot date as the provenance for every Opus 5 rule.
- Page says: "title: Prompting Claude Opus 5 / url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 / description: Behavioral differences and prompting patterns for Claude Opus 5, covering response verbosity, agentic narration, task scoping, subagent delegation, self-correction, and output artifacts when thinking is disabled. / snapshot: 2026-09-08"
- Applies when: Building or citing this file.
- Skill applies it by: The header of this file carries the URL and date; the six areas in the description are the checklist sections 4 to 6 of this file have to cover.

### O5-02 What's new page for capabilities and API changes
- Kind: link
- Rule: Point readers to the What's new page for Opus 5 capabilities and API changes rather than restating them.
- Page says: "For the model's capabilities and API changes, see [What's new in Claude Opus 5](https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5)."
- Applies when: A rearticulation needs a capability or API fact this page does not state.
- Skill applies it by: Listed under Related pages in section 8 with the note "capabilities and API changes"; the skill names the page in the Target model item instead of importing or guessing its content.

### O5-03 Cross-model guide applies first
- Kind: link
- Rule: Use the Prompting best practices guide for techniques that apply across all current Claude models.
- Page says: "For techniques that apply across all current Claude models, see [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)."
- Applies when: Every run with Opus 5 as target or executing model.
- Skill applies it by: Applies `references/technique-catalog.md` first and overlays this profile; the traceability IDs in the assumptions cite both.

### O5-04 Built for complex agentic coding and long-horizon work
- Kind: model-note
- Rule: Treat Opus 5 as the model built for complex agentic coding, enterprise work, and long-horizon agentic tasks.
- Page says: "Claude Opus 5 is built for complex agentic coding and enterprise work, with particular strengths in long-horizon agentic tasks."
- Applies when: Target or executing model is Opus 5.
- Skill applies it by: The taxonomy marks agentic long-horizon and multi-step coding rows as a natural fit; the rearticulated prompt hands over the full task in one `<task>` rather than chunking it.

### O5-05 Reuse Opus 4.8 prompts, tune only the listed behaviours
- Kind: migration
- Rule: Reuse existing Opus 4.8 prompts on Opus 5 as a starting point and tune only the behaviours this page lists.
- Page says: "It performs well out of the box on existing Claude Opus 4.8 prompts. The following patterns cover the behaviors that most often require tuning."
- Applies when: A pasted or saved prompt was written for Opus 4.8 and the target is now Opus 5.
- Skill applies it by: Keeps the substance of the Opus 4.8 prompt and applies only the deltas in sections 4 and 5 (verbosity, narration, deliverable length, verification removal, scope, delegation, correction narration, thinking-disabled mitigations); the Changed line names each delta applied. This sentence is also the basis for the baseline chain in section 2.

### O5-06 Migration note: thinking on by default, disable capped at high
- Kind: migration
- Rule: When migrating from Opus 4.8, account for thinking being on by default and disabling thinking being capped at high effort.
- Page says: "<Note> For API changes when migrating from Claude Opus 4.8 (thinking on by default, and disabling thinking capped at `high` effort), see the [migration guide](https://platform.claude.com/docs/en/models/opus-5/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5). </Note>"
- Applies when: Executing on Opus 5 after Opus 4.8, or any request that mentions turning thinking off.
- Skill applies it by: Section 2 records both facts and the link. A request that asks for thinking off together with `xhigh` effort is flagged as a conflict in the Target model item, with thinking on at `low` offered instead (see O5-62).

Page section: Capability improvements

### O5-07 Strongest on multi-file features, refactors, end-to-end work
- Kind: model-note
- Rule: Expect Opus 5 to be strongest on difficult coding work: multi-file features, larger refactors, and end-to-end feature work.
- Page says: "**Agentic coding:** Claude Opus 5 is strongest on difficult coding tasks: multi-file features, larger refactors, and end-to-end feature work."
- Applies when: The request is a multi-file feature, refactor, or end-to-end implementation on Opus 5.
- Skill applies it by: Does not split such requests into small sub-prompts; states the full feature scope in one `<task>`.

### O5-08 Complete specification up front, no stubs
- Kind: technique
- Rule: Give Opus 5 the complete task specification up front and let it run, expecting full completion with no stubs or placeholders.
- Page says: "It completes full tasks rather than leaving stubs or placeholders, and it performs best when given the complete task specification up front and left to run."
- Applies when: Agentic coding request on Opus 5.
- Skill applies it by: Gathers every known requirement, constraint, and acceptance criterion into the prompt before execution (Step 2 golden-rule pass); converts or removes "leave TODOs for later" and "stub out the rest" unless the user explicitly wants partial work; adds no mid-task check-in requirements.

### O5-09 Small gain on easy single-turn edits
- Kind: model-note
- Rule: Expect only a small gain over prior models on easy single-turn edits.
- Page says: "It also performs well on easier tasks like single-turn edits, where the difference from prior models is smaller."
- Applies when: The request is a small single-turn edit.
- Skill applies it by: Keeps the rearticulation minimal (Step 5's 25-line budget), adds no Opus 5 scaffolding, and may suggest a lower effort in the Target model item.

### O5-10 Review findings are high precision and high recall
- Kind: model-note
- Rule: Trust Opus 5 code review findings as high precision and high recall.
- Page says: "**Code review and bug-finding:** Claude Opus 5 reviews code with high precision and recall: it finds real bugs at a high rate per pass, and its additional findings are mostly real issues rather than false positives."
- Applies when: Code review or bug hunt on Opus 5.
- Skill applies it by: Asks for the findings list directly; adds no "avoid false positives" hedging and no demand that each finding be re-proved.

### O5-11 Fast review pass at lower effort, thorough pass later
- Kind: technique
- Rule: Run a fast review pass at lower effort and a thorough pass later, since review accuracy holds at lower effort.
- Page says: "Accuracy holds at lower effort settings, which supports a fast pass at review time and a more thorough pass later."
- Applies when: Code review where cost or latency matters.
- Skill applies it by: The Target model item suggests `low` or `medium` for a first review pass and notes that a deeper pass can follow; effort is never encoded in prompt prose.

### O5-12 No severity-limiting or conservatism wording in review prompts
- Kind: anti-pattern
- Rule: Do not tell an Opus 5 review prompt to report only high-severity issues or to be conservative; ask for everything and filter in a separate pass.
- Page says: "If your review prompt says \"only report high-severity issues\" or \"be conservative,\" the model may follow that instruction literally and report less; ask it to report everything and filter in a separate pass instead."
- Applies when: The raw request or a pasted review prompt contains severity-limiting or conservatism wording.
- Skill applies it by: Section 5 conversion: replaces the wording with "report every issue you find, tagged with severity" and adds a filtering step (a final ranked section in the same prompt, or a second pass). The page prints no snippet for this; the coverage text is borrowed from the Opus 4.8 baseline (o48_review_coverage) and the Target model item records the borrowing.

### O5-13 Low and medium effort are efficient
- Kind: fact
- Rule: Use low and medium effort for strong quality at a fraction of the tokens and latency of higher settings.
- Page says: "**Efficiency at lower effort:** `low` and `medium` [effort](https://platform.claude.com/docs/en/build-with-claude/effort) produce strong quality at a fraction of the tokens and latency of higher settings."
- Applies when: Any Opus 5 execution where cost or latency matters.
- Skill applies it by: Section 2 records it; the Target model item may recommend `low` or `medium` for routine tasks.

### O5-14 Start at the default high and adjust from evals
- Kind: technique
- Rule: Start at the default high effort and adjust from eval results.
- Page says: "Start with the default (`high`) and adjust based on your evals:"
- Applies when: Choosing an effort level for Opus 5 without prior measurements.
- Skill applies it by: The Target model item defaults to `high` when there is no signal about task difficulty and says `high` is the Opus 5 default.

### O5-15 Low and medium as the primary cost and latency control
- Kind: technique
- Rule: Use low and medium liberally as the primary control for token cost and response time wherever quality holds.
- Page says: "use `low` and `medium` liberally as your primary control for token cost and response time wherever quality holds,"
- Applies when: Cost-sensitive or latency-sensitive Opus 5 work.
- Skill applies it by: When the user signals speed or cost concerns, the Target model item suggests `low` or `medium` effort instead of the prompt carrying "be brief" prose; effort governs thinking, not response length (O5-28).

### O5-16 Step up to xhigh for demanding work
- Kind: technique
- Rule: Step up to xhigh effort for demanding coding and agentic work.
- Page says: "and step up to `xhigh` for demanding coding and agentic work."
- Applies when: Hard multi-file coding or long agentic tasks on Opus 5.
- Skill applies it by: The Target model item suggests `xhigh` for requests classified as demanding coding or long-horizon agentic work and notes that thinking cannot be disabled at `xhigh` (O5-60).

### O5-17 Re-run the effort sweep after carrying defaults over
- Kind: migration
- Rule: Re-run an effort sweep on your own evals if effort defaults were carried over from a prior model.
- Page says: "If you carried effort defaults over from a prior model, re-run an effort sweep on your own evals."
- Applies when: An effort setting was tuned for Opus 4.8 or another prior model.
- Skill applies it by: Section 2 records it; when a saved prompt hardcodes an effort rationale from an older model the Target model item flags it as unverified for Opus 5.

### O5-18 Effort page link
- Kind: link
- Rule: Consult the Effort page for the full recommended effort levels for Opus 5.
- Page says: "See [Effort](https://platform.claude.com/docs/en/build-with-claude/effort#recommended-effort-levels-for-claude-opus-5) for the full recommendations."
- Applies when: Choosing an effort suggestion for Opus 5.
- Skill applies it by: Listed under Related pages in section 8 with the note "recommended effort levels for Claude Opus 5".

### O5-19 Strong on charts, documents, diagrams, UI replication
- Kind: model-note
- Rule: Expect strong chart, document, and diagram understanding and strong UI and frontend visual replication.
- Page says: "**Vision:** Claude Opus 5 is strong on chart, document, and diagram understanding, and on UI and frontend visual replication."
- Applies when: The request includes images, charts, PDFs, diagrams, or a screenshot to replicate.
- Skill applies it by: Describes the expected output of the visual task plainly in `<task>` without extra hand-holding about reading the image.

### O5-20 Drop legacy vision workarounds
- Kind: migration
- Rule: Re-validate and drop prompt-side vision workarounds tuned for prior models.
- Page says: "Re-validate any prompt-side vision workarounds you tuned for prior models; they may no longer be needed."
- Applies when: A saved prompt contains vision hacks such as "describe every region first" or "zoom mentally".
- Skill applies it by: Section 5 conversion: strips or flags legacy vision workaround text and records it in the Changed line.

### O5-21 Tools to analyze, crop, and verify beat thinking alone for vision
- Kind: technique
- Rule: Give the model tools to iteratively analyze, crop, and visually verify its work rather than relying on thinking alone for vision tasks.
- Page says: "Vision performance is strongest when the model has tools to iteratively analyze, crop, and visually verify its work, and tool use is a more cost-effective lever than thinking alone."
- Applies when: Vision task on Opus 5 where image tools (crop, zoom, screenshot, render) are available.
- Skill applies it by: `<execution_guidance>` explicitly permits and encourages tool-based inspection (crop, zoom, re-render and compare) for visual tasks, aligned with the guide's crop-and-zoom guidance (BP-322); the Target model item does not propose raising effort as the fix for vision accuracy.

### O5-22 1M token context window, consistent throughout
- Kind: fact
- Rule: Rely on a 1M token context window (default and maximum) with consistent instruction following, tool calling, and reasoning throughout.
- Page says: "**Long-context work:** Claude Opus 5 has a [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) as both the default and the maximum, and its instruction following, tool calling, and reasoning stay consistent throughout the window."
- Applies when: Large documents, big codebases, or long sessions on Opus 5.
- Skill applies it by: Places long documents whole in `<documents>` without chunking instructions; adds no "remember the earlier instructions" reminders purely for context length; grafts no context-limit reminder for Opus 5 (contrast BP-241 for the Sonnet family); section 2 records the 1M figure.

### O5-23 Complex spreadsheets and slide decks
- Kind: model-note
- Rule: Expect strong handling of complex multi-sheet spreadsheets with non-trivial formulas and well-structured slide decks.
- Page says: "**Office and document tasks:** Claude Opus 5 generates and works with complex, multi-sheet spreadsheets with non-trivial formulas, and it produces well-structured slide decks."
- Applies when: The request produces or edits spreadsheets or slide decks.
- Skill applies it by: The taxonomy marks spreadsheet and deck requests as well supported on Opus 5; no step-by-step scaffolding is added.

### O5-24 Supply styles or templates for office deliverables
- Kind: technique
- Rule: Include any specific styles or templates the office deliverable must follow.
- Page says: "Prompt it with any specific styles or templates it needs to follow."
- Applies when: Spreadsheet or slide deck request where a house style or template exists.
- Skill applies it by: Asks for or attaches the template, sheet layout, or style rules in a dedicated block inside `<constraints>` (for example `<template>` or `<style_requirements>`) rather than leaving formatting implicit.

### O5-25 Coordinates subagent teams well
- Kind: model-note
- Rule: Expect Opus 5 to coordinate subagent teams well, including writer-verifier patterns, with few overwrite conflicts.
- Page says: "**Multi-agent coordination:** Claude Opus 5 coordinates teams of subagents well, with effective writer-verifier patterns and few cases of agents overwriting each other's work."
- Applies when: A genuinely parallelizable multi-agent task on Opus 5.
- Skill applies it by: Structures `<task>` around clear per-agent ownership for large independent workstreams; adds no elaborate conflict-avoidance rules.

### O5-26 Cap delegation for cost-sensitive workloads
- Kind: technique
- Rule: Cap delegation for cost-sensitive workloads.
- Page says: "For cost-sensitive workloads, cap delegation; see [Controlling subagent spawning](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning)."
- Applies when: Cost matters and the harness allows subagents.
- Skill applies it by: Cross-references O5-48 to O5-55; grafts o5_delegation_guidance when the user mentions budget or the task is small.

Page section: Response length and verbosity

### O5-27 Default responses run longer than prior Opus models
- Kind: model-note
- Rule: Expect Opus 5 default user-facing responses to run longer than prior Opus models.
- Page says: "Claude Opus 5's default user-facing responses run longer than prior Opus models'."
- Applies when: Any conversational or user-facing output on Opus 5.
- Skill applies it by: `<output_format>` carries a brief conciseness line (o5_conciseness) for chat-style outputs unless the user asked for depth; this is the guide's verbosity exception (BP-094).

### O5-28 Effort does not shorten visible responses
- Kind: fact
- Rule: Do not use effort to shorten visible responses; it controls thinking volume, not how much the model says.
- Page says: "The [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) controls how much the model [thinks](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost) rather than how much it says: lowering effort can reduce thinking volume without reliably shortening the visible response."
- Applies when: The user asks for shorter answers and the temptation is to lower effort.
- Skill applies it by: Converts "make it shorter" into an explicit length instruction in `<output_format>`; keeps effort as a separate cost lever and says so in the Target model item (BP-095).

### O5-29 Prompt explicitly for response length
- Kind: technique
- Rule: Prompt explicitly for the response length you want.
- Page says: "To control response length, prompt for it explicitly."
- Applies when: The desired output length differs from the Opus 5 default.
- Skill applies it by: `<output_format>` always states a target length or shape (sentences, bullets, sections) for Opus 5 targets (BP-096, BP-017).

### O5-30 Short conciseness instruction for user-facing products
- Kind: technique
- Rule: Use a short conciseness instruction for user-facing multi-turn products.
- Page says: "A short conciseness instruction is effective. For example, for a user-facing multi-turn product:"
- Applies when: Conversational or assistant-style output on Opus 5.
- Skill applies it by: Grafts o5_conciseness into `<output_format>` for chat-style requests.

### O5-31 Sample: o5_conciseness
- Kind: sample-prompt
- Rule: Insert this conciseness instruction to keep Opus 5 responses focused and brief.
- Page says: see snippet o5_conciseness; opens "Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer."
- Applies when: User-facing multi-turn product, or any request where the user wants tight answers.
- Skill applies it by: Grafts verbatim into `<output_format>` when the target is Opus 5 and the request is conversational or the user asks for brevity.

### O5-32 Pair with a reminder near the end of a long prompt
- Kind: technique
- Rule: In a long system prompt, pair the conciseness instruction with a short reminder near the end.
- Page says: "In a long system prompt, pair the instruction with a short reminder near the end of the prompt:"
- Applies when: The rearticulated prompt is long and conciseness matters.
- Skill applies it by: When the generated prompt exceeds a few hundred words, tone_preference is the final block of the prompt.

### O5-33 Sample: tone_preference
- Kind: sample-prompt
- Rule: Append this tone_preference reminder near the end of a long prompt.
- Page says: see snippet tone_preference; the block is "<tone_preference> Keep outputs reasonably concise. </tone_preference>"
- Applies when: Long system or task prompt on Opus 5 where a conciseness instruction appears earlier.
- Skill applies it by: Grafts verbatim, wrapper included, as the last block of long rearticulated prompts for Opus 5.

Page section: User-facing progress updates

### O5-34 Narrates readily during agentic work
- Kind: model-note
- Rule: Expect Opus 5 to narrate readily during agentic work, announcing upcoming actions with longer per-message output than prior models.
- Page says: "Claude Opus 5 narrates readily during agentic work: it tends to announce what it is about to do, and its per-message output in agentic sessions is often longer than prior models'."
- Applies when: Agentic, tool-using execution on Opus 5.
- Skill applies it by: `<execution_guidance>` carries o5_progress_updates by default for tool-heavy tasks; the Fable 5.1 progress_updates_line is not grafted on Opus 5.

### O5-35 Describe the cadence and shape to tune narration down
- Kind: technique
- Rule: Give explicit guidance on how to communicate with the user during a task; to tune narration down, describe the cadence and shape you want.
- Page says: "It benefits from explicit guidance on how to communicate with the user during a task. To tune narration down, describe the cadence and shape you want:"
- Applies when: Agentic task where the user wants less chatter.
- Skill applies it by: Describes when to speak (before the first tool call, on important findings or direction changes, at completion) and the shape of each update rather than writing "don't narrate".

### O5-36 Sample: o5_progress_updates
- Kind: sample-prompt
- Rule: Insert this cadence instruction to tune agentic narration down on Opus 5.
- Page says: see snippet o5_progress_updates; opens "Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction."
- Applies when: Agentic tool-using tasks on Opus 5 where terse progress updates are preferred.
- Skill applies it by: Grafts verbatim into `<execution_guidance>` for investigations, multi-step coding, and any task with many tool calls; section 6 uses the same cadence for the skill's own narration.

### O5-37 Describe and exemplify to tune narration up
- Kind: technique
- Rule: To tune narration up or change its style, explicitly describe what updates should look like and provide examples.
- Page says: "To tune narration up, or change its style, the same lever applies in the other direction: explicitly describe what updates should look like and provide examples."
- Applies when: The user wants more or differently styled progress reporting.
- Skill applies it by: Writes a short description plus one or two example update lines inside `<examples>`.

### O5-38 Positive examples beat what-not-to-do
- Kind: technique
- Rule: Prefer positive examples of the desired communication style over instructions about what not to do.
- Page says: "Positive examples of the communication style you want tend to be more effective than instructions about what not to do."
- Applies when: Any narration or tone instruction for Opus 5.
- Skill applies it by: Converts "don't be chatty" and "no fluff" into a positive description or example of the desired style (the guide's positive format control, BP-103).

Page section: Written deliverable length

### O5-39 Files written to disk run longer
- Kind: model-note
- Rule: Expect files Opus 5 writes to disk (reports, Markdown documents, summaries) to run longer than on prior models, independent of conversational verbosity.
- Page says: "Separate from conversational verbosity, files that Claude Opus 5 writes to disk (reports, Markdown documents, summaries) are often longer than on prior models."
- Applies when: The request produces a written document or file on Opus 5.
- Skill applies it by: Treats document length as a separate lever from chat brevity; grafts o5_deliverable_length whenever the output is a file, even if o5_conciseness is already present.

### O5-40 Add explicit length calibration for documents
- Kind: technique
- Rule: Add explicit length calibration for Claude-authored documents.
- Page says: "If your product includes Claude-authored documents, add explicit length calibration:"
- Applies when: The request produces reports, docs, or summaries.
- Skill applies it by: Grafts o5_deliverable_length into `<output_format>` for any file-producing task.

### O5-41 Sample: o5_deliverable_length
- Kind: sample-prompt
- Rule: Insert this length calibration for written documents on Opus 5.
- Page says: see snippet o5_deliverable_length; the text is "Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate."
- Applies when: Any task where Opus 5 writes a report, Markdown document, or summary to disk.
- Skill applies it by: Grafts verbatim into `<output_format>` for document-producing requests on Opus 5.

Page section: Task scope and over-verification

### O5-42 Verifies its own work unprompted
- Kind: model-note
- Rule: Expect Opus 5 to verify its own work without being told to.
- Page says: "Claude Opus 5 verifies its own work without being told to."
- Applies when: Any non-trivial task on Opus 5.
- Skill applies it by: Omits the `<verification>` tag and the guide's self_check_verify for Opus 5 targets; this profile overrides catalog entries BP-229 and BP-230 for this model. When Opus 5 is the executing model, Step 7 reports checks already performed rather than running a prescribed loop (section 6).

### O5-43 Remove explicit verification instructions
- Kind: anti-pattern
- Rule: Remove explicit verification instructions such as a final verification step or a verification subagent; they cause over-verification and waste tokens with no quality gain.
- Page says: "If your prompt contains explicit verification instructions (\"include a final verification step for any non-trivial task,\" \"use a subagent to verify\"), remove them: instructions like these cause over-verification on Claude Opus 5, and removing them reduces wasted tokens with no loss in quality."
- Applies when: A raw request or saved prompt contains verification-step or verify-with-subagent wording and the target is Opus 5.
- Skill applies it by: Section 5: deletes the wording rather than rewriting it (BP-233) and records the removal in the Changed line.

### O5-44 Remove legacy harness verification scaffolding
- Kind: anti-pattern
- Rule: Remove legacy harness scaffolding that adds separate verification steps.
- Page says: "The same applies to legacy harness scaffolding that adds separate verification steps."
- Applies when: Skill templates or harness wrappers carry separate verify phases from older models.
- Skill applies it by: The template's `<verification>` tag is conditional on the target model and is absent for Opus 5; harness authoring for Opus 5 carries no separate verify phase.

### O5-45 Can expand task scope
- Kind: model-note
- Rule: Expect Opus 5 to expand task scope by adding unrequested steps or applying its own judgment about what the task should be.
- Page says: "Claude Opus 5 can also expand the scope of a task, adding steps that weren't requested or applying its own judgment about what the task should be."
- Applies when: Narrow or precisely bounded requests on Opus 5.
- Skill applies it by: Includes o5_scope_constraint in `<constraints>` for narrow tasks by default; omits it for open-ended exploratory tasks where widening is wanted.

### O5-46 Constrain scope explicitly for narrow tasks
- Kind: technique
- Rule: Constrain scope explicitly for narrow tasks.
- Page says: "For narrow tasks, constrain scope explicitly:"
- Applies when: The user wants exactly what was asked and nothing more.
- Skill applies it by: Grafts o5_scope_constraint into `<constraints>` when the taxonomy classifies the request as narrow (single-file change, one named target, "just do X").

### O5-47 Sample: o5_scope_constraint
- Kind: sample-prompt
- Rule: Insert this scope constraint to keep Opus 5 on the requested task.
- Page says: see snippet o5_scope_constraint; opens "Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work."
- Applies when: Narrow tasks on Opus 5 where scope creep or silent transformation is unwanted.
- Skill applies it by: Grafts verbatim into `<constraints>` for narrow edits, single-file changes, and any request framed as "just do X". On Opus 5 this is the scope block; the Fable 5.1 keep_changes_to_task is not grafted.

Page section: Controlling subagent spawning

### O5-48 Delegates more readily than prior models
- Kind: model-note
- Rule: Expect Opus 5 to delegate to subagents more readily than prior models.
- Page says: "Claude Opus 5 delegates to subagents more readily than prior models."
- Applies when: Executing on Opus 5 in a harness that supports subagents (Claude Code, Agent SDK).
- Skill applies it by: For small or medium tasks includes delegation guidance in authored prompts so the model does not spawn agents for work it can finish itself; the guide's Subagent orchestration section makes the same point (BP-287).

### O5-49 Delegation pays off only on independent, sizeable tracks
- Kind: fact
- Rule: Delegate only for genuinely independent, sizeable tracks of work; delegation multiplies cost and time on small tasks.
- Page says: "Delegation pays off on genuinely independent, sizeable tracks of work, but it multiplies cost and time when applied to small tasks."
- Applies when: Deciding whether a rearticulated task should permit subagents.
- Skill applies it by: The taxonomy classifies the request by size and independence; the prompt permits delegation only for wide, parallelizable investigations.

### O5-50 Explicit delegation guidance or deterministic caps
- Kind: technique
- Rule: Give explicit guidance on which scenarios warrant delegation, or set deterministic caps on the number of agents launched.
- Page says: "If your harness supports subagents, give explicit guidance on which scenarios warrant delegation, or set deterministic caps on how many agents can be launched. For example:"
- Applies when: The harness supports subagents and the target is Opus 5.
- Skill applies it by: Grafts o5_delegation_guidance into `<execution_guidance>`; section 2 names the environment-variable caps as the deterministic alternative the user sets outside the prompt.

### O5-51 Sample: o5_delegation_guidance
- Kind: sample-prompt
- Rule: Insert this delegation guidance to keep Opus 5 subagent spawning low.
- Page says: see snippet o5_delegation_guidance; opens "Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation."
- Applies when: Opus 5 in Claude Code or the Agent SDK with a custom or omitted system prompt, or any cost-sensitive agentic task.
- Skill applies it by: Grafts verbatim into `<execution_guidance>` of agentic rearticulations for Opus 5 unless the task is explicitly a wide parallel investigation; it is the Opus 5 counterpart of the guide's subagent_usage_policy (BP-287, BP-288). Not grafted in-session under the `claude_code` preset (O5-54).

### O5-52 Deterministic caps: env vars and max_budget_usd
- Kind: fact
- Rule: Use CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH, CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS, and the SDK max_budget_usd option as the deterministic delegation caps in Claude Code and the Agent SDK.
- Page says: "If your harness is Claude Code or the Claude Agent SDK, the deterministic caps are the `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` and `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` environment variables and the SDK's `max_budget_usd` option."
- Applies when: The user wants hard limits on spawning or spend for Opus 5 in Claude Code or the Agent SDK.
- Skill applies it by: Section 2 (harness notes) records the exact names; when the user asks to limit subagents, the Target model item names these caps as environment-level controls the prompt cannot set.

### O5-53 Requires Claude Code 2.1.217 or later
- Kind: fact
- Rule: Require Claude Code 2.1.217 or later for the subagent caps, and update a pinned SDK before targeting Opus 5.
- Page says: "They require Claude Code 2.1.217 or later, so update a pinned SDK before pointing it at Claude Opus 5."
- Applies when: The harness version is pinned or older than 2.1.217.
- Skill applies it by: Section 2 records the version floor; the skill does not promise the caps work on older builds.

### O5-54 Delegation instruction only under the claude_code preset
- Kind: fact
- Rule: Add your own delegation instruction unless Claude Code's claude_code system prompt preset is in use, since only the preset injects one on Opus 5.
- Page says: "Claude Code adds a delegation instruction of its own on Claude Opus 5 only when you use its `claude_code` system prompt preset; with a custom or omitted system prompt, add a delegation instruction such as the example in this section yourself."
- Applies when: Opus 5 in Claude Code or the Agent SDK with a custom or omitted system prompt.
- Skill applies it by: In-session (interactive CLI, preset in use) the skill does not graft o5_delegation_guidance; in authored prompts, SDK code, or when the user says the system prompt is custom, it grafts it.

### O5-55 Agent SDK caps link
- Kind: link
- Rule: Consult the Agent SDK docs section on capping subagent depth, concurrency, and spend for full details.
- Page says: "See [Cap subagent depth, concurrency, and spend](https://code.claude.com/docs/en/agent-sdk/subagents#cap-subagent-depth-concurrency-and-spend) in the Agent SDK docs."
- Applies when: Configuring deterministic subagent caps.
- Skill applies it by: Listed under Related pages in section 8 with the note "cap subagent depth, concurrency, and spend (env vars and max_budget_usd)".

Page section: Self-correction

### O5-56 Catches and fixes its own mistakes
- Kind: model-note
- Rule: Expect Opus 5 to catch and fix its own mistakes without prompting.
- Page says: "Claude Opus 5 catches and fixes its own mistakes well without prompting."
- Applies when: Any task on Opus 5.
- Skill applies it by: Adds no self-review or re-check instructions to Opus 5 prompts; overrides the guide's self-check technique for this model together with O5-42.

### O5-57 No double-check or re-verify instructions
- Kind: anti-pattern
- Rule: Do not instruct re-checks the model already performs, such as double-check your answer or re-verify before responding.
- Page says: "Avoid instructing re-checks it already performs (\"double-check your answer,\" \"re-verify before responding\"); like verification instructions, these compound with the model's own behavior and add cost without improving results."
- Applies when: The raw request contains "double-check", "re-verify", "make sure you're right" or similar and the target is Opus 5.
- Skill applies it by: Section 5: strips the phrases and records the removal; if the user insists on a check, it becomes a concrete acceptance criterion in `<success_criteria>` rather than a re-check instruction.

### O5-58 Narrates corrections more than prior models
- Kind: model-note
- Rule: Expect Opus 5 to narrate corrections to earlier statements more than prior models, which can be undesirable in user-facing products.
- Page says: "The model also narrates corrections to its earlier statements more than prior models do, which can be undesirable in user-facing products. To limit correction narration to corrections that matter:"
- Applies when: User-facing or polished output on Opus 5.
- Skill applies it by: Grafts o5_correction_narration into `<output_format>` for user-facing products or when the user asks for clean output without self-commentary.

### O5-59 Sample: o5_correction_narration
- Kind: sample-prompt
- Rule: Insert this instruction to limit Opus 5 correction narration to corrections that matter.
- Page says: see snippet o5_correction_narration; opens "Only correct an earlier statement when the error would change the user's code, conclusions, or decisions."
- Applies when: User-facing products or any Opus 5 task where visible self-corrections are noise.
- Skill applies it by: Grafts verbatim when the output is user-facing or the request asks for a clean final answer; section 6 applies the same rule to the skill's own visible text.

Page section: Running with thinking disabled

### O5-60 Thinking on by default; disable only at high or below
- Kind: fact
- Rule: Assume thinking is on by default and can be disabled only at effort high or below.
- Page says: "Claude Opus 5 runs with [thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) on by default, and thinking can be disabled only at [effort](https://platform.claude.com/docs/en/build-with-claude/effort) `high` or below; see the [migration guide](https://platform.claude.com/docs/en/models/opus-5/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5)."
- Applies when: Any request to disable thinking on Opus 5, or a session configured with thinking off.
- Skill applies it by: Section 2 records it (with BP-218, BP-219); a request for thinking off at `xhigh` is flagged as incompatible in the Target model item, with thinking on at `low` suggested instead.

### O5-61 Two artifacts when thinking is disabled
- Kind: model-note
- Rule: Expect two occasional output artifacts when thinking is disabled.
- Page says: "With thinking disabled, two artifacts can occasionally appear in the model's visible output."
- Applies when: Opus 5 running with thinking disabled.
- Skill applies it by: Section 2 (harness notes) lists the two artifacts (tool calls as text, internal XML tags) and links them to o5_thinking_disabled_mitigation.

### O5-62 Keep thinking on at low effort rather than disabling it
- Kind: technique
- Rule: Keep thinking enabled and lower effort instead of disabling thinking; thinking at low effort beats thinking disabled at similar cost.
- Page says: "The primary mitigation for both is to keep thinking enabled and control token cost with lower effort levels instead of disabling thinking: for most tasks, thinking enabled at `low` effort performs better than thinking disabled at similar cost."
- Applies when: The user wants to cut cost and considers disabling thinking on Opus 5.
- Skill applies it by: Converts "turn thinking off to save tokens" into a Target model item suggestion of `low` effort with thinking on (BP-227).

### O5-63 Tool calls leak as text
- Kind: model-note
- Rule: Expect the model, with thinking disabled, to occasionally write a tool call as plain text instead of a tool_use block, so the call never runs and leaked text persists in agentic history.
- Page says: "**Tool calls as text.** With thinking disabled, the model occasionally writes a tool call into its user-facing text instead of emitting a structured `tool_use` block. The turn completes normally and the call never runs, and in agentic loops the leaked text stays in the conversation history, so later turns are affected as well."
- Applies when: Opus 5 with thinking disabled in tool-using workloads.
- Skill applies it by: When executing with thinking off, grafts o5_thinking_disabled_mitigation; section 6 says how the skill recognises and repairs a leaked text tool call.

### O5-64 Most common on tool-heavy workloads
- Kind: fact
- Rule: Expect the tool-call-as-text artifact most on tool-heavy workloads such as search.
- Page says: "This is most common on tool-heavy workloads such as search."
- Applies when: Search or other tool-heavy tasks on Opus 5 with thinking disabled.
- Skill applies it by: Prioritises the mitigation snippet, or a recommendation to re-enable thinking, for search-style agentic tasks when thinking is off.

### O5-65 Internal XML tags leak into output
- Kind: model-note
- Rule: Expect the model, with thinking disabled, to occasionally emit <thinking> or other internal XML tags in its visible response.
- Page says: "**Internal XML tags in output.** With thinking disabled, the model can emit `<thinking>` tags or other internal XML tags into its visible response."
- Applies when: Opus 5 with thinking disabled.
- Skill applies it by: Section 2 records it; grafts o5_thinking_disabled_mitigation when thinking must stay off; avoids tag names in the rearticulated prompt that look like internal tags, and never uses `<thinking>`/`<answer>` output tags on Opus 5 (BP-227).

### O5-66 Remove do-not-think rules
- Kind: anti-pattern
- Rule: Remove any system prompt rule that tells the model not to think or not to reason; it increases tag leakage.
- Page says: "If your system prompt contains a rule instructing the model not to think or not to reason, remove it; that kind of instruction increases tag leakage."
- Applies when: A raw request or saved prompt contains "don't think", "no reasoning", "answer without thinking" and the target is Opus 5.
- Skill applies it by: Section 5: strips the wording (including the guide's think_only_when_useful, whose "When in doubt, respond directly" falls in this class when thinking is disabled) and records the removal; a speed or cost intent becomes an effort suggestion in the Target model item.

### O5-67 One combined instruction when thinking must stay off
- Kind: technique
- Rule: For integrations that must keep thinking disabled, use one combined instruction granting permission to speak before a tool call, an alternative when no tool fits, and a general ban on internal tags.
- Page says: "For integrations that must keep thinking disabled, a single combined instruction mitigates both artifacts: it gives the model explicit permission to speak before a tool call, an alternative to forcing a call when no tool fits, and a general rule against internal tags:"
- Applies when: Thinking must remain disabled (integration constraint) on Opus 5.
- Skill applies it by: Grafts o5_thinking_disabled_mitigation as a single block; does not split it into three rules or add tag-specific variants.

### O5-68 Sample: o5_thinking_disabled_mitigation
- Kind: sample-prompt
- Rule: Insert this combined instruction when Opus 5 must run with thinking disabled.
- Page says: see snippet o5_thinking_disabled_mitigation; the text is "When you use a tool, you may say a brief sentence first. If no tool can express what the user asked for, say so instead of guessing. Do not include internal or system XML tags in your response."
- Applies when: Opus 5 with thinking disabled, especially tool-heavy or search workloads.
- Skill applies it by: Grafts verbatim only when the session or integration has thinking off; otherwise recommends thinking on at `low` effort.

### O5-69 Do not name thinking tags in anti-leak instructions
- Kind: anti-pattern
- Rule: Do not name thinking tags specifically in anti-leak instructions; the general form is more effective.
- Page says: "Instructions that call out thinking tags by name are less effective than the general form, so avoid naming them specifically."
- Applies when: Writing any instruction against tag leakage for Opus 5.
- Skill applies it by: Converts "never output <thinking> tags" into the general "Do not include internal or system XML tags in your response" wording from o5_thinking_disabled_mitigation.

Guide rules naming Opus 5 (from Prompting best practices; catalog IDs, quoted from the guide)

### BP-002 Opus 5 is inside the guide's covered set
- Kind: fact
- Rule: Treat the guide as authoritative for exactly these eleven current models and route any other model to the migration considerations.
- Guide says: "This is the reference for prompt engineering with current Claude models, including Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, and Claude Haiku 4.5."
- Applies when: Resolving whether guide techniques are measured on the target.
- Skill applies it by: Opus 5 needs no analogy note; the guide applies directly.

### BP-006 Further reading links for model facts
- Kind: fact
- Rule: Defer to the linked capability, what's-new, and migration pages rather than inventing model facts when a request needs them.
- Guide says: "For details on what's new in Claude Opus 5, see [What's new in Claude Opus 5](https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5). For migration guidance, see the [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide)."
- Applies when: A request turns on a capability claim the snapshots do not state.
- Skill applies it by: Names the page to check in the Target model item instead of asserting the claim; links are in section 8.

### BP-011 What's new in Claude Opus 5
- Kind: link
- Rule: Point to What's new in Claude Opus 5 for Opus 5 changes.
- Guide says: "For details on what's new in Claude Opus 5, see [What's new in Claude Opus 5](https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5)."
- Applies when: The user targets Opus 5 in a prompt-authoring request.
- Skill applies it by: Section 8 Related pages.

### BP-017 The guide's model table row for Opus 5
- Kind: model-note
- Rule: For Opus 5, set response length and verbosity, progress updates, written deliverable length, task scope, subagent control, and self-correction explicitly, and do not add over-verification instructions.
- Guide says: "| Claude Opus 5 | [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) | Differences from prior Opus models: response length and verbosity, user-facing progress updates, written deliverable length, task scope and over-verification, subagent control, and self-correction. |"
- Applies when: The user targets Opus 5.
- Skill applies it by: Section 4 states deliverable length, task scope, and subagent policy explicitly and omits `<verification>`; these stand in for the verification tag.

### BP-022 Prompting Claude Opus 5 page link
- Kind: link
- Rule: Open the Prompting Claude Opus 5 page for Opus 5 specifics.
- Guide says: "[Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)"
- Applies when: The user targets Opus 5.
- Skill applies it by: This file is the local rendering of that page; the header cites it.

### BP-059 Pinned model string and max_tokens in API samples
- Kind: fact
- Rule: Pin an explicit model string and max_tokens in any API sample the skill produces.
- Guide says: "\"model\": \"claude-opus-5\", / \"max_tokens\": 1024,"
- Applies when: Producing API calls or SDK code as the execution output.
- Skill applies it by: Sets `model` and `max_tokens` explicitly; uses `claude-opus-5` only when Opus 5 is the target, substituting the actual target otherwise, and records the choice in the Target model item.

### BP-062 Data-first ordering has no model exception
- Kind: fact
- Rule: Apply data-first ordering for every model; there is no model exception.
- Guide says: "This improves performance across all models."
- Applies when: Any long-document rearticulation for Opus 5.
- Skill applies it by: `<documents>` precedes `<task>` on Opus 5 exactly as on every other model.

### BP-081 Sample: model_identity
- Kind: sample-prompt
- Rule: Use this sentence pair to fix the assistant's identity.
- Guide says: see snippet model_identity; the text is "The assistant is Claude, created by Anthropic. The current model is Claude Opus 5."
- Applies when: Authored application system prompts that need correct self-identification.
- Skill applies it by: Grafts into `<role>` of the authored system prompt; the model name is Opus 5 only when Opus 5 is the target (BP-082).

### BP-082 Substitute the model that will actually run
- Kind: model-note
- Rule: Replace "Claude Opus 5" with the model that will actually run the prompt.
- Guide says: "The current model is Claude Opus 5."
- Applies when: Grafting either self-knowledge sample.
- Skill applies it by: Reads the target from the raw request or the alias table; substitutes display name and exact string; records the substitution in the Target model item. For an Opus 5 target the guide's wording stands as printed.

### BP-084 Sample: model_string
- Kind: sample-prompt
- Rule: Use this wording to set the default model and its API string.
- Guide says: see snippet model_string; opens "When an LLM is needed, please default to Claude Opus 5 unless the user requests otherwise. The exact model string for Claude Opus 5 is claude-opus-5."
- Applies when: System prompts for LLM-powered apps and coding assistants that generate SDK calls.
- Skill applies it by: Grafts into the authored system prompt with the target substituted; keeps both halves (default and exact string).

### BP-085 The exact API string claude-opus-5
- Kind: fact
- Rule: Use claude-opus-5 as the exact API model string for Claude Opus 5.
- Guide says: "The exact model string for Claude Opus 5 is claude-opus-5."
- Applies when: Generating or checking API calls that target Opus 5.
- Skill applies it by: Section 2 records the string; user-pasted code with a different Opus 5 string is corrected and the change recorded.

### BP-086 Default model is overridable
- Kind: technique
- Rule: Make the default model overridable by explicit user request.
- Guide says: "please default to Claude Opus 5 unless the user requests otherwise."
- Applies when: Authoring default-model instructions for an application.
- Skill applies it by: Phrases the default as a default in `<constraints>` so the assistant honours a user who names another model.

### BP-094 Verbosity exception
- Kind: model-note
- Rule: Treat Claude Opus 5 as the exception on verbosity: its default user-facing responses run longer than prior models.
- Guide says: "Claude Opus 5 is an exception on verbosity: its default user-facing responses run longer than prior models',"
- Applies when: The rearticulated prompt targets Opus 5.
- Skill applies it by: `<output_format>` carries an explicit length or conciseness instruction (o5_conciseness for chat-style output); this is the one case where the skill adds a conciseness instruction of its own accord (Standing rule 12 as reworded for model pages).

### BP-095 Effort does not change visible length
- Kind: model-note
- Rule: Do not use the effort parameter to control visible response length on Claude Opus 5; it does not reliably change it.
- Guide says: "raising or lowering [effort](https://platform.claude.com/docs/en/build-with-claude/effort) does not reliably change visible response length."
- Applies when: A pasted prompt or the raw request relies on effort to shorten Opus 5 output.
- Skill applies it by: Replaces that reliance with an explicit conciseness instruction and records it (same conversion as O5-28).

### BP-096 Prompt explicitly for conciseness
- Kind: model-note
- Rule: For Claude Opus 5, prompt explicitly for conciseness instead of relying on defaults or effort settings.
- Guide says: "Prompt explicitly for conciseness instead."
- Applies when: Any Opus 5 prompt where response length matters.
- Skill applies it by: Inserts a direct, positively phrased conciseness instruction into `<output_format>` (a target length or "answer in N paragraphs").

### BP-097 Link to the sample conciseness instruction
- Kind: link
- Rule: Consult the Prompting Claude Opus 5 page, section Response length and verbosity, for the sample conciseness instruction.
- Guide says: "See [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity) for a sample instruction."
- Applies when: Grafting a conciseness snippet for an Opus 5 target.
- Skill applies it by: The sample is o5_conciseness (O5-31); section 8 lists the anchor.

### BP-189 budget_tokens returns 400 on 4.7 and later
- Kind: fact
- Rule: Never emit budget_tokens for Claude 4.7 or later models; the API returns a 400 error.
- Guide says: "On Claude 4.7 and later models, setting `budget_tokens` returns a 400 error."
- Applies when: Any generated or migrated API configuration for Opus 5.
- Skill applies it by: Strips `budget_tokens`, substitutes adaptive thinking plus `output_config.effort`, and records the substitution in the Target model item.

### BP-218 Thinking on by default on Opus 5 and Sonnet 5
- Kind: model-note
- Rule: On Claude Opus 5 and Sonnet 5, thinking is on by default when the thinking parameter is omitted.
- Guide says: "On Claude Opus 5 and Claude Sonnet 5, thinking is on by default when you omit the `thinking` parameter."
- Applies when: Authoring a prompt or request for Opus 5.
- Skill applies it by: Adds no manual chain-of-thought scaffolding by default; thinking is already active.

### BP-219 Disable only at effort high or lower
- Kind: model-note
- Rule: On Claude Opus 5, thinking can be disabled only at effort high or lower.
- Guide says: "On Claude Opus 5, you can disable it only at effort `high` or lower."
- Applies when: A request asks to run Opus 5 with thinking disabled.
- Skill applies it by: Pairs any disable with effort `high` or lower and prefers keeping thinking on at a lower effort (O5-62).

### BP-227 Prefer thinking on at lower effort over the manual CoT fallback
- Kind: model-note
- Rule: On Claude Opus 5, keep thinking enabled at a lower effort instead of using the manual CoT fallback, because disabled thinking can leak internal XML tags into visible output.
- Guide says: "On Claude Opus 5, prefer keeping thinking enabled at a lower effort level instead: with thinking disabled, the model can occasionally emit internal XML tags into its visible output, so see [Running with thinking disabled](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) before applying this pattern there."
- Applies when: Prompt authoring for Opus 5 where the user considers turning thinking off or adding CoT tags.
- Skill applies it by: Never applies the `<thinking>`/`<answer>` output-tag pattern on Opus 5; recommends thinking on with lower effort in the Target model item.

### BP-228 Link: Running with thinking disabled
- Kind: link
- Rule: Read 'Running with thinking disabled' before applying the CoT pattern to Claude Opus 5.
- Guide says: "[Running with thinking disabled](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled)"
- Applies when: Any Opus 5 deliverable that disables thinking.
- Skill applies it by: Section 8 Related pages; the section's rules are O5-60 to O5-69 above.

### BP-229 Self-check instruction (Opus 5 excepted)
- Kind: technique
- Rule: Append a self-check instruction asking Claude to verify its answer against stated criteria before finishing.
- Guide says: "**Ask Claude to self-check.** Append something like \"Before you finish, verify your answer against \\[test criteria].\" This catches errors reliably, especially for coding and math."
- Applies when: Every rearticulated prompt except those whose target model is Claude Opus 5.
- Skill applies it by: On Opus 5 the `<verification>` tag is omitted; `<success_criteria>` stays and Step 7 still checks against it.

### BP-230 Sample: self_check_verify (not grafted on Opus 5)
- Kind: sample-prompt
- Rule: Use the guide's self-check phrasing with the placeholder replaced by the task's concrete criteria.
- Guide says: see snippet self_check_verify; the text is "Before you finish, verify your answer against \\[test criteria]."
- Applies when: Filling `<verification>` for any model other than Claude Opus 5.
- Skill applies it by: Not grafted when the target is Opus 5.

### BP-232 Opus 5 needs no verification instructions
- Kind: model-note
- Rule: Do not add explicit verification instructions for Claude Opus 5; it self-verifies well and carried-over instructions cause over-verification.
- Guide says: "Claude Opus 5 is the exception: it verifies its own work well without explicit instruction, and verification instructions carried over from prompts tuned for earlier models can cause over-verification, adding tokens and latency."
- Applies when: The target model is Opus 5 (in-session or authored).
- Skill applies it by: Template rule: omit `<verification>`; section 5: remove verification instructions from pasted prompts.

### BP-233 Remove, do not rewrite, when migrating to Opus 5
- Kind: migration
- Rule: When migrating a prompt to Claude Opus 5, remove verification instructions rather than rewriting them.
- Guide says: "When migrating to Claude Opus 5, remove these instructions rather than rewriting them. See [Task scope and over-verification](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#task-scope-and-over-verification)."
- Applies when: A pasted prompt tuned for an earlier model is retargeted to Opus 5.
- Skill applies it by: Deletes verification instructions outright and records the removal in the Changed line.

### BP-234 Link: Task scope and over-verification
- Kind: link
- Rule: Consult 'Task scope and over-verification' on the Opus 5 page for the full over-verification guidance.
- Guide says: "[Task scope and over-verification](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#task-scope-and-over-verification)"
- Applies when: Any Opus 5 prompt-authoring or migration deliverable.
- Skill applies it by: Section 8 Related pages; the section's rules are O5-42 to O5-47 above.

### BP-287 Opus 5 delegates more readily
- Kind: model-note
- Rule: Know that Claude Opus 5 also delegates to subagents more readily than prior models.
- Guide says: "Claude Opus 5 also delegates to subagents more readily than prior models; see [Controlling subagent spawning](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning) for guidance and a sample damping prompt."
- Applies when: Authoring a prompt for Claude Opus 5 whose task is simple or sequential.
- Skill applies it by: Grafts o5_delegation_guidance (the page's damping prompt) in place of the guide's generic subagent_usage_policy.

### BP-288 Link: Controlling subagent spawning
- Kind: link
- Rule: Consult the Opus 5 Controlling subagent spawning sub-page for guidance and a sample damping prompt.
- Guide says: "[Controlling subagent spawning](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning)"
- Applies when: Subagent overuse is a concern on Opus 5.
- Skill applies it by: Section 8 Related pages; the section's rules are O5-48 to O5-55 above.

### BP-366 Next steps card for this page
- Kind: link
- Rule: Consult 'Prompting Claude Opus 5' for Opus 5 differences covering response verbosity, agentic narration, task scoping, subagent delegation, and self-correction.
- Guide says: "<Card title=\"Prompting Claude Opus 5\" icon=\"terminal\" href=\"https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5\"> Behavioral differences and prompting patterns for Claude Opus 5, covering response verbosity, agentic narration, task scoping, subagent delegation, and self-correction. </Card>"
- Applies when: The target model is Opus 5.
- Skill applies it by: Cited as the source of this file; no prompt text change by itself.

## When this is the TARGET model: add to the rearticulated prompt

The content of the rearticulated prompt follows this section when the target is Opus 5, whether the prompt runs in-session or is authored for an application. The Fable 5.1 default snippets (progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule) are not grafted; their Opus 5 counterparts are named below.

Target model item (SKILL.md Step 5 assumptions). Always `Target model: opus-5 (<how resolved>)`. When the target differs from the executing model, the request is prompt authoring, or the user asked about speed, cost, or thinking, append: recommended effort with the page section cited (default `high`, O5-14; `low` or `medium` for routine work and first review passes, O5-11, O5-13, O5-15; `xhigh` for demanding coding and agentic work, O5-16; any carried-over effort marked unverified, O5-17); thinking on by default, disable only at `high` or below, syntax in the migration guide (O5-60); `budget_tokens` removed with the 400 reason (BP-189); sampling parameters flagged "check against the Opus 4.7 to Opus 5 migration guide" (O48-05 via the baseline); subagent caps named as environment-level controls (O5-52, O5-53); model string `claude-opus-5` when API code is produced (BP-059, BP-085). Any snippet borrowed from the Opus 4.8 baseline is marked "text measured on Prompting Claude Opus 4.8".

- `<role>`: one sentence per the guide. For an authored system prompt add model_identity with "Claude Opus 5" as printed (BP-081, BP-082) and, for LLM-powered apps, model_string with `claude-opus-5` (BP-084, BP-085).
- `<context>`: name the consumer of the output, because the conciseness and correction-narration rules depend on whether the output is user-facing (O5-30, O5-58). For office deliverables name the house style or template that section `<constraints>` carries (O5-24). No context-length reminders: the 1M window is consistent throughout (O5-22).
- `<documents>`: guide rules unchanged (BP-062). Long documents go in whole, without chunking instructions (O5-22).
- `<task>`: the complete specification up front, every requirement and acceptance criterion gathered in Step 2, no mid-task check-ins, no stub or TODO allowances (O5-08); full feature scope in one task for multi-file work (O5-07). Code review: "report every issue you find, tagged with severity", then a final ranked or filtered section or a second pass (O5-12), with the coverage sentence borrowed from o48_review_coverage. Vision: state the expected output plainly and allow crop, zoom, re-render and compare (O5-19, O5-21). Multi-agent: per-agent ownership, no conflict-avoidance rules (O5-25). Principle-level instructions rather than enumerated behaviour lists.
- `<constraints>`: o5_scope_constraint verbatim for narrow tasks (single-file change, one named target, "just do X"); omitted for open-ended exploration (O5-45 to O5-47). A `<template>` or `<style_requirements>` block for spreadsheets and decks with a house style (O5-24). When the task involves choosing a model, the default is overridable (BP-086).
- `<output_format>`: an explicit length or shape on every Opus 5 prompt (O5-29, BP-096, BP-017). o5_conciseness for chat-style or user-facing output (O5-30, O5-31, BP-094); o5_deliverable_length whenever the output is a file, even alongside o5_conciseness (O5-39 to O5-41); o5_correction_narration for user-facing products or when the user wants clean output (O5-58, O5-59). Positive descriptions of the wanted style rather than what to avoid (O5-38). For long-form prose the guide's avoid_excessive_markdown_and_bullet_points applies (formatting_in_chat_rule is Fable 5.1 only).
- `<examples>`: when the user wants narration tuned up or restyled, one or two example update lines (O5-37); positive examples of communication style (O5-38). Otherwise guide rules.
- `<success_criteria>`: guide rules; it stays even though `<verification>` is omitted, and any check the user insists on becomes a criterion here rather than a re-check instruction (O5-57). Review prompts: every finding carries a severity tag and the final section ranks them (O5-12). Documents: the stated length target is a checkable criterion (O5-40).
- `<execution_guidance>`: o5_progress_updates for tool-heavy tasks (O5-34 to O5-36) in place of progress_updates_line. o5_delegation_guidance when the harness supports subagents and the system prompt is custom or omitted, or the workload is cost-sensitive (O5-48 to O5-51, O5-54, BP-287); not in-session under the `claude_code` preset. o5_thinking_disabled_mitigation only when thinking must stay off (O5-67, O5-68). Tool-based inspection for vision (O5-21). No self-check, reflect-and-verify, or "verify with a subagent" blocks (O5-42 to O5-44, O5-56). No batch_nudge (measured on Fable 5.1). The guide's use_parallel_tool_calls, investigate_before_answering, and temp_file_cleanup apply as the taxonomy row requires.
- `<verification>`: omitted (O5-42 to O5-44, BP-232). Any verification or double-check instruction in a pasted prompt is removed, not rewritten (O5-43, O5-57, BP-233). The prompt states deliverable length, task scope, and subagent policy explicitly instead (BP-017).
- Closing block: tone_preference last when the prompt is long and a conciseness instruction appears earlier (O5-32, O5-33).

Reasoning exhortations: hand-written reasoning plans are dropped and effort is recommended in the Target model item (O5-14 to O5-16). No `<thinking>` output tags on Opus 5 (BP-227). If thinking is disabled, also strip "respond directly" and "do not reason" lines including think_only_when_useful (O5-66), graft o5_thinking_disabled_mitigation (O5-68), and recommend thinking on at `low` (O5-62).

Design and frontend: inherited from the Opus 4.8 baseline (frontend_aesthetics_short plus a concrete spec or o48_propose_directions), marked "text measured on Prompting Claude Opus 4.8" in the Target model item. Under an autonomous block the skill picks one direction, states it in the Target model item, and continues rather than ending the turn.

## When this is the TARGET model: remove or convert

Each conversion is recorded in the Changed line of the assumptions.

| Found in the raw request or pasted prompt | Action for an Opus 5 target | Basis |
|---|---|---|
| "include a final verification step", "use a subagent to verify", "verify your work before finishing", legacy harness verify phases | Remove; do not rewrite or soften | O5-43, O5-44, BP-232, BP-233 |
| "double-check your answer", "re-verify before responding", "make sure you're right" | Remove; if the user insists, write a concrete acceptance criterion in `<success_criteria>` | O5-57 |
| "only report high-severity issues", "be conservative" in a review prompt | "Report every issue you find, tagged with severity" plus a final ranked section or a second filtering pass; coverage text borrowed from o48_review_coverage | O5-12 |
| "don't think", "no reasoning", "answer without thinking", and think_only_when_useful when thinking is disabled | Remove; speed or cost intent becomes an effort suggestion in the Target model item | O5-66 |
| "never output <thinking> tags" or any tag-named anti-leak rule | The general sentence from o5_thinking_disabled_mitigation | O5-69 |
| "turn thinking off to save tokens" | Thinking on at `low` effort, stated in the Target model item | O5-62, BP-227 |
| Thinking off together with `xhigh` effort | Flag the conflict; thinking cannot be disabled above `high` | O5-06, O5-60, BP-219 |
| Lowering effort to get shorter answers | Explicit length instruction in `<output_format>`; effort stays a cost lever | O5-28, BP-095 |
| "don't be chatty", "no fluff", "don't narrate" | Positive cadence description (o5_progress_updates) or a positive style example | O5-35, O5-38 |
| "leave TODOs for later", "stub out the rest", mid-task check-in requirements | Remove unless the user explicitly wants partial work | O5-08 |
| Legacy vision workarounds ("describe every region first", "zoom mentally") | Strip or flag; allow tool-based crop and verify instead | O5-20, O5-21 |
| An effort rationale hardcoded from a prior model | Flag as unverified; recommend an effort sweep | O5-17 |
| Chunking instructions or "remember the earlier instructions" added for context length | Remove; the 1M window is consistent throughout | O5-22 |
| Elaborate conflict-avoidance rules for subagent teams | Remove; state per-agent ownership | O5-25 |
| Hand-written step-by-step reasoning plans | Drop; recommend effort; numbered work steps whose order matters stay | O5-14 to O5-16, BP-221 |
| `<thinking>`/`<answer>` manual chain-of-thought output tags | Do not apply on Opus 5 | BP-227 |
| `budget_tokens`, `thinking: {type: "enabled"}` | Adaptive thinking plus `output_config.effort`; record the 400 reason | BP-189 |
| `temperature`, `top_p`, `top_k` | Flag "check against the Opus 4.7 to Opus 5 migration guide"; do not assert a value | O48-05, O48-06 via the baseline |
| "raise temperature for variety" in a design brief | o48_propose_directions from the baseline, marked as measured on Opus 4.8 | O48-53 via the baseline |
| An Opus 4.8-era prompt as a whole | Keep its substance; apply only the deltas in this table and section 4 | O5-05 |
| A subagent cap expressed as prose ("never spawn more than two") | Keep o5_delegation_guidance in the prompt and name the environment variables and `max_budget_usd` in the Target model item as the deterministic control | O5-50, O5-52 |

## When this is the EXECUTING model: how the skill behaves in Steps 5-7

Applies when the model running the skill resolves to Opus 5 (the Target model item then reads "executing model: opus-5"). SKILL.md Steps 6 and 7 are written for Fable 5.1; where this page differs, this section governs the skill's own behaviour. The rearticulated prompt's content still follows the target profile.

- Narration cadence: the o5_progress_updates cadence (O5-36). One sentence before the first tool call; a brief update only on an important finding or a change of direction; no per-batch updates. This replaces the Fable 5.1 "one-line update before each tool batch" sentence in Step 6 (O5-34, O5-35).
- Final message shape: lead with the outcome; the first sentence answers "what happened" or "what did you find", with supporting detail after it (O5-36). The Step 7 recap keeps its three-to-eight-line shape and order, and stays fact-based (BP-089). The skill's own visible text follows o5_conciseness: disclaimers short, most of the text on the answer (O5-27, O5-31).
- Verification loop: Step 7 reports the checks already performed and runs no prescribed re-check loop (O5-42, O5-56); `<success_criteria>` still governs the recap and the files-touched check.
- Self-correction narration: the skill corrects an earlier statement only when the error would change the user's code, conclusions, or decisions; slips that change nothing are fixed silently (O5-59).
- Subagent policy: delegate only large, independent, parallelizable tracks; finish small work directly; never spawn a subagent to verify or double-check (O5-49, O5-51). In interactive Claude Code the `claude_code` preset already carries a delegation instruction, so o5_delegation_guidance is not grafted in-session; it is grafted only in authored prompts or when the user says the system prompt is custom (O5-54). If the user wants hard limits, name the environment variables and `max_budget_usd` and the 2.1.217 floor in the reply (O5-52, O5-53).
- Scope: deliver what was asked at the scope intended; say in a sentence when the request seems mistaken and continue; stop short of actions clearly beyond the ask (O5-47). This matches Standing rule 7 and Step 1d.
- Formatting: guide defaults; formatting_in_chat_rule is not applied to the skill's own output. The Step 5 display budget is kept short, since Opus 5 tends to over-fill (BP-094).
- Edit style: Standing rule 11 (targeted edits) applies as skill behaviour; the targeted_edits snippet text is measured on Fable 5.1 and is not grafted.
- Search-before-answer: the page is silent; the guide's investigate_before_answering and Standing rule 6 apply.
- Progress grounding: fact-based, no self-evaluation (BP-089); the page adds nothing.
- Last-paragraph check: Step 7 as written; the page is silent.
- Refusal handling: the page is silent; if a request is declined, report it plainly and do not rephrase to get around it (guide default, BP-138). Refusal stop details are in the Opus 4.7 to Opus 5 migration guide (O48-05).
- Context-count handling: the 1M window holds instruction following throughout (O5-22); do not wrap up early, trim, or propose a new session because of length; no compaction reminder is needed.
- Effort follow-up: when a run was slow but correct, suggest `low` or `medium` for similar work in the recap (O5-13, O5-15); for demanding coding suggest `xhigh` (O5-16). Effort is never proposed as a way to shorten output (O5-28).
- Thinking-disabled session: if the session runs with thinking off, expect tool calls to leak as text on tool-heavy work (O5-63, O5-64); if the skill notices its own tool call rendered as text, re-issue it as a structured call and say so; no internal tags in visible output (O5-65, O5-68).
- Vision work: inspect with tools (crop, zoom, re-render) rather than relying on thinking (O5-21).
- Harness-injected blocks to skip in-session: the preset's delegation instruction (O5-54); the Fable 5.1 batch_nudge is not a default here.

## Snippets

IDs only; verbatim text lives in `references/snippet-library.md`. All measured on Claude Opus 5 unless marked.

- o5_conciseness (O5-31) - `<output_format>`, chat-style or user-facing output.
- tone_preference (O5-33) - final block of a long prompt; keeps its XML wrapper.
- o5_progress_updates (O5-36) - `<execution_guidance>`, tool-heavy tasks; also the skill's own cadence when executing as Opus 5.
- o5_deliverable_length (O5-41) - `<output_format>`, any file-producing task.
- o5_scope_constraint (O5-47) - `<constraints>`, narrow tasks.
- o5_delegation_guidance (O5-51) - `<execution_guidance>`, subagent-capable harnesses with a custom or omitted system prompt, or cost-sensitive work; the Opus 5 form of subagent_usage_policy (BP-287).
- o5_correction_narration (O5-59) - `<output_format>`, user-facing products.
- o5_thinking_disabled_mitigation (O5-68) - `<execution_guidance>`, only when thinking must stay off.
- model_identity, model_string (BP-081, BP-084; guide snippets whose printed text names Opus 5) - `<role>` of authored system prompts.
- Borrowed from the Opus 4.8 baseline when needed, marked as measured on Opus 4.8: o48_review_coverage, o48_review_concrete_bar, o48_explicit_scope, frontend_aesthetics_short, o48_propose_directions, o48_aefrm_concrete_spec.
- Not grafted on Opus 5: self_check_verify (BP-230), progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule (all measured on Fable 5.1), subagent_usage_policy (replaced by o5_delegation_guidance), think_only_when_useful when thinking is disabled (O5-66), context_compaction_persistence and spend_entire_context (O5-22).

## Not covered by this page

The skill falls back to the main guide (`references/technique-catalog.md`) for: XML structure and tag order; role prompting; long-context ordering (BP-062); examples; positive format control and the list exception; plain-text math; prefill migration; parallel tool calls; hallucination controls (investigate_before_answering); state tracking across context windows; autonomy and safety confirmations; research structure; file-creation hygiene; frontend design (inherited via the Opus 4.8 profile); computer use (not on this page; the Opus 4.8 and Sonnet 5 pages print toolset strings for those models only, so do not assert them for Opus 5). The page prints no disable syntax for thinking, no sampling-parameter rule, no tokenizer note, no `max_tokens` figure, no refusal behaviour, no tone or writing-style section, and no effort default beyond naming `high`; cite the linked pages rather than asserting those.

Related pages (do not import their content; name them in the Target model item when a fact is needed):
- What's new in Claude Opus 5, https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5 (capabilities and API changes; O5-02, BP-011, BP-006).
- Migration guide, Opus 4.8 to Opus 5, https://platform.claude.com/docs/en/models/opus-5/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5 (thinking on by default, disable capped at high; O5-06, O5-60).
- Migration guide, Opus 4.7 to Opus 5, https://platform.claude.com/docs/en/models/opus-5/migration-guide#migrating-from-opus-47 (sampling parameters, effort default, 1M default, mid-conversation system messages, refusal stop details; O48-05, O48-06).
- Effort, recommended levels for Claude Opus 5, https://platform.claude.com/docs/en/build-with-claude/effort#recommended-effort-levels-for-claude-opus-5 (O5-18).
- Context windows, https://platform.claude.com/docs/en/build-with-claude/context-windows (O5-22).
- Thinking, https://platform.claude.com/docs/en/build-with-claude/thinking, and Thinking, steering and cost, https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost (O5-28, O5-60).
- Cap subagent depth, concurrency, and spend, https://code.claude.com/docs/en/agent-sdk/subagents#cap-subagent-depth-concurrency-and-spend (O5-55).
- Prompting Claude Opus 5, sections Response length and verbosity, Task scope and over-verification, Controlling subagent spawning, Running with thinking disabled (BP-097, BP-234, BP-288, BP-228).
- Prompting Claude Opus 4.8 (the baseline profile, `references/models/opus-4-8.md`).
