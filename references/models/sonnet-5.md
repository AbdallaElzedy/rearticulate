# Claude Sonnet 5

Source page: Prompting Claude Sonnet 5, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 (snapshot 2026-09-08). The page's description names its scope: "effort, adaptive thinking defaults, tool use, and migration from Claude Sonnet 4.6" (S5-01). Guide rules that name Sonnet 5 come from Prompting best practices, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (snapshot 2026-09-08), and are listed at the end of section 3 with their BP IDs.

How to read this file. Everything on the page is measured on Claude Sonnet 5; a rule here is applied to another model only by analogy, and the Target model item of the assumptions says so. The cross-model technique catalog (`references/technique-catalog.md`) applies first; this file only adds or overrides, and never duplicates a cross-model rule (S5-03). Profile IDs `S5-nn` are the page's rules in page order. Sections 4 and 5 govern the content of a rearticulated prompt whose target model is Sonnet 5; section 6 governs the skill's own behaviour when Sonnet 5 is the model running the skill. The two dimensions are resolved separately in SKILL.md Step 1a.

## Identity and API facts

- Profile: `sonnet-5`. Aliases: sonnet-5, sonnet5, claude-sonnet-5. API string: `claude-sonnet-5` (alias table in `references/model-notes.md`; the page does not print the string).
- Covered set: inside the guide's thirteen current models (BP-002); the guide's model table row is BP-016.
- Baseline: none with its own page. Page basis: "It performs well out of the box on existing Claude Sonnet 4.6 prompts." (S5-04). The Sonnet 4.6 facts this page prints are the migration reference: effort default `high` on both (S5-11); requests without a `thinking` field ran without thinking on 4.6 and run with adaptive thinking on 5 (S5-24); `budget_tokens` was deprecated on 4.6 and is removed on 5 (S5-31); non-default `temperature`, `top_p`, `top_k` return 400 on 5, a constraint "new for Sonnet-class models" (S5-49), so 4.6 still accepts them; the effort mapping is one step down (S5-18). Sonnet 4.6 itself lives in `references/models/legacy-4x.md`. Texts this page shares verbatim with the Opus 4.8 page are one snippet-library entry with both IDs as aliases and "Measured on: Sonnet 5, Opus 4.8" (see section 7).
- Thinking: adaptive thinking on by default; a request without a `thinking` field runs with adaptive thinking (S5-23, S5-24, BP-218). Disable with `thinking: {type: "disabled"}` (S5-25); the page prints no effort cap on disabling (contrast Opus 5). With thinking disabled the model is less likely to reach for tools or consider searching (S5-36). Migrating a no-thinking 4.6 workload: try thinking on at lower effort instead (S5-27).
- `budget_tokens`: manual extended thinking (`thinking: {type: "enabled", budget_tokens: N}`) "is not supported on Claude Sonnet 5 and returns a 400 error" (S5-31, BP-189, BP-362). Replace with adaptive thinking plus the effort parameter.
- Sampling parameters: a non-default `temperature`, `top_p`, or `top_k` returns a 400; remove them and steer tone and variety through system-prompt instructions (S5-49). For design variety use the propose-directions step (S5-54).
- Context window: the page prints no size. Sonnet 5 has context awareness and can track its remaining token budget (BP-241), so long agentic prompts take the guide's context_compaction_persistence and spend_entire_context.
- Tokenizer: a new tokenizer produces approximately 30 percent more tokens for the same text; `max_tokens` limits tuned for Sonnet 4.6 may truncate; the exact increase depends on content and workload shape, so 30 percent is not presented as exact (S5-33, S5-34).
- Effort: default `high`, the same as Sonnet 4.6 (S5-11). Levels the page names: `max` (no constraint on token spend, S5-13), `xhigh` (recommended for the hardest coding and agentic work, S5-12, S5-14), `high` (default, balances token usage and intelligence, S5-15), `medium` (cost-sensitive, S5-16), `low` (short scoped latency-sensitive tasks, S5-17). Cross-model mapping: Sonnet 5 `medium` is comparable to Sonnet 4.6 `high`, and Sonnet 5 `high` to Sonnet 4.6 `max` (S5-18); benchmark by observed thinking length rather than effort name (S5-19). The model respects effort strictly, scoping work to the literal ask at `low` and `medium`, with some under-thinking risk at `low` on moderately complex tasks (S5-20). Shallow reasoning is fixed by raising effort, not by prompting around it (S5-21, S5-30). Effort is also a tool-usage lever: `high` or `xhigh` show substantially more tool usage (S5-37). An effort level is never carried from another profile; re-derive it here, and for a Sonnet 4.6 level apply the one-step-down mapping.
- `max_tokens` headroom: `max_tokens` is a hard limit on thinking plus response text (S5-26). At `high`, `xhigh`, or `max` leave headroom; a tight budget shows as a response that is almost entirely thinking followed by a truncated answer and `stop_reason: "max_tokens"`, fixed by raising `max_tokens` or dropping to `medium` (S5-32). Inherited 4.6 budgets are scaled up by about 30 percent (S5-33).
- Refusal and safeguard notes: not printed on this page; fall back to the guide.

### Harness and environment notes

These facts reach a rearticulated prompt only through the taxonomy rows for computer use, harness authoring, and prompt authoring for another model; in an interactive session the skill informs the user.

- Computer use: `computer_toolset_20260801` (Claude API and Google Cloud) and the earlier `computer_20251124` tool version (S5-71). Browser use: `browser_toolset_20260801` on the Claude API and Google Cloud, for tasks inside webpages (S5-72). Screenshot ceiling 2576px / 3.75MP (S5-74); 1080p is the tested balance of performance and cost (S5-75); 720p or 1366×768 for cost-sensitive workloads (S5-76); test resolution and effort on the actual workload (S5-77). Links: S5-73.
- Coding products: token usage and behaviour differ between single-turn autonomous agents and multi-turn interactive agents (S5-59); the page's recommendation is `xhigh` or `high` effort, an auto mode, and fewer required human interactions, with task, intent, and constraints specified in the first turn (S5-60, S5-61).
- Review harnesses: a recall drop on a harness tuned for an earlier model is a harness effect (S5-63); fix the reporting bar (section 4) and measure recall or F1 on a held-out subset (S5-70).

## Behavioural deltas

One entry per page rule, in page order, grouped by the page's section headings; the guide rules that name Sonnet 5 follow at the end. Sample prompts are quoted in part here and stored verbatim in `references/snippet-library.md` under the snippet ID given.

Page section: Prompting Claude Sonnet 5 (introduction)

### S5-01 Page provenance
- Kind: fact
- Rule: Cite this page by its URL and snapshot date whenever a Sonnet 5 rule is traced back to its source.
- Page says: "title: Prompting Claude Sonnet 5 / url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 / description: Behavioral differences and prompting patterns for Claude Sonnet 5, covering effort, adaptive thinking defaults, tool use, and migration from Claude Sonnet 4.6. / snapshot: 2026-09-08"
- Applies when: Writing this file's header or citing any rule below.
- Skill applies it by: The header carries the URL and date so each rule cites "Prompting Claude Sonnet 5 > <section>".

### S5-02 What's new page for capabilities and API changes
- Kind: link
- Rule: Point readers to the What's new page for Sonnet 5 capabilities and API changes rather than restating them.
- Page says: "For the model's capabilities and API changes, see [What's new in Claude Sonnet 5](https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5)."
- Applies when: The skill needs capability or API-change detail (tokenizer, parameters) beyond prompting patterns.
- Skill applies it by: Section 8 Related pages; no capability tables are copied into the skill.

### S5-03 Cross-model guide applies first
- Kind: link
- Rule: Apply the cross-model Prompting best practices guide first, then layer the Sonnet 5 specific patterns on top.
- Page says: "For techniques that apply across all current Claude models, see [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)."
- Applies when: Every rearticulation targeting Sonnet 5.
- Skill applies it by: The technique catalog is the base layer and this file is a delta file; cross-model rules are not duplicated here.

### S5-04 Strong on coding and agentic work; 4.6 prompts carry over
- Kind: model-note
- Rule: Expect Sonnet 5 to be strong on coding and agentic work and to run existing Sonnet 4.6 prompts well without rewrites, tuning only the behaviours this page lists.
- Page says: "Claude Sonnet 5 has particular strengths in coding and agentic tasks. It performs well out of the box on existing Claude Sonnet 4.6 prompts. The patterns in this guide cover the behaviors that most often require tuning."
- Applies when: Deciding how far to rewrite a request that already works on Sonnet 4.6.
- Skill applies it by: Does not restructure a prompt that already follows the guide; adds only the delta items from this page (effort, thinking triggering, literalism, progress updates, design defaults, code review bar) and records them in the Changed line. This sentence is the baseline basis in section 2.

