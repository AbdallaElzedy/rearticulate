# Worked rearticulations

Nine worked examples of the `/rearticulate` output shape: five common request types executed in-session on Fable 5.1
(examples 1 to 5), then three prompt-authoring requests whose target model differs from the executing model (examples 6
to 8: Opus 5, Sonnet 5, Opus 4.8), then one Fable 5 target (example 9), the profile whose deltas change a prompt's shape
most. Open this file when no row in references/request-taxonomy.md matches cleanly, and
pattern-match on the closest example. Sources: Prompting best practices
(https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), Prompting
Claude Fable 5.1 (https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1),
Prompting Claude Opus 5 (https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5),
Prompting Claude Sonnet 5
(https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5) and Prompting Claude
Opus 4.8 (https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8). BP-nnn,
F51-nnn, O5-nn, S5-nn and O48-nn IDs resolve in references/technique-catalog.md, snippet IDs in
references/snippet-library.md, and each rationale names the guide or page section headings it draws on.

Conventions used below:

- Tags inside <rearticulated_prompt> follow the order fixed in templates/rearticulated-prompt.md; conditional tags
  appear only where they apply (Structure prompts with XML tags). The <examples> tag inside a rearticulated prompt is
  the template tag; the outer <examples> block wraps this file's worked examples.
- The first assumptions line is always "Posture: act | assess. Inferred steps: ... Confirm before: ..."; the others
  start with Reading:, Assumed:, or Changed:. Three lines at most, four when a Target model line is present.
- When the target model differs from the executing model, a "Target model: <profile> (<how resolved>)" line follows the
  Posture line and carries the settings the prompt cannot set for itself: recommended effort with the page section it
  comes from, thinking configuration in the page's syntax, max_tokens headroom, parameters removed with their reason. The
  content of the rearticulated prompt follows the target profile; the skill's own narration, verification pass and recap
  follow the executing profile (Fable 5.1 in these examples). Snippets measured on one model are never carried to another.
- A grafted snippet longer than six lines is shown as its tag plus "gist:" and a one-line summary (SKILL.md Step 5
  display budget); short verbatim snippets appear in full once, then as a gist. The verbatim text in the snippet
  library governs execution and a dry run shows it in full. Snippets the guide wraps in XML keep that wrapper
  (BP-176); plain-text snippets are labelled with their snippet-library ID.
- {{UPPER_SNAKE}} tokens stand for content the executing turn reads or resolves (BP-070). System details are
  illustrative; the shape is what to copy.

<examples>

<example>
<raw_request>fix the login bug</raw_request>
<classification>
Row: code change. Secondary: none.
Signals: imperative verb with a target (fix, login bug); no file named; no symptom given; tests unknown until the
repository is searched; no external side effects; domain inferred from the repository once read.
Verdict: change. An imperative with a target asks for action even without a file name (Tool usage); the Finish the
whole task exception for questions does not apply. Posture: act.
</classification>
<assumptions>
Posture: act. Inferred steps: locate the login code path and reproduce the failure before editing. Confirm before: none.
Reading: "the login bug" is the failure the existing tests or the most recent error report in this session expose; if
neither turns one up, the turn ends with the search results and one question instead of a guessed edit.
Assumed: the fix stays inside the login module; tests are committed only where this repository already keeps them.
</assumptions>
<rearticulated_prompt>
<role>You are a senior software engineer specializing in debugging authentication code in this repository.</role>
<context>The user reported a login bug without naming a file or a symptom. The user will review and commit the diff,
so the change must be small and traceable to a reproduced failure, and the existing tests are the acceptance check.
Environment: Claude Code on Windows; repository conventions in CLAUDE.md apply.</context>
<task>Posture: act. Make the change described below.
1. Locate the login path: search the repository for login, authenticate and sign-in handlers, and list the tests that
   exercise them.
2. Reproduce: run those tests. If they pass, check git log for recent changes on the path and the conversation for an
   error message. The reproduced failure defines the bug.
3. Read every file on the path before forming a hypothesis, and identify the root cause rather than the first symptom.
4. Apply the smallest edit that fixes the root cause.
5. Re-run the tests from step 2.
If step 2 finds no failure and no report, make no edit; report what was searched and ask the one question that would
identify the bug.</task>
<constraints>Change only the code the reproduced failure requires, because the reviewer will read the diff against that
failure. It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality.
<keep_changes_to_task>gist: report pre-existing bugs and unmentioned behaviour as follow-ups; implement the reading the
wording and code most directly support and state it; scratch checks stay out of the repo; commit tests only where asked
or conventional; implement every requested behaviour completely.</keep_changes_to_task></constraints>
<output_format>Prose in this order: the reproduced failure (test name and the error line in a code block), the root
cause in one or two sentences, the change by file path, the test result after the change, follow-ups noticed but not
made.</output_format>
<success_criteria>The test that failed in step 2 passes; every other test in the same suite still passes; git diff
touches only the files named in the reply; the reply names the root cause.</success_criteria>
<execution_guidance>
<progress_updates_line>Before you start, say in a line what you're about to do; brief updates while you work help the
user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so
a reader who only sees the last message has the full picture.</progress_updates_line>
<default_to_action>gist: implement changes rather than only suggesting them; when intent is unclear, infer the most
useful action and use tools to discover missing details instead of guessing.</default_to_action>
<investigate_before_answering>Never speculate about code you have not opened. If the user references a specific file,
you MUST read the file before answering. Make sure to investigate and read relevant files BEFORE answering questions
about the codebase. Never make any claims about code before investigating unless you are certain of the correct
answer - give grounded and hallucination-free answers.</investigate_before_answering>
<targeted_edits>The number of tokens used to edit files is best minimized, all else being equal. Therefore, when it
will not affect the end result, try to surgically edit a file rather than rewrite the entire thing.</targeted_edits>
<temp_file_cleanup>If you create any temporary new files, scripts, or helper files for iteration, clean up these files
by removing them at the end of the task.</temp_file_cleanup>
<batch_nudge>First privately list what you need next; then request every item that doesn't depend on another's result
in this one response.</batch_nudge>
</execution_guidance>
<verification>Before you finish, verify your answer against: the reproduced test passes and the rest of its suite
passes; git status lists only the intended files; no scratch files remain.</verification>
</rearticulated_prompt>
<execution_notes>
First line to the user: "Searching for the login path and running its tests before changing anything."
Batch 1 (one response): Grep for login, authenticate and signin; Glob for the matching test files; git log on the
candidate paths. Batch 2: Read every file Batch 1 surfaced. Sequential: run the tests, edit, re-run (each depends on
the previous result). A short factual note follows each batch.
Verify: the test output, git status, git diff --stat, a listing of the scratchpad. Recap: found (failure and root
cause), done (files by path), left out and why, next (follow-ups). If step 2 found nothing, the turn still delivers
the search results and ends with the single question (Finish the whole task).
</execution_notes>
<rationale>
Be clear and direct, golden rule (BP-030): a colleague would ask which login and what breaks; tools answer both
(BP-154), so the prompt lists discovery steps instead of guessing, and the only question is deferred to the end of a
turn that delivers the search (F51-99). Verdict from Tool usage (BP-148) and the Finish the whole task exception
(F51-88); one posture snippet, default_to_action, wrapper kept (BP-152, BP-176). Minimizing hallucinations in agentic
coding (BP-313 to BP-317). Prefer targeted edits (F51-132, F51-136). Verification through the existing tests, Ask
Claude to self-check (BP-229 to BP-231), plus the tests sentence (BP-250). keep_changes_to_task stays verbatim inside
its tag (F51-117); positive framing (BP-031, BP-103) governs only the sentences the skill wrote. minimize_overengineering
left out to keep the prompt proportional to a bug fix (BP-197, BP-206). Fable 5.1 defaults: progress line first, batch
nudge last (F51-37, F51-43). Recap shape from F51-37, F51-100, F51-118.
</rationale>
</example>

