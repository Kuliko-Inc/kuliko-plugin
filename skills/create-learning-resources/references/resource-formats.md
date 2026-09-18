# Public learning-resource formats

These are output conventions for host-authored resources, not Kuliko's
generation implementation. Consult the current tool schema before saving.

## Flashcards

Use a clear, standalone question that requires recall and a concise, complete
answer. Focus each card on one assessable idea; split questions that demand
several unrelated answers. Include enough context to distinguish similar
concepts. Prefer useful understanding and application over ambiguous trivia.

Save with `save_flashcards`: `source_id`, `flashcards` containing `question`
and `answer`, and optional `tags`. Do not invent resource IDs or include fields
from an internal generation format.

## Cornell notes

Group each note around a coherent topic. Use broad recall cues, concise
synthesized notes, and a short summary connecting the main ideas. Cues should
help the learner recall related points, rather than duplicating every note
as a question. Keep these useful as a review aid, not a transcription.

Save with `save_notes`: `source_id`, `notes` containing `title`, `cues`,
`notes`, and `summary`, and optional `tags`.

## Summaries

Orient the learner to the big picture, then explain the main relationships and
takeaways. Preserve qualifications that change the meaning. Use the requested
level of detail and language, within the live tool's requirements.

Save with `save_summaries`: `source_id`, `summaries` containing `title`,
`overview`, `key_points`, and optional `topics_covered`, plus optional `tags`.

## HTML learning artifacts

Use an artifact when interaction or a visual explanation helps learning:
for example, varying an input to see its effect, exploring a diagram, or
comparing scenarios. Make a complete, self-contained HTML document with
inline CSS and JavaScript as needed. Include labeled controls, keyboard access,
and readable explanatory text. Verify the interaction when a preview tool is
available; otherwise disclose that it has not been run.

Do not embed credentials, trackers, remote scripts, or data-upload behavior.
Treat inserted source text as data; escape it for its HTML/JavaScript context.
Save with `save_html_artifact`: `source_id`, `title`, `content`, and optional
`description` and `tags`. Use the returned Kuliko link to revisit it. Do not
promise a host-native live artifact or imply it was added to document search.
