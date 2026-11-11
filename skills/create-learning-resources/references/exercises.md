# Apply/Analyse Exercises

Read this workflow before creating, practising, or interpreting a saved Exercise.
Use actual discovered tool schemas with the host's namespace. API support or a
merged release does not establish that tools/workers are available on this host.
Exercises use their own tools, not `generate_learning_resources`, generic
resource saves, quiz grading, or `get_job_status`.

## Choose material, mode, and optional skills

Reuse suitable saved practice with `list_exercises`, then `get_exercise`.
Resolve the subject and document titles/IDs with `list_subjects` and
`list_documents`. For new generation, obtain the learner's explicit `subject_id`
and complete `source_ids` selection: 1–10 unique owned documents in that subject
or its descendant folders, with a backend-validated aggregate limit of 160,000
UTF-8 source bytes. A clearly stated selection in the conversation counts;
never silently select one document, omit a rejected document, or truncate text.
Show the selected-document summary. Empty, foreign, wrong-subject, and over-limit
selections need correction, not partial generation.

Use `apply` for using knowledge in a situation, and `analyse` for examining
relationships, claims, or competing explanations. Preserve the learner's mode
and language. Difficulty is `introductory`, `intermediate`, or `advanced`;
resolve missing required choices before generating. Optional `objectives`
contains at most two nonblank strings, each at most 2,000 UTF-8 bytes. Clarify or
combine objectives with the learner if more are requested; do not silently drop
them or invent an `instructions`, `count`, or singular generation `source_id`.
One request creates one coherent problem with variable related subquestions,
including six or more where useful; there is no fixed part count.

For practice from an existing backend skill, use `list_exercise_target_skills`
and match its `source_id` to the explicit selected documents before passing
optional `skill_ids`. The listing covers direct-subject catalogs only, not
folder catalogs. Paginate as needed. Missing/unready catalogs or absent targets
permit generation without optional skill targets; say that targeting is unknown.
Do not invent skill IDs or silently substitute a rebuilt catalog identity.
Requested targets are preferences. Only the published `criterion_skill_links`
show which abilities this exercise actually assesses; absent links are unknown.

All 18 canonical lowercase `language` values are supported:
`english`, `french`, `spanish`, `german`, `italian`, `portuguese`, `dutch`, `polish`,
`chinese`, `japanese`, `korean`, `arabic`, `hindi`, `russian`, `ukrainian`, `turkish`,
`indonesian`, `vietnamese`. Do not send ISO aliases. Preserve Unicode, right-to-left
text, long prompts, public labels, and citation associations without translating
or rewriting the learner's submitted answer.

## Tool inputs

IDs and versions come from returned records, never from guessed URLs. This table
lists required and optional inputs; consult discovery for current types/limits.

| Tool | Required inputs | Optional inputs |
| --- | --- | --- |
| `generate_exercise` | `subject_id`, `source_ids`, `mode`, `difficulty`, `language`, `idempotency_key` | `objectives`, `skill_ids` |
| `get_exercise_generation` | `generation_id` | — |
| `list_exercises` | — | `subject_id`, `source_id`, `limit`, `offset` |
| `get_exercise` | `exercise_id` | — |
| `open_exercise` | `exercise_id` | — |
| `list_exercise_target_skills` | `subject_id` | `limit`, `offset` |
| `get_exercise_draft` | `exercise_id` | — |
| `save_exercise_draft` | `exercise_id`, `content_version`, `expected_version`, `answer` | — |
| `delete_exercise_draft` | `exercise_id`, `expected_version` | — |
| `submit_exercise_answer` | `exercise_id`, `idempotency_key`, `content_version`, `draft_version`, `answer` | `assistance` |
| `get_exercise_history` | `exercise_id` | `limit`, `offset` |
| `get_exercise_attempt` | `attempt_id` | — |
| `get_exercise_results` | `attempt_id` | — |
| `get_exercise_skill_evidence` | `attempt_id` | — |
| `retry_exercise_assessment` | `attempt_id` | — |
| `reveal_exercise` | `exercise_id`, `idempotency_key`, `content_version`, `kind` | — |
| `report_exercise_feedback` | `attempt_id`, `idempotency_key`, `result_version`, `reason` | — |
| `archive_exercise` | `exercise_id` | — |

## Generate, attempt, assess, then reflect

1. Call `generate_exercise` within the requested saving scope. Retain a stable
   idempotency key and the full payload for identical network retries; reordered
   or duplicate source IDs are backend-canonicalized replays, not new charges.
   Poll the returned generation ID with `get_exercise_generation` every few
   seconds while `pending` or `processing`. Stop on `complete` or `unavailable`;
   report unknown states honestly. Read the returned exercise ID on completion.
   Never resubmit generation to poll or treat an interrupted response as failure.
2. Use `open_exercise` when its widget is supported. Otherwise read
   `get_exercise` and use the same standard tools in chat. Display the public
   prompt and selected sources/citations. Defer `criterion_labels` and their
   saved `question_parts` until showing saved results: even public labels can
   paraphrase marking expectations and cue an independent answer. Do not expose
   or reconstruct private grading expectations.
3. Encourage an independent answer before any hint or worked-answer reveal.
   Wait for the learner's answer. Read `get_exercise_draft` before editing; save
   exact free-form text with `save_exercise_draft` only within the requested
   scope. Preserve Unicode and whitespace, even mistakes. Use the returned
   `content_version` and draft `version` (`0` initially); subsequent saves and
   explicit deletions use the latest revision, including deletion tombstones.
   Draft saving is not submission or recorded assessment.