<example>
<raw_request>can you suggest some improvements to reports/assets/render_pdf.py</raw_request>
<classification>
Row: question / assessment. Secondary: none.
Signals: suggestion phrasing (suggest); one named file; no imperative verb, no earlier edit request, no "go ahead" or
"apply"; no side effects.
Verdict: assessment. The guide names "can you suggest some changes" as phrasing that yields suggestions (Tool usage),
and no act signal is present, so the assess reading is taken and stated. Posture: assess.
</classification>
<assumptions>
Posture: assess. Inferred steps: read the file and find its callers before commenting. Confirm before: none (no edits
this turn).
Reading: "suggest improvements" is a review request, not a change request; reply "apply them" or name the items to
switch to act.
Assumed: improvements means correctness, robustness and maintainability of the PDF rendering path as this repository
actually invokes it, not style preferences.
</assumptions>
<rearticulated_prompt>
<role>You are a senior Python reviewer specializing in document-rendering scripts and their operational reliability.</role>
<context>reports/assets/render_pdf.py renders the report HTML deliverables in this workspace to PDF. The user
wants a review to act on later, so each finding must be specific enough to implement in a later turn. This turn is
read-only.</context>
<task>Posture: assess. Deliver findings and recommendations; change no files.
1. Read reports/assets/render_pdf.py in full, then search the repository for its callers and any notes on how
   it is invoked.
2. Evaluate it under four headings: correctness (missing inputs, path handling), robustness (dependencies, error
   reporting), maintainability (structure, naming, dead code), and fit with how the repository calls it.
3. For each finding give the line range, the problem in one sentence, and the concrete change you would make.
4. Order the findings by impact, highest first.</task>
<constraints>Use Read, Grep and Glob only, because the deliverable is the assessment; if a finding could only be
confirmed by running or editing the script, say so rather than doing it. Base each finding on lines you read. Leave out
stylistic preferences with no functional effect.</constraints>
<output_format>A numbered list, one entry per finding: line range, problem, recommended change. A list is wanted
because the items are discrete and the user will pick from them. Close with a two-sentence overall verdict and one line
offering to apply all or selected items.</output_format>
<success_criteria>Every finding cites a line range that exists in the file as read; git status is unchanged; each
recommendation can be implemented without a further question; the highest-impact finding is first.</success_criteria>
<execution_guidance>
<progress_updates_line>gist: one line before starting, brief updates while working, a recap that stands alone.</progress_updates_line>
<do_not_act_before_instructions>gist: no implementation or file changes unless clearly instructed; when intent is
ambiguous, provide information, research and recommendations.</do_not_act_before_instructions>
<investigate_before_answering>gist: read the named file and the relevant files before any claim about the code.</investigate_before_answering>
<batch_nudge>First privately list what you need next; then request every item that doesn't depend on another's result
in this one response.</batch_nudge>
</execution_guidance>
<verification>Before you finish, verify your answer against: each cited line range matches the file content; git
status shows no modified files; the list is ordered by impact.</verification>
</rearticulated_prompt>
<execution_notes>
First line to the user: "Reading render_pdf.py and finding where the repository calls it; no edits this turn."
Batch 1 (one response): Read the file, Grep the repository for render_pdf, Glob for tests or docs beside it. No Edit
or Write calls; a recommendation that would need a run to confirm is flagged as unverified (BP-159).
Verify: re-open the cited ranges, run git status. Recap: findings in rank order, nothing changed, next is the user's
pick. The offer to apply is a follow-up at the end, not a permission request mid-task.
</execution_notes>
<rationale>
Tool usage names this exact phrasing as the less effective way to ask for a change (BP-146, BP-149), and the Finish
the whole task exception says a question or thinking out loud earns an assessment, reported and then stopped (F51-88).
With no act signal, the assess reading is chosen and written into <task> so the executing turn does not re-decide it
(BP-155). One posture snippet, do_not_act_before_instructions (BP-156 to BP-159); operating_autonomously is not
grafted under assess. Had the user written "go ahead and improve render_pdf.py", the task would open "Change
render_pdf.py to ..." (BP-150) with default_to_action. The list is stated positively as wanted because Fable 5.1
reaches for lists less (F51-72). Minimizing hallucinations in agentic coding (BP-316). Verification checks the
read-only criterion so the turn cannot drift into edits (BP-229).
</rationale>
</example>

<example>
<raw_request>analyze annual_report_2023.pdf, competitor_analysis_q2.xlsx and board_minutes.docx and tell me the strategic risks</raw_request>
<classification>
Row: long-document analysis. Secondary: question / assessment (the deliverable is an analysis).
Signals: three named documents (two or more sources makes the XML document structure mandatory); combined size likely
at or above 20k tokens (about 80 KB of text, checked with ls first); "tell me" asks for findings; two binary formats
need conversion before reading; no side effects.
Verdict: assessment. Posture: assess.
</classification>
<assumptions>
Posture: assess. Inferred steps: check the three files' sizes, convert the xlsx and docx to text in the scratchpad, read
all three. Confirm before: none.
Assumed: the files are in the working directory or at the paths the user names; "strategic risks" means threats to the
organisation's stated strategy, market position or plans that the documents state or imply.
Changed: the question moves after the documents and a quotes-first step is added, because queries at the end improve
responses by up to 30 percent with multi-document inputs.
</assumptions>
<rearticulated_prompt>
<role>You are a strategy analyst specializing in synthesising financial reports, competitive analyses and governance
records into evidence-based risk assessments.</role>
<context>The assessment will inform a board-level discussion, so every risk must trace to source text; readers will
check claims against the documents. Documents come first and the question last because that ordering improves results
with complex multidocument inputs. Quoting first concentrates the analysis on the relevant passages and lets the rest
of each document be ignored.</context>
<documents>
  <document index="1">
    <source>annual_report_2023.pdf</source>
    <document_content>{{ANNUAL_REPORT}}</document_content>
  </document>
  <document index="2">
    <source>competitor_analysis_q2.xlsx</source>
    <type>spreadsheet, sheets converted to CSV text</type>
    <document_content>{{COMPETITOR_ANALYSIS}}</document_content>
  </document>
  <document index="3">
    <source>board_minutes.docx</source>
    <document_content>{{BOARD_MINUTES}}</document_content>
  </document>
</documents>
<task>Posture: assess. Deliver the analysis; change no files.
1. Quote the passages from annual_report_2023.pdf, competitor_analysis_q2.xlsx and board_minutes.docx that describe a
   threat to the organisation's strategy, market position or stated plans, in <quotes> tags, each quote labelled with
   its document index.
2. Then, based on these quotes, identify the strategic risks, name the documents supporting each, and note where the
   sources disagree.
3. Rank the risks by severity and strength of evidence, stating a confidence level for each.</task>
<constraints>Use the three documents as the only evidence; a risk the documents do not support is left out rather than
supplied from general knowledge, because the readers will check every claim against the sources. Convey source content
in your own words apart from the marked quotes.</constraints>
<output_format>Two tagged sections: <quotes>, the extracted passages each labelled [doc n]; then <risks>, the ranked
risks as prose, one paragraph per risk ending with the supporting document indexes in brackets.</output_format>
<examples>
<example>gist of quoting_sources_example: one user request, one response that organises by agreement and difference and
conveys each source in indirect speech with a single marked phrase, one rationale sentence; the two [web_search: ...]
lines replaced by [Read: annual_report_2023.pdf] style lines.</example>
</examples>
<success_criteria>Every risk in <risks> cites at least one quote in <quotes>; every quote is verbatim from the named
document; source wording appears only as marked quotations and every other claim is reworded; risks are ordered by
severity; disagreements between documents are called out.</success_criteria>
<execution_guidance>
<progress_updates_line>gist</progress_updates_line>
<do_not_act_before_instructions>gist</do_not_act_before_instructions>
<batch_nudge>First privately list what you need next; then request every item that doesn't depend on another's result
in this one response.</batch_nudge>
</execution_guidance>
<verification>Before you finish, verify your answer against: each quote is found by search in its converted source;
each risk cites at least one quote; no risk rests on knowledge outside the documents; the order matches the stated
severities.</verification>
</rearticulated_prompt>
<execution_notes>
First line to the user: "Checking the three documents' sizes and converting the spreadsheet and minutes to text."
Batch 1 (one Bash call): sizes of the three files and availability of a Python xlsx and docx reader. Batch 2: convert
xlsx and docx to text files in the scratchpad (two independent commands). Batch 3: Read the PDF by page range and the
two text files in one response; the placeholders resolve to what was read. Then write <quotes>, then <risks>.
Verify: Grep each quote in its converted text; count citations per risk. Remove the scratchpad conversions before the
recap. Recap: risks found in rank order, sources used, anything unreadable and why, next (deeper dives offered).
</execution_notes>
<rationale>
Long context prompting: the 20k threshold and the multi-source rule (BP-060, BP-065) make <documents> mandatory; data
at the top for every model (BP-061, BP-062); query last with the 30 percent figure in <context> (BP-063); role and
brief context still precede the data (BP-075); the task names each document by source with explicit verbs (BP-071).
Document skeleton with sequential index, source with extension, metadata subtag only where the format matters (BP-066
to BP-069); placeholders in the display (BP-070). Quotes-first grounding names the documents and the relevance
criterion, uses <quotes>, continues with "Then, based on these quotes", and puts the answer in a second tag (BP-072,
BP-076 to BP-079). Quoting retrieved sources: one example is the exception to the 3 to 5 rule, tool name substituted
(F51-76 to F51-78); the marked-quotation criterion comes from F51-75. Assess posture F51-88; cleanup BP-299.
</rationale>
</example>