### S5-05 Migration note: four API parameter changes
- Kind: migration
- Rule: When a request carries Sonnet 4.6 era API settings, apply the four migration changes: adaptive thinking on by default, sampling parameters not accepted, manual extended thinking removed, new tokenizer.
- Page says: "<Note> For API parameter changes when migrating from Claude Sonnet 4.6 (adaptive thinking on by default, sampling parameters not accepted, manual extended thinking removed, and the new tokenizer), see the [migration guide](https://platform.claude.com/docs/en/models/sonnet-5/migration-guide#migrating-from-claude-sonnet-4-6-to-claude-sonnet-5). </Note>"
- Applies when: The raw request mentions temperature, top_p, top_k, budget_tokens, thinking on or off, or max_tokens values tuned for Sonnet 4.6.
- Skill applies it by: Removes sampling parameters and budget_tokens from any API call the rewritten prompt describes, states that adaptive thinking is the default, scales max_tokens, and cites the migration guide in the Target model item (section 8 holds the link).

Page section: Response length and verbosity

### S5-06 Length tracks task complexity
- Kind: model-note
- Rule: Expect response length to track task complexity by default: short on simple lookups, long on open-ended analysis.
- Page says: "Claude Sonnet 5 calibrates response length to the complexity of the task rather than defaulting to a fixed verbosity. This usually means shorter answers on simple lookups and longer ones on open-ended analysis."
- Applies when: The request contains no explicit length requirement.
- Skill applies it by: Injects no default length instruction for Sonnet 5; adds length control only when the user or the deliverable demands a specific verbosity (BP-016 asks for the expectation to be stated when there is one).

### S5-07 Tune verbosity explicitly when the product depends on it
- Kind: technique
- Rule: When the output must have a fixed style or verbosity, add an explicit verbosity instruction rather than relying on the model's default calibration.
- Page says: "If your product depends on a certain style or verbosity of output, you may need to tune your prompts. As an example, to decrease verbosity, you might add:"
- Applies when: The user wants terse output, or the deliverable has a fixed format (ticket, summary line, table).
- Skill applies it by: Grafts s5_conciseness, or a positive example of the desired length, into `<output_format>` when brevity is a stated requirement.

### S5-08 Sample: s5_conciseness
- Kind: sample-prompt
- Rule: Use this snippet to decrease verbosity on Sonnet 5.
- Page says: see snippet s5_conciseness; the text is "Provide concise, focused responses. Skip non-essential context, and keep examples minimal."
- Applies when: The user asks for a short or concise answer, or a rewrite produces over-long output.
- Skill applies it by: Grafts verbatim into `<output_format>` when brevity is required; identical text to o48_conciseness (one library entry, both IDs as aliases).

### S5-09 Counter verbosity habits with positive examples
- Kind: technique
- Rule: Counter a specific verbosity habit such as over-explaining with positive examples of the desired concision rather than with instructions about what not to do.
- Page says: "If you see specific kinds of verbosity (such as over-explaining), you can add additional instructions in your prompt to prevent them. Positive examples showing how Claude can communicate with the appropriate level of concision tend to be more effective than negative examples or instructions that tell the model what not to do."
- Applies when: The raw request contains negative phrasing like "don't over-explain" or "no fluff".
- Skill applies it by: Section 5 conversion: rewrites negative verbosity instructions into a short positive example of the target answer shape in `<examples>` (guide: positive format control, BP-103).

Page section: Calibrating effort and thinking depth

### S5-10 Effort parameter link
- Kind: link
- Rule: Refer to the effort parameter documentation for the full mechanics of trading intelligence against token spend.
- Page says: "The [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) allows you to tune Claude's intelligence versus token spend, trading off capability for faster speed and lower costs."
- Applies when: Explaining effort or answering how to reduce cost or latency.
- Skill applies it by: Section 8 Related pages; section 2 describes effort as an intelligence versus token-spend dial.

### S5-11 Effort defaults to high
- Kind: fact
- Rule: Assume effort defaults to high on Sonnet 5, unchanged from Sonnet 4.6.
- Page says: "On Claude Sonnet 5, effort defaults to `high`, the same as on Claude Sonnet 4.6."
- Applies when: No effort level is specified by the user or harness.
- Skill applies it by: Treats `high` as the baseline; the Target model item mentions effort only when the task is hardest-tier or latency-bound.

### S5-12 Raise to xhigh for the hardest tasks
- Kind: technique
- Rule: Raise effort to xhigh for the hardest coding and agentic tasks, and experiment with other levels to tune token usage against intelligence.
- Page says: "For the hardest coding and agentic tasks, raise effort to `xhigh`. Experiment with other effort levels to further tune token usage and intelligence:"
- Applies when: A hard multi-file coding or long agentic task.
- Skill applies it by: The Target model item recommends `xhigh` for hardest coding and agentic requests; execution follows the harness effort setting.

### S5-13 max: no constraint on token spend
- Kind: fact
- Rule: Use max effort only when absolute maximum capability is wanted with no constraint on token spend.
- Page says: "* **`max`:** Absolute maximum capability with no constraints on token spending."
- Applies when: Cost is irrelevant and the task is the hardest tier.
- Skill applies it by: Section 2 documents `max`; the skill does not recommend it by default.

### S5-14 xhigh: recommended for hardest coding and agentic work
- Kind: fact
- Rule: Recommend xhigh as the setting for the hardest coding and agentic use cases.
- Page says: "* **`xhigh`:** Extra high effort is the recommended setting for the hardest coding and agentic use cases."
- Applies when: Hardest coding or agentic requests.
- Skill applies it by: Section 2; the Target model item may state `xhigh` as the suggested effort.

### S5-15 high: the default balance
- Kind: fact
- Rule: Treat high as the default that balances token usage and intelligence for most use cases.
- Page says: "* **`high`:** The default. This setting balances token usage and intelligence for most use cases."
- Applies when: Most requests.
- Skill applies it by: Section 2; no prompt change for typical requests.

### S5-16 medium: cost-sensitive
- Kind: fact
- Rule: Use medium for cost-sensitive use cases that accept reduced intelligence for fewer tokens.
- Page says: "* **`medium`:** Good for cost-sensitive use cases that need to reduce token usage while trading off intelligence."
- Applies when: The user prioritises cost over depth.
- Skill applies it by: Section 2; notes that Sonnet 5 `medium` roughly matches Sonnet 4.6 `high` (S5-18).

### S5-17 low: short, scoped, latency-sensitive only
- Kind: fact
- Rule: Reserve low effort for short, scoped, latency-sensitive tasks that are not intelligence-sensitive.
- Page says: "* **`low`:** Reserve for short, scoped tasks and latency-sensitive workloads that are not intelligence-sensitive."
- Applies when: Quick lookups or latency-bound pipelines.
- Skill applies it by: Section 2; when the user insists on `low` for a multistep task the rearticulation adds s5_low_effort_multistep (S5-22).

### S5-18 Cross-model effort mapping
- Kind: migration
- Rule: Map effort across models as Sonnet 5 medium roughly equal to Sonnet 4.6 high, and Sonnet 5 high roughly equal to Sonnet 4.6 max.
- Page says: "As a rough cross-model mapping when migrating: Claude Sonnet 5 at medium is comparable in intelligence to Claude Sonnet 4.6 at high, and Claude Sonnet 5 at high is comparable to Claude Sonnet 4.6 at max."
- Applies when: A request or harness carries an effort level chosen for Sonnet 4.6.
- Skill applies it by: Translates one step down (4.6 `high` to 5 `medium`, 4.6 `max` to 5 `high`) and says so in the Target model item. Effort names are never carried unchanged from another profile.

### S5-19 Benchmark by observed thinking length
- Kind: technique
- Rule: When benchmarking across models, match runs by observed thinking length rather than by effort level name.
- Page says: "When benchmarking, match by observed thinking length rather than effort name."
- Applies when: The user is comparing Sonnet 5 against another model.
- Skill applies it by: Benchmarking rearticulations add a `<success_criteria>` entry that comparisons are paired by observed thinking length, not effort label.

### S5-20 Strict effort adherence; literal scope at low and medium
- Kind: model-note
- Rule: Expect Sonnet 5 to honour effort strictly, scoping work to exactly what was asked at low and medium, with some under-thinking risk on moderately complex tasks at low.
- Page says: "Claude Sonnet 5 respects effort levels strictly, especially at the low end. At `low` and `medium`, the model scopes its work to what was asked rather than going above and beyond. This is good for latency and cost, but on moderately complex tasks running at `low` effort there is some risk of under-thinking."
- Applies when: Running Sonnet 5 at `low` or `medium`.
- Skill applies it by: At `low` or `medium` the `<task>` spells out every wanted sub-step and every "also check X" expectation, since the model will not go beyond the literal ask; the Target model item notes the under-thinking risk at `low`.

### S5-21 Raise effort for shallow reasoning
- Kind: technique
- Rule: Fix shallow reasoning on complex problems by raising effort to high or xhigh instead of prompting around it.
- Page says: "If you observe shallow reasoning on complex problems, raise effort to `high` or `xhigh` rather than prompting around it."
- Applies when: Output shows shallow reasoning on a complex task.
- Skill applies it by: The first remedy is the effort dial; the skill tells the user to raise effort rather than stacking "think harder" phrases (section 6 effort follow-up).