4. When the learner requests submission, call `submit_exercise_answer` with
   their exact answer, current `draft_version`, and declared `assistance` array.
   Do not improve, summarize, translate, or answer for them. Disclose coaching
   and other help; never pass an empty assistance list to hide known assistance.
   The backend snapshots recorded reveal IDs. Retain the accepted attempt ID,
   submission payload, and key. Poll `get_exercise_attempt` while pending or
   processing, then read saved `get_exercise_results` and, when interpreting
   skills, `get_exercise_skill_evidence`. A widget launch is not completion.
5. Explain the saved qualitative outcomes, evidence quotes, feedback, and
   selected `next_step`, using `criterion_labels` and their saved `question_parts`
   to label each criterion ID. Parts and criteria need not be one-to-one; retain
   opaque IDs for joins, not as human labels or inferred numbering. Missing
   answers affect their saved criteria, not every criterion. Render
   `demonstrated`, `partly_demonstrated`, and `not_yet_demonstrated` as
   Demonstrated, Partly demonstrated, and Not yet demonstrated (localized as
   appropriate). Preserve a null next step when all criteria are demonstrated;
   do not invent one as a backend recommendation. No numeric grade is supplied.
6. Reveal only when the learner explicitly requests a hint or worked answer:
   `reveal_exercise` takes `kind: hint` or `kind: worked_answer` and the saved
   content version. Encourage trying first, but the backend does not enforce
   submission-first. Never reveal automatically on opening, polling, or reading
   feedback. Explain the reference after the explicit reveal, then invite a
   revision. A revised answer is a new, explicit practice submission with a new
   key; an identical retry of an uncertain request retains its original key.
   Even A → B → A submissions are distinct operations, not old-key replays.

## Evidence has a scope

Use `get_exercise_history` to distinguish first submissions, revisions, and
pending/unavailable attempts. Only the first accepted submission can qualify for
independent evidence; assistance, reveals, and current skill validity further
constrain eligibility. Later submissions remain practice-only, even if better,
completed first, or the first assessment was unavailable. Recovery preserves
this ordering. Offer a fresh exercise when independent confirmation is needed.
Do not reclassify a completed attempt after a later reveal; use its saved snapshot.

Interpret a criterion outcome only for its backend-validated linked skills.
Consume each skill's `independent_evidence_eligible`, not just the attempt's
`readiness_eligible`. Preserve `link_state: historical`, pinned skill identities,
source identities/content versions, result versions, and
`unresolved_criterion_ids`. Incomplete mappings are unresolved, not partial credit
to whichever documents have links. Never remap old evidence to rebuilt catalogs
or spread results over the requested `skill_ids`. Deduplicate evidence by
`(attempt_id, result_version, skill_id)` and count distinct attempts across
selected documents, not one attempt per document.

Accept defensible analytical alternatives grounded in the material; agreement
with a model or reference wording is not proof of correctness. If saved feedback
appears wrong, distinguish your conversational critique from the immutable
backend result and offer `report_exercise_feedback` for the exact result version
at the learner's request. Never replace the saved outcome with a local grade.
One demonstrated criterion is not general analytical ability or mastery.

Keep conversational coaching, passive explanation viewing, and recorded
submitted assessment distinct. A private package containing an explanation is
not a recorded viewing event. Neither creating an exercise nor revealing an
answer proves learning. Report service readiness only when actually returned;
do not derive numeric readiness changes, weighting, mastery, or an automated
recommendation engine from exercise evidence. Follow the saved next step while
keeping any additional conversational suggestion clearly separate.

## Recovery and ownership

- **Unavailable assessment:** this is unknown, not an incorrect answer. Retry
  the SAME saved attempt with `retry_exercise_assessment(attempt_id)`; there is
  no new answer/body. Respect backend retry limits and disabled-worker 503;
  retain the answer, quota receipt, eligibility, and provenance. Do not submit
  a new attempt to recover or promise successful grading.
- **Unavailable generation:** keep its generation ID and explain the failure.
  Deliberate regeneration is a new request/key and may consume allowance.
- **Stale-source 409:** preserve the learner's answer. Edited/deleted sources,
  ownership changes, or moves outside the permitted subject tree require
  deliberate regeneration with a new generation key and explicit selection.
  Moves within that tree remain supported. An accepted identical submission
  replay can still return the original attempt after source changes; it is not
  a new assessment. There is no read-time `can_assess` flag to invent.
- **Draft/content-version conflict:** refetch and reconcile deliberately with
  the learner; do not overwrite a newer draft/tombstone or discard local text.
  Distinguish this from stale-source rejection before choosing recovery.
- **Quota/ownership failures:** use backend 429 scope and reset timestamp;
  daily and subscription/signup-anniversary monthly allowances differ. Do not
  compute calendar-month resets, promise refunds, or treat 404 as an empty
  library. Pre-admission rejection creates no attempt; accepted unavailable
  work still counts. Identical accepted replay adds no charge.
- **Ownership:** retain `subject_id` and every `source_ids` member. Listing's
  singular `source_id` is only a membership filter. Preserve each source's
  citations and actual folder identity; never invent a root-subject link.
  Archive only on request with `archive_exercise`, once across all document
  views; immutable attempt history remains after archival/source changes.
- **Tool or UI unavailable:** if only the widget is missing, use the standard
  tools above. If creation/submission/evaluation tools are absent, offer
  explicitly unsaved conversational practice from available material. Retain
  any known saved attempt for later recovery. Do not invent a saved exercise,
  evaluation, exposure event, progress, grade, or readiness update. Never send
  Exercises to quiz tools as a substitute.
