# Claude Fable 5.1 and Claude Mythos 5.1

Source: Prompting Claude Fable 5.1, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
Snapshot date: 2026-09-08. Rule IDs F51-01 to F51-152 (the Fable 5.1 deltas section of `references/technique-catalog.md`). Lines 74 to 753 of the snapshot are SDK code samples; their facts are distilled into F51-51 and F51-52 and the code itself is not reproduced.

Profile: `fable-5-1`. Aliases: fable-5.1, fable51, fable-5-1, mythos-5.1, mythos-5-1, claude-fable-5-1, claude-mythos-5-1. Everything on this page applies to Claude Mythos 5.1 as well (F51-01).

Baseline: `fable-5`; page basis: "Your existing Claude Fable 5 prompts should perform well on Claude Fable 5.1 without changes, but a handful of behavioral differences are worth knowing about." Inheritance rule: a Fable 5 rule or `f5_*` snippet carries over to this profile unless a section on this page covers the same topic, in which case this page supersedes it. Topics this page covers: effort, progress updates, tool-call batching, conversation history, writing density, formatting in chat, quoting sources, finishing the task, compaction summaries, scope of changes and tests, search triggering, safeguard false positives, file edits, long outputs, subagents, vision (F51-01). When a Fable 5 snippet is borrowed for a topic this page does not cover (giving the reason, memory systems, send_to_user, grounded progress claims), the Target model item records "text measured on the Fable 5 page".

This is the default executing model in this workspace (the Claude Code session model). Section 6 is written in full and SKILL.md Steps 6 and 7 mirror it. In-session the Target model item reads `Target model: fable-5-1 (executing model)` and carries nothing else (the user, not the prompt, sets effort and thinking).

## Identity and API facts

- API string: `claude-fable-5-1` (F51-52). Display names: Claude Fable 5.1, Claude Mythos 5.1.
- Thinking: always on; adaptive thinking is the only mode; the `thinking` parameter cannot turn it off (guide, "Leverage thinking & interleaved thinking capabilities": "On Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, and Claude Mythos 5, thinking is always on and adaptive thinking is the only mode."). `budget_tokens` returns a 400, as on every 4.7 and later model (guide, BP-189).
- Effort: default `high`; the page names five levels: `low`, `medium`, `high`, `xhigh`, `max` (F51-23). Effort is the primary control for intelligence, latency, and cost (F51-24). Re-run the sweep when arriving from Fable 5, because level names do not map to the same amount of thinking across models (F51-25); an effort level is never carried from another profile. Gains over Fable 5 are largest at the higher settings (F51-26); `medium` roughly matches Fable 5 at lower cost (F51-27); `low` is often competitive with Opus and Sonnet on cost per task while scoring higher (F51-28). Two effort-specific behaviours: fewer search calls at `low` (F51-29), longer thinking before a long deliverable at `xhigh` and `max` (F51-30).
- `max_tokens`: at `xhigh` or `max` leave room for the thinking and the reply, not only the reply (F51-140); the long-output budget note substitutes the request's real `max_tokens`, for example 64,000 (F51-141).
- Sampling parameters and tokenizer: not printed on this page. Capabilities, API changes, pricing, and availability live on What's new in Claude Fable 5.1, https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1 (F51-02); the skill does not restate them from memory.
- Refusals: the model runs safety classifiers and can return `stop_reason: "refusal"` (F51-22, F51-128). False positives are fewer than Fable 5's at launch, and finding vulnerabilities in source code is permitted (F51-127). Three situations raise the false-positive rate: compile-check phrasing, lesser-known programming languages, base64 in tool output (F51-129 to F51-131). Fallback and billing: Refusals, fallback, and billing, https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1#refusals-fallback-and-billing.
- Prefill: unsupported on the last assistant turn, as on every 4.6 and later model (guide, BP-124, BP-352).
- Progress-update thinking blocks: empty under the default `thinking.display` of `"omitted"`; request them with `display: "updates"` (beta header `thinking-display-updates-2026-08-18`) or `"summarized"` (F51-33, F51-34).
- Turn-scoped system messages: a `role: "system"` entry in `messages` with `clear_at: "next_user_message"`; beta header `mid-conversation-system-clear-at-2026-08-21`; earlier copies are cleared once a later user message exists and cost no input tokens (F51-45 to F51-49).
- Thinking block binding: for accounts created on or after August 31, 2026, thinking blocks are valid only in the exact conversation that produced them; replaying one after its prefix changed returns a 400, or drops the block when `thinking.block_binding.prefix_mismatch_behavior: "drop_block"` is set (beta header `thinking-binding-controls-2026-08-01`); future models are expected to enforce the check for all accounts (F51-54 to F51-57).
- Pricing note used by this page: cache reads are cheaper, so early compaction may no longer pay off (F51-63).

### Harness and environment notes

These reach a rearticulated prompt only through the harness-authoring, async-agent, and computer-use taxonomy rows; in-session the skill only informs the user.

- Progress display: set `thinking.display` to `"updates"` or `"summarized"` before adding prompt text about updates (F51-32 to F51-34).
- Hidden tool output: when the product collapses tool output, deliver `tool_output_hidden_note` as a turn-scoped system message (F51-38, F51-39). Claude Code is such a product; SKILL.md Standing rule 8 carries the note's content.
- Agent loop shape: each assistant turn goes back exactly as returned, each user turn carries only the tool results, a fresh turn-scoped copy of `batch_nudge` follows it; without the beta, the nudge goes in a text block after the `tool_result` blocks (F51-45 to F51-52).
- Append-only history and the diagnostic recipe (`drop_block` plus `input_transformations` logging, or byte-identical request capture) (F51-53 to F51-64).
- Subagent harness: the start tool returns immediately, results arrive in a later `user` message, a separate wait tool exists (F51-145 to F51-147). In Claude Code, subagents launched in the background and the task notification are the equivalents.
- Vision: a container with the raw images and PIL or OpenCV, or a crop tool that returns a region cropped and enlarged; crop tool recipe https://platform.claude.com/cookbook/multimodal-crop-tool (F51-150 to F51-152). In Claude Code, Python via Bash serves as the container.
- Claude Code already injects its own parallel-calls reminder each turn; the prompt states batching once, in `batch_nudge` (guide, BP-174).

## Behavioural deltas

One entry per page rule, in page order. "Page says" quotes the page verbatim; sample prompts are shortened and point to the snippet ID in `references/snippet-library.md`.

Page section: front matter and symptom index (F51-01 to F51-22).

### F51-01 Page scope
- Kind: fact
- Rule: Treat this page as the authority on Fable 5.1 behavioural deltas across effort, progress updates, tool-call batching, conversation history, writing style, formatting, task completion, compaction summaries, scope and tests, search triggering, safeguard false positives, file edits, long outputs, subagents, and vision.
- Page says: "Behavioral differences and prompting patterns for Claude Fable 5.1 and Claude Mythos 5.1, covering effort, progress updates, tool-call batching, conversation history, writing style, formatting, task completion, compaction summaries, scope and test coverage, search triggering, safeguard false positives, file edits, long outputs, subagents, and vision."
- Applies when: The executing model is Fable 5.1 (the session model) or Mythos 5.1, or the user authors a prompt for either.
- Skill applies it by: This profile's sections mirror the fifteen topics; the taxonomy defaults to this profile because the session model is Fable 5.1; a user naming Mythos 5.1 gets the same profile.

### F51-02 What's new page for non-prompting facts
- Kind: link
- Rule: Send questions about capabilities, API changes, pricing, and availability to the What's new page, not to this prompting page.
- Page says: "For the model's capabilities, API changes, pricing, and availability, see [What's new in Claude Fable 5.1](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1)."
- Applies when: The raw request asks about capabilities, pricing, or availability rather than prompting behaviour.
- Skill applies it by: Section 2 cites the URL; the skill verifies such facts against that page instead of restating them from memory.

### F51-03 Cross-model guide is primary
- Kind: link
- Rule: Use the Prompting best practices guide for techniques that apply across all models; this page holds only Fable 5.1 specifics.
- Page says: "For techniques that apply across Claude models, see [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)."
- Applies when: Always.
- Skill applies it by: The technique catalog is built from the guide; F51 entries layer on top and never replace a general technique.

### F51-04 Fable 5 prompts carry over
- Kind: migration
- Rule: Carry existing Fable 5 prompts to Fable 5.1 unchanged and adjust only for the listed behavioural differences.
- Page says: "Your existing Claude Fable 5 prompts should perform well on Claude Fable 5.1 without changes, but a handful of behavioral differences are worth knowing about. Start with the section that matches what you observe:"
- Applies when: The user pastes a prompt written for Fable 5 or asks to migrate one.
- Skill applies it by: Step 4 keeps the pasted prompt's substance and applies only the F51 deltas (remove anti-formatting and narration-suppressing lines, add the finish-the-task and keep-changes blocks when the row calls for them); the Changed line says the base prompt was kept.

### F51-05 Diagnose by symptom
- Kind: technique
- Rule: Apply only the section whose symptom matches what is observed rather than grafting every block at once.
- Page says: "Start with the section that matches what you observe:"
- Applies when: Choosing which F51 blocks to graft.
- Skill applies it by: The symptom index below (F51-06 to F51-21) is the symptom-to-fix table; a block is grafted only when the request type or an observed symptom in the conversation matches its row. This is also why Step 5 keeps the displayed prompt proportional.

### F51-06 Symptom: effort, latency, cost
- Kind: model-note
- Rule: When unsure which effort level to run, or latency and cost exceed what the task warrants, apply the effort section.
- Page says: "Unsure which effort level to run, or latency and cost are higher than the task warrants: [Consider all effort levels]"
- Applies when: The user asks about effort, latency, or cost for Fable 5.1.
- Skill applies it by: The skill sets no effort itself (no effort override in frontmatter); it includes the F51-23 to F51-30 guidance in the Target model item when authoring for another caller or when the user asks.

### F51-07 Symptom: silence between tool calls
- Kind: model-note
- Rule: When there is little or no text between tool calls, apply the progress-updates section.
- Page says: "Little or no text between tool calls: [Ask for user-facing progress updates]"
- Applies when: The user says the agent goes quiet, or the task will involve a long tool chain.
- Skill applies it by: `progress_updates_line` is default-on for every tool-using run on this model; Step 6 applies it.

### F51-08 Symptom: one tool call per turn
- Kind: model-note
- Rule: When an agent loop issues one tool call per turn, apply the batching section.
- Page says: "One tool call per turn in agent loops: [Batch independent tool calls in agent loops]"
- Applies when: Multi-file or multi-lookup execution, or advice on a coding harness.
- Skill applies it by: `batch_nudge` closes every tool-using rearticulated prompt; Step 6 batches independent calls.

### F51-09 Symptom: bound to a different conversation
- Kind: model-note
- Rule: When requests fail with `bound to a different conversation` or the harness edits earlier turns, apply the append-only history section.
- Page says: "Requests fail with `bound to a different conversation`, or your harness edits earlier turns between requests: [Keep the conversation history append-only]"
- Applies when: The user debugs a harness that replays thinking blocks, or quotes that error string.
- Skill applies it by: Step 1 recognises the literal string as a harness-authoring signal and routes to F51-53 to F51-64.

### F51-10 Symptom: dense prose
- Kind: model-note
- Rule: When prose runs long and dense, apply the writing-density section.
- Page says: "Prose runs long and dense: [Writing density]"
- Applies when: Writing or report requests, or the user says the output is too dense.
- Skill applies it by: The writing row grafts `mannered_prose_definition` or `mannered_prose_short` into `<output_format>`.

### F51-11 Symptom: too little structure in chat
- Kind: model-note
- Rule: When chat replies carry less structure than the content needs, apply the formatting-in-chat section.
- Page says: "Chat replies carry less structure than the content needs: [Formatting in chat]"
- Applies when: Multifaceted answers come back as undifferentiated prose.
- Skill applies it by: `formatting_in_chat_rule` in `<output_format>`; the anti-formatting strip in Step 4.

### F51-12 Symptom: unmarked source wording
- Kind: model-note
- Rule: When summaries reproduce source wording without marking it as a quotation, apply the quoting section.
- Page says: "Summaries reproduce source wording without marking it as a quotation: [Quoting retrieved sources]"
- Applies when: Summarisation or comparison of retrieved or attached text.
- Skill applies it by: The long-document and research rows graft `quoting_sources_example` as a single example.