### S5-22 Sample: s5_low_effort_multistep
- Kind: sample-prompt
- Rule: When effort must stay at low for latency but the task needs multistep reasoning, add this targeted guidance.
- Page says: see snippet s5_low_effort_multistep; the text is "This task involves multistep reasoning. Think carefully through the problem before responding."
- Applies when: `low` is fixed by latency needs and the task is multistep.
- Skill applies it by: Grafts only when the user has pinned `low` on a multistep task; identical text to o48_low_effort_reasoning (one library entry, both IDs as aliases).

### S5-23 Adaptive thinking documentation link
- Kind: link
- Rule: Refer to the adaptive thinking documentation for how thinking is triggered and controlled.
- Page says: "On Claude Sonnet 5, [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) is on by default."
- Applies when: Documenting thinking behaviour.
- Skill applies it by: Section 8 Related pages.

### S5-24 Requests without a thinking field run with adaptive thinking
- Kind: fact
- Rule: Assume adaptive thinking is on by default on Sonnet 5; a request without a thinking field runs with adaptive thinking, unlike Sonnet 4.6 where it ran without thinking.
- Page says: "Requests without a `thinking` field run with adaptive thinking. This is a change from Claude Sonnet 4.6, where the same requests ran without thinking."
- Applies when: Any request, especially pipelines ported from Sonnet 4.6.
- Skill applies it by: Section 2 states the default; the rearticulation adds no "think step by step" boilerplate since thinking already runs adaptively (BP-218).

### S5-25 Disable syntax
- Kind: fact
- Rule: Turn thinking off entirely by passing thinking: {type: "disabled"}.
- Page says: "To turn thinking off entirely, pass `thinking: {type: \"disabled\"}`."
- Applies when: The user explicitly wants no thinking (latency or cost).
- Skill applies it by: Section 2 documents the exact parameter; a "disable thinking" request uses this form in the Target model item, paired with the tool-nudge rule (S5-36).

### S5-26 Revisit max_tokens for former no-thinking workloads
- Kind: migration
- Rule: Revisit max_tokens for workloads that ran without thinking on Sonnet 4.6, because max_tokens caps thinking plus response text together.
- Page says: "Because `max_tokens` is a hard limit on total output (thinking plus response text), revisit it for workloads that ran without thinking on Claude Sonnet 4.6."
- Applies when: A pipeline ported from Sonnet 4.6 with a tight `max_tokens`.
- Skill applies it by: Flags an inherited `max_tokens` from a no-thinking 4.6 setup for increase in the Target model item.

### S5-27 Prefer thinking on at lower effort over disabling
- Kind: migration
- Rule: If thinking was off on Sonnet 4.6, try thinking on with a lower effort level on Sonnet 5 rather than disabling it.
- Page says: "If you were previously using thinking off with Claude Sonnet 4.6, try thinking on with lower effort levels for Claude Sonnet 5."
- Applies when: Migrating a no-thinking Sonnet 4.6 workload.
- Skill applies it by: Replaces an inherited "thinking disabled" with "adaptive thinking at `low` or `medium` effort" in the Target model item and explains the trade.

### S5-28 Steer thinking triggering when it fires too often
- Kind: technique
- Rule: Steer adaptive thinking triggering with prompt guidance when the model emits thinking blocks too often, which can happen with large or complex system prompts, and measure the effect.
- Page says: "The triggering behavior for adaptive thinking is steerable. If you find the model emitting thinking blocks more often than you'd like, which can happen with large or complex system prompts, add guidance to steer it. As always, measure the effect of any prompting changes on performance. Example:"
- Applies when: Latency-sensitive use with a large system prompt and excess thinking.
- Skill applies it by: For latency-sensitive requests with thinking on, offers s5_thinking_trigger_guard and adds a note to measure quality after adding it.

### S5-29 Sample: s5_thinking_trigger_guard
- Kind: sample-prompt
- Rule: Use this snippet to reduce how often adaptive thinking triggers.
- Page says: see snippet s5_thinking_trigger_guard; the text is "Thinking adds latency and should only be used when it will meaningfully improve answer quality, typically for problems that require multistep reasoning. When in doubt, respond directly."
- Applies when: The model thinks more often than the use case warrants.
- Skill applies it by: Grafts in system-prompt position only when the user wants less thinking and latency is the stated concern. Differs by punctuation from o48_thinking_steer (em dash) and the guide's think_only_when_useful (hyphen); the three stay separate library entries, cross-referenced.

### S5-30 Under-thinking at medium: raise effort first
- Kind: technique
- Rule: For hard workloads at medium that under-think, raise effort first, and prompt directly for depth only when finer control is needed.
- Page says: "Conversely, if you're running hard workloads at `medium` and seeing under-thinking, the first lever is to raise effort. If you need finer control, prompt for it directly."
- Applies when: `medium` effort with visible under-thinking on hard tasks.
- Skill applies it by: Order of remedies: effort dial, then targeted prompt text; the skill recommends raising effort before grafting s5_low_effort_multistep.

### S5-31 Manual extended thinking returns 400
- Kind: migration
- Rule: Never send manual extended thinking (thinking: {type: "enabled", budget_tokens: N}) to Sonnet 5; it returns a 400 error, having been deprecated on Sonnet 4.6 and removed.
- Page says: "Manual extended thinking (`thinking: {type: \"enabled\", budget_tokens: N}`) is not supported on Claude Sonnet 5 and returns a 400 error. It was deprecated on Claude Sonnet 4.6 and is now removed. Use adaptive thinking with the effort parameter instead."
- Applies when: The raw request or code sets `budget_tokens`.
- Skill applies it by: Removes `budget_tokens` and `type: "enabled"` from any described call, replaces them with adaptive thinking plus an effort level, and warns about the 400 in the Target model item (BP-189, BP-362).

### S5-32 Leave max_tokens headroom at high and above
- Kind: technique
- Rule: At high, xhigh, or max effort, leave headroom in max_tokens for thinking and tool calls; if output is almost all thinking followed by a truncated answer with stop_reason max_tokens, raise max_tokens or drop to medium.
- Page says: "If you are running Claude Sonnet 5 at `high`, `xhigh`, or `max` effort, leave headroom in `max_tokens` so the model has room for thinking and tool calls. On long tasks, adaptive thinking can use a large share of the budget; if the budget is tight, you may see a response that is almost entirely thinking followed by a truncated answer and `stop_reason: \"max_tokens\"`. Raising `max_tokens` or dropping to `medium` effort resolves this."
- Applies when: Long tasks at `high` or above with a constrained `max_tokens`.
- Skill applies it by: Section 2 records the symptom and the two fixes; a long agentic rearticulation adds a Target model item note to leave `max_tokens` headroom.

### S5-33 New tokenizer: about 30 percent more tokens
- Kind: migration
- Rule: Expect roughly 30 percent more tokens for the same text under the Sonnet 5 tokenizer, so max_tokens limits tuned for Sonnet 4.6 may truncate equivalent output; the exact increase depends on content and workload shape.
- Page says: "Because Claude Sonnet 5 uses a [new tokenizer](https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5#new-tokenizer) that produces approximately 30% more tokens for the same text, `max_tokens` limits tuned for Claude Sonnet 4.6 may truncate equivalent output. The exact increase depends on the content and workload shape."
- Applies when: Any `max_tokens` or token budget inherited from Sonnet 4.6.
- Skill applies it by: Scales inherited budgets up by about 30 percent in the Target model item and cites the tokenizer; never presents 30 percent as exact.

### S5-34 New tokenizer link
- Kind: link
- Rule: Refer to the new tokenizer section of the What's new page for tokenizer details.
- Page says: "[new tokenizer](https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5#new-tokenizer)"
- Applies when: Explaining token count differences.
- Skill applies it by: Section 8 Related pages, next to the 30 percent figure.

Page section: Tool use triggering

### S5-35 More agentic by default; reaches for tools and self-verification
- Kind: model-note
- Rule: Expect Sonnet 5 to reach for tools and run self-verification loops more readily than Sonnet 4.6 by default.
- Page says: "Claude Sonnet 5 is more agentic than Claude Sonnet 4.6 by default and will reach for tools and run self-verification loops more readily."
- Applies when: Any agentic or tool-enabled request.
- Skill applies it by: Adds no "use your tools" nudges by default; adds scope limits in `<constraints>` where excess tool use or verification loops would be unwanted, and keeps `<verification>` concrete and bounded.

### S5-36 Explicit tool nudge when thinking is disabled
- Kind: technique
- Rule: When thinking is disabled and tool calls are required, add an explicit nudge in the system prompt because the model is less likely to reach for tools or consider searching.
- Page says: "With thinking disabled, the model is less likely to reach for tools or consider searching; if you rely on tool calls with thinking off, add an explicit nudge in the system prompt."
- Applies when: Thinking is disabled and the task depends on tool use or search.
- Skill applies it by: If the Target model item disables thinking, `<execution_guidance>` carries an explicit "use <tool> to <purpose>" instruction.

### S5-37 Effort as a tool-usage lever
- Kind: fact
- Rule: Use effort as a lever for tool usage: high or xhigh produce substantially more tool usage in agentic search and coding.
- Page says: "Effort is also a lever for tool usage: `high` or `xhigh` effort settings show substantially more tool usage in agentic search and coding."
- Applies when: The task needs thorough tool-driven exploration.
- Skill applies it by: The Target model item recommends `high` or `xhigh` for agentic search and coding when more tool use is wanted.

