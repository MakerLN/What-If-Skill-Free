# Licences and monetization checklist

Written from general knowledge, not from legal review. Every line marked
VERIFY should be checked on the project's own page before the first
monetized upload. Licences and platform policies change.

## Components

| Piece | What it is | Licence (VERIFY) | Notes |
|---|---|---|---|
| what-if-animation (original skill) | pipeline, Remotion studio, rig | MIT | Keep the LICENSE file if you redistribute. |
| Kokoro (`kokoro` package, Kokoro-82M model) | local text-to-speech | Apache 2.0 | Read the model card for the voice list and any usage notes. |
| faster-whisper / Whisper | word timings | MIT | Only used to measure timings, no audio of it is published. |
| espeak-ng | phonemizer Kokoro may call | GPL-3.0 | Used as an external tool; matters if you redistribute it, not for the audio you make. |
| Remotion | video renderer | Own source-available licence | Free for individuals and very small companies, a paid company licence beyond that. VERIFY this one first: it applies to the renderer, not to the original skill. |
| Fonts (Bricolage Grotesque, Fragment Mono, Kalam) | titles and text | SIL OFL | Fine for commercial use. |
| `sfx_free.py` sounds | synthesized by code | Yours | No third-party licence. |
| `studio/library/sfx/` clips from the original repo | ElevenLabs-generated starter clips | Unclear | The original README says they came from a paid plan. Don't assume they are cleared for your channel. |

## If you add CC0 sounds or music

- Freesound: filter by licence "Creative Commons 0".
- Kenney.nl audio packs are published as CC0.
- Keep a line per file in `out/<slug>/CREDITS.md`: name, source URL, licence.
- Avoid anything marked CC-BY unless you are ready to credit it in the video
  description, and avoid CC-NC entirely for a monetized channel.

## Platform policy reminders (VERIFY on the platform's current page)

- Templated, near-identical videos posted at volume can be treated as
  repetitive or mass-produced content and lose monetization. One episode a
  day in the same structure is the risky pattern. Vary the topic, the angle,
  the voice and the structure, and add real original commentary or research.
- The original skill requires every script fact to be checked and sourced.
  Keep that; it is also what separates these episodes from low-effort content.
- Read the platform's current rules on disclosing synthetic or AI-generated
  content before uploading.
