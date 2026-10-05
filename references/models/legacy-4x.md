# Claude Opus 4.7, Claude Opus 4.6, Claude Opus 4.5, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Haiku 4.5, and Claude Mythos Preview

Source page: none. These seven models have no dedicated prompting page, so this profile is built only from Prompting best practices, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (snapshot 2026-09-08), using every statement in that guide that names one of them. The guide's own model table lists five pages and none of them is for a model in this profile (BP-013), so there is no "the page says" layer here and nothing supersedes the guide.

How to read this file. Its rules are the guide's inline model mentions, so every ID is a `BP-nnn` entry in `references/technique-catalog.md`; no new ID space is introduced. Because the source is the guide rather than a page, the verbatim-quote bullet in section 3 reads "Guide says" instead of "Page says", which is the same slot and the same convention the sibling profiles use for their trailing guide rules. Section 3 is grouped by model rather than by guide section, because a statement about Opus 4.6 says nothing about Haiku 4.5 (BP-025). A statement that names several models therefore appears once per group, under the same BP ID, with the heading naming the model the group is about; the Rule and the quote are the catalog's in every copy. Sections 4 and 5 govern the content of a rearticulated prompt whose target model is one of these seven; section 6 governs the skill's own behaviour when one of them is the model running the skill. The two dimensions are resolved separately in SKILL.md Step 1a. This whole profile is applied by analogy, and section 8 says what that costs.

## Identity and API facts

- Profile: `legacy-4x`. Aliases: opus-4.7, opus-4.6, opus-4.5, sonnet-4.6, sonnet-4.5, haiku-4.5, mythos-preview, and their `claude-*` forms (alias table in `references/model-notes.md`).
- Covered set: split. Opus 4.7, Opus 4.6, Sonnet 4.6, and Haiku 4.5 are inside the guide's thirteen current models; Opus 4.5, Sonnet 4.5, and Mythos Preview are outside it (BP-002). The split is the tier: tier A is a current model with no page of its own, tier B is a model outside the thirteen, for which the guide is applied by analogy and the Step 4 migration checklist runs.
- Baseline: none (guide only). Page basis: not applicable; the guide's inline mentions and its Migration considerations are the whole basis (BP-002, BP-005).
- API model strings: the guide prints exactly one, `claude-sonnet-4-5-20250929`, as the before-migration model in its extended-thinking-to-adaptive example (BP-213). No string is printed for the other six; cite the models overview, https://platform.claude.com/docs/en/models/overview, rather than asserting one.
- Thinking, `budget_tokens`, and prefill, per model:

| Model | In the thirteen | Thinking | `budget_tokens` | Last-turn prefill | Closest page for analogy |
|---|---|---|---|---|---|
| Opus 4.7 | Yes (tier A) | Adaptive; off when the `thinking` parameter is omitted (BP-217, BP-194) | 400 error (BP-189) | Unsupported (BP-124) | `opus-4-8`, by reverse analogy of "performs well out of the box on existing Claude Opus 4.7 prompts" (O48-04) |
| Opus 4.6 | Yes (tier A) | Adaptive; off when omitted (BP-217, BP-194) | Still functional but deprecated (BP-188) | Unsupported (BP-124) | `opus-4-8` by analogy, plus this model's own guide blocks |
| Opus 4.5 | No (tier B) | Pre-4.6: manual extended thinking with `budget_tokens` (BP-201) | Supported (BP-201) | Supported (BP-128) | Guide only |
| Sonnet 4.6 | Yes (tier A) | Adaptive; off when omitted (BP-217, BP-194) | Still functional but deprecated (BP-188) | Unsupported (BP-124) | `sonnet-5`, by reverse reading of "Differences from Claude Sonnet 4.6" (BP-016), plus the Sonnet 4.6 facts that page prints (`sonnet-5`, section 2) |
| Sonnet 4.5 | No (tier B) | Pre-4.6: manual extended thinking with `budget_tokens` (BP-201) | Supported (BP-201) | Supported (BP-128) | Guide only, plus the Sonnet 5 migration link (BP-361) |
| Haiku 4.5 | Yes (tier A) | Not printed. Derived: not 4.6 or later, so not adaptive (BP-194); the guide's "older models" sentence is read as covering it (BP-201). Assumed, recorded in the Reading line; confirm against the per-model configuration table (BP-202) | Not printed. Same derivation as the thinking cell; cite the per-model configuration table rather than asserting the shape (BP-201, BP-202) | Supported (BP-128) | Guide only, plus the Sonnet 5 migration link (BP-361) |
| Mythos Preview | No (tier B) | Adaptive (BP-194) | Not printed; do not assert | Unsupported, 400 error (BP-124, BP-126, BP-352) | Guide only; limited availability |

- How to set thinking: adaptive thinking is `thinking: {type: "adaptive"}` with no budget field, and effort is set through the top-level `output_config` object rather than inside `thinking` (BP-209, BP-210, BP-347); the `thinking: {type: "adaptive"}` syntax itself is BP-348. On Opus 4.6, Opus 4.7, and Sonnet 4.6 the caller must set it, because omitting the parameter runs the request without thinking (BP-217). The legacy shape `thinking: {type: "enabled", budget_tokens: N}` is the pre-4.6 configuration and is what Opus 4.5, Sonnet 4.5, and Haiku 4.5 accept (BP-201). When a request never used extended thinking, no thinking change is made (BP-216).
- Sampling parameters (`temperature`, `top_p`, `top_k`): Sonnet 4.6 accepts them, because the 400 on a non-default value is "new for Sonnet-class models" on Sonnet 5 (S5-49); by the same sentence the pre-4.6 models keep them too. Nothing is printed for the Opus models in this profile; flag a sampling parameter as "check against the migration guide" rather than asserting a value.
- Effort default and recommended sweep: printed for one model only. Sonnet 4.6 defaults to `high`, the same default as Sonnet 5, and `max` is available on it (S5-11, S5-18). For the others the guide prints no default and no level list; the effort page lists per-model availability (BP-191). Effort is profile-local and is never carried across: a Sonnet 4.6 level moving to Sonnet 5 maps one step down (4.6 `high` to 5 `medium`, 4.6 `max` to 5 `high`) and comparisons are paired by observed thinking length rather than by level name (S5-18, S5-19). Effort is also the fallback knob when prompt tuning has not curbed over-aggressive behaviour on Opus 4.6 (BP-184, BP-186).
- `max_tokens` headroom: no per-model ceiling is printed. Under adaptive thinking `max_tokens` is the hard output limit and the preferred cost cap after effort (BP-190), and it stays in the request unchanged when a thinking configuration is migrated (BP-212).
- Context window: no size is printed for any of the seven. What is printed is context awareness: Sonnet 4.6, Sonnet 4.5, and Haiku 4.5 track their remaining token budget through a conversation (BP-241, BP-242, BP-243). The Opus models in this profile and Mythos Preview are not named as context-aware; do not claim they are.
- Tokenizer: not printed. The approximately 30 percent figure belongs to the Sonnet 5 tokenizer (S5-33) and is a reason to scale a budget up when moving to Sonnet 5, not a fact about these models.
- Refusal and safeguard behaviour: not printed for any of the seven. The guide's refusal facts (`stop_reason: "refusal"`, the `reasoning_extraction` category, documented fallback) come from the Fable pages and are measured there (F5-09 to F5-11, F5-71, F51-127). Report a refusal plainly and do not rephrase a prompt to defeat a warranted one (BP-138).
- Prefill support: the boundary runs through this profile. Opus 4.7, Opus 4.6, Sonnet 4.6, and Mythos Preview reject a prefilled last assistant turn with a 400; Opus 4.5, Sonnet 4.5, and Haiku 4.5 still accept one (BP-124, BP-126, BP-128, BP-352). An assistant message anywhere other than the last turn is unaffected on every model (BP-128).
- Vision: Opus 4.5 and Opus 4.6 have improved vision over earlier Claude models, including multi-image contexts and screenshot or UI interpretation, and video handled as extracted frames (BP-318 to BP-321). Nothing is printed for the Sonnet and Haiku models here.

### Harness and environment notes

These facts reach a rearticulated prompt only through the taxonomy rows for harness authoring and prompt authoring for another model; in an interactive session the skill informs the user instead of trying to set them from inside a prompt.

- Append-only history applies on every current model: pass each assistant turn back exactly as the API returned it, thinking blocks included (BP-356). Per-turn reminders belong in turn-scoped system messages and instruction changes in mid-conversation system messages (BP-358). The Fable 5.1 error on modifying the conversation before a thinking block is measured on Fable 5.1 and is not asserted here (BP-357).
- Compacting harnesses: when the harness compacts context or saves context to external files, say so in the prompt so the model can behave accordingly (BP-244). This matters most on the three context-aware models in this profile, which would otherwise sometimes wrap up work as the limit approaches (BP-245).
- The memory tool pairs with context awareness for managing context transitions (BP-247); when a memory directory or memory tool exists, the prompt names it as the place to save progress before a refresh.
- Verification tools for long autonomous runs (computer use, browser use, a browser automation MCP server) are the guide's answer to correctness without continuous human feedback (BP-257 to BP-259). The computer-use and browser-use toolset strings the skill holds are measured on Sonnet 5 and Opus 4.8 (S5-71 to S5-77, O48-72 to O48-79); do not attach them to a model in this profile.

## Behavioural deltas

One entry per guide statement that names a model in this profile, grouped by model rather than by guide section. The quote bullet reads "Guide says" because there is no page. Sample prompts are quoted in part here; the verbatim text lives in `references/snippet-library.md` under the snippet ID given.

Group: the guide's frame for all seven

### BP-002 Four of the seven are inside the guide's thirteen
- Kind: fact
- Rule: Treat the guide as authoritative for exactly these thirteen current models and route any other model to the migration considerations.
- Guide says: "This is the reference for prompt engineering with current Claude models, including Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, and Claude Haiku 4.5."
- Applies when: Resolving the tier for a target in this profile.
- Skill applies it by: Opus 4.7, Opus 4.6, Sonnet 4.6, and Haiku 4.5 are tier A and the Reading line reads `Target model: <name> (legacy-4x tier A: current, no page, closest page <x> by analogy)`; Opus 4.5, Sonnet 4.5, and Mythos Preview are tier B and it reads `Target model: <name> (legacy-4x tier B: outside the guide's thirteen; guide applied by analogy, migration checklist run)`. Haiku 4.5 is the third form, because 6c documents no closest page for it: `Target model: Haiku 4.5 (legacy-4x tier A: current, no page, guide applied directly, no closest page documented)`.

