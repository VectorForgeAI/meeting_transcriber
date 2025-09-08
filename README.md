<p align="center">
  <img src="docs/banner.svg" alt="Meeting Minutes Generator banner" width="720"/>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <a href="https://github.com/VectorForgeAI/meeting_transcriber/pulls"><img alt="PRs" src="https://img.shields.io/badge/PRs-welcome-blue"></a>
</p>

> 📝 Turn raw transcripts into clean, action-oriented minutes with a single import. Clear decisions. Concrete actions. Fast.

Optional demo screenshot: see `docs/quickstart.png`.

### Quick Start

- **Import the Custom GPT**
  1) Open ChatGPT → Create a GPT → Import from file
  2) Upload `MeetingMinutes_GPT.json`
  3) Upload a transcript and say “Generate minutes.” ⚡

- **Run the CLI**

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o-mini   # optional (defaults to gpt-4o-mini)
python scripts/minutes.gen.py examples/sample_transcript.txt out.md
```

### Repository Tree

```text
.
├─ README.md
├─ MeetingMinutes_GPT.json
├─ LICENSE
├─ .gitignore
├─ .gitattributes
├─ /docs
│  ├─ banner.svg
│  ├─ quickstart.png             # optional screenshot placeholder
│  └─ minutes-template.md
├─ /examples
│  └─ sample_transcript.txt
├─ /scripts
│  └─ minutes.gen.py
└─ /.github
   ├─ ISSUE_TEMPLATE/bug_report.md
   ├─ ISSUE_TEMPLATE/feature_request.md
   ├─ PULL_REQUEST_TEMPLATE.md
   └─ workflows/ci.yml
```

### Why this repo

- **Clarity**: Many transcripts are messy. This repo turns them into structured minutes with consistent sections and clear attributions.
- **Speed**: Import a ready-made Custom GPT or run a one-file CLI to get results in minutes.
- **Action focus**: Prioritizes decisions and action items so owners, deadlines, and risks are explicit.

### Features

- **Opinionated minutes format** with enforced section order ✅
- **Action Items table** with owners, deadlines, and notes ✅
- **Precision attribution** to avoid ambiguity ✅
- **Confidentiality reminders** for sensitive content ✅
- **20–50% compression target** while preserving critical details ✅

### Usage Options

#### A) Import JSON in Custom GPT

1) Download `MeetingMinutes_GPT.json`
2) In ChatGPT → Create a GPT → Import from file
3) Upload your transcript file and prompt: “Generate minutes.”

#### B) Use the CLI (scripts/minutes.gen.py) with API

```bash
export OPENAI_API_KEY=sk-...
python scripts/minutes.gen.py examples/sample_transcript.txt out.md
```

Output goes to `out.md`. Copy into your doc tool or compare with `docs/minutes-template.md`.

### Action Items table spec

| Action Item | Owner | Deadline | Details/Notes |
|---|---|---|---|
| Draft vendor RFP | Dana | Oct 1, 2025 | Include SLA + pricing tiers |

### Security & Privacy

- Treat transcripts as sensitive. Remove PII where possible.
- Do not commit real transcripts to the repository.
- The GPT prompt includes a confidentiality note and guidance for edge cases.

### Contributing

- PRs welcome! See the [PR template](.github/PULL_REQUEST_TEMPLATE.md) and open issues.

### License

MIT © VectorForgeAI

### FAQ

- **Does this require labeled speakers?** Works best with named speakers, but will handle generic diarization (Speaker 1, 2, …).
- **How compressed are the minutes?** Targets 20–50% of original tokens; key facts remain intact.
- **What if ownership is unclear?** The model asks for clarification or marks owner as TBD with context.
- **Unsupported inputs?** Long audio files must be transcribed first; this tool accepts text transcripts.
- **Can I change the section order?** The format is enforced; add info under “Notes” if needed.
- **Is browsing or code execution used?** No. Those capabilities are disabled to protect privacy and focus.

### Roadmap

- Optional redaction pass
- Speaker diarization hints
- Multi-language support

<p align="center">
  <em>Mini diagram (inline SVG): pipeline at a glance</em><br/>
  <svg width="420" height="40" xmlns="http://www.w3.org/2000/svg" aria-label="mini-pipeline">
    <rect x="0" y="0" width="420" height="40" rx="6" fill="#f6f8fa"/>
    <g font-family="Segoe UI, Roboto, Arial" font-size="12" fill="#24292e">
      <rect x="8" y="8" width="110" height="24" rx="4" fill="#e8eef3"/>
      <text x="16" y="24">Raw Transcript</text>
      <text x="130" y="24">→</text>
      <rect x="150" y="8" width="120" height="24" rx="4" fill="#e8eef3"/>
      <text x="158" y="24">Custom GPT Spec</text>
      <text x="278" y="24">→</text>
      <rect x="298" y="8" width="114" height="24" rx="4" fill="#d1f0d0"/>
      <text x="306" y="24">Minutes (Markdown)</text>
    </g>
  </svg>
</p>

---

### Footer

If this saved you time, give it a ⭐ and share it with a teammate. ✅


