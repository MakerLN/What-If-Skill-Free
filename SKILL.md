---
name: what-if-animation-free
description: Creates short What If animated episodes in flat 2D vector style using SVG and Remotion, with local Kokoro TTS, Whisper word timings, and procedural or CC0 sound effects instead of paid APIs. Use when the user requests a What If video, an animated hypothetical story, a short 2D explainer, or an episode with audience-choice endings (A/B/C or more).
---

# What If episode — no paid API keys

This skill adapts the open-source `what-if-animation` project by kelano86:
https://github.com/kelano86/what-if-animation

The original project supplies the Remotion studio, scene/character system, shot-planning workflow, storyboard process, and mastering scripts. This skill replaces the ElevenLabs voice and sound-effect steps with local/free alternatives. It also defines a flat 2D visual direction and an optional audience-choice ending.

Do not recreate the original project's files from memory. Inspect the installed project and its references, then adapt the existing implementation.

## Core output

Create a short vertical animated episode, normally 15–25 seconds, based on one What If premise. The default output is a finished MP4 plus the script, voice audio, word timings, storyboard, credits, and intermediate assets in `out/<slug>/`.

The duration may exceed 25 seconds when the narration or a requested three-or-more-option ending needs more time. Never speed up speech excessively or make the choices unreadable just to force the episode into a fixed duration.

## Visual direction

Use a simple, polished **flat 2D vector/cartoon style** suitable for vertical social videos.

- Characters are illustrated 2D people or creatures built from clean SVG shapes: head, torso, arms, legs, hands, clothing, and simple facial features.
- Do not reduce every character to a bare stick figure unless the user explicitly requests stick figures.
- Use simple, readable environments with a small number of recognizable props.
- Prefer a mostly frontal, flat 2D composition. Do not create 3D scenes, realistic perspective sets, or dramatic perspective camera moves unless explicitly requested.
- Simulate camera movement in 2D with pan, scale, crop, and position changes.
- Use restrained shadows, highlights, gradients, particles, impact lines, motion trails, and other lightweight effects to add polish without clutter.
- Preserve character proportions, clothing, colors, and facial design between shots and episodes. Use reusable SVG components or a consistent character rig rather than redrawing the character differently in every scene.
- Compose for 9:16 vertical video. Keep important characters, captions, and choice cards inside mobile-safe areas.
- Keep backgrounds and props visually subordinate to the main action.
- Use original characters and compositions. Do not copy the identifiable characters, artwork, or branding of existing channels.

If the installed original studio is built around a different visual style, inspect its components and adapt the scene/character renderer to this flat 2D direction. Do not blindly preserve instructions that require realistic perspective or a dusk-lit 3D-looking set.

## Step 0: one-time setup

1. Locate the original `what-if-animation` project. Find its `SKILL.md`, `references/`, `scripts/`, and `studio/` directories. Check the current Antigravity skill location and the workspace before assuming a path.
2. If the original project is missing, tell the user that the base project must be installed and stop. Do not recreate its files from memory.
3. Read the original `SKILL.md` and all relevant files in `references/` before changing or running the pipeline.
4. Make sure the `studio/` project has been copied into the working folder and that `npm install` has completed there, following the original README.
5. Run `python scripts/voice_free.py --check` from this skill's folder. It reports which free voice and audio tools are installed and which are missing.
6. If dependencies are missing, install them using the included setup files where available. On Windows, use `install_windows.bat` if present. On macOS or Linux, use the appropriate package manager for system dependencies. Run `--check` again and report any remaining blocker clearly.
7. Do not ask the user to manually perform setup steps that the agent can safely execute in the current workspace. Before large downloads or system-wide changes, explain what will be installed and request permission when required by the environment.

## Step 1: create the episode plan

Follow the original project's planning process and reference material. Do not skip the research, script, shot list, storyboard, or self-check stages.

For each episode:

