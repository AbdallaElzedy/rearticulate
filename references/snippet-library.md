# Snippet library: the verbatim graftable blocks

Sources (verbatim snapshots dated 2026-09-08):

- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Prompting Claude Fable 5.1 (also Claude Mythos 5.1): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
- Prompting Claude Fable 5 (also Claude Mythos 5): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
- Prompting Claude Opus 5: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
- Prompting Claude Sonnet 5: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
- Prompting Claude Opus 4.8: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8

Every fenced block below is the source text as the page prints it, reproduced exactly: its em dashes, its hyphens where the page uses a hyphen, its capitalisation including all-caps words such as NEVER and MUST, its ellipsis characters, its curly apostrophes where the page has them, and its line breaks inside a multi-line block. Where a page renders a bracket or an underscore MDX-escaped (`\[test criteria]`, `\<smoothly\_flowing\_prose\_paragraphs>`), the fence holds the rendered text and a Note line records the escape, because the escape is a documentation artifact and not part of the prompt. The skill's own prose in this file and in every other file of the skill avoids em dashes and uses normal sentence case; that rule governs what the skill writes, never what it quotes, so a grafted snippet is inserted unchanged and is never rewritten to match the skill's house style [BP-302, BP-309]. Where one text appears on two pages it has one section here that lists both sources, both models, and both alias IDs; where two pages print the same instruction with different punctuation, the section holds one fence per page so each stays verbatim. A snippet reproduced under "## Default snippets (verbatim)" in `templates/rearticulated-prompt.md` appears here with identical text and is marked "also in templates/rearticulated-prompt.md", so a default run can read the template alone and a dry run can read this file alone.

Parameters are not snippets. Four things belong in the Target model item of the Reading line and never in a fenced block grafted into a prompt: `budget_tokens`, which returns a 400 on Opus 4.7 and later and is deprecated but functional on 4.6, so a migrated prompt moves to `thinking: {type: "adaptive"}` plus `output_config.effort` [BP-188, BP-189]; the sampling parameters `temperature`, `top_p`, and `top_k`, which return a 400 on Sonnet 5 for any non-default value, so tone and variety are steered through the prompt instead and design variety comes from the propose-directions snippet [S5-49, S5-55]; the effort level, which is re-derived per profile and never written into the prompt as "think harder" [F5-25, S5-21, O48-20]; and `max_tokens`, which stays in the request as the hard ceiling and is only quoted inside `long_output_budget_note` as that request's real value [F51-142, BP-190]. One wording caution rides along with them: the word "think" is a trigger on Opus 4.5 with thinking disabled, so on that model every snippet below that contains it (`think_thoroughly`, the low-effort multistep line, the thinking-trigger guard) is replaced by consider, evaluate, or reason through [BP-235, BP-236].

## Guide (all current models)

### analytics_dashboard_more_effective
- Source: Prompting best practices, "Be clear and direct", the more-effective side of the accordion example
- Measured on: all current models
- Graft when: the raw request contains an ambition word (full-featured, polished, complete, production-ready, go all out) or the frontend row applies and the verb is build rather than fix; the two trailing sentences go into `<task>` with the noun adapted to the actual deliverable [BP-028, BP-033, BP-344].
- Do not graft when: the user asked for a minimal, scoped, or single-file change, on any profile; richness modifiers there are scope creep, and Step 5 records the minimal reading instead [BP-035, F51-117].
- Text:
```text
Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation.
```

### quality_modifiers_dashboard
- Source: Prompting best practices, "Migration considerations", item 2 "Frame your instructions with modifiers"
- Measured on: all current models
- Graft when: the raw request is a terse build instruction and the user wants a complete result; this is the instead-of and use pair that shows the transformation, quoted in the Changed line rather than pasted into the prompt.
- Do not graft when: any profile, as prompt content. It is a pattern statement about rewriting, not a block to insert; the block to insert is `analytics_dashboard_more_effective`.
- Text:
```text
For example, instead of "Create an analytics dashboard", use "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation."
```

### tts_no_ellipses
- Source: Prompting best practices, "Add context to improve performance", the with-context example
- Measured on: all current models
- Graft when: the output reaches any non-human rendering, parsing, or speech surface, including a text-to-speech engine, a parser, a screen reader, a plain-text chat widget, and a ticket body; it is also the model shape for every motivated formatting constraint the skill writes, consumer named and consequence stated [BP-037, BP-039].
- Do not graft when: the destination is not one of those surfaces, on any profile. On any destination other than a speech engine the shape is adapted and the skill writes its own sentence, never pasting the TTS wording, and the adaptation is recorded in the Changed line.
- Text:
```text
Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them.
```

### role_python_coding_assistant
- Source: Prompting best practices, "Give Claude a role", the system parameter in every SDK sample
- Measured on: all current models
- Graft when: filling `<role>`; substitute the language, framework, or security domain detected in Step 1c, for example "specializing in PowerShell and Cortex the analytics platform the vendor query language" [BP-054, BP-055].
- Do not graft when: the request really is not general Python help, on any profile. The sentence stays verbatim only for general Python work; otherwise the pattern is kept and the domain replaced.
- Text:
```text
You are a helpful coding assistant specializing in Python.
```

### multidocument_structure
- Source: Prompting best practices, "Long context prompting", accordion "Example multidocument structure"
- Measured on: all current models
- Graft when: two or more input documents precede the query, or inputs total 20k tokens or more; the skeleton fills `<documents>` with sequential index attributes and the user's question follows in `<task>` [BP-060, BP-061, BP-067].
- Do not graft when: there is one short paste, on any profile; a single source can sit inline. The ordering has no model exception, so no profile takes the query first [BP-062].
- Note: the page prints this inside an accordion, so every line carries four spaces of MDX indentation; the block below is that text with the accordion indentation removed and its own internal indentation kept.
- Text:
```text
<documents>
  <document index="1">
    <source>annual_report_2023.pdf</source>
    <document_content>
      {{ANNUAL_REPORT}}
    </document_content>
  </document>
  <document index="2">
    <source>competitor_analysis_q2.xlsx</source>
    <document_content>
      {{COMPETITOR_ANALYSIS}}
    </document_content>
  </document>
</documents>

Analyze the annual report and competitor analysis. Identify strategic advantages and recommend Q3 focus areas.
```

### quote_extraction
- Source: Prompting best practices, "Long context prompting", accordion "Example quote extraction"
- Measured on: all current models
- Graft when: the row is long-document analysis and conclusions have to rest on cited source text; the structure is copied (role sentence, `<documents>`, a quote step into `<quotes>` tags, then a derived-output step into a second named tag) with the domain, sources, and tag names substituted [BP-072, BP-076, BP-078].
- Do not graft when: any profile, as literal content. The physician wording is the shape, not the text; grafting it unchanged into a security or engineering task misstates the role.
- Note: the page prints this inside an accordion with four spaces of MDX indentation, removed below.
- Text:
```text
You are an AI physician's assistant. Your task is to help doctors diagnose possible patient illnesses.

<documents>
  <document index="1">
    <source>patient_symptoms.txt</source>
    <document_content>
      {{PATIENT_SYMPTOMS}}
    </document_content>
  </document>
  <document index="2">
    <source>patient_records.txt</source>
    <document_content>
      {{PATIENT_RECORDS}}
    </document_content>
  </document>
  <document index="3">
    <source>patient01_appt_history.txt</source>
    <document_content>
      {{PATIENT01_APPOINTMENT_HISTORY}}
    </document_content>
  </document>
</documents>

Find quotes from the patient records and appointment history that are relevant to diagnosing the patient's reported symptoms. Place these in <quotes> tags. Then, based on these quotes, list all information that would help the doctor diagnose the patient's symptoms. Place your diagnostic information in <info> tags.
```

### model_identity
- Source: Prompting best practices, "Model self-knowledge", fence labelled "Sample prompt for model identity"
- Measured on: all current models
- Graft when: the deliverable is an application system prompt that needs correct self-identification; substitute the target model's display name from the alias table in `references/model-notes.md` section 3 [BP-059, BP-082].
- Do not graft when: the run is an in-session rearticulation on any profile. The session model already knows what it is, and the sentence would be noise.
- Text:
```text
The assistant is Claude, created by Anthropic. The current model is Claude Opus 5.
```

### model_string
- Source: Prompting best practices, "Model self-knowledge", fence labelled "Sample prompt for model string"
- Measured on: all current models
- Graft when: the deliverable is a system prompt for an LLM-powered app or a coding assistant that generates SDK calls; keep both halves, the overridable default and the exact string, and pin the target's own string [BP-084, BP-086].
- Do not graft when: the run is an in-session rearticulation on any profile, or the target's API string is not printed in the sources; in that case point at the models overview instead of asserting a string [BP-006].
- Text:
```text
When an LLM is needed, please default to Claude Opus 5 unless the user requests
otherwise. The exact model string for Claude Opus 5 is claude-opus-5.
```

### tool_use_summary
- Source: Prompting best practices, "Communication style and verbosity", fence labelled "Sample prompt"
- Measured on: all current models
- Graft when: the run involves tool calls and the user wants a report of the work done; it goes in `<execution_guidance>` [BP-092, BP-093].
- Do not graft when: a brevity qualifier would be attached to it on fable-5-1. On that profile it pairs with `progress_updates_line` and never with a keep-it-brief line, because narration-brevity language is what suppresses the updates in the first place [F51-35, BP-100]. On opus-5 prefer `o5_progress_updates`, which sets the same expectation with the cadence that page measured.
- Text:
```text
After completing a task that involves tool use, provide a quick summary of the work you've done.
```

### smoothly_flowing_prose_paragraphs (alias prose_paragraphs_positive)
- Source: Prompting best practices, "Control the format of responses", the two positive-framing try lines
- Measured on: all current models
- Graft when: `<output_format>` needs a positive statement of prose shape in place of a do-not-use-markdown prohibition, or the response has prose sections a parser or a reader must separate from code and lists [BP-103, BP-104, BP-105].
- Do not graft when: the deliverable is a table, a list the user asked for, or code, on any profile; and do not use the tag form when nothing downstream parses the response, where the plain sentence is enough [BP-106, BP-113].
- Note: the page renders the tag line MDX-escaped as `\<smoothly\_flowing\_prose\_paragraphs>`; the rendered text is below.
- Text:
```text
Your response should be composed of smoothly flowing prose paragraphs.
```
```text
Write the prose sections of your response in <smoothly_flowing_prose_paragraphs> tags.
```

### avoid_excessive_markdown_and_bullet_points
- Source: Prompting best practices, "Control the format of responses", fence labelled "Sample prompt"
- Measured on: all current models (the guide prints no model exception; the fable-5-1 exclusion below comes from that page, not from this block's provenance)
- Graft when: the deliverable is long-form prose (a report, a document, a technical explanation, an analysis) and the target is fable-5, opus-5, sonnet-5, opus-4-8, or legacy-4x; keep the wrapper tag so the executing turn recognises the block [BP-110, BP-111, BP-176].
- Do not graft when: the target is fable-5-1. That page's own section says to remove inherited anti-formatting language or replace it with a rule that says when formatting is appropriate, and the model already reaches for bold, headers, and lists less than earlier models did; use `formatting_in_chat_rule` instead. An anti-formatting block inherited from an older prompt is removed on that target rather than kept [F51-73, F51-74, BP-116]. The list exception holds on every profile: when the user asked for a list or a ranking, say so positively rather than grafting this block [BP-113].
- Text:
````text
<avoid_excessive_markdown_and_bullet_points>
When writing reports, documents, technical explanations, analyses, or any long-form
content, write in clear, flowing prose using complete paragraphs and sentences. Use
standard paragraph breaks for organization and reserve markdown primarily for `inline
code`, code blocks (```...```), and simple headings (## and ###). Avoid using **bold**
and *italics*.

DO NOT use ordered lists (1. ...) or unordered lists (*) unless: a) you're presenting
truly discrete items where a list format is the best option, or b) the user explicitly
requests a list or ranking

Instead of listing items with bullets or numbers, incorporate them naturally into
sentences. This guidance applies especially to technical writing. Using prose instead of
excessive formatting will improve user satisfaction. NEVER output a series of overly
short bullet points.

Your goal is readable, flowing text that guides the reader naturally through ideas
rather than fragmenting information into isolated points.
</avoid_excessive_markdown_and_bullet_points>
````

### plain_text_math
- Source: Prompting best practices, "LaTeX output", fence labelled "Sample prompt"
- Measured on: all current models
- Graft when: math appears in the deliverable and the destination does not render LaTeX (a terminal, a plain file, an email, a ticket); it goes in `<output_format>` [BP-118, BP-119, BP-120].
- Do not graft when: the surface renders LaTeX, on any profile. There is no profile exception in either direction; the destination decides.
- Also in templates/rearticulated-prompt.md.
- Text:
```text
Format your response in plain text only. Do not use LaTeX, MathJax, or any markup
notation such as \( \), $, or \frac{}{}. Write all math expressions using standard text
characters (e.g., "/" for division, "*" for multiplication, and "^" for exponents).
```

