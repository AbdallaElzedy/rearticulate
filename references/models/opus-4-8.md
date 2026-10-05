# Claude Opus 4.8

Source page: Prompting Claude Opus 4.8, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8 (snapshot 2026-09-08). The page's front matter names its scope: "Behavioral differences and prompting patterns for Claude Opus 4.8, covering verbosity, effort calibration, tool use, subagents, and frontend defaults." Guide rules that name Opus 4.8 or its generation come from Prompting best practices, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (snapshot 2026-09-08), and are listed at the end of section 3 with their BP IDs.

How to read this file. Everything on the page is measured on Claude Opus 4.8; a rule here is applied to another model only by analogy, and the Target model item of the assumptions says so (BP-025). The cross-model technique catalog (`references/technique-catalog.md`) applies first; this file only adds or overrides, and never duplicates a cross-model rule (O48-02). Profile IDs `O48-nn` are the page's rules in page order. Sections 4 and 5 govern the content of a rearticulated prompt whose target model is Opus 4.8; section 6 governs the skill's own behaviour when Opus 4.8 is the model running the skill. The two dimensions are resolved separately in SKILL.md Step 1a.

Relation to the Sonnet 5 profile. The two pages share most of their section shape and several snippet texts word for word, so `references/models/sonnet-5.md` is the sibling to read alongside this one. What is genuinely different on Opus 4.8, and must never be copied across: thinking is off unless the caller sets it (O48-23), effort starts at `xhigh` for coding and agentic work with `high` as the floor for intelligence-sensitive work and no printed default (O48-13), a 64k starting max output budget at `xhigh` or `max` (O48-28), reasoning is favoured over tool calls (O48-29), fewer subagents are spawned by default so the subagent snippet encourages delegation (O48-43 to O48-45), the house visual style is described concretely (O48-46), and less frontend prompting is needed than for earlier models (O48-55).

## Identity and API facts

- Profile: `opus-4-8`. Aliases: opus-4.8, opus48, opus-4-8, claude-opus-4-8. API string: `claude-opus-4-8`, the model the guide's adaptive-thinking migration example targets (BP-213), with `max_tokens` pinned in the same example (BP-212).
- Covered set: inside the guide's thirteen current models (BP-002); the guide's model table row is BP-018 and its page link is BP-023.
- Baseline: `opus-4-7`, which has no page of its own and lives in `references/models/legacy-4x.md`. Page basis: "It performs well out of the box on existing Claude Opus 4.7 prompts." (O48-04). A working Opus 4.7 prompt is therefore kept and only the eleven delta topics of this page are applied: verbosity, effort and thinking depth, tool triggering, progress updates, literalism, tone, subagents, design and frontend, interactive coding, code review, computer use. Opus 4.8 is in turn the baseline of `opus-5` ("It performs well out of the box on existing Claude Opus 4.8 prompts.", O5-05), so Opus 5 borrows this page's review-coverage, frontend, literalism, and effort-sweep texts and records them as measured here.
- Documented strengths: "long-horizon agentic work, knowledge work, vision, and memory tasks" (O48-03). A long agentic, vision, or memory request can lean on the model's autonomy instead of heavy step-by-step scaffolding.
- Thinking: off unless the caller explicitly sets `thinking: {type: "adaptive"}` (O48-23, BP-217). This is the sharpest difference from Opus 5 and Sonnet 5, where thinking is on when the parameter is omitted (BP-218). Adaptive triggering is steerable: large or complex system prompts make it fire more often, and o48_thinking_steer damps it (O48-24, O48-26); measure quality after adding it. Mechanics: adaptive thinking, https://platform.claude.com/docs/en/build-with-claude/thinking (O48-25). When a caller keeps thinking off and the task needs reasoning, the guide's manual chain-of-thought fallback applies (BP-225).
- `budget_tokens`: not accepted; the guide states a 400 error on Claude 4.7 and later (BP-189). Convert to adaptive thinking plus `output_config.effort`, leaving messages and `max_tokens` unchanged (BP-208 to BP-212).
- Sampling parameters (`temperature`, `top_p`, `top_k`): not printed on this page. The page's Note routes five areas to the Opus 4.7 to Opus 5 migration guide and says Opus 4.8 shares those behaviours: sampling parameters, effort default, 1M context window default, mid-conversation system messages, and refusal stop details (O48-05, O48-06). The skill flags any sampling assumption in a raw request as "check against the Opus 4.7 to Opus 5 migration guide" rather than asserting a value. For design variety the sanctioned replacement is o48_propose_directions, not a temperature setting (O48-53).
- Context window: 1M as the default, among the shared Opus 4.7 migration behaviours; the page prints no number of its own, so cite the migration guide (O48-05).
- Tokenizer: not printed. Do not apply the Sonnet 5 scaling figure here.
- Effort: no default is printed on this page; the effort default is one of the areas routed to the migration guide (O48-05). Starting points the page does print: `xhigh` for coding and agentic use cases, and a minimum of `high` for most intelligence-sensitive use cases (O48-13). Levels named: `max` (gains in some use cases, diminishing returns from token usage, sometimes prone to overthinking, test it on intelligence-demanding tasks, O48-14), `xhigh` (best for most coding and agentic use cases, O48-15), `high` (balances token usage and intelligence, the floor for intelligence-sensitive work, O48-16), `medium` (cost-sensitive, O48-17), `low` (short scoped latency-sensitive work that is not intelligence-sensitive, O48-18). Effort is respected strictly: at `low` and `medium` the model scopes work to what was asked rather than going above and beyond, with under-thinking risk at `low` on moderately complex tasks (O48-19). Shallow reasoning is fixed by raising effort, not by prompting around it (O48-20, O48-27). Effort is also the tool-usage lever (O48-30) and shapes computer-use behaviour (O48-79). "Effort is likely to be more important for this model than for any prior Opus, so experiment with it actively when you upgrade." (O48-22), which makes an effort sweep part of any migration onto Opus 4.8. Reference: effort, https://platform.claude.com/docs/en/build-with-claude/effort (O48-12). An effort level is never carried from another profile; re-derive it here (model-notes section 7).
- `max_tokens` headroom: at `max` or `xhigh` effort, "set a large max output token budget so the model has room to think and act across its subagents and tool calls. Start at 64k tokens and tune from there." (O48-28). Whenever the skill recommends `xhigh` or `max` for this target, the 64k starting budget goes in the Target model item or `<execution_guidance>`.
- Refusal and safeguard behaviour: not printed on this page; refusal stop details are among the areas routed to the migration guide (O48-05). Cross-model role: the Fable 5 page names Claude Opus 4.8 as the documented fallback for declined Fable 5 requests, configured as server-side or client-side fallback (F5-10, F5-11), and the guide's model table describes the Fable 5 page as "Differences from Claude Opus 4.8" (BP-015). Neither fact says anything about Opus 4.8's own refusal behaviour.
- Prefill: last-turn prefilled assistant responses are unsupported from Claude 4.6 onward, so not on Opus 4.8 (BP-124).

### Harness and environment notes

These facts reach a rearticulated prompt only through the taxonomy rows for computer use, harness authoring, and prompt authoring for another model; in an interactive session the skill informs the user rather than trying to set them from inside a prompt.

- Computer use: `computer_toolset_20260801` (Claude API and Google Cloud) and the earlier `computer_20251124` tool version (O48-72). Browser use: `browser_toolset_20260801` on the Claude API and Google Cloud, for tasks inside webpages (O48-73). Screenshot ceiling 2576px / 3.75MP (O48-76); 1080p is the tested balance of performance and cost (O48-77); 720p or 1366x768 for cost-sensitive workloads (O48-78); test resolution and effort on the actual workload (O48-79). Links: O48-74, O48-75.
- Coding products: token usage is higher in interactive multi-turn sessions than in single-turn autonomous agents because the model reasons more after user turns (O48-58). The page's recommendation is `xhigh` or `high` effort, autonomous features such as an auto mode, fewer required human interactions, and task, intent, and constraints specified upfront in the first turn (O48-59, O48-60); the model is more autonomous than prior models, so a complete upfront specification pays off (O48-61).
- Review harnesses: bug finding is meaningfully better with higher recall and precision in internal evals (O48-63); an initial recall drop on a harness tuned for an earlier model is a harness effect, not a capability regression (O48-64); fix the reporting bar (section 4) and measure recall or F1 on a held-out subset before rollout (O48-71).
- Design defaults appear in slide decks as well as web UIs (O48-48), so the design overrides in section 4 apply to presentation requests too.

## Behavioural deltas

One entry per page rule, in page order, grouped by the page's section headings; the guide rules that name Opus 4.8 or its generation follow at the end. Sample prompts are quoted in part here and stored verbatim in `references/snippet-library.md` under the snippet ID given.

Page section: Prompting Claude Opus 4.8 (introduction)

### O48-01 Opus 4.8 to Opus 5 migration link
- Kind: link
- Rule: Consult the Opus 4.8 to Opus 5 migration guide for the API changes involved in moving off Opus 4.8.
- Page says: "For the API changes involved in moving from Claude Opus 4.8 to the latest Opus model, see [Migrating to Claude Opus 5 from Claude Opus 4.8](https://platform.claude.com/docs/en/models/opus-5/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5)."
- Applies when: The user moves a prompt or application from Opus 4.8 to Opus 5, or asks about API differences between the two.
- Skill applies it by: Section 8 Related pages, and the same row in `references/model-notes.md`. When the target switches from opus-4-8 to opus-5 the Target model item cites this link instead of guessing API deltas.

### O48-02 Cross-model guide applies first
- Kind: link
- Rule: Apply the cross-model Prompting best practices guide first, then layer this page's deltas on top.
- Page says: "For techniques that apply across all current Claude models, see [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)."
- Applies when: Every rearticulation targeting Opus 4.8; this page only overrides or adds.
- Skill applies it by: The technique catalog is the base layer and this file is a delta file. No main-guide tag is dropped because the target is Opus 4.8.

### O48-03 Documented strengths
- Kind: fact
- Rule: Treat long-horizon agentic work, knowledge work, vision, and memory tasks as the model's documented strengths.
- Page says: "Claude Opus 4.8 has particular strengths in long-horizon agentic work, knowledge work, vision, and memory tasks."
- Applies when: Choosing or justifying Opus 4.8 as the target, or deciding how much scaffolding a long agentic prompt needs.
- Skill applies it by: Section 2 records the strengths; a long agentic, vision, or memory request leans on the model's autonomy in `<task>` instead of a prescribed step-by-step plan (BP-221).

