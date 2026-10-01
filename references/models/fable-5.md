# Claude Fable 5 and Claude Mythos 5

Source page: Prompting Claude Fable 5, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5 (snapshot 2026-09-08). The page's own description is the authoritative list of what it covers: "Behavioral differences and prompting patterns for Claude Fable 5 and Claude Mythos 5, covering effort, instruction following, long runs, memory, and scaffolding changes." (F5-01). One file serves both names, because the page covers both (F5-01), and the alias table in `references/model-notes.md` points Mythos 5 here. Guide rules that name Fable 5 or Mythos 5 come from Prompting best practices, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (snapshot 2026-09-08), and are listed at the end of section 3 with their BP IDs.

How to read this file. Everything on the page is measured on Claude Fable 5 and Claude Mythos 5; a rule here is applied to another model only by analogy, and the Reading line's Target model item says so (BP-025). The cross-model technique catalog (`references/technique-catalog.md`) applies first; this file only adds or overrides (F5-03). Profile IDs `F5-nn` are the page's rules in page order. Sections 4 and 5 govern the content of a rearticulated prompt whose target model is Fable 5 or Mythos 5; section 6 governs the skill's own behaviour when a Fable 5 model is the model running the skill. Those two dimensions are resolved separately in SKILL.md Step 1a.

Baseline: none (guide only). Page basis: "Claude Fable 5 has several behavioral differences from Claude Opus 4.8 that may require prompt or scaffolding updates. Capability improvements at this level are also a good prompt to re-evaluate which instructions, tools, and guardrails are still needed." (F5-07). The page is written as a set of differences from Claude Opus 4.8, but nothing is inherited from the Opus 4.8 profile: the sections of this page are the whole of the Fable 5 profile, and an Opus 4.8 instruction that this page does not ask for is a candidate for removal rather than for grafting (F5-07, F5-19, F5-70). In the other direction, Claude Fable 5.1 takes this profile as its baseline, so the `f5_*` snippets carry into `references/models/fable-5-1.md` except where a 5.1 section covers the same topic (F51-04).

## Identity and API facts

- Profile: `fable-5`. Aliases: fable-5, fable5, mythos-5, mythos5, claude-fable-5, claude-mythos-5. Display names: Claude Fable 5, Claude Mythos 5.
- API model string: not printed on this page or in the guide's samples. Look it up in the models overview, https://platform.claude.com/docs/en/models/overview, or the `claude-api` skill rather than inventing one; the guide's samples pin an explicit model string and `max_tokens` whenever API code is produced (BP-059).
- Covered set: inside the guide's eleven current models (BP-002); the guide's model table row is BP-015, and the page link is BP-020.
- Capabilities, API changes, pricing, and availability: Introducing Claude Fable 5 and Claude Mythos 5, https://platform.claude.com/docs/en/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5 (F5-02, BP-009). The skill names that page instead of restating its content.
- Thinking: always on, and adaptive thinking is the only mode; there is no way to disable it and no extended thinking budget (F5-08, BP-195, BP-220). Thinking output is summarized only (F5-08). Nothing in a rearticulated prompt configures thinking on this profile.
- `budget_tokens`: not supported. No extended thinking budgets exist on the Fable family (F5-08), and on Claude 4.7 and later the parameter returns a 400 error (BP-189). Convert a legacy configuration to adaptive thinking plus `output_config.effort` and record the substitution.
- Sampling parameters (`temperature`, `top_p`, `top_k`): not printed on this page. Do not assert a value or a 400; flag any sampling parameter in a raw request as "not printed for this model, check Introducing Claude Fable 5 and Claude Mythos 5" in the Target model item.
- Effort: "the primary control for the trade-off between intelligence, latency, and cost" (F5-25). Default `high`; `xhigh` for the most capability-sensitive workloads; `medium` or `low` for routine work (F5-26). Levels the page names: `low`, `medium`, `high`, `xhigh`. It does not name `max`; do not recommend it from this profile. Lower effort here still performs well and often exceeds `xhigh` on prior models (F5-27), so a routine rearticulation can drop to `medium` or `low` without a quality worry; reduce effort when a task completes but takes longer than necessary or a quicker interactive style is wanted (F5-28). Higher effort brings the best verification behaviour and the most rigorous output (F5-30) at the cost of over-gathering on routine work (F5-29). Effort is an API parameter, never prompt prose: the skill recommends a level in the Target model item and does not write "think harder" into the prompt (F5-25). Effort is profile-local and is re-derived here rather than carried from another profile (`model-notes.md` section 7). Reference: Effort, https://platform.claude.com/docs/en/build-with-claude/effort (F5-23).
- `max_tokens` headroom: no figure printed. What the page does state is time, not tokens: individual requests on hard tasks can run for many minutes at higher effort and autonomous runs for hours (F5-21). Fall back to the guide for `max_tokens` (BP-059, BP-190).
- Context window: not printed. The page's context rule is about what the model is shown, not about the size: avoid surfacing explicit context-budget counts to the model, and if the harness must show them, add `f5_ample_context` (F5-53, F5-54, F5-55). Never quote a remaining-token figure into a rearticulated prompt.
- Last-turn prefill: unsupported from Claude 4.6 onward, so also on this profile (BP-124). A prefill construct is converted to a direct instruction, a named output tag, or enumerated labels (SKILL.md Step 4).
- Tokenizer: not printed on this page; do not assert a scaling factor.
- Refusals and safeguards: the model runs safety classifiers targeting offensive cybersecurity techniques (building exploits, malware, or attack tooling), biology and life sciences content (lab methods or molecular mechanisms), and extraction of the model's summarized thinking (F5-09). Benign cybersecurity work and beneficial life sciences tasks may also trigger them (F5-10). A blocked request returns `stop_reason: "refusal"` (F5-20), and prompts that tell the model to echo, transcribe, or explain its internal reasoning as response text can trigger the `reasoning_extraction` refusal category, with elevated fallbacks to Claude Opus 4.8 (F5-71). Fable 5 is not intended for offensive cybersecurity or biology and life sciences work (F5-20). Documented remedy: server-side or client-side fallback to Claude Opus 4.8, https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback (F5-11). Reasoning visibility comes from the structured `thinking` blocks of adaptive thinking and from a send-to-user tool, never from an instruction to reproduce reasoning (F5-72).

### Harness and environment notes

These facts reach a rearticulated prompt only through the taxonomy rows for harness authoring, async agents, and prompt authoring for another model; in an interactive session the skill informs the user and does not try to set them from inside a prompt.

- Long turns change the harness, not the prompt: adjust client timeouts, streaming, and user-facing progress indicators before migrating, and check on runs asynchronously, for example through scheduled jobs, rather than blocking (F5-21, F5-22). Inside Claude Code the equivalent is `run_in_background` plus `Monitor` for long commands instead of a blocking wait.
- Fallback cannot be configured from inside a prompt. In Claude Code the skill reports a refusal and tells the user that Claude Opus 4.8 is the documented fallback model to switch to; server-side and client-side fallback are harness settings (F5-10, F5-11).
- `send_to_user` is a client-side tool the harness defines, not a Claude Code tool. Its input is the message to display; the harness renders that input directly and returns a simple acknowledgement, and tool inputs are never summarized, so the content arrives intact (F5-61). Defining it is not enough: without elicitation language in the system prompt the model rarely calls it (F5-64). Add it only when the UX depends on verbatim mid-task delivery (F5-63), and never route narration or reasoning through it (F5-66). The JSON definition is stored as the snippet `send_to_user`, the tool's own name and the id the rule set records, and pairs with `f5_send_to_user_elicitation` (F5-62, F5-65, F5-73).
- A memory system can be as simple as a Markdown file the model writes notes into (F5-45). In this workspace the convention already exists (the project memory directory indexed by `MEMORY.md`), so the skill points the prompt at that path instead of creating a parallel store, and grafts `f5_memory_notes` only where no convention exists.
- Fresh-context verifier subagents outperform self-critique on long runs, and long-lived subagents that keep context across subtasks save time and cost through cache reads (F5-43, F5-68).

## Behavioural deltas

One entry per page rule, in page order, grouped by the page's section headings; the guide rules that name Fable 5 and Mythos 5 follow at the end. Sample prompts are quoted in part here and stored verbatim in `references/snippet-library.md` under the snippet ID given.

Page section: Prompting Claude Fable 5 (introduction and the API Note)

### F5-01 Page provenance, and Mythos 5 shares it
- Kind: fact
- Rule: Treat this page as covering both Claude Fable 5 and Claude Mythos 5.
- Page says: "Behavioral differences and prompting patterns for Claude Fable 5 and Claude Mythos 5, covering effort, instruction following, long runs, memory, and scaffolding changes."
- Applies when: The active model is Fable 5 or Mythos 5.
- Skill applies it by: The Mythos 5 aliases in `model-notes.md` resolve to this file, and every rule in this profile applies to both models; the five areas in the description are the checklist sections 4 to 6 have to cover.

### F5-02 Introducing page for capabilities and API facts
- Kind: link
- Rule: Consult the Introducing Claude Fable 5 and Claude Mythos 5 page for capabilities, API changes, pricing, and availability rather than this prompting page.
- Page says: "For the model's capabilities, API changes, pricing, and availability, see [Introducing Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5)."
- Applies when: A question concerns model capabilities, API parameters, pricing, or availability rather than prompting patterns.
- Skill applies it by: Section 2 and section 8 record the link; the skill names the page in the Target model item instead of restating pricing or availability.

### F5-03 Cross-model guide applies first
- Kind: link
- Rule: Apply the cross-model Prompting best practices guide together with this page.
- Page says: "For techniques that apply across all current Claude models, see [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)."
- Applies when: Every rearticulation, since the model page only layers model-specific patterns on top of the general guide.
- Skill applies it by: Applies `references/technique-catalog.md` first and overlays this profile as additions and overrides; the Reading line cites both ID sets.