### S5-38 Instruct when and how to use each tool
- Kind: technique
- Rule: To increase tool use, instruct the model explicitly about when and how to use each tool, describing why and how, for example for a web search tool it is not using.
- Page says: "For scenarios where you want more tool use, you can also adjust your prompt to explicitly instruct the model about when and how to properly use its tools. For instance, if you find that the model is not using your web search tools, clearly describe why and how it should."
- Applies when: The model under-uses an available tool.
- Skill applies it by: Adds a tool-guidance block in `<execution_guidance>` naming each relevant tool, when to call it, and why (guide: explicit action verbs and targeted triggers, BP-145, BP-181).

Page section: User-facing progress updates

### S5-39 Regular, higher-quality updates without scaffolding
- Kind: model-note
- Rule: Expect regular, higher-quality user-facing updates during long agentic traces without scaffolding.
- Page says: "Claude Sonnet 5 provides regular, higher-quality updates to the user throughout long agentic traces."
- Applies when: Long agentic tasks.
- Skill applies it by: Adds no progress-cadence instruction for Sonnet 5 unless the user asks for a specific update format; the Fable 5.1 progress_updates_line is not grafted.

### S5-40 Remove forced status-message scaffolding
- Kind: anti-pattern
- Rule: Remove scaffolding that forces interim status messages, such as "After every 3 tool calls, summarize progress".
- Page says: "If you've added scaffolding to force interim status messages (\"After every 3 tool calls, summarize progress\"), try removing it."
- Applies when: The raw request or an inherited prompt contains a forced progress cadence.
- Skill applies it by: Section 5: deletes forced cadence lines and records the removal.

### S5-41 Describe and exemplify the update shape when miscalibrated
- Kind: technique
- Rule: If update length or content is miscalibrated, describe explicitly what updates should look like and provide examples.
- Page says: "If you find that the length or contents of Claude Sonnet 5's user-facing updates are not well-calibrated to your use case, explicitly describe what these updates should look like in the prompt and provide examples."
- Applies when: The user wants a particular update shape (one line, bullet, none).
- Skill applies it by: Adds a short description plus one example update in `<output_format>` or `<examples>`.

Page section: More literal instruction following

### S5-42 Literal, explicit interpretation
- Kind: model-note
- Rule: Expect literal, explicit interpretation, especially at lower effort: the model does not silently generalise an instruction from one item to another and does not infer unstated requests.
- Page says: "Claude Sonnet 5 interprets prompts literally and explicitly, particularly at lower effort levels. It does not silently generalize an instruction from one item to another, and it does not infer requests you didn't make."
- Applies when: Every rearticulation for Sonnet 5, most of all at `low` or `medium` effort.
- Skill applies it by: Makes every implied step explicit in `<task>`, enumerates the full target set for each instruction, and states expected side tasks (tests, docs) rather than relying on inference; no all-caps emphasis, since instruction following is literal (BP-016).

### S5-43 Literalism is precision for pipelines
- Kind: fact
- Rule: Lean on literalism for precision: Sonnet 5 generally performs better for API use cases with carefully tuned prompts, structured extraction, and pipelines needing predictable behaviour.
- Page says: "The upside of this literalism is precision, and it generally performs better for API use cases with carefully tuned prompts, structured extraction, and pipelines where you want predictable behavior."
- Applies when: Structured extraction, classification, or pipeline requests.
- Skill applies it by: The taxonomy marks extraction and pipeline rows as well suited to Sonnet 5; the rearticulation gives exact schemas and field-level instructions.

### S5-44 State scope explicitly
- Kind: technique
- Rule: State scope explicitly whenever an instruction should apply broadly rather than to the one item mentioned.
- Page says: "If you need Claude to apply an instruction broadly, state the scope explicitly (for example, \"Apply this formatting to every section, not just the first one\")."
- Applies when: Any instruction meant for all items, files, sections, or records.
- Skill applies it by: Appends an explicit scope clause ("every X, not just the first") to each instruction in `<task>`, `<constraints>`, and `<output_format>` that has to generalise.

### S5-45 Sample: s5_explicit_scope
- Kind: sample-prompt
- Rule: Use this phrasing pattern to make an instruction apply across all items.
- Page says: see snippet s5_explicit_scope; the text is "Apply this formatting to every section, not just the first one"
- Applies when: An instruction must generalise beyond the first instance.
- Skill applies it by: Adapts the noun ("section") to the user's target set when inserting; identical text to o48_explicit_scope (one library entry, both IDs as aliases).

Page section: Tone and writing style

### S5-46 Re-evaluate style prompts against the new baseline
- Kind: model-note
- Rule: Re-evaluate style prompts against the Sonnet 5 baseline because long-form prose style may have shifted.
- Page says: "As with any new model, prose style on long-form writing may shift. If your product relies on a specific voice, re-evaluate style prompts against the new baseline."
- Applies when: Long-form writing requests with a required voice.
- Skill applies it by: When voice matters, includes an explicit tone instruction and, where available, a short example passage in `<examples>` rather than relying on inherited style prompts.

### S5-47 Explicit tone instruction for a warmer voice
- Kind: technique
- Rule: For a warmer or more conversational voice, add an explicit tone instruction that names the tone and one concrete behaviour.
- Page says: "For instance, if your product voice is warmer or more conversational, add:"
- Applies when: The user wants a warm or conversational register.
- Skill applies it by: Grafts s5_warm_tone, or an adapted tone line, into the role or tone position of the rewritten prompt.

### S5-48 Sample: s5_warm_tone
- Kind: sample-prompt
- Rule: Use this snippet for a warm, collaborative voice.
- Page says: see snippet s5_warm_tone; the text is "Use a warm, collaborative tone. Acknowledge the user's framing before answering."
- Applies when: Warm or conversational output is requested.
- Skill applies it by: Grafts verbatim; identical text to o48_warm_tone (one library entry, both IDs as aliases).

### S5-49 Sampling parameters return 400
- Kind: migration
- Rule: Remove temperature, top_p, and top_k from Sonnet 5 requests, since any non-default value returns a 400 error (new for Sonnet-class models), and steer tone and variety through system-prompt instructions instead.
- Page says: "If you previously relied on `temperature` for stylistic variety, note that setting `temperature`, `top_p`, or `top_k` to a non-default value returns a 400 error on Claude Sonnet 5. This constraint is new for Sonnet-class models. Remove these parameters when migrating, and use system-prompt instructions to guide tone and variety instead."
- Applies when: The raw request mentions temperature, top_p, top_k, or "more randomness or variety".
- Skill applies it by: Deletes sampling parameters from any described call with the 400 reason in the Target model item and translates the intent into prompt text (a tone line, or s5_design_propose_directions for design variety). Sonnet 4.6 and pre-4.6 models keep them (the constraint is new for Sonnet-class models).

Page section: Design and frontend defaults

### S5-50 A default visual style on open-ended briefs
- Kind: model-note
- Rule: Expect a consistent default visual style on open-ended frontend briefs that may feel wrong for dashboards, dev tools, fintech, healthcare, or enterprise apps.
- Page says: "Claude Sonnet 5 may settle into a consistent default visual style on open-ended frontend and design briefs. A default house style can read well for some briefs but feel off for dashboards, dev tools, fintech, healthcare, or enterprise apps."
- Applies when: Open-ended UI, landing page, or design requests.
- Skill applies it by: The frontend row for Sonnet 5 adds either a concrete visual spec or the propose-options step rather than leaving the brief open. The page does not describe the palette of the house style; do not borrow the Opus 4.8 description.

### S5-51 Generic design instructions shift, not vary, the palette
- Kind: anti-pattern
- Rule: Do not rely on generic design instructions like "don't use that color" or "make it clean and minimal"; they shift the model to a different fixed palette instead of producing variety.
- Page says: "Generic instructions (\"don't use that color,\" \"make it clean and minimal\") tend to shift the model to a different fixed palette rather than producing variety. Two approaches work reliably:"
- Applies when: The raw design request contains vague or negative aesthetic instructions.
- Skill applies it by: Section 5 conversion: replaces vague or negative aesthetic phrases with a concrete spec (hex values, type, radius, spacing) or with the propose-four-directions step.

### S5-52 Specify a concrete alternative
- Kind: technique
- Rule: Specify a concrete visual alternative, because the model follows explicit specs precisely.
- Page says: "**1. Specify a concrete alternative.** The model follows explicit specs precisely:"
- Applies when: The user knows the look they want.
- Skill applies it by: Expands the user's direction into an explicit spec block (palette hexes, typography, radius, spacing, sections, motion) shaped like s5_design_concrete_spec_aefrm.

