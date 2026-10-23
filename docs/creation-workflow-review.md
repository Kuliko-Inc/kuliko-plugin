# Saved guide and resources: web/mobile review

This is the plugin-side scenario for [KUL-411](https://linear.app/kuliko/issue/KUL-411).
It is a procedure and evidence template, **not a completed client test**.
Run it separately in ChatGPT web and the ChatGPT mobile app. A Codex tool call,
server test, or static package check cannot substitute for either client run.

## Package audit

The four study skills already select `generate_study_guide` for topic-based
creation, with subject resolution, explicit resource selection, and job polling.
The KUL-411 audit found an outdated optional widget name in each skill and
aligned it to `open_study_guide_generator`, as exposed by the connector schema
and current Connect source. Opening this widget is not a generation submission.
The two text-creation tools retired under KUL-295 remain retired.

The audit covers the portable and compatibility manifests, both MCP configs,
all skill instructions, OpenAI metadata, resource-format references, README
examples, and assets. The regression check also covers `examples/` and `docs/`.
It rejects known retired creation names; it does not prove every name or argument
matches a deployed schema. Account mappings, submission metadata, server
annotations, and deployed-tool verification belong to the Connect workstream.

## Prepare each client run

Use only a dedicated test account whose identity has been verified before any
test tool call. Never use the owner's real account for testing. An existing
authenticated connection is not evidence that it is a test account. If a verified
test account is unavailable, stop the client scenario and use local fixtures;
leave client evidence unverified. Do not modify or delete real-account content
as test cleanup.

Record the plugin commit (including local diff or archive checksum), manifest
version, installed app/submission version, endpoint, and independently verified
Connect/API build identifiers. Mark unavailable identifiers as unknown rather
than treating the manifest version as the deployed server build.

Record the test time/timezone, web browser/version or mobile app/version and OS,
and a non-sensitive test-account label. Authenticate that client's Kuliko
connection, refresh tool discovery, and retain its tool names and input schemas.
Confirm that the direct generator and the read tools below are accessible there.
Missing discovery or access is a blocked/failed run, not permission to invent an
alias. Use the live schema if it differs from these example arguments and record
the discrepancy.

Choose a unique run label such as `KUL-411-web-<timestamp>` or
`KUL-411-mobile-<timestamp>`. Each run creates saved content and consumes the
account's generation allowance. Do not silently reuse an earlier run's results.

## Exact learner prompt

Replace `<run label>` with the chosen unique label:

> In Kuliko, use or create a subject named "<run label> Biology". Generate and
> save an English introductory study guide on photosynthesis, focusing on the
> light-dependent reactions and the Calvin cycle. Also generate flashcards and
> summaries from that guide. Wait for processing to finish, then show me the saved
> guide and read back at least one flashcard and one summary to verify they saved.

## Expected tool sequence and assertions

1. Call `list_subjects`. Use the exact matching subject ID, or call
   `create_subject` with the requested name and retain its returned ID. If the
   lookup fails, record that failure instead of assuming no subject exists.
2. Call `generate_study_guide` once with the returned `subject_id`,
   `topic: "Photosynthesis: light-dependent reactions and the Calvin cycle"`,
   `guidance: "Introductory biology"`, `lang: "english"`, and
   `generate_resources: ["flashcards", "summaries"]`.
   These resource types are explicitly requested in the prompt. Do not substitute
   a chat draft, an upload, or a widget launch for the direct submission.
3. Preserve the returned `job_id`; poll `get_job_status` with that ID. Honor
   `poll_after_seconds` when provided; otherwise wait a few seconds between reads.
   Continue for `queued`, `running`, or `retrying`. Stop on `completed`, `failed`,
   or another terminal/unknown status. On failure or an uncertain response,
   preserve evidence and inspect existing state; do not submit another generator
   call automatically. Capture any returned dependent job handles and verify
   those too before declaring resource completion.
4. Resolve the saved `source_id` from the result or `list_documents` scoped to
   the run's subject. If multiple sources match, disambiguate against the job
   result before continuing. Read `get_document` and `get_document_text` for that
   exact source. Verify the subject association, nonempty guide content about
   the requested topic, and preserved citation links and Sources. Record the
   returned title, ID, and link; a job status or consume link alone is insufficient.
5. Call `list_learning_resources` twice for that exact `source_id`: once with
   `resource_type: "flashcards"` and once with `resource_type: "summaries"`.
   Omit search and due-only filters. Require nonempty saved results of both types
   linked to this source. Record returned IDs/counts and read an actual card's
   question/answer and a summary's content. Follow pagination if the live schema
   exposes it. Empty results fail the resource assertion even if the guide exists;
   do not mask the failure by separately generating replacements.
6. In a fresh conversation on the same client/account, read the same source and
   both resource types again without a creation call. Verify the same saved IDs
   remain readable. Open the returned guide link in that client and record whether
   the guide renders. Preserve screenshots or a recording and the tool transcript.

For a separate optional widget check, ask to configure the guide in a form and
verify `open_study_guide_generator` is selected when available. Do not count
opening a form as proof of persistence or as completion of the direct scenario.

## Evidence record (fill only after execution)

| Evidence | ChatGPT web | ChatGPT mobile |
| --- | --- | --- |
| Execution status | Not run | Not run |
| Time, client version, OS, account label | — | — |
| Plugin commit/diff or package checksum; manifest version | — | — |
| Installed app/submission version; Connect/API builds; endpoint | — | — |
| Discovered tools/schema capture | — | — |
| Subject ID; exact generation arguments; job IDs and terminal states | — | — |
| Source ID/title/link; guide body and citation verification | — | — |
| Flashcard IDs/count and sample read-back | — | — |
| Summary IDs/count and sample read-back | — | — |
| Fresh-conversation reads and guide rendering | — | — |
| Transcript/screenshot/recording links; errors or limitations | — | — |
| Verdict against all assertions | Unverified | Unverified |

Link completed evidence to KUL-411 through the authorized review workflow.
This checklist does not authorize resubmission or deployment. Server annotation
rationale and scanner/authentication case 16881773 are outside this plugin change.