<example>
<raw_request>write the leadership summary of the service outage, it will be read aloud on the ops call</raw_request>
<classification>
Row: writing / formatting. Secondary: none (one source document, well under the long-context threshold).
Signals: write, summary, a spoken consumer (read aloud), a non-technical audience (leadership), an incident domain with
a workspace rule on neutral wording; no side effects (the text is returned in the reply, not sent). Verdict: change
(produce the deliverable). Posture: act.
</classification>
<assumptions>
Posture: act. Inferred steps: locate and read the service outage report in this workspace before writing. Confirm
before: none.
Assumed: read aloud means spoken from the text as written, by the presenter or a text-to-speech engine, so the text
must be pronounceable; about ninety seconds spoken, which is roughly two hundred words.
Changed: the workspace rule on neutral incident language goes into <constraints>; the Fable 5.1 formatting rule is used
instead of an anti-markdown block, and mannered prose is removed by instruction.
</assumptions>
<rearticulated_prompt>
<role>You are an incident communications writer specializing in briefing non-technical leadership in plain spoken
English.</role>
<context>The summary will be read aloud on the operations call by the presenter or a text-to-speech engine, to leaders
who have not followed the technical detail. Facts come from the incident report below; the writer adds no new facts.
Institutional incident communications use neutral, observed-fact wording.</context>
<documents>
  <document index="1">
    <source>{{INCIDENT_REPORT_PATH}} (the service outage report, located at execution)</source>
    <document_content>{{INCIDENT_REPORT}}</document_content>
  </document>
</documents>
<task>Posture: act. Write the deliverable described below.
1. Read the incident report and note the facts a leader needs: what happened, what was affected, what has been done,
   what is still open, what leadership is asked to decide.
2. Write the summary as speech: short declarative sentences, numbers spelled the way a speaker says them, acronyms
   expanded on first use because the listener cannot see them.
3. Present it inside <summary> tags, beginning with the first sentence of the summary itself.</task>
<constraints>Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech
engine will not know how to pronounce them; the same reason rules out brackets, slashes, symbols and bare acronyms. Use
neutral observed-fact terms (accessed, the actor, unauthorized change) in place of breach, attack, fraud, victim,
takeover, disclosure or exposed, because institutional incident communications avoid liability language. State only
facts present in the report; where the report is uncertain, say so plainly.</constraints>
<output_format>Your response should be composed of smoothly flowing prose paragraphs: three or four, about two hundred
words in total, in the order what happened, what was affected, what has been done, what is open, what leadership is
asked to decide. Paragraphs carry the structure because the listener cannot see a list. Use lists and bullet points
when asked to, or when the content is multifaceted enough that they help with clarity. If the person explicitly
requests minimal formatting, always format your responses without bullet points, headers, lists, or bold emphasis, as
requested. In conversational, personal, or emotional exchanges, keep to plain prose. Please remove all mannered
prose.</output_format>
<examples>
<example>Over the past two weeks an outside party used a stored configuration key to copy mail from six mailboxes in one
department.</example>
<example>We do not yet know whether any of the copied mail contained regulated personal data; the review of the export
finishes on Friday.</example>
<example>We are asking for approval to rotate the affected keys on every mail server by the end of the month.</example>
</examples>
<success_criteria>Spoken length about ninety seconds (two hundred to two hundred and thirty words); no ellipses,
bullets, headers, bold, brackets or unexpanded acronyms; every fact traces to the report; none of the avoided words
appears; the five parts appear in order; the response starts with the summary's first sentence.</success_criteria>
<execution_guidance>
<progress_updates_line>gist</progress_updates_line>
<default_to_action>gist</default_to_action>
<batch_nudge>First privately list what you need next; then request every item that doesn't depend on another's result
in this one response.</batch_nudge>
</execution_guidance>
<verification>Before you finish, verify your answer against: the word count; a scan of the text for ellipsis
characters, three consecutive dots, markdown symbols, brackets, unexpanded acronyms and the avoided words; each factual
sentence matched to a passage in the report.</verification>
</rearticulated_prompt>
<execution_notes>
First line to the user: "Reading the service outage report, then drafting a two-hundred-word spoken summary."
Batch 1 (one response): Glob for the incident report and Read it, or Read directly when the path is already known.
Draft, then run the scan named in verification on the draft (a short Python check in the scratchpad is acceptable and
is removed afterwards). Recap: source used, what the summary covers, what the report left uncertain and how the summary
flags it, next (a written version for the call notes, if wanted).
</execution_notes>
<rationale>
Add context to improve performance: the TTS motivation is grafted with its reason (BP-037, BP-039) and generalised to
brackets and acronyms rather than enumerated (BP-040). Control the format of responses: prose stated positively
(BP-103, BP-104), lead sentence and named output tag in place of a preamble ban (BP-135, BP-136), prompt written
without markdown to match the output (BP-107, BP-109), the Formatting in chat rule on Fable 5.1 in place of the
anti-markdown block (BP-115, BP-116, F51-73, F51-74), the reason lists are unwanted stated positively (F51-72).
Writing density: the short mannered-prose instruction because the prompt is already long (F51-69, F51-70). Use
examples effectively: three samples, domain-relevant, varied in length, one covering the uncertainty edge case, each
in <example> (BP-041 to BP-046); they show sentence shape, the facts come from the report. Workspace norms supplied
(BP-029); length stated (BP-027); the long-output budget note omitted because the deliverable is short (F51-138).
</rationale>
</example>

<example>
<raw_request>migrate all the ingest-monitor query probes to the new analytics CLI and make sure nothing breaks</raw_request>
<classification>
Row: agentic long-horizon. Secondary: code change (contributes keep_changes_to_task and targeted edits).
Signals: "migrate all" (many files, many steps, possibly more than one context window); "nothing breaks" (regression
check against a baseline, tests); a target system that fails under concurrency (a rate-limited analytics API returns 500s to
parallel queries); git present; no tenant writes expected (probes are read-only queries). Verdict: change. Posture: act.
</classification>
<assumptions>
Posture: act. Inferred steps: inventory the probes and record a baseline of their results before changing any. Confirm
before: git commit (not requested, offered at the end); any command that writes to the tenant (none expected).
Assumed: "nothing breaks" means every migrated probe returns the same coverage and alert decision as the baseline on a
fixed window and the ingest-monitor test suite still passes; this runs in one session, so state files live in the scratchpad
and are removed at the end (say "continue later" to keep them in the project).
Assumed: probe runs are serialised because the tenant throttles concurrency; file reads and edits stay batched.
</assumptions>
<rearticulated_prompt>
<role>You are a senior platform engineer specializing in Python migrations of query tooling against the Cortex the analytics platform
API and its command-line client.</role>
<context>ingest-monitor monitors ingestion health across the analytics platform datasets through per-dataset query probes. The probes must move
from their current query path to the analytics CLI (analytics.exe, invoked through Bash because PowerShell 5.1 strips quotes
and produces bogus 500s). The security team relies on ingest-monitor alerts; a silent change in probe output would hide a
dead feed, which is why baseline comparison outranks speed. This runs in Claude Code, whose context is compacted as it
fills. The tenant returns 500s under concurrent queries. Repository conventions in CLAUDE.md apply.</context>
<task>Posture: act. Make the change described below. This is the first window of a possibly multi-window task: steps 1
to 3 set up the framework, step 4 iterates.
1. Inventory every probe (file, dataset, query form) into {{SCRATCHPAD}}/tests.json with status not_started, following
   the tests.json schema in the snippet library.