1. Turn the user's premise into one clear hypothetical situation.
2. Check factual claims against reliable sources. Keep a source list in the episode metadata or research notes. Clearly distinguish real facts from speculative consequences.
3. Write an original Brazilian Portuguese script. Use a strong opening that immediately establishes the unusual situation, then develop consequences in a clear cause-and-effect sequence.
4. Follow the original project's seven-beat guidance where it fits the premise. Do not force beats that make the story confusing or too long.
5. Make the ending lead naturally into the audience-choice question when choice mode is enabled.
6. Build a shot list aligned to the spoken words and intended pacing.
7. Render a storyboard with one still per shot and inspect it before full animation.
8. Check readability, character continuity, composition, scene logic, and visual variety. Fix storyboard problems before rendering the episode.

Show the storyboard to the user before full animation when the workflow or user request allows for review. If the user explicitly asks for a fully automatic run, inspect it internally and proceed, reporting major assumptions afterward.

## Step 2: generate voice and word timings locally

Do not call ElevenLabs or any paid voice API. Use `scripts/voice_free.py`:

```bash
python scripts/voice_free.py --text-file out/<slug>/script.txt \
  --out out/<slug>/voice.wav --timings out/<slug>/voice.words.json \
  --lang p --voice pf_dora --speed 1.05
```

The script should:

1. Generate narration with Kokoro.
2. Trim excessive pauses while preserving natural delivery.
3. Run Whisper on the final trimmed audio to obtain word-level start/end times.

The generic timing format is:

```json
{
  "text": "spoken text",
  "audio": "voice.wav",
  "duration": 12.34,
  "words": [
    { "word": "Example", "start": 0.0, "end": 0.42 }
  ]
}
```

Before generating the shot list, inspect the original project's voice/timing scripts and identify the exact JSON schema expected by the planner. If it differs, modify `write_timings()` in `voice_free.py` to produce the expected schema. Prefer adapting the free script rather than changing working original scripts unnecessarily.

For Brazilian Portuguese:

- Use `--lang p`.
- Default to `pf_dora`; other available male voices include `pm_alex` and `pm_santa`.
- Generate a short voice test when the user has not chosen a voice. Let the user choose before producing a full episode when practical.
- Write numbers and units as spoken words in narration when that improves pronunciation.
- Avoid unnecessary English terms and acronyms in narration. Spell out unfamiliar abbreviations phonetically only in the narration text; preserve correct spelling in on-screen text.
- Listen to proper names and technical terms in the generated audio. Fix mispronunciations before building final timings.

## Step 3: generate sound effects and mix audio locally

Do not call the original ElevenLabs sound-effect script. Do not reuse `studio/library/sfx/` assets from the original project unless their licence and permitted usage are explicitly established.

Use `scripts/sfx_free.py` to generate procedural effects:

```bash
python scripts/sfx_free.py --list
python scripts/sfx_free.py whoosh studio/library/sfx_free/whoosh.wav --dur 0.5
python scripts/sfx_free.py --all studio/library/sfx_free/
```

Generate the procedural sound library once, then reuse it. Match effects to actions in the shot list:

- `whoosh` for movement or transitions;
- `pop` for objects or labels appearing;
- `thud` for impacts;
- `rewind` for reverse-time moments;
- `ding` for a reveal;
- `riser` before a major turn;
- `glitch` for interruptions or failures;
- `pad` for a simple ambient bed.

A CC0 music track may be used when a richer music bed is needed. Record its source and licence in `CREDITS.md`. Do not assume that an asset is CC0 merely because it is downloadable for free.

Align effects to the action and the attack of each sound. Keep sound effects below the narration, avoid clipping, and mix the final episode to approximately -14 LUFS using the original `mixcheck` and `master` scripts when compatible.

## Step 4: audience-choice ending

Use an audience-choice ending by default unless the user asks for a different ending or the premise does not support a meaningful choice.

### Number of options

- Default to exactly two options: A and B.
- If the user requests three options, use A, B, and C.
- If the user requests more than three, support A, B, C, D, and so on, provided every option remains readable on a phone screen.
- Do not add extra options just to fill space.

### Choice writing