### F51-13 Symptom: turn ends early or asks permission
- Kind: model-note
- Rule: When the turn ends before the work is done, or the model asks permission for work already requested, apply the finish-the-whole-task section.
- Page says: "Turn ends before the work is done, or the model asks permission for work you already requested: [Finish the whole task]"
- Applies when: Agentic requests, and the skill's own same-turn contract.
- Skill applies it by: The SKILL.md contract (the turn ends after Step 7) and the autonomy blocks in `<execution_guidance>`.

### F51-14 Symptom: compaction drops details
- Kind: model-note
- Rule: When client-side compaction summaries drop constraints, decisions, or exact details, apply the compaction-summary section.
- Page says: "Client-side compaction summaries drop constraints, decisions, or exact details: [Tell the model what to preserve in compaction summaries]"
- Applies when: Multi-session work with progress notes, or a user building a compacting harness.
- Skill applies it by: Progress notes for multi-session work follow the six preservation items; `compaction_summary_instruction` is grafted for client-side compaction and transcript summaries.

### F51-15 Symptom: unrequested changes and tests
- Kind: model-note
- Rule: When there are unrequested fixes or extensions, or more committed test files than the task called for, apply the keep-changes section.
- Page says: "Unrequested fixes or extensions, or more committed test files than the task called for: [Keep changes and tests to what the task asks for]"
- Applies when: Code-change requests.
- Skill applies it by: `keep_changes_to_task` is mandatory in `<constraints>` for the code-change row.

### F51-16 Symptom: answering from memory at low effort
- Kind: model-note
- Rule: When the model answers from memory instead of searching at low effort, apply the search-triggering section.
- Page says: "Answers from memory instead of searching at low effort: [Search triggering at low effort]"
- Applies when: Research requests naming products, tools, models, or people, especially at low effort.
- Skill applies it by: The research row grafts `search_name_as_written`.

### F51-17 Symptom: refusal on benign coding requests
- Kind: model-note
- Rule: When benign coding requests return `stop_reason: "refusal"`, apply the safeguard section.
- Page says: "Benign coding requests return `stop_reason: \"refusal\"`: [Reduce safeguard false positives]"
- Applies when: Security-shaped or compiler-shaped coding questions, obscure languages, base64 in tool output.
- Skill applies it by: Step 4 rewrites compile-check phrasing; `<context>` adds language context; base64 goes to files.

### F51-18 Symptom: whole-file rewrites
- Kind: model-note
- Rule: When whole files are rewritten for small changes, apply the targeted-edits section.
- Page says: "Whole files rewritten for small changes: [Prefer targeted edits over whole-file rewrites]"
- Applies when: Any code or text edit task.
- Skill applies it by: `targeted_edits` for edit tasks; Standing rule 11 and Step 6 use targeted edits.

### F51-19 Symptom: long deliverables at xhigh or max
- Kind: model-note
- Rule: When long deliverables at `xhigh` or `max` take a long time or hit `max_tokens`, apply the long-outputs section.
- Page says: "Long deliverables at `xhigh` or `max` effort take a long time or hit `max_tokens`: [Leave room for long outputs at xhigh and max effort]"
- Applies when: Long documents, large tables, or complete files at high effort settings.
- Skill applies it by: The long-deliverable signal in Step 1c triggers `long_output_budget_note` as the prompt's last element before `batch_nudge`.

### F51-20 Symptom: lead idles while subagents run
- Kind: model-note
- Rule: When the lead agent idles while subagents run, apply the subagents section.
- Page says: "Lead agent idles while subagents run: [Let the lead agent keep working while subagents run]"
- Applies when: The task delegates to subagents, or the user builds a multi-agent harness.
- Skill applies it by: The subagent policy block adds the lead-keeps-working sentence.

### F51-21 Symptom: vision misses detail
- Kind: model-note
- Rule: When answers about charts and dense images miss detail, apply the vision section.
- Page says: "Answers about charts and dense images miss detail: [Give vision work tools to crop and zoom]"
- Applies when: Vision or data-extraction requests over images.
- Skill applies it by: The vision row adds crop-and-zoom guidance to `<execution_guidance>`.

### F51-22 Safety classifiers and refusal stop reason
- Kind: fact
- Rule: Expect Fable 5.1 to run safety classifiers and to be able to return `stop_reason: "refusal"`.
- Page says: "Claude Fable 5.1 runs safety classifiers and can return `stop_reason: \"refusal\"`. See [Refusals, fallback, and billing](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1#refusals-fallback-and-billing) and [Reduce safeguard false positives]"
- Applies when: Any request, most of all security-flavoured coding tasks, which are routine in this workspace.
- Skill applies it by: Section 2 records the note and link; rearticulation phrases security questions per F51-127 to F51-131 so the executed prompt is less likely to trip a classifier; a refusal is reported plainly, never rephrased around (section 6).

Page section: Consider all effort levels (F51-23 to F51-30).

### F51-23 Start at high, sweep the rest
- Kind: technique
- Rule: Start at the default effort level `high`, then test `low`, `medium`, `xhigh`, and `max` against your own evals.
- Page says: "Start at the default [effort](https://platform.claude.com/docs/en/build-with-claude/effort) level, `high`, then test the other levels (`low`, `medium`, `xhigh`, and `max`) against your own evals."
- Applies when: Choosing effort for an API integration, or a user asks which effort to use.
- Skill applies it by: Section 2 records `high` as the default; when a request asks for effort guidance, the Target model item recommends starting at `high` and sweeping against evals rather than guessing.

### F51-24 Effort is the primary control
- Kind: fact
- Rule: Treat effort as the primary control for trading off intelligence, latency, and cost.
- Page says: "Effort is the primary control for trading off intelligence, latency, and cost on Claude Fable 5.1."
- Applies when: Any cost or latency tuning question.
- Skill applies it by: When the user wants a Fable 5.1 workload cheaper or faster, the rearticulated prompt directs the executor to effort first, not prompt trimming.

### F51-25 Re-run the sweep from Fable 5
- Kind: migration
- Rule: Re-run the effort sweep when moving from Fable 5, because effort level names do not map to the same amount of thinking across models.
- Page says: "Re-run the sweep even if you already ran one on Claude Fable 5: effort level names don't correspond to the same amount of thinking across models."
- Applies when: Migrating an integration from Fable 5 to Fable 5.1, or any time the target profile changes.
- Skill applies it by: The migration checklist in the prompt-authoring row includes "re-run the effort sweep"; an effort level is never copied from another profile's Target model item.

### F51-26 Gains at every level, largest at the top
- Kind: fact
- Rule: Expect Fable 5.1's gains over Fable 5 at every effort level, largest at the higher settings.
- Page says: "Claude Fable 5.1's capability gains over Claude Fable 5 show up across effort levels and are largest at the higher settings."
- Applies when: Explaining or choosing effort.
- Skill applies it by: Section 2 fact, cited when the executor answers effort questions.

### F51-27 Medium as the first step down
- Kind: technique
- Rule: Step down to `medium` or `low` where evals show quality holds, since `medium` roughly matches Fable 5 at lower cost.
- Page says: "At `medium`, results roughly match Claude Fable 5 at lower cost, so step down to `medium` or `low` where your evals show quality holds."
- Applies when: Cost optimisation with evals available.
- Skill applies it by: Cost-tuning prompts tell the executor to propose `medium` as the first step-down candidate.

### F51-28 Low effort versus smaller models
- Kind: fact
- Rule: Include Fable 5.1 at `low` in any comparison where a smaller model at higher effort is the alternative.
- Page says: "At `low`, Claude Fable 5.1 is often competitive with Claude Opus and Claude Sonnet models on cost per task while scoring higher, so include it in the comparison wherever you'd otherwise run a smaller model at a higher effort level."
- Applies when: Model-selection questions weighing Fable 5.1 against Opus or Sonnet.
- Skill applies it by: The executor cites it when a request asks which model to use for a cheap task.

### F51-29 Fewer search calls at low
- Kind: model-note
- Rule: Remember that at `low` effort Fable 5.1 calls search and retrieval tools less often.
- Page says: "at `low`, Claude Fable 5.1 calls search and retrieval tools less often (see [Search triggering at low effort]"
- Applies when: Research tasks at low or unknown effort.
- Skill applies it by: The research row grafts `search_name_as_written` whenever effort is low or unknown names appear.

### F51-30 Longer thinking before long deliverables
- Kind: model-note
- Rule: Remember that at `xhigh` and `max` Fable 5.1 can think for longer before writing a long deliverable.
- Page says: "at `xhigh` and `max` it can think for longer before writing a long deliverable (see [Leave room for long outputs at xhigh and max effort]"
- Applies when: Long deliverables at high effort settings.
- Skill applies it by: The writing row grafts `long_output_budget_note`.

Page section: Ask for user-facing progress updates (F51-31 to F51-39).

### F51-31 Fewer user-facing updates by default
- Kind: model-note
- Rule: Expect fewer user-facing updates during long tool-calling turns than Fable 5, more so at higher effort and in longer chains.
- Page says: "Claude Fable 5.1's default behavior is to write fewer user-facing updates during long tool-calling turns than Claude Fable 5 does. This becomes more pronounced at higher effort and in longer tool chains. Users see the agent go quiet for minutes at a time, or a final message that covers only the last step rather than the whole task."
- Applies when: Any tool-heavy execution, including the skill's own execution half.
- Skill applies it by: Steps 6 and 7 counteract it: an opening line, a one-line update before each tool batch and a short note after it, and a recap that covers the whole task rather than the last step.

### F51-32 Check the client first
- Kind: technique
- Rule: Before changing the prompt, check that the client actually receives progress updates.
- Page says: "First, check that your client receives progress updates at all."
- Applies when: A user reports the agent goes quiet in their own API integration.
- Skill applies it by: For that request the rearticulated prompt orders the diagnostic steps: client display setting first, prompt audit second, added instruction third.

### F51-33 Updates arrive as thinking blocks
- Kind: fact
- Rule: Between-tool-call notes arrive as progress-update thinking blocks, which are empty under the default `thinking.display` of `"omitted"`.
- Page says: "The model's short notes between tool calls, what it just found and what it's doing next, come back as [progress-update `thinking` blocks](https://platform.claude.com/docs/en/build-with-claude/thinking#progress-updates), and those blocks are empty under the default `thinking.display` of `\"omitted\"`."
- Applies when: Debugging progress updates in an API client.
- Skill applies it by: Section 2 API fact with the link; not actionable inside Claude Code.

### F51-34 Request updates or summarized display
- Kind: fact
- Rule: Set `display: "updates"` (beta header `thinking-display-updates-2026-08-18`) and render each non-empty thinking block as a status line, or set `"summarized"`.
- Page says: "Set `display: \"updates\"` (beta, `thinking-display-updates-2026-08-18` header) and render each non-empty `thinking` block as a status line, or set `\"summarized\"` to receive them along with summarized reasoning. If you aren't requesting them, the model's updates may simply not be reaching your users."
- Applies when: Building or debugging an API client that should show progress.
- Skill applies it by: Section 2 API fact; included in prompts that author harness code for Fable 5.1.

### F51-35 Remove narration suppressors first
- Kind: anti-pattern
- Rule: Remove system prompt lines that suppress narration, such as "hold all findings for the final response", before adding anything else.
- Page says: "Second, audit your prompt for instructions that suppress narration. Some earlier models were eager to give updates while working, which led to system prompt lines such as \"hold all findings for the final response.\" Remove lines like that before adding anything."
- Applies when: A pasted prompt or the raw request contains narration-suppressing language and the target is Fable 5.1.
- Skill applies it by: Step 4 strips "hold all findings for the final response" and "keep progress text brief" style lines; the Changed line records the removal.

### F51-36 Add a short progress line for human-in-the-loop work
- Kind: technique
- Rule: If more updates are wanted, add a short system prompt line saying when user-facing text is wanted and what each update should contain.
- Page says: "If you still want more updates, for example when pair programming or in other human-in-the-loop work, add a short system prompt line that says when you want user-facing text from the model and what each update should contain:"
- Applies when: Pair programming and other human-in-the-loop work, which includes every attended /rearticulate run.
- Skill applies it by: `progress_updates_line` opens `<execution_guidance>` on every tool-using run for this profile; Step 6 applies it literally.
- Snippet: progress_updates_line