2. Create {{SCRATCHPAD}}/init.sh that runs the ingest-monitor test suite and every probe on a fixed window and writes a
   baseline file; run it once and record each probe's baseline outcome in tests.json.
3. Create {{SCRATCHPAD}}/progress.txt with the plan and the decisions so far.
4. Migrate one dataset at a time: edit its probe to call the CLI, run that probe on the same window, compare with the
   baseline, set its tests.json status, append a progress note. Continue until every probe is migrated.
5. Run init.sh again: every probe matches the baseline and the suite passes.
6. Remove iteration-only scratch files; keep tests.json and progress.txt until the recap is written, then remove them.</task>
<constraints>Change only the probe query path and what the CLI call requires (argument quoting, output parsing); alert
thresholds, baselines and dashboards stay as they are, because the migration must be invisible to alert consumers. It
is unacceptable to remove or edit tests because this could lead to missing or buggy functionality.
<keep_changes_to_task>gist: pre-existing bugs become follow-ups; implement the most direct reading and state it; scratch
checks stay out of the repo; commit tests only where asked or conventional; implement everything asked, completely.</keep_changes_to_task></constraints>
<output_format>A one-line progress update as each dataset completes (dataset, match or mismatch). A final recap in
prose with one table: probe, old path, new CLI call, baseline match, note; then a paragraph of follow-ups noticed but
not made.</output_format>
<success_criteria>tests.json shows every probe passing; init.sh exits zero with every probe matching the baseline on the
fixed window; the ingest-monitor suite passes; git diff touches only probe files and the CLI adapter; no scratch files
remain; the recap names any probe left unmigrated and why.</success_criteria>
<execution_guidance>
<progress_updates_line>gist</progress_updates_line>
<default_to_action>gist</default_to_action>
<use_parallel_tool_calls>gist: independent reads, searches and edits in one response; dependent calls in sequence;
never placeholders or guessed parameters. Applies to file operations.</use_parallel_tool_calls>
<reduce_parallel_execution>Execute operations sequentially with brief pauses between each step to ensure stability.
(Applies to analytics.exe calls, because the tenant returns 500s under concurrency.)</reduce_parallel_execution>
<targeted_edits>gist: surgically edit rather than rewrite when the result is the same.</targeted_edits>
<delivering_work>gist: the request sets the scope and the scope is the deliverable; make routine calls yourself; do
everything independent of a question before asking it; a decided step is run, not announced; extras are end-of-task
suggestions.</delivering_work>
<autonomy_safety_confirmation>gist: local reversible actions proceed; ask before destructive, hard-to-reverse or
visible-to-others actions; no destructive shortcuts such as --no-verify. Stop and ask in the chat before: git commit;
any command that writes to the tenant.</autonomy_safety_confirmation>
<subagent_usage_policy>gist: subagents for parallel, isolated workstreams; work directly for sequential, single-file or
context-dependent steps. Continue independent work while a subagent runs and collect its result afterward.</subagent_usage_policy>
<context_compaction_persistence>gist: the context window compacts; save progress to tests.json and progress.txt before
it does; do not stop early because of the token budget.</context_compaction_persistence>
<spend_entire_context>gist: plan the work; spend the output context on the task; do not run out of context with
significant unrecorded work.</spend_entire_context>
<temp_file_cleanup>gist: remove temporary files, scripts and helpers at the end.</temp_file_cleanup>
<batch_nudge>First privately list what you need next; then request every item that doesn't depend on another's result
in this one response.</batch_nudge>
</execution_guidance>
<verification>Before you finish, verify your answer against: the init.sh exit code and per-probe baseline match; the
suite result; tests.json has no not_started or failing entries; git status lists only probe files and the adapter; the
scratchpad holds no leftover files.</verification>
</rearticulated_prompt>
<execution_notes>
First line to the user: "Inventorying the ingest-monitor probes and taking a baseline before changing any of them."
Batch 1 (one response): Glob the probe files, Read the query client module, Grep the query call sites, git status and
git log. Sequential: init.sh baseline (each analytics.exe call one at a time). Per dataset: Edit, run the probe, compare (a
dependent chain); edits for several datasets may share one batch, their probe runs may not. After each dataset update
tests.json and append progress.txt, so a compaction loses nothing. A resumed window opens with the fresh-start lines:
call pwd; review progress.txt, tests.json and the git log; run init.sh before touching new probes.
Verify: init.sh, the suite, tests.json, git status. Remove scratch files. Recap: found, done (files by path, baseline
result), left out and why, next; the offer to commit sits at the end of the turn.
</execution_notes>
<rationale>
Long-horizon reasoning and state tracking, and Workflows across multiple context windows: the first window sets up
tests, a setup script and notes, later windows iterate (BP-248, BP-249, BP-251); tests.json schema and progress-notes
shape (BP-262, BP-263, BP-267, BP-268); fresh-start lines for a resumed window (BP-252, BP-254 to BP-256); git is the
state record, commits only when asked, never a push (BP-264). Context awareness and multiwindow workflows: the harness
compacts, so the persistence and full-context blocks are grafted and <context> says so (BP-244, BP-246, BP-260,
BP-261). Balancing autonomy and safety: the block plus the confirm list from Step 1 (BP-269 to BP-276, F51-92). Finish
the whole task: delivering_work grafted whole for this attended run (F51-95 to F51-102); operating_autonomously is
added whole, first sentence unchanged, only when the user says they are stepping away (F51-86, F51-91). Optimize
parallel tool calling: parallel for file work, the sequential sentence scoped to tenant calls (BP-167 to BP-173).
Subagent orchestration plus the lead-keeps-working sentence (BP-289, BP-290, F51-143). Keep changes and tests to what
the task asks for (F51-117, BP-250). Reduce file creation: cleanup (BP-298, BP-299), state files named by full path
before creation. Prefer targeted edits (F51-136). Fable 5.1 defaults: progress line, batch nudge (F51-37, F51-43).
</rationale>
</example>

<example>
<raw_request>write a system prompt for our support bot on claude-opus-5 that answers in plain prose and NEVER uses ellipses or markdown</raw_request>
<classification>
Row: prompt authoring for another model. Secondary: writing / formatting (the authored prompt governs prose output).
Signals: "write a system prompt for" with a model named after "on" (the deliverable is for that model, so the target row
switches); an all-caps prohibition with no reason; two negative-only format rules beside their positive form (plain prose);
no files named, so an existing bot prompt is searched for; no side effects (the prompt is returned, not deployed). Verdict:
change (produce the deliverable). Posture: act.
</classification>
<assumptions>
Posture: act. Inferred steps: search the workspace for an existing support-bot prompt or product notes; product facts not
found become {{PLACEHOLDERS}}. Confirm before: none.
Target model: opus-5 (named in the request as claude-opus-5; executing model Fable 5.1). Settings: effort starts at the
default high, tuned from evals with low and medium where quality holds (Capability improvements); thinking on by default,
disabled only at effort high or below with thinking: {type: "disabled"}, thinking on at lower effort preferred (Running
with thinking disabled); effort does not shorten visible replies, so length is set in the prompt; max_tokens pinned; no prefill.
Reading: "plain prose" means paragraphs of complete sentences with no lists, headers, bold or code fences; the ellipsis and
markdown rule is a rendering constraint of a plain-text chat widget that shows markdown symbols literally and in which
ellipses read as hesitation; the reason is inferred and written into the prompt.
Changed: NEVER and the two bare prohibitions become one positive formatting instruction with its reason; o5_conciseness,
o5_correction_narration and tone_preference (last) added; no verification, double-check or do-not-think rule in the
authored prompt; <verification> omitted from this block because the target is Opus 5, its checks moved to <success_criteria>.
</assumptions>
<rearticulated_prompt>
<role>You are a prompt engineer specializing in system prompts for customer-support assistants on the Claude API.</role>
<context>The deliverable is a system prompt that will run on Claude Opus 5 (API string claude-opus-5) behind a customer
support bot. Replies render in a plain-text chat widget, so markdown symbols would appear literally and ellipses would read
as hesitation; that is why plain prose is wanted. Opus 5 replies run longer than prior models and effort does not shorten
them, so length is set in the prompt; it verifies its own work and narrates corrections readily, so the prompt states both
explicitly and carries no verification instruction. Prompting Claude Opus 5 is the model page; the prompt is returned, not deployed.</context>
<task>Posture: act. Write the deliverable described below.
1. Search the workspace for an existing support-bot prompt or product notes (Grep for support and system prompt across md,
   txt, yaml and py files) and read anything found; otherwise use {{PRODUCT_NAME}}, {{SCOPE_OF_SUPPORT}}, {{ESCALATION_PATH}}.