### BP-013 There is no page to read first
- Kind: technique
- Rule: Read the prompting page for the target model first, then apply the general techniques.
- Guide says: "Each of these models has its own prompting page. Read the one for your model first, then the techniques that follow."
- Applies when: Every rearticulation whose target is one of these seven.
- Skill applies it by: The sentence cannot be followed literally here, because the guide's table names no page for any of the seven. This file stands in its place, and the closest page named in section 2 is read next for orientation only: its facts are read, none of its page-measured snippet text is grafted (BP-025, section 4), and what the reading changes is which of the guide's own blocks the skill selects. The analogy and that limit are both recorded in the Reading line. Haiku 4.5 has no closest page at all, so its Reading line says the guide is applied directly.

### BP-016 The Sonnet 5 row names Sonnet 4.6 as its baseline
- Kind: model-note
- Rule: For Sonnet 5, set response length, effort and thinking depth, tool-use trigger conditions, literal instruction following, and design and frontend defaults explicitly.
- Guide says: "| Claude Sonnet 5 | [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5) | Differences from Claude Sonnet 4.6: response length, effort and thinking-depth calibration, tool use triggering, literal instruction following, and design and frontend defaults. |"
- Applies when: The target is Sonnet 4.6, where this row is the only structured statement the guide makes about how Sonnet 4.6 differs from a model that has a page.
- Skill applies it by: Read in reverse, this row names the five axes on which Sonnet 4.6 differs from Sonnet 5: response length, effort and thinking-depth calibration, tool use triggering, literal instruction following, and design and frontend defaults. On those five axes a Sonnet 5 delta is a Sonnet 4.6 baseline, so an `s5_*` snippet written to correct Sonnet 5 behaviour is not grafted onto Sonnet 4.6 (BP-025); the sentences the skill writes itself on those axes are stated explicitly rather than left to a default, and the analogy is recorded in the Reading line.

### BP-025 A model-named technique is measured on that model
- Kind: technique
- Rule: When a technique is stated for a named model, apply it only to that model unless evals confirm it transfers.
- Guide says: "Where a technique names a specific model, treat it as measured on that model and re-check it against your own evals before applying it to another."
- Applies when: Every graft in this profile, and every use of a page-measured snippet on a target in it.
- Skill applies it by: Section 3 is grouped per model so an Opus 4.6 rule is never applied to Haiku 4.5 silently; when a rule is extended across models the Assumed line says so. No `f5_*`, `f51`-measured, `o5_*`, `s5_*`, or `o48_*` snippet is grafted onto one of these targets without that entry.

### BP-005 Migration considerations apply only to ported prompts
- Kind: fact
- Rule: Apply migration considerations only to prompts that were written for an earlier model generation.
- Guide says: "**Migration considerations** last, for prompts moving from earlier generations."
- Applies when: The raw request contains a pasted prompt, names an older model, or asks to port a prompt.
- Skill applies it by: Step 4's migration checklist runs for a tier B target as a matter of course, and for a tier A target only on those triggers. A fresh request written for Opus 4.6 today needs no migration pass.

Group: Claude Opus 4.6

### BP-160 Responds more strongly to the system prompt (with Opus 4.5)
- Kind: model-note
- Rule: Expect Claude Opus 4.5 and Claude Opus 4.6 to respond more strongly to the system prompt than previous models.
- Guide says: "Claude Opus 4.5 and Claude Opus 4.6 are also more responsive to the system prompt than previous models."
- Applies when: Running or rearticulating prompts for Opus 4.5 or Opus 4.6.
- Skill applies it by: System-prompt text is kept short and plainly worded for these two targets, because every added directive lands harder; emphasis is dropped rather than added.

### BP-161 Prompts written against undertriggering now overtrigger
- Kind: anti-pattern
- Rule: Watch for tool and skill overtriggering when reusing prompts that were written to reduce undertriggering.
- Guide says: "If your prompts were designed to reduce undertriggering on tools or skills, these models may now overtrigger."
- Applies when: A pasted or inherited prompt carries forceful tool-use or skill-use directives and the target is Opus 4.5 or Opus 4.6.
- Skill applies it by: Step 4 treats every emphatic tool mandate in the paste as a strip candidate and records the removal in the Changed line.

### BP-162 Dial back aggressive language
- Kind: migration
- Rule: Fix overtriggering by dialing back aggressive language in the prompt.
- Guide says: "The fix is to dial back any aggressive language."
- Applies when: Migrating a prompt to Opus 4.5 or Opus 4.6 that overtriggers tools or skills.
- Skill applies it by: All-caps emphasis, "CRITICAL", "you MUST", and intensifiers become plain conditional wording; this is the same conversion the skill applies everywhere, and on these two targets it is mandatory rather than stylistic.

### BP-163 Phrasing pattern: "Use this tool when..."
- Kind: sample-prompt
- Rule: Replace "CRITICAL: You MUST use this tool when..." with the plain form "Use this tool when...".
- Guide says: see snippet use_this_tool_when, quoted as "Where you might have said \"CRITICAL: You MUST use this tool when...\", you can use more normal prompting like \"Use this tool when...\"."
- Applies when: A tool mandate has to be rewritten for one of these targets.
- Skill applies it by: A phrasing pattern rather than a grafted block: the tool name and the trigger condition are substituted into the plain form inside `<execution_guidance>`.

### BP-177 More upfront exploration, especially at higher effort
- Kind: model-note
- Rule: Expect Claude Opus 4.6 to do more upfront exploration than earlier models, especially at higher effort settings, and tune thoroughness guidance down rather than up.
- Guide says: "Claude Opus 4.6 does more upfront exploration than previous models, especially at higher [`effort`](https://platform.claude.com/docs/en/build-with-claude/effort) settings."
- Applies when: The target is Opus 4.6, or the raw request carries a prompt written for an older model that needed encouragement to investigate.
- Skill applies it by: No blanket "be thorough" or "explore extensively" text; the depth of investigation the task actually needs is stated inside `<task>` or `<execution_guidance>`.

### BP-178 Bound unprompted context gathering
- Kind: model-note
- Rule: Treat unprompted context gathering and multi-thread research as a known Opus 4.6 tendency that the prompt should bound, not amplify.
- Guide says: "This initial work often helps to optimize the final results, but the model may gather extensive context or pursue multiple threads of research without being prompted."
- Applies when: Any Opus 4.6 task where investigation scope creep costs tokens or time.
- Skill applies it by: `<constraints>` or `<execution_guidance>` bounds investigation, for example "read the files named in the task; widen only if they do not answer the question".

### BP-179 Tune existing thoroughness boosters
- Kind: technique
- Rule: If an existing prompt encouraged the model to be more thorough, tune that guidance for Claude Opus 4.6.
- Guide says: "If your prompts previously encouraged the model to be more thorough, you should tune that guidance for Claude Opus 4.6:"
- Applies when: A pasted prompt written for a pre-4.6 model contains thoroughness boosters and the target is Opus 4.6.
- Skill applies it by: The three sub-rules that follow it (BP-180, BP-182, BP-184) are applied in order and each change is recorded in the Changed line.

### BP-180 Targeted instructions instead of blanket defaults
- Kind: technique
- Rule: Replace blanket tool-use defaults with targeted trigger conditions tied to a benefit.
- Guide says: "**Replace blanket defaults with more targeted instructions.** Instead of \"Default to using \[tool],\" add guidance like \"Use \[tool] when it would enhance your understanding of the problem.\""
- Applies when: The raw request or paste contains "Default to using X" or an equivalent standing instruction.
- Skill applies it by: Converts to "Use X when it would <benefit>" in `<execution_guidance>`, naming the benefit from context.

### BP-181 Phrasing pattern: targeted tool trigger
- Kind: sample-prompt
- Rule: Phrase tool-use guidance as a condition attached to a concrete benefit.
- Guide says: see snippet targeted_tool_trigger, quoted as "Use [tool] when it would enhance your understanding of the problem."
- Applies when: Writing any tool-use guidance for a target in this profile.
- Skill applies it by: A phrasing pattern rather than a grafted block; the tool name and the benefit are the user's own.

### BP-182 Remove catch-all triggers
- Kind: anti-pattern
- Rule: Remove over-prompting such as "If in doubt, use [tool]" because it causes overtriggering on current models.
- Guide says: "**Remove over-prompting.** Tools that undertriggered in previous models are likely to trigger appropriately now. Instructions like \"If in doubt, use \[tool]\" will cause overtriggering."
- Applies when: The raw request or paste contains "if in doubt", "always", or "default to" attached to a tool.
- Skill applies it by: Step 4 strips the catch-all and substitutes the targeted trigger from BP-181.

### BP-183 Tools trigger appropriately now
- Kind: fact
- Rule: Assume tools that undertriggered on older models now trigger appropriately without extra nudging.
- Guide says: "Tools that undertriggered in previous models are likely to trigger appropriately now."
- Applies when: Deciding whether a tool nudge is needed at all.
- Skill applies it by: The default is no nudge; a nudge is written only when the raw request reports an actual under-use.

### BP-184 Effort is the fallback knob
- Kind: technique
- Rule: Use a lower effort setting as the fallback when Claude stays overly aggressive after prompt tuning.
- Guide says: "**Use effort as a fallback.** If Claude continues to be overly aggressive, use a lower setting for `effort`."
- Applies when: Prompt-level tuning has not curbed excessive exploration or tool use and the caller controls the API request.
- Skill applies it by: Recommends a lower effort in the Target model item instead of writing more prompt text to emulate restraint; the skill cannot set effort from inside a prompt.

### BP-185 May think extensively
- Kind: model-note
- Rule: Expect Opus 4.6 to sometimes think extensively, which inflates thinking tokens and slows responses.
- Guide says: "In some cases, Claude Opus 4.6 may think extensively, which can inflate thinking tokens and slow down responses."
- Applies when: Latency or token cost matters and the target is Opus 4.6.
- Skill applies it by: The Target model item names the symptom and the two remedies; when the request stresses speed or cost, commit_to_approach goes into `<execution_guidance>`.

### BP-186 Constrain reasoning or lower effort
- Kind: technique
- Rule: When extensive thinking is undesirable, add explicit instructions that constrain reasoning, or lower effort to cut thinking and token usage.
- Guide says: "If this behavior is undesirable, you can add explicit instructions to constrain its reasoning, or you can lower the `effort` setting to reduce overall thinking and token usage."
- Applies when: Visible overthinking on an Opus 4.6 target.
- Skill applies it by: Order of remedies: the effort dial first in the Target model item, then commit_to_approach as the prompt-side constraint.