### S5-53 Sample: s5_design_concrete_spec_aefrm
- Kind: sample-prompt
- Rule: Use this full brief as the model for a concrete design specification.
- Page says: see snippet s5_design_concrete_spec_aefrm; opens "Design a desktop landing page for a supplement brand called AEFRM." and closes with the palette "#E9ECEC, #C9D2D4, #8C9A9E, #44545B, #11171B."
- Applies when: A frontend or design brief where the user can describe a direction.
- Skill applies it by: Mirrors its structure (atmosphere, feel, tonal system, imagery, layout and radius, typography, structure, motion, palette hexes) with the user's own values; the AEFRM content itself is not grafted. Identical text to o48_aefrm_concrete_spec (one library entry, both IDs as aliases); also the exemplar in `examples/rearticulations.md`.

### S5-54 Propose options before building
- Kind: technique
- Rule: Have the model propose several visual directions and let the user choose before building; this is the recommended way to get different design directions across runs since temperature is not accepted.
- Page says: "**2. Have the model propose options before building.** This breaks the default and gives users control. Because `temperature` is not accepted on Claude Sonnet 5, this approach is the recommended way to produce meaningfully different design directions across runs. Example prompt:"
- Applies when: Open-ended design briefs, or the user asked for variety or randomness.
- Skill applies it by: Prepends the s5_design_propose_directions step to `<task>` for open-ended design requests; it is also the conversion target for any "raise temperature for variety" request (S5-49).

### S5-55 Sample: s5_design_propose_directions
- Kind: sample-prompt
- Rule: Use this snippet to make the model propose four directions and implement only the chosen one.
- Page says: see snippet s5_design_propose_directions; the text is "Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the user to pick one, then implement only that direction."
- Applies when: Open-ended design briefs.
- Skill applies it by: In same-turn execution the skill presents the four options and the pick is a sanctioned turn-ending checkpoint (input only the user can provide); under an autonomous block the skill picks one direction, states it in the Target model item, and continues. Differs from o48_propose_directions by punctuation ("plus a one-line rationale" versus an em dash); the two stay separate library entries, cross-referenced.

### S5-56 Short anti-generic directive alongside the variety approaches
- Kind: technique
- Rule: Add a short system-prompt directive to steer away from generic "AI slop" aesthetics, alongside the variety approaches.
- Page says: "To steer away from generic patterns that users call the \"AI slop\" aesthetic, you can include a short directive in your system prompt. The [frontend-design skill](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md) provides a fuller treatment, but this snippet works well alongside the preceding variety approaches:"
- Applies when: Any frontend build request.
- Skill applies it by: Grafts frontend_aesthetics_short in the system-prompt position of frontend requests, together with a concrete spec or the propose-options step; in Claude Code, "Invoke frontend-design before <step>" replaces the paste when that skill is loaded (BP-342).

### S5-57 frontend-design skill link
- Kind: link
- Rule: Refer to the frontend-design skill for the fuller treatment of avoiding generic aesthetics.
- Page says: "The [frontend-design skill](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md) provides a fuller treatment"
- Applies when: Frontend or design requests needing more than the short directive.
- Skill applies it by: Section 8 Related pages; when executing in Claude Code the local frontend-design skill is invoked if installed.

### S5-58 Sample: frontend_aesthetics_short (alias frontend_aesthetics on this page)
- Kind: sample-prompt
- Rule: Use this XML block verbatim as the anti-generic aesthetics directive.
- Page says: see snippet frontend_aesthetics_short; the block opens "<frontend_aesthetics> NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds)..."
- Applies when: Frontend build requests.
- Skill applies it by: Grafts unchanged, wrapper tag and its all-caps NEVER included as quoted, in the system-prompt block of frontend rearticulations. The rule list names this block `frontend_aesthetics`; the library stores the guide's long block under that ID and this identical page block (also printed on the Opus 4.8 page) under `frontend_aesthetics_short`, with the page IDs as aliases and "Measured on: Sonnet 5, Opus 4.8".

Page section: Interactive coding products

### S5-59 Single-turn versus interactive coding agents differ
- Kind: model-note
- Rule: Expect token usage and behaviour to differ between autonomous single-turn coding agents and interactive multi-turn coding agents.
- Page says: "Token usage and behavior can differ between autonomous, asynchronous coding agents with a single user turn and interactive, synchronous coding agents with multiple user turns."
- Applies when: Designing or rearticulating coding-agent requests.
- Skill applies it by: The taxonomy distinguishes single-turn autonomous coding from interactive coding and applies the upfront-specification rule to both.

### S5-60 xhigh or high, auto mode, fewer interactions
- Kind: technique
- Rule: For coding products, use xhigh or high effort, add autonomous features such as an auto mode, and reduce the number of human interactions required.
- Page says: "To maximize both performance and token efficiency in coding products, use `xhigh` or `high` effort, add autonomous features like an auto mode, and reduce the number of human interactions required from your users."
- Applies when: Coding requests in agentic products.
- Skill applies it by: The Target model item recommends `high` or `xhigh` for coding, and `<task>` is written so the agent finishes without check-ins (explicit stop conditions, decisions pre-made).

### S5-61 Specify task, intent, and constraints in the first turn
- Kind: technique
- Rule: Specify the task, intent, and relevant constraints upfront in the first human turn to maximise autonomy and intelligence while minimising extra token usage.
- Page says: "When limiting the number of required user interactions, it's important to specify the task, intent, and relevant constraints upfront in the first human turn. Providing well-specified, clear, and accurate task descriptions upfront can help maximize autonomy and intelligence while minimizing extra token usage after user turns."
- Applies when: Every coding rearticulation.
- Skill applies it by: This is the core justification for the skill on Sonnet 5: `<task>`, `<context>` (intent and motivation), and `<constraints>` are front-loaded into one complete first-turn prompt (guide: clear and direct, context and motivation, success criteria).

### S5-62 Avoid drip-fed, underspecified prompts
- Kind: anti-pattern
- Rule: Avoid ambiguous or underspecified prompts delivered progressively over multiple turns; they reduce token efficiency and sometimes performance.
- Page says: "In contrast, ambiguous or underspecified prompts conveyed progressively over multiple user turns tend to relatively reduce token efficiency and sometimes performance."
- Applies when: The user tends to drip-feed requirements.
- Skill applies it by: Step 2 gathers all known requirements into the single rewritten prompt and asks any unavoidable question at the end of the first turn rather than leaving it for later turns.

Page section: Code review harnesses

### S5-63 Initial recall drop is a harness effect
- Kind: model-note
- Rule: Treat an initial recall drop on Sonnet 5 in a review harness tuned for an earlier model as a harness effect, not a capability regression.
- Page says: "If your code-review harness was tuned for an earlier model, you may initially see lower recall on Claude Sonnet 5. This is likely a harness effect, not a capability regression."
- Applies when: Code review requests or harness migrations.
- Skill applies it by: Adds no "be more thorough" text; fixes the reporting bar per S5-64 to S5-69 and states the diagnosis in the Target model item.

### S5-64 Conservative review instructions are followed faithfully
- Kind: model-note
- Rule: Expect Sonnet 5 to follow conservative review instructions ("only report high-severity issues", "be conservative", "don't nitpick") more faithfully: it investigates as deeply, finds the bugs, and then withholds findings below the stated bar.
- Page says: "When a review prompt says things like \"only report high-severity issues,\" \"be conservative,\" or \"don't nitpick,\" Claude Sonnet 5 may follow that instruction more faithfully than earlier models did: it may investigate the code just as thoroughly, identify the bugs, and then not report findings it judges to be below your stated bar. This can show up as the model doing the same depth of investigation but converting fewer investigations into reported findings, especially on lower-severity bugs."
- Applies when: Code review prompts containing severity or conservatism filters.
- Skill applies it by: Section 5: removes the filters and adds s5_code_review_coverage, or replaces them with the concrete bar (s5_code_review_concrete_bar).

### S5-65 Precision rises, measured recall can fall
- Kind: fact
- Rule: Expect precision to rise and measured recall to fall on filtered review prompts even though underlying bug-finding ability has improved.
- Page says: "Precision typically rises, but measured recall can fall even though the model's underlying bug-finding ability has improved."
- Applies when: Evaluating review output quality.
- Skill applies it by: Review `<success_criteria>` are framed around coverage plus downstream ranking, not around a low finding count.

### S5-66 Sample: s5_code_review_coverage
- Kind: sample-prompt
- Rule: Use this snippet to make the finding stage optimise for coverage with confidence and severity tags.
- Page says: see snippet s5_code_review_coverage; opens "Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that."
- Applies when: Code review or bug-finding requests.
- Skill applies it by: Grafts into the `<task>` of review prompts and adds confidence and severity fields to `<output_format>`; identical text to o48_review_coverage (one library entry, both IDs as aliases).

### S5-67 Say the finding stage is for coverage
- Kind: technique
- Rule: Use the coverage prompt even without a real second step, and when a verification, deduplication, or ranking stage exists, tell the model explicitly that the finding stage is for coverage rather than filtering.
- Page says: "This prompt can be used without having an actual second step, but moving confidence filtering out of the finding step often helps. If your harness has a separate verification, deduplication, or ranking stage, tell the model explicitly that its job at the finding stage is coverage rather than filtering."
- Applies when: Multi-stage review pipelines, or any review where recall matters.
- Skill applies it by: States the stage role ("your job here is coverage") in `<role>` or `<task>`; in same-turn execution the skill can run the verification pass itself after the coverage pass.