1. End the story at a genuine decision point for the protagonist.
2. Ask one short, direct question about what the protagonist should do next.
3. Write each answer as a distinct action, not merely a different description of the same action.
4. Keep each option concise enough to read quickly.
5. Make the consequences of the options meaningfully different, so the audience has a reason to choose.
6. Do not reveal which option is correct or imply that one option is the official choice unless the story requires it.
7. Do not invent audience voting results in later episodes. Ask the user for the winning option if it has not been provided.

### Visual design of the options

- Display the question above the options.
- Give every option its own solid background color. Colors must be visibly different from one another within the same ending.
- Suggested sequence: A = blue, B = red/orange, C = green, D = purple. Adjust for contrast and the episode's palette when necessary.
- Show the option letter prominently, followed by the action text.
- Use large, high-contrast, mobile-readable typography.
- Arrange options vertically in the 9:16 frame unless the number of options makes another layout more readable.
- Keep the protagonist and important scene elements from being hidden behind the option cards.
- Animate the cards entering one at a time, synchronized with the narration, using restrained motion such as a slide, pop, or scale-in.
- Keep the final choice screen visible long enough for viewers to read every option. Calculate this from the actual narration timing and reading time; do not cut off the last option.
- The options are visual cards, not interactive buttons. The viewer votes by commenting the corresponding letter.

### Example ending

Question: "O que Robson deve fazer?"

- A) Robson deve entrar na casa e procurar o irmão.
- B) Robson deve fugir e chamar ajuda.

For a three-option request, add a third genuinely different action with its own color:

- C) Robson deve tentar falar com quem está lá dentro.

Use a short call to action such as: "Comente A ou B para decidir o que acontece." Update the letters to match the actual number of options. Do not say "A, B ou C" when the episode only has A and B.

## Step 5: animate and render

After the storyboard is approved or internally checked:

1. Implement the shots using the existing Remotion studio and reusable SVG components.
2. Keep the animation deterministic: the same frame/time input must produce the same visual output. Avoid random values that change between renders unless they are seeded.
3. Use the word timings to synchronize captions, visual events, and the choice cards.
4. Use 2D transforms for camera-like movement: translate, scale, crop, and controlled shake. Do not introduce 3D perspective by default.
5. Render a low-resolution or short preview first when practical. Inspect it for missing assets, broken SVGs, timing errors, abrupt transitions, and text overflow.
6. Render the final vertical video using the project's established Remotion scripts.
7. Combine narration, effects, ambience, and music with FFmpeg or the existing mastering scripts.
8. Run the final audio/video checks and confirm the MP4 exists before reporting completion.

Do not claim that a render succeeded until the output file has been verified.

## Step 6: episode continuation

When the user asks for a continuation:

1. Read the previous episode's script, character definitions, palette, and ending options.
2. If the winning option is not supplied, ask which letter won. Never guess or fabricate comment results.
3. Continue from the selected option, preserving character, environment, and story continuity.
4. Begin with a very short recap only when needed for viewers to understand the continuation.
5. Create a new meaningful decision at the end if the user wants another interactive episode.

## Step 7: credits and publishing checks

Create `out/<slug>/CREDITS.md` listing each component used and its licence or terms:

- Kokoro voice model and voice used;
- Whisper model used for word timings;
- procedural sound effects generated by this skill;
- any external CC0 or otherwise licensed music/sound assets, with source links;
- relevant project and library licences.

Before delivery, remind the user to check the licences and platform policies that apply to their planned use. Do not promise monetization or claim that repetitive, templated videos will qualify for monetization. Encourage original scripts, varied subjects, meaningful editing, and genuine creative contribution.

## Limits and honesty

- Kokoro is a free local voice option, but its delivery may sound less natural than premium voice services.
- Procedural sound effects are intentionally simple. A properly licensed sound library can improve the result.
- The skill has not necessarily been validated end to end in every environment. On the first run, create a short test episode, inspect the result, and fix compatibility issues before producing multiple episodes.
- Rendering is local and may take time depending on resolution, frame rate, effects, and hardware.
- Do not claim that any viral channel uses this exact workflow unless that creator has publicly confirmed it.
- Every factual claim in the narration must be checked and sourced. Clearly label speculation as speculation.
- Use original characters, scripts, and compositions. Do not imitate a specific creator's identifiable character designs or reproduce copyrighted material.