### F51-37 The progress line
- Kind: sample-prompt
- Rule: Say in one line what you are about to do, give brief updates while working, and close with a recap that stands on its own.
- Page says: see snippet progress_updates_line; "Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so a reader who only sees the last message has the full picture."
- Applies when: Any tool-using execution a human follows.
- Skill applies it by: Grafted into `<execution_guidance>` first on every run; Step 7's recap order (found, done, next) is the snippet's closing clause.
- Snippet: progress_updates_line

### F51-38 Tell the model when tool output is hidden
- Kind: technique
- Rule: Tell the model when the product collapses or hides tool output, otherwise it may run commands to show output the UI never displays; deliver the note as a turn-scoped system message.
- Page says: "If your product collapses or hides tool output, tell the model. Otherwise it may run commands to \"show\" the user output that your UI never displays. Deliver the note in a [turn-scoped system message](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) (`clear_at: \"next_user_message\"`, beta):"
- Applies when: Claude Code (command output is shown to the model and only partly to the user) and any harness that hides tool output.
- Skill applies it by: SKILL.md Standing rule 8: command output is visible to Claude, not reliably to the user, so anything the user must read goes in the reply, and no command is run only to display output.
- Snippet: tool_output_hidden_note

### F51-39 The hidden-output note
- Kind: sample-prompt
- Rule: Put anything the user needs to read from a command's output into the reply, since only the model sees the full output.
- Page says: see snippet tool_output_hidden_note; "Only you see that command's output — the user's terminal shows at most a few lines of it. If the user needs to read any of it, put it in your reply."
- Applies when: Executing shell commands in Claude Code or any UI that collapses tool output.
- Skill applies it by: Adopted as Standing rule 8 rather than grafted per prompt; grafted verbatim only when authoring a harness prompt.
- Snippet: tool_output_hidden_note

Page section: Batch independent tool calls in agent loops (F51-40 to F51-52).

### F51-40 Parallel calls when items are named
- Kind: model-note
- Rule: Expect parallel tool calls when a request explicitly names several things to fetch.
- Page says: "Claude Fable 5.1 usually issues parallel tool calls as expected: when a request names several things to fetch, it issues those calls in parallel."
- Applies when: Rearticulating requests that touch several files or sources.
- Skill applies it by: `<task>` enumerates the files and lookups explicitly so the default parallel behaviour engages.

### F51-41 One per turn when calls are implied
- Kind: model-note
- Rule: Expect one-call-per-turn behaviour in coding and computer-use loops where the next independent calls are implied rather than named.
- Page says: "The exception is coding and computer-use loops where the next independent calls are implied by the task rather than explicitly requested (custom coding agents, bash-and-editor harnesses, computer use): there it may issue them one per turn instead."
- Applies when: Code-change and agentic tasks in Claude Code, which is a bash-and-editor harness.
- Skill applies it by: The code-change and agentic rows make the batching block mandatory; Step 6 batches independent calls.

### F51-42 Serial calls cost time, not quality
- Kind: fact
- Rule: Treat serial tool calls as a cost and latency problem, not a quality problem.
- Page says: "This doesn't affect answer quality, but each extra turn costs tokens, a round trip, and wall-clock time."
- Applies when: Weighing whether to add the batching nudge.
- Skill applies it by: Motivation sentence available for `<context>` when `batch_nudge` is grafted and the user questions it.

### F51-43 One-sentence nudge at the end
- Kind: technique
- Rule: Add a one-sentence batching nudge at the end of the current request.
- Page says: "A one-sentence nudge at the end of the current request addresses it:"
- Applies when: Any execution with several independent reads, searches, or checks.
- Skill applies it by: `batch_nudge` is the last line of the whole rearticulated prompt.
- Snippet: batch_nudge

### F51-44 The batch nudge
- Kind: sample-prompt
- Rule: Privately list what is needed next, then request every item that does not depend on another's result in one response.
- Page says: see snippet batch_nudge; "First privately list what you need next; then request every item that doesn't depend on another's result in this one response."
- Applies when: Every tool-using execution turn.
- Skill applies it by: Grafted as the closing line; Step 6 obeys it literally.
- Snippet: batch_nudge

### F51-45 Re-append the nudge as a turn-scoped system message
- Kind: technique
- Rule: Each time tool results go back, append the nudge after that user message as a `role: "system"` entry with `clear_at: "next_user_message"`.
- Page says: "Each time you send tool results back, append it after that user message as a [turn-scoped system message](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages): a `role: \"system\"` entry in `messages` with `clear_at: \"next_user_message\"`."
- Applies when: Authoring an API agent loop for Fable 5.1.
- Skill applies it by: Section 2 API pattern; grafted into prompts that write or review a harness loop.

### F51-46 The API clears earlier copies
- Kind: fact
- Rule: Rely on the API to clear earlier turn-scoped copies once a later user message exists.
- Page says: "Once a later user message exists, the API clears the earlier copies, so the model reads only the newest one."
- Applies when: Designing per-turn reminders in an API harness.
- Skill applies it by: Section 2 API fact.

### F51-47 Beta header for turn-scoped messages
- Kind: fact
- Rule: Send the beta header `mid-conversation-system-clear-at-2026-08-21` to use turn-scoped system messages.
- Page says: "Turn-scoped system messages are in beta and require the [beta header](https://platform.claude.com/docs/en/api/beta-headers) `mid-conversation-system-clear-at-2026-08-21`."
- Applies when: Harness authoring for Fable 5.1.
- Skill applies it by: Section 2 quotes the exact header so executor-written code uses it verbatim.

### F51-48 Fallback without the beta
- Kind: technique
- Rule: Without the beta, place the nudge in a text block after the `tool_result` blocks in the same user message.
- Page says: "Without the beta, place the sentence in a text block after the `tool_result` blocks in the same user message instead."
- Applies when: Harness authoring without beta access.
- Skill applies it by: Section 2 fallback pattern for harness-authoring prompts.

### F51-49 Fresh copy each turn, old copies untouched
- Kind: technique
- Rule: Append a fresh copy of the nudge each turn and leave earlier copies in place byte-for-byte.
- Page says: "Append a fresh copy each turn and leave the earlier copies where they are, byte-for-byte. They stay in the array, but once cleared the model doesn't see them and they cost no input tokens."
- Applies when: Harness authoring with turn-scoped system messages.
- Skill applies it by: Section 2 pattern; the zero-input-token fact is kept so the executor does not "optimise" old copies away.

### F51-50 Never delete or rewrite old copies
- Kind: anti-pattern
- Rule: Never delete or rewrite earlier turn-scoped copies; that edits earlier turns, restarts the prompt cache, and invalidates later thinking blocks.
- Page says: "Deleting or rewriting them is an edit to earlier turns: it restarts the [prompt cache](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) from that point and invalidates the thinking blocks that came after them"
- Applies when: Harness authoring or review.
- Skill applies it by: The executor flags such deletions when reviewing harness code.

### F51-51 Loop shape
- Kind: fact
- Rule: Each assistant turn goes back exactly as returned, each user turn carries only the tool results, and a fresh turn-scoped nudge follows it.
- Page says: "The following loop shows this placement. Each assistant turn goes back exactly as returned, each user turn carries only the tool results, and a fresh turn-scoped copy of the nudge follows it."
- Applies when: Harness authoring for Fable 5.1.
- Skill applies it by: Section 2 loop shape; the SDK samples are not reproduced.

### F51-52 SDK loop facts
- Kind: fact
- Rule: Call the beta messages endpoint with model `claude-fable-5-1` and the `mid-conversation-system-clear-at-2026-08-21` beta, append `response.content` unchanged as the assistant turn, loop while `stop_reason` is `tool_use`, return `tool_result` blocks (with `is_error` true for failures) as the user turn, then append `{role: system, content: nudge, clear_at: next_user_message}`.
- Page says: "messages.append({\"role\": \"assistant\", \"content\": response.content}) if response.stop_reason != \"tool_use\": break ... messages.append({\"role\": \"user\", \"content\": tool_results}) messages.append({\"role\": \"system\", \"content\": BATCH_NUDGE, \"clear_at\": \"next_user_message\"})"
- Applies when: The executor writes or reviews an API agent loop for Fable 5.1.
- Skill applies it by: Section 2 facts distilled from the SDK samples (snapshot lines 74 to 753); the code itself is not copied into the skill.

Page section: Keep the conversation history append-only (F51-53 to F51-64).

### F51-53 Append turns exactly as returned
- Kind: technique
- Rule: Append each assistant turn exactly as the API returned it, thinking blocks included, and never edit earlier turns between requests.
- Page says: "Append each assistant turn to the history exactly as the API returned it, thinking blocks included, and don't edit earlier turns between requests."
- Applies when: Any API harness for Fable 5.1.
- Skill applies it by: Grafted into prompts about harness design or the "bound to a different conversation" symptom; SKILL.md Standing rule 12 applies the same principle in-session.

### F51-54 Thinking blocks bound to their conversation
- Kind: fact
- Rule: For accounts created on or after August 31, 2026, thinking blocks are valid only in the exact conversation that produced them.
- Page says: "For new accounts created on or after August 31, 2026, Claude Fable 5.1's thinking blocks are valid [only in the exact conversation that produced them](https://platform.claude.com/docs/en/build-with-claude/thinking#preserved-in-conversation)"
- Applies when: Harness authoring; explaining 400 errors on replay.
- Skill applies it by: Section 2 fact with date and link.

### F51-55 Prefix change returns 400
- Kind: fact
- Rule: Expect a 400 when a request replays a thinking block after its prefix (system prompt, tool list, or any earlier message) has changed.
- Page says: "a request that replays a thinking block after its prefix (the system prompt, the tool list, or any earlier message) has changed returns a 400"
- Applies when: Debugging replay failures.
- Skill applies it by: The executor uses it to diagnose the "bound to a different conversation" symptom.

### F51-56 drop_block option
- Kind: fact
- Rule: Set `thinking.block_binding.prefix_mismatch_behavior: "drop_block"` (beta header `thinking-binding-controls-2026-08-01`) to drop affected blocks instead of failing.
- Page says: "or drops the affected blocks if you set `thinking.block_binding.prefix_mismatch_behavior: \"drop_block\"` (beta, `thinking-binding-controls-2026-08-01` header)"
- Applies when: Harness authoring where prefix changes cannot be avoided.
- Skill applies it by: Section 2 API fact with the exact parameter path and header.

### F51-57 Adopt append-only now
- Kind: migration
- Rule: Adopt append-only history now even if the account is not yet enforced.
- Page says: "Future models are expected to enforce this check for all accounts, so adopt the pattern now even if yours isn't enforced today."
- Applies when: Any harness work.
- Skill applies it by: Migration checklist item.

### F51-58 Three history edits that trip the check
- Kind: anti-pattern
- Rule: Avoid injecting and removing per-turn reminders, summarizing older turns in place, and changing the system prompt mid-session.
- Page says: "The history edits that trip the check are the same ones that restart the [prompt cache](https://platform.claude.com/docs/en/build-with-claude/prompt-caching): injecting and removing per-turn reminders, summarizing older turns in place, or changing the system prompt mid-session."
- Applies when: Reviewing or authoring harness code.
- Skill applies it by: The executor flags each of the three when reviewing harness code; F51-59 to F51-61 hold the replacements.

### F51-59 Reminders as turn-scoped messages
- Kind: technique
- Rule: Send per-turn reminders as turn-scoped system messages instead of injecting and removing them.
- Page says: "Send per-turn reminders as [turn-scoped system messages](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages)"
- Applies when: Harness authoring.
- Skill applies it by: Replacement pattern paired with the injected-reminder anti-pattern.

### F51-60 Mid-conversation system message for changes
- Kind: technique
- Rule: Change instructions or tools with a mid-conversation system message rather than rewriting `system` or `tools`.
- Page says: "change instructions or tools with a [mid-conversation system message](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages) instead of rewriting `system` or `tools`"
- Applies when: Harness authoring where instructions change mid-session.
- Skill applies it by: Replacement pattern paired with the system-prompt-rewrite anti-pattern.