### S5-68 Define the self-filter bar concretely
- Kind: technique
- Rule: When the model must self-filter in one pass, define the bar concretely instead of using qualitative words like "important".
- Page says: "If you do want the model to self-filter in a single pass, be concrete about where the bar is rather than using qualitative terms like \"important\": for example, \"report any bugs that could cause incorrect behavior, a test failure, or a misleading result; only omit nits like pure style or naming preferences.\""
- Applies when: Single-pass review with a severity filter.
- Skill applies it by: Section 5: replaces "important", "significant", "high-severity only" with s5_code_review_concrete_bar or an equally concrete bar in `<constraints>`.

### S5-69 Sample: s5_code_review_concrete_bar
- Kind: sample-prompt
- Rule: Use this concrete severity bar for single-pass self-filtering reviews.
- Page says: see snippet s5_code_review_concrete_bar; the text is "report any bugs that could cause incorrect behavior, a test failure, or a misleading result; only omit nits like pure style or naming preferences."
- Applies when: Single-pass review where some filtering is wanted.
- Skill applies it by: Grafts into `<constraints>`; identical text to o48_review_concrete_bar (one library entry, both IDs as aliases).

### S5-70 Validate recall or F1 on a subset
- Kind: technique
- Rule: Iterate review prompts against a subset of evals or test cases to validate recall or F1 gains.
- Page says: "Iterate on prompts against a subset of your evals or test cases to validate recall or F1 score gains."
- Applies when: Tuning a review harness.
- Skill applies it by: Adds a `<success_criteria>` entry of measured recall or F1 on a held-out subset when the user is building a review harness.

Page section: Computer use

### S5-71 Computer use toolset versions
- Kind: fact
- Rule: Use computer_toolset_20260801 (Claude API and Google Cloud) or the earlier computer_20251124 tool version for computer use on Sonnet 5.
- Page says: "Claude Sonnet 5 supports the `computer_toolset_20260801` toolset (on the Claude API and Google Cloud) and the earlier `computer_20251124` tool version."
- Applies when: Computer-use agent requests targeting Sonnet 5.
- Skill applies it by: Section 2 (harness notes) records both strings; a rewritten computer-use setup names `computer_toolset_20260801` as the current toolset.

### S5-72 Browser use toolset
- Kind: fact
- Rule: Use the browser use tool browser_toolset_20260801 (Claude API and Google Cloud) for tasks inside webpages.
- Page says: "On the Claude API and Google Cloud, Claude Sonnet 5 also supports the [browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) (`browser_toolset_20260801`) for tasks inside webpages."
- Applies when: Web-page automation requests.
- Skill applies it by: Section 2 records the string and platform availability; section 8 lists the link.

### S5-73 Computer use tool documentation link
- Kind: link
- Rule: Refer to the computer use tool documentation for capability details.
- Page says: "[Computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) capability works across resolutions"
- Applies when: Computer-use requests.
- Skill applies it by: Section 8 Related pages.

### S5-74 Maximum screenshot resolution
- Kind: fact
- Rule: Keep screenshots within the maximum resolution of 2576px / 3.75MP; computer use works across resolutions up to that limit.
- Page says: "[Computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) capability works across resolutions, up to a maximum resolution of 2576px / 3.75MP."
- Applies when: Configuring screenshot size for computer-use agents.
- Skill applies it by: Section 2 records the ceiling; computer-use rearticulations state the screenshot resolution within it in `<constraints>`.

### S5-75 1080p as the default balance
- Kind: fact
- Rule: Default to 1080p screenshots for a good balance of computer-use performance and cost.
- Page says: "Internal computer use testing shows that sending images at 1080p provides a good balance of performance and cost."
- Applies when: Computer-use setup without special cost constraints.
- Skill applies it by: Recommends 1080p as the default screenshot resolution in `<execution_guidance>`.

### S5-76 720p or 1366×768 for cost-sensitive work
- Kind: fact
- Rule: For cost-sensitive computer-use workloads, use 720p or 1366×768, which are lower-cost options with strong performance.
- Page says: "For particularly cost-sensitive workloads, 720p or 1366×768 are lower-cost options with strong performance."
- Applies when: Cost-sensitive computer-use agents.
- Skill applies it by: Offers 720p or 1366×768 when the user prioritises cost.

### S5-77 Test resolution and effort on the workload
- Kind: technique
- Rule: Test resolution and effort settings on your own workload to find the ideal computer-use configuration.
- Page says: "Conduct your own testing to find the ideal settings for your use case; experimenting with effort settings can also help tune the model's behavior."
- Applies when: Any computer-use deployment.
- Skill applies it by: Adds a validation step (try resolutions and effort levels, measure) to `<verification>` of computer-use requests rather than fixing values without testing.

Guide rules naming Sonnet 5 (from Prompting best practices; catalog IDs, quoted from the guide)

### BP-002 Sonnet 5 is inside the guide's covered set
- Kind: fact
- Rule: Treat the guide as authoritative for exactly these thirteen current models and route any other model to the migration considerations.
- Guide says: "This is the reference for prompt engineering with current Claude models, including Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, and Claude Haiku 4.5."
- Applies when: Resolving whether guide techniques are measured on the target.
- Skill applies it by: Sonnet 5 needs no analogy note; the guide applies directly.

### BP-006 Further reading links for model facts
- Kind: fact
- Rule: Defer to the linked capability, what's-new, and migration pages rather than inventing model facts when a request needs them.
- Guide says: "For details on what's new in Claude Sonnet 5, see [What's new in Claude Sonnet 5](https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5). For migration guidance, see the [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide)."
- Applies when: A request turns on a capability claim the snapshots do not state.
- Skill applies it by: Names the page to check in the Target model item; links in section 8.

### BP-010 What's new in Claude Sonnet 5
- Kind: link
- Rule: Point to What's new in Claude Sonnet 5 for Sonnet 5 changes.
- Guide says: "For details on what's new in Claude Sonnet 5, see [What's new in Claude Sonnet 5](https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5)."
- Applies when: The user targets Sonnet 5 in a prompt-authoring request.
- Skill applies it by: Section 8 Related pages.

### BP-016 The guide's model table row for Sonnet 5
- Kind: model-note
- Rule: For Sonnet 5, set response length, effort and thinking depth, tool-use trigger conditions, literal instruction following, and design and frontend defaults explicitly.
- Guide says: "| Claude Sonnet 5 | [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5) | Differences from Claude Sonnet 4.6: response length, effort and thinking-depth calibration, tool use triggering, literal instruction following, and design and frontend defaults. |"
- Applies when: The user targets Sonnet 5.
- Skill applies it by: Section 4 states response-length expectations in `<output_format>` when there is one, uses targeted tool-trigger conditions instead of "default to X" phrasing, drops all-caps emphasis because instruction following is literal, and requests frontend richness explicitly.

### BP-021 Prompting Claude Sonnet 5 page link
- Kind: link
- Rule: Open the Prompting Claude Sonnet 5 page for Sonnet 5 specifics.
- Guide says: "[Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)"
- Applies when: The user targets Sonnet 5.
- Skill applies it by: This file is the local rendering of that page; the header cites it.

### BP-062 Data-first ordering has no model exception
- Kind: fact
- Rule: Apply data-first ordering for every model; there is no model exception.
- Guide says: "This improves performance across all models."
- Applies when: Any long-document rearticulation for Sonnet 5.
- Skill applies it by: `<documents>` precedes `<task>` on Sonnet 5 exactly as on every other model.

### BP-189 budget_tokens returns 400 on 4.7 and later
- Kind: fact
- Rule: Never emit budget_tokens for Claude 4.7 or later models; the API returns a 400 error.
- Guide says: "On Claude 4.7 and later models, setting `budget_tokens` returns a 400 error."
- Applies when: Any generated or migrated API configuration for Sonnet 5.
- Skill applies it by: Same conversion as S5-31: adaptive thinking plus `output_config.effort`, recorded in the Target model item.

### BP-218 Thinking on by default on Opus 5 and Sonnet 5
- Kind: model-note
- Rule: On Claude Opus 5 and Sonnet 5, thinking is on by default when the thinking parameter is omitted.
- Guide says: "On Claude Opus 5 and Claude Sonnet 5, thinking is on by default when you omit the `thinking` parameter."
- Applies when: Authoring a prompt or request for Sonnet 5.
- Skill applies it by: Adds no manual chain-of-thought scaffolding by default; consistent with S5-24.

### BP-241 Context awareness
- Kind: model-note
- Rule: Know that Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, and Claude Haiku 4.5 feature context awareness and can track their remaining token budget throughout a conversation.
- Guide says: "Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, and Claude Haiku 4.5 feature [context awareness](https://platform.claude.com/docs/en/build-with-claude/context-windows#context-awareness), enabling the model to track its remaining context window (that is, its \"token budget\") throughout a conversation."
- Applies when: Authoring a long agentic prompt for Sonnet 5, or reasoning about how Sonnet 5 behaves near the context limit as the executing model.
- Skill applies it by: Long agentic prompts for Sonnet 5 graft the guide's context_compaction_persistence and spend_entire_context so the model does not wrap up early; the agentic row's model overlay names Sonnet 5 as a taker of these snippets.