### BP-187 Sample: commit_to_approach
- Kind: sample-prompt
- Rule: Instruct the model to choose an approach, commit to it, and revisit only on directly contradicting new information.
- Guide says: see snippet commit_to_approach; the block opens "When you're deciding how to approach a problem, choose an approach and commit to it." and closes "You can always course-correct later if the chosen approach fails."
- Applies when: An Opus 4.6 target where latency or thinking cost is a stated concern.
- Skill applies it by: Grafts verbatim into `<execution_guidance>`; not a default, because upfront exploration usually improves the result (BP-178).

### BP-269 May take hard-to-reverse actions without guidance
- Kind: model-note
- Rule: Know that, without guidance, Claude Opus 4.6 may take hard-to-reverse or shared-system actions such as deleting files, force-pushing, or posting to external services.
- Guide says: "Without guidance, Claude Opus 4.6 may take actions that are difficult to reverse or affect shared systems, such as deleting files, force-pushing, or posting to external services."
- Applies when: Authoring a prompt for Opus 4.6, or any agentic task in this profile with destructive or externally visible side effects.
- Skill applies it by: The Step 1f side-effect scan is mandatory for an Opus 4.6 target rather than conditional, and autonomy_safety_confirmation is grafted whether or not the scan fires.

### BP-270 Confirm before risky actions
- Kind: technique
- Rule: To make Claude confirm before potentially risky actions, add explicit reversibility and impact guidance to the prompt.
- Guide says: "If you want Claude Opus 4.6 to confirm before taking potentially risky actions, add guidance to your prompt:"
- Applies when: Agentic tasks that could touch shared systems or perform destructive operations.
- Skill applies it by: Each flagged step is written in `<task>` with the `[confirm]` marker, the list is repeated in the Reading line, and the block below goes into `<execution_guidance>`.

### BP-271 Sample: autonomy_safety_confirmation
- Kind: sample-prompt
- Rule: Use this prompt block to have Claude weigh reversibility and impact, take local reversible actions freely, ask before destructive or shared-system actions, and never use destructive actions as a shortcut.
- Guide says: see snippet autonomy_safety_confirmation; the block opens "Consider the reversibility and potential impact of your actions." and closes "don't bypass safety checks (e.g. --no-verify) or discard unfamiliar files that may be in-progress work."
- Applies when: Opus 4.6 targets always; other targets in this profile when the side-effect signal fires. The catalog records it as measured on Opus 4.6 and applied to all models as a precaution.
- Skill applies it by: Grafted verbatim with its wrapper into `<execution_guidance>`; it is also the source of SKILL.md Standing rules 1 and 2, so the skill's own behaviour already matches it.

### BP-286 Strong predilection for subagents
- Kind: model-note
- Rule: Watch for subagent overuse: Claude Opus 4.6 has a strong predilection for subagents and may spawn them when a direct approach such as a grep call would be faster and sufficient.
- Guide says: "**Watch for overuse:** Claude Opus 4.6 has a strong predilection for subagents and may spawn them in situations where a simpler, direct approach would suffice. For example, the model may spawn subagents for code exploration when a direct grep call is faster and sufficient."
- Applies when: Authoring for Opus 4.6, or observing excessive subagent spawning.
- Skill applies it by: subagent_usage_policy is mandatory for an Opus 4.6 target, not conditional on the agentic row; the guide's own example (code exploration versus a direct grep) is named in `<execution_guidance>` when the task involves searching a codebase.

### BP-289 Add explicit subagent guidance when overuse appears
- Kind: technique
- Rule: If subagent use is excessive, add explicit guidance about when subagents are and are not warranted.
- Guide says: "If you're seeing excessive subagent use, add explicit guidance about when subagents are and aren't warranted:"
- Applies when: Observed or expected subagent overuse, which for Opus 4.6 is expected by default (BP-286).
- Skill applies it by: The block below is grafted; hand-written delegation choreography in the raw request is stripped and replaced by it.

### BP-290 Sample: subagent_usage_policy
- Kind: sample-prompt
- Rule: Use this prompt block to reserve subagents for parallel, isolated, or independent workstreams and to work directly for simple, sequential, single-file, or context-dependent tasks.
- Guide says: see snippet subagent_usage_policy; the block opens "Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams that don't need to share state." and closes "work directly rather than delegating."
- Applies when: Opus 4.6 targets always; other targets in this profile when delegation is possible.
- Skill applies it by: Grafted verbatim into `<execution_guidance>`; execution applies the same test before spawning any subagent.

Group: Claude Opus 4.7

Also relevant: BP-002 (inside the thirteen, no page), BP-189 (`budget_tokens` returns a 400 on Claude 4.7 and later), BP-217 (thinking off when the parameter is omitted, stated as Opus 4.6 through Opus 4.8), BP-194 (adaptive thinking), BP-124 and BP-126 (no last-turn prefill, stated as starting with Claude 4.6 models). The guide makes no behavioural statement about this model; its behavioural layer is section 4 paragraph 1, by analogy with `opus-4-8` (O48-04) with the assumption recorded.

Group: Claude Opus 4.5 and Claude Opus 4.6 together

### BP-300 Both tend to overengineer
- Kind: model-note
- Rule: Know that Claude Opus 4.5 and Claude Opus 4.6 tend to overengineer by creating extra files, adding unnecessary abstractions, or building in unrequested flexibility.
- Guide says: "Claude Opus 4.5 and Claude Opus 4.6 have a tendency to overengineer by creating extra files, adding unnecessary abstractions, or building in flexibility that wasn't requested."
- Applies when: Authoring for Opus 4.5 or Opus 4.6, or any code-change request in this profile where scope creep is a risk.
- Skill applies it by: `<success_criteria>` always carries "files created or modified: only <the files named in task>", and the block below goes into `<constraints>` for these two targets regardless of task size.

### BP-301 Keep solutions minimal
- Kind: technique
- Rule: If overengineering appears, add specific guidance to keep solutions minimal.
- Guide says: "If you're seeing this undesired behavior, add specific guidance to keep solutions minimal."
- Applies when: Code-change requests for Opus 4.5 or Opus 4.6, especially bug fixes and small features.
- Skill applies it by: minimize_overengineering in `<constraints>`; the skill's own scope sentence stays positive with a because clause, and the grafted guide block keeps its negative wording as quoted.