2. Draft the system prompt, in order: a one-sentence role; the identity sentences "The assistant is Claude, created by
   Anthropic. The current model is Claude Opus 5." as plain text; the support scope and escalation rule; the formatting
   instruction stated as what to do with its reason (smoothly flowing prose paragraphs of complete sentences, because the
   widget shows markdown symbols literally and ellipses read as hesitation); the three reply examples from <examples>;
   o5_conciseness verbatim; o5_correction_narration verbatim; <tone_preference> verbatim as the closing lines.
3. Write the API skeleton: model claude-opus-5, the prompt in the system parameter, max_tokens pinned, no thinking field.
4. Scan the draft for markdown symbols, ellipses, all-caps words, and any verify, double-check or do-not-reason sentence;
   remove what the scan finds.</task>
<constraints>Keep the system prompt to what the request asks (support scope, plain prose, no ellipses or markdown) plus the
Opus 5 length and correction instructions, because every extra rule is one the bot will follow. Write each rule as what to
do, with its reason, so the bot generalises to unlisted cases. No verification or re-check instruction and no rule against
thinking, because Opus 5 self-verifies and such rules add cost or leak internal tags. Files created or modified: none.</constraints>
<output_format>The system prompt in one fenced text block, written in the same plain prose it asks for; then the API
skeleton as a JSON block; then three to five plain sentences on settings: the default high effort and the low or medium
sweep, thinking on by default and disabled only at high or below, max_tokens as the hard ceiling, and no prefill.</output_format>
<examples>
<example>Two charges in one month usually mean the plan renewed on the day a seat was added. Your invoice shows both on the
3rd, so both charges are expected. If you did not add a seat, reply here and I will open a billing ticket for you.</example>
<example>Password resets go to the address on the account within a few minutes. Yours went out at 14:02 today. If it has not
arrived, check the spam folder first, then tell me and I will resend it.</example>
<example>Earlier I said the export limit was 500 rows; it is 5,000 for your plan, which changes what you can do here. You can
export the whole report in one file.</example>
</examples>
<success_criteria>The system prompt contains, in order: one role sentence, the two identity sentences, the scope and
escalation rule, the formatting instruction with its reason, the three reply examples, the two Opus 5 snippets verbatim and
<tone_preference> last; it contains no markdown symbol, ellipsis, three consecutive dots, all-caps word, or verify,
double-check or do-not-think sentence; the skeleton pins model claude-opus-5 and max_tokens and has no thinking or
budget_tokens field; the settings sentences state the thinking default and the cap on disabling it; files created or modified: none.</success_criteria>
<execution_guidance>
<progress_updates_line>gist</progress_updates_line>
<default_to_action>gist</default_to_action>
<batch_nudge>First privately list what you need next; then request every item that doesn't depend on another's result
in this one response.</batch_nudge>
</execution_guidance>
</rearticulated_prompt>
<execution_notes>
First line to the user: "Looking for an existing support-bot prompt in the workspace, then drafting the Opus 5 system prompt."
Batch 1 (one response): Grep for support and system prompt, Glob for prompt files, Read the snippet library entries for the
three Opus 5 snippets. Draft, then the scan from task step 4 (a short regex check in the scratchpad, removed afterwards).
No <verification> tag: Step 7 runs the <success_criteria> checks on Fable 5.1, the executing model, and reports them; the
Opus 5 exception governs the authored prompt's content, not the skill's closing pass. Recap: what the workspace held, the
prompt and skeleton delivered, settings stated, next (an effort sweep on the team's evals).
</execution_notes>
<rationale>
Prompt authoring row: role and standing instructions in the system parameter, task in the user message (BP-056); model
string and max_tokens pinned (BP-059); identity sentences as plain text, unsubstituted because the guide's sample already
names Opus 5 (BP-081, BP-082, BP-087); no prefill on a 4.6+ model (BP-124). Add context to improve performance: the
all-caps bare prohibition is the guide's own less-effective example, converted to a motivated positive instruction with
the inferred reason recorded and written once (BP-037 to BP-040); prose stated as what to do, in a prompt written in the
style it asks for (BP-103, BP-104, BP-107). Opus 5 row (BP-017): explicit length because Opus 5 runs longer and effort
does not shorten it (BP-094 to BP-096; O5-27 to O5-31); tone_preference as the end-of-prompt reminder (O5-32, O5-33);
correction narration limited to corrections that matter (O5-58, O5-59); reply examples because positive examples beat
prohibitions (O5-38). No verification or re-check instruction and no rule against thinking (BP-232, BP-233; O5-43,
O5-57, O5-66), so <verification> is omitted and its checks live in <success_criteria>, which Step 7 still runs on the
executing model. Settings: effort default high with low and medium as the cost control (O5-13 to O5-16); thinking on by
default, disabling capped at high, thinking on at lower effort preferred (O5-06, O5-60, O5-62; BP-227). Three support
examples, varied, one a correction edge case (BP-043, BP-044, BP-046). Fable 5.1 executing defaults (F51-37, F51-43).
</rationale>
</example>

<example>
<raw_request>same bot but for --model sonnet-5</raw_request>
<classification>
Row: prompt authoring for another model (carried from the previous turn). Secondary: writing / formatting.
Signals: --model flag present, stripped from the raw request and resolved to sonnet-5 ahead of any model named in text;
"same bot" points at the previous turn's deliverable, which supplies the product facts, scope and plain-prose requirement;
no files; no side effects. Verdict: change. Posture: act.
</classification>
<assumptions>
Posture: act. Inferred steps: take the Opus 5 system prompt from the previous turn as the base and re-derive every
model-specific part. Confirm before: none.
Target model: sonnet-5 (--model flag; executing model Fable 5.1). Settings: effort defaults to high, xhigh for the hardest
work, medium where cost matters, re-derived rather than carried from the Opus 5 turn (Calibrating effort and thinking
depth); adaptive thinking on by default, turned off with thinking: {type: "disabled"}, thinking on at lower effort the
better trade; temperature, top_p and top_k removed because any non-default value returns a 400 (Tone and writing style);
budget_tokens returns a 400; max_tokens gets about 30 percent headroom because the tokenizer produces about 30 percent more tokens.
Reading: "same bot" keeps the role, product facts, scope, escalation rule, reply examples and the plain-prose instruction
with its reason; only the model-specific parts change.
Changed: o5_conciseness, o5_correction_narration and tone_preference removed as Opus 5-measured; s5_conciseness added
because the product fixes the verbosity; every rule given explicit scope because Sonnet 5 does not generalise an
instruction from one item to another; identity sentence substituted; <verification> present again (target is not Opus 5).
</assumptions>
<rearticulated_prompt>
<role>You are a prompt engineer specializing in system prompts for customer-support assistants on the Claude API.</role>
<context>The deliverable is the previous turn's support-bot system prompt re-targeted to Claude Sonnet 5 (API string
claude-sonnet-5) for the same plain-text widget, which shows markdown symbols literally. Sonnet 5 reads prompts literally,
most of all at lower effort, and does not generalise a rule from one item to another, so every rule names its scope; its
reply length tracks task complexity unless the prompt fixes it; sampling parameters are not accepted. Prompting Claude
Sonnet 5 is the model page for this target. The prompt is returned in the reply, not deployed.</context>
<documents>
  <document index="1"><source>previous turn: the Opus 5 support-bot system prompt and skeleton</source>
    <document_content>{{OPUS5_SUPPORT_PROMPT}}</document_content></document>