### BP-361 Migration guide from Sonnet 4.5 or earlier
- Kind: link
- Rule: Follow the Sonnet 5 migration guide when moving from Sonnet 4.5 or earlier.
- Guide says: "See [Migrating to Claude Sonnet 5 from Claude Sonnet 4.5 or earlier](https://platform.claude.com/docs/en/models/sonnet-5/migration-guide#migrating-from-sonnet-45) in the migration guide, which covers the effort default change and the removal of manual extended thinking (`budget_tokens`)."
- Applies when: The raw request targets Sonnet 5 with prompts or configs written for Sonnet 4.5 or earlier.
- Skill applies it by: Points to this guide in the Target model item when migrating a Sonnet prompt; section 8 holds the link. Sonnet 4.5 itself is outside the covered set's page coverage and lives in `references/models/legacy-4x.md`.

### BP-362 Effort default change and budget_tokens removal
- Kind: fact
- Rule: Account for the Sonnet 5 effort default change and the removal of manual extended thinking (budget_tokens).
- Guide says: "which covers the effort default change and the removal of manual extended thinking (`budget_tokens`)."
- Applies when: Prompts or API configs targeting Sonnet 5 that assume the old effort default or set budget_tokens.
- Skill applies it by: The strip-and-convert pass removes `budget_tokens` and states effort explicitly; from Sonnet 4.6 the default is unchanged at `high` (S5-11), so the "effort default change" applies to Sonnet 4.5 and earlier and is taken from the linked guide, not asserted here.

### BP-365 Next steps card for this page
- Kind: link
- Rule: Consult 'Prompting Claude Sonnet 5' for Sonnet 5 differences covering effort, adaptive thinking defaults, tool use, and migration from Sonnet 4.6.
- Guide says: "<Card title=\"Prompting Claude Sonnet 5\" icon=\"terminal\" href=\"https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5\"> Behavioral differences and prompting patterns for Claude Sonnet 5, covering effort, adaptive thinking defaults, tool use, and migration from Claude Sonnet 4.6. </Card>"
- Applies when: The target model is Sonnet 5.
- Skill applies it by: Cited as the source of this file; no prompt text change by itself.

## When this is the TARGET model: add to the rearticulated prompt

The content of the rearticulated prompt follows this section when the target is Sonnet 5. The Fable 5.1 default snippets (progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule) are not grafted. Instruction granularity on Sonnet 5 is enumerated: every item and its scope spelled out, most of all at `low` or `medium` effort (S5-20, S5-42, S5-44).

Target model item (SKILL.md Step 5 assumptions). Always `Target model: sonnet-5 (<how resolved>)`. When the target differs from the executing model, the request is prompt authoring, or the user asked about speed, cost, or thinking, append: recommended effort with the page section cited (default `high`, S5-11; `xhigh` for the hardest coding and agentic work, S5-12, S5-14; `high` or `xhigh` when more tool use is wanted, S5-37; `low` only for short scoped latency-bound tasks, S5-17; a Sonnet 4.6 level translated one step down, S5-18); adaptive thinking on by default, disable with `thinking: {type: "disabled"}` (S5-24, S5-25), with thinking on at lower effort preferred over disabling (S5-27); `budget_tokens` removed with the 400 reason (S5-31, BP-189); `temperature`, `top_p`, `top_k` removed with the 400 reason (S5-49); `max_tokens` headroom at `high` and above and the truncation symptom (S5-32); inherited budgets scaled by about 30 percent for the new tokenizer, not presented as exact (S5-33); model string `claude-sonnet-5` when API code is produced. For an in-session run with none of these triggers the line is `Target model: sonnet-5 (executing model)` and nothing else.

- `<role>`: one sentence per the guide. For a multi-stage review harness add the stage role: the finding stage's job is coverage, not filtering (S5-67).
- `<context>`: state the intent and motivation in the first turn (S5-61). For extraction and pipeline work say that predictable, literal behaviour is wanted (S5-43). When the Target model item disables thinking, say so here so the tool nudge in `<execution_guidance>` has its reason (S5-36). For long agentic work the guide's compaction context applies (BP-241).
- `<documents>`: guide rules unchanged (BP-062).
- `<task>`: every implied step written out; the full target set enumerated for each instruction (S5-42); each instruction that has to generalise carries an explicit scope clause shaped like s5_explicit_scope, "every X, not just the first" (S5-44, S5-45); at `low` or `medium` every wanted sub-step and "also check" expectation stated (S5-20). Coding: explicit stop conditions and pre-made decisions so the agent finishes without check-ins (S5-60); all known requirements gathered in one prompt (S5-62). Design: the s5_design_propose_directions step first for an open brief, or a concrete spec shaped like s5_design_concrete_spec_aefrm when the user has a direction (S5-52 to S5-55). Review: s5_code_review_coverage in the finding stage (S5-66). Benchmarking: pair runs by observed thinking length (S5-19). Computer use: a resolution-and-effort validation step (S5-77).
- `<constraints>`: scope limits where excess tool use or self-verification loops would be unwanted (S5-35); the concrete bar s5_code_review_concrete_bar for a single-pass self-filtering review (S5-68, S5-69); computer use: screenshot resolution within 2576px / 3.75MP (S5-74). Scope sentences use the enumerated form, not a principle-level sentence.
- `<output_format>`: no default length instruction (S5-06); s5_conciseness only when the user or the product fixes the verbosity (S5-07, S5-08); a stated response-length expectation when one exists (BP-016); when the user specifies an update style, a description plus one example update (S5-41); s5_warm_tone or an adapted tone line when a warm register is wanted (S5-47, S5-48); an explicit tone instruction when voice matters (S5-46); review output schema with confidence and severity fields (S5-66); exact schemas and field-level instructions for extraction (S5-43). For long-form prose the guide's avoid_excessive_markdown_and_bullet_points applies.
- `<examples>`: positive examples of the wanted concision in place of negative verbosity rules (S5-09); an example update line when the update shape is specified (S5-41); a short example passage when voice matters (S5-46).
- `<success_criteria>`: guide rules; review harness: measured recall or F1 on a held-out subset (S5-70) and coverage before ranking (S5-65); benchmarking: pairing by observed thinking length (S5-19); computer use: resolution and effort tested on the workload (S5-77); extraction: exact schema conformance (S5-43).
- `<execution_guidance>`: no progress-cadence scaffolding (S5-39, S5-40); a description plus example only when the user wants a specific update shape (S5-41). An explicit "use <tool> to <purpose>" nudge when thinking is disabled (S5-36); a tool-guidance block naming each tool, when to call it, and why, when a tool is under-used (S5-38); no "use your tools" nudge otherwise (S5-35). s5_low_effort_multistep only when the user has pinned `low` on a multistep task (S5-17, S5-22); s5_thinking_trigger_guard only when latency is the stated concern and thinking is on (S5-28, S5-29). For long agentic work context_compaction_persistence and spend_entire_context (BP-241). frontend_aesthetics_short in system-prompt position for frontend builds, paired with a spec or the propose step (S5-56, S5-58), or "Invoke frontend-design before <step>" when that skill is loaded (S5-57). The guide's use_parallel_tool_calls, investigate_before_answering, and temp_file_cleanup apply as the taxonomy row requires; batch_nudge is not grafted.
- `<verification>`: filled per the guide with self_check_verify and concrete checks; Sonnet 5 has no exception. Keep the checks bounded to `<success_criteria>` because the model runs self-verification loops readily (S5-35). Review harness: the recall or F1 measurement step (S5-70). Computer use: the resolution and effort sweep (S5-77).
- Closing lines: none specific to Sonnet 5.

Reasoning exhortations: hand-written reasoning plans are dropped and effort is recommended in the Target model item (S5-21, S5-30); no "think step by step" boilerplate (S5-24); s5_low_effort_multistep only when `low` is pinned; the trigger guard only when latency is the stated concern and thinking is on.

## When this is the TARGET model: remove or convert

Each conversion is recorded in the Changed line of the assumptions.