### F51-61 Server-side trimming
- Kind: technique
- Rule: Let server-side compaction or context editing do any trimming rather than summarizing turns in place.
- Page says: "and let server-side [compaction](https://platform.claude.com/docs/en/build-with-claude/compaction) or [context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing) do any trimming."
- Applies when: Harness authoring with long conversations.
- Skill applies it by: Replacement pattern paired with the in-place-summary anti-pattern.

### F51-62 Client compaction shape
- Kind: technique
- Rule: If compacting on the client, replace the whole history with one summary message plus the new user turn and replay nothing else.
- Page says: "If you compact on the client, the simplest shape is to replace the whole history with one summary message plus the new user turn and replay nothing else: no thinking blocks carry over, so nothing fails, and the model thinks afresh on the compacted conversation (see [Custom compaction on the client](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#custom-compaction-on-the-client))."
- Applies when: Client-side compaction in a Fable 5.1 harness.
- Skill applies it by: Pattern paired with `compaction_summary_instruction` for the summary's content.

### F51-63 Compact later
- Kind: technique
- Rule: Experiment with later compaction points, since cheaper cache reads weaken the case for early compaction.
- Page says: "Because cache reads are now cheaper (see [Pricing](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1#pricing)), compacting early to save cost may no longer be the right cost-intelligence tradeoff on Claude Fable 5.1, so experiment with later compaction points."
- Applies when: Tuning compaction thresholds.
- Skill applies it by: Advice with the pricing link, included in harness-tuning prompts.

### F51-64 Find hidden history edits
- Kind: technique
- Rule: Find hidden history edits by running with `prefix_mismatch_behavior: "drop_block"` and logging `input_transformations`, or by capturing raw requests and confirming consecutive requests are byte-identical up to the appended turns.
- Page says: "To find edits your harness already makes, run a session with `prefix_mismatch_behavior: \"drop_block\"` and log `input_transformations`, as described in [How to tell whether your integration is impacted](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#how-to-tell-whether-your-integration-is-impacted), or capture the exact requests it sends over a few normal turns and confirm that consecutive requests are byte-identical up to the appended turns."
- Applies when: Auditing an existing harness for Fable 5.1 compatibility.
- Skill applies it by: The harness-audit prompt includes both checks as numbered steps with the link.

Page section: Writing density (F51-65 to F51-70).

### F51-65 Fewer stock phrases
- Kind: model-note
- Rule: Expect fewer stock phrases and less unexplained jargon than earlier models.
- Page says: "Claude Fable 5.1's writing is generally a step up from earlier Claude models, with fewer stock phrases and less unexplained jargon."
- Applies when: Writing tasks.
- Skill applies it by: No generic "avoid cliches" instruction is added for this profile; the default is already improved.

### F51-66 Denser prose in some cases
- Kind: model-note
- Rule: Expect denser prose than Fable 5 in some cases: longer sentences and fewer paragraph breaks.
- Page says: "In some cases, though, its prose is denser than Claude Fable 5's: sentences run longer and there are fewer paragraph breaks."
- Applies when: Writing and report requests.
- Skill applies it by: The writing row adds an `<output_format>` line about sentence length and paragraph breaks and grafts the mannered-prose snippet.

### F51-67 Define the anti-pattern in the user message
- Kind: technique
- Rule: Add an instruction that defines mannered prose to the user message (preferred) or the system prompt.
- Page says: "An instruction that defines the anti-pattern, mannered prose, helps. Add it to a user message (preferred) or the system prompt:"
- Applies when: Writing deliverables where tone matters.
- Skill applies it by: The snippet goes inside the rearticulated prompt's `<output_format>`, which is the user-message position.
- Snippet: mannered_prose_definition

### F51-68 The mannered-prose definition
- Kind: sample-prompt
- Rule: Define mannered prose and instruct the model to say what it means with literal phrases.
- Page says: see snippet mannered_prose_definition; "Mannered prose substitutes metaphor and flourish for direct statement. ... The fix is to say what you mean. When a literal phrase is available, use it."
- Applies when: Writing, report, memo, or summary requests.
- Skill applies it by: Grafted into `<output_format>` for the writing row; consistent with the workspace's no-dramatic-language reporting style.
- Snippet: mannered_prose_definition

### F51-69 Short version when length matters
- Kind: fact
- Rule: Use the one-line version when prompt length matters.
- Page says: "The short version also tends to work:"
- Applies when: Compact prompts, or when the rearticulated prompt is already long.
- Skill applies it by: `mannered_prose_short` is the fallback in the template's default snippets.
- Snippet: mannered_prose_short

### F51-70 The short version
- Kind: sample-prompt
- Rule: Ask for removal of all mannered prose.
- Page says: see snippet mannered_prose_short; "Please remove all mannered prose."
- Applies when: Any writing request where the long definition is unnecessary.
- Skill applies it by: Default graft for short writing requests.
- Snippet: mannered_prose_short

Page section: Formatting in chat (F51-71 to F51-74).

### F51-71 Legacy anti-formatting rules
- Kind: model-note
- Rule: Recognise that earlier models overused bullets and bold and that many prompts carry anti-formatting rules written for them.
- Page says: "Earlier models overused bullets and bold in chat, and many prompts carry anti-formatting rules written to hold that down."
- Applies when: A pasted prompt contains anti-formatting rules.
- Skill applies it by: Step 4 identifies anti-formatting language in pasted prompts as a legacy artefact.

### F51-72 Fable 5.1 under-formats
- Kind: model-note
- Rule: Expect Fable 5.1 to use bold less and to reach for headers, lists, or quotation marks less often.
- Page says: "Claude Fable 5.1 leans the other way: it uses bold less and is less likely to reach for headers, lists, or quotation marks."
- Applies when: Formatting decisions for this profile's output.
- Skill applies it by: `<output_format>` states positively when lists, headers, or tables are wanted instead of restricting them.

### F51-73 Remove or replace anti-formatting language
- Kind: anti-pattern
- Rule: Remove anti-formatting language from prompts for Fable 5.1, or replace it with a rule saying when specific formatting is appropriate.
- Page says: "If your prompt contains anti-formatting language, remove it or replace it with a rule that says when specific formatting is appropriate, such as the following:"
- Applies when: The target is Fable 5.1 and the raw request or pasted prompt says "no bullets", "no markdown", or similar without a stated user preference.
- Skill applies it by: Step 4 removes the block or replaces it with `formatting_in_chat_rule`; a minimal-formatting request the user made themselves stays, because the rule honours it.
- Snippet: formatting_in_chat_rule

### F51-74 The formatting rule
- Kind: sample-prompt
- Rule: Use lists when asked or when content is multifaceted, honour explicit minimal-formatting requests, and keep plain prose in conversational or emotional exchanges.
- Page says: see snippet formatting_in_chat_rule; "Use lists and bullet points when asked to, or when the content is multifaceted enough that they help with clarity. If the person explicitly requests minimal formatting, always format your responses without bullet points, headers, lists, or bold emphasis, as requested. In conversational, personal, or emotional exchanges, keep to plain prose."
- Applies when: Chat-style output on this profile.
- Skill applies it by: Default `<output_format>` formatting rule for this profile; other profiles use `avoid_excessive_markdown_and_bullet_points` from the guide.
- Snippet: formatting_in_chat_rule

Page section: Quoting retrieved sources (F51-75 to F51-78).

### F51-75 Unmarked source passages
- Kind: model-note
- Rule: Expect Fable 5.1 to reproduce source passages without marking them as quotations more often than Fable 5 when summarizing.
- Page says: "When summarizing documents, Claude Fable 5.1 is more likely than Claude Fable 5 to reproduce passages of the source text without marking them as quotations."
- Applies when: Summarisation of retrieved or attached documents.
- Skill applies it by: The long-document and research rows add to `<success_criteria>`: "source wording appears only as marked quotations; every other claim is reworded".

### F51-76 One complete example
- Kind: technique
- Rule: Add one complete example of a correct response: the user's request, the response, and a sentence explaining why it is correct.
- Page says: "To address this, add one complete example of a correct response to the system prompt: the user's request, the response, and a sentence explaining why the response is correct."
- Applies when: Summarisation or comparison tasks over sources.
- Skill applies it by: `<examples>` accepts this single user/response/rationale example, an exception to the 3 to 5 default.
- Snippet: quoting_sources_example

### F51-77 The quoting example
- Kind: sample-prompt
- Rule: Show a response organised by agreement and difference, conveying each source in indirect speech, with one short marked quotation.
- Page says: see snippet quoting_sources_example; "<example> <user>look up how the Riverton Ledger and the Coast Dispatch each covered the Harbor Bridge closure and compare their reporting</user> <response> [web_search: Harbor Bridge closure Riverton Ledger] ... </response> <rationale>CORRECT: ... One short marked phrase from one source; every other claim is reworded. ...</rationale> </example>"
- Applies when: Research or document-comparison requests whose output is a summary.
- Skill applies it by: Grafted into `<examples>` with the `[web_search: ...]` lines swapped for the tool in use (WebSearch, WebFetch, or Read in Claude Code).
- Snippet: quoting_sources_example

### F51-78 Substitute the tool name
- Kind: technique
- Rule: Replace the two `[web_search: ...]` lines with the actual tool's name so the model reads them as templated tool output.
- Page says: "Replace the two `[web_search: ...]` lines with your own tool's name, so the model reads them as templated tool output rather than literal text to emit."
- Applies when: Grafting the quoting example.
- Skill applies it by: Snippet graft note: substitute the tool name before inserting.
- Snippet: quoting_sources_example

Page section: Finish the whole task (F51-79 to F51-102).

### F51-79 Long tasks with little methodology
- Kind: model-note
- Rule: Expect Fable 5.1 to execute very long tasks with little methodology guidance when the goal is clear.
- Page says: "Claude Fable 5.1 can execute very long tasks without much guidance on methodology, especially when the goal is clear."
- Applies when: Agentic long-horizon requests.
- Skill applies it by: Rearticulation invests in a clear goal and `<success_criteria>` rather than step-by-step methodology.

### F51-80 Nudge on asynchronous workloads
- Kind: technique
- Rule: On complex asynchronous workloads, nudge the model not to end its turn before the work is done.
- Page says: "On complex asynchronous workloads, though, nudge it not to end its turn before the work is done."
- Applies when: Long autonomous tasks, and the skill's own same-turn contract.
- Skill applies it by: `operating_autonomously` for unattended runs; the SKILL.md contract forbids ending after the rewrite.
- Snippet: operating_autonomously

### F51-81 Describing instead of doing
- Kind: model-note
- Rule: Watch for the model describing what it would do next instead of doing it.
- Page says: "Without the nudge, the model sometimes describes what it would do next instead of doing it (\"Next, I'll …\")"
- Applies when: Execution half of every run.
- Skill applies it by: Step 7 last-paragraph check: a plan or promise means do the work before ending.

### F51-82 Asking permission for covered work
- Kind: model-note
- Rule: Watch for the model stopping to ask permission for a step the original request already covered.
- Page says: "or stops to ask permission for a step the original request already covered (\"Shall I apply this?\")"
- Applies when: Execution half of every run.
- Skill applies it by: Standing rule 9: reversible in-scope actions proceed; follow-ups are offered after the work, not permission before it.

### F51-83 Continue loops waste capability
- Kind: fact
- Rule: Recognise that "continue" and "go ahead" loops suit pair programming but waste long-horizon capability.
- Page says: "Users have to reply \"continue\" or \"go ahead,\" which suits pair programming and other human-in-the-loop work but doesn't use the model's full long-horizon capability."
- Applies when: Deciding how autonomous the rearticulated prompt should be.
- Skill applies it by: The agentic row defaults to the act posture with autonomy blocks; the assessment row does not.

### F51-84 Apply both blocks, first alone if short
- Kind: technique
- Rule: Apply both system prompt additions; if prompt length must be limited, keep only the first, which retains most of the effect.
- Page says: "Two system prompt additions together mitigate this. Apply both. If you need to limit prompt length, use only the first, which keeps most of the effect."
- Applies when: Grafting autonomy guidance.
- Skill applies it by: For unattended runs `operating_autonomously` is the mandatory half and `delivering_work` the second when length allows; for attended runs see section 4 (the interactive graft rule).
- Snippet: operating_autonomously

### F51-85 Purpose of the first block
- Kind: fact
- Rule: The first block tells the model not to ask about work already requested and to carry out the next steps it has stated.
- Page says: "The first tells the model not to ask about work already requested and to carry out the next steps it has stated:"
- Applies when: Describing the autonomy block.
- Skill applies it by: Catalog summary line for `operating_autonomously`.
- Snippet: operating_autonomously

