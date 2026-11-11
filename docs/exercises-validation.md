# KUL-453 Exercises validation

## Source evidence — 11 November 2026

Implementation branch `codex/kul-453` was created from freshly fetched plugin
main `c5ff7abf5819e62a3cf3d4e7805d83b43646e517` before editing. Remote main was
also fetched for both dependencies; their working-tree changes were not used
or altered.

- Connect: `0be267bd5171c268fbb987095c233eaa88d4753d` (KUL-452, PR 92).
  Contract evidence: `docs/exercises.md`, `app/mcp/tools/exercises.py`,
  `app/mcp/exercise_types.py`, `app/mcp/tool_types.py`, and
  `app/mcp/apps/exercise_widget.py`.
- API: `be0711f996e456c7614f2cd25530589359f8125c`.
  Evidence: `src/api_types/exercises.rs`, `src/libs/exercises/generation.rs`,
  `src/libs/exercises/language.rs`, and `docs/exercises/api-contract.md`.
  New generation permits 1–10 unique documents including descendant folders,
  not the issue's older 20-document/root-only contract. The internal allowance
  for older persisted contexts does not raise the new-request limit.

Package version is 0.3.0 across all three manifests. MCP endpoints, plugin
identity, and default prompts are unchanged. The package adds no local grader,
readiness formula, or recommendation policy.

## Executed checks

| Check | Result and boundary |
| --- | --- |
| Retired-tool reference guard | Passed across public package text |
| Metadata and Exercise contract validator | Passed: JSON/YAML, manifest consistency, skill links, all 18 published tool signatures, input table, enum/constraint snapshot; compared directly with fetched Connect `origin/main` |
| Plugin regression tests | 18 passed, including invalid metadata, broken nested references, obsolete generation fields, unknown tools, and upstream constraint/signature drift |
| Connect `tests/test_exercises.py` | 102 passed from a clean `git archive origin/main` export using the existing Connect Python environment; no unrelated working-tree code or `.env` copied |
| Claude `plugin validate .` | Passed; existing SVG icon produced a nonblocking `ICON_INVALID` directory warning, and CLI advised adding a marketplace install line. Neither directory publication nor marketplace setup was in scope |
| Whitespace check | `git diff --check` passed |
| Independent source review | No remaining material workflow/contract findings; corrected standalone skill export instructions and deferred criterion labels until saved results to avoid pre-attempt answer cues |

The Connect tests exercise actual FastMCP discovery/tool handling with mocked
backend responses. They cover both modes, all 18 language values, non-Latin/RTL
answers, invalid input, public response filtering, exact payload forwarding,
draft conflicts/tombstones, unavailable recovery, provenance, and skill evidence.
They do not execute the plugin prompts in a host or establish real grading,
source ownership enforcement, quota accounting, or rendering.

Reproduce package checks in a Python 3.12+ virtual environment:

```sh
python3 -m pip install PyYAML==6.0.3
python3 scripts/check_tool_references.py
python3 scripts/check_exercise_contract.py
python3 scripts/check_exercise_contract.py --connect-repo /path/to/kuliko-connect
python3 -m unittest discover -s tests -v
git diff --check
claude plugin validate .
```

The optional Connect comparison reads `origin/main`; fetch it first. The pinned
fixture is an auditable source snapshot, not a live-tool availability assertion.
CI runs the package checks without requiring a second repository checkout.

## Live availability and remaining host validation

Only the supplied isolated loopback runtime was probed. Port 8252 had an MCP
listener and returned HTTP 401 without credentials. Port 8452 had no API
listener and a direct HTTP connection failed. Private session files were not
read, credentials were not printed, and the regular Kuliko connection was not
used. The existing KUL-452 Inspector results are upstream evidence, not a new
KUL-453 test or proof of actual Claude/ChatGPT chat rendering.

No authenticated live create → independent attempt → evaluation → explicit
reference reveal → revision sequence was possible against this runtime. The
following matrix remains **unverified live** in Claude and ChatGPT, for widget
and standard-tool flows where supported. Use only isolated Free/Pro accounts
and an enabled isolated API; never substitute the regular connection.

| Scenario | Required observation |
| --- | --- |
| Apply singleton and Analyse multi-document creation | Explicit subject/selection; root plus descendant document summaries and citations; one coherent variable-part problem |
| English, French, Japanese, Arabic | Canonical languages, long/non-Latin/RTL prompt and public labels; exact answer whitespace and Unicode survive save/submission |
| Creation bounds and replay | Two objectives accepted, three rejected; empty/foreign/wrong-subject/over-limit selections and obsolete fields rejected without dropping sources; reordered/duplicate replay creates no extra charge |
| Independent attempt and feedback | Explicit submission; backend qualitative outcomes, quotes and selected next step joined by public criterion ID/label, with independent question-part associations |
| Reveal and revision | No automatic reveal or criterion labels before results; explicit hint/worked-answer provenance; later revision is practice-only; prior attempt snapshot remains immutable |
| Unavailable assessment and disabled worker | Unknown outcome; same saved attempt retried, never new submission; backend retry/503 limits preserved |
| Source and draft conflicts | Stale-source 409 retains answer and offers deliberate regeneration; draft conflicts/tombstones instead refetch/reconcile; accepted identical replay still retrieves original attempt |
| Skill targeting/evidence | Direct-subject catalog limitation explicit; missing catalogs permit untargeted practice; historical/rebuilt/unresolved identities retained, no inferred mapping or mastery |
| Daily/monthly limits | Display backend scope/reset, including signup/subscription-anniversary short-month behavior; rejected admission creates no attempt; unavailable accepted work retains charge |
| UI/tool absence | Missing widget uses standard tools; absent assessment tools use clearly unsaved coaching, with no fabricated progress, grades, or readiness updates |
| Exam and teach-back routing | Learner explains first; read-only readiness request makes no writes; saved criterion feedback and conversational suggestions remain distinct |

Capture each host/version, test-account tier (no credentials), selected IDs,
generation/attempt/result versions, tool payloads with sensitive material
redacted, and observed UI/backend results. Mark unavailable or unexecuted cases
explicitly; transport success alone cannot close a rendering row.