| Found in the raw request or pasted prompt | Action for a Sonnet 5 target | Basis |
|---|---|---|
| `temperature`, `top_p`, `top_k` at non-default values | Remove with the 400 reason; translate the intent into prompt text (a tone line, or s5_design_propose_directions for variety) | S5-49, S5-54 |
| `thinking: {type: "enabled", budget_tokens: N}` | Remove; adaptive thinking plus an effort level; warn about the 400 | S5-31, BP-189, BP-362 |
| "thinking disabled" inherited from a Sonnet 4.6 setup | Thinking on at `low` or `medium`, with the trade explained | S5-27 |
| An effort level chosen for Sonnet 4.6 | One step down (4.6 `high` to 5 `medium`, 4.6 `max` to 5 `high`) | S5-18 |
| A `max_tokens` value tuned for Sonnet 4.6 | Scale up by about 30 percent and leave headroom at `high` and above; flag a former no-thinking budget for increase | S5-26, S5-32, S5-33 |
| "After every 3 tool calls, summarize progress" and other forced cadences | Remove | S5-40 |
| "only report high-severity issues", "be conservative", "don't nitpick" in a review prompt | Remove and add s5_code_review_coverage, or replace with s5_code_review_concrete_bar | S5-64, S5-66, S5-68 |
| "important", "significant" as a review bar | The concrete bar | S5-68, S5-69 |
| "be more thorough" added to recover review recall | Remove; fix the reporting bar instead | S5-63 |
| "don't over-explain", "no fluff", "don't ramble" | A short positive example of the target answer shape | S5-09 |
| "think step by step" boilerplate | Remove; adaptive thinking already runs | S5-24 |
| Stacked "think harder" phrases for shallow reasoning | Remove; recommend raising effort to `high` or `xhigh` | S5-21, S5-30 |
| Hand-written reasoning plans | Drop; recommend effort; numbered work steps whose order matters stay | S5-21, BP-221 |
| "don't use that color", "make it clean and minimal" | A concrete spec (hex values, type, radius, spacing) or the propose-four-directions step | S5-51, S5-52, S5-54 |
| "raise temperature for variety" in a design brief | s5_design_propose_directions | S5-49, S5-54 |
| "use your tools", "always search first" nudges | Remove unless thinking is disabled or a named tool is under-used; then a targeted "use <tool> to <purpose>" instruction | S5-35, S5-36, S5-38 |
| A single-item instruction with implied breadth | Add the explicit scope clause "every X, not just the first" | S5-44, S5-45 |
| Requirements spread over several turns | Gather them into the one first-turn prompt; ask any unavoidable question at the end of that turn | S5-61, S5-62 |
| All-caps emphasis, "CRITICAL: you MUST" | Plain conditional wording; instruction following is literal | BP-016, BP-162 |
| A default length instruction inherited from another model | Remove unless the deliverable fixes the verbosity | S5-06, S5-07 |
| Fable 5.1 default snippets (progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule) in a ported prompt | Remove; measured on Fable 5.1 | S5-39, section 4 |
| A Sonnet 4.6-era prompt as a whole | Keep its substance; apply only the deltas in this table and section 4 | S5-04 |

## When this is the EXECUTING model: how the skill behaves in Steps 5-7

Applies when the model running the skill resolves to Sonnet 5 (the Target model item then reads "executing model: sonnet-5"). SKILL.md Steps 6 and 7 are written for Fable 5.1; where this page differs, this section governs the skill's own behaviour. The rearticulated prompt's content still follows the target profile.

- Narration cadence: an opening line, then natural updates during long traces; no per-batch update rule (S5-39). The Fable 5.1 "one-line update before each tool batch" sentence in Step 6 does not apply.
- Final message shape: the Step 7 recap of three to eight lines, fact-based (BP-089); response length tracks task complexity, so the recap is short for a lookup and longer for an analysis (S5-06). The Step 5 display budget is kept.
- Verification loop: Step 7 runs as written; Sonnet 5 has no exception. The model reaches for self-verification readily (S5-35), so the checks are the ones named in `<verification>` and no more.
- Literal reading: read the request literally, state assumptions rather than widen scope, and do not infer unrequested work; at `low` or `medium` effort the skill says when a sub-step was not asked for instead of doing it (S5-20, S5-42). This matches Step 1d and Standing rule 7.
- Subagent policy: the page is silent; the guide's subagent_usage_policy applies. Small work is finished with direct tool calls.
- Formatting: guide defaults; formatting_in_chat_rule is not applied to the skill's own output.
- Edit style: Standing rule 11 applies as skill behaviour; the targeted_edits snippet text is measured on Fable 5.1 and is not grafted.
- Search-before-answer: the model reaches for tools readily with thinking on (S5-35); if the session runs with thinking disabled, the skill deliberately searches and reads before answering, because the model is then less likely to (S5-36). Standing rule 6 applies.
- Progress grounding: fact-based, no self-evaluation (BP-089); the page adds nothing.
- Last-paragraph check: Step 7 as written; the page is silent.
- Refusal handling: the page is silent; guide default (report plainly, do not rephrase to evade).
- Context-count handling: Sonnet 5 is context-aware (BP-241); do not wrap up early because the remaining budget looks small; continue until the task is done or the window is genuinely exhausted.
- Effort follow-up: if reasoning was shallow on a complex task, tell the user to raise effort to `high` or `xhigh` rather than re-prompting with "think harder" (S5-21, S5-30); for the hardest coding suggest `xhigh` (S5-12); if a long run truncated with `stop_reason: "max_tokens"`, suggest more headroom or `medium` (S5-32).
- Design work in-session: the propose-four-directions pick is a sanctioned turn-ending checkpoint; under an autonomous block the skill picks one direction, states it in the Target model item, and continues (S5-55).
- Tone: the page says prose style may shift (S5-46); the skill's own voice follows Standing rule 12 (factual, no self-evaluation).
- Harness-injected blocks to skip in-session: none named on the page; the Fable 5.1 batch_nudge is not a default here.

## Snippets

IDs only; verbatim text lives in `references/snippet-library.md`. All measured on Claude Sonnet 5; texts shared verbatim with the Opus 4.8 page are one library entry with both IDs as aliases and "Measured on: Sonnet 5, Opus 4.8".

- s5_conciseness (S5-08; alias o48_conciseness) - `<output_format>`, only when verbosity is fixed by the user or product.
- s5_low_effort_multistep (S5-22; alias o48_low_effort_reasoning) - `<execution_guidance>`, only when `low` is pinned on a multistep task.
- s5_thinking_trigger_guard (S5-29) - system-prompt position, only when latency is the stated concern and thinking is on; separate entry from o48_thinking_steer (em dash) and the guide's think_only_when_useful (hyphen), cross-referenced.
- s5_explicit_scope (S5-45; alias o48_explicit_scope) - a pattern adapted to the user's target set, in `<task>`, `<constraints>`, or `<output_format>`.
- s5_warm_tone (S5-48; alias o48_warm_tone) - role or tone position, only when warmth is requested.
- s5_design_concrete_spec_aefrm (S5-53; alias o48_aefrm_concrete_spec) - a template shape mirrored with the user's values; the AEFRM content is not grafted.
- s5_design_propose_directions (S5-55) - first step of `<task>` for open design briefs; separate entry from o48_propose_directions (em dash), cross-referenced.
- frontend_aesthetics_short (S5-58; aliases: the rule list's `frontend_aesthetics` for this page and for the Opus 4.8 page) - system-prompt position for frontend builds; the guide's long block stays under `frontend_aesthetics`.
- s5_code_review_coverage (S5-66; alias o48_review_coverage) - `<task>` of review prompts, with confidence and severity fields in `<output_format>`.
- s5_code_review_concrete_bar (S5-69; alias o48_review_concrete_bar) - `<constraints>` of single-pass self-filtering reviews.
- From the guide, measured on the Sonnet family: context_compaction_persistence, spend_entire_context (BP-241) - `<execution_guidance>` for long agentic work.
- Not grafted on Sonnet 5: progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule (measured on Fable 5.1); the guide's long frontend_aesthetics (the page prints the short block); o5_* snippets (measured on Opus 5).

## Not covered by this page

The skill falls back to the main guide (`references/technique-catalog.md`) for: XML structure and tag order; role prompting; long-context ordering (BP-062); examples; positive format control and the list exception; plain-text math; prefill migration; parallel tool calls; hallucination controls; state tracking across context windows (the page names no context window size; context awareness is the guide's fact, BP-241); autonomy and safety confirmations; subagent orchestration (the page is silent on subagents); research structure; file-creation hygiene; the self-check verification instruction (no exception on Sonnet 5). The page prints no API string, no context window size, no refusal or safeguard behaviour, no house-style palette description (do not borrow the Opus 4.8 one), and no subagent guidance; cite the linked pages rather than asserting those.

Related pages (do not import their content; name them in the Target model item when a fact is needed):
- What's new in Claude Sonnet 5, https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5 (capabilities and API changes; S5-02, BP-010, BP-006); new tokenizer section, https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5#new-tokenizer (S5-34).
- Migration guide, Sonnet 4.6 to Sonnet 5, https://platform.claude.com/docs/en/models/sonnet-5/migration-guide#migrating-from-claude-sonnet-4-6-to-claude-sonnet-5 (S5-05); from Sonnet 4.5 or earlier, https://platform.claude.com/docs/en/models/sonnet-5/migration-guide#migrating-from-sonnet-45 (BP-361, BP-362).
- Effort, https://platform.claude.com/docs/en/build-with-claude/effort (S5-10).
- Adaptive thinking, https://platform.claude.com/docs/en/build-with-claude/thinking (S5-23).
- Context awareness, https://platform.claude.com/docs/en/build-with-claude/context-windows#context-awareness (BP-241).
- frontend-design skill, https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md (S5-57).
- Browser use tool, https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool (S5-72); Computer use tool, https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool (S5-73).
- Prompting Claude Opus 4.8 (`references/models/opus-4-8.md`) for the shared snippet texts; Sonnet 4.6 in `references/models/legacy-4x.md`.
