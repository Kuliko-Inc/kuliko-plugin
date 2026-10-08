# Kuliko

Study with your course material and keep your learning resources in Kuliko.
This plugin brings four study skills, a setup skill and Kuliko's remote MCP connection to
compatible Claude, ChatGPT, and Codex hosts.

**Development preview:** package structure has been validated. End-to-end host
installation, authentication, and study workflows are still being verified.
Directory availability depends on submission and review.

## Skills

| Skill | Try asking |
| --- | --- |
| `study-from-course-material` | Help me understand my lecture notes and improve my study resources. |
| `teach-it-back` | Let me explain this concept; challenge gaps in my understanding. |
| `create-learning-resources` | Make flashcards from my notes, or save these finished Cornell notes. |
| `prepare-for-an-exam` | My biology exam is Friday. What should I practice based on my results? |

Study sessions use the readiness and practice evidence returned by Kuliko,
plus your answers, to choose useful activities. They reuse existing resources,
create missing ones, and improve content within your requested scope. Other
available connectors can supply relevant course material, supporting explanations,
or scheduling context; Kuliko remains the home for your learning resources.

## Try it in Claude Code

Clone this repository, open its directory, and run:

```sh
claude plugin validate .
claude --plugin-dir .
```

Authenticate the Kuliko MCP connection when prompted. Ask a natural study
question or invoke `/kuliko:teach-it-back`.

For a personal Claude skill upload, ZIP one folder from `skills/`, preserving
its folder name, `SKILL.md`, and referenced supporting files. Follow
[Claude's custom skill upload instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
Check the current upload metadata limits; a standalone upload may require a
shorter description than the plugin skill. Connect Kuliko separately when
using a standalone skill.

## Try it in ChatGPT or Codex

Follow the supported local-plugin workflow in
[OpenAI's packaging guide](https://developers.openai.com/plugins/build/plugins).
The same `skills/` files are shared across platforms. Local plugin availability
varies by host and workspace; a local Codex check does not verify ChatGPT chat.

For a ChatGPT developer-mode MCP connection, use the technical ID returned by
registration in your local configuration. Account-specific connection mappings
and credentials do not belong in this repository.

## Connection and capabilities

The public MCP endpoint is `https://mcp.kuliko.ai/mcp`. Sign in through your
host's connection flow. Tool-backed workflows require a connected Kuliko account
and access to the relevant tools. Interactive widgets require host UI support.
Without a connection, skills can work with material supplied in the conversation
but cannot retrieve or save your Kuliko resources.

The skills honor requests to keep a session in chat or avoid saved changes.
Using a study skill does not by itself authorize sharing your material or
creating calendar events.

## Package layout

- `skills/`: shared workflows and supporting resource-format guidance.
- `plugin.json` and `mcp.json`: portable plugin identity and MCP configuration.
- `.claude-plugin/plugin.json` and `.mcp.json`: Claude compatibility configuration.
- `.codex-plugin/plugin.json`: OpenAI compatibility metadata.
- `assets/icon.svg`: Kuliko icon used by the Claude plugin listing.
- `skills/*/agents/openai.yaml`: OpenAI skill metadata and MCP dependencies.

Keep plugin identities, versions, and endpoint declarations consistent when
editing the platform manifests. Public files describe learning workflows and
tool usage. Resource generation and readiness calculation run in Kuliko's service.

See [Kuliko](https://kuliko.ai) for the product and
[repository issues](https://github.com/Kuliko-Inc/kuliko-plugin/issues) for plugin feedback.
See Kuliko's [privacy policy](https://kuliko.ai/privacy-policy) for information
about how the hosted service handles your data.

## License

The files in this repository are licensed under the [MIT License](LICENSE).
Use of Kuliko's hosted service is governed by its separate terms and account
requirements.

## ChatGPT study hub (KUL-279)

Connect servers with `MCP_OPENAI_EXTENSIONS_ENABLED=true` add Kuliko Library,
a conversation Study Session, entity deep links, mentions, shared study context,
structured preferences, native pickers, and supported-file preview/import.
These are capability-dependent OpenAI extensions; the standard tools and
Claude widgets continue to work without them. The server flag defaults off
until host validation is complete. Updating this package alone does not enable
extensions on the hosted server.

The OpenAI setup entry points to `skills/kuliko-setup/SKILL.md`. Shared study
skills remain usable in Claude. A local desktop connector loads MCP tools;
loading the skills also requires the host's plugin/skill installation workflow.

The released browser SDK only supports sending messages, so Explain/Teach it
back prepares an editable, copyable draft instead of sending without consent.
Saved-content editors and DOCX/TIFF native previews remain follow-up work.
See Connect's `docs/openai-extensions.md` for local connections and host checks.