### BP-302 Sample: minimize_overengineering
- Kind: sample-prompt
- Rule: Use this prompt block to constrain scope, documentation, defensive coding, and abstractions to the minimum needed for the current task.
- Guide says: see snippet minimize_overengineering; the block opens "Avoid over-engineering. Only make changes that are directly requested or clearly necessary." and covers Scope, Documentation, Defensive coding, and Abstractions, closing "The right amount of complexity is the minimum needed for the current task."
- Applies when: Code-change requests targeting Opus 4.5 or Opus 4.6.
- Skill applies it by: Grafted verbatim into `<constraints>` inside its own tag and not rewritten into positive form (BP-302's own note: the positive-framing rule governs sentences the skill writes, not guide text it quotes).

### BP-318 Improved vision
- Kind: fact
- Rule: Assume Claude Opus 4.5 and Claude Opus 4.6 (and later models) have stronger vision than earlier Claude models when planning image work.
- Guide says: "Claude Opus 4.5 and Claude Opus 4.6 have improved vision capabilities compared to previous Claude models."
- Applies when: The request involves images, screenshots, or other visual inputs on these two targets.
- Skill applies it by: The image task is stated directly with no hedges or workarounds for weak vision; legacy "describe what you can make out" phrasing is removed.

### BP-319 Several images in one pass
- Kind: fact
- Rule: Keep multiple related images together in one context when the task is image processing or data extraction.
- Guide says: "They perform better on image processing and data extraction tasks, particularly when there are multiple images present in context."
- Applies when: A vision or extraction task with more than one image.
- Skill applies it by: `<documents>` carries the whole image set in one turn rather than one image per turn.

### BP-320 Screenshots and UI elements read directly
- Kind: fact
- Rule: For screenshot and UI interpretation tasks, ask the model to read the UI elements directly from the screenshot.
- Guide says: "These improvements carry over to computer use, where the models can more reliably interpret screenshots and UI elements."
- Applies when: Computer-use or screenshot-reading tasks on these two targets.
- Skill applies it by: `<task>` names the element to read rather than asking for a general description first.

### BP-321 Video as frames
- Kind: technique
- Rule: Analyze video by splitting it into frames and treating the frames as images.
- Guide says: "You can also use these models to analyze videos by breaking them up into frames."
- Applies when: The raw request supplies video.
- Skill applies it by: `<task>` gets an explicit frame-extraction step before the analysis step.

### BP-322 Crop or zoom tool
- Kind: technique
- Rule: Give the model a crop or zoom tool, or an agent skill that provides one, when fine image detail matters.
- Guide says: "One technique that has proven effective to further boost performance is to give Claude a crop tool or [agent skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)."
- Applies when: Image analysis where small regions, small text, or dense data matter (charts, tables, documents, dense screenshots).
- Skill applies it by: Default-on instruction for detail-sensitive image requests on these targets: crop and enlarge the relevant region with Python PIL or OpenCV via Bash and re-read it before answering, iterating analyze, crop, verify. The Fable 5.1 version of this advice is F51-149 and is not borrowed here.

### BP-323 Measured uplift from zooming
- Kind: fact
- Rule: Expect measurable accuracy gains from letting the model zoom into relevant image regions.
- Guide says: "Testing has shown consistent uplift on image evaluations when Claude is able to \"zoom\" in on relevant regions of an image."
- Applies when: Justifying the crop step in `<execution_guidance>` or `<verification>`.
- Skill applies it by: The crop step is stated as a required step, not an optional one, on detail-sensitive image work.

### BP-326 Both build complex real-world web applications
- Kind: fact
- Rule: Treat Opus 4.5 and Opus 4.6 as capable of building complex, real-world web applications with strong frontend design.
- Guide says: "Claude Opus 4.5 and Claude Opus 4.6 build complex, real-world web applications with strong frontend design."
- Applies when: The request is to build or restyle a web frontend or full web application.
- Skill applies it by: The ask is not scaled down to a toy or a stub; the full application the user described is requested, with richness modifiers on the ambition word (BP-344, BP-345).

### BP-327 Never leave frontend design unguided
- Kind: anti-pattern
- Rule: Never leave frontend design unguided, because the model defaults to the generic "AI slop" aesthetic.
- Guide says: "However, without guidance, models can default to generic patterns that create what users call the \"AI slop\" aesthetic. To create distinctive, creative frontends that surprise and delight:"
- Applies when: Any request that produces UI, a web page, a dashboard, or a styled component.
- Skill applies it by: The frontend row always injects design guidance for these targets: frontend_aesthetics as a system-style section before the task instructions, or "Invoke frontend-design before <step>" in `<execution_guidance>` when that skill is loaded (BP-342).

### BP-330 Sample: frontend_aesthetics, the long block
- Kind: sample-prompt
- Rule: Insert the frontend_aesthetics system prompt snippet whenever the task builds or restyles a frontend.
- Guide says: see snippet frontend_aesthetics; the block opens "<frontend_aesthetics> You tend to converge toward generic, \"on distribution\" outputs. In frontend design, this creates what users call the \"AI slop\" aesthetic." and closes "Avoid this: it is critical that you think outside the box!"
- Applies when: Frontend, UI, web page, dashboard, or component generation or restyling on a target in this profile.
- Skill applies it by: This profile takes the long block, which is the version the guide prints in full for Opus 4.5 and Opus 4.6, not the short `frontend_aesthetics_short` block that the Sonnet 5 and Opus 4.8 pages print. It is grafted verbatim with its wrapper as a system-style section before the task instructions. Its bullets carry the rest of the guide's frontend advice: typography (BP-332), cohesive colour with CSS variables (BP-333), motion at high-impact moments (BP-334), layered backgrounds (BP-335), the four generic-aesthetic prohibitions (BP-336 to BP-339), varying themes and fonts (BP-340), and the residual convergence on Space Grotesk (BP-341). Deeper treatment: the frontend design blog post (BP-328) and Claude Design for interactive non-API work (BP-329).

Group: Claude Opus 4.5 only

### BP-235 Sensitive to the word "think" when thinking is disabled
- Kind: model-note
- Rule: When extended thinking is disabled on Claude Opus 4.5, avoid the word "think" and its variants because the model is particularly sensitive to them.
- Guide says: "When extended thinking is disabled, Claude Opus 4.5 is particularly sensitive to the word \"think\" and its variants. Consider using alternatives like \"consider,\" \"evaluate,\" or \"reason through\" in those cases."
- Applies when: Prompt authoring for Opus 4.5 with extended thinking disabled. The condition matters: with thinking on, "think" is used freely.
- Skill applies it by: For that target and that condition only, the finished prompt is scanned for "think", "thinking", and "think through" before it is shown.

### BP-236 Substitute consider, evaluate, reason through
- Kind: anti-pattern
- Rule: Convert "think" and its variants to "consider", "evaluate", or "reason through" when the target is Opus 4.5 with thinking disabled.
- Guide says: "Consider using alternatives like \"consider,\" \"evaluate,\" or \"reason through\" in those cases."
- Applies when: Step 4 on a prompt whose target is Opus 4.5 running with extended thinking disabled.
- Skill applies it by: The substitution is made and recorded in the Changed line; the guide's think_thoroughly line is not grafted for that target (BP-222 excludes it explicitly), and the manual chain-of-thought fallback (BP-225) is phrased with "reason through" instead of "think through".

Group: thinking configuration across the family

### BP-194 Adaptive thinking on 4.6 and later and on Mythos Preview
- Kind: fact
- Rule: Treat Claude 4.6 and later models and Claude Mythos Preview as adaptive-thinking models where Claude decides when and how much to think.
- Guide says: "Claude 4.6 and later models and Claude Mythos Preview use [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) (`thinking: {type: \"adaptive\"}`), where Claude dynamically decides when and how much to think."
- Applies when: Determining the thinking configuration for Opus 4.7, Opus 4.6, Sonnet 4.6, or Mythos Preview.
- Skill applies it by: The Target model item prints `thinking: {type: "adaptive"}` for these four and pairs it with an effort setting in `output_config`; no manual reasoning choreography is written on top of it.

### BP-217 Thinking is off when the parameter is omitted
- Kind: model-note
- Rule: On Claude Opus 4.6 through Opus 4.8 and Sonnet 4.6, thinking is off when the thinking parameter is omitted.
- Guide says: "On Claude Opus 4.6 through Claude Opus 4.8 and Claude Sonnet 4.6, thinking is off when you omit the `thinking` parameter."
- Applies when: Authoring a prompt or an API request for Opus 4.6, Opus 4.7, or Sonnet 4.6.
- Skill applies it by: The Target model item says the caller must set `thinking: {type: "adaptive"}` explicitly, because omitting it runs the request with no thinking at all. This is the opposite default from Opus 5 and Sonnet 5 (BP-218) and from the always-on Fable family (BP-220), so a prompt ported from either direction gets the thinking line rewritten. When the task needs reasoning and thinking must stay off, the manual fallback below applies.

### BP-225 Manual chain of thought as the fallback when thinking is off
- Kind: technique
- Rule: When thinking is off, ask Claude to think through the problem step by step as a manual chain-of-thought fallback.
- Guide says: "**Manual chain-of-thought (CoT) prompting as a fallback.** When thinking is off, you can still encourage step-by-step reasoning by asking Claude to think through the problem."
- Applies when: A target in this profile runs with thinking off, whether because it was omitted on a 4.6-class model or because a pre-4.6 model has no thinking budget set.
- Skill applies it by: Adds a step-by-step reasoning request, with the final answer in `<answer>` tags so a parser can extract it (BP-226). The `<thinking>` half of that pairing was withdrawn by the guide. On Opus 4.5 with thinking disabled the wording uses "reason through" (BP-236). Enabling thinking is offered first, since the guide calls this a fallback.

### BP-188 budget_tokens is deprecated but still functional on Opus 4.6 and Sonnet 4.6
- Kind: fact
- Rule: Treat budget_tokens extended thinking as deprecated on Opus 4.6 and Sonnet 4.6 even though it still functions there.
- Guide says: "If you need a hard ceiling on thinking costs, extended thinking with a `budget_tokens` cap is still functional on Opus 4.6 and Sonnet 4.6 but is deprecated."
- Applies when: A pasted API configuration or a prompt-authoring request targets Opus 4.6 or Sonnet 4.6 and sets `budget_tokens`.
- Skill applies it by: The value is not deleted as an error, since the request still works; the Target model item flags it as deprecated and offers the adaptive-thinking-plus-effort migration, and the Changed line records the offer rather than a silent rewrite.

### BP-189 budget_tokens returns 400 on Claude 4.7 and later
- Kind: fact
- Rule: Never emit budget_tokens for Claude 4.7 or later models; the API returns a 400 error.
- Guide says: "On Claude 4.7 and later models, setting `budget_tokens` returns a 400 error."
- Applies when: Any generated or migrated API configuration for Opus 4.7 (and for every profile above it).
- Skill applies it by: Removes `budget_tokens` and `type: "enabled"` from any described call for an Opus 4.7 target, substitutes adaptive thinking plus `output_config.effort`, and states the 400 reason in the Target model item. Inside this profile the line runs between Opus 4.6 (deprecated, works) and Opus 4.7 (400).

### BP-190 Lower effort or max_tokens as the cost ceiling
- Kind: technique
- Rule: Cap thinking cost on current models by lowering effort or using max_tokens as the hard limit under adaptive thinking.
- Guide says: "Prefer lowering the [effort](https://platform.claude.com/docs/en/build-with-claude/effort) setting or using `max_tokens` as a hard limit with [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)."
- Applies when: The user wants a hard ceiling on thinking cost on a 4.6-class or later target.
- Skill applies it by: The Target model item recommends the effort dial first and `max_tokens` second, and never recommends `budget_tokens` for that purpose.

### BP-201 Pre-4.6 models use manual extended thinking
- Kind: fact
- Rule: Configure pre-4.6 models with manual extended thinking and budget_tokens, as listed in the per-model configuration table.
- Guide says: "Older models use manual [extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) with `budget_tokens`; see the [per-model configuration table](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting#supported-models) for which configuration each model accepts."
- Applies when: The target is Opus 4.5, Sonnet 4.5, or Haiku 4.5.
- Skill applies it by: Split by model. For Opus 4.5 and Sonnet 4.5, both outside the guide's thirteen and squarely the "older models" this sentence is about, the Target model item keeps `thinking: {type: "enabled", budget_tokens: N}` and does not "modernise" it to adaptive. For Haiku 4.5 the guide names no model here and Haiku 4.5 is one of the thirteen current models (BP-002), so the shape is not asserted: the item names the per-model configuration table (BP-202) as the authority and records the reading as an assumption. In all three cases the levels and modes each model accepts come from that table rather than from this file.

### BP-347 Update thinking configuration when migrating to a 4.6 model
- Kind: migration
- Rule: Replace manual thinking with budget_tokens by adaptive thinking and control depth with the effort parameter.
- Guide says: "4. **Update thinking configuration:** Claude 4.6 models use [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) (`thinking: {type: \"adaptive\"}`) instead of manual thinking with `budget_tokens`. Use the [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) to control thinking depth."
- Applies when: A pasted configuration written for a pre-4.6 model is being pointed at Opus 4.6, Opus 4.7, or Sonnet 4.6.
- Skill applies it by: The migration checklist in Step 4 performs the swap and records it; "think harder" phrasing in the paste maps to an effort level rather than a token budget (BP-347, BP-350).

Group: Claude Sonnet 4.6

Also relevant: BP-188 (budget_tokens deprecated), BP-217 (thinking off when omitted), BP-194 (adaptive), BP-124 (no last-turn prefill), BP-016 (the five axes on which Sonnet 5 differs from this model). The Sonnet 4.6 facts printed on the Sonnet 5 page are the effort default `high` with `max` available (S5-11, S5-18), acceptance of `temperature`, `top_p`, and `top_k` (S5-49), and the one-step-down mapping and observed-thinking-length benchmarking when moving to Sonnet 5 (S5-18, S5-19); they live in section 2 of this file and in `references/models/sonnet-5.md`.

### BP-241 Context awareness
- Kind: model-note
- Rule: Know that Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, and Claude Haiku 4.5 feature context awareness and can track their remaining token budget throughout a conversation.
- Guide says: "Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, and Claude Haiku 4.5 feature [context awareness](https://platform.claude.com/docs/en/build-with-claude/context-windows#context-awareness), enabling the model to track its remaining context window (that is, its \"token budget\") throughout a conversation."
- Applies when: Authoring a long agentic prompt for Sonnet 4.6, Sonnet 4.5, or Haiku 4.5, or reasoning about how one of them behaves near the context limit as the executing model.
- Skill applies it by: Long agentic prompts for these three graft context_compaction_persistence and spend_entire_context so the model does not wrap up early; the agentic taxonomy row's model overlay names them as takers of these snippets. The Opus models in this profile are not named as context-aware and do not take the snippets on this basis (BP-025). On Haiku 4.5 the condition is wider, any run that may approach the context window, because this is the only statement the guide makes about the model.

### BP-243 Context awareness improves context management
- Kind: fact
- Rule: Expect context-aware models to manage work and context more effectively because they know how much space remains.
- Guide says: "This enables Claude to execute tasks and manage context more effectively by understanding how much space it has to work."
- Applies when: Multi-window or long agentic work on the three context-aware models.
- Skill applies it by: No token-accounting scaffolding is written into the prompt; the model is told the harness compacts (BP-244) and left to manage the rest.

### BP-244 Tell the model the harness compacts context
- Kind: technique
- Rule: When running in a harness that compacts context or saves context to external files (like Claude Code), tell Claude so in the prompt so it can behave accordingly.
- Guide says: "If you are using Claude in an agent harness that compacts context or allows saving context to external files (like in Claude Code), consider adding this information to your prompt so Claude can behave accordingly."
- Applies when: The task is long enough that the context limit could be approached, and the target runs in a compacting harness.
- Skill applies it by: `<context>` states that the harness compacts context and names the memory directory when one exists; the block below goes into `<execution_guidance>`.

### BP-245 Do not wrap up early
- Kind: anti-pattern
- Rule: Do not let Claude wrap up work early as it approaches the context limit; counter this tendency with explicit prompt guidance.
- Guide says: "Otherwise, Claude may sometimes naturally try to wrap up work as it approaches the context limit."
- Applies when: Long tasks without compaction guidance in the prompt.
- Skill applies it by: Grafts the persistence block; and as executing behaviour (section 6) never stops a task because the remaining budget looks small.

### BP-246 Sample: context_compaction_persistence
- Kind: sample-prompt
- Rule: Use this prompt block to tell Claude the context will be compacted, to save progress to memory before refresh, and never to stop a task early because of the token budget.
- Guide says: see snippet context_compaction_persistence; the block opens "Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off." and closes "Never artificially stop any task early regardless of the context remaining."
- Applies when: Agentic long-horizon requests for Sonnet 4.6, Sonnet 4.5, or Haiku 4.5, executed in a compacting harness. On Haiku 4.5 the condition is wider, any run that may approach the context window, because this is the only statement the guide makes about the model.
- Skill applies it by: Grafted into `<execution_guidance>` beside spend_entire_context when the multi-session or many-steps signal fires.

### BP-247 Pair the memory tool with context awareness
- Kind: link
- Rule: Pair the memory tool with context awareness to manage context transitions.
- Guide says: "The [memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) pairs well with context awareness for managing context transitions."
- Applies when: Multi-window tasks on the three context-aware models where state must survive a refresh.
- Skill applies it by: When a memory tool or memory directory is available, the prompt names it as the place to save progress before compaction; the link is in section 8.

### BP-261 Sample: spend_entire_context
- Kind: sample-prompt
- Rule: Use this prompt block to encourage planning, spending the entire output context on the task, and avoiding running out of context with uncommitted work.
- Guide says: see snippet spend_entire_context; the block opens "This is a very long task, so it may be beneficial to plan out your work clearly." and closes "Continue working systematically until you have completed this task."
- Applies when: Agentic long-horizon requests on the three context-aware models.
- Skill applies it by: Grafted into `<execution_guidance>` beside context_compaction_persistence. On Haiku 4.5 the condition is wider, any run that may approach the context window, because this is the only statement the guide makes about the model. The guide prints this block under a multiwindow subsection that names no model, so it is also available to any target in this profile on multi-window work.

Group: Claude Sonnet 4.5

Also relevant: BP-241, BP-243 to BP-247, BP-261 (context awareness and the two blocks), BP-201 (manual extended thinking), BP-128 (prefill still supported).

### BP-213 claude-sonnet-4-5-20250929 is the guide's before-migration example string
- Kind: fact
- Rule: Use the guide's model pairing as the migration reference: claude-sonnet-4-5-20250929 (older, extended thinking) to claude-opus-4-8 (adaptive).
- Guide says: "\"model\": \"claude-sonnet-4-5-20250929\","
- Applies when: Illustrating or performing a before-and-after thinking migration, or writing API code that names Sonnet 4.5.
- Skill applies it by: This is the only API string the guide prints for any model in this profile, so it is the one the skill may pin; the target replaces `claude-opus-4-8` on the after side when the migration goes somewhere else. Every other string in this profile is routed to the models overview.

### BP-361 Migration guide for Sonnet 4.5 or earlier
- Kind: link
- Rule: Follow the Sonnet 5 migration guide when moving from Sonnet 4.5 or earlier.
- Guide says: "See [Migrating to Claude Sonnet 5 from Claude Sonnet 4.5 or earlier](https://platform.claude.com/docs/en/models/sonnet-5/migration-guide#migrating-from-sonnet-45) in the migration guide, which covers the effort default change and the removal of manual extended thinking (`budget_tokens`)."
- Applies when: A prompt or configuration written for Sonnet 4.5, Haiku 4.5, or an earlier model is being pointed at Sonnet 5.
- Skill applies it by: The Target model item names this guide as the authority for the move; the skill does not invent the effort default change from its own snapshots. This is the Sonnet 5 migration note that a prompt coming from Sonnet 4.5 or earlier carries, and it is separate from the Sonnet 4.6 to Sonnet 5 route (S5-05).

### BP-362 What that migration covers
- Kind: fact
- Rule: Account for the Sonnet 5 effort default change and the removal of manual extended thinking (budget_tokens).
- Guide says: "which covers the effort default change and the removal of manual extended thinking (`budget_tokens`)."
- Applies when: Migrating a Sonnet 4.5-era or Haiku 4.5-era configuration to Sonnet 5.
- Skill applies it by: `budget_tokens` is removed with the 400 reason for a Sonnet 5 target and the effort level is re-derived from the Sonnet 5 profile rather than carried; the effort default change itself is taken from the linked guide, not asserted here, because from Sonnet 4.6 the default is unchanged at `high` (S5-11).

Group: Claude Haiku 4.5

Also relevant: BP-241, BP-243 to BP-247, BP-261 (context awareness and the two blocks), BP-201 (manual extended thinking), BP-128 (prefill still supported), BP-361 and BP-362 (migration to Sonnet 5).

### BP-002 Haiku 4.5 is inside the thirteen but has no page
- Kind: fact
- Rule: Treat the guide as authoritative for exactly these thirteen current models and route any other model to the migration considerations.
- Guide says: "This is the reference for prompt engineering with current Claude models, including Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, and Claude Haiku 4.5."
- Applies when: The target is Haiku 4.5.
- Skill applies it by: Tier A, and the only tier A model with no closest page, so its Reading line says the guide is applied directly. The guide's general techniques apply with no analogy note; the only Haiku-specific statement in the guide is context awareness (BP-241), so section 4 for a Haiku target is the guide's defaults plus the two context blocks, grafted whenever the run may approach the window rather than only on the agentic long-horizon row, since otherwise the one statement the guide makes about this model never reaches a prompt (BP-241, BP-245). No Sonnet-page or Opus-page snippet is grafted without an Assumed entry (BP-025).

Group: Claude Mythos Preview

### BP-124 Last-turn prefill is unsupported from Claude 4.6 models and Mythos Preview
- Kind: fact
- Rule: Do not use prefilled assistant responses on the last assistant turn with Claude 4.6 models or Claude Mythos Preview; they are no longer supported.
- Guide says: "Starting with Claude 4.6 models and [Claude Mythos Preview](https://anthropic.com/glasswing), prefilled responses (providing a partial assistant message for Claude to continue from) on the last assistant turn are no longer supported."
- Applies when: Prompt authoring for Mythos Preview, Opus 4.6, Opus 4.7, or Sonnet 4.6; API code the user is writing; or a pasted prompt that ends with a partial assistant turn.
- Skill applies it by: Step 4 detects the construct and converts it per the five paths below; a trailing partial assistant turn is never emitted for these four targets. Opus 4.5, Sonnet 4.5, and Haiku 4.5 keep prefill if the user insists, with the migration path noted (BP-128).

### BP-125 What counts as a prefill
- Kind: fact
- Rule: A prefilled response means providing a partial assistant message for Claude to continue from; use this definition to recognise prefill in pasted prompts and code.
- Guide says: "prefilled responses (providing a partial assistant message for Claude to continue from)"
- Applies when: Classifying a construct: a trailing assistant message, "start your answer with {", "Here is the JSON:" as an assistant turn.
- Skill applies it by: Step 1c flags natural-language equivalents such as "begin your response with" as well as literal partial turns; historical assistant turns used as conversation examples are not prefills and are kept (BP-128).

### BP-126 Prefill returns a 400
- Kind: fact
- Rule: Expect a 400 error when a request with a prefilled assistant message is sent to a model that no longer supports prefill.
- Guide says: "Requests with prefilled assistant messages to these models return a 400 error."
- Applies when: The user reports a 400, or is authoring API calls for Mythos Preview or a 4.6-class model.
- Skill applies it by: The diagnostic goes in `<context>` when a 400 is mentioned alongside a trailing assistant message, and the 400 reason is stated in the Changed line when the construct is removed.

### BP-127 Direct instruction replaces most prefill
- Kind: fact
- Rule: Assume most former prefill use cases can be met by direct instruction because instruction following has advanced.
- Guide says: "Model intelligence and instruction following have advanced such that most use cases of prefill no longer require it."
- Applies when: Any pasted prompt that uses prefill for format, preamble suppression, refusals, continuation, or context hydration.
- Skill applies it by: The direct instruction is tried first; structured outputs or tools are escalated to only when the format must be schema-exact.

### BP-128 Earlier models keep prefill; non-final assistant turns are unaffected
- Kind: fact
- Rule: Earlier models still support prefill, and assistant messages placed elsewhere in the conversation (not the last turn) remain allowed on all models.
- Guide says: "Earlier models continue to support prefills, and adding assistant messages elsewhere in the conversation is not affected."
- Applies when: The target is Opus 4.5, Sonnet 4.5, or Haiku 4.5, or a transcript contains historical assistant messages as few-shot conversation examples.
- Skill applies it by: For those three targets a prefill may stay, with the migration path recorded in the Assumed line; historical assistant turns are never stripped on any target. A compliance-forcing prefill is removed regardless of model, and the legitimate purpose is stated in `<context>` (BP-138).

### BP-129 Mythos Preview reference link
- Kind: link
- Rule: Know that Claude Mythos Preview is the other model family (besides Claude 4.6) where last-turn prefill is unsupported.
- Guide says: "[Claude Mythos Preview](https://anthropic.com/glasswing)"
- Applies when: Recording prefill support for Mythos Preview, or noting its availability.
- Skill applies it by: Section 8 holds the link; the Reading line notes limited availability for a Mythos Preview target, and only the prefill and adaptive-thinking facts are asserted for it, since those are the only two the guide prints. Mythos Preview is not Mythos 5 or Mythos 5.1, which resolve to the Fable profiles.

### BP-194 Mythos Preview uses adaptive thinking
- Kind: fact
- Rule: Treat Claude 4.6 and later models and Claude Mythos Preview as adaptive-thinking models where Claude decides when and how much to think.
- Guide says: "Claude 4.6 and later models and Claude Mythos Preview use [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) (`thinking: {type: \"adaptive\"}`), where Claude dynamically decides when and how much to think."
- Applies when: Writing a thinking configuration for Mythos Preview.
- Skill applies it by: Prints `thinking: {type: "adaptive"}`; whether omitting the parameter turns thinking off is not printed for Mythos Preview (BP-217 names Opus 4.6 to 4.8 and Sonnet 4.6 only), so the skill sets it explicitly rather than relying on a default.

Group: the five migration paths away from prefill (Claude 4.6 and later, Mythos Preview)

### BP-130 to BP-133 Path 1: output formatting
- Kind: migration
- Rule: Replace prefills that force JSON, YAML, or classification structure with Structured Outputs, after first simply asking the model to conform to the schema, with retries; for classification use a tool with an enum field of valid labels or structured outputs.
- Guide says: "Prefills have been used to force specific output formats like JSON/YAML, classification, and similar patterns where the prefill constrains Claude to a particular structure. **Migration:** The [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) feature is designed specifically to constrain Claude's responses to follow a given schema." plus "Try asking the model to conform to your output structure first, as newer models can reliably match complex schemas when told to, especially if implemented with retries." and "For classification tasks, use either tools with an enum field containing your valid labels or structured outputs."
- Applies when: The paste prefills a leading `{`, `<answer>`, or a fixed label.
- Skill applies it by: `<output_format>` states the schema and, when the deliverable is parsed, names the XML indicator or the JSON shape; the Structured Outputs page is named in the Target model item for API work (BP-133).

### BP-134 to BP-137 Path 2: eliminating preambles
- Kind: migration
- Rule: Replace preamble-skipping prefills with a direct system-prompt instruction to respond without preamble, or with XML tags, structured outputs, or tool calling, and strip a stray preamble in post-processing.
- Guide says: "Prefills like `Here is the requested summary:\n` were used to skip introductory text. **Migration:** Use direct instructions in the system prompt:" plus the snippet no_preamble, "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc.", then "Alternatively, direct the model to output within XML tags, use structured outputs, or use tool calling." and "If the occasional preamble slips through, strip it in post-processing."
- Applies when: The paste prefills "Here is..." or an equivalent opener.
- Skill applies it by: Grafts no_preamble into `<output_format>` and, for API work, mentions post-processing as the residual safeguard rather than adding more prompt text.

### BP-138 Path 3: avoiding bad refusals
- Kind: migration
- Rule: Do not use prefill to steer around refusals; clear prompting in the user message is sufficient because the model handles appropriate refusals much better now.
- Guide says: "Prefills were used to steer around unnecessary refusals. **Migration:** Claude is much better at appropriate refusals now. Clear prompting within the `user` message without prefill should be sufficient."
- Applies when: The paste uses a prefill to force compliance.
- Skill applies it by: The construct is removed and the legitimate purpose is stated plainly in `<context>`; no prompt is rewritten to defeat a warranted refusal, which is also SKILL.md Step 4's rule.

### BP-139 to BP-141 Path 4: continuations
- Kind: migration
- Rule: Move continuations into the user message with the final text of the interrupted response included, or retry the request when continuation is error handling with no UX penalty.
- Guide says: "Prefills were used to continue partial completions, resume interrupted responses, or pick up where a previous generation left off. **Migration:** Move the continuation to the user message, and include the final text from the interrupted response:" plus "Your previous response was interrupted and ended with \`\[previous\_response]\`. Continue from where you left off." and "If this is part of error-handling or incomplete-response-handling and there is no UX penalty, retry the request."
- Applies when: The paste resumes a truncated generation.
- Skill applies it by: The continuation template becomes a user-turn instruction; for a pipeline the Target model item offers the retry as the simpler fix.

### BP-142 to BP-144 Path 5: context hydration and role consistency
- Kind: migration
- Rule: Inject what were previously prefilled-assistant reminders into the user turn in very long conversations, and in complex agentic systems hydrate through tools or during context compaction.
- Guide says: "Prefills were used to periodically ensure refreshed or injected context. **Migration:** For very long conversations, inject what were previously prefilled-assistant reminders into the user turn." plus "If context hydration is part of a more complex agentic system, consider hydrating through tools (expose or encourage use of tools containing context based on heuristics such as number of turns) or during [context compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)."
- Applies when: The paste re-injects standing context as an assistant turn.
- Skill applies it by: Harness-authoring deliverables move the reminder to a user turn or a turn-scoped system message (BP-358) and name the compaction page (BP-144); the skill's own append-only rule (Standing rule 12) is the same principle.

### BP-351 to BP-353 The migration step that names the boundary
- Kind: migration
- Rule: Stop using prefilled assistant responses and use the documented alternatives instead; treat prefilled last-assistant-turn responses as unsupported from Claude 4.6 models and Claude Mythos Preview onward.
- Guide says: "5. **Migrate away from prefilled responses:** Prefilled responses on the last assistant turn are no longer supported starting with Claude 4.6 models and Claude Mythos Preview. See [Migrating away from prefilled responses](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#migrating-away-from-prefilled-responses) for detailed guidance on alternatives."
- Applies when: A migration-flavoured request whose target is a 4.6-class model or Mythos Preview.
- Skill applies it by: The boundary is recorded per model in section 2's table; the five paths above are the alternatives, and the section link (BP-353) is in section 8.

Group: anti-laziness and proactivity on Claude 4.6 and later

### BP-354 Dial back anti-laziness prompting
- Kind: migration
- Rule: Dial back anti-laziness prompting that pushed earlier models to be more thorough or use tools more aggressively.
- Guide says: "6. **Tune anti-laziness prompting:** If your prompts previously encouraged the model to be more thorough or use tools more aggressively, dial back that guidance."
- Applies when: The raw request or paste contains amplifiers such as "be extremely thorough", "use every tool", "do not stop until", "check everything", or "do not be lazy", and the target is Opus 4.6 or Sonnet 4.6, which are the models the guide's phrase "Claude 4.6 models" names.
- Skill applies it by: Step 4 strips the amplifier and substitutes a plain statement of what has to be covered; the removal is recorded in the Changed line. For Opus 4.7 and for the pre-4.6 targets in this profile (Opus 4.5, Sonnet 4.5, Haiku 4.5) the guide does not make this claim: it says "Claude 4.6 models", not "4.6 and later". An amplifier on those four is softened as a matter of the skill's own house style and the change is recorded as an assumption.

### BP-355 4.6 models overtrigger on inherited instructions
- Kind: model-note
- Rule: Expect Claude 4.6 models to be more proactive and to overtrigger on instructions written for earlier models.
- Guide says: "Claude 4.6 models are more proactive and may overtrigger on instructions that were needed for previous models."
- Applies when: Executing on, or authoring for, Opus 4.6 or Sonnet 4.6, the models the guide names, with prompts inherited from earlier generations; on Opus 4.7 the same strip pass is applied by analogy with the assumption recorded.
- Skill applies it by: This is the rationale for the whole strip pass above and for the plain wording of anything the skill writes itself; execution does not over-expand scope beyond what the rewritten prompt states.

## When this is the TARGET model: add to the rearticulated prompt

The content of the rearticulated prompt follows this section when the target is one of the seven. The base layer is the guide, applied in full: this profile adds per-model blocks and removes per-model anti-patterns, and nothing else. For Opus 4.7 the guide prints only the four API facts in section 2 (the `budget_tokens` 400, thinking off when the parameter is omitted, adaptive thinking, and no last-turn prefill) and no behavioural statement, so its behavioural layer is the guide's defaults plus the guide's own blocks that profile's page calls for: subagent_usage_policy and minimize_overengineering on a code change, both by analogy with `opus-4-8` and with the assumption recorded, and autonomy_safety_confirmation when the Step 1f side-effect scan fires, as for the other five non-4.6 targets (BP-271, section 7). The snippet text stays the guide's, never the Opus 4.8 page's (BP-025). The Fable 5.1 default snippets (progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule) are not grafted, because they are measured on Fable 5.1. Neither are the page-measured snippets of any other profile (`f5_*`, `o5_*`, `s5_*`, `o48_*`), including the short frontend block that the Sonnet 5 and Opus 4.8 pages print; this profile takes the guide's long `frontend_aesthetics` instead (BP-330).

Target model item (SKILL.md Step 5, Reading line). Always one of the three tier forms from BP-002: `Target model: <name> (legacy-4x tier A: current, no page, closest page <x> by analogy)`, `Target model: Haiku 4.5 (legacy-4x tier A: current, no page, guide applied directly, no closest page documented)`, or `Target model: <name> (legacy-4x tier B: outside the guide's thirteen; guide applied by analogy, migration checklist run)`. When the target differs from the executing model, the request is prompt authoring, or the user asked about speed, cost, or thinking, append: the thinking configuration in the guide's exact syntax, which is `thinking: {type: "adaptive"}` set explicitly on Opus 4.6, Opus 4.7, Sonnet 4.6, and Mythos Preview because omitting it runs without thinking on the first three (BP-194, BP-217), and `thinking: {type: "enabled", budget_tokens: N}` kept as it is on Opus 4.5, Sonnet 4.5, and Haiku 4.5 (BP-201); `budget_tokens` flagged as deprecated on Opus 4.6 and Sonnet 4.6 (BP-188) and removed with the 400 reason on Opus 4.7 (BP-189); a lower effort recommended as the fallback knob when over-aggression or overthinking is the complaint (BP-184, BP-186), with the effort page cited for per-model availability (BP-191) and `high` named as the Sonnet 4.6 default (S5-11); `max_tokens` as the hard cost ceiling under adaptive thinking (BP-190); prefill support per section 2's table with the 400 reason where it applies (BP-124, BP-126, BP-128); the model string only when the guide prints one, which is `claude-sonnet-4-5-20250929` for Sonnet 4.5 (BP-213), and otherwise the models overview named as the source; and, for a move to a paged model, the migration guide for that route (BP-361 for Sonnet 4.5 or earlier to Sonnet 5).

- `<role>`: one sentence, domain-matched, per the guide (BP-055 to BP-060). Nothing model-specific. Keep it plain on Opus 4.5 and Opus 4.6, where system-prompt text lands harder than on earlier models (BP-160).
- `<context>`: the why, the consumer, and the environment facts, per the guide (BP-061 to BP-063). For Sonnet 4.6, Sonnet 4.5, and Haiku 4.5 on a long task, state that the harness compacts context and name the memory directory when one exists (BP-244, BP-247). When a prefill was removed because the target rejects it, state the legitimate purpose the prefill served (BP-138). When thinking is off on the target, say so, so the manual chain-of-thought step has its reason (BP-217, BP-225).
- `<documents>`: guide rules unchanged, data before instructions (BP-062). For a vision task on Opus 4.5 or Opus 4.6, put the whole image set in one turn rather than one image per turn (BP-319).
- `<task>`: guide rules; posture sentence first, explicit verbs, numbered when order or completeness matters. On Opus 4.6 the depth of investigation the task needs is stated here rather than left to a "be thorough" line (BP-177, BP-179). Video work gets an explicit frame-extraction step (BP-321); detail-sensitive image work gets a crop-and-re-read step (BP-322, BP-323). A frontend build asks for the full application the user described, with richness modifiers on the ambition word (BP-326, BP-344, BP-345). When thinking is off, the reasoning step is written out as manual chain of thought, phrased with "reason through" on Opus 4.5 (BP-225, BP-236).
- `<constraints>`: minimize_overengineering verbatim for Opus 4.5 and Opus 4.6 on any code change (BP-300 to BP-302). For Opus 4.6, a bound on investigation, for example "read the files named in the task; widen only if they do not answer the question" (BP-178). The skill's own constraint sentences stay positive with a because clause; grafted guide blocks keep their quoted wording.
- `<output_format>`: guide rules; positive, with XML indicators when the output is parsed, plain-text math when math appears (BP-119, BP-120). On Opus 4.5, Sonnet 4.5, and Haiku 4.5 a last-turn prefill is still supported and may be used deliberately as a format lever, for example an opening `<quotes>` tag to guarantee a two-block output shape, with the choice and the migration path recorded (BP-128). no_preamble when a preamble-suppressing prefill was removed (BP-135). A schema statement, and Structured Outputs named for API work, when a format-forcing prefill was removed (BP-130 to BP-133). No default length or verbosity instruction, since the guide prints no verbosity note for these models and the skill writes none of its own (SKILL.md Standing rule 12).
- `<examples>`: guide rules; 3 to 5 when format, tone, or structure matters and can be shown, or the single quoting_sources_example for a summary of retrieved sources. `<thinking>` tags inside a few-shot example are the guide's way to show a reasoning pattern (BP-224), which matters most on the targets in this profile that run with thinking off.
- `<success_criteria>`: guide rules, observable, always including "files created or modified: only <the files named in task>", which is also the counter to the Opus 4.5 and 4.6 file-creation habit (BP-300, BP-303).
- `<execution_guidance>`: the guide's blocks, chosen by the taxonomy row: use_parallel_tool_calls, investigate_before_answering, temp_file_cleanup, general_purpose_solution, complex_research, and one posture snippet (default_to_action or do_not_act_before_instructions). Per model on top of those: autonomy_safety_confirmation and subagent_usage_policy for Opus 4.6, and for Opus 4.5 by analogy with the assumption recorded, since the guide states both for 4.6 and the catalog applies the autonomy block to all models as a precaution (BP-269 to BP-271, BP-286 to BP-290); commit_to_approach for Opus 4.6 when latency or thinking cost is a stated concern (BP-185 to BP-187); context_compaction_persistence for Sonnet 4.6, Sonnet 4.5, and Haiku 4.5 on long agentic work, and on Haiku 4.5 on any run that may approach the context window, because context awareness is the only statement the guide makes about that model; spend_entire_context beside it there, and on any target in this profile on multi-window or long-horizon work, since the guide prints that block under a subsection that names no model (BP-241, BP-244 to BP-246, BP-261); frontend_aesthetics in its long form, in system-prompt position, for any frontend build: on Opus 4.5 and Opus 4.6 because the guide states it for them, and on the other five targets by analogy with the assumption recorded, since the guide offers the block as a general system-prompt snippet and BP-327 is the reason not to leave a brief unguided (BP-025); or "Invoke frontend-design before <step>" when that skill is loaded (BP-327, BP-330, BP-342). Tool guidance, where any is needed, is written as a targeted trigger tied to a benefit rather than a standing default (BP-180, BP-181). batch_nudge and progress_updates_line are not grafted.
- `<verification>`: filled per the guide with self_check_verify and concrete checks drawn from `<success_criteria>` (BP-229 to BP-231). No model in this profile is exempt; the Opus 5 exemption is measured on Opus 5 (BP-232, BP-233). For long autonomous runs, name the verification tools the harness provides (BP-257 to BP-259). For detail-sensitive image work, the crop-and-re-read pass is a check, not an option (BP-323).
- Closing lines: long_output_budget_note is measured on Fable 5.1 and is not grafted; for a long deliverable, state the length expectation in `<output_format>` instead.

Reasoning exhortations: the guide's own rule applies, general instructions over prescriptive steps, so a hand-written step-by-step reasoning plan is dropped in favour of a short general instruction, and numbered work steps whose order or completeness matters stay (BP-221, BP-222, BP-223). The exception is a target running with thinking off, where the manual chain-of-thought step is written out on purpose (BP-225), and Opus 4.5 with thinking disabled, where the wording avoids "think" (BP-235, BP-236).

## When this is the TARGET model: remove or convert

Each conversion is recorded in the Changed line of the assumptions. For a tier B target the whole migration checklist runs, not only the thinking and prefill items: be specific about the desired behaviour (BP-343), frame instructions with quality and detail modifiers (BP-344, BP-345, snippet analytics_dashboard_more_effective), and request animations and interactive elements explicitly (BP-346).

| Found in the raw request or pasted prompt | Action for a target in this profile | Basis |
|---|---|---|
| A prefilled last assistant turn, "start your answer with", "Sure, here is" | Remove for Opus 4.7, Opus 4.6, Sonnet 4.6, and Mythos Preview, with the 400 reason, converted by the matching one of the five paths; may stay for Opus 4.5, Sonnet 4.5, and Haiku 4.5 with the migration path noted | BP-124, BP-126, BP-128, BP-130 to BP-144 |
| `thinking: {type: "enabled", budget_tokens: N}` | Remove with the 400 reason on Opus 4.7; flag as deprecated and offer the adaptive-plus-effort swap on Opus 4.6 and Sonnet 4.6; keep as it is on Opus 4.5, Sonnet 4.5, and Haiku 4.5 | BP-189, BP-188, BP-201, BP-347 |
| A request with no `thinking` field but a task that needs reasoning, on Opus 4.6, Opus 4.7, or Sonnet 4.6 | Set `thinking: {type: "adaptive"}` explicitly, because omitting it runs without thinking | BP-217, BP-194 |
| The word "think" or its variants, targeting Opus 4.5 with thinking disabled | Substitute "consider", "evaluate", or "reason through" throughout | BP-235, BP-236 |
| Anti-laziness amplifiers: "be extremely thorough", "use every tool", "do not stop until", "check everything" | Remove and substitute a plain statement of what has to be covered | BP-354, BP-179 |
| All-caps emphasis, "CRITICAL: You MUST use this tool when..." | Plain conditional wording, "Use this tool when..."; mandatory on Opus 4.5 and Opus 4.6, which respond strongly to the system prompt | BP-160 to BP-163 |
| "Default to using X", "If in doubt, use X" | "Use X when it would <benefit>" | BP-180 to BP-183 |
| Hand-written reasoning choreography and step-by-step plans | Drop in favour of a short general instruction; keep numbered work steps whose order matters; keep a manual chain-of-thought step when the target runs with thinking off | BP-221 to BP-223, BP-225 |
| A prompt that encouraged more exploration, targeting Opus 4.6 | Tune it down: state the investigation depth the task needs and bound it | BP-177 to BP-179 |
| Latency or token complaints answered with more prompt text, on Opus 4.6 | Recommend a lower effort in the Target model item; add commit_to_approach only if that is not enough | BP-184 to BP-187 |
| Hand-written delegation choreography, or nothing at all, on Opus 4.6 | Replace with subagent_usage_policy; it is mandatory rather than conditional for this target | BP-286 to BP-290 |
| Extra files, helper abstractions, or unrequested configurability in the ask, on Opus 4.5 or Opus 4.6 | Add minimize_overengineering and the files-touched success criterion | BP-300 to BP-303 |
| Vision workarounds and hedges written for weaker vision, on Opus 4.5 or Opus 4.6 | Remove; state the image task directly and add the crop step when detail matters | BP-318, BP-322, BP-323 |
| A vague or unguided frontend brief on any target in this profile | Add the long frontend_aesthetics block plus the concrete brief; never leave the design unguided. Stated for Opus 4.5 and Opus 4.6; applied to the other five by analogy with the assumption recorded | BP-327, BP-330, BP-025 |
| Token-budget scaffolding or "wrap up when the context runs low" on Sonnet 4.6, Sonnet 4.5, or Haiku 4.5 | Replace with context_compaction_persistence and spend_entire_context | BP-241, BP-245, BP-246, BP-261 |
| Fable 5.1 default snippets in a ported prompt (progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule) | Remove; measured on Fable 5.1 | BP-025 |
| `frontend_aesthetics_short`, `s5_*`, `o48_*`, `o5_*`, or `f5_*` snippets in a ported prompt | Remove or substitute the guide's own block; those texts are measured on their own pages | BP-025, BP-330 |
| A verification instruction removed because a prompt came from an Opus 5 rewrite | Restore it; the no-verification rule is measured on Opus 5 | BP-229, BP-232, BP-233 |
| Sampling parameters (`temperature`, `top_p`, `top_k`) | Keep on Sonnet 4.6 and the pre-4.6 models, since the 400 is new for Sonnet-class models on Sonnet 5; flag for the migration guide on the Opus targets | S5-49 |

## When this is the EXECUTING model: how the skill behaves in Steps 5-7

Applies when the model running the skill resolves to one of these seven (the Reading line then reads "executing model: legacy-4x, <name>"). SKILL.md Steps 6 and 7 run as written, which is the guide-default behaviour: the Fable 5.1 sentences inside those steps describe the skill's own house cadence, not a model-measured claim, and they stay. The closest page for the executing model is named by analogy in the Reading line, exactly as for a target (BP-002, BP-025). The rearticulated prompt's content still follows the target profile.

- Narration cadence: SKILL.md Step 6 as written. One line saying what is about to happen, a one-line factual update before each tool batch, a short note after. The guide states no cadence for these models, so nothing is added and nothing is suppressed; the Fable 5.1 progress_updates_line and the Opus 5 narrate-on-findings rule are both page-measured and neither is borrowed.
- Verification pass: the full Step 7, run with tools rather than asserted. No model in this profile has the Opus 5 exemption (BP-232, BP-233), and self_check_verify is the guide's default for coding and math work (BP-229 to BP-231).
- Delegation: apply the subagent_usage_policy test before spawning anything, and prefer direct Grep, Glob, and Read for code exploration (BP-289, BP-290). On Opus 4.6 that preference is a correction of a known tendency, not a style choice: the guide's own example is a subagent spawned for code exploration where a direct grep call would be faster (BP-286).
- Formatting: guide defaults. formatting_in_chat_rule is measured on Fable 5.1 and is not applied to the skill's own output.
- Edit style: SKILL.md Standing rule 11 applies as skill behaviour, targeted edits with whole-file rewrites only for short or mostly-changing files. The targeted_edits snippet text is measured on Fable 5.1 and is not grafted into a prompt for these targets.
- Search behaviour: Standing rule 6, read every named file before claiming anything about it and back each claim with a read or search result (BP-314 to BP-317). The Fable 5.1 low-effort search-triggering fix (F51-125) is page-measured and does not transfer; if the session answers from memory instead of searching, the remedy here is the guide's investigate_before_answering wording and, on a 4.6-class model, a higher effort setting from the caller (BP-184 read in reverse).
- Progress-claim grounding: facts only, no self-evaluation, per Standing rule 12 and the guide (BP-089). The Fable 5 rule that progress claims are audited against tool results (F5-38) is page-measured; the underlying practice is already SKILL.md Step 6's "back each claim with a read or search result".
- Scope discipline: keep changes to the ask, with pre-existing bugs and unrequested improvements becoming follow-ups (Standing rule 7). On Opus 4.5 and Opus 4.6 this is the executing-side counterpart of BP-300: no extra files, no helper abstraction for a one-off, no unrequested configurability.
- Exploration and commitment on Opus 4.6: bound investigation to what the task needs (BP-178), and when latency matters choose an approach and see it through rather than re-opening decisions (BP-185, BP-187).
- Reversibility: Standing rules 1 and 4 already encode the guide's autonomy-and-safety block (BP-269 to BP-271). On an Opus 4.6 executing model the check is mandatory rather than a precaution, because the guide names this model as one that may take hard-to-reverse or shared-system actions without guidance.
- Context handling on Sonnet 4.6, Sonnet 4.5, and Haiku 4.5: these are context-aware and can see their remaining budget (BP-241). Do not wrap up early because the number looks small (BP-245); save progress and state to the memory directory before a refresh and continue (BP-246, BP-247).
- Vision work in-session on Opus 4.5 and Opus 4.6: read screenshots and UI elements directly (BP-320), keep related images in one context (BP-319), split video into frames (BP-321), and crop and enlarge before answering when a detail is small (BP-322, BP-323).
- Thinking on the executing side: whether thinking is on is a harness setting the skill cannot change. On an Opus 4.5 session running with thinking disabled, the "think" sensitivity is a prompt-authoring rule for that target (BP-235) and does not change the skill's own narration; when the session's reasoning looks shallow, the remedy is a higher effort setting from the caller, not stacked exhortations (BP-184, BP-186 read in reverse).
- Refusal handling: not printed for any of these models. Report a refusal plainly, name no fallback the sources do not state for this model, and do not rephrase the request to evade it (BP-138).
- Last-paragraph check and recap: Step 7 as written; `<success_criteria>` governs the recap.

## Snippets

IDs only; verbatim text lives in `references/snippet-library.md`. Every snippet here is a guide block, so each is measured on the model the guide names beside it and on nothing else (BP-025).

- autonomy_safety_confirmation (BP-271) - `<execution_guidance>`. Measured on Opus 4.6; the catalog applies it to all models as a precaution, so it is grafted for Opus 4.6 always, for Opus 4.5 and Opus 4.7 by analogy with the assumption recorded, and for the other four when the side-effect signal fires.
- subagent_usage_policy (BP-290) - `<execution_guidance>`. Mandatory for an Opus 4.6 target (BP-286); grafted for Opus 4.5 and Opus 4.7 by analogy with the assumption recorded; conditional elsewhere in this profile.
- minimize_overengineering (BP-302) - `<constraints>`. Measured on Opus 4.5 and Opus 4.6; grafted for both on any code change, and for Opus 4.7 by analogy with `opus-4-8` with the assumption recorded.
- commit_to_approach (BP-187) - `<execution_guidance>`. Opus 4.6 only, and only when latency or thinking cost is a stated concern.
- context_compaction_persistence (BP-246) - `<execution_guidance>`. Sonnet 4.6, Sonnet 4.5, Haiku 4.5 on long agentic work, and on Haiku 4.5 on any run that may approach the context window, because context awareness is the only statement the guide makes about that model (BP-241).
- spend_entire_context (BP-261) - `<execution_guidance>`. Not model-named in the guide: available to every target here on multi-window or long-horizon work, and grafted beside context_compaction_persistence on the three context-aware models, where BP-241 makes it the default rather than a choice.
- frontend_aesthetics (BP-330) - system-prompt position, before the task instructions, for frontend builds on any target here; measured on Opus 4.5 and Opus 4.6, extended to the other five as an assumption (BP-025). This profile takes the long form, the one the guide prints in full; `frontend_aesthetics_short` is the Sonnet 5 and Opus 4.8 page block and is not used here.
- no_preamble (BP-135) - `<output_format>`, when a preamble-suppressing prefill was removed.
- Guide blocks available to every target here, chosen by the taxonomy row rather than by model: use_parallel_tool_calls, investigate_before_answering, temp_file_cleanup, general_purpose_solution, self_check_verify, plain_text_math, complex_research, spend_entire_context on multi-window work, quoting_sources_example with an `Assumed:` entry recording that its text was measured on the Fable 5.1 page (BP-025), analytics_dashboard_more_effective, and one posture snippet, default_to_action or do_not_act_before_instructions.
- Phrasing patterns rather than grafted blocks: use_this_tool_when (BP-163) and targeted_tool_trigger (BP-181); the tool name, the trigger condition, and the benefit are substituted from the request.
- Not grafted on any target in this profile: progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule, mannered_prose_short, long_output_budget_note (all measured on Fable 5.1); every `f5_*`, `o5_*`, `s5_*`, and `o48_*` snippet; frontend_aesthetics_short; tone_preference (measured on Opus 5). Any of these appearing in a ported prompt is removed per section 5.

## Not covered by this page

There is no page. This profile is applied by analogy in its entirety, and the guide says why that has to be stated: "Where a technique names a specific model, treat it as measured on that model and re-check it against your own evals before applying it to another" (BP-025). So a rule in section 3 governs only the model or models its own quote names, and a technique extended from one of these models to another, or borrowed from a paged sibling, is recorded as an assumption in the Reading line. Any model outside the guide's thirteen covered models, whether one of the three tier B models here or a name the alias table does not contain, gets the closest page named in the Reading line and the Step 4 migration checklist (BP-002, BP-005).

Everything not in sections 2 to 7 falls back to the main guide (`references/technique-catalog.md`) unchanged, because the guide is this profile's whole base layer: being clear and direct, context and motivation, role prompting, XML structure and tag order, long-context ordering (BP-062), examples and multishot, positive format control and the list exception, plain-text math, explicit action verbs and posture, parallel tool calls, thinking and self-check verification, long-horizon state tracking and multi-window workflows, research structure, subagent orchestration, file-creation hygiene, hallucination controls, and the seven migration considerations.

Facts the sources do not print for these models, which the skill names a linked page for rather than asserting: the context window size of any of the seven; refusal, safeguard, and fallback behaviour; tokenizer characteristics; sampling-parameter acceptance on the Opus models here; the effort default and level list for every model except Sonnet 4.6; `max_tokens` ceilings; and the API model string for every model except Sonnet 4.5. Nor is there a house visual style description for any of them: the Opus 4.8 palette description is measured on that page and is not borrowed (O48-46 to O48-54).

Related pages (do not import their content; name them in the Target model item when a fact is needed):
- Migration guide, https://platform.claude.com/docs/en/about-claude/models/migration-guide - the route for models with no page (BP-012, BP-360).
- Migrating to Claude Sonnet 5 from Claude Sonnet 4.5 or earlier, https://platform.claude.com/docs/en/models/sonnet-5/migration-guide#migrating-from-sonnet-45 (BP-361, BP-362).
- Models overview, https://platform.claude.com/docs/en/models/overview - model strings for the six the guide does not print (BP-007).
- Effort, https://platform.claude.com/docs/en/build-with-claude/effort - levels and per-model availability (BP-191).
- Thinking, https://platform.claude.com/docs/en/build-with-claude/thinking (BP-192); Extended thinking, https://platform.claude.com/docs/en/build-with-claude/extended-thinking (BP-203); per-model thinking configuration table, https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting#supported-models (BP-202).
- Context awareness, https://platform.claude.com/docs/en/build-with-claude/context-windows#context-awareness (BP-242); Memory tool, https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (BP-247); Compaction, https://platform.claude.com/docs/en/build-with-claude/compaction (BP-144).
- Migrating away from prefilled responses, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#migrating-away-from-prefilled-responses (BP-353); Structured Outputs, https://platform.claude.com/docs/en/build-with-claude/structured-outputs (BP-133); Claude Mythos Preview, https://anthropic.com/glasswing (BP-129).
- Agent skills overview, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview (BP-324); crop tool recipe, https://platform.claude.com/cookbook/multimodal-crop-tool (BP-325).
- Improving frontend design through skills, https://www.claude.com/blog/improving-frontend-design-through-skills (BP-328); Claude Design, https://support.claude.com/en/articles/14604416-get-started-with-claude-design (BP-329); frontend-design skill, https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md (BP-342).
- Prompting Claude Sonnet 5, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 - the page the guide describes as covering "migration from Claude Sonnet 4.6", so it is the named authority for a Sonnet 4.6 target and for the Sonnet 4.6 to Sonnet 5 route (BP-365, BP-016, S5-05).
- Sibling profiles for the closest-page analogies: `references/models/opus-4-8.md` for Opus 4.7 and Opus 4.6, and `references/models/sonnet-5.md` for the Sonnet 4.6 facts it prints.