</documents>
<task>Posture: act. Write the deliverable described below.
1. Start from document 1. Keep the role, product facts, scope and escalation rule, the formatting instruction with its
   reason, and the three reply examples.
2. Remove o5_conciseness, o5_correction_narration and <tone_preference>. Change the identity sentence to "The current model
   is Claude Sonnet 5."
3. Give every rule its scope in the pattern "Apply this formatting to every section, not just the first one": the
   formatting rule covers every reply, including follow-ups, refusals and escalation messages; the scope rule covers every
   request outside {{SCOPE_OF_SUPPORT}}, however it is phrased.
4. Add s5_conciseness verbatim: "Provide concise, focused responses. Skip non-essential context, and keep examples minimal."
5. Write the API skeleton: model claude-sonnet-5, the prompt in the system parameter, max_tokens with the tokenizer headroom,
   no thinking field, and no temperature, top_p or top_k.
6. Scan the prompt for markdown symbols, ellipses, all-caps words, the string Opus, and any rule without a stated scope.</task>
<constraints>Keep the base prompt's substance and change only the model-specific parts (identity, snippets, scope wording,
skeleton), because the user asked for the same bot. Sampling parameters and budget_tokens stay out of the skeleton, because
Sonnet 5 returns a 400 for them. Files created or modified: none.</constraints>
<output_format>The system prompt in one fenced text block in plain prose; then the skeleton as a JSON block; then three to
five plain sentences on settings: effort default high with xhigh and medium as the sweep; thinking on by default and the
disable syntax, thinking on at lower effort preferred; the tokenizer note behind max_tokens; the sampling parameters removed and why.</output_format>
<success_criteria>The prompt keeps the base role, facts, scope rule, formatting instruction and reply examples; it contains
the Sonnet 5 identity sentence and s5_conciseness verbatim, no Opus 5 snippet, and a stated scope on every rule sentence;
the skeleton pins model claude-sonnet-5 and max_tokens and has no thinking, budget_tokens, temperature, top_p or top_k
field; the settings sentences state the thinking default, the disable syntax, the 400 on sampling parameters and the
tokenizer note; files created or modified: none.</success_criteria>
<execution_guidance>
<progress_updates_line>gist</progress_updates_line>
<default_to_action>gist</default_to_action>
<batch_nudge>First privately list what you need next; then request every item that doesn't depend on another's result
in this one response.</batch_nudge>
</execution_guidance>
<verification>Before you finish, verify your answer against: a scan of the prompt text for markdown symbols, ellipses,
all-caps words and the string Opus; each rule sentence read for a stated scope; the skeleton parsed as JSON with exactly
the keys model, max_tokens, system and messages.</verification>
</rearticulated_prompt>
<execution_notes>
First line to the user: "Re-targeting the support-bot prompt from the previous turn to Sonnet 5."
Batch 1 (one response): Read the snippet library entries for s5_conciseness and s5_explicit_scope; the base prompt is
already in the conversation. Edit the base, then run the scan and the JSON parse from task step 6 (a short check in the
scratchpad, removed afterwards). Verify per <verification>. Recap: what changed against the Opus 5 version (removed, added,
reworded), the skeleton differences, settings stated, next (an effort sweep; if the team ran Sonnet 4.6 before, medium on
Sonnet 5 is comparable to high on Sonnet 4.6 and high to max).
</execution_notes>
<rationale>
The --model flag outranks a model named in text and is stripped from the raw request (design spec addendum, model
resolution). Sonnet 5 row (BP-016): response length set explicitly because it tracks task complexity by default (S5-06 to
S5-08); literal instruction following means each rule states its scope in the s5_explicit_scope pattern (S5-42, S5-44,
S5-45); the positive reply examples stay because they counter verbosity habits better than prohibitions (S5-09).
Model-tagged snippets apply only to their model, so the Opus 5 conciseness, correction and tone_preference snippets are
removed rather than carried (BP-025; O5-31, O5-33, O5-59). Settings re-derived for the new target: effort default high,
xhigh for the hardest work, medium for cost, never copied across models (S5-11 to S5-19); adaptive thinking on by default,
thinking: {type: "disabled"} to turn it off, thinking on at lower effort preferred (S5-24, S5-25, S5-27); manual extended
thinking returns a 400 (S5-31; BP-189); temperature, top_p and top_k return a 400 and tone is steered by the prompt
(S5-49); max_tokens headroom for thinking plus reply and the tokenizer's roughly 30 percent increase (S5-26, S5-32, S5-33).
Identity substituted for the target (BP-081, BP-082); system parameter and pinned model string (BP-056, BP-059); no
prefill (BP-124); no forced progress cadence to strip (S5-40). The previous deliverable is data in <documents>, one short
source so the tag is optional (BP-049, BP-065, BP-070). <verification> returns because the exception is Opus 5 only
(BP-232). Fable 5.1 executing defaults (F51-37, F51-43). Note which half of the prompt each rule governs: <execution_guidance>
and <verification> steer this turn and so follow the executing profile, which is why progress_updates_line and batch_nudge
appear here even though the Sonnet 5 profile grafts neither into an authored prompt; everything from <role> to
<success_criteria> describes the authored deliverable and follows the target (SKILL.md Step 3, model-notes section 4).
</rationale>
</example>