### professional_presentation
- Source: Prompting best practices, "Document creation", fence labelled "Sample prompt"
- Measured on: all current models
- Graft when: the request is a presentation or slide deck; `[topic]` is the fill slot and goes into `<task>`. Pair it with a frontend aesthetics snippet when visual quality matters, choosing the long or the short form by target.
- Do not graft when: the deliverable is a document rather than a deck, on any profile; the animation clause misdirects a memo or a report.
- Text:
```text
Create a professional presentation on [topic]. Include thoughtful design elements,
visual hierarchy, and engaging animations where appropriate.
```

### no_preamble
- Source: Prompting best practices, "Migrating away from prefilled responses", the Eliminating preambles migration note
- Measured on: all current models
- Graft when: the deliverable should open with its own content (a summary, extracted data, generated text); it goes in `<output_format>` paired with a positive lead such as "Begin with the first sentence of the summary." because the guide frames the snippet itself in the negative [BP-134, BP-135, BP-103].
- Do not graft when: the reply is conversational or the user wants an orienting sentence first, on any profile. On fable-5-1 do not stack it with a brevity line; suppressing the opening line and the narration together is what leaves a turn silent [F51-35].
- Also in templates/rearticulated-prompt.md.
- Text:
```text
Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc.
```

### continuation_from_interrupted
- Source: Prompting best practices, "Migrating away from prefilled responses", the continuation migration note
- Measured on: all current models
- Graft when: the request is to resume output that was cut off; the fill slot takes the literal final text of the interrupted response and the whole thing goes in the user message, which is `<task>` here [BP-139, BP-140].
- Do not graft when: the target is 4.6 or later or Mythos Preview and the intent was a trailing assistant turn. Last-turn prefill is unsupported there, and this snippet is the sanctioned replacement rather than something to add alongside it [BP-124, BP-128].
- Note: the page renders it MDX-escaped as `\`\[previous\_response]\``; the rendered text is below, with the fill slot in backticks.
- Text:
```text
Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off.
```

### change_this_function
- Source: Prompting best practices, "Tool usage", accordion "Example: Explicit instructions", the more-effective side
- Measured on: all current models
- Graft when: the raw request is suggestion-phrased ("can you suggest some changes to improve this function") under the act posture; this is the canonical imperative shape the rewritten `<task>` opens with [BP-145, BP-146, BP-149].
- Do not graft when: the posture is assess on any profile. Converting a review request into an imperative changes the deliverable, which is the one thing Step 1d exists to prevent.
- Text:
```text
Change this function to improve its performance.
```

### make_these_edits
- Source: Prompting best practices, "Tool usage", accordion "Example: Explicit instructions", the second more-effective form
- Measured on: all current models
- Graft when: the raw request enumerates edits to a named component or flow but hedges on whether to apply them; it is the second canonical imperative shape for `<task>` [BP-145, BP-149].
- Do not graft when: the posture is assess, or no concrete edits were named, on any profile; without named edits the step is a discovery step, not an edit step [BP-154].
- Text:
```text
Make these edits to the authentication flow.
```

### Counter-examples (never grafted)

Two source fences are held here because other files cite them by ID, not because either is ever inserted into a prompt. Both are the guide's before case: the wording a conversion replaces.

#### less_effective_suggest_changes
- Source: Prompting best practices, "Tool usage", accordion "Example: Explicit instructions", the less-effective side
- Measured on: all current models
- Graft when: never. It is the pattern Step 4 detects and converts to `change_this_function` or `make_these_edits` under the act posture [BP-146, BP-148 to BP-151].
- Do not graft when: any profile, ever. It is the before case of the guide's own conversion and is held only so Step 4 can name what it replaced; if it appears in a pasted prompt it is converted, never carried through [BP-146, BP-148 to BP-151].
- Text:
```text
Can you suggest some changes to improve this function?
```

#### less_effective_never_ellipses
- Source: Prompting best practices, "Add context to improve performance", the without-context example
- Measured on: all current models
- Graft when: never. It is the unmotivated all-caps prohibition that `tts_no_ellipses` replaces, consumer named and consequence stated [BP-037, BP-038].
- Do not graft when: any profile, ever. The unmotivated all-caps prohibition is what the skill removes; the replacement is `tts_no_ellipses` with the consumer named and the consequence stated [BP-037, BP-038].
- Text:
```text
NEVER use ellipses
```

### use_this_tool_when
- Source: Prompting best practices, "Tool usage", the note on emphatic tool directives
- Measured on: all current models
- Graft when: the raw request or a pasted prompt carries an emphatic tool mandate; the substitution is recorded in the Changed line and the plain conditional form goes into the prompt [BP-162, BP-163, BP-354].
- Do not graft when: any profile, as prompt content. It is a substitution rule, not a block. Opus 4.6 over-triggers on the emphatic form, which is why the conversion is not optional there [BP-161, BP-355].
- Note: the graft form is the second half of the sentence, "Use this tool when...", with the actual condition appended.
- Text:
```text
Where you might have said "CRITICAL: You MUST use this tool when...", you can use more normal prompting like "Use this tool when...".
```

### default_to_action
- Source: Prompting best practices, "Tool usage", fence labelled "Sample prompt for proactive action"
- Measured on: all current models
- Graft when: the posture is act; it goes in `<execution_guidance>` with its wrapper tag kept, and it is one of exactly one posture snippet per prompt [BP-152, BP-153, BP-156].
- Do not graft when: the posture is assess, on any profile, and never alongside `do_not_act_before_instructions`; the two contradict each other and the pair leaves the posture undefined.
- Also in templates/rearticulated-prompt.md.
- Text:
```text
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is
unclear, infer the most useful likely action and proceed, using tools to discover any
missing details instead of guessing. Try to infer the user's intent about whether a tool
call (e.g., file edit or read) is intended or not, and act accordingly.
</default_to_action>
```

### do_not_act_before_instructions
- Source: Prompting best practices, "Tool usage", fence labelled "Sample prompt for conservative action"
- Measured on: all current models
- Graft when: the posture is assess, which covers review, audit, explain, and compare requests with no act signal; it goes in `<execution_guidance>` with its wrapper kept [BP-156, BP-157].
- Do not graft when: the posture is act, on any profile, and never alongside `default_to_action`. Under assess the autonomy blocks (`operating_autonomously`, `delivering_work`, `f5_autonomous_reminder`) are omitted too, because they push in the opposite direction.
- Also in templates/rearticulated-prompt.md.
- Text:
```text
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed to make
changes. When the user's intent is ambiguous, default to providing information, doing
research, and providing recommendations rather than taking action. Only proceed with
edits, modifications, or implementations when the user explicitly requests them.
</do_not_act_before_instructions>
```

### use_parallel_tool_calls
- Source: Prompting best practices, "Optimize parallel tool calling", fence labelled "Sample prompt for maximum parallel efficiency"
- Measured on: all current models
- Graft when: the task fans out across several independent reads, searches, or commands and throughput matters; keep the wrapper tag [BP-168, BP-169, BP-176].
- Do not graft when: the target system fails under concurrency, where `reduce_parallel_execution` takes its place; and not alongside `batch_nudge` on fable-5-1, where batching is stated once, because the harness already injects a parallel-calls reminder and a third copy is padding [F51-44, BP-173].
- Text:
```text
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool
calls, make all of the independent tool calls in parallel. Prioritize calling tools
simultaneously whenever the actions can be done in parallel rather than sequentially.
For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into
context at the same time. Maximize use of parallel tool calls where possible to increase
speed and efficiency. However, if some tool calls depend on previous calls to inform
dependent values like the parameters, do NOT call these tools in parallel and instead
call them sequentially. Never use placeholders or guess missing parameters in tool
calls.
</use_parallel_tool_calls>
```

### reduce_parallel_execution
- Source: Prompting best practices, "Optimize parallel tool calling", fence labelled "Sample prompt to reduce parallel execution"
- Measured on: all current models
- Graft when: the target system is rate-limited, throttling, or fragile, or the user asked for careful step-by-step operation; in this workspace the live analytics platform returns 500s at volume and concurrency, so it fires on tenant-query rows [BP-173].
- Do not graft when: nothing in the environment fails under concurrency, on any profile; it costs round trips for no gain and contradicts `use_parallel_tool_calls` and `batch_nudge`, which are then omitted.
- Text:
```text
Execute operations sequentially with brief pauses between each step to ensure stability.
```

### targeted_tool_trigger
- Source: Prompting best practices, "Overthinking and excessive thoroughness", the replace-blanket-defaults bullet
- Measured on: all current models
- Graft when: `<execution_guidance>` needs guidance for an optional tool (search, grep, subagents, web fetch), and always in place of a "Default to using X" or "If in doubt, use X" line found in the raw request or a pasted prompt; fill the slot and name the benefit, for example "Use Grep when it would enhance your understanding of the code paths involved." [BP-180, BP-181].
- Do not graft when: any profile, in the blanket-default form. The blanket form is the anti-pattern this replaces.
- Note: the page renders the slot MDX-escaped as `\[tool]`; the rendered text is below.
- Text:
```text
Use [tool] when it would enhance your understanding of the problem.
```

### commit_to_approach
- Source: Prompting best practices, "Overthinking and excessive thoroughness", fence labelled "Sample prompt"
- Measured on: all current models
- Graft when: several approaches are viable, the row is agentic long-horizon, speed or cost is stressed, or the user reports flip-flopping and over-deliberation [BP-186, BP-187]. The guide states the symptom for Opus 4.6, so on that target it is the named remedy after a lower effort setting, and elsewhere it is the guide's general block [BP-177 to BP-179, BP-185].
- Do not graft when: the deliverable is a comparison of options, on any profile; the request there is the survey the snippet suppresses. On fable-5, `f5_act_when_ready` covers the same ground in the wording that page measured, and only one of the two is grafted [F5-24].
- Text:
```text
When you're deciding how to approach a problem, choose an approach and commit to it.
Avoid revisiting decisions unless you encounter new information that directly
contradicts your reasoning. If you're weighing two approaches, pick one and see it
through. You can always course-correct later if the chosen approach fails.
```