### F51-86 The operating-autonomously block
- Kind: sample-prompt
- Rule: Operate autonomously, proceed on reversible in-scope actions, stop only for destructive or scope changes, treat questions as assessment requests, and finish stated next steps before ending the turn.
- Page says: see snippet operating_autonomously; "You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work. For reversible actions that follow from the original request, proceed without asking. Stop only for destructive actions or genuine scope changes the user must decide. ... Exception: when the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. ... Before ending your turn, check your last paragraph. ... Before running a command that changes system state (such as restarts, deletes, or config edits), check that the evidence actually supports that specific action. ..."
- Applies when: Agentic and code-change requests under the act posture.
- Skill applies it by: Whole and unparaphrased for unattended runs (background, scheduled, or the user says run without asking). For attended runs in Claude Code the user is watching, so the opening sentence would be false and F51-91 forbids paraphrasing it; the skill then grafts `delivering_work` whole and takes paragraphs two to four of this block (the exception, the last-paragraph check, evidence before state changes), which are true in either setting. Recorded in the Changed line.
- Snippet: operating_autonomously

### F51-87 Reversible actions proceed
- Kind: technique
- Rule: For reversible actions that follow from the original request, proceed without asking; stop only for destructive actions or genuine scope changes.
- Page says: "For reversible actions that follow from the original request, proceed without asking. Stop only for destructive actions or genuine scope changes the user must decide. Offering follow-ups after the task is done is fine; asking permission before doing the work is not."
- Applies when: Execution half of every run.
- Skill applies it by: Standing rule 1; follow-ups go in the recap, never as permission requests mid-task.
- Snippet: operating_autonomously

### F51-88 Questions get an assessment
- Kind: technique
- Rule: When the user is describing a problem, asking a question, or thinking out loud, deliver an assessment and stop without applying a fix.
- Page says: "Exception: when the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one."
- Applies when: Step 1 posture test.
- Skill applies it by: Step 1d and the assessment row; the Reading line states which posture was chosen; under assess, no file changes.
- Snippet: operating_autonomously

### F51-89 Last-paragraph check
- Kind: technique
- Rule: Before ending, check the last paragraph; if it is a plan, analysis, question, next-steps list, or promise, do that work now, including retries and gathering missing information.
- Page says: "Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ('I'll…', 'let me know when…'), do that work now with tool calls. That includes retrying after errors and gathering missing information yourself. Do not stop because the context or session is long. End your turn only when the task is complete or you are blocked on input only the user can provide."
- Applies when: Step 7 of every run.
- Skill applies it by: Step 7 and Standing rule 9; the skill never ends after the rewrite unless the run is a dry run.
- Snippet: operating_autonomously

### F51-90 Evidence before state changes
- Kind: technique
- Rule: Before a state-changing command (restart, delete, config edit), confirm the evidence supports that specific action.
- Page says: "Before running a command that changes system state (such as restarts, deletes, or config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause."
- Applies when: Any execution that mutates system or repo state.
- Skill applies it by: Standing rule 4; `<verification>` lists evidence-before-mutation for destructive steps.
- Snippet: operating_autonomously

### F51-91 Keep the opening sentence as written
- Kind: technique
- Rule: Keep the opening sentence about the user not watching exactly as written, since it carries much of the effect.
- Page says: "The opening sentence, which tells the model the user isn't watching, carries much of the effect. Keep it as written."
- Applies when: Grafting `operating_autonomously`.
- Skill applies it by: The first sentence is never paraphrased; when it would be false (attended run) the block is not grafted whole and section 4's interactive rule applies instead.
- Snippet: operating_autonomously

### F51-92 List required confirmations
- Kind: technique
- Rule: If specific confirmations are required, add a sentence after the opening listing them.
- Page says: "If your product needs the model to stop for specific confirmations, add a sentence after it listing them."
- Applies when: Tasks with external side effects (sending, deleting, deploying, publishing, live API writes).
- Skill applies it by: Step 1f flags `[confirm]` steps; a sentence naming them follows the block's first paragraph: "Stop and ask in the chat before: <the confirm steps>, and before any destructive, hard-to-reverse, or visible-to-others action that emerges during the work."
- Snippet: operating_autonomously

### F51-93 Trade-off on ambiguous requests
- Kind: anti-pattern
- Rule: Check the trade-off that the autonomy block can make the model less likely to ask about ambiguous requests.
- Page says: "This block can also make the model less likely to ask about ambiguous requests, so check that trade-off on your own tasks."
- Applies when: Ambiguous raw requests receiving the autonomy block.
- Skill applies it by: Step 2 resolves ambiguity before the block is applied; when readings differ materially and a wrong guess would be unsafe, the question goes at the end of a turn that delivers the independent work rather than grafting full autonomy.
- Snippet: operating_autonomously

### F51-94 Purpose of the second block
- Kind: fact
- Rule: The second block defines the user's request as the scope of the deliverable.
- Page says: "The second defines the user's request as the scope of the deliverable:"
- Applies when: Describing `delivering_work`.
- Skill applies it by: Catalog summary line for `delivering_work`.
- Snippet: delivering_work

### F51-95 The delivering-work block
- Kind: sample-prompt
- Rule: Treat the request or approved plan as the scope and the deliverable, resolve routine ambiguity yourself, deliver every unblocked part, run decided steps instead of announcing them, and keep extras as end-of-task suggestions.
- Page says: see snippet delivering_work; "# Delivering work The user's request — or the plan they approved — sets the scope, and the scope is the deliverable: don't quietly narrow, widen, or swap it. ... A step you have decided on is something to run, not to announce ... Keep changes to what the request needs. ..."
- Applies when: Agentic and code-change requests; always for attended runs (section 4).
- Skill applies it by: Grafted whole into `<execution_guidance>` (or `<constraints>` when the prompt is short); its ambiguity rule is the source of Step 2's materially-different test.
- Snippet: delivering_work

### F51-96 Scope is the deliverable
- Kind: technique
- Rule: Let the request or approved plan set the scope and never quietly narrow, widen, or swap it.
- Page says: "The user's request — or the plan they approved — sets the scope, and the scope is the deliverable: don't quietly narrow, widen, or swap it."
- Applies when: Composing `<constraints>` on every run.
- Skill applies it by: `<constraints>` always states the scope as the deliverable; `<success_criteria>` includes "files created or modified: only <the files named in task>"; the recap reports any part not delivered.
- Snippet: delivering_work

### F51-97 Routine judgment calls
- Kind: technique
- Rule: Make routine judgment calls yourself and check in only when different readings would lead to materially different work.
- Page says: "Read ambiguity the way a careful colleague would: make routine judgment calls yourself, and check in only when different readings would lead to materially different work."
- Applies when: Step 2 golden-rule pass.
- Skill applies it by: Step 2: routine ambiguities get stated assumptions; only materially different readings that are unsafe to guess produce a question.
- Snippet: delivering_work

### F51-98 Voice a real problem, keep building
- Kind: technique
- Rule: If the task as specified has a real problem, say so in a sentence or two, keep building under stated assumptions, and deliver the full request if the user reaffirms.
- Page says: "If you see a real problem with the task as specified, say so in a sentence or two and keep building under stated assumptions; if the user hears the concern and reaffirms, that is their decision, so deliver the full request."
- Applies when: Execution reveals a flaw in the requested approach.
- Skill applies it by: Step 6: voice the concern briefly in the progress text, continue under stated assumptions, never silently substitute a different deliverable.
- Snippet: delivering_work

### F51-99 Questions at the end of a delivering turn
- Kind: technique
- Rule: When a question arises mid-task, first do everything independent of the answer, then state the assumption, or put the question at the end of a turn that also delivers progress when a wrong guess would be unsafe or useless.
- Page says: "If a question comes up partway, first do everything that doesn't depend on the answer; then state the assumption you made, or — when going ahead on a wrong guess would be unsafe or would make the work useless — put the question at the end of a turn that also delivers that progress."
- Applies when: Mid-execution blockers.
- Skill applies it by: Standing rule 1 and Step 2: questions go at the end of a turn that already delivers the independent work.
- Snippet: delivering_work

### F51-100 Name what was left out
- Kind: technique
- Rule: If one part is blocked, complete every other part in full and say exactly what was left out and why.
- Page says: "If one part turns out to be blocked, complete every other part in full and say exactly what you left out and why — the whole task is the deliverable, and scaling it down is the user's call, not yours."
- Applies when: Partial blockers during execution.
- Skill applies it by: Step 7's recap names any omitted part and the reason.
- Snippet: delivering_work

### F51-101 Run decided steps
- Kind: technique
- Rule: Run a step you have decided on rather than announcing it and ending the turn.
- Page says: "A step you have decided on is something to run, not to announce: describing the next step and ending the turn leaves it undone until the user replies."
- Applies when: Execution half of every run.
- Skill applies it by: The SKILL.md contract and Standing rule 9: showing the rewrite is not the end of the turn; decided steps run immediately.
- Snippet: delivering_work

### F51-102 Extras are suggestions
- Kind: technique
- Rule: Keep changes to what the request needs; unrequested cleanup, documentation, or changes to other files become end-of-task suggestions; clearly out-of-scope, risky, or destructive actions still need the user's go-ahead.
- Page says: "Keep changes to what the request needs. Something else you notice worth doing — cleanup or documentation the task didn't call for, a change to a file the task didn't require — is a suggestion to make at the end, not a change to make; actions clearly beyond what the ask implies, and risky or destructive ones, still need the user's go-ahead."
- Applies when: Code-change and agentic execution.
- Skill applies it by: `<constraints>` minimal scope; Standing rule 7; the recap carries a follow-ups list.
- Snippet: delivering_work

Page section: Tell the model what to preserve in compaction summaries (F51-103 to F51-113).

### F51-103 Responds to explicit preservation lists
- Kind: model-note
- Rule: Tell Fable 5.1 explicitly what a compaction summary must retain.
- Page says: "Claude Fable 5.1 responds well to being told explicitly what its summary must retain when a long conversation is compacted."
- Applies when: Long conversations that will be compacted or handed off.
- Skill applies it by: Multi-session progress notes reuse the preservation list.
- Snippet: compaction_summary_instruction

### F51-104 Server-side already does it
- Kind: fact
- Rule: Server-side compaction already preserves these items; add the instruction only for client-side compaction.
- Page says: "Server-side [compaction](https://platform.claude.com/docs/en/build-with-claude/compaction) already does this. If you compact on the client side, use the following summarization instruction:"
- Applies when: Deciding whether to graft the snippet.
- Skill applies it by: Graft only for client-side compaction harnesses, transcript-summary requests, or the skill's own handoff notes in multi-session work.
- Snippet: compaction_summary_instruction

### F51-105 The summarization instruction
- Kind: sample-prompt
- Rule: Summarize inside summary tags preserving problems and resolutions, options considered, decisions and constraints stated exactly, current status, open items, and hard-to-reconstruct details, keeping the user's words close and condensing your own reasoning.
- Page says: see snippet compaction_summary_instruction; "Summarize the transcript inside <summary></summary> tags. Include relevant information in the summary such that this conversation will be continued by a new context window without needing to redo work or be reprovided with relevant constraints or context. Be sure to preserve: (1) ... (6) ... Weight the two voices differently: ..."
- Applies when: Client-side compaction, session handoff notes, or a request to summarise a transcript or working session.
- Skill applies it by: Grafted verbatim for the transcript-summary sub-row and for compacting harnesses; its six items shape the multi-session progress-notes format.
- Snippet: compaction_summary_instruction

### F51-106 Preserve problems and resolutions
- Kind: technique
- Rule: Preserve any difficulties or problems that came up and how they were handled or resolved.
- Page says: "(1) any difficulties or problems that came up, and how they were handled or resolved;"
- Applies when: Writing handoff or compaction summaries.
- Skill applies it by: Progress-notes item 1.
- Snippet: compaction_summary_instruction

### F51-107 Preserve options considered
- Kind: technique
- Rule: Preserve possibilities, options, or approaches raised, tried, or set aside, and why.
- Page says: "(2) any possibilities, options, or approaches that were raised, tried, or set aside, and why;"
- Applies when: Writing handoff or compaction summaries.
- Skill applies it by: Progress-notes item 2.
- Snippet: compaction_summary_instruction