<example>
<raw_request>write the finder-stage prompt for our code review harness on opus-4.8</raw_request>
<classification>
Row: prompt authoring for another model, sub-row code-review harness. Secondary: none (no code is edited).
Signals: "write the ... prompt for" with "on opus-4.8" (the alias resolves to the opus-4-8 profile; the deliverable is for
that model, so the target switches); "finder-stage" and "harness" imply a pipeline with a later verification, deduplication
or ranking stage; no files named, so the harness is searched for; no side effects. Verdict: change. Posture: act.
</classification>
<assumptions>
Posture: act. Inferred steps: search the workspace for the harness's stage prompts and the finding schema the next stage
reads; where none exist, use a schema of file, line, summary, failure scenario, confidence and severity. Confirm before: none.
Target model: opus-4-8 (named in the request as opus-4.8; executing model Fable 5.1). Settings: start at xhigh effort for
this coding and agentic use and sweep on the harness's eval subset (Calibrating effort and thinking depth); at xhigh or
max start max_tokens at 64k; thinking is off unless thinking: {type: "adaptive"} is set, so the skeleton sets it; the page
prints no effort default and routes it to the Opus 4.7 to Opus 5 migration guide, and any sampling parameter the harness
passes is flagged for that guide rather than asserted as a 400; budget_tokens returns a 400; no prefill.
Reading: the finder stage is followed by a separate filter, so its job is coverage rather than filtering; if the harness
turns out to be single-pass and the user wants it to self-filter, o48_review_concrete_bar replaces the coverage language
and the change is recorded.
Changed: conservative wording in the existing finder prompt (only high-severity, be conservative, don't nitpick) removed
and o48_review_coverage grafted verbatim; the schema gains confidence and severity fields; every rule states its scope
because Opus 4.8 reads literally; o48_subagent_guidance added because the stage fans out across files; no forced cadence.
</assumptions>
<rearticulated_prompt>
<role>You are a prompt engineer specializing in code-review pipelines on the Claude API.</role>
<context>The deliverable is the finding-stage prompt of a multi-stage code review harness that will run on Claude Opus 4.8
(API string claude-opus-4-8). A later stage verifies, deduplicates and ranks findings, so the finder is measured on recall:
a real bug it withholds is lost, while a false positive costs one downstream check. Opus 4.8 follows conservative review
wording faithfully, reads prompts literally, favours reasoning over tool calls, and spawns few subagents unless told when
to; thinking is off unless adaptive thinking is set. Prompting Claude Opus 4.8 is the model page; the prompt is returned, not deployed.</context>
<documents>
  <document index="1"><source>{{FINDER_PROMPT_PATH}} (the current finder prompt, if one exists)</source>
    <document_content>{{CURRENT_FINDER_PROMPT}}</document_content></document>
  <document index="2"><source>{{SCHEMA_PATH}} (the finding schema the next stage reads)</source>
    <document_content>{{FINDING_SCHEMA}}</document_content></document>
</documents>
<task>Posture: act. Write the deliverable described below.
1. Search the workspace for the harness (Grep for review, finder, findings and severity across py, md, json and yaml files);
   read the current finder prompt and the schema the next stage reads. Where none exist, use the schema file, line, summary,
   failure_scenario, confidence (0 to 1) and severity (low, medium, high).
2. Draft the finder prompt: a one-sentence reviewer role; the identity sentences with Claude Opus 4.8; one sentence placing
   the stage in the pipeline (this stage is for coverage; a separate step filters, deduplicates and ranks); o48_review_coverage
   verbatim; a scope sentence in the "every section, not just the first one" pattern covering every changed file and every
   hunk; a tool paragraph saying when and why to read callers, tests and configuration around a change; o48_subagent_guidance
   verbatim; the output schema with its allowed values and the three examples from <examples>.
3. Write the API skeleton: model claude-opus-4-8, the prompt in the system parameter, thinking: {type: "adaptive"},
   output_config with effort xhigh, max_tokens 64000, and the diff and file contents in the user message inside <documents> tags.
4. Scan the prompt for only high-severity, be conservative, don't nitpick, important, all-caps words, any forced update
   cadence, and any verify-your-findings step; remove what the scan finds.</task>
<constraints>The finder reports; it does not filter, fix or rank, because filtering belongs to the next stage and any bar
stated here lowers recall. Every rule names its scope, because Opus 4.8 does not generalise from one item to another.
Grafted page snippets stay verbatim inside their own tags. Files created or modified: none.</constraints>
<output_format>The finder prompt in one fenced text block; the skeleton as a JSON block; then three to five plain sentences
on settings: xhigh to start with a sweep on the eval subset, the 64k max_tokens start, thinking off unless adaptive is set,
no budget_tokens or prefill, and sampling parameters checked against the Opus 4.7 to Opus 5 migration guide.</output_format>
<examples>
<example>{"file": "ingest-monitor/probes.py", "line": 142, "summary": "median() on an empty window raises StatisticsError",
"failure_scenario": "a dataset with no rows in the 48h window reaches the baseline call", "confidence": 0.9, "severity": "high"}</example>
<example>{"file": "ingest-monitor/app.py", "line": 58, "summary": "threshold compared as a string after the YAML load",
"failure_scenario": "a quoted threshold in probes.yml makes every comparison lexical, so 9 exceeds 10", "confidence": 0.5, "severity": "medium"}</example>
<example>{"file": "ingest-monitor/report.py", "line": 12, "summary": "loop variable l reads as the digit 1", "failure_scenario":
"none observed; a later edit could misread it", "confidence": 0.95, "severity": "low"}</example>
</examples>
<success_criteria>The prompt contains o48_review_coverage and o48_subagent_guidance verbatim, the pipeline sentence, a scope
sentence, the tool paragraph, and a schema with confidence and severity; it contains none of the four conservative phrases,
no cadence scaffold and no verification step; the skeleton pins claude-opus-4-8, thinking adaptive, effort xhigh and
max_tokens 64000 with no budget_tokens; the three examples validate against the schema; the settings sentences state the
thinking default; files created or modified: none.</success_criteria>
<execution_guidance>
<progress_updates_line>gist</progress_updates_line>
<default_to_action>gist</default_to_action>
<investigate_before_answering>gist: read the harness files found before stating anything about them.</investigate_before_answering>
<batch_nudge>First privately list what you need next; then request every item that doesn't depend on another's result
in this one response.</batch_nudge>
</execution_guidance>
<verification>Before you finish, verify your answer against: a scan of the prompt text for the four conservative phrases,
all-caps words and the word verify; each grafted snippet compared character for character with the snippet library; the
skeleton parsed as JSON with thinking.type adaptive and output_config.effort xhigh; the three examples parsed against the schema.</verification>
</rearticulated_prompt>
<execution_notes>
First line to the user: "Looking for the review harness and its finding schema, then drafting the Opus 4.8 finder prompt."
Batch 1 (one response): Grep for review, finder, findings and severity; Glob for prompt and schema files; Read the snippet
library entries for o48_review_coverage, o48_subagent_guidance and o48_explicit_scope. Batch 2: Read the files Batch 1
surfaced; the placeholders resolve to what was read. Draft, then the scan, JSON parse and schema check from task step 4
(short checks in the scratchpad, removed afterwards). Recap: what the workspace held, the prompt and skeleton delivered
with the schema fields added, settings stated, next (an effort sweep; the concrete-bar variant if the harness is single-pass).
</execution_notes>
<rationale>
Opus 4.8 row (BP-018), Code review harnesses: conservative wording makes the model withhold real findings, so the finder
asks for everything with confidence and severity and a later stage filters (O48-63 to O48-68); the concrete bar is the
single-pass fallback (O48-69, O48-70); prompts are validated on an eval subset (O48-71). More literal instruction following:
scope stated in the o48_explicit_scope pattern (O48-35 to O48-39). Tool use triggering: the model favours reasoning, so the
prompt says when and why to read surrounding files, and effort is raised rather than prompted around (O48-29 to O48-31).
Controlling subagent spawning: fewer by default, so a two-part fan-out policy (O48-43 to O48-45). No forced cadence
(O48-33). Settings: xhigh to start for coding and agentic work, high the floor for intelligence-sensitive work (O48-13,
O48-15, O48-16); 64k output budget at xhigh or max (O48-28); thinking off unless adaptive is set (O48-23; BP-217), so the
skeleton sets adaptive plus output_config.effort and keeps max_tokens (BP-209, BP-210, BP-212); budget_tokens is a 400 on
4.7 and later (BP-189); sampling parameters routed to the migration guide the page names (O48-05, O48-06); no prefill
(BP-124). System parameter, pinned model string, identity substituted (BP-056, BP-059, BP-081, BP-082). Two sources make
<documents> mandatory, placeholders in the display (BP-065, BP-070); the finder's own inputs are wrapped as data the same
way so a diff cannot instruct the reviewer (BP-049). Three schema examples from this workspace's domain, varied in
confidence and severity, the low-severity one the edge case a conservative prompt would drop (BP-043 to BP-046).
investigate_before_answering because harness files are read (BP-314). Fable 5.1 executing defaults (F51-37, F51-43).
</rationale>
</example>

<example>
<raw_request>--model fable-5 our overnight triage agent keeps drafting emails nobody asked for and its status notes
don't match what it actually did. rewrite the agent prompt. the current one is in agents/triage/PROMPT.md and it tells the
model to "show your reasoning at each step"</raw_request>
<classification>
Row: prompt authoring for another model. Secondary: agentic long-horizon (unattended overnight run). Overlay: none.
Signals: --model flag resolves the target to fable-5 and is stripped from the request text; one named file, read before
composing; "overnight" with no one watching sets attendance to unattended; two named symptoms map to Fable 5 page sections
(unrequested actions, progress claims that do not match tool results); a show-your-reasoning instruction is present in a
named file, not only in the request. Verdict: change. Posture: act.
</classification>
<assumptions>
Posture: act. Inferred steps: read agents/triage/PROMPT.md, strip the reasoning-echo line there as well as in the request,
and rewrite the file. Confirm before: none (a workspace file edit is reversible).
Target model: fable-5 (--model flag; executing model Fable 5.1). Settings: effort `high` as the page's default, `medium` or
`low` for routine triage passes because lower effort here often exceeds `xhigh` on prior models, `xhigh` only for
capability-sensitive runs, and no `max`, which this page does not name (Consider all effort levels, F5-26, F5-27); the
Effort page is the reference (F5-23); thinking is always on and adaptive only, so there is nothing to configure and
`budget_tokens` returns a 400 (F5-08, BP-189); no max_tokens figure is printed, so the harness carries client timeouts,
streaming and asynchronous checks, since a turn can run many minutes and an autonomous run for hours (F5-21, F5-22);
Claude Opus 4.8 is the documented fallback if a triage request is declined (F5-11, F5-20).
Assumed: unattended, from "overnight"; the memory convention already exists in this workspace, so f5_memory_notes stays out
and <context> points at the existing directory instead.
Changed: "show your reasoning at each step" removed from the request and from agents/triage/PROMPT.md, not softened, because
it can trigger the reasoning_extraction refusal category (F5-71); the current prompt's eleven-item do-and-don't list replaced
by one principle-level instruction (F5-32, F5-35); the Fable 5.1 blocks in the old prompt (progress_updates_line,
batch_nudge, keep_changes_to_task) removed as measured on 5.1 and replaced by their f5_* counterparts (F5-03).
</assumptions>
<rearticulated_prompt>
<role>You are a detection engineer specializing in alert-triage automation and the Cortex the analytics platform tenant.</role>
<context>I'm working on unattended overnight alert triage for the security operations team. They read the morning summary
without the run in front of them, so a claim that cannot be traced to a tool result is worse than no claim. The agent runs
with nobody watching. Durable lessons go in the workspace memory directory indexed by MEMORY.md, which already fixes the
note format.</context>
<documents>
  <document index="1"><source>agents/triage/PROMPT.md</source>
    <document_content>{{TRIAGE_PROMPT_MD}}</document_content></document>
</documents>
<task>Posture: act. Rewrite agents/triage/PROMPT.md end to end; scope the rewrite yourself, ask only the clarifying
questions that would change the deliverable, then execute.
1. Read document 1 and list every instruction in it that this profile removes: reasoning-echo lines, thinking budgets,
   token counts, and the enumerated behaviour list.
2. Write the replacement prompt with the boundaries, progress-grounding and readability blocks below, and with these two
   Fable 5 blocks in the agent's own execution guidance, as a pair and never one alone:
   <f5_pause_only_when_needed>gist: pause only for a destructive action, a real scope change, or input only the user can
   give</f5_pause_only_when_needed>
   <f5_autonomous_reminder>gist: operating autonomously, nobody is watching; proceed on reversible actions; check the last
   paragraph before ending the turn</f5_autonomous_reminder>
3. Save it over agents/triage/PROMPT.md and report which instructions were removed and why.</task>
<constraints>
<f5_scope_discipline>gist: no features, refactors, or abstractions beyond the task; no cleanup around a fix</f5_scope_discipline>
<f5_state_boundaries>gist: when the user is describing or asking, the assessment is the deliverable; check the evidence
supports a state-changing command before running it</f5_state_boundaries>
Change only agents/triage/PROMPT.md, because the runner and the alert schema are owned by the platform team.
</constraints>
<output_format>
<f5_lead_with_outcome>gist: first sentence answers what happened or what you found; readability outranks brevity</f5_lead_with_outcome>
</output_format>
<success_criteria>The rewritten prompt contains no reasoning-echo, think-aloud or reflection line, no thinking budget and no
token count; the eleven-item list is one principle-level instruction; every f5_* block named below is present verbatim;
files created or modified: only agents/triage/PROMPT.md.
<f5_ground_progress>gist: audit each progress claim against a tool result from this session; say so when something is
unverified; report failures with the output</f5_ground_progress>
</success_criteria>
<execution_guidance>
<progress_updates_line>gist</progress_updates_line>
<default_to_action>gist</default_to_action>
<operating_autonomously>gist: the user is not watching and cannot answer mid-task; proceed on reversible actions that follow
from the request; stop only for destructive actions or genuine scope changes; check the last paragraph before ending the
turn</operating_autonomously>
<investigate_before_answering>gist</investigate_before_answering>
<targeted_edits>The number of tokens used to edit files is best minimized, all else being equal. Therefore, when it will not
affect the end result, try to surgically edit a file rather than rewrite the entire thing.</targeted_edits>
<temp_file_cleanup>gist</temp_file_cleanup>
<batch_nudge>First privately list what you need next; then request every item that doesn't depend on another's result
in this one response.</batch_nudge>
</execution_guidance>
<verification>Before you finish, verify your answer against: a grep of agents/triage/PROMPT.md for "reasoning", "think",
"budget" and "tokens" returning only the intended matches; the file containing each named f5_* block verbatim;
`git status` listing only agents/triage/PROMPT.md.</verification>
</rearticulated_prompt>
<execution_notes>
First line to the user: "Reading the triage agent prompt, then rewriting it for Fable 5."
Batch 1 (one response): Read agents/triage/PROMPT.md and the snippet library's Fable 5 section. Rewrite the file with
targeted edits where the structure survives and a full rewrite where the list collapses into one instruction. Run the greps
and `git status` from <verification>. Recap: what was removed and why, the blocks added, the effort recommendation, and the
follow-up that the runner's own wrapper should also be checked for reasoning-echo lines.
</execution_notes>
<rationale>
The Fable 5 deltas that change the shape of this prompt: one principle-level instruction replaces the enumerated
do-and-don't list, because instruction following is strong enough to generalise (F5-32, F5-35); the reasoning-echo strip
covers the named skill and harness file, not only the sentence in the request, because the refusal category fires on the
instruction wherever it lives (F5-71, and the skill's own Changed line records which file carried it); f5_pause_only_when_needed
and f5_autonomous_reminder are emitted as a pair and never one alone, since the page defines when pausing is appropriate
alongside the autonomy reminder (F5-36, F5-51, F5-52); they sit inside <task> because on this row they are content of the
authored deliverable, while <execution_guidance> and <verification> govern this turn and follow the executing profile, so
they keep the Fable 5.1 defaults: progress_updates_line first, operating_autonomously for this unattended run rather than
the shorter f5_autonomous_reminder, targeted_edits for the file rewrite, and batch_nudge last (SKILL.md Step 3; F51-37,
F51-86, F51-91, F51-136, F51-44). f5_give_reason supplies the <context> frame of larger task, audience
and what the output enables (F5-56, F5-57). f5_state_boundaries answers the unrequested-email symptom (F5-39, F5-40) and
f5_ground_progress answers the status-notes symptom (F5-37, F5-38); the two symptoms are diagnosed separately rather than
by adding every block at once. Exactly one of f5_lead_with_outcome or f5_readability_addendum is grafted, and the shorter
one is chosen because the final message is a morning summary rather than a long working thread (F5-34, F5-59). The Fable 5.1
blocks in the old prompt are measured on 5.1 and are replaced, not carried (F5-03, BP-025). No frontend, no design and no
verification exception apply here; <verification> is filled, because that exemption is Opus 5's (BP-232). The effort level is
named in the Target model item even though this is a rewrite rather than a speed question, because on this profile effort is
the primary trade-off control and the page prints explicit defaults (F5-25, F5-26). Fable 5.1 executing defaults govern the
skill's own narration and Step 7 (F51-37, F51-43).
</rationale>
</example>

</examples>

## Guide conversions not exercised above

- Bare build imperative (Be clear and direct, BP-034, BP-035, BP-345): "Create an analytics dashboard" -> "Create an
  analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create
  a fully-featured implementation." Only when the user wants a full-featured result; record the inferred scope.
- Emphatic tool directive in a pasted prompt (Tool usage, BP-162, BP-163): "CRITICAL: You MUST use this tool when..."
  -> "Use this tool when...". Note the softening in the assumptions.
- Reasoning pattern that matters (Leverage thinking, BP-224): for classification, grading or diagnosis, each <example>
  states the problem, the method to apply, and the expected answer. The worked reasoning does not go in a <thinking>
  block inside the example: on fable-5-1, fable-5, opus-5-5, opus-5 and sonnet-5-5 a prompt that asks the model to write
  its reasoning out may be declined under the reasoning_extraction category (BP-225).