### reflect_after_tool_results
- Source: Prompting best practices, "Leverage thinking & interleaved thinking capabilities", the guide-Claude's-thinking-behavior fence
- Measured on: all current models (the guide prints no model exception; the Fable-family and opus-5 exclusions below come from those pages, not from this block's provenance)
- Graft when: the row is multistep tool use (code change, research, agentic long-horizon) and the target is sonnet-5, opus-4-8, or legacy-4x [BP-193, BP-204].
- Do not graft when: the target is fable-5-1, fable-5, or opus-5. Prompts, skills, or harness instructions that tell that model to echo, transcribe, or explain its internal reasoning as response text can trigger the `reasoning_extraction` refusal category and cause elevated fallbacks to Claude Opus 4.8, so reflection and show-your-thinking lines are stripped rather than reworded; reasoning visibility there comes from adaptive thinking's structured thinking blocks and a send-to-user tool [F5-71, F5-72]. On fable-5-1 reasoning choreography is stripped as well, keeping at most a general `think_thoroughly` for complex tasks, and thinking is always on so the block buys nothing [BP-220]. On opus-5 it reads as a verification instruction and belongs to the removal list [O5-43].
- Text:
```text
After receiving tool results, carefully reflect on their quality and determine optimal
next steps before proceeding. Use your thinking to plan and iterate based on this new
information, and then take the best next action.
```

### think_thoroughly
- Source: Prompting best practices, "Leverage thinking & interleaved thinking capabilities", the prefer-general-instructions bullet
- Measured on: all current models with thinking on
- Graft when: the task benefits from deeper reasoning and a hand-written step-by-step reasoning plan would otherwise be written; the general instruction often produces better reasoning than the plan, so the plan is dropped and this is kept [BP-221, BP-222].
- Do not graft when: the target is Opus 4.5 with thinking off, where the word "think" is itself the trigger and consider, evaluate, or reason through is substituted [BP-235, BP-236]. Numbered work steps whose order or completeness matters are not reasoning choreography and stay on every target. It also adds nothing to a lookup or a one-line edit, where the prompt stays short [BP-196, BP-206].
- Text:
```text
think thoroughly
```

### think_only_when_useful (aliases s5_thinking_trigger_guard, o48_thinking_steer)
- Source: three pages print the same guard. Prompting best practices, "Leverage thinking & interleaved thinking capabilities", fence labelled "Sample prompt" (`think_only_when_useful`); Prompting Claude Sonnet 5, "Calibrating effort and thinking depth" (`s5_thinking_trigger_guard`, S5-29); Prompting Claude Opus 4.8, "Calibrating effort and thinking depth" (`o48_thinking_steer`, O48-26)
- Measured on: all current models with adaptive thinking, and specifically Claude Sonnet 5 and Claude Opus 4.8 on their own pages
- Graft when: adaptive thinking triggers more often than the use case warrants, which happens with large or complex system prompts, and latency is the stated concern [BP-207, S5-29, O48-24].
- Do not graft when: latency is not the stated concern, on any profile; it is never a default. Do not graft on fable-5-1 or fable-5, where thinking is always on, adaptive is the only mode, and it cannot be disabled, so the guard has nothing to steer [BP-220, F5-08]; use it there only if the user explicitly asks for lower latency. Do not graft on opus-5 when thinking is disabled, where do-not-think rules increase internal tag leakage and `o5_thinking_disabled_mitigation` is the sanctioned block instead [O5-66, O5-68]. Do not graft on Opus 4.5 with thinking off, because of the word "think" [BP-236].
- Note: the three pages punctuate the same sentence differently, so each is fenced separately and grafted from the target's own page. The guide uses a hyphen and hard line breaks, Sonnet 5 a comma, Opus 4.8 an em dash.
- Text (Prompting best practices):
```text
Thinking adds latency and should only be used when it will meaningfully improve
answer quality - typically for problems that require multistep reasoning. When in
doubt, respond directly.
```
- Text (Prompting Claude Sonnet 5):
```text
Thinking adds latency and should only be used when it will meaningfully improve answer quality, typically for problems that require multistep reasoning. When in doubt, respond directly.
```
- Text (Prompting Claude Opus 4.8):
```text
Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multistep reasoning. When in doubt, respond directly.
```

### self_check_verify
- Source: Prompting best practices, "Leverage thinking & interleaved thinking capabilities", the Ask-Claude-to-self-check bullet
- Measured on: all current models (the guide prints no model exception; the opus-5 exclusion below comes from that page, not from this block's provenance)
- Graft when: filling `<verification>` on fable-5-1, fable-5, sonnet-5, opus-4-8, or legacy-4x, with the slot replaced by the concrete checks from `<success_criteria>`: the tests to run, the numbers to reconcile, the files that must exist, a diff that touches only the named files. The guide says this catches errors reliably, especially for coding and math [BP-229, BP-230, BP-231].
- Do not graft when: the target is opus-5. That model verifies its own work well without explicit instruction, and verification instructions carried over from prompts tuned for earlier models cause over-verification that adds tokens and latency; when migrating, such instructions are removed rather than rewritten. The `<verification>` tag is omitted entirely on that target, `<success_criteria>` stays, Step 7 still verifies against it, and the prompt states deliverable length, task scope, and subagent policy explicitly instead [BP-232, BP-233, O5-43, O5-57]. The same rule retires `f5_self_verification_interval` and any double-check line on that target.
- Note: the page renders the slot MDX-escaped as `\[test criteria]`; the rendered text is below.
- Also in templates/rearticulated-prompt.md.
- Text:
```text
Before you finish, verify your answer against [test criteria].
```

### context_compaction_persistence
- Source: Prompting best practices, "Long-horizon reasoning and state tracking", "Context awareness and multiwindow workflows", fence labelled "Sample prompt"
- Measured on: all current models, and named for the context-aware models Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, and Claude Haiku 4.5, which track their remaining token budget [BP-241, BP-246]
- Graft when: the row is agentic long-horizon and the run happens in a compacting harness such as Claude Code, or the multi-session signal fired; it goes in `<execution_guidance>` [BP-244, BP-246].
- Do not graft when: the run is a single short turn, on any profile. On fable-5 prefer `f5_ample_context`, and only when the harness actually shows a remaining-token countdown to the model, because surfacing explicit context-budget counts is what triggers the early stopping in the first place; never quote a figure [F5-53, F5-54, F5-55].
- Text:
```text
Your context window will be automatically compacted as it approaches its limit, allowing
you to continue working indefinitely from where you left off. Therefore, do not stop
tasks early due to token budget concerns. As you approach your token budget limit, save
your current progress and state to memory before the context window refreshes. Always be
as persistent and autonomous as possible and complete tasks fully, even if the end of
your budget is approaching. Never artificially stop any task early regardless of the
context remaining.
```

### tests_unacceptable_to_remove
- Source: Prompting best practices, "Workflows across multiple context windows", item 2
- Measured on: all current models
- Graft when: the task touches a test suite, above all in multi-session work; it goes in `<constraints>` verbatim inside its own tag [BP-250, BP-311].
- Do not graft when: no tests exist, on any profile. It is quoted, not rewritten into positive form; the positive-framing rule governs what the skill writes, not what it quotes [BP-302, BP-309].
- Text:
```text
It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality.
```

### fresh_start_pwd
- Source: Prompting best practices, "Workflows across multiple context windows", item 4 "Starting fresh versus compacting", first prescriptive line
- Measured on: all current models
- Graft when: a multi-session task is resumed in a fresh window; it is step 1 of `<task>`, ahead of state recovery [BP-254].
- Do not graft when: the session is continuing rather than restarting, on any profile, or the task legitimately spans directories, where the directory restriction would be wrong.
- Text:
```text
Call pwd; you can only read and write files in this directory.
```

### fresh_start_review_state
- Source: Prompting best practices, "Workflows across multiple context windows", item 4, second prescriptive line
- Measured on: all current models
- Graft when: a multi-session task is resumed and state files exist; substitute the project's actual state file names [BP-255].
- Do not graft when: no state files exist, on any profile; naming files that are not there sends the run looking for them.
- Text:
```text
Review progress.txt, tests.json, and the git logs.
```

### fresh_start_integration_test
- Source: Prompting best practices, "Workflows across multiple context windows", item 4, third prescriptive line
- Measured on: all current models
- Graft when: a multi-session coding task is resumed; it is the gate in `<task>` between state recovery and new work [BP-256].
- Do not graft when: the task is not coding, or no runnable baseline exists, on any profile.
- Text:
```text
Manually run through a fundamental integration test before moving on to implementing new features.
```

### spend_entire_context
- Source: Prompting best practices, "Workflows across multiple context windows", item 6, fence labelled "Sample prompt"
- Measured on: all current models, named for the context-aware Claude Sonnet 5, Sonnet 4.6, Sonnet 4.5, and Haiku 4.5 [BP-241, BP-261]. The guide prints the block itself under a general multiwindow subsection that names no model, so it is available on multi-window work for any target the Do-not-graft line does not exclude
- Graft when: the row is agentic long-horizon and the many-steps or multi-session signal fired; it goes in `<execution_guidance>` [BP-261].
- Do not graft when: the task is short or narrow, on any profile; it invites the run to keep going where the scope says stop. Do not graft on opus-5 at all, whose page says the 1M window holds instruction following throughout and needs no context scaffold [O5-22], nor on the Opus models in legacy-4x or on Mythos Preview, which the guide does not name as context-aware. On fable-5 and fable-5-1 use `f5_ample_context` instead, and only when the harness shows the model a countdown, because explicit context-budget language is itself what triggers the early stopping [F5-53, F5-54, F5-55].
- Text:
```text
This is a very long task, so it may be beneficial to plan out your work clearly. It's
encouraged to spend your entire output context working on the task - just make sure you
don't run out of context with significant uncommitted work. Continue working
systematically until you have completed this task.
```

### tests_json_example
- Source: Prompting best practices, "State management best practices", accordion "Example: State tracking", the `tests.json` block
- Measured on: all current models
- Graft when: a multi-session coding task tracks tests in a structured file; it is referenced from `<execution_guidance>` as the schema to follow [BP-262, BP-263].
- Do not graft when: the task keeps no test state, on any profile.
- Note: the page prints this inside the "Example: State tracking" accordion with two spaces of MDX indentation, removed below.
- Text:
```json
{
  "tests": [
    { "id": 1, "name": "authentication_flow", "status": "passing" },
    { "id": 2, "name": "user_management", "status": "failing" },
    { "id": 3, "name": "api_endpoints", "status": "not_started" }
  ],
  "total": 200,
  "passing": 150,
  "failing": 25,
  "not_started": 25
}
```

### progress_notes_example
- Source: Prompting best practices, "State management best practices", accordion "Example: State tracking", the progress notes block
- Measured on: all current models
- Graft when: a multi-session task keeps a freeform progress notes file; the shape to follow is done, next, notes [BP-262, BP-263].
- Do not graft when: the task is a single turn, on any profile. On fable-5-1 the six items of `compaction_summary_instruction` shape a handoff note better than this three-line example when the note has to survive a compaction [F51-105].
- Note: the page prints this inside the "Example: State tracking" accordion with two spaces of MDX indentation, removed below.
- Text:
```text
// Progress notes (progress.txt)
Session 3 progress:
- Fixed authentication token validation
- Updated user model to handle edge cases
- Next: investigate user_management test failures (test #2)
- Note: Do not remove tests as this could lead to missing functionality
```

### autonomy_safety_confirmation
- Source: Prompting best practices, "Balancing autonomy and safety", fence labelled "Sample prompt"
- Measured on: all current models, and named for Claude Opus 4.6, which may take hard-to-reverse actions without guidance [BP-269, BP-271]
- Graft when: the side-effect signal fired in Step 1f (git push, force, reset, rebase, amend, branch deletion; rm -rf or recursive removal; SQL DROP, DELETE, TRUNCATE; a write to a live system such as the analytics insert endpoints, ServiceNow, or SCM; send, email, notify, comment, publish, deploy, release; service restart, config or registry edit; cron or scheduled agents; edits to `.claude` settings, hooks, or CLAUDE.md); it goes in `<execution_guidance>` verbatim inside its own tag, with the flagged steps also marked `[confirm]` in `<task>` [BP-270 to BP-276].
- Do not graft when: no side effect is in play, on any profile. On fable-5-1 it is not a substitute for `operating_autonomously`: when both apply, the autonomy block is grafted whole and one sentence listing the required confirmations follows its first paragraph, because the page says to keep that opening as written and add the confirmations after it [F51-91, F51-92].
- Text:
```text
Consider the reversibility and potential impact of your actions. You are encouraged to
take local, reversible actions like editing files or running tests, but for actions that
are hard to reverse, affect shared systems, or could be destructive, ask the user before
proceeding.

Examples of actions that warrant confirmation:
- Destructive operations: deleting files or branches, dropping database tables, rm -rf
- Hard to reverse operations: git push --force, git reset --hard, amending published commits
- Operations visible to others: pushing code, commenting on PRs/issues, sending
messages, modifying shared infrastructure

When encountering obstacles, do not use destructive actions as a shortcut. For example,
don't bypass safety checks (e.g. --no-verify) or discard unfamiliar files that may be
in-progress work.
```

### complex_research (alias structured_research)
- Source: Prompting best practices, "Research and information gathering", fence labelled "Sample prompt"
- Measured on: all current models
- Graft when: the row is research and the task is complex, meaning several sources, competing explanations, or a claim that has to be confirmed across sources; it goes in `<execution_guidance>`, and `<success_criteria>` adds cross-source confirmation of key claims [BP-278 to BP-281].
- Do not graft when: the question is a lookup, on any profile; the hypothesis tree is overhead there. Do not graft the self-critique clause on fable-5, where reflection instructions risk the `reasoning_extraction` refusal; use `f5_ground_progress` for the calibration half instead [F5-38, F5-71].
- Note: `templates/rearticulated-prompt.md` cites this snippet as `structured_research`; the two names are the same block.
- Text:
```text
Search for this information in a structured way. As you gather data, develop several
competing hypotheses. Track your confidence levels in your progress notes to improve
calibration. Regularly self-critique your approach and plan. Update a hypothesis tree or
research notes file to persist information and provide transparency. Break down this
complex research task systematically.
```

### subagent_usage_policy
- Source: Prompting best practices, "Subagent orchestration", fence labelled "Sample prompt"
- Measured on: all current models, and named for Claude Opus 4.6, which has a strong subagent predilection [BP-286, BP-290]
- Graft when: the row is agentic long-horizon and delegation is possible; the sentence "continue independent work while subagents run and collect results afterward" follows it, because the lead agent should not idle [BP-289, BP-290, F51-143].
- Do not graft when: the target is opus-5 in interactive Claude Code, where the `claude_code` preset already injects a delegation instruction, and where `o5_delegation_guidance` is the wording that page measured for authored prompts and SDK runs [O5-51, O5-54]. On opus-4-8 prefer `o48_subagent_guidance`, which addresses the opposite tendency: that model spawns fewer subagents by default [O48-43, O48-45]. Do not graft it at all on fable-5: that page says the model dispatches parallel subagents more readily than prior models and asks for frequent delegation with explicit guidance, so a damping policy points the wrong way; `f5_delegate_subagents` is the measured replacement and is grafted instead of this block, never alongside it [F5-41, F5-42, F5-44].
- Text:
```text
Use subagents when tasks can run in parallel, require isolated context, or involve
independent workstreams that don't need to share state. For simple tasks, sequential
operations, single-file edits, or tasks where you need to maintain context across steps,
work directly rather than delegating.
```

### temp_file_cleanup
- Source: Prompting best practices, "Reduce file creation in agentic coding", fence labelled "Sample prompt"
- Measured on: all current models
- Graft when: the row is code change or agentic long-horizon; it goes in `<execution_guidance>` and nowhere else, so the cleanup expectation is stated once, and Step 7 removes the scratch files before the recap [BP-295, BP-298, BP-299].
- Do not graft when: the deliverable is the file the user asked for, on any profile; scratch means scratch. In this workspace scratch files go to the scratchpad directory, which the cleanup then clears.
- Also in templates/rearticulated-prompt.md.
- Text:
```text
If you create any temporary new files, scripts, or helper files for iteration, clean up
these files by removing them at the end of the task.
```

### minimize_overengineering
- Source: Prompting best practices, "Overeagerness", fence labelled "Sample prompt"
- Measured on: all current models, and named for Claude Opus 4.5 and Claude Opus 4.6, which overengineer [BP-300, BP-302]
- Graft when: the row is code change and the target is opus-5, sonnet-5, opus-4-8, or legacy-4x (chiefly Opus 4.6 and Opus 4.5); it goes in `<constraints>` verbatim inside its own tag [BP-300 to BP-302].
- Do not graft when: the target is fable-5-1, where `keep_changes_to_task` is the block that page measured for the same symptom and covers scope, tests, and ambiguity together [F51-117]; or fable-5, where `f5_scope_discipline` is the measured wording and one principle-level instruction beats an enumerated do-and-don't list [F5-31, F5-32].
- Text:
```text
Avoid over-engineering. Only make changes that are directly requested or clearly
necessary. Keep solutions simple and focused:

- Scope: Don't add features, refactor code, or make "improvements" beyond what was
asked. A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need
extra configurability.

- Documentation: Don't add docstrings, comments, or type annotations to code you didn't
change. Only add comments where the logic isn't self-evident.

- Defensive coding: Don't add error handling, fallbacks, or validation for scenarios
that can't happen. Trust internal code and framework guarantees. Only validate at system
boundaries (user input, external APIs).

- Abstractions: Don't create helpers, utilities, or abstractions for one-time
operations. Don't design for hypothetical future requirements. The right amount of
complexity is the minimum needed for the current task.
```

### general_purpose_solution
- Source: Prompting best practices, "Avoid focusing on passing tests and hardcoding", fence labelled "Sample prompt"
- Measured on: all current models
- Graft when: the row is code change and tests are present or the task is algorithmic; it goes in `<constraints>`, and it carries the escape clause the skill relies on, that an infeasible task or an incorrect test is reported rather than worked around [BP-309, BP-311, BP-312].
- Do not graft when: no tests and no algorithm are involved, on any profile. It is quoted, not rewritten into positive form.
- Text:
```text
Please write a high-quality, general-purpose solution using the standard tools
available. Do not create helper scripts or workarounds to accomplish the task more
efficiently. Implement a solution that works correctly for all valid inputs, not just
the test cases. Do not hard-code values or create solutions that only work for specific
test inputs. Instead, implement the actual logic that solves the problem generally.

Focus on understanding the problem requirements and implementing the correct algorithm.
Tests are there to verify correctness, not to define the solution. Provide a principled
implementation that follows best practices and software design principles.

If the task is unreasonable or infeasible, or if any of the tests are incorrect, please
inform me rather than working around them. The solution should be robust, maintainable,
and extendable.
```

### investigate_before_answering
- Source: Prompting best practices, "Minimizing hallucinations in agentic coding", fence labelled "Sample prompt"
- Measured on: all current models
- Graft when: the request names files or asks about a codebase, under either posture; keep the wrapper tag [BP-314, BP-315, BP-316].
- Do not graft when: no files and no codebase are involved, on any profile. Its all-caps MUST and BEFORE stay as quoted; the plain-wording rule applies to what the skill writes, not to a grafted block [BP-302].
- Also in templates/rearticulated-prompt.md.
- Text:
```text
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file,
you MUST read the file before answering. Make sure to investigate and read relevant
files BEFORE answering questions about the codebase. Never make any claims about code
before investigating unless you are certain of the correct answer - give grounded and
hallucination-free answers.
</investigate_before_answering>
```

### frontend_aesthetics
- Source: Prompting best practices, "Frontend design", fence labelled "Sample prompt for frontend aesthetics"
- Measured on: the guide's section names Claude Opus 4.5 and Claude Opus 4.6; the block is the guide's own system prompt snippet for all models it covers
- Graft when: the row is frontend or design, the verb is build or restyle, and the target is legacy-4x (stated for Opus 4.6 and Opus 4.5, applied to the other five there by analogy with the assumption recorded); it is placed ahead of the task-specific instructions because the guide frames it as system prompt content, with the wrapper tag kept [BP-330, BP-176, BP-025].
- Do not graft when: the target is opus-4-8, sonnet-5, opus-5, fable-5-1, or fable-5. The first two pages replace the long block with `frontend_aesthetics_short`, paired with a concrete spec or the propose-directions snippet, and the long version is not what those pages measured [O48-55, O48-57, S5-57, S5-58]; opus-5 inherits the Opus 4.8 baseline, and fable-5-1 and fable-5 both take the short block with an Assumed entry, because each newer model needs less frontend prompting and a block written for Opus 4.5 and Opus 4.6 is the kind of prior-model prescription the Fable 5 page says to remove [F5-19, F5-70, O48-55]. Do not graft when a loaded skill already covers the step either: write "Invoke frontend-design before <step>" in `<execution_guidance>` instead of pasting a duplicate [BP-342].
- Note: S5.json S5-58 and O48.json O48-57 label the short Sonnet 5 and Opus 4.8 block with the snippet_id `frontend_aesthetics`. That ID resolves to `frontend_aesthetics_short`, not to this section; this long block is the guide's own text and is never what S5-58 or O48-57 means.
- Text:
```text
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this
creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive
frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic
fonts like Arial and Inter; opt instead for distinctive choices that elevate the
frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency.
Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw
from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only
solutions for HTML. Use Motion library for React when available. Focus on high-impact
moments: one well-orchestrated page load with staggered reveals (animation-delay)
creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer
CSS gradients, use geometric patterns, or add contextual effects that match the overall
aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the
context. Vary between light and dark themes, different fonts, different aesthetics. You
still tend to converge on common choices (Space Grotesk, for example) across
generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>
```

## Fable 5.1

Measured on Claude Fable 5.1 and Claude Mythos 5.1, whose page covers both names (F51-01, F51-04). The page is organised by symptom: diagnose by what is observed and graft the matching section's block rather than adding every block at once [F51-05].

### progress_updates_line
- Source: Prompting Claude Fable 5.1, "Ask for user-facing progress updates" (F51-36, F51-37)
- Measured on: Claude Fable 5.1
- Graft when: every tool-using run on this target, as the first block of `<execution_guidance>`. Its closing clause (what you found, what you did, what is next) is the shape of the Step 7 recap [F51-37, BP-089].
- Do not graft when: the target is sonnet-5 or opus-4-8, whose pages say progress updates come naturally and that a forced cadence such as "After every 3 tool calls, summarize progress" is unnecessary [S5-40, O48-33]; or opus-5, where `o5_progress_updates` is the measured cadence [O5-36]. No brevity qualifier is ever attached to it, and any inherited "hold all findings for the final response" or "keep progress text brief" line is removed before it is added [F51-35, BP-100]. Do not turn it into a counted interval on this target either; it asks for an opening line, updates while working, and a standalone recap, not a tool-call quota.
- Also in templates/rearticulated-prompt.md.
- Text:
```text
Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so a reader who only sees the last message has the full picture.
```

### tool_output_hidden_note
- Source: Prompting Claude Fable 5.1, "Ask for user-facing progress updates", the collapsed-tool-output note (F51-38, F51-39)
- Measured on: Claude Fable 5.1
- Graft when: the product collapses or hides tool output; the page delivers it as a turn-scoped system message (`clear_at: "next_user_message"`, beta header `mid-conversation-system-clear-at-2026-08-21`). In this skill it is adopted as Standing rule 8 rather than grafted per prompt, and it fires as prompt content only when the deliverable is a harness [F51-131, F51-38].
- Do not graft when: the surface shows full tool output, on any profile; and it is not a licence to run commands in order to display their output, which is the behaviour it exists to prevent.
- Text:
```text
Only you see that command's output — the user's terminal shows at most a few lines of it. If the user needs to read any of it, put it in your reply.
```

### batch_nudge
- Source: Prompting Claude Fable 5.1, "Batch independent tool calls in agent loops" (F51-43, F51-44)
- Measured on: Claude Fable 5.1
- Graft when: every tool-using run on this target, as the last line of the whole prompt. In an API harness a fresh copy is appended each turn as a turn-scoped system message, and the earlier copies are left byte-for-byte where they are; without the beta header the sentence goes in a text block after the `tool_result` blocks in the same user message [F51-45 to F51-52].
- Do not graft when: `reduce_parallel_execution` applies, because the target system fails under concurrency; and not stacked with `use_parallel_tool_calls`, because batching is stated once and the harness already injects a parallel-calls reminder [BP-173]. On other profiles use `use_parallel_tool_calls`, which is the guide's block for the same behaviour.
- Also in templates/rearticulated-prompt.md.
- Text:
```text
First privately list what you need next; then request every item that doesn't depend on another's result in this one response.
```

### mannered_prose_definition
- Source: Prompting Claude Fable 5.1, "Writing density" (F51-67, F51-68)
- Measured on: Claude Fable 5.1
- Graft when: the deliverable is writing (a report, a memo, a summary) and the prose runs long and dense; the page prefers it in a user message over the system prompt, and here it goes in `<output_format>` alongside a statement of how long sentences and paragraphs should run [F51-67, F51-69].
- Do not graft when: the prompt is already long, where `mannered_prose_short` is the page's own short version; or the deliverable is code or a table, on any profile.
- Text:
```text
Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a parameter worth varying," the mannered writer produces "a dial worth turning." Instead of "this point still matters," they write "this point earns its keep." The phrases exist to display the writer, not to convey the idea, and readers can tell. That is why mannered prose irritates: it makes the reader work harder so the writer can perform. It is also imprecise. Metaphors drag in connotations the writer did not choose and cannot control. The fix is to say what you mean. When a literal phrase is available, use it.
```

### mannered_prose_short
- Source: Prompting Claude Fable 5.1, "Writing density", the short version (F51-69, F51-70)
- Measured on: Claude Fable 5.1
- Graft when: the deliverable is writing and the prompt is already long; the page says the short version also tends to work [F51-70].
- Do not graft when: a full definition would land better and there is room for it, where `mannered_prose_definition` is preferred. It is a density instruction, not a conciseness instruction, so it is not a way to smuggle a narration-brevity line onto this target [F51-35, BP-100].
- Also in templates/rearticulated-prompt.md.
- Text:
```text
Please remove all mannered prose.
```

### formatting_in_chat_rule
- Source: Prompting Claude Fable 5.1, "Formatting in chat" (F51-73, F51-74)
- Measured on: Claude Fable 5.1
- Graft when: the deliverable is chat-style or long-form on this target, and as the replacement for any anti-formatting block inherited from a prompt written for an earlier model; it goes in `<output_format>` alongside a positive statement of when lists, headers, or tables are wanted, because this model reaches for them less [F51-72, F51-74, BP-116].
- Do not graft when: the target is not fable-5-1, where `avoid_excessive_markdown_and_bullet_points` addresses the opposite tendency. A minimal-formatting request the user made themselves stays in force: the block itself honours it.
- Also in templates/rearticulated-prompt.md.
- Text:
```text
Use lists and bullet points when asked to, or when the content is multifaceted enough that they help with clarity. If the person explicitly requests minimal formatting, always format your responses without bullet points, headers, lists, or bold emphasis, as requested. In conversational, personal, or emotional exchanges, keep to plain prose.
```

### quoting_sources_example
- Source: Prompting Claude Fable 5.1, "Quoting retrieved sources" (F51-76, F51-77)
- Measured on: Claude Fable 5.1
- Graft when: the deliverable is a summary or comparison of retrieved or attached sources; it is the single `<example>` in `<examples>`, and the two `[web_search: ...]` lines are replaced with the tool actually in use (WebSearch, WebFetch, or Read) so the model reads them as templated tool output rather than literal text to emit. `<success_criteria>` then requires that source wording appear only as marked quotations [F51-75, F51-78].
- Do not graft when: the deliverable is not a summary of sources, on any profile; and it does not substitute for the 3-to-5 example rule elsewhere, because this row's whole point is one complete correct example [BP-046]. On other profiles it is grafted only with an `Assumed:` entry recording that the text was measured on the Fable 5.1 page [BP-025].
- Text:
```text
<example>
<user>look up how the Riverton Ledger and the Coast Dispatch each covered the Harbor Bridge closure and compare their reporting</user>
<response>
[web_search: Harbor Bridge closure Riverton Ledger]
[web_search: Harbor Bridge closure Coast Dispatch]
Both outlets agree on the basics: the bridge closed on March 3 after inspectors found cracked welds, and the state expects repairs to take about eight months. Where they differ is emphasis. The Ledger treats it as a local-economy story. The Dispatch frames it as a funding failure; its editorial calls the closure "entirely foreseeable." Read together, the Ledger explains who is affected now and the Dispatch explains how it came to this — neither account alone gives the whole picture.
</response>
<rationale>CORRECT: The response is organized around where the two outlets agree and differ, not as a walk through either article. Each outlet's reporting is conveyed in one or two sentences of the assistant's own indirect speech. One short marked phrase from one source; every other claim is reworded. The response is still specific and complete.</rationale>
</example>
```

### operating_autonomously
- Source: Prompting Claude Fable 5.1, "Finish the whole task", the first of the two system prompt additions (F51-84, F51-86)
- Measured on: Claude Fable 5.1
- Graft when: the run is unattended, meaning a background or scheduled task, or the user has said to run without asking or that they are stepping away; it is grafted whole and unparaphrased, its opening sentence as written, because that sentence carries much of the effect. When the side-effect signal fired, one sentence listing the required confirmations follows the first paragraph [F51-86, F51-91, F51-92].
- Do not graft when: the posture is assess, or the run is attended, where `delivering_work` is grafted instead [F51-95]. Step 2 resolves ambiguity before this block goes in, because it lowers the model's tendency to ask about ambiguous requests, and that trade-off is checked rather than absorbed [F51-93]. On fable-5 the measured wording is `f5_autonomous_reminder`, which is shorter and differs in its second sentence; on other profiles no equivalent is grafted.
- Also in templates/rearticulated-prompt.md.
- Text:
```text
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work. For reversible actions that follow from the original request, proceed without asking. Stop only for destructive actions or genuine scope changes the user must decide. Offering follow-ups after the task is done is fine; asking permission before doing the work is not.

Exception: when the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one.

Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ('I'll…', 'let me know when…'), do that work now with tool calls. That includes retrying after errors and gathering missing information yourself. Do not stop because the context or session is long. End your turn only when the task is complete or you are blocked on input only the user can provide.

Before running a command that changes system state (such as restarts, deletes, or config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

### delivering_work
- Source: Prompting Claude Fable 5.1, "Finish the whole task", the second of the two system prompt additions (F51-94, F51-95)
- Measured on: Claude Fable 5.1
- Graft when: the run is attended, which is the ordinary interactive case; it goes whole into `<execution_guidance>`, the one home it and `operating_autonomously` share, so the posture is stated once. Its ambiguity rule is the source of the Step 2 test, that a check-in happens only when different readings would lead to materially different work [F51-95, F51-96, F51-99].
- Do not graft when: the posture is assess, on any profile. The page says to apply both autonomy blocks together and, where prompt length forces a choice, to keep only the first; this skill instead picks by attendance, keeps `operating_autonomously` for unattended runs, and carries that block's Exception and last-paragraph paragraphs through SKILL.md Step 1d and Step 7 [F51-84, F51-95]. On opus-5 the measured equivalent is `o5_scope_constraint`.
- Also in templates/rearticulated-prompt.md.
- Text:
```text
# Delivering work
The user's request — or the plan they approved — sets the scope, and the scope is the deliverable: don't quietly narrow, widen, or swap it. Read ambiguity the way a careful colleague would: make routine judgment calls yourself, and check in only when different readings would lead to materially different work. If you see a real problem with the task as specified, say so in a sentence or two and keep building under stated assumptions; if the user hears the concern and reaffirms, that is their decision, so deliver the full request.

If a question comes up partway, first do everything that doesn't depend on the answer; then state the assumption you made, or — when going ahead on a wrong guess would be unsafe or would make the work useless — put the question at the end of a turn that also delivers that progress. If one part turns out to be blocked, complete every other part in full and say exactly what you left out and why — the whole task is the deliverable, and scaling it down is the user's call, not yours. A step you have decided on is something to run, not to announce: describing the next step and ending the turn leaves it undone until the user replies.

Keep changes to what the request needs. Something else you notice worth doing — cleanup or documentation the task didn't call for, a change to a file the task didn't require — is a suggestion to make at the end, not a change to make; actions clearly beyond what the ask implies, and risky or destructive ones, still need the user's go-ahead.
```

### compaction_summary_instruction
- Source: Prompting Claude Fable 5.1, "Tell the model what to preserve in compaction summaries" (F51-104, F51-105)
- Measured on: Claude Fable 5.1
- Graft when: the request is to summarise a working session, to write a handoff note, or to build a harness that compacts on the client side; server-side compaction already does this, so the block is for client-side compaction [F51-103, F51-105].
- Do not graft when: the summary is a deliverable for a reader rather than for a fresh context window, on any profile; its completeness-over-length instruction is wrong for a memo. Its six items are, however, the right shape for multi-session progress notes.
- Text:
```text
Summarize the transcript inside <summary></summary> tags. Include relevant information in the summary such that this conversation will be continued by a new context window without needing to redo work or be reprovided with relevant constraints or context. Be sure to preserve: (1) any difficulties or problems that came up, and how they were handled or resolved; (2) any possibilities, options, or approaches that were raised, tried, or set aside, and why; (3) anything that was asked for, decided, agreed, ruled out, or established as a preference, constraint, or boundary — stated exactly; (4) exactly where things stand now — what has been covered, settled, or completed so far; (5) anything still open, unresolved, promised, or expected to happen next; (6) specific details that would be hard to reconstruct — names, numbers, dates, exact wording, links or references — kept exactly. Be complete on these even at the cost of length; keep everything else concise. Weight the two voices differently: keep what the user said, asked for, shared, or established carefully and close to their own words; your own explanations and reasoning can be condensed much further, to what they concluded or produced — as long as nothing in the six items above is dropped.
```

### keep_changes_to_task
- Source: Prompting Claude Fable 5.1, "Keep changes and tests to what the task asks for" (F51-114, F51-117)
- Measured on: Claude Fable 5.1
- Graft when: every code-change request on this target; it goes verbatim in `<constraints>`. The page reports that unrequested additions and committed test code drop substantially with no measurable change in task success [F51-117, F51-121, F51-122].
- Do not graft when: the target is not fable-5-1. On opus-5 the measured block is `o5_scope_constraint`; on sonnet-5 and opus-4-8 the explicit-scope pattern plus `minimize_overengineering` cover it; on fable-5 it is `f5_scope_discipline`. Its last sentence is load-bearing and stays: this is about extras only, and every behaviour the task asks for is implemented completely.
- Also in templates/rearticulated-prompt.md.
- Text:
```text
If, while working or testing, you find a pre-existing bug, a performance concern, or behavior the task doesn't mention, don't fix, optimize or extend it in this change unless the requested behavior cannot work without it; report it as a follow-up in your summary. Where the task is ambiguous, implement the reading its wording and the surrounding code most directly support, state that assumption in your summary, and don't build for the other readings as well. Verify your work however you like; scratch scripts and quick checks need not be kept. Commit tests only where the task asks for them or this repository already keeps tests for this kind of change, sized like the neighboring test files — roughly one focused test per stated behavior — and don't turn scratch checks into additional permanent test files. This is about extras only: implement every behavior the task asks for, completely.
```

### search_name_as_written
- Source: Prompting Claude Fable 5.1, "Search triggering at low effort" (F51-125, F51-126)
- Measured on: Claude Fable 5.1
- Graft when: the row is research or a question about a named entity and effort is low, where this model is less likely than Fable 5 to call a search or retrieval tool. The page's first option is to raise effort for the affected turns instead, so the snippet is the fallback when effort is fixed [F51-123, F51-124, F51-126].
- Do not graft when: no named entity is in play, on any profile, or effort can simply be raised. During execution it is obeyed literally: at least one search carries the name exactly as the user wrote it. On other profiles it is grafted only with an `Assumed:` entry recording that the text was measured on the Fable 5.1 page [BP-025].
- Text:
```text
When a query centers on a name you do not confidently recognize, or recognize from a fast-moving area like AI models and developer tools where the landscape shifts within months, the name itself is the thing to verify: search before answering, and include the name as the user wrote it in at least one query alongside any reformulations. This holds even when you have some background on it — partial background is exactly what makes an out-of-date answer sound authoritative, so familiarity is not a reason to skip the search.
```

### targeted_edits
- Source: Prompting Claude Fable 5.1, "Prefer targeted edits over whole-file rewrites" (F51-132, F51-136)
- Measured on: Claude Fable 5.1
- Graft when: any code or document edit on this target; it goes in `<execution_guidance>`, appended to the system prompt or the first user message per the page. It brings the model back in line with Fable 5 for small and medium changes [F51-133, F51-136].
- Do not graft when: the file is short or most of it is changing, where a rewrite is the cheaper move and the snippet's own condition (when it will not affect the end result) already allows it. On other profiles it is grafted only with an `Assumed:` entry recording that the text was measured on the Fable 5.1 page [BP-025].
- Also in templates/rearticulated-prompt.md.
- Text:
```text
The number of tokens used to edit files is best minimized, all else being equal. Therefore, when it will not affect the end result, try to surgically edit a file rather than rewrite the entire thing.
```

### long_output_budget_note
- Source: Prompting Claude Fable 5.1, "Leave room for long outputs at xhigh and max effort" (F51-141, F51-142)
- Measured on: Claude Fable 5.1
- Graft when: the deliverable is long (a multi-section document, a large table or dataset, a complete code file) and the run is at xhigh or max effort; it is appended to the end of the user message, which here means the last element of the prompt before `batch_nudge`, with `[max_tokens]` replaced by the request's actual value, for example 64,000. The page's first recommendation is to run such requests at high instead, so the snippet accompanies a deliberate xhigh or max run [F51-137 to F51-142].
- Do not graft when: the deliverable is short, on any profile. The value substituted is `max_tokens`, never `budget_tokens`, which returns a 400 on Opus 4.7 and later and does not exist on the Fable family [F5-08, BP-189]. On sonnet-5 the neighbouring fact is different: the hard limit covers thinking plus response, and inherited limits are scaled up about 30 percent for the new tokenizer [S5-26, S5-33]. On fable-5 the page prints no max_tokens for the note to carry, so client timeouts, streaming, and asynchronous checks are named instead [F5-21, F5-22].
- Also in templates/rearticulated-prompt.md.
- Text:
```text
Everything produced in one reply, including any reasoning or drafting done before the reply, counts toward a single limit of about [max_tokens] tokens. If that limit is reached before the reply is finished, the person receives a cut-off response and has to start over. Composing an entire output or deliverable in full as reasoning and then again as a reply would double the length of the turn without improving the result, so don't do that.

Instead, when the person has asked for a long or effort-intensive deliverable such as a multi-section document, a large table or dataset, or a complete code file, spend extra effort on understanding the request, checking the inputs the answer depends on, settling the structure and other difficult decisions, and otherwise using the reasoning space to reason and the output space to write an output. Usually it is not needed to draft an output multiple times.
```

## Fable 5

Measured on Claude Fable 5 and Claude Mythos 5, whose page covers both names (F5-01). This page steers with one principle-level instruction rather than enumerated behaviours, so two snippets that cover the same ground are not stacked [F5-32, F5-35].

### f5_act_when_ready
- Source: Prompting Claude Fable 5, "Longer turns by default" (F5-24)
- Measured on: Claude Fable 5
- Graft when: the request is ambiguous or open-ended and the model would otherwise overplan; it goes in `<constraints>`, which is where the profile places it [F5-17, F5-24].
- Do not graft when: the deliverable is a survey of options, on any profile. On other profiles `commit_to_approach` is the guide's block for the same symptom, and only one of the two is grafted. Its last sentence stays as written: the restriction does not apply to thinking blocks.
- Text:
```text
When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks.
```

### f5_scope_discipline
- Source: Prompting Claude Fable 5, "Consider all effort levels" (F5-31)
- Measured on: Claude Fable 5
- Graft when: the row is code change on this target, above all a bug fix or a one-shot operation at high or xhigh effort, where unrequested tidying and refactoring appear; it goes in `<constraints>` [F5-31].
- Do not graft when: the target is not fable-5, where the measured equivalents are `keep_changes_to_task` (fable-5-1), `o5_scope_constraint` (opus-5), and `minimize_overengineering` (sonnet-5, opus-4-8, legacy-4x); and not stacked with any of them, because one principle-level instruction is the page's method and a second list dilutes it [F5-32].
- Text:
```text
Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need surrounding cleanup and a one-shot operation usually doesn't need a helper. Don't design for hypothetical future requirements: do the simplest thing that works well. Avoid premature abstraction and half-finished implementations. Don't add error handling, fallbacks, or validation for scenarios that cannot happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs). Don't use feature flags or backwards-compatibility shims when you can just change the code.
```

### f5_lead_with_outcome
- Source: Prompting Claude Fable 5, "Strong instruction following" (F5-33, F5-34)
- Measured on: Claude Fable 5
- Graft when: the output is read by a person, above all at high effort, where this model elaborates beyond what the task needs; it is the default `<output_format>` block on this target, and the skill's own final message follows it when Fable 5 is the executing model [F5-34].
- Do not graft when: the run is tool-heavy and long, where `f5_readability_addendum` covers the same ground at more length and only one of the two is used, chosen by task length [F5-59]. Do not graft on fable-5-1, where narration-brevity language is removed rather than added [F51-35, BP-100]. Its point is that readability outranks brevity, so it is not a licence to compress into fragments.
- Text:
```text
Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail and reasoning come after. Being readable and being concise are different things, and readability matters more.

The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon.
```

### f5_pause_only_when_needed
- Source: Prompting Claude Fable 5, "Strong instruction following", the checkpoint instruction (F5-36)
- Measured on: Claude Fable 5
- Graft when: the rearticulation is multi-step or long-running on this target; it goes in `<execution_guidance>` and pairs with `f5_autonomous_reminder` for unattended pipelines [F5-36, F5-51, F5-52].
- Do not graft when: the posture is assess, on any profile. The page's point is that the cases need not be enumerated, so the `[confirm]` list in `<task>` carries the specifics and this block carries the principle.
- Text:
```text
Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise.
```

### f5_ground_progress
- Source: Prompting Claude Fable 5, "Ground progress claims during long runs" (F5-38)
- Measured on: Claude Fable 5
- Graft when: the model will report on work it performed with tools; it goes in `<success_criteria>` or `<verification>` on this target, and it is how the executing model audits its own progress claims [F5-37, F5-38].
- Do not graft when: no tool work happens, on any profile. It is an evidence audit, not a reflection instruction, so it does not carry the `reasoning_extraction` risk that show-your-reasoning lines do [F5-71].
- Text:
```text
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.
```

### f5_state_boundaries
- Source: Prompting Claude Fable 5, "State the boundaries" (F5-40)
- Measured on: Claude Fable 5
- Graft when: the posture is assess on this target, meaning a diagnostic, investigative, or question-shaped request; it goes in `<constraints>` and carries the evidence-before-mutation sentence that Standing rule 4 restates [F5-40, F51-90].
- Do not graft when: the posture is act, on any profile. On fable-5-1 the same two paragraphs live inside `operating_autonomously` as its Exception and state-change paragraphs, so grafting both duplicates them.
- Text:
```text
When the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one. Before running a command that changes system state (restarts, deletes, config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

### f5_delegate_subagents
- Source: Prompting Claude Fable 5, "Parallel subagents" (F5-44)
- Measured on: Claude Fable 5
- Graft when: the rearticulation has independent subtasks and subagents are available; it goes in `<execution_guidance>` on this target [F5-44].
- Do not graft when: the work is sequential or single-file, on any profile. On opus-5 the measured block is `o5_delegation_guidance`, which pushes the other way; on opus-4-8 it is `o48_subagent_guidance`; on other profiles it is `subagent_usage_policy`. A subagent runs in a forked context and cannot see this prompt, so the relevant `<task>`, `<constraints>`, and confirm list are passed in its arguments verbatim [BP-290].
- Text:
```text
Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context.
```

### f5_memory_notes
- Source: Prompting Claude Fable 5, "Construct a memory system" (F5-46)
- Measured on: Claude Fable 5
- Graft when: the task asks the model to maintain memory or a notes directory and no harness or project memory convention already covers it; it goes in `<constraints>` on this target [F5-45, F5-46].
- Do not graft when: a convention exists, on any profile; this workspace keeps a memory index, and a second discipline would conflict with it. Do not graft it as a substitute for the compaction and state-tracking blocks, which solve a different problem.
- Text:
```text
Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong.
```

### f5_memory_bootstrap
- Source: Prompting Claude Fable 5, "Construct a memory system", the seeding prompt (F5-48)
- Measured on: Claude Fable 5
- Graft when: the user asks to build or seed memory from session history; `[X]` is filled with the memory path and the block becomes the request body in `<task>` [F5-48].
- Do not graft when: memory already exists and the ask is to update it, on any profile, where `f5_memory_notes` is the discipline to state instead. It spawns subagents, so it is grafted only where delegation is wanted.
- Text:
```text
Reflect on the previous sessions we've had together. Use subagents to identify core themes and lessons, and store them in [X]. Make sure you know to reference [X] for future use.
```

### f5_autonomous_reminder
- Source: Prompting Claude Fable 5, "Rare cases of early stopping" (F5-51, F5-52)
- Measured on: Claude Fable 5
- Graft when: the run is an unattended or scheduled pipeline on this target, or the user has said to go end to end; the page pairs it with the checkpoint instruction `f5_pause_only_when_needed`, which defines when pausing is appropriate [F5-51, F5-52, F5-36].
- Do not graft when: the posture is assess, or the run is attended, on any profile. On fable-5-1 the measured block is `operating_autonomously`, which is longer and differs in wording; the two are not interchangeable and only the target's own page supplies the text [BP-025].
- Text:
```text
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking "Want me to…?" or "Shall I…?" will block the work. For reversible actions that follow from the original request, proceed without asking. Offering follow-ups after the task is done is fine; asking permission after already discussing with the user before doing the work is not. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ("I'll…", "let me know when…"), do that work now with tool calls. End your turn only when the task is complete or you are blocked on input only the user can provide.
```

### f5_ample_context
- Source: Prompting Claude Fable 5, "Rare cases of context-budget concern" (F5-55)
- Measured on: Claude Fable 5
- Graft when: the harness shows a remaining-token countdown to the model and the model has started suggesting a new session, offering to summarise and hand off, or trimming its own work [F5-53, F5-55].
- Do not graft when: no count is visible to the model, on any profile. The page's first instruction is to avoid surfacing explicit context-budget counts at all, so the snippet is a mitigation for a harness that must show them, and no figure is ever quoted alongside it [F5-53, F5-54]. When the executing model is Fable 5, the harness's remaining-token count is ignored rather than acted on [F5-53].
- Text:
```text
You have ample context remaining. Do not stop, summarize, or suggest a new session on account of context limits. Continue the work.
```

### f5_give_reason
- Source: Prompting Claude Fable 5, "Give the reason, not only the request" (F5-56, F5-57)
- Measured on: Claude Fable 5
- Graft when: the user's purpose is known or can be inferred; it is the frame for `<context>` on this target, with the three slots filled from CLAUDE.md, memory, the selection, the named files, and earlier turns. The page notes this matters most for long-running agents drawing on multiple workstreams [F5-56, F5-57].
- Do not graft when: a slot would be guessed and the guess would change the deliverable, on any profile; ask for that one slot, or record it as an `Assumed:` entry. The purpose sentence is written once and generalisation is relied on rather than enumerating variants [BP-040].
- Text:
```text
I'm working on [the larger task] for [who it's for]. They need [what the output enables]. With that in mind: [request].
```

### f5_readability_addendum
- Source: Prompting Claude Fable 5, "Readability when communicating with the user" (F5-58, F5-59)
- Measured on: Claude Fable 5
- Graft when: the run is extended or agentic on this target (many tool calls, a large working context) and the final message is the user's first look at the work; it goes in `<output_format>` [F5-58, F5-59].
- Do not graft when: the task is short, where `f5_lead_with_outcome` says the same thing in one paragraph and only one of the two is used [F5-34]. Do not graft on fable-5-1, where `progress_updates_line` covers the opening line and the recap, and narration-brevity language is removed instead of added [F51-37, F51-35].
- Text:
```text
Terse shorthand is fine between tool calls (that's you thinking out loud, and brevity there is good). Your final summary is different: it's for a reader who didn't see any of that.

If you've been working for a while without the user watching (overnight, across many tool calls, since they last spoke), your final message is their first look at any of it. Write it as a re-grounding, not a continuation of your working thread: the outcome first, then the one or two things you need from them, each explained as if new. The vocabulary you built up while working is yours, not theirs; leave it behind unless you re-introduce it.

When you write the summary at the end, drop the working shorthand. Write complete sentences. Spell out terms. Don't use arrow chains, hyphen-stacked compounds, or labels you made up earlier. When you mention files, commits, flags, or other identifiers, give each one its own plain-language clause. Open with the outcome: one sentence on what happened or what you found. Then the supporting detail. If you have to choose between short and clear, choose clear.
```

### send_to_user (the Fable 5 tool definition; also cited as f5_send_to_user_tool_definition)
- Source: Prompting Claude Fable 5, "Create a send-to-user tool", the tool definition (F5-61, F5-62)
- Measured on: Claude Fable 5
- Graft when: the deliverable is a harness for long asynchronous agents on this target; the client-side tool delivers messages to the user verbatim without ending the turn. Defining the tool alone is not enough, so it is paired with `f5_send_to_user_elicitation` [F5-60, F5-62, F5-65].
- Do not graft when: the run is an in-session rearticulation on any profile. The skill does not add tool definitions to rearticulated prompts; this block reaches a prompt only through the harness-authoring and async-agent rows. Narration is never routed through the tool [F5-66].
- Text:
```json
{
  "name": "send_to_user",
  "description": "Display a message directly to the user. Use this for progress updates, partial results, or content the user must see exactly as written before the task finishes.",
  "input_schema": {
    "type": "object",
    "properties": {
      "message": {
        "type": "string",
        "description": "The content to display to the user."
      }
    },
    "required": ["message"]
  }
}
```

### f5_send_to_user_elicitation
- Source: Prompting Claude Fable 5, "Create a send-to-user tool", the elicitation language (F5-65)
- Measured on: Claude Fable 5
- Graft when: a `send_to_user` tool exists in the harness; it goes in the tools section of the authored prompt, because defining the tool without this language does not reliably get it called [F5-64, F5-65].
- Do not graft when: no such tool exists, on any profile. Its second sentence is the boundary that matters: user-facing content only, never narration or reasoning, which is also how this page's reasoning-visibility rule is satisfied without a show-your-reasoning instruction [F5-66, F5-72].
- Text:
```text
Between tool calls, when you have content the user must read verbatim (a partial deliverable, a direct answer to their question), call the send_to_user tool with that content. Use send_to_user only for user-facing content, not for narration or reasoning.
```

### f5_self_verification_interval
- Source: Prompting Claude Fable 5, "Recommended scaffolding changes", the make-self-verification-explicit bullet (F5-68, F5-69)
- Measured on: Claude Fable 5
- Graft when: the prompt is a long-running build or implementation on this target; `[X]` is filled with a concrete interval such as after each module, and it goes in `<verification>`. The page's finding is that separate, fresh-context verifier subagents tend to outperform self-critique, so the verification is delegated rather than self-directed [F5-68, F5-69].
- Do not graft when: the target is opus-5, where verification instructions are removed rather than rewritten and subagents are explicitly not used to verify or double-check the model's own work; this is one of the two known conflicts between pages, resolved in favour of the target's own page [O5-43, O5-51, and section 1 of references/model-notes.md]. Do not graft on a short task, on any profile.
- Text:
```text
Establish a method for checking your own work at an interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the specification.
```

## Opus 5

Measured on Claude Opus 5. This profile's defining removal is verification: the `<verification>` tag is omitted and every verify, double-check, or re-verify line is deleted rather than reworded, with deliverable length, task scope, and subagent policy stated explicitly in their place [O5-43, O5-47, O5-51, BP-232, BP-233].

### o5_conciseness
- Source: Prompting Claude Opus 5, "Response length and verbosity" (O5-30, O5-31)
- Measured on: Claude Opus 5
- Graft when: the deliverable is chat-style on this target, or the user asked for brevity. This model's default user-facing responses run longer than prior models', and raising or lowering effort does not reliably change visible response length, so length is prompted for explicitly [O5-28, O5-29, O5-31, BP-094].
- Do not graft when: the deliverable is a written file, where `o5_deliverable_length` is the measured block; and not on fable-5-1, where narration-brevity lines are removed, not added [F51-35, BP-100]. On sonnet-5 and opus-4-8 the equivalent line is grafted only when the user or the product fixes the verbosity [S5-07, O48-08].
- Text:
```text
Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
```

### tone_preference
- Source: Prompting Claude Opus 5, "Response length and verbosity", the end-of-prompt reminder (O5-32, O5-33)
- Measured on: Claude Opus 5
- Graft when: the prompt is long on this target and a conciseness instruction already appears earlier; it is the last block of the prompt, keeping its wrapper tag [O5-33, BP-176].
- Do not graft when: the prompt is short, on any profile, where the earlier conciseness line is enough and the repetition is padding. Do not graft on fable-5-1 for the same reason `o5_conciseness` is not grafted there.
- Text:
```text
<tone_preference>
Keep outputs reasonably concise.
</tone_preference>
```

### o5_progress_updates
- Source: Prompting Claude Opus 5, "User-facing progress updates" (O5-35, O5-36)
- Measured on: Claude Opus 5
- Graft when: the task is agentic and tool-heavy on this target and terse updates are preferred; it goes in `<execution_guidance>`. When Opus 5 is the executing model this is also the narration cadence for Steps 6 and 7: one sentence before the first tool call, an update only on an important finding or a change of direction, and an outcome-first close [O5-36, O5-42].
- Do not graft when: the target is sonnet-5 or opus-4-8, whose pages call a forced cadence unnecessary and warn against lines such as "After every 3 tool calls, summarize progress" [S5-40, O48-33]; or fable-5-1, which needs more narration than this asks for and takes `progress_updates_line` instead [F51-37]. A counted interval is not added on any profile.
- Text:
```text
Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it.
```

### o5_deliverable_length
- Source: Prompting Claude Opus 5, "Written deliverable length" (O5-40, O5-41)
- Measured on: Claude Opus 5
- Graft when: the task has this model write a report, a Markdown document, or a summary to disk; it goes in `<output_format>` [O5-41].
- Do not graft when: the deliverable is a chat reply, where `o5_conciseness` applies instead. On fable-5-1 the writing-density blocks (`mannered_prose_definition`, `mannered_prose_short`) address prose density rather than document length, and neither is a substitute for the other.
- Text:
```text
Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.
```

### o5_scope_constraint
- Source: Prompting Claude Opus 5, "Task scope and over-verification" (O5-46, O5-47)
- Measured on: Claude Opus 5
- Graft when: the task is narrow on this target, a single-file change, or anything the user framed as just do X; it goes in `<constraints>` [O5-47].
- Do not graft when: the target is not opus-5, where the measured equivalents are `keep_changes_to_task` (fable-5-1), `f5_scope_discipline` (fable-5), and `minimize_overengineering` (sonnet-5, opus-4-8, legacy-4x). It is grafted instead of a verification instruction, not alongside one: on this target scope statements do the work that verify lines did on earlier models [O5-43, BP-233].
- Text:
```text
Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked.
```

### o5_delegation_guidance
- Source: Prompting Claude Opus 5, "Controlling subagent spawning" (O5-50, O5-51)
- Measured on: Claude Opus 5
- Graft when: the deliverable is an authored prompt, an Agent SDK run, or a custom or omitted system prompt on this target, or the agentic task is cost-sensitive; it goes in `<execution_guidance>` [O5-51].
- Do not graft when: the run is interactive Claude Code on this target, where the `claude_code` preset already carries a delegation instruction and a second copy is redundant [O5-54]; or when the task really is a wide parallel investigation, which the block itself permits. Do not graft on opus-4-8, which spawns fewer subagents by default and needs `o48_subagent_guidance` pushing the other way [O48-43]. Its no-subagent-verification clause is why `f5_self_verification_interval` is not grafted on this target [O5-51].
- Note: the deterministic caps are environment controls the prompt cannot set: `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, and the SDK `max_budget_usd` option, all requiring Claude Code 2.1.217 or later. Name them in the Reading line rather than in the prompt [O5-52, O5-55].
- Text:
```text
Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low.
```

### o5_correction_narration
- Source: Prompting Claude Opus 5, "Self-correction" (O5-58, O5-59)
- Measured on: Claude Opus 5
- Graft when: the output is user-facing on this target, or the request asks for a clean final answer, and visible self-corrections would be noise; it goes in `<output_format>` [O5-59].
- Do not graft when: the user wants the reasoning trail, on any profile, or the deliverable is an audit where every correction matters. It limits which corrections are narrated; it never suppresses the correction itself.
- Text:
```text
Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it.
```

### o5_thinking_disabled_mitigation
- Source: Prompting Claude Opus 5, "Running with thinking disabled" (O5-67, O5-68)
- Measured on: Claude Opus 5
- Graft when: an integration must keep thinking off on this target, above all a tool-heavy or search workload. With thinking disabled this model can emit tool calls as text and leak internal XML tags, and disabling is possible only at effort high or lower [O5-60 to O5-65, O5-68].
- Do not graft when: thinking is on, on any profile. The page's preference is thinking on at low effort over thinking disabled, so the snippet is a mitigation rather than a design choice. Do not pair it with a do-not-think rule, which increases tag leakage [O5-66]. Its third sentence is the one that matters here: `<thinking>` and `<answer>` output tags appear only for thinking-off targets in authored prompts, never for the session model [BP-226, BP-195].
- Text:
```text
When you use a tool, you may say a brief sentence first. If no tool can express what the user asked for, say so instead of guessing. Do not include internal or system XML tags in your response.
```

## Sonnet 5

Measured on Claude Sonnet 5. Eight of the sections below are shared with the Opus 4.8 page, which prints the same text; each lists both sources and both alias IDs, and the Opus 4.8 section points back to them. This model reads prompts literally and explicitly, most of all at low and medium effort: it does not silently generalise an instruction from one item to another and does not infer requests that were not made [S5-42, S5-20].

### s5_conciseness / o48_conciseness
- Source: Prompting Claude Sonnet 5, "Response length and verbosity" (S5-08); Prompting Claude Opus 4.8, "Response length and verbosity" (O48-09). Identical text on both pages.
- Measured on: Claude Sonnet 5 and Claude Opus 4.8
- Graft when: the user asks for a short answer, or the product depends on concise output, and the target is sonnet-5 or opus-4-8; it goes in `<output_format>` [BP-016, BP-018].
- Do not graft when: the verbosity is not fixed by the user or the product, on either target; the skill writes no generic be-concise instruction of its own. Do not graft on fable-5-1, where narration-brevity lines are removed [F51-35, BP-100]. On opus-5 use `o5_conciseness`, which is that page's own wording: stating expected response length explicitly applies there too, but as that page's block in `<output_format>`, not as this one [BP-017].
- Text:
```text
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

### s5_low_effort_multistep / o48_low_effort_reasoning
- Source: Prompting Claude Sonnet 5, "Calibrating effort and thinking depth" (S5-22); Prompting Claude Opus 4.8, "Calibrating effort and thinking depth" (O48-21). Identical text on both pages.
- Measured on: Claude Sonnet 5 and Claude Opus 4.8
- Graft when: effort is pinned at low for latency reasons and the task still needs multistep reasoning; it goes in `<execution_guidance>` [S5-22, O48-21].
- Do not graft when: effort can simply be raised, which is the first remedy on both pages [S5-21, O48-19]; when the user has not pinned low effort; or on Opus 4.5 with thinking off, because of the word "think" [BP-235, BP-236]. Do not graft on fable-5-1 or fable-5, where a general `think_thoroughly` is the most that is kept and reasoning choreography is otherwise stripped [F5-71].
- Text:
```text
This task involves multistep reasoning. Think carefully through the problem before responding.
```

### s5_explicit_scope / o48_explicit_scope
- Source: Prompting Claude Sonnet 5, "More literal instruction following" (S5-45); Prompting Claude Opus 4.8, "More literal instruction following" (O48-39). Identical phrasing pattern on both pages, quoted inline as the example of stating scope explicitly.
- Measured on: Claude Sonnet 5 and Claude Opus 4.8
- Graft when: an instruction has to apply across all items rather than the first, on either target; adapt the noun (section, file, row, host, finding) to the actual target set, and enumerate every wanted sub-step rather than relying on generalisation [S5-44, S5-45, O48-38, O48-39]. Also on opus-5 as borrowed text, with the Target model item recording "text measured on Prompting Claude Opus 4.8" [O5-05, BP-025].
- Do not graft when: only the first instance is meant, on either target. It is a phrasing pattern, so it is adapted rather than pasted, and the adaptation is recorded in the Changed line.
- Text:
```text
Apply this formatting to every section, not just the first one
```

### s5_warm_tone / o48_warm_tone
- Source: Prompting Claude Sonnet 5, "Tone and writing style" (S5-48); Prompting Claude Opus 4.8, "Tone and writing style" (O48-42). Identical text on both pages.
- Measured on: Claude Sonnet 5 and Claude Opus 4.8
- Graft when: a warmer or more conversational voice than the default is wanted on either target; it goes in `<output_format>` or a `tone_preference` tag [S5-48, O48-42].
- Do not graft when: warmth was not requested, on either target. The Opus 4.8 executing default is a direct tone with minimal validation phrasing, so this block is a deliberate override rather than a courtesy addition [O48-40].
- Text:
```text
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

### s5_design_concrete_spec_aefrm / o48_aefrm_concrete_spec
- Source: Prompting Claude Sonnet 5, "Design and frontend defaults" (S5-53); Prompting Claude Opus 4.8, "Design and frontend defaults" (O48-51). Identical brief on both pages.
- Measured on: Claude Sonnet 5 and Claude Opus 4.8
- Graft when: the row is frontend or design on either target and the user can describe a direction; the rearticulation mirrors its sections (atmosphere, feel, tonal system, imagery, layout and radius, typography, structure, motion, palette hexes) with the user's own values. A concrete spec is what both pages recommend in place of temperature-driven variety [S5-53, S5-54, O48-49, O48-51]. Also on opus-5 as borrowed text, with the Target model item recording "text measured on Prompting Claude Opus 4.8" [O5-05, BP-025].
- Do not graft when: any profile, as literal content. The AEFRM brief is a structural template; grafting its supplement-brand copy, its Alumni Sans SC clause, or its five hex values into an unrelated build produces a design nobody asked for. When the user has no direction, use the propose-directions snippet instead.
- Text:
```text
Design a desktop landing page for a supplement brand called AEFRM.

The visual direction should come from a cold monochrome atmosphere using pale silver-gray tones that gradually deepen into blue-gray and near-black, similar to a misted metallic surface.

The page should feel sharp and controlled, with a strong sense of structure and restraint.

Use this tonal system across the full page instead of introducing bright accent colors.

Use the uploaded image on the hero design in black and white.

The layout should be built with clear horizontal sections and a centered max-width container. Use 4px corner radius consistently across cards, buttons, inputs, and media frames. Margins should feel generous, with enough empty space around each section so the page breathes.

Typography should use a square, angular sans-serif with wider letter spacing than usual, especially in headings and navigation, so the text feels more engineered and less compressed. Headline text can be large and uppercase, while supporting copy remains short and sparse. The sub texts should be written with Alumni Sans SC in 4-6px like tiny little texts on corners bottom centre like that.

For the structure, start with a hero section containing a strong product statement, one short supporting paragraph, and a clean product placeholder or packshot frame. Below that, add a benefit grid with three or four blocks, then a formulation or ingredients section, and finally a cta.

Buttons should be flat and precise, with subtle hover changes using transition: all 160ms ease out where brightness and border contrast shift slightly rather than using dramatic motion.

Color palette should stay within this range:
#E9ECEC, #C9D2D4, #8C9A9E, #44545B, #11171B.
```

### s5_design_propose_directions / o48_propose_directions
- Source: Prompting Claude Sonnet 5, "Design and frontend defaults" (S5-55); Prompting Claude Opus 4.8, "Design and frontend defaults" (O48-54). Same instruction, punctuated differently on each page.
- Measured on: Claude Sonnet 5 and Claude Opus 4.8
- Graft when: the design brief is open-ended on either target, or variety is wanted across runs; it goes in `<task>`. It is the sanctioned replacement for temperature-driven variety, which matters on sonnet-5 because any non-default sampling value returns a 400, and on opus-4-8 because the page converts temperature-for-variety into this block [S5-49, S5-55, O48-53, O48-54]. Also on opus-5 as borrowed text, with the Target model item recording "text measured on Prompting Claude Opus 4.8" [O5-05, BP-025]. In same-turn execution the four options are presented and the pick is awaited before implementing, which is the one place a rearticulated prompt legitimately ends a turn on a question.
- Do not graft when: the user already gave a direction, on either target, where the concrete spec is the better block; or when the run is unattended, because nobody is there to pick. Do not graft alongside `analytics_dashboard_more_effective`, which tells the run to build now.
- Note: Sonnet 5 writes "plus a one-line rationale" after a comma; Opus 4.8 writes an em dash. Each is fenced separately and grafted from the target's own page.
- Text (Prompting Claude Sonnet 5):
```text
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the user to pick one, then implement only that direction.
```
- Text (Prompting Claude Opus 4.8):
```text
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface — one-line rationale). Ask the user to pick one, then implement only that direction.
```

### frontend_aesthetics_short
- Source: Prompting Claude Sonnet 5, "Design and frontend defaults" (S5-58, cited in the rule set as `frontend_aesthetics`); Prompting Claude Opus 4.8, "Design and frontend defaults" (O48-57, likewise). Identical text on both pages.
- Measured on: Claude Sonnet 5 and Claude Opus 4.8
- Graft when: the row is frontend or UI generation on either target; it is inserted unchanged, wrapper tag and all-caps NEVER included, and paired with either a concrete spec or the propose-directions snippet [S5-58, O48-57]. Also on opus-5, whose page inherits the Opus 4.8 design baseline, with the Target model item recording "text measured on Prompting Claude Opus 4.8" [O5-05, BP-025]; and on fable-5-1 and fable-5, whose pages have no design section, with an Assumed entry naming the Sonnet 5 and Opus 4.8 pages [BP-025, F5-19, F5-70].
- Do not graft when: the target is legacy-4x, which takes the guide's long `frontend_aesthetics` block instead [BP-330]. Conversely the long block is not grafted on sonnet-5 or opus-4-8: both pages trim it to this short form, and the longer guidance for earlier models lives in the frontend-design skill rather than in the prompt [O48-55, S5-57, BP-342]. On opus-4-8, remember the page's persistent house style (a cream background around #F4F1EA, serif display type, italic accents, a terracotta or amber accent) suits editorial and portfolio briefs and misfits dashboards, dev tools, fintech, healthcare, and enterprise apps, so palette and type are always specified alongside this block [O48-46 to O48-52].
- Text:
```text
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

### s5_code_review_coverage / o48_review_coverage
- Source: Prompting Claude Sonnet 5, "Code review harnesses" (S5-66); Prompting Claude Opus 4.8, "Code review harnesses" (O48-66). Identical text on both pages.
- Measured on: Claude Sonnet 5 and Claude Opus 4.8
- Graft when: the row is code review or bug finding on either target, above all with a downstream filter; the output schema then gains a confidence field and a severity field so the filter can rank the findings [S5-66, S5-67, O48-66]. Also on opus-5 as borrowed text, whose page states the report-everything rule without printing a snippet, with the Reading line recording "text measured on the Opus 4.8 page" [O5-12, BP-025].
- Do not graft when: the user wants the single pass to self-filter, where the concrete bar is the right block; the mere absence of a second stage is not the trigger, because the page says the coverage prompt still helps without one [O48-67, O48-69]. Conservative review filters are removed on all four of sonnet-5, opus-4-8, opus-5, and their inheritors [S5-64, O48-65, O5-12].
- Text:
```text
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

### s5_code_review_concrete_bar / o48_review_concrete_bar
- Source: Prompting Claude Sonnet 5, "Code review harnesses" (S5-69); Prompting Claude Opus 4.8, "Code review harnesses" (O48-70). Identical text on both pages, quoted inline as the example of a concrete bar.
- Measured on: Claude Sonnet 5 and Claude Opus 4.8
- Graft when: the review is single-pass on either target and some self-filtering is wanted; it goes in `<constraints>`, and it replaces qualitative words such as important with a stated bar [S5-68, S5-69, O48-69, O48-70].
- Do not graft when: a downstream filter exists, where coverage is the goal and this block would drop findings early; and not alongside the coverage snippet, which tells the run not to filter at all.
- Note: the pages print it lowercase inside a sentence; it is reproduced as printed and reads as a clause of the surrounding constraint.
- Text:
```text
report any bugs that could cause incorrect behavior, a test failure, or a misleading result; only omit nits like pure style or naming preferences.
```

## Opus 4.8

Measured on Claude Opus 4.8. This page shares its shape with the Sonnet 5 page: literalism, verbosity calibration, natural progress updates, tone, design defaults, and review coverage all print the same text under the `o48_*` IDs, so those sections live once in the Sonnet 5 group above and are listed here as pointers. One block is unique to this page, and one thinking snippet is folded into the guide's `think_only_when_useful` section.

Shared with the Sonnet 5 page, one section each above: `s5_conciseness / o48_conciseness`, `s5_low_effort_multistep / o48_low_effort_reasoning`, `s5_explicit_scope / o48_explicit_scope`, `s5_warm_tone / o48_warm_tone`, `s5_design_concrete_spec_aefrm / o48_aefrm_concrete_spec`, `s5_design_propose_directions / o48_propose_directions`, `frontend_aesthetics_short`, `s5_code_review_coverage / o48_review_coverage`, `s5_code_review_concrete_bar / o48_review_concrete_bar`. The thinking steer is `think_only_when_useful (aliases s5_thinking_trigger_guard, o48_thinking_steer)` in the guide group, where the Opus 4.8 variant with its em dash is fenced separately.

### o48_subagent_guidance
- Source: Prompting Claude Opus 4.8, "Controlling subagent spawning" (O48-44, O48-45)
- Measured on: Claude Opus 4.8
- Graft when: the coding task on this target mixes direct edits with fan-out reads. This model spawns fewer subagents by default, so the guidance pushes toward delegation for fan-out while keeping single-response work in the lead agent [O48-43, O48-45].
- Do not graft when: the target is opus-5, where `o5_delegation_guidance` pushes the other way and keeps spawn counts low [O5-51]; or fable-5, where `f5_delegate_subagents` is the measured block [F5-44]. The page labels the parenthetical a toy example, so it is adapted to the actual task rather than pasted with the refactoring example intact.
- Text:
```text
Do not spawn a subagent for work you can complete directly in a single response (e.g. refactoring a function you can already see).

Spawn multiple subagents in the same turn when fanning out across items or reading multiple files.
```

## Index by model

Each row lists the snippet IDs a rearticulated prompt for that target may graft, so a profile file in `references/models/` can be cross-checked against this library. A snippet outside its row is grafted only with an `Assumed:` entry naming the page that measured it [BP-025]. The first row is the full guide-measured set; every profile row is that base minus its removals plus its page-measured additions, and nothing is re-added that the base already holds. Four guide blocks in the base are stated by the guide for named models (`minimize_overengineering` and `frontend_aesthetics` for Opus 4.5 and Opus 4.6, `context_compaction_persistence` and `spend_entire_context` for Sonnet 5, Sonnet 4.6, Sonnet 4.5, and Haiku 4.5), so they sit in the base as the guide's own text and each profile row says whether that profile takes them [BP-025].

| Profile | May graft |
|---|---|
| all profiles (guide-wide) | analytics_dashboard_more_effective, quality_modifiers_dashboard (as a rewrite pattern), tts_no_ellipses, role_python_coding_assistant, multidocument_structure, quote_extraction, model_identity, model_string, tool_use_summary, smoothly_flowing_prose_paragraphs (alias prose_paragraphs_positive), avoid_excessive_markdown_and_bullet_points, plain_text_math, professional_presentation, no_preamble, continuation_from_interrupted, change_this_function, make_these_edits, use_this_tool_when (as a substitution), default_to_action or do_not_act_before_instructions, use_parallel_tool_calls, reduce_parallel_execution, targeted_tool_trigger, commit_to_approach, think_thoroughly (thinking on only), think_only_when_useful, reflect_after_tool_results, self_check_verify, minimize_overengineering, frontend_aesthetics, context_compaction_persistence, tests_unacceptable_to_remove, fresh_start_pwd, fresh_start_review_state, fresh_start_integration_test, spend_entire_context, tests_json_example, progress_notes_example, autonomy_safety_confirmation, complex_research, subagent_usage_policy, temp_file_cleanup, general_purpose_solution, investigate_before_answering |
| fable-5-1 | the guide-wide set minus avoid_excessive_markdown_and_bullet_points, reflect_after_tool_results, think_only_when_useful, minimize_overengineering, frontend_aesthetics (long), context_compaction_persistence, spend_entire_context (the guide scopes context awareness to Sonnet 5, Sonnet 4.6, Sonnet 4.5, and Haiku 4.5, BP-241; the counterparts here are f5_ample_context for a visible countdown and compaction_summary_instruction for client-side compaction, F51-103 to F51-113), and every conciseness or narration-brevity line; plus progress_updates_line, tool_output_hidden_note, batch_nudge, mannered_prose_definition, mannered_prose_short, formatting_in_chat_rule, quoting_sources_example, operating_autonomously or delivering_work, compaction_summary_instruction, keep_changes_to_task, search_name_as_written, targeted_edits, long_output_budget_note, frontend_aesthetics_short with an Assumed entry |
| fable-5 | the guide-wide set minus reflect_after_tool_results, think_only_when_useful, minimize_overengineering, subagent_usage_policy (damping intent conflicts with F5-41; covered by f5_delegate_subagents, F5-42, F5-44), context_compaction_persistence, spend_entire_context, and any show-your-reasoning, think-aloud, reflection, thinking-budget, or token-count line; plus f5_act_when_ready, f5_scope_discipline, f5_lead_with_outcome or f5_readability_addendum (exactly one), f5_pause_only_when_needed, f5_ground_progress, f5_state_boundaries, f5_delegate_subagents, f5_memory_notes, f5_memory_bootstrap, f5_autonomous_reminder, f5_ample_context (the counterpart of the two context blocks here), f5_give_reason, send_to_user, f5_send_to_user_elicitation, f5_self_verification_interval, frontend_aesthetics_short with an Assumed entry naming the Sonnet 5 and Opus 4.8 pages; minus frontend_aesthetics (long), which was written for Opus 4.5 and Opus 4.6 and is the kind of prior-model prescription this page says to remove (F5-19, F5-70, O48-55, BP-025) |
| opus-5 | the guide-wide set minus self_check_verify, reflect_after_tool_results, subagent_usage_policy, context_compaction_persistence, spend_entire_context, frontend_aesthetics (long), and every verify, double-check, or re-verify line; plus o5_conciseness, tone_preference, o5_progress_updates, o5_deliverable_length, o5_scope_constraint, o5_delegation_guidance, o5_correction_narration, o5_thinking_disabled_mitigation, minimize_overengineering, and, as borrowed Opus 4.8 text with an Assumed entry, s5_code_review_coverage / o48_review_coverage (O5-12), o48_explicit_scope, o48_propose_directions, o48_aefrm_concrete_spec, frontend_aesthetics_short (O5-05) |
| sonnet-5 | the guide-wide set minus frontend_aesthetics (long), any forced progress cadence of the o5_progress_updates kind, and any sampling parameter; plus s5_conciseness / o48_conciseness, s5_low_effort_multistep / o48_low_effort_reasoning, think_only_when_useful (Sonnet 5 variant, alias s5_thinking_trigger_guard), s5_explicit_scope / o48_explicit_scope, s5_warm_tone / o48_warm_tone, s5_design_concrete_spec_aefrm / o48_aefrm_concrete_spec, s5_design_propose_directions (Sonnet 5 variant), frontend_aesthetics_short, s5_code_review_coverage / o48_review_coverage, s5_code_review_concrete_bar / o48_review_concrete_bar, minimize_overengineering |
| opus-4-8 | the guide-wide set minus frontend_aesthetics (long), context_compaction_persistence and any other block grafted on the strength of context awareness (BP-241 names Sonnet 5, Sonnet 4.6, Sonnet 4.5, and Haiku 4.5, not this model, and O48-05 routes the 1M context fact to the migration guide; spend_entire_context may still be grafted on multi-window work as a guide block that names no model, BP-261), temperature-for-variety, and any forced cadence; keeping from the base avoid_excessive_markdown_and_bullet_points, reflect_after_tool_results, and self_check_verify, and taking minimize_overengineering only with an Assumed entry naming Opus 4.5 and Opus 4.6 (BP-300 to BP-302, BP-025); plus the page-measured o48_conciseness, o48_low_effort_reasoning, o48_thinking_steer, o48_explicit_scope, o48_warm_tone, o48_aefrm_concrete_spec, o48_propose_directions in its own variant, frontend_aesthetics_short, o48_review_coverage, o48_review_concrete_bar, and o48_subagent_guidance |
| legacy-4x | the guide-wide set, with the four model-named guide blocks routed per model: frontend_aesthetics in its long form and minimize_overengineering stated for Opus 4.5 and Opus 4.6 and applied to the other five by analogy with the assumption recorded, context_compaction_persistence for Sonnet 4.6, Sonnet 4.5, and Haiku 4.5 only, with spend_entire_context grafted beside it there and also available to any target in this profile on multi-window work, since the guide prints it under a subsection that names no model (BP-261); autonomy_safety_confirmation always on Opus 4.6 and elsewhere when the side-effect signal fires; subagent_usage_policy mandatory on Opus 4.6, on Opus 4.5 and Opus 4.7 by analogy with the assumption recorded, and conditional elsewhere; commit_to_approach on Opus 4.6 when latency or thinking cost is raised; minus the Fable 5.1 defaults (progress_updates_line, batch_nudge, keep_changes_to_task, targeted_edits, formatting_in_chat_rule), which are page-measured additions elsewhere and never enter this row, and, on Opus 4.5 with thinking off, every snippet containing the word "think" (think_thoroughly, the low-effort multistep line, the thinking-trigger guard) |
