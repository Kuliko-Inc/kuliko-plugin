---
name: kuliko-setup
description: Set up Kuliko study workflows after installation or when the user asks how to begin studying with Kuliko. Open the library when supported and explain existing material, file upload, or topic-based study guide creation.
---

# Start studying with Kuliko

Check the available Kuliko tools and connection. If authentication is missing,
use the host's normal connection flow. Do not claim access to a library that
could not be read.

When `open_kuliko_library` is available, open it once and use its initial result.
Explain that the Library browses material and the Study Session panel keeps
practice beside the conversation, only on hosts that expose those surfaces.
Otherwise use `list_subjects` and `list_documents` to find the learner's material.
Do not tell Claude users to find ChatGPT sidebar or settings controls.

Offer existing material, a local file upload, or a study guide on a topic.
Reuse the learner's supplied subject/topic and ask only for missing information.
Opening the plugin is not permission to create material or start practice.
Use `upload_document` for files and the currently available study-guide tools
for topics. Explain native file import only when the host supports it.

For an explicit request to study, reuse suitable flashcards or a quiz. Explain
that ratings save with Submit and quiz answers save with Save & exit or Submit
quiz. Keep saved progress in Kuliko. Do not fabricate scores or assessment
history. Native settings edit the same account preferences used by Kuliko.

When supported, selected material can provide context to ChatGPT; attaching a
passage does not send a prompt. Explain/Teach it back drafts require the user
to send them. Respect removed context and read-only requests.