### O48-04 Opus 4.7 prompts carry over
- Kind: model-note
- Rule: Reuse existing Opus 4.7 prompts as the starting point and tune only the behaviours this page lists.
- Page says: "It performs well out of the box on existing Claude Opus 4.7 prompts. The following patterns cover the behaviors that most often require tuning."
- Applies when: The user has a working Opus 4.7 prompt and names opus-4-8 as the target.
- Skill applies it by: Does not rewrite a supplied Opus 4.7 prompt wholesale; applies only this page's deltas (verbosity, effort, tool triggering, progress updates, literalism, tone, subagents, design, interactive coding, code review, computer use) and says so in the Changed line. This sentence is the baseline basis in section 2.

### O48-05 Note: five API areas shared with the Opus 4.7 migration
- Kind: migration
- Rule: Apply the Opus 4.7 to Opus 5 API parameter changes (sampling parameters, effort default, 1M context window default, mid-conversation system messages, refusal stop details) to Opus 4.8 as well.
- Page says: "<Note> For the API parameter changes since Claude Opus 4.7 (sampling parameters, effort default, 1M context window default, mid-conversation system messages, and refusal stop details), see [Migrating to Claude Opus 5 from Claude Opus 4.7](https://platform.claude.com/docs/en/models/opus-5/migration-guide#migrating-from-opus-47), which covers the same changes on the way to the latest Opus model; Claude Opus 4.8 shares these behaviors. </Note>"
- Applies when: The rearticulated prompt or the described API call mentions temperature, top_p, top_k, an effort default, context size, mid-conversation system messages, or refusal handling.
- Skill applies it by: Section 2 lists the five areas as shared and points at the migration link; any sampling-parameter or context-window assumption in the raw request is flagged as "check against the Opus 4.7 to Opus 5 migration guide" rather than answered with a value this page does not print.

### O48-06 Opus 4.7 migration anchor
- Kind: link
- Rule: Use the Opus 4.7 anchor of the Opus 5 migration guide as the source for Opus 4.8 API parameter behaviours.
- Page says: "[Migrating to Claude Opus 5 from Claude Opus 4.7](https://platform.claude.com/docs/en/models/opus-5/migration-guide#migrating-from-opus-47)"
- Applies when: Any question about Opus 4.8 sampling parameters, effort default, 1M context default, mid-conversation system messages, or refusal stop details.
- Skill applies it by: The URL is in sections 2 and 8; the skill cites it instead of inventing parameter facts.

Page section: Response length and verbosity

### O48-07 Length tracks judged complexity
- Kind: model-note
- Rule: Expect response length to track how complex the model judges the task to be: shorter on simple lookups, much longer on open-ended analysis.
- Page says: "Claude Opus 4.8 calibrates response length to how complex it judges the task to be, rather than defaulting to a fixed verbosity. This usually means shorter answers on simple lookups and much longer ones on open-ended analysis."
- Applies when: The request is open-ended analysis (risk of very long output) or a simple lookup (risk of terse output) and the user has a length expectation.
- Skill applies it by: Adds an explicit length or depth statement to `<output_format>` whenever the user's expectation differs from what the complexity would imply (BP-018); otherwise injects no default length instruction. As the executing model the skill keeps its Step 5 presentation inside the display budget and lets the executed answer scale with complexity.