### F5-04 Built for work that was too complex, long-running, or ambiguous
- Kind: model-note
- Rule: Treat Fable 5 as suited to problems that were too complex, long-running, or ambiguous for prior models, including end-to-end work that takes a person hours to weeks.
- Page says: "Claude Fable 5 takes on problems that were previously too complex, long-running, or ambiguous for prior models, and is particularly effective at end-to-end work that takes a person hours, days, or weeks to complete."
- Applies when: Scoping how much of a large request to hand to the model in one go.
- Skill applies it by: Does not pre-decompose a large request into small sequential steps; `<task>` states the end-to-end goal and lets the model scope it (with F5-67).

### F5-05 Hardest problems, not only the simple ones
- Kind: technique
- Rule: Give Fable 5 the hardest unsolved problems and do not judge it only on simple workloads.
- Page says: "The teams seeing the best outcomes apply Claude Fable 5 to their hardest unsolved problems; testing it only on simpler workloads tends to undersell its capability range."
- Applies when: Choosing which requests to route here, or evaluating the output.
- Skill applies it by: The rearticulated prompt carries the full ambition of the request rather than a reduced version; a reduction, if any, is recorded in the Assumed line.

### F5-06 Straightforward tasks stay reliable
- Kind: fact
- Rule: Expect Fable 5 to handle straightforward tasks reliably as well.
- Page says: "It also performs reliably on more straightforward tasks."
- Applies when: A user request is simple.
- Skill applies it by: Keeps the prompt short for simple requests (SKILL.md Step 5's 25-line budget) and adds no heavy scaffolding just because the model is Fable 5.

### F5-07 Re-evaluate prompts, tools, and guardrails on arrival
- Kind: model-note
- Rule: Re-evaluate existing prompts, tools, and guardrails when moving to Fable 5, because its behaviour differs from Opus 4.8.
- Page says: "Claude Fable 5 has several behavioral differences from Claude Opus 4.8 that may require prompt or scaffolding updates. Capability improvements at this level are also a good prompt to re-evaluate which instructions, tools, and guardrails are still needed. The patterns below cover the behaviors that most often require tuning."
- Applies when: A prompt or skill was written for Opus 4.8 or older and now runs on Fable 5.
- Skill applies it by: Drops the legacy instructions this profile says are unnecessary and names each removal in the Changed line; this sentence is also the page basis recorded in section 1.

### F5-08 Adaptive thinking only, summarized output, no budgets
- Kind: fact
- Rule: Do not set extended thinking budgets or expect full thinking output on Fable 5 and Mythos 5; they use adaptive thinking only, summarized thinking output, and a refusal stop reason.
- Page says: "For API parameter changes specific to Claude Fable 5 and Claude Mythos 5 (adaptive thinking only, summarized-only thinking output, no extended thinking budgets, the `refusal` stop reason and fallback handling), see [Introducing Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5)."
- Applies when: The rearticulated prompt or the execution harness would reference thinking budgets, `budget_tokens`, or verbatim thinking.
- Skill applies it by: Section 5 removes every "use N thinking tokens" and "show your full thinking" instruction; section 2 records adaptive-only thinking, summarized-only output, the absent budget, and the refusal stop reason.

### F5-09 Three safety-classifier domains
- Kind: fact
- Rule: Know that Fable 5 runs safety classifiers on offensive cybersecurity techniques, biology and life sciences content, and extraction of its summarized thinking.
- Page says: "Claude Fable 5 runs safety classifiers that target offensive cybersecurity techniques (such as building exploits, malware, or attack tooling), biology and life sciences content (such as lab methods or molecular mechanisms), and extraction of the model's summarized thinking."
- Applies when: Any request touching security tooling, biology, or the model's own thinking.
- Skill applies it by: Never writes an instruction asking the model to reproduce its thinking; for security requests `<context>` states the defensive or investigative purpose and the asset owner in one sentence, so intent is unambiguous (`model-notes.md` section 9).

### F5-10 Benign work can also trigger the safeguards
- Kind: model-note
- Rule: Expect that benign cybersecurity and beneficial life sciences tasks may still trigger the safeguards.
- Page says: "Benign cybersecurity work and beneficial life sciences tasks may also trigger these safeguards."
- Applies when: Executing defensive security or life-sciences requests on Fable 5.
- Skill applies it by: On a refusal for a benign task the skill does not rephrase to evade; it reports the refusal plainly and names Claude Opus 4.8 as the documented fallback (section 6).

### F5-11 Fallback to Opus 4.8
- Kind: link
- Rule: Configure server-side or client-side fallback to Opus 4.8 to re-route declined requests automatically.
- Page says: "To re-route declined requests automatically, configure [server-side or client-side fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback) to Claude Opus 4.8."
- Applies when: Building a harness that runs Fable 5 in domains that may trigger refusals.
- Skill applies it by: Cites the refusals-and-fallback page in section 8; inside Claude Code the skill cannot configure fallback, so it tells the user to switch model when a refusal occurs.

Page section: Capability improvements

### F5-12 Long-horizon autonomy with instruction retention
- Kind: model-note
- Rule: Rely on Fable 5 to sustain multiday goal-directed runs with strong instruction retention.
- Page says: "**Long-horizon autonomy.** Claude Fable 5 sustains productive output over extended periods, completing multiday, goal-directed runs with strong instruction retention across long, complex tasks."
- Applies when: Long autonomous tasks.
- Skill applies it by: States instructions once at the top of the prompt; adds no per-step repetition and no "remember the earlier instructions" reminders.

### F5-13 First-shot correctness on well-specified problems
- Kind: model-note
- Rule: Specify complex problems well and expect a single-pass implementation.
- Page says: "**First-shot correctness on complex, well-specified problems.** Early testers reported single-pass implementations of systems that previously took days of iteration."
- Applies when: Complex build or implementation requests.
- Skill applies it by: Invests Step 2 in a complete specification (success criteria, constraints, inputs) rather than in reasoning choreography, because well-specified problems are where first-shot correctness shows.

### F5-14 Vision, with bash and crop tools for degraded images
- Kind: model-note
- Rule: Hand Fable 5 dense technical images and screenshots directly and let it use bash and crop tools on degraded images.
- Page says: "**Vision.** Claude Fable 5 interprets dense technical images, web applications, and detailed screenshots with substantially higher accuracy, often while using fewer output tokens, and is trained to use bash and crop tools to handle flipped, blurry, or noisy images."
- Applies when: Requests involving screenshots, diagrams, or noisy images.
- Skill applies it by: Does not pre-describe image contents in the prompt; `<execution_guidance>` mentions that crop and bash tools are available when an image is flipped, blurry, or noisy.

### F5-15 Enterprise workflows: instructions, scope, professional output
- Kind: model-note
- Rule: Expect professional-grade output and scope discipline on financial analysis, spreadsheets, slides, and documents.
- Page says: "**Enterprise workflows.** Claude Fable 5 follows instructions, stays in scope, and produces professional-grade output on financial analysis, spreadsheets, slides, and documents."
- Applies when: Document, spreadsheet, slide, or analysis deliverables.
- Skill applies it by: Specifies format and audience in `<output_format>` and skips lengthy quality exhortations for these deliverable types.

### F5-16 Code review and debugging across history
- Kind: model-note
- Rule: Use Fable 5 for bug-finding across codebases and repository history, outside the cybersecurity domains the classifiers cover.
- Page says: "**Code review and debugging.** Bug-finding recall (outside the cybersecurity domains the safety classifiers cover) is noticeably higher than Claude Opus 4.8, including search across codebases and repository history."
- Applies when: Code review, debugging, or repository-history requests.
- Skill applies it by: `<task>` explicitly allows searching across the codebase and git history; security-adjacent review is framed as defensive code quality work (F5-09).

### F5-17 Navigating ambiguity: let it determine next steps
- Kind: model-note
- Rule: Let Fable 5 determine next steps on complex, multithreaded requests instead of over-decomposing them.
- Page says: "**Navigating ambiguity.** Claude Fable 5 performs well when given complex, multithreaded requests and asked to determine next steps."
- Applies when: Ambiguous or multi-part requests.
- Skill applies it by: Preserves the ambiguity honestly and asks the model to determine next steps, paired with `f5_act_when_ready` so the openness does not become a planning loop.

### F5-18 Dependable parallel subagents and peer communication
- Kind: model-note
- Rule: Expect dependable dispatch of parallel subagents and sustained communication with long-running subagents and peer agents.
- Page says: "**Delegation and collaboration.** Claude Fable 5 is significantly more dependable at dispatching and sustaining parallel subagents, and reliably manages ongoing communication with long-running subagents and peer agents."
- Applies when: Tasks with independent subtasks.
- Skill applies it by: Delegates independent parts to subagents when executing on this profile (section 6) and states which parts are independent in `<task>`.

### F5-19 Generally more capable than prior models
- Kind: fact
- Rule: Assume Fable 5 is generally more capable than prior models on almost all tasks.
- Page says: "Beyond these specific improvements, Claude Fable 5 is generally more capable than prior models on almost all tasks."
- Applies when: Deciding how much hand-holding a prompt needs.
- Skill applies it by: Defaults to lighter scaffolding than the legacy-4x notes prescribe; a legacy block is kept only when this page asks for it.

### F5-20 Not intended for offensive cybersecurity or life sciences
- Kind: fact
- Rule: Do not target Fable 5 for offensive cybersecurity or biology and life sciences work; requests there can return `stop_reason: "refusal"`.
- Page says: "Claude Fable 5 is not intended for offensive cybersecurity or biology and life sciences work; requests in those domains can return [`stop_reason: \"refusal\"`](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)."
- Applies when: A request falls in those domains.
- Skill applies it by: Treats a refusal stop reason as a model-level outcome, not a prompt defect; surfaces it and suggests the fallback model rather than re-prompting.

Page section: Longer turns by default

### F5-21 Many minutes per turn, hours per autonomous run
- Kind: fact
- Rule: Expect single requests to run many minutes at higher effort and autonomous runs to extend for hours.
- Page says: "Individual requests on hard tasks can run for many minutes at higher [effort](https://platform.claude.com/docs/en/build-with-claude/effort) settings, especially when the task requires gathering context, building, and self-verifying, and autonomous runs can extend for hours. This is one of the largest shifts teams encounter when adjusting to Claude Fable 5."
- Applies when: Hard tasks at `high` or `xhigh` effort.
- Skill applies it by: Says in the opening line of Step 6 that a long run is expected for a hard task; does not read a long tool sequence as a hang and does not cut the work short.

### F5-22 Timeouts, streaming, and asynchronous checking
- Kind: technique
- Rule: Adjust client timeouts, streaming, and progress indicators before migrating, and check on runs asynchronously instead of blocking.
- Page says: "Adjust client timeouts, streaming, and user-facing progress indicators before migrating, and consider restructuring harnesses to check on runs asynchronously, for example through scheduled jobs, rather than blocking."
- Applies when: Harness or pipeline design for Fable 5.
- Skill applies it by: Section 2 (harness notes) records it; in-session the skill uses `run_in_background` and `Monitor` for long commands rather than a blocking wait, and mentions the timeout change when the deliverable is a harness.

### F5-23 Effort page link
- Kind: link
- Rule: Refer to the effort page for the effort parameter.
- Page says: "[effort](https://platform.claude.com/docs/en/build-with-claude/effort)"
- Applies when: Any discussion of effort settings.
- Skill applies it by: Cites the Effort page, https://platform.claude.com/docs/en/build-with-claude/effort, in the Target model item every time a level is named on this profile, which by F5-26 is every run; the URL is also in section 8.

### F5-24 Sample: f5_act_when_ready
- Kind: sample-prompt
- Rule: Include an act-when-ready instruction to stop Fable 5 from overplanning on ambiguous tasks.
- Page says: see snippet `f5_act_when_ready`; opens "When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages."
- Applies when: The request is ambiguous or open-ended, or the model is prone to planning loops.
- Skill applies it by: Grafts verbatim into `<constraints>` for ambiguous or open-ended requests, and for routine work run at higher effort (F5-29).

Page section: Consider all effort levels

### F5-25 Effort is the primary trade-off control
- Kind: fact
- Rule: Treat effort as the primary control for the intelligence, latency, and cost trade-off.
- Page says: "[Effort](https://platform.claude.com/docs/en/build-with-claude/effort) is the primary control for the trade-off between intelligence, latency, and cost on Claude Fable 5."
- Applies when: Tuning speed versus quality.
- Skill applies it by: Effort is a parameter, not prompt prose: the skill recommends a level in the Target model item and writes no "think harder" line into the prompt.

### F5-26 high default, xhigh for capability-sensitive, medium or low for routine
- Kind: technique
- Rule: Use `high` as the default effort, `xhigh` for the most capability-sensitive workloads, and `medium` or `low` for routine work.
- Page says: "Use `high` as the default for most tasks, with `xhigh` for the most capability-sensitive workloads and `medium` or `low` for routine work."
- Applies when: Choosing effort per task.
- Skill applies it by: The Target model item suggests a level matching the request class, and does so on every run, including one where the target is the executing model, because the page states these defaults unconditionally and makes effort the primary trade-off control here (F5-25); only `low`, `medium`, `high`, and `xhigh` are offered, because the page names no `max`.

### F5-27 Lower effort here can beat xhigh on prior models
- Kind: fact
- Rule: Expect lower effort on Fable 5 to still perform well and often exceed `xhigh` on prior models.
- Page says: "Lower effort settings on Claude Fable 5 still perform well and often exceed `xhigh` performance on prior models."
- Applies when: Deciding whether a routine task needs high effort.
- Skill applies it by: Recommends `medium` or `low` for routine rearticulations without a quality caveat, and says so when a user worries about the step-down; on a routine same-model run the step-down is still named in the Target model item rather than left implicit.

### F5-28 Reduce effort when a task is slow but correct
- Kind: technique
- Rule: Reduce effort if a task completes but takes longer than necessary, or when a quicker interactive style is wanted.
- Page says: "Reduce effort if a task completes but takes longer than necessary, or if you want a quicker, more interactive working style."
- Applies when: Turns are slow but correct.
- Skill applies it by: After a slow but successful run, the recap suggests a lower effort for follow-ups (section 6).

### F5-29 Over-gathering on routine work at higher effort
- Kind: model-note
- Rule: Expect over-gathering and over-deliberation on routine work at higher effort.
- Page says: "On routine work at higher effort, Claude Fable 5 can gather context and deliberate beyond what the task needs."
- Applies when: Routine tasks run at `high` or `xhigh`.
- Skill applies it by: Adds `f5_act_when_ready` or `f5_scope_discipline` for routine tasks, or recommends a lower effort in the Target model item.

### F5-30 Higher effort brings the best verification and rigour
- Kind: model-note
- Rule: Use higher effort when verification rigour and sophisticated reasoning matter.
- Page says: "At the same time, higher effort often produces excellent verification behavior, sophisticated reasoning, and the most rigorous output."
- Applies when: Capability-sensitive tasks.
- Skill applies it by: Keeps `high` or `xhigh` for correctness-critical rearticulations, and on a long-running build pairs them with `f5_self_verification_interval`; on a short correctness-critical task the verification weight goes into concrete checks in `<verification>` instead, because that snippet's own condition is a long build (F5-68, F5-69).

### F5-31 Sample: f5_scope_discipline
- Kind: sample-prompt
- Rule: Include a scope-discipline instruction to prevent unrequested tidying or refactoring at higher effort.
- Page says: see snippet `f5_scope_discipline`; opens "Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need surrounding cleanup and a one-shot operation usually doesn't need a helper."
- Applies when: Coding tasks, especially bug fixes or one-shot operations, at `high` or `xhigh` effort.
- Skill applies it by: Grafts verbatim into `<constraints>` of coding rearticulations; it is the Fable 5 form of the scope-control technique, in place of the Fable 5.1 `keep_changes_to_task` and the guide's `minimize_overengineering`.

Page section: Strong instruction following

### F5-32 Steer with a brief instruction, not an enumeration
- Kind: technique
- Rule: Steer behaviour with a brief instruction instead of enumerating each behaviour by name.
- Page says: "Instruction-following is improved enough that you can steer most behaviors with a brief instruction rather than enumerating each behavior by name."
- Applies when: Writing behaviour constraints for Fable 5.
- Skill applies it by: Collapses long lists of do-and-don't bullets into one principle-level instruction; each collapsed list is recorded in the Changed line.

### F5-33 Un-steered elaboration at higher effort
- Kind: model-note
- Rule: Expect un-steered elaboration at higher effort: surveying unpursued options, long root-cause explanations, heavily-structured PR descriptions, and comments narrating the next line.
- Page says: "For example, when un-steered, Claude Fable 5 can elaborate beyond what the task needs, especially at higher effort settings: surveying options it won't pursue, explaining root causes at length, producing heavily-structured PR descriptions, or writing comments that narrate what the next line does. A short brevity instruction is as effective as listing each pattern:"
- Applies when: Any Fable 5 output where brevity matters.
- Skill applies it by: Grafts `f5_lead_with_outcome` rather than listing each elaboration pattern; the enumerated version, if the user pasted one, is removed and recorded.

### F5-34 Sample: f5_lead_with_outcome
- Kind: sample-prompt
- Rule: Include a lead-with-the-outcome brevity instruction that favours readability over compression.
- Page says: see snippet `f5_lead_with_outcome`; opens "Lead with the outcome. Your first sentence after finishing should answer \"what happened\" or \"what did you find\"" and closes "The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon."
- Applies when: Any rearticulated prompt whose output is read by a person, most of all at high effort.
- Skill applies it by: Grafts verbatim into `<output_format>` as the default output-style block for this profile; the skill's own final message follows the same shape when Fable 5 is the executing model (section 6). This is the page-supplied brevity block, so Standing rule 12's ban on a self-written be-concise line is satisfied by grafting it rather than paraphrasing it.

### F5-35 One checkpoint instruction, not a list of approval points
- Kind: technique
- Rule: Do not enumerate every checkpoint case in long-running workflows; one instruction about when to stop suffices.
- Page says: "The same applies to checkpoint behavior in long-running workflows. To have Claude Fable 5 stop only where it genuinely needs you, there is no need to enumerate every case:"
- Applies when: Long-running workflows with user checkpoints.
- Skill applies it by: Uses `f5_pause_only_when_needed` in place of a list of approval points; the `[confirm]` markers from Step 1f stay, because they name specific side-effecting steps rather than describing a policy.

### F5-36 Sample: f5_pause_only_when_needed
- Kind: sample-prompt
- Rule: Include a pause-only-when-needed checkpoint instruction.
- Page says: see snippet `f5_pause_only_when_needed`; the text is "Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise."
- Applies when: Multi-step or long-running rearticulations on Fable 5.
- Skill applies it by: Grafts verbatim into `<execution_guidance>` of multi-step prompts, paired with `f5_autonomous_reminder` for unattended pipelines (F5-51).

Page section: Ground progress claims during long runs

### F5-37 Audit progress against tool results
- Kind: technique
- Rule: Instruct Fable 5 to audit progress claims against actual tool results on long runs.
- Page says: "On long autonomous runs, instruct Claude Fable 5 to audit progress against actual tool results. In Anthropic's testing, this nearly eliminated fabricated status reports even on tasks designed to elicit them:"
- Applies when: Long autonomous runs that report status.
- Skill applies it by: Includes `f5_ground_progress` in multi-step and long-running rearticulations; the skill's own final report follows it when Fable 5 executes (section 6).

### F5-38 Sample: f5_ground_progress
- Kind: sample-prompt
- Rule: Include an evidence-audit instruction for progress reports.
- Page says: see snippet `f5_ground_progress`; opens "Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly."
- Applies when: Any prompt where the model will report on work it performed with tools.
- Skill applies it by: Grafts verbatim into `<success_criteria>` or `<verification>` for tool-using tasks; it is the replacement for a show-your-reasoning line stripped under F5-71.

Page section: State the boundaries

### F5-39 Occasional unrequested actions
- Kind: model-note
- Rule: Define explicit constraints, because Fable 5 can occasionally take unrequested actions such as drafting an email or creating defensive git-branch backups.
- Page says: "Claude Fable 5 can occasionally take unrequested actions (drafting an email when none was asked for, creating defensive git-branch backups). Define explicit constraints on what Claude Fable 5 should and should not do:"
- Applies when: Requests that are questions, problem descriptions, or thinking out loud.
- Skill applies it by: States the deliverable type explicitly in the posture sentence of `<task>` (assessment versus change) and adds `f5_state_boundaries` when the request is diagnostic.

### F5-40 Sample: f5_state_boundaries
- Kind: sample-prompt
- Rule: Include a boundaries instruction that makes the assessment the deliverable for diagnostic requests and gates state-changing commands on evidence.
- Page says: see snippet `f5_state_boundaries`; opens "When the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one." and continues with the evidence gate "Before running a command that changes system state (restarts, deletes, config edits), check that the evidence actually supports that specific action.", closing "A signal that pattern-matches to a known failure may have a different cause."
- Applies when: Diagnostic, investigative, or question-shaped requests on Fable 5.
- Skill applies it by: Grafts verbatim into `<constraints>` under the assess posture; when Fable 5 executes, the skill applies no fix to a request that was a question (Step 1d, Standing rules 4 and 7).

Page section: Parallel subagents

### F5-41 Dispatches parallel subagents readily
- Kind: model-note
- Rule: Expect Fable 5 to dispatch parallel subagents more readily than prior models.
- Page says: "Claude Fable 5 dispatches parallel subagents more readily than prior models."
- Applies when: Tasks with parallelizable subtasks.
- Skill applies it by: Adds no encouragement to delegate, only guidance on when delegation is appropriate; the guide's damping `subagent_usage_policy` is not grafted on this profile.

### F5-42 Use subagents frequently, communicate asynchronously
- Kind: technique
- Rule: Use subagents frequently, give explicit delegation guidance, and prefer asynchronous orchestrator-to-subagent communication over blocking.
- Page says: "Use subagents frequently, provide explicit guidance about when delegation is appropriate, and prefer asynchronous communication between orchestrator and subagents over blocking until each subagent returns."
- Applies when: Orchestrating multi-part work on Fable 5.
- Skill applies it by: `<task>` says which parts are independent and may be delegated; when executing, the skill runs subagents in parallel and keeps working rather than waiting on each (section 6).

### F5-43 Long-lived subagents save time and cost
- Kind: fact
- Rule: Prefer long-lived subagents that keep context across subtasks to save time and cost through cache reads.
- Page says: "Long-lived subagents that keep their context across subtasks save time and cost through cache reads and avoid bottlenecking on the slowest subagent."
- Applies when: Designing subagent lifetimes.
- Skill applies it by: Reuses one subagent across related subtasks instead of spawning a fresh one per subtask, and says so in `<execution_guidance>` when the prompt sets up an orchestration.

### F5-44 Sample: f5_delegate_subagents
- Kind: sample-prompt
- Rule: Include a delegate-and-keep-working instruction.
- Page says: see snippet `f5_delegate_subagents`; the text is "Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context."
- Applies when: Multi-part rearticulations where subagents are available.
- Skill applies it by: Grafts verbatim into `<execution_guidance>` of multi-part prompts, next to the guide's `use_parallel_tool_calls`.

Page section: Construct a memory system

### F5-45 Provide a place to write notes
- Kind: technique
- Rule: Provide a place for the model to record lessons from previous runs, as simple as a Markdown file.
- Page says: "Claude Fable 5 performs particularly well when it can record lessons from previous runs and reference them. Provide a place to write notes, as simple as a Markdown file:"
- Applies when: Recurring or multi-session work.
- Skill applies it by: `<context>` names the memory location (in this workspace, the project memory directory indexed by `MEMORY.md`) and `<task>` instructs the model to consult and update it.

### F5-46 Sample: f5_memory_notes
- Kind: sample-prompt
- Rule: Include a one-lesson-per-file memory discipline instruction.
- Page says: see snippet `f5_memory_notes`; opens "Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered." and closes "Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong."
- Applies when: Prompts that ask the model to maintain memory or notes.
- Skill applies it by: Grafts verbatim when the request involves recording lessons or maintaining a notes directory, and only where no harness or project convention already sets the format.

### F5-47 Bootstrap memory from past sessions
- Kind: technique
- Rule: Bootstrap the memory system by having the model review past sessions.
- Page says: "To bootstrap the memory system from existing history, have Claude Fable 5 review past sessions:"
- Applies when: Starting a memory system where prior session history exists.
- Skill applies it by: Offers `f5_memory_bootstrap` as the prompt for an initial memory-building pass, with the memory path filled in.

### F5-48 Sample: f5_memory_bootstrap
- Kind: sample-prompt
- Rule: Use the reflect-on-previous-sessions prompt to seed memory.
- Page says: see snippet `f5_memory_bootstrap`; the text is "Reflect on the previous sessions we've had together. Use subagents to identify core themes and lessons, and store them in [X]. Make sure you know to reference [X] for future use."
- Applies when: A user asks to build or seed memory from history.
- Skill applies it by: Fills `[X]` with the memory path and uses the filled text as the body of `<task>`; the substitution is recorded in the Assumed line.

Page section: Rare cases of early stopping

### F5-49 Text-only statements of intent, or needless permission requests
- Kind: model-note
- Rule: Watch for turns ending in a text-only statement of intent without the tool call, or needless permission requests, deep into long sessions.
- Page says: "Deep into a long session, Claude Fable 5 can occasionally end a turn with a text-only statement of intent (\"I'll now run X\") without issuing the corresponding tool call, or pause to ask permission when it already has enough to proceed."
- Applies when: Long sessions on Fable 5.
- Skill applies it by: Step 7's last-paragraph check is treated as load-bearing on this profile; for unattended runs the prompt carries `f5_autonomous_reminder`.

### F5-50 A continue is enough to recover
- Kind: technique
- Rule: Recover from early stopping with a simple continue or go-ahead message.
- Page says: "A \"continue\" or \"go ahead and do it end to end\" suffices."
- Applies when: The model stopped with a stated intent but no action.
- Skill applies it by: Tells the user that a one-word continue is enough; no rewritten prompt is needed, and the already-shown prompt is not re-presented (Standing rule 10).

### F5-51 Pair the reminder with the checkpoint instruction
- Kind: technique
- Rule: Pair the autonomous reminder with the checkpoint instruction to define when pausing is appropriate.
- Page says: "To define when pausing is appropriate, pair this with the checkpoint instruction in [Strong instruction following](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5#strong-instruction-following). For autonomous pipelines, add a system reminder:"
- Applies when: Autonomous pipelines on Fable 5.
- Skill applies it by: Emits `f5_pause_only_when_needed` together with `f5_autonomous_reminder` so the two define both when to stop and when not to; neither is grafted alone for an unattended run.

### F5-52 Sample: f5_autonomous_reminder
- Kind: sample-prompt
- Rule: Include the autonomous-operation system reminder for unattended pipelines.
- Page says: see snippet `f5_autonomous_reminder`; opens "You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking \"Want me to…?\" or \"Shall I…?\" will block the work." and closes "End your turn only when the task is complete or you are blocked on input only the user can provide."
- Applies when: Unattended or scheduled runs, and when the user has said to proceed end to end.
- Skill applies it by: Grafts verbatim as the posture snippet in `<execution_guidance>` when the user indicates they will not be watching or asks for end-to-end completion; it is the Fable 5 counterpart of the Fable 5.1 `operating_autonomously`. When Step 1f found side effects, the confirmations sentence follows it, and Step 2 resolves ambiguity before it is grafted, because it lowers the model's tendency to ask.

Page section: Rare cases of context-budget concern

### F5-53 Session-length worry, triggered by a visible countdown
- Kind: model-note
- Rule: Expect occasional suggestions of a new session, summarize-and-hand-off, or trimmed work in very long sessions, most often triggered by a visible remaining-token countdown.
- Page says: "In very long sessions, Claude Fable 5 can occasionally suggest a new session, offer to summarize and hand off, or trim its own work. This is most often triggered when the harness shows a remaining-token countdown to the model."
- Applies when: Very long sessions.
- Skill applies it by: When executing, the skill does not trim or hand off work because of a token countdown (section 6); when composing, it never quotes remaining-token counts into the prompt.

### F5-54 Do not surface context-budget counts
- Kind: technique
- Rule: Avoid surfacing explicit context-budget counts to the model.
- Page says: "Avoid surfacing explicit context-budget counts where possible. If the harness must show them, a reassurance helps:"
- Applies when: Harness design and prompt content.
- Skill applies it by: Strips token-budget and context-remaining figures from the rearticulated prompt and records the removal; if the harness shows them anyway, adds `f5_ample_context`.

### F5-55 Sample: f5_ample_context
- Kind: sample-prompt
- Rule: Include a context reassurance when a token countdown is visible.
- Page says: see snippet `f5_ample_context`; the text is "You have ample context remaining. Do not stop, summarize, or suggest a new session on account of context limits. Continue the work."
- Applies when: The harness displays a remaining-token countdown.
- Skill applies it by: Appends to `<execution_guidance>` only when the environment exposes context counts to the model; never with a figure attached.

Page section: Give the reason, not only the request

### F5-56 Intent behind the request improves performance
- Kind: technique
- Rule: Provide the intent behind the request, especially for long-running agents drawing on multiple workstreams.
- Page says: "Claude Fable 5 tends to perform better when it understands the intent behind a request: context lets it connect the task to relevant information rather than inferring intent on its own. Provide context about why you're asking, especially for long-running agents drawing on multiple workstreams:"
- Applies when: Every rearticulation; strongest for long-running or multi-workstream work.
- Skill applies it by: Fills `<context>` with the larger task, the audience, and what the output enables, using the `f5_give_reason` frame.

### F5-57 Sample: f5_give_reason
- Kind: sample-prompt
- Rule: Frame the request with the larger task, the audience, and what the output enables.
- Page says: see snippet `f5_give_reason`; the text is "I'm working on [the larger task] for [who it's for]. They need [what the output enables]. With that in mind: [request]."
- Applies when: Any request where the user's purpose is known or can be asked.
- Skill applies it by: Uses the frame as the shape of `<context>` with the slots filled from CLAUDE.md, memory, the named files, and earlier turns; asks the user for a missing slot only when it changes the deliverable, and records an inferred slot in the Assumed line.

Page section: Readability when communicating with the user

### F5-58 Hard-to-follow text in extended agentic conversations
- Kind: model-note
- Rule: Expect hard-to-follow text in extended agentic conversations: arrow-chain shorthand, deep implementation detail, references to unseen thinking, overly technical phrasing.
- Page says: "In extended or agentic conversations (many tool calls, large working context), Claude Fable 5 can produce text that's hard to follow: dense arrow-chain shorthand, deep implementation detail, references to thinking the user never saw, or overly technical phrasing. A communication-style addendum mitigates this:"
- Applies when: Agentic tasks with many tool calls.
- Skill applies it by: Includes `f5_readability_addendum` for tool-heavy tasks; the skill's own final message uses no arrow chains and no labels it invented while working (section 6).

### F5-59 Sample: f5_readability_addendum
- Kind: sample-prompt
- Rule: Include the communication-style addendum distinguishing working shorthand from the final summary.
- Page says: see snippet `f5_readability_addendum`; opens "Terse shorthand is fine between tool calls (that's you thinking out loud, and brevity there is good). Your final summary is different: it's for a reader who didn't see any of that." and closes "If you have to choose between short and clear, choose clear."
- Applies when: Extended agentic rearticulations on Fable 5.
- Skill applies it by: Grafts verbatim into `<output_format>` for tool-heavy or long unattended tasks; it overlaps `f5_lead_with_outcome`, so exactly one of the two is grafted, chosen by task length (the addendum for long agentic runs, the shorter block otherwise), and the choice is recorded.

Page section: Create a send-to-user tool

### F5-60 A tool for verbatim mid-turn messages
- Kind: technique
- Rule: Give long asynchronous agents a tool to surface verbatim messages to the user without ending the turn.
- Page says: "When running long, asynchronous agents, give the agent a way to surface a message the user must see exactly as written, without ending its turn: a deliverable (a generated code snippet or a drafted message), a progress update with specific numbers, or a direct reply to a question the user asked mid-loop."
- Applies when: Long asynchronous agent harnesses.
- Skill applies it by: Harness-level, recorded in section 2. Claude Code has no `send_to_user` tool, so in-session the skill puts deliverables in the final message and does not rely on mid-turn text arriving verbatim.

### F5-61 Implementation contract for the tool
- Kind: fact
- Rule: Render the tool's input directly in the UI and return a simple acknowledgement; tool inputs are never summarized.
- Page says: "The tool's input is the message to display; when Claude calls it, render the input directly in your UI and return a simple acknowledgement as the tool result. Tool inputs are never summarized, so the content arrives intact."
- Applies when: Implementing the send-to-user tool in a harness.
- Skill applies it by: Section 2 records the contract for harness-authoring requests; it is not applied inside ordinary rearticulated prompts.

### F5-62 Sample: send_to_user
- Kind: sample-prompt
- Rule: Define the `send_to_user` tool with a single required string input named `message`.
- Page says: the JSON tool definition printed in "Create a send-to-user tool", stored verbatim as the snippet `send_to_user`. The page prints it as a multi-line JSON block, so it is described here rather than reflowed into a quoted span. Its name is `send_to_user`, its description is "Display a message directly to the user. Use this for progress updates, partial results, or content the user must see exactly as written before the task finishes.", and its `input_schema` has one property, `message`, listed in `required`.
- Applies when: Building a harness for long asynchronous Fable 5 agents.
- Skill applies it by: Stored verbatim in `references/snippet-library.md` under the id `send_to_user` for harness-authoring deliverables; the skill does not add tool definitions to ordinary rearticulated prompts.

### F5-63 Add the tool only for verbatim mid-task delivery
- Kind: technique
- Rule: Add the tool only when UX depends on verbatim mid-task delivery; routine progress narration is covered by the model's own summaries.
- Page says: "Add this tool whenever your UX depends on delivering content or direct user interactions verbatim mid-task. For agents that only narrate routine progress, the model's own summaries are typically adequate."
- Applies when: Deciding whether a harness needs the tool.
- Skill applies it by: Recommends the tool only for deliverable-carrying asynchronous agents, not for every pipeline.

### F5-64 The definition alone is not enough
- Kind: fact
- Rule: Pair the tool with a system-prompt instruction, since defining it alone is not enough for Fable 5 to call it.
- Page says: "Defining the tool is not sufficient on its own; without an instruction in the system prompt, Claude Fable 5 rarely calls it. Pair the tool with elicitation language such as:"
- Applies when: The `send_to_user` tool is present.
- Skill applies it by: When the environment exposes such a tool, `f5_send_to_user_elicitation` goes into the prompt alongside the definition; a harness deliverable that defines the tool without elicitation language is flagged.

### F5-65 Sample: f5_send_to_user_elicitation
- Kind: sample-prompt
- Rule: Include elicitation language telling the model when to call `send_to_user`.
- Page says: see snippet `f5_send_to_user_elicitation`; the text is "Between tool calls, when you have content the user must read verbatim (a partial deliverable, a direct answer to their question), call the send_to_user tool with that content. Use send_to_user only for user-facing content, not for narration or reasoning."
- Applies when: A `send_to_user` tool is defined in the harness.
- Skill applies it by: Grafts verbatim into the tools part of `<execution_guidance>` when the tool exists; omitted otherwise, since Claude Code does not provide it.

### F5-66 Do not route narration through the tool
- Kind: anti-pattern
- Rule: Do not route narration or internal reasoning through `send_to_user`.
- Page says: "Do not route narration or internal reasoning through `send_to_user`; over-calling it for non-user-facing content defeats the purpose."
- Applies when: Any prompt using the `send_to_user` tool.
- Skill applies it by: Section 5 removes instructions that would push progress narration or reasoning through the tool and keeps it for user-facing content only.

Page section: Recommended scaffolding changes

### F5-67 Start at the top of your difficulty range
- Kind: technique
- Rule: Start at the top of the difficulty range and have Fable 5 scope the task, ask clarifying questions, and execute.
- Page says: "**Start at the top of your difficulty range.** Pick a task harder than what you'd assign to prior models, and have Claude Fable 5 scope it, ask clarifying questions, and execute."
- Applies when: Choosing task granularity for Fable 5.
- Skill applies it by: `<task>` hands over the whole goal with an explicit instruction to scope it, ask only the questions that change the deliverable, and execute, instead of slicing it into small tasks (with F5-04, F5-17).

### F5-68 Self-verification by fresh-context verifier subagents
- Kind: technique
- Rule: Make self-verification explicit in long-run prompts and prefer fresh-context verifier subagents over self-critique.
- Page says: "**Make self-verification explicit in long-run prompts.** Separate, fresh-context verifier subagents tend to outperform self-critique. For long-running tasks, instruct: `Establish a method for checking your own work at an interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the specification.`"
- Applies when: Long-running build tasks on Fable 5.
- Skill applies it by: Implements the self-check technique on this profile as verification against the specification by a fresh-context subagent at a set interval, not as "review your own reasoning"; `<verification>` carries `f5_self_verification_interval` alongside the guide's concrete checks.

### F5-69 Sample: f5_self_verification_interval
- Kind: sample-prompt
- Rule: Include an interval-based self-verification instruction using subagents against the specification.
- Page says: see snippet `f5_self_verification_interval`; the text is "Establish a method for checking your own work at an interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the specification."
- Applies when: Long-running build or implementation prompts.
- Skill applies it by: Fills `[X]` with a concrete interval (for example after each module or each completed file) and places the filled text in `<verification>`; the interval chosen is recorded in the Assumed line.

### F5-70 Refactor prompts and skills written for prior models
- Kind: technique
- Rule: Refactor prompts and skills written for prior models; remove overly prescriptive instructions when default performance is better.
- Page says: "**Refactor existing prompts and skills.** Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality. Review and consider removing older instructions if default performance is better. Claude Fable 5 also does a good job of updating skills on the fly based on what it learns from the task at hand."
- Applies when: Migrating prompts or skills from Opus 4.8 or older.
- Skill applies it by: Reduces a legacy step-by-step prescription to intent plus constraints and records the reduction; when the request is to improve a skill, the deliverable stays principle-level rather than exhaustive.

### F5-71 Do not instruct the model to reproduce its reasoning
- Kind: anti-pattern
- Rule: Do not instruct the model to echo, transcribe, or explain its internal reasoning in the response; it can trigger the `reasoning_extraction` refusal category.
- Page says: "**Don't instruct Claude to reproduce its reasoning in the response.** Prompts, skills, or harness instructions that tell the model to echo, transcribe, or explain its internal reasoning as response text can trigger the [`reasoning_extraction` refusal category](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#refusal-response) on Claude Fable 5, causing elevated fallbacks to Claude Opus 4.8. Audit existing skills and system prompts for reflection or show-your-thinking instructions when migrating."
- Applies when: Any prompt, skill, or harness instruction containing show-your-reasoning, think-aloud, explain-your-thinking, or reflection wording targeting Fable 5.
- Skill applies it by: Section 5 strips those lines, and the audit covers the pasted prompt, the skill files it names, and any system prompt in scope, not only the request sentence; the replacement is outcome-first reporting plus evidence-grounded verification (`f5_lead_with_outcome`, `f5_ground_progress`). Each strip is recorded in the Changed line.

### F5-72 Reasoning visibility comes from thinking blocks and a send-to-user tool
- Kind: link
- Rule: Obtain reasoning visibility from the structured thinking blocks of adaptive thinking, and surface progress with a send-to-user tool, instead of asking the model to reproduce its reasoning.
- Page says: "If your application needs reasoning visibility, read the structured `thinking` blocks from [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) instead, and use a [send-to-user tool](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5#create-a-send-to-user-tool) to surface progress during long runs."
- Applies when: A user wants to see the model's reasoning or progress.
- Skill applies it by: Explains that thinking blocks (summarized only, F5-08) and a progress tool are the sanctioned route, cites the adaptive thinking page in section 8, and writes no reasoning-echo instruction.

### F5-73 Create a send-to-user tool (scaffolding bullet)
- Kind: link
- Rule: Create a client-side send-to-user tool for long asynchronous agents.
- Page says: "**Create a send-to-user tool.** For long, asynchronous agents, a client-side tool delivers messages to the user verbatim without ending the turn. See [Create a send-to-user tool](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5#create-a-send-to-user-tool)."
- Applies when: Harness design for long asynchronous Fable 5 agents.
- Skill applies it by: Cross-references `send_to_user` and `f5_send_to_user_elicitation` in section 7; the fourth of the four scaffolding changes in section 4.

Guide rules naming Fable 5 and Mythos 5 (from Prompting best practices; catalog IDs, quoted from the guide)

### BP-002 Fable 5 and Mythos 5 are inside the guide's covered set
- Kind: fact
- Rule: Treat the guide as authoritative for exactly these eleven current models and route any other model to the migration considerations.
- Guide says: "This is the reference for prompt engineering with current Claude models, including Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, and Claude Haiku 4.5."
- Applies when: Resolving whether guide techniques are measured on the target.
- Skill applies it by: Fable 5 and Mythos 5 need no analogy note; the guide applies directly.

### BP-009 Introducing Fable 5 link
- Kind: link
- Rule: Point to Introducing Claude Fable 5 and Claude Mythos 5 for Fable 5 capabilities and API changes.
- Guide says: "For Claude Fable 5 capabilities and API changes, see [Introducing Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5)."
- Applies when: The user targets Fable 5 or Mythos 5 in a prompt-authoring request.
- Skill applies it by: Section 8 Related pages, together with F5-02.

### BP-015 The guide's model table row for Fable 5 and Mythos 5
- Kind: model-note
- Rule: For Fable 5 or Mythos 5, check effort levels, instruction following, long-run progress claims, memory systems, and the `reasoning_extraction` refusal category.
- Guide says: "| Claude Fable 5 and Claude Mythos 5 | [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) | Differences from Claude Opus 4.8: effort levels, instruction following, long-run progress claims, memory systems, and the `reasoning_extraction` refusal category. |"
- Applies when: The user targets Fable 5 or Mythos 5.
- Skill applies it by: The five topics are the checklist for sections 4 to 6: effort in the Target model item, brief-instruction steering in `<constraints>`, `f5_ground_progress` for progress claims, the memory snippets for recurring work, and the F5-71 strip for reasoning echo.

### BP-020 Prompting Claude Fable 5 page link
- Kind: link
- Rule: Open the Prompting Claude Fable 5 page for Fable 5 and Mythos 5 specifics.
- Guide says: "[Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)"
- Applies when: The user targets Fable 5 or Mythos 5.
- Skill applies it by: This file is the local rendering of that page; the header cites it.

### BP-024 General principles apply to Fable 5 and Mythos 5
- Kind: fact
- Rule: Apply the general-principle techniques to every current model, including Fable 5.1, Mythos 5.1, Fable 5, and Mythos 5, without needing a model-specific exception unless one is stated.
- Guide says: "The techniques in this section and the sections that follow apply to current Claude models, including Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, and Claude Mythos 5."
- Applies when: Every rearticulation on this profile.
- Skill applies it by: The always-on template tags are filled for Fable 5 exactly as for any other model; only the conditional tags consult this profile.

### BP-189 budget_tokens returns 400 on 4.7 and later
- Kind: fact
- Rule: Never emit `budget_tokens` for Claude 4.7 or later models; the API returns a 400 error.
- Guide says: "On Claude 4.7 and later models, setting `budget_tokens` returns a 400 error."
- Applies when: Any generated or migrated API configuration for Fable 5 or Mythos 5.
- Skill applies it by: Strips `budget_tokens`, substitutes adaptive thinking plus `output_config.effort`, and records the substitution with the 400 reason (with F5-08).

### BP-195 Thinking always on for the Fable and Mythos models
- Kind: model-note
- Rule: For Claude Fable 5.1, Mythos 5.1, Fable 5, and Mythos 5, assume thinking is always on and adaptive is the only mode.
- Guide says: "On Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, and Claude Mythos 5, thinking is always on and adaptive thinking is the only mode."
- Applies when: Any Fable 5 or Mythos 5 target, and whenever a prompt-authoring request names one.
- Skill applies it by: Adds no manual chain-of-thought scaffolding, no `<thinking>`/`<answer>` output tags, and no "think step by step" fallback; never proposes disabling thinking.

### BP-220 Thinking always on regardless of the parameter
- Kind: model-note
- Rule: On Fable 5.1, Mythos 5.1, Fable 5, and Mythos 5, thinking is always on regardless of the thinking parameter.
- Guide says: "On Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, and Claude Mythos 5, thinking is always on, regardless of whether you set the `thinking` parameter."
- Applies when: A pasted configuration sets or clears the `thinking` parameter for a Fable 5 target.
- Skill applies it by: Removes the parameter as inert and records it; the Target model item says thinking needs no configuration on this profile.

### BP-364 Prompting Claude Fable 5 card
- Kind: link
- Rule: Consult Prompting Claude Fable 5 for Fable 5 and Mythos 5 differences covering effort, instruction following, long runs, memory, and scaffolding changes.
- Guide says: "<Card title=\"Prompting Claude Fable 5\" icon=\"terminal\" href=\"https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5\"> Behavioral differences and prompting patterns for Claude Fable 5 and Claude Mythos 5, covering effort, instruction following, long runs, memory, and scaffolding changes. </Card>"
- Applies when: The target model is Claude Fable 5 or Claude Mythos 5.
- Skill applies it by: Cited as the source of this file; no prompt text change by itself.

## When this is the TARGET model: add to the rearticulated prompt

The content of the rearticulated prompt follows this section when the target is Fable 5 or Mythos 5, whether the prompt runs in-session or is authored for an application. The Fable 5.1 default snippets (progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule, mannered_prose_short, long_output_budget_note) are not grafted; their Fable 5 counterparts are named below. Instruction granularity on this profile is principle-level: one short instruction in place of an enumerated behaviour list (F5-32), with numbered work steps kept only where order or completeness matters.

Target model item (SKILL.md Step 5 assumptions). Always `Target model: fable-5 (<how resolved>)`. On this profile the recommended effort level is always named, even when the target is the executing model, because effort is the primary trade-off control here and the page prints explicit defaults (F5-25, F5-26), with the Effort page cited alongside it (F5-23). When the target differs from the executing model, the request is prompt authoring, or the user asked about speed, cost, or thinking, append the rest: recommended effort with the page section cited (default `high`, F5-26; `xhigh` for the most capability-sensitive workloads, F5-26, F5-30; `medium` or `low` for routine work, F5-26, F5-27; a step down when a run was slow but correct, F5-28; no `max`, which this page does not name); thinking always on, adaptive only, summarized output, nothing to configure (F5-08, BP-195, BP-220); `budget_tokens` removed with the 400 reason (F5-08, BP-189); sampling parameters flagged "not printed for this model, check Introducing Claude Fable 5 and Claude Mythos 5" rather than asserted; no `max_tokens` figure printed, and instead the expectation that a hard task can run for many minutes and an autonomous run for hours, so client timeouts, streaming, and progress indicators are the harness's business and long runs are checked asynchronously (F5-21, F5-22); no remaining-token figure quoted anywhere (F5-54); Claude Opus 4.8 named as the documented fallback for a refusal, with server-side or client-side fallback configured outside the prompt (F5-11); an effort level carried from another profile marked unverified and re-derived here (`model-notes.md` section 7); the model string looked up rather than invented when API code is produced (BP-059).

- `<role>`: one sentence, domain-matched, per the guide. For an authored system prompt the guide's model_identity and model_string samples are grafted with the display name substituted (Claude Fable 5 or Claude Mythos 5) and the model string looked up in the models overview, since the guide prints Opus 5 in both samples (BP-082, BP-084).
- `<context>`: the `f5_give_reason` frame, filled with the larger task, who it is for, and what the output enables (F5-56, F5-57). Name the consumer of the output, because the readability and brevity blocks depend on whether a person reads it (F5-58). For security, vulnerability, or investigation work state the defensive or investigative purpose and the asset owner in one sentence, because the classifiers cover offensive cybersecurity and benign work can trigger them (F5-09, F5-10). For recurring work name the memory location the model should consult and update (F5-45). No remaining-token counts, no context-budget language (F5-54). For an image-bearing request, no pre-description of what the image shows (F5-14).
- `<documents>`: guide rules unchanged, documents before `<task>` (BP-062). Images and screenshots are handed over as they are; a flipped, blurry, or noisy image is noted as such so the model reaches for crop or bash tools (F5-14).
- `<task>`: the end-to-end goal in one place, not pre-decomposed into small sequential steps (F5-04, F5-05, F5-17), with an explicit instruction to scope it, ask only the clarifying questions that change the deliverable, and execute (F5-67). A complete specification for complex builds, since first-shot correctness shows on well-specified problems (F5-13). Posture sentence first (assessment or change), because unrequested actions are the failure mode this page names (F5-39). Code review and debugging may search across the codebase and repository history (F5-16). Independent parts named as delegable (F5-42). For a memory-seeding request, the filled `f5_memory_bootstrap` text is the body (F5-48). For documents, spreadsheets, slides, and financial analysis, format and audience rather than quality exhortations (F5-15).
- `<constraints>`: `f5_scope_discipline` verbatim on coding tasks, most of all at `high` or `xhigh` effort (F5-29, F5-31); `f5_act_when_ready` when the request is ambiguous, open-ended, or routine-at-high-effort (F5-24, F5-29); `f5_state_boundaries` under the assess posture and for diagnostic or troubleshooting requests (F5-39, F5-40); `f5_memory_notes` when the prompt asks the model to maintain notes and no project convention already fixes the format (F5-45, F5-46). Skill-written constraint sentences stay positive with a because clause; grafted snippets stay verbatim. One principle-level sentence in place of a do-and-don't list (F5-32).
- `<output_format>`: exactly one of `f5_lead_with_outcome` (the default output-style block) or `f5_readability_addendum` (for tool-heavy and long unattended runs), chosen by task length and recorded (F5-33, F5-34, F5-58, F5-59). Positive statements of the wanted style; plain-text math when math appears; XML indicators when the output is parsed (guide). For enterprise deliverables the format and audience are stated here (F5-15).
- `<examples>`: guide rules unchanged, since the page prints nothing about examples: 3 to 5 examples when format, tone, or structure matters and can be shown, or the single `quoting_sources_example` for summaries of retrieved sources.
- `<success_criteria>`: observable criteria per the guide, including "files created or modified: only <the files named in task>". `f5_ground_progress` when the model will report on work it did with tools, so each claim is auditable against a tool result (F5-37, F5-38). For complex builds the acceptance criteria carry the weight that a reasoning plan would have carried on an older model (F5-13).
- `<execution_guidance>`: `f5_pause_only_when_needed` for multi-step work (F5-35, F5-36), paired with `f5_autonomous_reminder` whenever the run is unattended or the user asked for end-to-end completion (F5-49, F5-51, F5-52); the two are emitted together, never one alone, and the Step 1f confirmations sentence follows the reminder. `f5_delegate_subagents` for multi-part work, with long-lived subagents reused across related subtasks and communication asynchronous rather than blocking (F5-18, F5-41 to F5-44). `f5_ample_context` only when the harness shows the model a remaining-token countdown (F5-53 to F5-55). `f5_send_to_user_elicitation` only when the harness defines that tool, and never as a channel for narration or reasoning (F5-64 to F5-66). Crop and bash tool permission for degraded images (F5-14). The guide's `use_parallel_tool_calls`, `investigate_before_answering`, and `temp_file_cleanup` as the taxonomy row requires. No progress-cadence scaffolding from the Fable 5.1 page and no `batch_nudge`.
- `<verification>`: filled per the guide with concrete checks drawn from `<success_criteria>` (self_check_verify applies; this profile has no Opus 5 style exception), plus `f5_self_verification_interval` on long-running builds with `[X]` filled in, run by fresh-context verifier subagents against the specification rather than as self-critique (F5-68, F5-69). `f5_ground_progress` sits here when the reporting is the thing being verified (F5-38).
- Closing block: none specific to this profile. The last element of a long-deliverable prompt is whatever the taxonomy row requires from the guide, not the Fable 5.1 `long_output_budget_note`.

The four recommended scaffolding changes, as the skill applies them: start at the top of the difficulty range, so `<task>` carries the whole hard goal with scope-then-execute framing (F5-67); make self-verification explicit through fresh-context verifier subagents at an interval (F5-68, F5-69); refactor prompts and skills that are too prescriptive for this model, reducing legacy step-by-step prescriptions to intent plus constraints and recording each reduction (F5-70); and, for long asynchronous agents, create the send-to-user tool with its elicitation language (F5-60 to F5-65, F5-73). The fifth bullet of that page section is the reasoning-echo prohibition, which lives in section 5 (F5-71, F5-72).

Reasoning exhortations: none. Hand-written reasoning plans are dropped, effort is recommended in the Target model item instead (F5-25, F5-26), and show-your-reasoning, think-aloud, and reflection lines are removed rather than softened, because they can trigger the `reasoning_extraction` refusal category (F5-71). At most a general "think thoroughly" survives for a complex task (BP-221). No thinking configuration and no `<thinking>` output tags (BP-195, BP-220).

Design and frontend: this page has no design section, so one block is chosen rather than left open. A frontend build on a Fable 5 target takes `frontend_aesthetics_short`, with an `Assumed:` entry naming the Sonnet 5 and Opus 4.8 pages as the ones that measured it (S5-58, O48-57, BP-025). The guide's long `frontend_aesthetics` is not grafted here: it is stated for Opus 4.5 and Opus 4.6 (BP-330), two models older than this page's own baseline, and this page says Fable 5 is generally more capable than prior models on almost all tasks and that skills written for prior models are often too prescriptive and can degrade output quality (F5-19, F5-70); the Opus 4.8 page already reports needing less frontend prompting than earlier models (O48-55), so the trimmed block is the one that fits. This also matches fable-5-1, which inherits this profile and takes the short block. When the `frontend-design` skill is loaded the prompt says "Invoke frontend-design before <step>" instead of duplicating a snippet (SKILL.md, Working with other skills). Do not borrow the Opus 4.8 house-style palette for a Fable 5 target.

## When this is the TARGET model: remove or convert

Each conversion is recorded in the Changed line of the assumptions.

| Found in the raw request or pasted prompt | Action for a Fable 5 or Mythos 5 target | Basis |
|---|---|---|
| "show your reasoning", "think aloud", "explain your thinking", "walk me through your reasoning", reflection steps | Remove, do not soften; they can trigger the `reasoning_extraction` refusal category and elevated fallbacks to Opus 4.8. Replace with outcome-first reporting and evidence-grounded verification (`f5_lead_with_outcome`, `f5_ground_progress`) | F5-71 |
| Reflection or show-your-thinking instructions inside a skill file, harness wrapper, or system prompt the request names | Audit and remove there too, not only in the request sentence; say in the Changed line which file carried it | F5-71 |
| "show your full thinking", "print your thinking verbatim", a request for the raw thinking text | Remove; thinking output is summarized only, and asking for its extraction is one of the three classifier domains | F5-08, F5-09, F5-71 |
| A request to see the model's reasoning for a legitimate product need | Structured `thinking` blocks from adaptive thinking, plus a send-to-user tool for progress during long runs | F5-72, F5-73 |
| `budget_tokens`, `thinking: {type: "enabled", budget_tokens: N}`, "use N thinking tokens", "think for 30k tokens" | Remove; there are no extended thinking budgets on this family and the parameter returns a 400 on 4.7 and later. Adaptive thinking plus `output_config.effort` | F5-08, BP-189 |
| `thinking: {type: "disabled"}` or any disable attempt | Remove as inert; thinking is always on regardless of the parameter | BP-195, BP-220 |
| Remaining-token counts, "you have N tokens left", "wrap up before you run out of context" | Strip the figure. If the harness shows a countdown anyway, add `f5_ample_context` | F5-53, F5-54, F5-55 |
| "start a new session", "summarize and hand off when context gets tight" | Remove; continue the work instead | F5-53, F5-55 |
| Long enumerated do-and-don't lists ported from an Opus 4.8 prompt | Collapse into one principle-level instruction | F5-07, F5-19, F5-32 |
| An enumerated list of every approval checkpoint | `f5_pause_only_when_needed`, plus `f5_autonomous_reminder` when the run is unattended; `[confirm]` markers for named side-effecting steps stay | F5-35, F5-36, F5-51 |
| Prescriptive step-by-step skill instructions written for a prior model | Reduce to intent plus constraints; over-prescription degrades output here. Numbered work steps whose order or completeness matters stay | F5-70 |
| Opus 4.8-era guardrails, tool mandates, and instructions generally | Re-evaluate and drop what this page does not ask for; name each removal | F5-07, F5-19 |
| A large goal pre-sliced into small sequential steps | Restore the end-to-end goal and instruct scope, clarify, execute | F5-04, F5-05, F5-17, F5-67 |
| Heavy scaffolding on a simple request | Keep the prompt short; the model is reliable on straightforward tasks | F5-06, F5-19 |
| Quality exhortations on a document, spreadsheet, slide, or financial-analysis deliverable | Specify format and audience instead | F5-15 |
| Pre-described image contents, or legacy vision workarounds | Hand the image over as it is; note crop and bash tools for flipped, blurry, or noisy images | F5-14 |
| "wait for each subagent to return before continuing" | Asynchronous delegation with `f5_delegate_subagents`; reuse long-lived subagents across related subtasks | F5-42, F5-43, F5-44 |
| "review your own reasoning at each step" as the verification method | `f5_self_verification_interval`: fresh-context verifier subagents checking the work against the specification at an interval | F5-68, F5-69 |
| Narration or reasoning routed through `send_to_user` | Remove; the tool carries user-facing content only | F5-66 |
| A `send_to_user` tool definition with no elicitation language | Add `f5_send_to_user_elicitation`; the definition alone is rarely called | F5-62, F5-64, F5-65 |
| An offensive-security framing (build an exploit, write malware, attack tooling), or lab methods and molecular mechanisms | Do not rewrite to evade a warranted refusal. If the real purpose is defensive or investigative, state it plainly in `<context>`; otherwise report that the domain is outside this model's intended use and name Claude Opus 4.8 as the documented fallback | F5-09, F5-10, F5-11, F5-20 |
| An effort level or effort rationale carried from Opus 4.8 or another profile | Re-derive here and mark the carried value unverified; lower effort on this model often exceeds `xhigh` on prior models | F5-27, F5-28 |
| `max` effort | Not named on this page; recommend `low`, `medium`, `high`, or `xhigh` only | F5-26 |
| "think harder", "use maximum reasoning", stacked reasoning intensifiers | Remove; recommend an effort level in the Target model item | F5-25, F5-26 |
| Last-turn prefill, "start your answer with", "Sure, here is" | Convert to a direct instruction, a named output tag, or enumerated labels; prefill is unsupported from 4.6 onward | BP-124 |
| Fable 5.1 default snippets in a ported prompt (progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule, mannered_prose_short, long_output_budget_note) | Remove; measured on Fable 5.1. Use the `f5_*` counterparts named in section 4 | F5-03, section 4 |
| `temperature`, `top_p`, `top_k` | Flag "not printed for this model, check Introducing Claude Fable 5 and Claude Mythos 5"; do not assert a value or a 400 | F5-02, section 2 |

## When this is the EXECUTING model: how the skill behaves in Steps 5-7

Applies when the model running the skill resolves to Fable 5 or Mythos 5 (the Reading line then records the executing model as fable-5). SKILL.md Steps 6 and 7 are written for Fable 5.1; where this page differs, this section governs the skill's own behaviour. The rearticulated prompt's content still follows the target profile.

- Narration cadence: one line up front saying what is about to happen, then brief factual notes around tool batches. Terse shorthand between tool calls is fine, because that is working text (F5-59); the page asks for no set cadence and no suppression, so Step 6's per-batch update stands, written plainly. When a hard task is about to run long, the opening line says so, because a turn can take many minutes (F5-21).
- Final message shape: outcome first. The first sentence answers "what happened" or "what did you find", with supporting detail after (F5-34). After a long unattended stretch the recap is written as a re-grounding rather than a continuation of the working thread: complete sentences, terms spelled out, no arrow chains, no hyphen-stacked compounds, no labels invented mid-run, each file, commit, or flag in its own plain-language clause (F5-59). Step 7's three-to-eight-line shape and order are kept, facts only, no self-evaluation (BP-089).
- Progress-claim grounding: before reporting progress, audit each claim against a tool result from this session; report only what there is evidence for; say explicitly when something is not yet verified; report failures with the output, skipped steps as skipped, and finished-and-verified items plainly without hedging (F5-37, F5-38). This is the load-bearing rule for the Step 7 recap on this profile.
- Verification pass: Step 7 runs in full; this profile has no Opus 5 style exception. Checks come from `<verification>` and `<success_criteria>` and are run with tools rather than asserted. On a long build the skill verifies at an interval with a fresh-context verifier subagent against the specification instead of critiquing its own work (F5-68, F5-69), and it does not skip the interval to save time.
- Delegation: delegate independent subtasks and keep working while they run; intervene when a subagent goes off track or lacks context (F5-44). Communication is asynchronous rather than blocking, and one long-lived subagent is reused across related subtasks instead of a fresh one per subtask (F5-42, F5-43). For long commands, background execution and asynchronous checking rather than a blocking wait (F5-22).
- Scope and posture: under assess the deliverable is the assessment: report findings and stop, apply no fix until asked (F5-40, Step 1d). Before any state-changing command, check that the evidence supports that specific action, since a signal that pattern-matches a known failure may have another cause (F5-40, Standing rule 4). No unrequested extras: no drafted message nobody asked for, no defensive branch backups, no surrounding cleanup on a bug fix (F5-31, F5-39, Standing rule 7).
- Early stopping and the last-paragraph check: before ending a turn, check the last paragraph. A plan, an analysis, a question, a list of next steps, or a promise about undone work means doing that work now with tool calls; the turn ends only when the task is complete or the skill is blocked on input only the user can provide (F5-49, F5-52, Standing rule 9). A stated intent with no tool call is the failure this page names; if the user has to say "continue", that is the documented recovery and the prompt is not rewritten (F5-50, Standing rule 10).
- Context-count handling: ignore the harness's remaining-token countdown. Do not stop, summarize, hand off, trim the work, or propose a new session on account of context limits, and do not surface a token countdown to a subagent either (F5-53, F5-54, F5-55).
- Formatting: guide defaults. The Fable 5.1 `formatting_in_chat_rule` is not applied to the skill's own output, and neither is `mannered_prose_short`; the readability rules in F5-59 cover the final message. Step 5's display budget is kept.
- Edit style: Standing rule 11 applies as skill behaviour, targeted edits with a whole-file rewrite only for a short or mostly-changing file; the `targeted_edits` snippet text is measured on Fable 5.1 and is not grafted. Scratch files go in the scratchpad directory and are removed before the recap.
- Search behaviour: this page prints no search-triggering rule (that topic belongs to the Fable 5.1 page), so the guide's `investigate_before_answering` and Standing rule 6 govern: read every named file before claiming anything about it, back each claim with a read or search result, and resolve unknown tool parameters from a prior read. Code review and debugging may range across the codebase and repository history (F5-16).
- Memory: when a run produces a durable lesson, record it as one lesson per file with a one-line summary at the top, in the workspace's existing memory directory rather than a parallel store; update an existing note instead of duplicating it, do not save what the repo or the chat history already records, and delete a note that turns out to be wrong (F5-45, F5-46). Seeding memory from history is a subagent job (F5-48).
- Own reasoning: the skill does not echo, transcribe, or explain its internal reasoning in the reply. Step 5 shows the rearticulated prompt and the assumption lines; the Step 7 recap reports outcomes and evidence, not a reasoning narrative (F5-71, F5-72).
- Refusal handling: a refusal is a model-level outcome, not a prompt defect. Report it plainly, do not rephrase to evade it and do not rewrite a prompt to defeat a warranted refusal, and name Claude Opus 4.8 as the documented fallback the user can switch to; server-side and client-side fallback are harness settings the skill cannot set from inside a prompt (F5-10, F5-11, F5-20, BP-138).
- send_to_user: not available in Claude Code. Deliverables and anything the user must read verbatim go in the final message, and mid-turn text is not treated as guaranteed to arrive intact (F5-60, F5-61, F5-63).
- Effort follow-up: after a slow but correct run, suggest a lower effort for similar work; for capability-sensitive follow-ups suggest `xhigh`; for routine follow-ups `medium` or `low`, since lower effort here still performs well (F5-26 to F5-28, F5-30). Effort is a setting the user changes, not something the skill writes into a prompt (F5-25).
- Vision work: take the image as given and use bash or crop tools when it is flipped, blurry, or noisy, rather than reasoning around a bad image (F5-14).
- Harness-injected blocks to skip in-session: the Fable 5.1 defaults, `progress_updates_line` and `batch_nudge`, are not Fable 5 rules and are not grafted into prompts on this profile.

## Snippets

IDs only; verbatim text lives in `references/snippet-library.md`. All measured on Claude Fable 5 and Claude Mythos 5. Claude Fable 5.1 inherits these for topics its own page does not cover, recorded there as "text measured on the Fable 5 page" (F51-04).

- f5_give_reason (F5-57) - shape of `<context>`, slots filled from the request and the workspace.
- f5_act_when_ready (F5-24) - `<constraints>`, ambiguous or open-ended requests, and routine work at higher effort.
- f5_scope_discipline (F5-31) - `<constraints>`, coding tasks at `high` or `xhigh`; the Fable 5 form of scope control, in place of keep_changes_to_task and minimize_overengineering.
- f5_state_boundaries (F5-40) - `<constraints>`, diagnostic and question-shaped requests under the assess posture.
- f5_lead_with_outcome (F5-34) - `<output_format>`, default output-style block; also the skill's own final-message shape when executing here.
- f5_readability_addendum (F5-59) - `<output_format>`, tool-heavy and long unattended runs; grafted instead of f5_lead_with_outcome, not alongside it.
- f5_ground_progress (F5-38) - `<success_criteria>` or `<verification>`, any task where the model reports on tool work.
- f5_pause_only_when_needed (F5-36) - `<execution_guidance>`, multi-step and long-running work.
- f5_autonomous_reminder (F5-52) - `<execution_guidance>`, unattended or end-to-end runs; always paired with f5_pause_only_when_needed; the Fable 5 counterpart of the Fable 5.1 operating_autonomously.
- f5_delegate_subagents (F5-44) - `<execution_guidance>`, multi-part work with subagents available.
- f5_ample_context (F5-55) - `<execution_guidance>`, only when the harness shows the model a remaining-token countdown.
- f5_self_verification_interval (F5-69) - `<verification>`, long-running builds; `[X]` filled with a concrete interval.
- f5_memory_notes (F5-46) - `<constraints>`, prompts that maintain notes where no project convention fixes the format.
- f5_memory_bootstrap (F5-48) - body of `<task>` for a memory-seeding request; `[X]` filled with the memory path.
- send_to_user (F5-62) - harness-authoring deliverables only, never inside an ordinary rearticulated prompt.
- f5_send_to_user_elicitation (F5-65) - `<execution_guidance>`, only when the harness defines the send_to_user tool; paired with the definition.
- From the guide, applied here with no model exception: self_check_verify (BP-229, BP-230), use_parallel_tool_calls, investigate_before_answering, temp_file_cleanup, plain_text_math, no_preamble, quoting_sources_example, autonomy_safety_confirmation, general_purpose_solution, model_identity and model_string with the display name and string substituted (BP-082, BP-084).
- Not grafted on Fable 5: progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule, mannered_prose_short, long_output_budget_note (all measured on Fable 5.1; f5_* counterparts above); o5_* snippets (measured on Opus 5); s5_* and o48_* snippets (measured on Sonnet 5 and Opus 4.8), the one exception being frontend_aesthetics_short, which section 4 grafts for a frontend build with an Assumed entry because this page has no design section; the guide's long frontend_aesthetics (stated for Opus 4.5 and Opus 4.6, BP-330, and too prescriptive for this model, F5-19, F5-70); subagent_usage_policy and minimize_overengineering, whose damping intent conflicts with F5-41 and F5-42 and is covered by f5_delegate_subagents and f5_scope_discipline; context_compaction_persistence and spend_entire_context (measured on the Sonnet family; f5_ample_context is the counterpart here).

## Not covered by this page

The skill falls back to the main guide (`references/technique-catalog.md`) for: XML structure and tag order; role prompting; long-context ordering (BP-062); examples; positive format control and the list exception; plain-text math; prefill migration (BP-124); parallel tool calls; hallucination controls; research structure; file-creation hygiene; autonomy and safety confirmations; conversation-history and compaction handling; writing density and formatting in chat; quoting retrieved sources; targeted edits; long-output budgets; search triggering at low effort; frontend and design work; computer and browser use. Those last eight are Fable 5.1 page topics or guide topics, so their snippets keep their own measured-on models and are not attributed to Fable 5. The page prints no API model string, no context window size, no `max_tokens` figure, no tokenizer note, no sampling-parameter rule, no pricing, and no `max` effort level; cite the linked pages rather than asserting those.

Related pages (do not import their content; name them in the Target model item when a fact is needed):
- Introducing Claude Fable 5 and Claude Mythos 5, https://platform.claude.com/docs/en/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5 (capabilities, API changes, pricing, availability; adaptive thinking only, summarized-only thinking output, no extended thinking budgets, the refusal stop reason and fallback handling; F5-02, F5-08, BP-009).
- Prompting best practices, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (F5-03, BP-020, BP-364).
- Effort, https://platform.claude.com/docs/en/build-with-claude/effort (F5-23, F5-25).
- Thinking (adaptive thinking and its structured thinking blocks), https://platform.claude.com/docs/en/build-with-claude/thinking (F5-72).
- Refusals and fallback, https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback, and the refusal response section, https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#refusal-response (the `reasoning_extraction` category; F5-11, F5-20, F5-71).
- Prompting Claude Fable 5, sections Strong instruction following and Create a send-to-user tool (F5-51, F5-72, F5-73).
- Prompting Claude Fable 5.1 (`references/models/fable-5-1.md`), the profile that takes this one as its baseline (F51-04).