### F51-108 Preserve decisions exactly
- Kind: technique
- Rule: Preserve, stated exactly, anything asked for, decided, agreed, ruled out, or established as a preference, constraint, or boundary.
- Page says: "(3) anything that was asked for, decided, agreed, ruled out, or established as a preference, constraint, or boundary — stated exactly;"
- Applies when: Writing handoff or compaction summaries.
- Skill applies it by: Progress-notes item 3; the assumption lines record decisions verbatim for the same reason.
- Snippet: compaction_summary_instruction

### F51-109 Preserve current status
- Kind: technique
- Rule: Preserve exactly where things stand: what has been covered, settled, or completed.
- Page says: "(4) exactly where things stand now — what has been covered, settled, or completed so far;"
- Applies when: Writing handoff or compaction summaries.
- Skill applies it by: Progress-notes item 4; mirrors the recap's "done".
- Snippet: compaction_summary_instruction

### F51-110 Preserve open items
- Kind: technique
- Rule: Preserve anything still open, unresolved, promised, or expected next.
- Page says: "(5) anything still open, unresolved, promised, or expected to happen next;"
- Applies when: Writing handoff or compaction summaries.
- Skill applies it by: Progress-notes item 5; mirrors the recap's "next".
- Snippet: compaction_summary_instruction

### F51-111 Preserve hard-to-reconstruct details
- Kind: technique
- Rule: Preserve names, numbers, dates, exact wording, links, and references exactly.
- Page says: "(6) specific details that would be hard to reconstruct — names, numbers, dates, exact wording, links or references — kept exactly."
- Applies when: Writing handoff or compaction summaries.
- Skill applies it by: Progress-notes item 6.
- Snippet: compaction_summary_instruction

### F51-112 Complete on the six, concise elsewhere
- Kind: technique
- Rule: Be complete on the six preserved items even at the cost of length, and keep everything else concise.
- Page says: "Be complete on these even at the cost of length; keep everything else concise."
- Applies when: Writing handoff or compaction summaries.
- Skill applies it by: Progress-notes length rule.
- Snippet: compaction_summary_instruction

### F51-113 Weight the two voices
- Kind: technique
- Rule: Keep the user's words close to verbatim and condense your own reasoning to conclusions, as long as none of the six items is dropped.
- Page says: "Weight the two voices differently: keep what the user said, asked for, shared, or established carefully and close to their own words; your own explanations and reasoning can be condensed much further, to what they concluded or produced — as long as nothing in the six items above is dropped."
- Applies when: Writing handoff or compaction summaries.
- Skill applies it by: Progress-notes voice-weighting rule.
- Snippet: compaction_summary_instruction

Page section: Keep changes and tests to what the task asks for (F51-114 to F51-122).

### F51-114 Delivers more than asked
- Kind: model-note
- Rule: Expect Fable 5.1 to sometimes fix nearby code, extend unmentioned behaviour, or commit more test files than warranted on open-ended features.
- Page says: "When asked to implement an open-ended feature, Claude Fable 5.1 delivers what's asked for and sometimes more: it may fix nearby code, extend behavior the task didn't mention, or commit more test files than the change warrants."
- Applies when: Code-change requests.
- Skill applies it by: `keep_changes_to_task` is mandatory in `<constraints>` for the code-change row.
- Snippet: keep_changes_to_task

### F51-115 Responds to explicit exclusions
- Kind: fact
- Rule: Give explicit instructions about what to leave out.
- Page says: "It responds well to explicit instructions about what to leave out."
- Applies when: Composing `<constraints>` for code changes.
- Skill applies it by: `<constraints>` names the exclusions (follow-ups reported in the summary instead of fixed); the grafted snippet stays verbatim even though it is phrased negatively, because the positive-framing rule governs what the skill writes, not what it quotes.
- Snippet: keep_changes_to_task

### F51-116 Measured effect
- Kind: fact
- Rule: Expect unrequested additions and committed test code to drop substantially with no measurable change in task success.
- Page says: "With the following instruction, unrequested additions and committed test code drop substantially with no measurable change in task success:"
- Applies when: Justifying the snippet.
- Skill applies it by: Evidence note in the catalog.
- Snippet: keep_changes_to_task

### F51-117 The keep-changes block
- Kind: sample-prompt
- Rule: Do not fix or extend unrelated findings, implement the most direct reading of ambiguity and state it, keep scratch checks out of the repo, commit tests only where asked or conventional and sized like neighbours, and implement every requested behaviour completely.
- Page says: see snippet keep_changes_to_task; "If, while working or testing, you find a pre-existing bug, a performance concern, or behavior the task doesn't mention, don't fix, optimize or extend it in this change unless the requested behavior cannot work without it; report it as a follow-up in your summary. ... This is about extras only: implement every behavior the task asks for, completely."
- Applies when: Every code-change request.
- Skill applies it by: Grafted verbatim into `<constraints>` for the code-change row (default snippet in the template).
- Snippet: keep_changes_to_task

### F51-118 Report follow-ups, do not fix
- Kind: technique
- Rule: Report pre-existing bugs, performance concerns, or unmentioned behaviour as follow-ups instead of fixing them, unless the requested behaviour cannot work without the fix.
- Page says: "If, while working or testing, you find a pre-existing bug, a performance concern, or behavior the task doesn't mention, don't fix, optimize or extend it in this change unless the requested behavior cannot work without it; report it as a follow-up in your summary."
- Applies when: Code-change execution.
- Skill applies it by: Standing rule 7; the recap has a follow-ups section.
- Snippet: keep_changes_to_task

### F51-119 Implement the most direct reading
- Kind: technique
- Rule: Implement the reading the wording and surrounding code most directly support, state the assumption, and do not build for other readings.
- Page says: "Where the task is ambiguous, implement the reading its wording and the surrounding code most directly support, state that assumption in your summary, and don't build for the other readings as well."
- Applies when: Ambiguous code-change requests.
- Skill applies it by: Step 2 records the chosen reading in the Reading line.
- Snippet: keep_changes_to_task

### F51-120 Scratch checks need not be kept
- Kind: technique
- Rule: Verify however you like, but do not keep scratch scripts and quick checks.
- Page says: "Verify your work however you like; scratch scripts and quick checks need not be kept."
- Applies when: Ad-hoc verification during code changes.
- Skill applies it by: Scratch files live in the scratchpad directory and are removed before the recap (Standing rule 11).
- Snippet: keep_changes_to_task

### F51-121 Test policy
- Kind: technique
- Rule: Commit tests only where the task asks or the repository already keeps tests for this kind of change, sized like neighbouring tests at roughly one focused test per stated behaviour, never promoting scratch checks to permanent tests.
- Page says: "Commit tests only where the task asks for them or this repository already keeps tests for this kind of change, sized like the neighboring test files — roughly one focused test per stated behavior — and don't turn scratch checks into additional permanent test files."
- Applies when: Code changes involving tests.
- Skill applies it by: Step 1c detects the tests signal; `<constraints>` sets test policy per this rule.
- Snippet: keep_changes_to_task

### F51-122 Extras only; requested behaviour complete
- Kind: technique
- Rule: Implement every behaviour the task asks for completely; the exclusions apply to extras only.
- Page says: "This is about extras only: implement every behavior the task asks for, completely."
- Applies when: Every code-change request.
- Skill applies it by: `<success_criteria>` always includes completeness of the requested behaviours beside the no-extras constraint.
- Snippet: keep_changes_to_task

Page section: Search triggering at low effort (F51-123 to F51-126).

### F51-123 Answers from memory at low
- Kind: model-note
- Rule: Expect Fable 5.1 at `low` effort to call search or retrieval tools less than Fable 5 and to answer from memory more.
- Page says: "At `low` effort, Claude Fable 5.1 is less likely than Claude Fable 5 to call a search or retrieval tool, and more likely to answer from memory."
- Applies when: Research requests at low effort.
- Skill applies it by: The research row grafts `search_name_as_written` and a success criterion that claims are source-verified.
- Snippet: search_name_as_written

### F51-124 Raise effort for affected turns
- Kind: technique
- Rule: Where possible, raise effort for the affected turns rather than the whole conversation.
- Page says: "In some cases the simplest fix is to raise effort for the affected turns rather than the whole conversation. See [Change effort mid-conversation](https://platform.claude.com/docs/en/build-with-claude/effort#changing-effort-mid-conversation)."
- Applies when: API harnesses where effort can change per turn.
- Skill applies it by: Model-line advice with the link for authored prompts; inside Claude Code the skill has no effort override and relies on the prompt nudge.

### F51-125 Name recognition is not current knowledge
- Kind: technique
- Rule: Say in the system prompt that recognizing a name is not the same as knowing its current state and that such names should be searched as the user wrote them.
- Page says: "In other cases, a prompt nudge toward verification helps. In the system prompt, say that recognizing a name isn't the same as knowing its current state, and that such names should be searched as the user wrote them:"
- Applies when: Research requests naming products, tools, models, or people.
- Skill applies it by: `search_name_as_written` in `<execution_guidance>` and "search the name as written" as a `<task>` step.
- Snippet: search_name_as_written

### F51-126 The search nudge
- Kind: sample-prompt
- Rule: Verify unfamiliar or fast-moving names by searching before answering, including the name exactly as written in at least one query, regardless of partial background knowledge.
- Page says: see snippet search_name_as_written; "When a query centers on a name you do not confidently recognize, or recognize from a fast-moving area like AI models and developer tools where the landscape shifts within months, the name itself is the thing to verify: search before answering, and include the name as the user wrote it in at least one query alongside any reformulations. ..."
- Applies when: Research and question requests involving named entities.
- Skill applies it by: Grafted for the research row; Step 6 runs at least one WebSearch with the literal name.
- Snippet: search_name_as_written

Page section: Reduce safeguard false positives (F51-127 to F51-131).

### F51-127 Fewer false positives; vulnerability finding permitted
- Kind: model-note
- Rule: Expect fewer safeguard false positives than Fable 5 at launch, and treat finding vulnerabilities in source code as permitted.
- Page says: "Claude Fable 5.1's safety classifiers produce fewer false positives than Claude Fable 5's did at launch, and finding vulnerabilities in source code is permitted."
- Applies when: Security review or vulnerability-hunting requests, which are common in this the analytics platform workspace.
- Skill applies it by: Legitimate security-review requests are framed plainly as vulnerability finding with the defensive purpose and asset owner stated in `<context>`; nothing is watered down.

### F51-128 Three situations raise the rate
- Kind: fact
- Rule: A blocked request returns `stop_reason: "refusal"`; three situations make false positives more likely.
- Page says: "False positives still occur, and a blocked request returns `stop_reason: \"refusal\"` (see [Refusals, fallback, and billing](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1#refusals-fallback-and-billing)). Three situations make them more likely:"
- Applies when: A refusal is observed on a benign coding request.
- Skill applies it by: Section 6 refusal handling checks the three triggers first; the bullets below are rearticulation rewrites.

### F51-129 Compile-check phrasing
- Kind: technique
- Rule: Instead of asking "Does this program compile without errors?", ask "Are there any bugs in this program?".
- Page says: "**Compile-check phrasing:** Instead of \"Does this program compile without errors?\", ask \"Are there any bugs in this program?\""
- Applies when: The raw request asks whether code compiles or runs without errors.
- Skill applies it by: Step 4 converts compile-check phrasing into a bug-finding question in `<task>`.