### O48-08 Tune the prompt when the product fixes style or verbosity
- Kind: technique
- Rule: Tune the prompt when a product depends on a specific style or verbosity instead of relying on the model's default calibration.
- Page says: "If your product depends on a certain style or verbosity of output, you may need to tune your prompts. As an example, to decrease verbosity, you might add:"
- Applies when: Prompt authoring for an application with a fixed verbosity or style requirement.
- Skill applies it by: Names the requirement in `<constraints>` and grafts o48_conciseness into `<output_format>` when shorter output is what the product needs (Standing rule 12: no generic be-concise line of the skill's own).

### O48-09 Sample: o48_conciseness
- Kind: sample-prompt
- Rule: Use this snippet to decrease verbosity on Opus 4.8.
- Page says: see snippet o48_conciseness; the text is "Provide concise, focused responses. Skip non-essential context, and keep examples minimal."
- Applies when: The user wants shorter answers, or the product depends on concise output.
- Skill applies it by: Grafts verbatim into `<output_format>`; identical text to s5_conciseness (one library entry, both IDs as aliases, measured on Sonnet 5 and Opus 4.8). Grafting it onto another profile requires an `Assumed:` entry saying it was measured here.

### O48-10 Name the observed verbosity symptom
- Kind: technique
- Rule: Add targeted instructions against specific observed kinds of verbosity such as over-explaining.
- Page says: "If you see specific examples of kinds of verbosity (such as over-explaining), you can add additional instructions in your prompt to prevent them."
- Applies when: The user reports a concrete verbosity symptom (over-explaining, restating, excess caveats).
- Skill applies it by: Converts a vague complaint like "too wordy" into the named symptom in `<constraints>` and pairs it with a positive example rather than a bare prohibition (O48-11).

### O48-11 Positive concision examples beat prohibitions
- Kind: technique
- Rule: Prefer positive examples of appropriately concise communication over negative examples or do-not instructions.
- Page says: "Positive examples showing how Claude can communicate with the appropriate level of concision tend to be more effective than negative examples or instructions that tell the model what not to do."
- Applies when: Any verbosity-control instruction for this target.
- Skill applies it by: Section 5 conversion: rewrites "do not ramble" style rules into a short positive example of the wanted answer shape in `<examples>` (guide: positive format control, BP-103).

Page section: Calibrating effort and thinking depth

### O48-12 Effort parameter link
- Kind: link
- Rule: Refer to the effort parameter documentation for the intelligence versus token-spend trade-off.
- Page says: "The [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) allows you to tune Claude's intelligence versus token spend, trading off capability for faster speed and lower costs."
- Applies when: The rearticulated prompt or execution plan needs to name an effort level.
- Skill applies it by: Section 8 Related pages; section 2 describes effort as an intelligence versus token-spend dial and cites this page when recommending a level.

### O48-13 Start at xhigh for coding and agentic work, high minimum for intelligence-sensitive work
- Kind: technique
- Rule: Start with xhigh effort for coding and agentic use cases, use a minimum of high for most intelligence-sensitive use cases, and experiment from there.
- Page says: "Start with the `xhigh` effort level for coding and agentic use cases, and use a minimum of `high` effort for most intelligence-sensitive use cases. Experiment with other effort levels to further tune token usage and intelligence:"
- Applies when: The target or executing model is Opus 4.8 and the task is coding, agentic, or intelligence-sensitive.
- Skill applies it by: Sections 2 and 4: the Target model item recommends `xhigh` for coding and agentic requests and `high` as the floor otherwise, with the level always stated as an API parameter rather than written into prompt prose.

### O48-14 max: diminishing returns and overthinking
- Kind: fact
- Rule: Test max effort only for intelligence-demanding tasks, because it can show diminishing returns and is sometimes prone to overthinking.
- Page says: "* **`max`:** Max effort can deliver performance gains in some use cases, but may show diminishing returns from increased token usage. This setting can also sometimes be prone to overthinking. Test max effort for intelligence-demanding tasks."
- Applies when: The user asks for maximum quality or proposes `max` on this target.
- Skill applies it by: The Target model item notes the diminishing-returns and overthinking risk and pairs `max` with the 64k starting output budget (O48-28).

### O48-15 xhigh: best for most coding and agentic work
- Kind: fact
- Rule: Use xhigh as the best effort setting for most coding and agentic use cases.
- Page says: "* **`xhigh`:** Extra high effort is the best setting for most coding and agentic use cases."
- Applies when: Coding or agentic requests.
- Skill applies it by: The default effort recommendation in the Target model item for coding and agentic rows, paired with the 64k output budget (O48-28).

### O48-16 high: balanced and the intelligence-sensitive floor
- Kind: fact
- Rule: Use high as the balanced setting and as the minimum for most intelligence-sensitive use cases.
- Page says: "* **`high`:** This setting balances token usage and intelligence. For most intelligence-sensitive use cases, use a minimum of `high` effort."
- Applies when: Analysis, writing, and knowledge-work requests that are not coding or agentic.
- Skill applies it by: The default effort recommendation for those rows in the Target model item.

### O48-17 medium: cost-sensitive
- Kind: fact
- Rule: Reserve medium effort for cost-sensitive use cases that accept a trade-off in intelligence.
- Page says: "* **`medium`:** Good for cost-sensitive use cases that need to reduce token usage while trading off intelligence."
- Applies when: The user states cost sensitivity.
- Skill applies it by: May recommend `medium` when cost is a stated constraint, always with the under-thinking warning and the raise-effort-first remedy attached (O48-19, O48-27).

### O48-18 low: short, scoped, latency-sensitive only
- Kind: fact
- Rule: Reserve low effort for short, scoped, latency-sensitive tasks that are not intelligence-sensitive.
- Page says: "* **`low`:** Reserve for short, scoped tasks and latency-sensitive workloads that are not intelligence-sensitive."
- Applies when: Quick lookups or latency-bound pipelines.
- Skill applies it by: Recommends `low` only for short scoped work; otherwise the Target model item says why a higher level is chosen.

### O48-19 Strict effort adherence; literal scope at low and medium
- Kind: model-note
- Rule: Expect strict adherence to effort levels, with low and medium scoping work to exactly what was asked and a risk of under-thinking at low on moderately complex tasks.
- Page says: "Claude Opus 4.8 respects effort levels strictly, especially at the low end. At `low` and `medium`, the model scopes its work to what was asked rather than going above and beyond. This is good for latency and cost, but on moderately complex tasks running at `low` effort there is some risk of under-thinking."
- Applies when: Any run at `low` or `medium` effort, or when the user expects extras beyond the literal task.
- Skill applies it by: At `low` or `medium`, `<task>` spells out every wanted sub-step and every "also check X" expectation because the model will not go above and beyond; the Target model item records the under-thinking risk at `low`. Section 6 applies the same reading to the skill's own run.

### O48-20 Raise effort for shallow reasoning
- Kind: technique
- Rule: Raise effort to high or xhigh when reasoning is shallow, rather than prompting around it.
- Page says: "If you observe shallow reasoning on complex problems, raise effort to `high` or `xhigh` rather than prompting around it."
- Applies when: The user reports shallow or under-thought answers on complex problems.
- Skill applies it by: Recommends the effort change in the Target model item first and does not stack "think harder" phrases; o48_low_effort_reasoning is grafted only when effort must stay low (O48-21).

### O48-21 Sample: o48_low_effort_reasoning
- Kind: sample-prompt
- Rule: Graft this targeted guidance only when effort must stay at low for latency and the task needs multistep reasoning.
- Page says: see snippet o48_low_effort_reasoning; the text is "This task involves multistep reasoning. Think carefully through the problem before responding."
- Applies when: Effort is pinned at `low` for latency and the task is moderately complex.
- Skill applies it by: Grafts into `<execution_guidance>` only in that case, never when effort can simply be raised (O48-20); identical text to s5_low_effort_multistep (one library entry, both IDs as aliases).

### O48-22 Sweep effort actively when upgrading
- Kind: model-note
- Rule: Experiment actively with effort when upgrading to Opus 4.8, because it matters more here than on any prior Opus.
- Page says: "Effort is likely to be more important for this model than for any prior Opus, so experiment with it actively when you upgrade."
- Applies when: Migrating a workload from an earlier Opus onto Opus 4.8.
- Skill applies it by: Section 2 records the sweep; a migration rearticulation adds an effort sweep to `<verification>` or the evaluation step and names it in `<success_criteria>`.

### O48-23 Thinking is off unless the caller sets adaptive
- Kind: fact
- Rule: Treat thinking as off on Opus 4.8 unless thinking: {type: "adaptive"} is explicitly set.
- Page says: "On Claude Opus 4.8, thinking is off unless you explicitly set `thinking: {type: \"adaptive\"}`."
- Applies when: Any API prompt authoring for this target, or any request that assumes thinking is on.
- Skill applies it by: Section 2 records the default and the exact enabling syntax. When the request expects reasoning, the Target model item states that adaptive thinking must be set by the caller; any `budget_tokens` assumption is stripped with the 400 reason (BP-189) and the remaining parameter questions are routed to the migration guide (O48-05).

### O48-24 Adaptive triggering is steerable
- Kind: technique
- Rule: Steer adaptive thinking triggering with prompt guidance when the model thinks more often than wanted, and measure the effect.
- Page says: "The triggering behavior for [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) is steerable. If you find the model thinking more often than you'd like, which can happen with large or complex system prompts, add guidance to steer it. As always, measure the effect of any prompting changes on performance."
- Applies when: Adaptive thinking is on, the system prompt is large or complex, and thinking latency is the complaint.
- Skill applies it by: Grafts o48_thinking_steer into `<execution_guidance>` and adds a measurement step; the large-system-prompt trigger is also why the rearticulated prompt itself stays inside the Step 5 line budget (BP-206).

### O48-25 Adaptive thinking documentation link
- Kind: link
- Rule: Use the adaptive thinking page for the mechanics of the thinking parameter.
- Page says: "[adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)"
- Applies when: Explaining or configuring thinking on this target.
- Skill applies it by: The URL sits next to the thinking default in section 2 and in section 8.

### O48-26 Sample: o48_thinking_steer
- Kind: sample-prompt
- Rule: Use this snippet to make adaptive thinking trigger less often.
- Page says: see snippet o48_thinking_steer; the text is "Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multistep reasoning. When in doubt, respond directly."
- Applies when: Adaptive thinking is enabled and the model thinks more often than the use case warrants.
- Skill applies it by: Grafts into `<execution_guidance>` only when adaptive thinking is on, over-triggering is the reported problem, and latency is the concern, and pairs it with the measurement step O48-24 requires. The verbatim text keeps its em dash, which is what separates it from s5_thinking_trigger_guard (comma) and the guide's think_only_when_useful (hyphen, BP-207); the Opus 4.8 text is fenced separately inside the shared `think_only_when_useful` entry, alongside the Sonnet 5 comma form and the guide's hyphen form (BP-207).

### O48-27 Under-thinking at medium: raise effort first
- Kind: technique
- Rule: For hard workloads at medium effort showing under-thinking, raise effort first and prompt for depth only if finer control is needed.
- Page says: "Conversely, if you're running hard workloads at `medium` and seeing under-thinking, the first lever is to raise effort. If you need finer control, prompt for it directly."
- Applies when: `medium` effort with visible under-thinking on hard tasks.
- Skill applies it by: Orders the remedies: the effort change in the Target model item first, a depth instruction only when the user has pinned effort.

### O48-28 Note: 64k starting output budget at max or xhigh
- Kind: fact
- Rule: At max or xhigh effort set a large max output token budget, starting at 64k tokens and tuning from there.
- Page says: "<Note> If you are running Claude Opus 4.8 at `max` or `xhigh` effort, set a large max output token budget so the model has room to think and act across its subagents and tool calls. Start at 64k tokens and tune from there. </Note>"
- Applies when: Running at `max` or `xhigh`, especially with subagents and tool calls.
- Skill applies it by: Section 2 records the figure; whenever the skill recommends `xhigh` or `max` for this target, the Target model item or `<execution_guidance>` states the 64k starting budget. This is the Opus 4.8 counterpart of the Sonnet 5 headroom rule and is not carried to other profiles.

Page section: Tool use triggering

### O48-29 Reasoning is favoured over tool calls
- Kind: model-note
- Rule: Expect Opus 4.8 to favour reasoning over tool calls, which is usually beneficial.
- Page says: "Claude Opus 4.8 has a tendency to favor reasoning over tool calls. This produces better results in most cases."
- Applies when: Any agentic or search task where the user expects tool calls.
- Skill applies it by: Sections 4 and 6: the rearticulation does not assume the model will search before answering, so freshness-sensitive tasks state search-before-answer explicitly in `<execution_guidance>`; as the executing model the skill deliberately reads and searches before making claims (Standing rule 6).

### O48-30 Effort is the tool-usage lever
- Kind: technique
- Rule: Raise effort to high or xhigh to increase tool usage, especially in knowledge work, agentic search, and coding.
- Page says: "However, increasing the effort setting is a useful lever to increase the level of tool usage, especially in knowledge work. `high` or `xhigh` effort settings show substantially more tool usage in agentic search and coding."
- Applies when: The task needs thorough tool-driven exploration and the user wants more tool use.
- Skill applies it by: The Target model item recommends `high` or `xhigh` and explains the tool-usage effect rather than adding "use your tools" nudges.

### O48-31 Say when, how, and why to use each tool
- Kind: technique
- Rule: Explicitly instruct when and how to use each tool, including why, when the model under-uses one such as web search.
- Page says: "For scenarios where you want more tool use, you can also adjust your prompt to explicitly instruct the model about when and how to properly use its tools. For instance, if you find that the model is not using your web search tools, clearly describe why and how it should."
- Applies when: An available tool the task requires is not being called.
- Skill applies it by: Adds a tool-usage paragraph to `<execution_guidance>` naming each expected tool, when to call it, and why, using the guide's context-and-motivation and targeted-trigger techniques (BP-145, BP-181) instead of a blanket default.

Page section: User-facing progress updates

### O48-32 Regular, higher-quality updates without scaffolding
- Kind: model-note
- Rule: Expect more regular, higher-quality user-facing updates during long agentic traces without extra scaffolding.
- Page says: "Claude Opus 4.8 provides more regular, higher-quality updates to the user throughout long agentic traces."
- Applies when: Long agentic tasks.
- Skill applies it by: Adds no progress-cadence instruction for this target; the Fable 5.1 progress_updates_line is not grafted. Section 6: as the executing model the skill gives natural interim updates and follows no forced cadence.

### O48-33 Remove forced status-message scaffolding
- Kind: anti-pattern
- Rule: Remove scaffolding that forces interim status messages, such as summarising after every three tool calls.
- Page says: "If you've added scaffolding to force interim status messages (\"After every 3 tool calls, summarize progress\"), try removing it."
- Applies when: The raw request or a pasted prompt carries a forced progress-update cadence.
- Skill applies it by: Section 5: deletes the cadence lines and records the removal in the Changed line.

### O48-34 Describe and exemplify the update shape instead
- Kind: technique
- Rule: Describe the desired shape of progress updates explicitly and provide examples when their length or content is miscalibrated.
- Page says: "If you find that the length or contents of Claude Opus 4.8's user-facing updates are not well-calibrated to your use case, explicitly describe what these updates should look like in the prompt and provide examples."
- Applies when: Updates are too long, too short, or off-topic for the product.
- Skill applies it by: Adds a description of the update shape plus one example update in `<output_format>` or `<examples>`, in place of a cadence rule.

Page section: More literal instruction following

### O48-35 Literal, explicit interpretation
- Kind: model-note
- Rule: Expect literal and explicit interpretation of prompts, particularly at lower effort levels.
- Page says: "Claude Opus 4.8 interprets prompts literally and explicitly, particularly at lower effort levels."
- Applies when: Every rearticulation for this target, most of all at `low` or `medium` effort.
- Skill applies it by: Spells out every wanted behaviour and its scope in `<task>`, `<constraints>`, and `<output_format>`; drops all-caps emphasis, which literal following makes unnecessary (BP-018, BP-162). Section 6: as the executing model the skill follows the user's stated scope and records an assumption rather than widening it silently.

### O48-36 No silent generalisation, no inferred requests
- Kind: model-note
- Rule: Do not rely on the model to generalise an instruction from one item to another or to infer work you did not request.
- Page says: "It does not silently generalize an instruction from one item to another, and it does not infer requests you didn't make."
- Applies when: The raw request states an instruction on one item but expects it applied to many.
- Skill applies it by: Detects single-item instructions with implied breadth and rewrites them with explicit scope (O48-38, o48_explicit_scope), enumerating the full target set.

### O48-37 Literalism is precision for pipelines
- Kind: fact
- Rule: Lean on the literalism as an asset for API pipelines, structured extraction, and carefully tuned prompts that need predictable behaviour.
- Page says: "The upside of this literalism is precision and less thrash, and it generally performs better for API use cases with carefully tuned prompts, structured extraction, and pipelines where you want predictable behavior."
- Applies when: Structured extraction, classification, or pipeline prompt authoring.
- Skill applies it by: Favours exhaustive explicit rules and a strict output schema over open-ended guidance for those rows, and records literal following as an advantage in the Target model item.

### O48-38 State scope explicitly
- Kind: technique
- Rule: State the scope explicitly whenever an instruction should apply broadly.
- Page says: "If you need Claude to apply an instruction broadly, state the scope explicitly (for example, \"Apply this formatting to every section, not just the first one\")."
- Applies when: Any instruction meant to cover more than the item it is attached to.
- Skill applies it by: Appends an explicit scope clause (every, all, each, not just) to each rule in `<task>`, `<constraints>`, and `<output_format>` that has to generalise.

### O48-39 Sample: o48_explicit_scope
- Kind: sample-prompt
- Rule: Use this phrasing pattern to make an instruction's scope explicit.
- Page says: see snippet o48_explicit_scope; the text is "Apply this formatting to every section, not just the first one"
- Applies when: A formatting or handling rule must cover all items rather than the first instance.
- Skill applies it by: Adapts the noun ("section") to the user's target set while keeping the "every X, not just the first" shape; identical text to s5_explicit_scope (one library entry, both IDs as aliases).

Page section: Tone and writing style

### O48-40 Direct, opinionated default voice
- Kind: model-note
- Rule: Expect a direct, opinionated prose style with minimal validation-forward phrasing and sparing emoji use, and expect long-form style to shift from prior models.
- Page says: "As with any new model, prose style on long-form writing may shift. Claude Opus 4.8 tends toward a direct, opinionated style with minimal validation-forward phrasing and sparing emoji use."
- Applies when: Long-form writing or a product voice on this target.
- Skill applies it by: Sections 3 and 6: the skill's own presentation is direct and free of validation phrases (Standing rule 12); when the user wants warmth the rearticulation grafts o48_warm_tone.

### O48-41 Re-evaluate voice prompts against the new baseline
- Kind: technique
- Rule: Re-evaluate existing style prompts against the Opus 4.8 baseline when a product depends on a specific voice.
- Page says: "If your product relies on a specific voice, re-evaluate style prompts against the new baseline."
- Applies when: Migrating a voice-sensitive product prompt onto this target.
- Skill applies it by: Keeps the supplied voice rules, restates them positively, adds a short example passage in `<examples>` where one can be shown, and adds a `<verification>` check comparing output against the wanted voice.

### O48-42 Sample: o48_warm_tone
- Kind: sample-prompt
- Rule: Use this snippet when the product voice should be warmer or more conversational than the default.
- Page says: see snippet o48_warm_tone; the text is "Use a warm, collaborative tone. Acknowledge the user's framing before answering."
- Applies when: A warmer, more conversational register is requested.
- Skill applies it by: Grafts into the role or tone position, or into `<constraints>`, only when warmth is asked for; identical text to s5_warm_tone (one library entry, both IDs as aliases).

Page section: Controlling subagent spawning

### O48-43 Fewer subagents by default
- Kind: model-note
- Rule: Expect Opus 4.8 to spawn fewer subagents by default.
- Page says: "Claude Opus 4.8 tends to spawn fewer subagents by default."
- Applies when: Fan-out or multi-file agentic tasks.
- Skill applies it by: Sections 4 and 6: because the default is fewer, the subagent snippet for this target encourages delegation where it helps, which is the opposite direction from the Opus 5 damping prompt (o5_delegation_guidance). As the executing model the skill delegates only where delegation is clearly useful and states in the plan when fan-out is intended.

### O48-44 Spawning is steerable with explicit guidance
- Kind: technique
- Rule: Give explicit guidance about when subagents are desirable, because the spawning behaviour is steerable through prompting.
- Page says: "However, this behavior is steerable through prompting; give Claude Opus 4.8 explicit guidance around when subagents are desirable. A toy example for a coding use case:"
- Applies when: The request involves parallelisable work (many items, many files).
- Skill applies it by: Adds a subagent policy paragraph to `<execution_guidance>` (o48_subagent_guidance for coding fan-out) so the model neither over- nor under-delegates.

### O48-45 Sample: o48_subagent_guidance
- Kind: sample-prompt
- Rule: Graft this two-part subagent policy for coding use cases.
- Page says: see snippet o48_subagent_guidance; the two parts are "Do not spawn a subagent for work you can complete directly in a single response (e.g. refactoring a function you can already see)." and "Spawn multiple subagents in the same turn when fanning out across items or reading multiple files."
- Applies when: A coding task with a mix of direct edits and fan-out reads.
- Skill applies it by: Grafts into `<execution_guidance>` for coding fan-out on this target. The page labels it a toy example, so the parenthetical is adapted to the actual task; the second sentence is the half that matters here, since the default is fewer subagents (O48-43).

Page section: Design and frontend defaults

### O48-46 The persistent house style
- Kind: model-note
- Rule: Expect a consistent default house style: warm cream or off-white background around #F4F1EA, serif display type (Georgia, Fraunces, Playfair), italic word-accents, and a terracotta or amber accent.
- Page says: "Claude Opus 4.8 has strong design instincts, with a consistent default house style: warm cream/off-white backgrounds (~`#F4F1EA`), serif display type (Georgia, Fraunces, Playfair), italic word-accents, and a terracotta/amber accent."
- Applies when: Any UI, slide, or web design request on this target.
- Skill applies it by: Design rearticulations always specify a palette and type direction, or ask for options, so the house style is a choice rather than a default. This description is printed only on the Opus 4.8 page; the Sonnet 5 profile deliberately does not borrow it.

### O48-47 Where the house style fits and where it misfits
- Kind: fact
- Rule: Accept the default house style for editorial, hospitality, and portfolio briefs; override it for dashboards, dev tools, fintech, healthcare, and enterprise apps.
- Page says: "This reads well for editorial, hospitality, and portfolio briefs, but will feel off for dashboards, dev tools, fintech, healthcare, or enterprise apps."
- Applies when: The design brief's domain is known.
- Skill applies it by: Classifies the brief's domain in the frontend row; a dashboard, dev-tool, fintech, healthcare, or enterprise brief must carry a concrete alternative spec (O48-50) or the propose-options step (O48-52).

### O48-48 The default appears in decks as well as web UIs
- Kind: fact
- Rule: Expect the house style default in slide decks as well as web UIs.
- Page says: "The default appears in slide decks and web UIs."
- Applies when: Slide deck or web UI generation.
- Skill applies it by: Applies the design overrides to presentation requests too, not only to web pages.

### O48-49 Generic negative design instructions do not create variety
- Kind: anti-pattern
- Rule: Do not rely on generic instructions such as "don't use cream" or "make it clean and minimal" for design variety; they shift the model to a different fixed palette.
- Page says: "This default is persistent. Generic instructions (\"don't use cream,\" \"make it clean and minimal\") tend to shift the model to a different fixed palette rather than producing variety."
- Applies when: A design prompt contains only generic or negative style instructions.
- Skill applies it by: Section 5 conversion: replaces them with a concrete spec (O48-50) or the propose-options instruction (O48-52) and explains the reason in the Assumed line.

### O48-50 Escape 1: specify a concrete alternative
- Kind: technique
- Rule: Specify a concrete visual alternative, because the model follows explicit design specs precisely.
- Page says: "**1. Specify a concrete alternative.** The model follows explicit specs precisely:"
- Applies when: The user knows the visual direction they want.
- Skill applies it by: Expands the user's design intent into concrete palette hexes, typography, radius, spacing, motion, and structure across `<task>` and `<constraints>`, using o48_aefrm_concrete_spec as the reference shape.

### O48-51 Sample: o48_aefrm_concrete_spec
- Kind: sample-prompt
- Rule: Use this full brief as the reference shape for a concrete design specification.
- Page says: see snippet o48_aefrm_concrete_spec; it opens "Design a desktop landing page for a supplement brand called AEFRM." and closes with the palette "#E9ECEC, #C9D2D4, #8C9A9E, #44545B, #11171B."
- Applies when: A design request where the user has a direction; used as a structural template, not copied literally.
- Skill applies it by: Mirrors its sections (atmosphere, feel, tonal system, imagery, layout and radius, typography, structure, motion, palette hexes) with the user's own values; the AEFRM content itself is never grafted. Identical text to s5_design_concrete_spec_aefrm (one library entry, both IDs as aliases).

### O48-52 Escape 2: propose options before building
- Kind: technique
- Rule: Have the model propose several visual directions before building; this breaks the default and gives users control.
- Page says: "**2. Have the model propose options before building.** This breaks the default and gives users control."
- Applies when: The user has no fixed visual direction.
- Skill applies it by: Prepends a propose-then-pick step (o48_propose_directions) to `<task>` for design requests without a stated direction.

### O48-53 Propose-options replaces temperature for variety
- Kind: migration
- Rule: Replace temperature-based design variety with the propose-options approach, which yields meaningfully different directions across runs.
- Page says: "If you previously relied on `temperature` for design variety, use this approach; it produces meaningfully different directions across runs."
- Applies when: A supplied prompt or workflow uses temperature to get design variety.
- Skill applies it by: Section 5: strips the temperature reliance from the prompt or plan, substitutes o48_propose_directions, and records the substitution in the Changed line. Sampling parameter behaviour itself is routed to the migration guide (O48-05), so the skill does not assert a 400 here as it does on Sonnet 5.

### O48-54 Sample: o48_propose_directions
- Kind: sample-prompt
- Rule: Use this snippet to make the model propose four visual directions and implement only the chosen one.
- Page says: see snippet o48_propose_directions; the text is "Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface — one-line rationale). Ask the user to pick one, then implement only that direction."
- Applies when: A design brief without a fixed direction, or variety wanted across runs.
- Skill applies it by: Grafts into the first step of `<task>` for design requests on this target. The verbatim text keeps its em dash, which separates it from s5_design_propose_directions ("plus a one-line rationale"); the Opus 4.8 text is fenced separately inside the shared `s5_design_propose_directions / o48_propose_directions` entry.

### O48-55 Less frontend prompting is needed than for earlier models
- Kind: model-note
- Rule: Use less frontend design prompting than for earlier models; Opus 4.8 avoids the generic "AI slop" aesthetic with minimal guidance.
- Page says: "Additionally, Claude Opus 4.8 requires less frontend design prompting than previous models to avoid generic patterns that users call the \"AI slop\" aesthetic. With earlier models, Anthropic recommended a lengthier prompt snippet in the [frontend-design skill](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md). However, Claude Opus 4.8 generates distinctive, creative frontends with more minimal prompting guidance."
- Applies when: Frontend generation, especially when a long anti-slop block written for an earlier model is supplied.
- Skill applies it by: Section 5: trims a lengthy earlier-model frontend snippet (the guide's long frontend_aesthetics, BP-330) down to the short frontend_aesthetics_short block plus the variety advice (O48-50 to O48-54), and records the trim.

### O48-56 frontend-design skill link
- Kind: link
- Rule: Refer to the frontend-design skill for the lengthier snippet Anthropic recommended for earlier models.
- Page says: "[frontend-design skill](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md)"
- Applies when: The target is an earlier model than Opus 4.8, or the user asks where the longer frontend prompt lives.
- Skill applies it by: Section 8 Related pages, and the same link in `references/models/legacy-4x.md` as the source of earlier models' frontend guidance. In Claude Code, "Invoke frontend-design before <step>" replaces the paste when that skill is loaded (BP-342).

### O48-57 Sample: frontend_aesthetics_short
- Kind: sample-prompt
- Rule: Graft this short anti-generic aesthetics block together with the variety advice for frontend work.
- Page says: see snippet frontend_aesthetics_short; the block opens "<frontend_aesthetics> NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds)..." and closes "Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions. </frontend_aesthetics>"
- Applies when: Any frontend or UI generation request on this target.
- Skill applies it by: Grafts unchanged, wrapper tag and its all-caps NEVER included as quoted, in the system-prompt position, paired with o48_propose_directions or a concrete spec. The page's rule list names this block `frontend_aesthetics`; the library stores the guide's long block under that ID (BP-330) and this identical page block, also printed on the Sonnet 5 page, under `frontend_aesthetics_short` with both page IDs as aliases.

Page section: Interactive coding products

### O48-58 Interactive sessions cost more tokens than single-turn agents
- Kind: model-note
- Rule: Expect higher token usage in interactive multi-turn coding sessions than in single-turn autonomous agents, because the model reasons more after user turns.
- Page says: "Claude Opus 4.8's token usage and behavior can differ between autonomous, asynchronous coding agents with a single user turn and interactive, synchronous coding agents with multiple user turns. Specifically, it tends to use more tokens in interactive settings, primarily because it reasons more after user turns. This can improve long-horizon coherence, instruction following, and coding capabilities in long, interactive coding sessions, but also comes with more token usage."
- Applies when: Building or running an interactive coding product on this target.
- Skill applies it by: Section 2 and the interactive coding taxonomy row: the Target model item notes the token trade-off and the rearticulation prefers a fully specified first turn (O48-60).

### O48-59 xhigh or high, an auto mode, fewer interactions
- Kind: technique
- Rule: Use xhigh or high effort, add autonomous features such as an auto mode, and reduce required human interactions to maximise performance and token efficiency in coding products.
- Page says: "To maximize both performance and token efficiency in coding products, use `xhigh` or `high` effort, add autonomous features like an auto mode, and reduce the number of human interactions required from your users."
- Applies when: Prompt or product design for a coding agent.
- Skill applies it by: The Target model item recommends `xhigh` or `high`, and `<task>` carries explicit stop conditions and pre-made decisions so the agent finishes without check-ins.

### O48-60 Specify task, intent, and constraints in the first turn
- Kind: technique
- Rule: Specify the task, intent, and relevant constraints upfront in the first human turn when limiting user interactions.
- Page says: "Of course, when limiting the number of required user interactions, it's important to specify the task, intent, and relevant constraints upfront in the first human turn. Providing well-specified, clear, and accurate task descriptions upfront can help maximize autonomy and intelligence while minimizing extra token usage after user turns."
- Applies when: Any coding request on this target, and any product that minimises user turns.
- Skill applies it by: This is the core justification for the skill on Opus 4.8: `<task>`, `<context>` (intent and motivation), and `<constraints>` are front-loaded into one complete first-turn prompt so execution needs no follow-up turns.

### O48-61 More autonomous than prior models
- Kind: model-note
- Rule: Lean on Opus 4.8's greater autonomy by giving a complete upfront specification.
- Page says: "Because Claude Opus 4.8 is more autonomous than prior models, this usage pattern helps to maximize performance."
- Applies when: Coding or agentic work on this target.
- Skill applies it by: Section 6: as the executing model the skill proceeds through Steps 6 and 7 once the rearticulated prompt is presented rather than pausing for confirmation, except for a dry run, a `[confirm]` step, or a question only the user can answer.

### O48-62 Drip-fed, underspecified prompts cost more
- Kind: anti-pattern
- Rule: Avoid ambiguous or underspecified prompts conveyed progressively over multiple turns; they reduce token efficiency and sometimes performance.
- Page says: "In contrast, ambiguous or underspecified prompts conveyed progressively over multiple user turns tend to relatively reduce token efficiency and sometimes performance."
- Applies when: The raw request is vague and would otherwise be clarified across several turns.
- Skill applies it by: Step 2 resolves ambiguity in one pass with stated assumptions and explicit success criteria; any unavoidable question goes at the end of the first turn rather than deferring the work.

Page section: Code review harnesses

### O48-63 Better bug finding, higher recall and precision
- Kind: model-note
- Rule: Expect meaningfully better bug finding, with higher recall and precision than prior models in internal evals.
- Page says: "Claude Opus 4.8 is meaningfully better at finding bugs than prior models, and has both higher recall and precision in internal evals."
- Applies when: Code review or bug-hunting tasks.
- Skill applies it by: Section 2 and the code-review taxonomy row; sets the expectation used when interpreting a recall change (O48-64), so no "be more thorough" text is added.

### O48-64 A recall drop is a harness effect
- Kind: model-note
- Rule: Treat lower initial recall from a harness tuned for an earlier model as a harness effect, not a capability regression.
- Page says: "However, if your code-review harness was tuned for an earlier model, you may initially see lower recall. This is likely a harness effect, not a capability regression."
- Applies when: The user reports fewer review findings after moving a harness onto Opus 4.8.
- Skill applies it by: States the diagnosis in the Target model item and applies the coverage fix (o48_review_coverage) before any other change.

### O48-65 Conservative review wording is followed faithfully
- Kind: anti-pattern
- Rule: Do not use "only report high-severity issues", "be conservative", or "don't nitpick" in a finding-stage review prompt; Opus 4.8 follows them faithfully and withholds real findings.
- Page says: "When a review prompt says things like \"only report high-severity issues,\" \"be conservative,\" or \"don't nitpick,\" Claude Opus 4.8 may follow that instruction more faithfully than earlier models did: it may investigate the code just as thoroughly, identify the bugs, and then not report findings it judges to be below your stated bar. This can show up as the model doing the same depth of investigation but converting fewer investigations into reported findings, especially on lower-severity bugs. Precision typically rises, but measured recall can fall even though the model's underlying bug-finding ability has improved."
- Applies when: Any review prompt for this target containing conservative or severity-gating wording.
- Skill applies it by: Section 5: strips the wording from finding-stage prompts, replaces it with o48_review_coverage or a concrete bar (O48-69), and notes the precision-up recall-down mechanics in the Target model item. Review `<success_criteria>` are framed around coverage plus downstream ranking, not a low finding count.

### O48-66 Sample: o48_review_coverage
- Kind: sample-prompt
- Rule: Graft this coverage-first language into the finding stage of a code review prompt.
- Page says: see snippet o48_review_coverage; it opens "Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that." and closes "For each finding, include your confidence level and an estimated severity so a downstream filter can rank them."
- Applies when: A code review or bug-finding prompt, especially with a downstream filter.
- Skill applies it by: Grafts into `<task>` and adds confidence and severity fields to the `<output_format>` schema; identical text to s5_code_review_coverage (one library entry, both IDs as aliases). Opus 5, which prints no snippet of its own for this rule, borrows this text and records it as measured here (O5-12).

### O48-67 The coverage prompt works without a second stage
- Kind: technique
- Rule: Use the coverage prompt even without an actual second step, because moving confidence filtering out of the finding step often helps on its own.
- Page says: "This prompt can be used without having an actual second step, but moving confidence filtering out of the finding step often helps."
- Applies when: A single-stage review harness.
- Skill applies it by: May graft o48_review_coverage even when the user has no verification stage, stating that a later filter is optional; in same-turn execution the skill can run the filtering pass itself after the coverage pass.

### O48-68 Name the finding stage's job when later stages exist
- Kind: technique
- Rule: When the harness has a separate verification, deduplication, or ranking stage, tell the model explicitly that its finding-stage job is coverage rather than filtering.
- Page says: "If your harness has a separate verification, deduplication, or ranking stage, tell the model explicitly that its job at the finding stage is coverage rather than filtering."
- Applies when: A multi-stage review harness.
- Skill applies it by: Adds the stage role sentence ("your job at this stage is coverage") to `<role>` or `<task>`.

### O48-69 Define a self-filter bar concretely
- Kind: technique
- Rule: For single-pass self-filtering, define the reporting bar concretely instead of with qualitative words such as "important".
- Page says: "If you do want the model to self-filter in a single pass, be concrete about where the bar is rather than using qualitative terms like \"important\": for example, \"report any bugs that could cause incorrect behavior, a test failure, or a misleading result; only omit nits like pure style or naming preferences.\""
- Applies when: The user wants a single-pass review that filters.
- Skill applies it by: Replaces "important", "significant", and "high-severity" with the concrete inclusion and exclusion rule o48_review_concrete_bar in `<constraints>`.

### O48-70 Sample: o48_review_concrete_bar
- Kind: sample-prompt
- Rule: Graft this concrete reporting bar when a single-pass review must self-filter.
- Page says: see snippet o48_review_concrete_bar; the text is "report any bugs that could cause incorrect behavior, a test failure, or a misleading result; only omit nits like pure style or naming preferences."
- Applies when: A single-pass code review with self-filtering and no downstream filter.
- Skill applies it by: Grafts into `<constraints>`; identical text to s5_code_review_concrete_bar (one library entry, both IDs as aliases).

### O48-71 Validate recall or F1 on a subset
- Kind: technique
- Rule: Iterate review prompts against a subset of evals or test cases to validate recall or F1 gains.
- Page says: "Iterate on prompts against a subset of your evals or test cases to validate recall or F1 score gains."
- Applies when: Tuning a review harness prompt for this target.
- Skill applies it by: Adds a `<verification>` step and a `<success_criteria>` entry that measure recall or F1 on a held-out subset before rollout.

Page section: Computer use

### O48-72 Computer use toolset versions
- Kind: fact
- Rule: Use computer_toolset_20260801 (Claude API and Google Cloud) or the earlier computer_20251124 tool version for computer use on Opus 4.8.
- Page says: "Claude Opus 4.8 supports the `computer_toolset_20260801` toolset (on the Claude API and Google Cloud) and the earlier `computer_20251124` tool version."
- Applies when: Computer-use prompt or tool-definition authoring for this target.
- Skill applies it by: Section 2 (harness notes) records both strings; a rewritten computer-use setup names `computer_toolset_20260801` as the current toolset and flags any other version string as unsupported by this page.

### O48-73 Browser use toolset
- Kind: fact
- Rule: Use browser_toolset_20260801 for tasks inside webpages, on the Claude API and Google Cloud.
- Page says: "On the Claude API and Google Cloud, Claude Opus 4.8 also supports the [browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) (`browser_toolset_20260801`) for tasks inside webpages."
- Applies when: Web-page automation requests for this target.
- Skill applies it by: Section 2 records the string; the rearticulation selects the browser toolset for in-page tasks and names the platform restriction.

### O48-74 Browser use tool link
- Kind: link
- Rule: Refer to the browser use tool page for browser_toolset_20260801 details.
- Page says: "[browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)"
- Applies when: Configuring browser use on this target.
- Skill applies it by: Section 8 Related pages.

### O48-75 Computer use tool link
- Kind: link
- Rule: Refer to the computer use tool page for computer use mechanics.
- Page says: "[Computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)"
- Applies when: Configuring computer use on this target.
- Skill applies it by: Section 8 Related pages.

### O48-76 Maximum screenshot resolution
- Kind: fact
- Rule: Keep screenshots at or below the maximum resolution of 2576px / 3.75MP; computer use works across resolutions up to that limit.
- Page says: "[Computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) capability works across resolutions, up to a maximum resolution of 2576px / 3.75MP."
- Applies when: Choosing screenshot size for a computer-use setup.
- Skill applies it by: Section 2 records the ceiling; computer-use rearticulations state a resolution within it in `<constraints>`.

### O48-77 1080p as the default balance
- Kind: fact
- Rule: Send images at 1080p as the default balance of performance and cost for computer use.
- Page says: "Internal computer use testing shows that sending images at 1080p provides a good balance of performance and cost."
- Applies when: A computer-use setup with no stated cost constraint.
- Skill applies it by: Recommends 1080p in `<execution_guidance>` for computer-use requests.

### O48-78 Lower-cost resolutions
- Kind: fact
- Rule: Use 720p or 1366x768 as lower-cost resolutions with strong performance for cost-sensitive computer-use workloads.
- Page says: "For particularly cost-sensitive workloads, 720p or 1366×768 are lower-cost options with strong performance."
- Applies when: Cost is a stated constraint on a computer-use workload.
- Skill applies it by: Recommends 720p or 1366x768 instead of 1080p in that case.

### O48-79 Test resolution and effort on the workload
- Kind: technique
- Rule: Test resolution and effort settings on your own workload to find the ideal computer-use configuration.
- Page says: "Conduct your own testing to find the ideal settings for your use case; experimenting with effort settings can also help tune the model's behavior."
- Applies when: Any computer-use deployment on this target.
- Skill applies it by: Adds a resolution-and-effort sweep to `<verification>`; section 2 notes that effort also shapes computer-use behaviour, so the effort lever (O48-30) applies there too.

Guide rules naming Opus 4.8 or its generation (from Prompting best practices; catalog IDs, quoted from the guide)

### BP-002 Opus 4.8 is inside the guide's covered set
- Kind: fact
- Rule: Treat the guide as authoritative for exactly these thirteen current models and route any other model to the migration considerations.
- Guide says: "This is the reference for prompt engineering with current Claude models, including Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, and Claude Haiku 4.5."
- Applies when: Resolving whether guide techniques are measured on the target.
- Skill applies it by: Opus 4.8 needs no analogy note; the guide applies directly. Opus 4.7 and 4.6 are also in the set but have no page, so they use this profile by analogy (`references/models/legacy-4x.md`).

### BP-015 The Fable 5 row is framed against Opus 4.8
- Kind: model-note
- Rule: Read the Fable 5 page as the set of differences from Opus 4.8, which makes Opus 4.8 the reference point for that migration.
- Guide says: "| Claude Fable 5 and Claude Mythos 5 | [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) | Differences from Claude Opus 4.8: effort levels, instruction following, long-run progress claims, memory systems, and the `reasoning_extraction` refusal category. |"
- Applies when: Moving a prompt between Opus 4.8 and the Fable family, in either direction.
- Skill applies it by: A Fable 5 target keeps the substance of an Opus 4.8 prompt and takes only the F5 deltas; no O48 snippet is carried onto a Fable target without an `Assumed:` entry. The Fable 5 page also names Claude Opus 4.8 as the documented fallback for declined Fable 5 requests (F5-10, F5-11), which is a routing fact about Fable 5, not a statement about this model's own safeguards.

### BP-018 The guide's model table row for Opus 4.8
- Kind: model-note
- Rule: For Opus 4.8, set response length, effort and thinking depth, tool-use trigger conditions, literal instruction following, subagent control, and design and frontend defaults explicitly.
- Guide says: "| Claude Opus 4.8 | [Prompting Claude Opus 4.8](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8) | Response length, effort and thinking-depth calibration, tool use triggering, literal instruction following, subagent control, and design and frontend defaults. |"
- Applies when: The user targets Opus 4.8.
- Skill applies it by: Section 4 states a response-length expectation when one exists, recommends effort rather than prompting for depth, uses targeted tool-trigger conditions instead of "default to X" phrasing, drops all-caps emphasis because instruction following is literal, adds an explicit subagent policy, and specifies the design direction. Subagent control is the item that separates this row from the Sonnet 5 row (BP-016).

### BP-023 Prompting Claude Opus 4.8 page link
- Kind: link
- Rule: Open the Prompting Claude Opus 4.8 page for Opus 4.8 specifics.
- Guide says: "[Prompting Claude Opus 4.8](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8)"
- Applies when: The user targets Opus 4.8.
- Skill applies it by: This file is the local rendering of that page; the header cites it.

### BP-062 Data-first ordering has no model exception
- Kind: fact
- Rule: Apply data-first ordering for every model; there is no model exception.
- Guide says: "This improves performance across all models."
- Applies when: Any long-document rearticulation for Opus 4.8.
- Skill applies it by: `<documents>` precedes `<task>` on Opus 4.8 exactly as on every other model.

### BP-124 Last-turn prefill is unsupported
- Kind: fact
- Rule: Do not use a prefilled assistant response on the last assistant turn with Claude 4.6 models or later, which includes Opus 4.8.
- Guide says: "Starting with Claude 4.6 models and [Claude Mythos Preview](https://anthropic.com/glasswing), prefilled responses (providing a partial assistant message for Claude to continue from) on the last assistant turn are no longer supported."
- Applies when: A pasted prompt ends with a partial assistant turn, or the request says "start your answer with".
- Skill applies it by: Step 4 converts prefill constructs into a direct instruction, a named output tag, or enumerated labels; historical assistant turns used as examples stay.

### BP-189 budget_tokens returns 400 on 4.7 and later
- Kind: fact
- Rule: Never emit budget_tokens for Claude 4.7 or later models; the API returns a 400 error.
- Guide says: "On Claude 4.7 and later models, setting `budget_tokens` returns a 400 error."
- Applies when: Any generated or migrated API configuration for Opus 4.8.
- Skill applies it by: Strips `budget_tokens` and `type: "enabled"`, substitutes `thinking: {type: "adaptive"}` plus `output_config.effort`, keeps `max_tokens`, and records the substitution with the 400 reason in the Target model item (BP-208 to BP-212).

### BP-213 claude-opus-4-8 is the guide's adaptive-thinking example target
- Kind: fact
- Rule: Use the guide's model pairing as the migration reference: claude-sonnet-4-5-20250929 (older, extended thinking) to claude-opus-4-8 (adaptive).
- Guide says: "\"model\": \"claude-opus-4-8\"," on the after side of the migration example; the before side reads "\"model\": \"claude-sonnet-4-5-20250929\","
- Applies when: Illustrating or performing a before-and-after thinking migration, or emitting API code for this target.
- Skill applies it by: The API string `claude-opus-4-8` is taken from the guide's after-shape example, which pins adaptive thinking, `output_config.effort` of `high`, and `max_tokens` of 16000 across every SDK sample (BP-209 to BP-215). The example's `high` is the guide's illustration, not a printed Opus 4.8 default (O48-05).

### BP-217 Thinking is off when the parameter is omitted
- Kind: model-note
- Rule: On Claude Opus 4.6 through Opus 4.8 and Sonnet 4.6, thinking is off when the thinking parameter is omitted.
- Guide says: "On Claude Opus 4.6 through Claude Opus 4.8 and Claude Sonnet 4.6, thinking is off when you omit the `thinking` parameter."
- Applies when: Authoring a prompt or request for this target.
- Skill applies it by: Section 2 thinking default; agrees with O48-23. If the task needs reasoning, the Target model item asks the caller to enable adaptive thinking, or the manual chain-of-thought fallback is applied (BP-225).

### BP-225 Manual chain-of-thought as a fallback when thinking is off
- Kind: technique
- Rule: When thinking is off, ask the model to think through the problem step by step as a manual chain-of-thought fallback.
- Guide says: "**Manual chain-of-thought (CoT) prompting as a fallback.** When thinking is off, you can still encourage step-by-step reasoning by asking Claude to think through the problem."
- Applies when: An authored prompt for Opus 4.8 that will run with thinking left off, typically because the caller cannot change the configuration.
- Skill applies it by: Prompt-authoring rows only: adds a step-by-step reasoning request with the final answer in `<answer>` tags when the target runs with thinking off. The first choice is still to have the caller set `thinking: {type: "adaptive"}` (O48-23) or to raise effort (O48-20).

## When this is the TARGET model: add to the rearticulated prompt

The content of the rearticulated prompt follows this section when the target is Opus 4.8. The Fable 5.1 default snippets (progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule) are not grafted. Instruction granularity is enumerated exactly as on Sonnet 5: every item and its scope spelled out, most of all at `low` or `medium` effort (O48-19, O48-35, O48-38). What this profile adds on top of the Sonnet 5 shape is the subagent policy, the tool-usage paragraph, the 64k output budget note, and caller-set adaptive thinking (SKILL.md model deltas row).

Target model item (SKILL.md Step 5, Reading line). Always `Target model: opus-4-8 (<how resolved>)`. When the target differs from the executing model, the request is prompt authoring, or the user asked about speed, cost, or thinking, the item also carries:

- Recommended effort with the page section cited: `xhigh` to start for coding and agentic work (O48-13, O48-15); `high` as the minimum for intelligence-sensitive work (O48-13, O48-16); `medium` only under stated cost pressure (O48-17); `low` only for short scoped latency-bound work, with the under-thinking risk named (O48-18, O48-19); `max` only for intelligence-demanding tasks, with the diminishing-returns and overthinking caveat (O48-14). No default level is asserted, because the page does not print one (O48-05). An effort sweep is recommended on any upgrade onto Opus 4.8 (O48-22).
- Thinking: off unless the caller sets `thinking: {type: "adaptive"}` (O48-23, BP-217); o48_thinking_steer only when adaptive is on and over-triggering is the reported problem (O48-24, O48-26).
- `max_tokens`: a large output budget starting at 64k whenever `xhigh` or `max` is recommended (O48-28).
- `budget_tokens` removed with the 400 reason (BP-189), converted to adaptive thinking plus `output_config.effort` (BP-208 to BP-212).
- Sampling parameters, the effort default, the 1M context default, mid-conversation system messages, and refusal stop details flagged as "check against the Opus 4.7 to Opus 5 migration guide" rather than asserted (O48-05, O48-06).
- Model string `claude-opus-4-8` when API code is produced (BP-213).

For an in-session run with none of these triggers the item reads `Target model: opus-4-8 (executing model)` and nothing more, with one exception. On a code change, agentic long-horizon, or frontend row the item names the starting level and the output budget on every run, in-session included, because the page calls effort more important on this model than on any prior Opus and warns of under-thinking below `high`: `xhigh` to start, 64k max_tokens, and no default printed, which the page routes to the Opus 4.7 to Opus 5 migration guide (O48-13, O48-15, O48-19, O48-22, O48-28, O48-05). The short form stands on every other row, because the page prints starting points rather than a default, which is why this profile stays silent where the Fable 5 page names a level on every run.

- `<role>`: one sentence per the guide. For a multi-stage review harness add the stage role: the finding stage's job is coverage, not filtering (O48-68).
- `<context>`: state the task, intent, and constraints upfront so no follow-up turn is needed (O48-60, O48-62). For computer use or in-page automation name the toolset in context: `computer_toolset_20260801` (or the earlier `computer_20251124`) for screen control and `browser_toolset_20260801` for tasks inside webpages, both on the Claude API and Google Cloud only, and flag any other version string as unsupported by this page (O48-72, O48-73). For extraction and pipeline work say that predictable, literal behaviour is wanted (O48-37). For a design brief name the domain, because the house style suits editorial, hospitality, and portfolio work and misfits dashboards, dev tools, fintech, healthcare, and enterprise apps (O48-46, O48-47). When the caller cannot enable adaptive thinking, say so here so the reasoning fallback has its reason (BP-225).
- `<documents>`: guide rules unchanged, documents before the task (BP-062).
- `<task>`: every implied step written out and the full target set enumerated for each instruction (O48-35, O48-36); each instruction that has to generalise carries an explicit scope clause shaped like o48_explicit_scope, "every X, not just the first" (O48-38, O48-39); at `low` or `medium` every wanted sub-step and "also check" expectation stated (O48-19). Coding: explicit stop conditions and pre-made decisions so the run finishes without check-ins (O48-59). Design: o48_propose_directions as the first step for an open brief (O48-52, O48-54), or a concrete spec shaped like o48_aefrm_concrete_spec when the user has a direction (O48-50, O48-51), applied to slide decks as well as web UIs (O48-48). Review: o48_review_coverage in the finding stage (O48-66, O48-67); when it is not stated whether a downstream filter exists, the words finder, finding stage, or first pass imply a later stage, so coverage is grafted and the inference recorded, and o48_review_concrete_bar is used instead only when the user wants the single pass to self-filter, because the coverage prompt still helps when there is no second step (O48-67, O48-69, O48-70). Computer use: a resolution-and-effort validation step (O48-79). Migration onto Opus 4.8: an effort sweep as a numbered step (O48-22).
- `<constraints>`: the concrete bar o48_review_concrete_bar for a single-pass self-filtering review (O48-69, O48-70); a named verbosity requirement when the product fixes it (O48-08); the named verbosity symptom rather than a bare prohibition (O48-10); screenshot resolution within 2576px / 3.75MP for computer use (O48-76); o48_warm_tone here or in the tone position when a warmer register is wanted (O48-42). Scope sentences use the enumerated form, not a principle-level sentence.
- `<output_format>`: an explicit length or depth statement whenever the user's expectation differs from what the task's complexity would imply, and none otherwise (O48-07, BP-018); o48_conciseness only when the user or the product fixes the verbosity (O48-08, O48-09); a description plus one example update when the user wants a particular update shape (O48-34); review output schema with confidence and severity fields (O48-66); exact schemas and field-level instructions for extraction and pipelines (O48-37); an explicit tone instruction when voice matters (O48-41).
- `<examples>`: positive examples of the wanted concision in place of negative verbosity rules (O48-10, O48-11); an example update line when the update shape is specified (O48-34); a short example passage when voice matters (O48-41).
- `<success_criteria>`: guide rules; review harness: coverage before ranking rather than a low finding count (O48-65); computer use: resolution and effort tested on the workload (O48-79); extraction: exact schema conformance (O48-37); migration: the effort sweep completed (O48-22); thinking steer: the latency and quality effect measured, not assumed (O48-24). Recall or F1 on a labelled subset validates the harness rather than any single invocation, so it is named as the maintainers' follow-up in the recap, together with a note when no labelled subset exists (O48-71).
- `<execution_guidance>`: no progress-cadence scaffolding (O48-32, O48-33). A subagent policy paragraph, o48_subagent_guidance for coding fan-out, because the model spawns fewer subagents by default (O48-43, O48-44, O48-45). A tool-usage paragraph naming each expected tool, when to call it, and why, whenever a tool is under-used or the task is freshness-sensitive, because reasoning is favoured over tool calls (O48-29, O48-31); more tool use otherwise comes from raising effort, not from a nudge (O48-30). The 64k output budget note when `xhigh` or `max` is recommended (O48-28). o48_low_effort_reasoning only when the user has pinned `low` on a multistep task (O48-21); o48_thinking_steer only when adaptive thinking is on and latency is the stated concern (O48-26). frontend_aesthetics_short in system-prompt position for frontend builds, paired with a concrete spec or the propose step (O48-55, O48-57), or "Invoke frontend-design before <step>" when that skill is loaded (O48-56, BP-342). Computer use: 1080p by default, 720p or 1366x768 when cost is a stated constraint (O48-77, O48-78). The guide's use_parallel_tool_calls, investigate_before_answering, and temp_file_cleanup apply as the taxonomy row requires; batch_nudge is not grafted.
- `<verification>`: filled per the guide with self_check_verify and concrete checks; Opus 4.8 has no exception, unlike Opus 5 where the tag is omitted (O5-43). Thinking steer: a step that measures latency and answer quality before and after `o48_thinking_steer`, because the page requires measuring the effect of any prompting change (O48-24). Computer use: the resolution and effort sweep (O48-79). Voice-sensitive writing: a comparison against the wanted voice (O48-41). Migration: the effort sweep with its measurement (O48-22).
- Closing lines: none specific to Opus 4.8.

Reasoning exhortations: hand-written reasoning plans are dropped and effort is recommended in the Target model item (O48-20, O48-27, BP-221); o48_low_effort_reasoning only when `low` is pinned (O48-21); o48_thinking_steer only when adaptive thinking is on and over-triggering is the problem (O48-26); the manual chain-of-thought pattern only when the caller cannot enable adaptive thinking (BP-225).

## When this is the TARGET model: remove or convert

Each conversion is recorded in the Changed line of the assumptions.

| Found in the raw request or pasted prompt | Action for an Opus 4.8 target | Basis |
|---|---|---|
| `thinking: {type: "enabled", budget_tokens: N}` | Remove; `thinking: {type: "adaptive"}` plus `output_config.effort`, `max_tokens` kept; warn about the 400 | BP-189, BP-208 to BP-212 |
| An assumption that thinking is on | Correct it: thinking is off unless the caller sets adaptive; say who has to set it | O48-23, BP-217 |
| `temperature`, `top_p`, `top_k` at non-default values | Do not assert a 400 as on Sonnet 5; flag them for the Opus 4.7 to Opus 5 migration guide and translate the intent into prompt text | O48-05, O48-06 |
| "raise temperature for variety" in a design brief | o48_propose_directions | O48-53, O48-54 |
| An effort level chosen for another model or another profile | Re-derive from this page: `xhigh` for coding and agentic, `high` floor for intelligence-sensitive; sweep on upgrade | O48-13, O48-22 |
| `xhigh` or `max` with no output budget stated | Add the 64k starting max output token budget | O48-28 |
| Stacked "think harder" phrases for shallow reasoning | Remove; recommend raising effort to `high` or `xhigh` | O48-20, O48-27 |
| Hand-written reasoning plans | Drop; recommend effort; numbered work steps whose order or completeness matters stay | O48-20, BP-221 |
| "After every 3 tool calls, summarize progress" and other forced cadences | Remove | O48-33 |
| "use your tools", "always search first", "if in doubt use X" | Replace with a targeted paragraph naming the tool, when, and why, or raise effort instead | O48-29, O48-30, O48-31 |
| "only report high-severity issues", "be conservative", "don't nitpick" in a finding-stage review prompt | Remove and add o48_review_coverage, or replace with o48_review_concrete_bar | O48-65, O48-66, O48-69 |
| "important", "significant" as a review bar | The concrete bar | O48-69, O48-70 |
| "be more thorough" added to recover review recall | Remove; the drop is a harness effect, so fix the reporting bar instead | O48-64 |
| "don't over-explain", "no fluff", "don't ramble" | A short positive example of the target answer shape | O48-10, O48-11 |
| A default length instruction inherited from another model | Remove unless the user or the deliverable fixes the verbosity | O48-07, O48-08 |
| A single-item instruction with implied breadth | Add the explicit scope clause "every X, not just the first" | O48-36, O48-38 |
| All-caps emphasis, "CRITICAL: you MUST" | Plain conditional wording; instruction following is literal | O48-35, BP-018, BP-162 |
| "don't use cream", "make it clean and minimal", or any generic negative aesthetic instruction | A concrete spec (palette hexes, type, radius, spacing, motion) or the propose-four-directions step | O48-49, O48-50, O48-52 |
| The guide's long frontend_aesthetics block, or another earlier-model anti-slop block | Trim to frontend_aesthetics_short plus the variety advice | O48-55, O48-57, BP-330 |
| A prompt that damps delegation ("never spawn subagents", o5_delegation_guidance carried from Opus 5) | Reverse the direction: this model spawns fewer subagents by default, so graft o48_subagent_guidance where fan-out helps | O48-43, O48-44, O48-45 |
| Requirements spread over several turns | Gather them into the one first-turn prompt; ask any unavoidable question at the end of that turn | O48-60, O48-62 |
| A last-turn assistant prefill or "start your answer with" | Convert to a direct instruction, a named output tag, or enumerated labels | BP-124 |
| An Opus 4.7-era prompt as a whole | Keep its substance; apply only this table and section 4 | O48-04 |
| Fable 5.1 default snippets (progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule) in a ported prompt | Remove; measured on Fable 5.1 | O48-32, section 4 |

## When this is the EXECUTING model: how the skill behaves in Steps 5-7

Applies when the model running the skill resolves to Opus 4.8 (the Reading line then reads "executing model: opus-4-8"). SKILL.md Steps 6 and 7 are written for Fable 5.1; where this page differs, this section governs the skill's own behaviour. The rearticulated prompt's content still follows the target profile.

- Narration cadence: an opening line, then natural updates during long traces; no per-batch update rule, because updates are already regular and higher quality (O48-32). The Fable 5.1 "one-line update before each tool batch" sentence in Step 6 does not apply, and no forced cadence is imposed on the skill's own run (O48-33).
- Final message shape: the Step 7 recap of three to eight lines, facts only (BP-089). Response length tracks judged complexity, so the recap is short for a lookup and longer for an analysis (O48-07); the Step 5 display budget is kept.
- Tone: direct, with minimal validation-forward phrasing and sparing emoji use, which is the model's default and matches Standing rule 12 (O48-40). No self-evaluation.
- Verification pass: Step 7 runs as written; Opus 4.8 has no exception, so the prompt keeps its `<verification>` tag and the skill runs each check with tools rather than asserting it. This is the opposite of the Opus 5 rule (O5-43).
- Literal reading: read the request literally, state assumptions instead of widening scope, and do not infer unrequested work; at `low` or `medium` effort the skill says when a sub-step was not asked for rather than doing it (O48-19, O48-35, O48-36). This matches Step 1d and Standing rule 7.
- Autonomy: once the rearticulated prompt is presented the skill continues through Steps 6 and 7 without pausing for approval, because the model is more autonomous than prior models and the prompt is fully specified (O48-60, O48-61). The exceptions are unchanged: a dry run, a `[confirm]` step, and a question only the user can answer.
- Subagent policy: the model spawns fewer subagents by default (O48-43), so small work is finished with direct tool calls, and delegation is a deliberate decision stated in the plan when fanning out across items or files (O48-44, O48-45). The guide's subagent_usage_policy governs the rest.
- Search behaviour and progress grounding: the model favours reasoning over tool calls (O48-29), so the skill deliberately reads every named file and searches before making claims about code or data instead of relying on inference (Standing rule 6, BP-316, BP-317). Progress text is factual and grounded in tool results, with no self-evaluation (BP-089).
- Formatting: guide defaults; formatting_in_chat_rule is measured on Fable 5.1 and is not applied to the skill's own output.
- Edit style: Standing rule 11 applies as skill behaviour; the targeted_edits snippet text is measured on Fable 5.1 and is not grafted.
- Last-paragraph check: Step 7 as written; the page is silent.
- Effort follow-up: if reasoning was shallow on a complex task, tell the user to raise effort to `high` or `xhigh` rather than re-prompting with "think harder" (O48-20, O48-27); for coding and agentic work suggest `xhigh` (O48-15); for intelligence-sensitive work that is not coding or agentic, name `high` as the minimum (O48-13, O48-16), and say that the page prints no default (O48-05); if the run is long and effort is `xhigh` or `max`, suggest a large output budget starting at 64k (O48-28); if more tool use is wanted, effort is the lever (O48-30).
- Thinking in session: whether adaptive thinking is on is the harness's setting, not something the skill can change from inside a prompt (O48-23). If thinking is off and the work needs reasoning, the skill says so and names the setting rather than padding the prompt with reasoning exhortations.
- Design work in-session: the propose-four-directions pick is a sanctioned turn-ending checkpoint (input only the user can provide); under an autonomous block the skill picks one direction, states it in the Reading line, and continues (O48-52, O48-54).
- Refusal handling: refusal stop details are routed to the migration guide (O48-05); guide default applies, which is to report a refusal plainly and not rephrase to evade it.
- Context handling: the page prints no context-awareness behaviour and no window size of its own (the 1M default is a migration-guide fact, O48-05); the guide's state-tracking and compaction rules apply unchanged, and BP-241 context awareness is not claimed for this model.
- Harness-injected blocks to skip in-session: none named on the page; the Fable 5.1 batch_nudge is not a default here.

## Snippets

IDs only; verbatim text lives in `references/snippet-library.md`. All measured on Claude Opus 4.8; texts shared verbatim with the Sonnet 5 page are one library entry with both IDs as aliases and "Measured on: Sonnet 5, Opus 4.8".

- o48_conciseness (O48-09; alias s5_conciseness) - `<output_format>`, only when the user or the product fixes the verbosity.
- o48_low_effort_reasoning (O48-21; alias s5_low_effort_multistep) - `<execution_guidance>`, only when `low` is pinned on a multistep task.
- o48_thinking_steer (O48-26) - `<execution_guidance>`, only when adaptive thinking is on and over-triggering is the reported problem; its text is fenced separately inside the library's `think_only_when_useful` entry, which lists o48_thinking_steer as an alias, because this text keeps its em dash where s5_thinking_trigger_guard has a comma and the guide has a hyphen (BP-207).
- o48_explicit_scope (O48-39; alias s5_explicit_scope) - a pattern adapted to the user's target set, in `<task>`, `<constraints>`, or `<output_format>`.
- o48_warm_tone (O48-42; alias s5_warm_tone) - role or tone position, only when warmth is requested.
- o48_subagent_guidance (O48-45) - `<execution_guidance>` for coding fan-out; Opus 4.8 only, and it encourages delegation because the default is fewer subagents, the opposite direction from o5_delegation_guidance.
- o48_aefrm_concrete_spec (O48-51; alias s5_design_concrete_spec_aefrm) - a template shape mirrored with the user's values; the AEFRM content is not grafted.
- o48_propose_directions (O48-54) - first step of `<task>` for open design briefs; its text is fenced separately inside the shared `s5_design_propose_directions / o48_propose_directions` entry, because this text keeps its em dash.
- frontend_aesthetics_short (O48-57; the page's rule list names it `frontend_aesthetics`, and the Sonnet 5 page prints the same block, S5-58) - system-prompt position for frontend builds; the guide's long block stays under `frontend_aesthetics` (BP-330).
- o48_review_coverage (O48-66; alias s5_code_review_coverage) - `<task>` of review prompts, with confidence and severity fields in `<output_format>`; also the text Opus 5 borrows for O5-12.
- o48_review_concrete_bar (O48-70; alias s5_code_review_concrete_bar) - `<constraints>` of single-pass self-filtering reviews.
- From the guide, applied here with no model exception: self_check_verify (BP-229, BP-230), use_parallel_tool_calls, investigate_before_answering, temp_file_cleanup, plain_text_math, no_preamble, quoting_sources_example, autonomy_safety_confirmation, general_purpose_solution, avoid_excessive_markdown_and_bullet_points for long-form prose (BP-110), reflect_after_tool_results for multistep tool use (BP-193, BP-204), and model_identity and model_string with the target's display name and string substituted (BP-082, BP-084). `minimize_overengineering` is grafted only with an `Assumed:` entry naming Opus 4.5 and Opus 4.6 as the models the guide names for that symptom (BP-300 to BP-302, BP-025).
- Not grafted on Opus 4.8: context_compaction_persistence and spend_entire_context on the strength of context awareness, which BP-241 states for Sonnet 5, Sonnet 4.6, Sonnet 4.5, and Haiku 4.5 and not for this model, whose 1M context default is a migration-guide fact (O48-05); spend_entire_context may still be grafted on multi-window work as a guide block that names no model (BP-261). Also not grafted: progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule (measured on Fable 5.1); the guide's long frontend_aesthetics (this page prints the short block); o5_* snippets, in particular o5_delegation_guidance, whose direction is reversed here (O48-43); f5_* snippets, including the memory blocks, even though memory is a named strength (O48-03), because their texts are measured on the Fable pages.

## Not covered by this page

The skill falls back to the main guide (`references/technique-catalog.md`) for: XML structure and tag order; role prompting; long-context ordering (BP-062); examples and multishot patterns; positive format control and the list exception; plain-text math; prefill migration (BP-124); parallel tool calls; hallucination controls; state tracking and compaction across context windows; autonomy and safety confirmations; subagent orchestration beyond the spawning-rate note (the page gives a rate and a toy policy, not an orchestration pattern); research structure; file-creation hygiene; the self-check verification instruction (no exception on Opus 4.8); memory-system technique (memory is named as a strength, O48-03, but no memory guidance is printed, so the Fable 5 memory snippets are not borrowed); vision technique (vision is a named strength with no technique printed).

The page prints no effort default, no sampling parameter behaviour, no context window size of its own, no mid-conversation system message rules, and no refusal or safeguard behaviour: all five are routed to the Opus 4.7 to Opus 5 migration guide, which the page says Opus 4.8 shares (O48-05, O48-06). It also prints no tokenizer figure (do not apply the Sonnet 5 scaling), no API model string (the string comes from the guide's migration example, BP-213), and no context-awareness claim (BP-241 names the Sonnet family, not this model). Cite the linked pages rather than asserting any of these.

Related pages (do not import their content; name them in the Target model item when a fact is needed):
- Migrating to Claude Opus 5 from Claude Opus 4.8, https://platform.claude.com/docs/en/models/opus-5/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5 (API changes when moving off Opus 4.8; O48-01).
- Migrating to Claude Opus 5 from Claude Opus 4.7, https://platform.claude.com/docs/en/models/opus-5/migration-guide#migrating-from-opus-47 (sampling parameters, effort default, 1M context default, mid-conversation system messages, refusal stop details, shared by Opus 4.8; O48-05, O48-06).
- Prompting best practices, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (the base layer; O48-02, BP-023).
- Effort, https://platform.claude.com/docs/en/build-with-claude/effort (O48-12).
- Adaptive thinking, https://platform.claude.com/docs/en/build-with-claude/thinking (O48-24, O48-25).
- frontend-design skill, https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md (the longer frontend guidance for earlier models; O48-56, BP-342).
- Browser use tool, https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool (O48-74); Computer use tool, https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool (O48-75).
- Prompting Claude Sonnet 5 (`references/models/sonnet-5.md`) for the shared snippet texts; Prompting Claude Opus 5 (`references/models/opus-5.md`), which takes this profile as its baseline (O5-05); Opus 4.7 and Opus 4.6 in `references/models/legacy-4x.md`, which use this profile by analogy (O48-04, BP-002).
