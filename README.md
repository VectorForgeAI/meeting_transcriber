Meeting Transcriber → Minutes Generator

<p align="center">
  <img src="docs/banner.svg" alt="Meeting Minutes Generator banner" width="720"/>
</p>
<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <a href="https://github.com/VectorForgeAI/meeting_transcriber/pulls"><img alt="PRs" src="https://img.shields.io/badge/PRs-welcome-blue"></a>
</p>

📝 Purpose: Turn a voice or video recording into a clean text transcript, then into action-oriented meeting minutes you can paste or share.

### What you’ll build (at a glance)

Pipeline:
🎙️ Audio/Video (Zoom, Teams, MP4, M4A, WAV) → 🔧 Whisper (local/offline) + FFmpeg → 📄 Transcript (.txt) → 🤖 Custom GPT or CLI → 🗂️ Minutes (Markdown)

You control the data (local transcription possible).

You choose the path to minutes:

- Custom GPT import (no coding).
- CLI script using an API key (automation-friendly).

Optional demo screenshot: see `docs/quickstart.png`.

### Quick Start

#### Option A — Fastest: Import the Custom GPT

1) Open ChatGPT → Create a GPT → Import from file
2) Upload `MeetingMinutes_GPT.json`
3) Upload your transcript and say: “Generate minutes.” ⚡

#### Option B — Scripted: Use the CLI to make minutes

```bash
# Requires an OpenAI-compatible API key in your environment
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o-mini   # optional; defaults to gpt-4o-mini
python scripts/minutes.gen.py examples/sample_transcript.txt out.md
```

Output goes to `out.md`. Compare against `docs/minutes-template.md`.

### Core Use Case (What you’re actually doing)

1) Transcribe your meeting recording to text
2) Feed that text into the minutes generator (Custom GPT or CLI)

This repo ships both pieces you need: a clean Whisper workflow for the transcript and a reliable minutes generator that enforces a consistent, action-focused format.

### Dependencies (Transcription)

You need these to convert audio/video → text:

- FFmpeg (required by Whisper CLI)
- Python 3.10+
- Whisper (open-source)

Install FFmpeg

Windows (PowerShell):

```powershell
winget install Gyan.FFmpeg   # or: choco install ffmpeg
# Verify:
ffmpeg -version
where ffmpeg
```

macOS (Homebrew):

```bash
brew install ffmpeg
# Verify:
ffmpeg -version
which ffmpeg
```

Ubuntu/Debian:

```bash
sudo apt update && sudo apt install -y ffmpeg
ffmpeg -version
which ffmpeg
```

Install Whisper (CPU by default)

```bash
# (Optional but recommended) create a virtual env first
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -U openai-whisper
# For NVIDIA GPU acceleration (optional), install torch per PyTorch instructions, then use Whisper.
```

On Windows with AMD GPUs, run on CPU unless you already have a working ROCm stack. CPU with the small model is usually a good balance of speed and quality.

### Transcribe: Examples

Single file → transcript (.txt)

```bash
python -m whisper "path/to/Meeting.mp4" \
  --model small \
  --task transcribe \
  --language en \
  --output_format txt \
  --output_dir ./transcripts \
  --device cpu \
  --verbose False
```

Batch directory (bash):

```bash
mkdir -p transcripts
for f in recordings/*.{mp4,m4a,wav,mp3}; do
  [ -f "$f" ] || continue
  python -m whisper "$f" --model small --language en --output_format txt --output_dir ./transcripts --device cpu --verbose False
done
```

Notes

- Choose model: tiny | base | small | medium | large. Bigger = better quality, slower.
- Outputs land in `./transcripts` as `filename.txt`.
- If you see an empty or missing text file, FFmpeg usually isn’t on your PATH (fix with the install steps above).

### Generate Minutes (Two Ways)

1) Custom GPT (No code)

- Import `MeetingMinutes_GPT.json` into ChatGPT (Create → Import).
- Upload the transcript `.txt`.
- Prompt: “Generate minutes.”
- The GPT enforces the format: Meeting Details → Agenda Overview → Discussion Summary → Key Decisions → Action Items (table) → Open Items & Risks → Next Steps & Adjournment → Notes (if needed)

2) CLI (Scripted)

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o-mini
python scripts/minutes.gen.py transcripts/Meeting.txt out.md
```

The script uses the same system prompt as the Custom GPT.

Temperature set to 0.2 for consistent, concise outputs.

### Action Items Table (Spec)

| Action Item | Owner | Deadline | Details/Notes |
|---|---|---|---|
| Draft vendor RFP | Dana | Oct 1, 2025 | Include SLA + pricing tiers |

### Getting the Latest Version

Fresh clone

```bash
git clone https://github.com/VectorForgeAI/meeting_transcriber.git
cd meeting_transcriber
```

Update an existing clone

```bash
git pull origin main
```

Pin to a known version (recommended for teams)

```bash
git checkout <commit-sha-or-tag>
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

- Clarity: Transcripts are messy. We deliver structured minutes with consistent sections and crisp attributions.
- Speed: Import a Custom GPT or run a one-file CLI. Produce minutes in minutes.
- Action focus: The format elevates decisions, owners, deadlines, and risks—no fluff.

### Security & Privacy

- Treat recordings and transcripts as sensitive.
- Avoid committing real transcripts to the repo.
- The Custom GPT disables browsing, image gen, and code execution to reduce data exposure.
- If using the CLI, protect your API key (use environment variables or a secrets manager).

### Troubleshooting

- FFmpeg not found: Install using the steps above. Confirm with `ffmpeg -version`. On Windows, ensure `where ffmpeg` returns a path.
- Blank or missing .txt: FFmpeg isn’t installed or accessible; re-install and re-run.
- Slow transcription: Use a smaller Whisper model (small), or move to a machine with a GPU (NVIDIA + PyTorch).
- Garbage output / wrong language: Pass `--language en` (or the correct ISO code) to force language.
- Long files fail: Ensure enough disk space and try smaller models; split extremely long recordings if needed.

### Contributing

- PRs welcome!
- Use the PR template.
- Keep README practical and user-first.
- Add screenshots only if they help the first-run experience.

### FAQ

- Do I need labeled speakers?\
  No. It works with generic diarization (Speaker 1/2/3). Named speakers improve attributions.
- Can I skip local transcription?\
  Yes—use any service to create a .txt transcript, then run the minutes generator.
- Will it change the section order?\
  No. The format is enforced. Add extras under Notes.
- Is internet required?\
  Transcription with Whisper can run offline. The CLI minutes script uses an API key (internet required). The Custom GPT runs in ChatGPT.
- How compressed are the minutes?\
  We target 20–50% of the transcript while retaining key facts, decisions, and actions.

### License

MIT © VectorForgeAI

If this saved you time, give it a ⭐ and share it with a teammate. ✅

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