### F51-130 Context for lesser-known languages
- Kind: technique
- Rule: For lesser-known programming languages, give the model context about what the language is and how it works, for example its documentation.
- Page says: "**Lesser-known programming languages:** Give the model context about what the language is and how it works, for example by giving it access to the language's documentation."
- Applies when: Code tasks in obscure or domain-specific languages (a vendor query DSL, for example).
- Skill applies it by: `<context>` adds one sentence describing the language and points to its documentation or reference file (for example the user's the vendor query language function reference).

### F51-131 Base64 in tool output
- Kind: technique
- Rule: Remove tools that return base64-encoded data into the model's context.
- Page says: "**Base64 in tool output:** Tools that return base64-encoded data into the model's context can trigger false positives, so removing them is the recommended fix."
- Applies when: Harness or tool design; any task that would dump base64 into context.
- Skill applies it by: Standing rule 8: write base64 payloads to files instead of echoing them into context; flag base64-returning tools when reviewing harness designs.

Page section: Prefer targeted edits over whole-file rewrites (F51-132 to F51-136).

### F51-132 Append the targeted-edit instruction
- Kind: technique
- Rule: If whole files are rewritten for small changes, append the targeted-edit instruction to the system prompt or first user message.
- Page says: "If Claude Fable 5.1 rewrites whole files for small changes, append the following instruction to the system prompt or the first user message."
- Applies when: Any code or text edit task on this profile.
- Skill applies it by: `targeted_edits` in `<execution_guidance>` for edit tasks; Step 6 uses Edit over Write.
- Snippet: targeted_edits

### F51-133 Rewrites more often than Fable 5
- Kind: model-note
- Rule: Expect Fable 5.1 to rewrite an entire text file more often than Fable 5.
- Page says: "Claude Fable 5.1 is more likely than Claude Fable 5 to rewrite an entire text file rather than make a targeted edit."
- Applies when: Edit tasks.
- Skill applies it by: Execution uses the Edit tool for existing files unless most of the file changes; this delta is why Fable 5 needs no equivalent snippet.
- Snippet: targeted_edits

### F51-134 Rewrites cost more
- Kind: fact
- Rule: Rewrites usually yield the same file but cost more output tokens and time unless the file is short or mostly changing.
- Page says: "The resulting file is usually the same, but unless the file is short or most of it is changing, a rewrite costs more output tokens and time."
- Applies when: Choosing between Edit and Write.
- Skill applies it by: Standing rule 11: rewrite only when the file is short or most of it changes.
- Snippet: targeted_edits

### F51-135 Brings 5.1 back in line
- Kind: fact
- Rule: Expect the instruction to bring Fable 5.1 back in line with Fable 5 for small and medium changes.
- Page says: "The instruction brings Claude Fable 5.1 back in line with Claude Fable 5 for small and medium changes."
- Applies when: Justifying the snippet.
- Skill applies it by: Evidence note in the catalog.
- Snippet: targeted_edits

### F51-136 The targeted-edits instruction
- Kind: sample-prompt
- Rule: Minimise edit tokens by surgically editing a file rather than rewriting it when the end result is unaffected.
- Page says: see snippet targeted_edits; "The number of tokens used to edit files is best minimized, all else being equal. Therefore, when it will not affect the end result, try to surgically edit a file rather than rewrite the entire thing."
- Applies when: Every code or document edit task.
- Skill applies it by: Default snippet in the template for the code-change and writing-edit rows.
- Snippet: targeted_edits

Page section: Leave room for long outputs at xhigh and max effort (F51-137 to F51-142).

### F51-137 Longer thinking at xhigh and max
- Kind: model-note
- Rule: Expect Fable 5.1 at `xhigh` and especially `max` to think longer before starting its reply.
- Page says: "At `xhigh` and especially `max` effort, Claude Fable 5.1 can think for longer before it starts writing its reply."
- Applies when: High-effort long deliverables.
- Skill applies it by: The writing row grafts `long_output_budget_note` for long deliverables.
- Snippet: long_output_budget_note

### F51-138 Drafting twice
- Kind: model-note
- Rule: Expect a long deliverable to be drafted in thinking and then written again as the reply, doubling wait and output tokens.
- Page says: "When a single request asks for a long deliverable, such as a full rewrite of a long document, it may draft much of that deliverable in its thinking and then write it out again as the reply, which means a longer wait and more output tokens."
- Applies when: Full document rewrites, large tables, complete files.
- Skill applies it by: Step 1c's long-deliverable signal triggers the budget note.
- Snippet: long_output_budget_note

### F51-139 Run long deliverables at high
- Kind: technique
- Rule: Run long-deliverable requests at `high` and move to `xhigh` or `max` only where a quality gain has been measured.
- Page says: "The simplest approach is to run requests like these at `high`, the recommended starting point, and move to `xhigh` or `max` only where you've measured a quality gain"
- Applies when: Effort choice for long outputs.
- Skill applies it by: Model-line advice when the user asks about effort for document generation.

### F51-140 max_tokens headroom
- Kind: technique
- Rule: Set `max_tokens` to leave room for both thinking and the reply.
- Page says: "Set `max_tokens` to leave room for the thinking and the reply, not just the reply length you expect."
- Applies when: API calls at `xhigh` or `max` for long outputs.
- Skill applies it by: Model-line API advice when authoring prompts or harness code for another caller.

### F51-141 Append the budget note
- Kind: technique
- Rule: Append the budget note to the end of the user message, replacing `[max_tokens]` with the request's actual value such as 64,000.
- Page says: "Append the following note to the end of the user message. It makes the thinking much shorter on prose and code requests. Replace `[max_tokens]` with the request's actual `max_tokens` value, for example 64,000."
- Applies when: Grafting the budget note.
- Skill applies it by: Placed as the prompt's last element before `batch_nudge`, with the real budget substituted; inside Claude Code the session's output limit if known, otherwise a stated approximation recorded in the Assumed line.
- Snippet: long_output_budget_note

### F51-142 The budget note
- Kind: sample-prompt
- Rule: Treat reasoning and reply as one token budget, avoid drafting the deliverable twice, and use reasoning space for understanding, input checks, and structure decisions while writing the output once.
- Page says: see snippet long_output_budget_note; "Everything produced in one reply, including any reasoning or drafting done before the reply, counts toward a single limit of about [max_tokens] tokens. ... Usually it is not needed to draft an output multiple times."
- Applies when: Multi-section documents, large tables or datasets, complete code files.
- Skill applies it by: Grafted at the end of the rearticulated prompt for the writing row when the deliverable is long.
- Snippet: long_output_budget_note

Page section: Let the lead agent keep working while subagents run (F51-143 to F51-148).

### F51-143 Do not force the lead to wait
- Kind: technique
- Rule: Do not force the lead agent to stop and wait for each subagent.
- Page says: "If your coding agent lets Claude Fable 5.1 delegate work to subagents, don't force the lead agent to stop and wait for each one."
- Applies when: The task delegates to subagents, or the user builds a multi-agent harness.
- Skill applies it by: The subagent policy block adds "continue independent work while subagents run and collect results afterward".

### F51-144 Measured time savings
- Kind: fact
- Rule: Expect lower average time to completion at similar quality, token usage, and cost when the lead continues.
- Page says: "On coding tasks, letting the lead continue while subagents run lowers average time to completion at similar quality, token usage, and cost."
- Applies when: Justifying the policy.
- Skill applies it by: Evidence note in the catalog.

### F51-145 Start tool returns immediately
- Kind: technique
- Rule: Make the tool that starts a subagent return immediately.
- Page says: "Have the tool that starts a subagent return immediately."
- Applies when: Harness design for subagents.
- Skill applies it by: Harness pattern in section 2; in Claude Code the skill launches subagents in the background where available.

### F51-146 Results in a later user message
- Kind: technique
- Rule: Pass each subagent's result back to the lead in a later user message once ready.
- Page says: "Pass each subagent's result back to the lead in a later `user` message once it's ready."
- Applies when: Harness design for subagents.
- Skill applies it by: Harness pattern in section 2.

### F51-147 A separate wait tool
- Kind: technique
- Rule: Give the lead a separate tool it can call when it wants to wait for a result.
- Page says: "Give the lead a separate tool it can call when it wants to wait for a result."
- Applies when: Harness design for subagents.
- Skill applies it by: Harness pattern; the subagent policy block names the wait mechanism available in the session.

### F51-148 The model still often waits
- Kind: fact
- Rule: Accept that the model still often chooses to wait; savings come from runs where it carries on.
- Page says: "The model still often chooses to wait. The time savings come from the runs where it carries on with other work."
- Applies when: Setting expectations for subagent parallelism.
- Skill applies it by: The recap does not over-promise parallelism.

Page section: Give vision work tools to crop and zoom (F51-149 to F51-152).

### F51-149 Iterative analyze, crop, verify
- Kind: model-note
- Rule: Expect better out-of-the-box vision, with best results on dense charts when the model can iteratively analyze, crop, and visually verify.
- Page says: "Claude Fable 5.1 has better vision capabilities out of the box, and on complex visual inputs such as dense charts it does its best work when it can iteratively analyze, crop, and visually verify what it sees."
- Applies when: Vision and data-extraction requests over images.
- Skill applies it by: The vision row adds an iterative analyze, crop, verify step to `<task>`.

### F51-150 Container with PIL and OpenCV
- Kind: technique
- Rule: Run the model as an agent with a container holding the raw images or videos and PIL or OpenCV pre-installed.
- Page says: "To get the full benefit, run the model as an agent with access to a container that holds the raw images or videos and has basic image-processing libraries (such as PIL and OpenCV) pre-installed."
- Applies when: Vision tasks where a runtime is available (Claude Code with Python).
- Skill applies it by: `<execution_guidance>` for the vision row: crop and enlarge regions with Python PIL or OpenCV via Bash and re-read them before answering detail questions.

### F51-151 Crop tool alone
- Kind: technique
- Rule: If a container is too much overhead, provide an image-cropping tool that returns a chosen region cropped and enlarged.
- Page says: "If running a container is too much overhead, an image-cropping tool alone delivers most of the uplift: a tool that returns a chosen region of the image, cropped and enlarged, lets the model examine specific details in more depth and scales test-time compute with image tokens."
- Applies when: Vision harness design without a full container.
- Skill applies it by: Pattern grafted into prompts that design vision agents.

### F51-152 Crop tool recipe
- Kind: link
- Rule: Use the crop tool recipe for a working crop-tool definition.
- Page says: "The [crop tool recipe](https://platform.claude.com/cookbook/multimodal-crop-tool) has a working definition."
- Applies when: Building a crop tool.
- Skill applies it by: Cited in section 2 under vision.

## When this is the TARGET model: add to the rearticulated prompt

Tag by tag. Default-on items are grafted on every run of the named kind; conditional items need their trigger.

- `<role>`: no model-specific addition. Invest in a clear goal, not methodology (F51-79).
- `<context>`: for a lesser-known or domain-specific language (a vendor query DSL, for example) one sentence saying what the language is and where its reference lives (F51-130). For security, vulnerability, or malware-analysis requests one sentence stating the defensive or investigative purpose and the asset owner; vulnerability finding in source is permitted (F51-127; the purpose sentence is inherited from the Fable 5 page, F5-09). For harness-authoring requests the API facts from section 2 that the task needs (display settings, beta headers, binding behaviour). When grafting `batch_nudge` into a prompt the user will question, the motivation sentence (F51-42).
- `<documents>`: no model-specific addition.
- `<task>`: enumerate the files and lookups explicitly so parallel calls engage (F51-40). Compile-check questions become "Are there any bugs in this program?" (F51-129). For summaries of retrieved sources, a step that marks quotations and rewords everything else (F51-75). For vision, an iterative analyze, crop, verify step (F51-149). For multi-source research, "search the name as written" as a step (F51-125). Harness-audit prompts carry the two numbered checks of F51-64.
- `<constraints>`: `keep_changes_to_task` verbatim for every code change (F51-114 to F51-122); the scope-is-the-deliverable sentence on every run (F51-96). Grafted snippets stay verbatim even where phrased negatively.
- `<output_format>`: `formatting_in_chat_rule` for chat-style output, and a positive statement of when lists, headers, or tables are wanted (F51-72 to F51-74). For prose deliverables `mannered_prose_definition`, or `mannered_prose_short` when the prompt is already long, plus a line on sentence length and paragraph breaks (F51-66 to F51-70). No generic avoid-cliches or be-concise instruction (F51-65; narration-brevity lines are removed, F51-35).
- `<examples>`: for summaries or comparisons of retrieved sources, `quoting_sources_example` as a single `<user>`/`<response>`/`<rationale>` example with the tool name substituted (F51-76 to F51-78).
- `<success_criteria>`: completeness of every requested behaviour beside the no-extras constraint (F51-122); "source wording appears only as marked quotations; every other claim is reworded" for summaries (F51-75); claims source-verified for research (F51-123); "files created or modified: only <the files named in task>" (F51-96, F51-102).
- `<execution_guidance>`: `progress_updates_line` first on every tool-using run (F51-36, F51-37). Autonomy: for unattended runs (background, scheduled, or the user says run without asking) `operating_autonomously` whole with its first sentence as written, followed by the confirmations sentence when Step 1f flagged `[confirm]` steps, then `delivering_work` when length allows (F51-80, F51-84, F51-91, F51-92); for attended runs `delivering_work` whole plus paragraphs two to four of `operating_autonomously`, and, when confirmations exist, the sentence "This runs in an interactive Claude Code session; the harness permission prompt is not a substitute for the confirmations listed above" in `<context>` (F51-86, F51-93). Exactly one posture snippet from the guide (`default_to_action` or `do_not_act_before_instructions`), never both. `targeted_edits` for edit tasks (F51-132, F51-136). `search_name_as_written` for research (F51-125, F51-126). Subagent policy plus "continue independent work while subagents run and collect results afterward" when delegation is in play (F51-143). Crop-and-zoom guidance for vision (F51-150). Base64 to files (F51-131). `compaction_summary_instruction` for transcript summaries and client-side compaction; its six items shape progress notes for multi-session work (F51-103 to F51-113). Closing lines of the whole prompt, in this order: `long_output_budget_note` with the real budget when the deliverable is long (F51-141, F51-142), then `batch_nudge` (F51-43, F51-44).
- `<verification>`: filled; this page has no verification exception. Evidence before any state-changing command is a listed check (F51-90).
- Target model item: in-session `Target model: fable-5-1 (executing model)`. For authored prompts or when the user asks about speed, cost, or thinking: start at `high` and sweep (F51-23, F51-25); `medium` as the first step-down (F51-27); `low` for cheap tasks with the search caveat (F51-28, F51-29); `max_tokens` headroom at `xhigh` or `max` (F51-140); thinking always on, no `budget_tokens` (section 2); raise effort per turn for search-heavy turns (F51-124).

## When this is the TARGET model: remove or convert

Each item is recorded in the Changed line.

- Anti-formatting blocks inherited from prompts for earlier models ("no bullets", "no markdown", "no bold"): remove, or replace with `formatting_in_chat_rule`. A minimal-formatting request the user made themselves stays; the rule honours it (F51-71, F51-73, F51-74).
- "Hold all findings for the final response", "keep progress text brief", and other narration suppressors: remove before adding anything (F51-35).
- "Does this compile without errors?": "Are there any bugs in this program?" (F51-129).
- A Fable 5 prompt being ported: keep its substance; apply only the F51 deltas; say the base prompt was kept (F51-04).
- Show-your-reasoning, think-aloud, echo-or-explain-your-reasoning, and reflection instructions: remove. This strip is inherited from the Fable 5 page (F5-71, `reasoning_extraction`) and is not restated on the 5.1 page; the skill inherits it as a conservative measure and marks it "not restated on the 5.1 page" in the Changed line. Keep at most a general "think thoroughly" for complex tasks (guide, BP-222).
- Thinking budgets, `budget_tokens`, "use N thinking tokens", "show your full thinking": remove; thinking is always on and adaptive (section 2; guide BP-189).
- Prefill constructs on the last assistant turn: convert to a direct instruction, a named output tag, or enumerated labels (guide, BP-124, BP-352).
- All-caps emphasis, "CRITICAL: you MUST", anti-laziness amplifiers, "if in doubt use X": plain conditional wording and targeted triggers; 4.6 and later models over-trigger on them (guide, BP-162, BP-355).
- Step-by-step methodology for a task whose goal is clear: a clear goal plus `<success_criteria>` (F51-79).
- A paraphrased first sentence of `operating_autonomously`: restore the verbatim sentence for unattended runs, or drop the block in favour of the attended graft (F51-91).
- Harness prompts that force the lead to wait on each subagent: the lead keeps working (F51-143).
- Tools returning base64 into context: remove them, or write payloads to files (F51-131).
- Harness code that injects and removes per-turn reminders, summarizes older turns in place, rewrites `system` or `tools` mid-session, or deletes old turn-scoped copies: turn-scoped system messages, mid-conversation system messages, server-side compaction or context editing (F51-50, F51-58 to F51-61).
- Remaining-token counts or context-budget figures quoted into the prompt: remove; the last-paragraph paragraph already says not to stop because the context is long (F51-89; inherited concern from F5-53, F5-54).
- Generic be-concise or register instructions: none added for this profile (guide, BP-088).

## When this is the EXECUTING model: how the skill behaves in Steps 5-7

As SKILL.md Steps 6 and 7 are written. This section is the source those steps mirror; if they drift, this profile wins for this model.

- Progress updates line (F51-31, F51-36, F51-37): say in one line what is about to happen; give a one-line factual update before each tool batch and a short note after it; the final message is a recap that stands alone and covers the whole task, not only the last step.
- Batching nudge (F51-41 to F51-44): privately list what is needed next, then request every item that does not depend on another's result in one response; serialise only dependent calls, or all calls when the target system fails under concurrency (a rate-limited analytics API returns 500s). Claude Code injects its own parallel-calls reminder, so the prompt states batching once, in `batch_nudge` (guide, BP-174).
- Formatting in chat (F51-72 to F51-74): use lists and headers when the content is multifaceted or the user asked; honour an explicit minimal-formatting request; plain prose in conversational exchanges. Reach for structure more readily than the model's default, since this model under-formats.
- Writing density (F51-66 to F51-70): shorter sentences and more paragraph breaks than the model's default; literal phrases over metaphor; this matches the workspace's reporting style (no dramatic titles or language).
- Finish the whole task (F51-80 to F51-83, F51-89, F51-101): the turn ends after Step 7; a decided step is run, not announced; the last-paragraph check runs before every turn ends; the only exceptions are a dry run and a question only the user can answer, which goes at the end of a turn that already delivers the independent work.
- Delivering work (F51-95 to F51-102): the request sets the scope and the scope is the deliverable; routine judgment calls are made and recorded; a real problem with the task is voiced in a sentence and work continues under stated assumptions; blocked parts are named with reasons; extras are follow-ups.
- Keep changes and tests to the ask (F51-117 to F51-122): no fixes, optimisations, or extensions beyond the request unless the requested behaviour cannot work without them; the most direct reading of ambiguity, stated; scratch checks in the scratchpad and removed; tests committed only where asked or conventional, sized like neighbours; every requested behaviour implemented completely.
- Targeted edits (F51-133 to F51-136): Edit over Write for existing files; rewrite only when the file is short or most of it changes.
- Search at low effort (F51-123, F51-126): for any name not confidently recognised, or from a fast-moving area, at least one WebSearch with the name exactly as the user wrote it before answering; familiarity is not a reason to skip.
- Safeguard phrasing (F51-127 to F51-131): frame security reviews plainly as vulnerability finding with the purpose stated; ask "are there any bugs" rather than "does it compile"; give a sentence of context for the vendor query language and other domain languages; write base64 to files. If a benign request is declined, say so plainly, check the three triggers, and do not rephrase to get around it; a blocked request shows as `stop_reason: "refusal"`.
- Long outputs at xhigh or max (F51-137 to F51-142): for a long deliverable, spend the reasoning space on understanding, input checks, and structure, then write the output once; never draft the deliverable in full twice.
- Quoting sources (F51-75 to F51-78): summaries convey sources in indirect speech; source wording appears only as marked quotation.
- Subagents keep working (F51-143 to F51-148): launch independent subagents in the background where available, continue independent work, collect results afterward; the recap does not over-promise parallelism.
- Vision crop (F51-149, F51-150): for dense charts, small text, or tables, crop and enlarge the region with Python PIL or OpenCV via Bash and re-read it before answering; iterate analyze, crop, verify.
- Final-message shape (F51-37): recap of three to eight lines in this order: found; done (files changed by path, commands run, results observed); verified and how, with verified facts marked apart from inferences; left out and why; follow-ups noticed but not done; next. Facts only, no self-evaluation.
- Verification loop (guide, BP-229 to BP-231): Step 7 runs every check in `<verification>` with tools; nothing on this page softens it.
- Evidence before mutation (F51-90): before restarts, deletes, config edits, or API writes, confirm the evidence supports that specific action.
- Compaction and progress notes (F51-103 to F51-113): handoff notes for multi-session work follow the six preservation items and weight the user's words above the skill's own reasoning.
- Context-count handling (F51-89): do not stop, trim, or propose a new session because the context or session is long; never copy the harness's remaining-token figure into a prompt.
- Effort follow-up advice (F51-06, F51-23 to F51-28): the skill cannot set effort in-session; when the user asks about speed or cost, recommend the sweep from `high` and `medium` as the first step down.
- Harness-injected blocks to skip in-session: Claude Code's own parallel-calls reminder (so no duplicate beyond `batch_nudge`); the hidden-tool-output note is already Standing rule 8, so `tool_output_hidden_note` is not grafted in-session.
- Target model item: `Target model: fable-5-1 (executing model)`.

## Snippets

Measured on this page (verbatim text in `references/snippet-library.md`):

- progress_updates_line (F51-36, F51-37): default on every tool-using run.
- tool_output_hidden_note (F51-38, F51-39): harness authoring only; Standing rule 8 in-session.
- batch_nudge (F51-43, F51-44): default closing line of every tool-using prompt.
- mannered_prose_definition (F51-67, F51-68): writing row.
- mannered_prose_short (F51-69, F51-70): writing row when the prompt is long.
- formatting_in_chat_rule (F51-73, F51-74): default `<output_format>` rule for chat-style output.
- quoting_sources_example (F51-76 to F51-78): single example for summaries of retrieved sources; tool name substituted.
- operating_autonomously (F51-80, F51-84 to F51-93): unattended runs whole; attended runs paragraphs two to four.
- delivering_work (F51-94 to F51-102): agentic and code-change rows; whole for attended runs.
- compaction_summary_instruction (F51-103 to F51-113): transcript summaries, client-side compaction, progress-note shape.
- keep_changes_to_task (F51-114 to F51-122): every code change, in `<constraints>`.
- search_name_as_written (F51-123, F51-125, F51-126): research row.
- targeted_edits (F51-132 to F51-136): edit tasks.
- long_output_budget_note (F51-137, F51-138, F51-141, F51-142): long deliverables, last element before `batch_nudge`.

Inherited from `fable-5` for topics this page does not cover (graft with "text measured on the Fable 5 page" in the Target model item): f5_give_reason (context frame), f5_ground_progress (evidence-audited status reports), f5_memory_notes and f5_memory_bootstrap (memory systems, only when no harness convention exists), send_to_user and f5_send_to_user_elicitation (async agent harnesses), f5_self_verification_interval (long builds). Superseded by this page and not grafted for this profile: f5_autonomous_reminder (use operating_autonomously), f5_state_boundaries (its text is inside operating_autonomously), f5_delegate_subagents (F51-143 covers subagents), f5_ample_context (F51-89 covers context length), f5_scope_discipline (keep_changes_to_task covers scope; minimize_overengineering from the guide covers over-abstraction), f5_lead_with_outcome and f5_readability_addendum (progress_updates_line's recap clause covers the final message; borrow only on an observed final-message symptom, recorded).

## Not covered by this page

The skill falls back to the main guide (`references/technique-catalog.md`) for everything below.

- General technique: role, XML structure, examples count and diversity, document structure and quotes-first grounding, positive format control, plain-text math, success criteria, self-check, tool-description writing, structured research, state tracking, `autonomy_safety_confirmation`, `minimize_overengineering`, `general_purpose_solution`, `frontend_aesthetics`, vision beyond cropping (video as frames, multiple images, screenshots read directly).
- Capabilities, context window size, tokenizer, pricing, availability, sampling parameters: What's new in Claude Fable 5.1 (F51-02). The skill verifies rather than recalls.
- Refusal fallback configuration and billing on refusal: Refusals, fallback, and billing (F51-22, F51-128).
- The `reasoning_extraction` refusal category, safety-classifier domains, give-the-reason framing, memory systems, send_to_user, grounded progress claims: the Fable 5 page (`references/models/fable-5.md`), inherited as the baseline.
- Effort API mechanics and mid-conversation effort changes: the effort page (F51-23, F51-124).
- Cross-model migration checklist, prefill migration, thinking-configuration migration: the guide's Migration considerations.
- Thinking display, turn-scoped and mid-conversation system messages, preserved thinking, compaction, context editing: the linked API pages named in section 2; this profile quotes only the facts the page states.
