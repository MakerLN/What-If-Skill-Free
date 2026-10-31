---
name: what-if-animation-free
description: Make a "What If" animated episode (15-25 s, stick-figure, drawn in code with SVG + Remotion) WITHOUT a paid API key. Replaces the ElevenLabs voice and sound-effect steps of the what-if-animation skill (kelano86) with free local tools - Kokoro TTS, Whisper word timings, and code-synthesized or CC0 sound effects. Use this whenever the user wants a What If episode, a What If animation, a stick-figure explainer from one topic line, or says they have no ElevenLabs key, want it free, want to monetize without paid voice licenses, or want to run what-if-animation in Antigravity or another agent. Use it even if they only say "make a What If episode about X".
compatibility: Needs the original what-if-animation skill (studio/ Remotion project + references/), Node 18+, ffmpeg, Python 3.9+ with numpy. Voice needs `pip install kokoro soundfile faster-whisper` and espeak-ng.
---

# What If episode, no paid API

This skill is a patch on top of the open-source `what-if-animation` skill
(https://github.com/kelano86/what-if-animation, MIT). That skill already has
the hard parts: the script formula, the shot list, the Remotion engine, the
character rig, the storyboard and the checklists. Its only paid dependency is
ElevenLabs, used for the voice (with word timings) and the sound effects.
Everything below swaps those two pieces and leaves the rest alone, so the
episodes keep the same look and pacing.

## Step 0: set up once (the agent does this on first use)

1. Confirm the original skill is installed. Look for its `SKILL.md`,
   `references/`, `scripts/` and `studio/` in the skills folder (for example
   `~/.gemini/antigravity/skills/what-if-animation` or
   `.agent/skills/what-if-animation`). If it's missing, tell the user to
   clone it and stop; don't recreate it from memory.
2. Make sure the studio has been copied to the working folder and
   `npm install` has run there (the original README has the commands).
3. Run `python scripts/voice_free.py --check` from this skill's folder. It
   lists which free tools are installed and which are missing.
4. If anything is missing, install it yourself instead of sending the user
   to do it by hand. Tell the user in one line what you're installing (the
   Python packages include PyTorch, so the download is large), then run
   `python -m pip install -r requirements.txt` from this skill's folder.
   On Windows, `install_windows.bat` in the same folder also installs ffmpeg
   and espeak-ng with winget; on Mac or Linux install those two with the
   system package manager. Run `--check` again and stop only if something is
   still missing. Do this automatically the first time the skill is used.

## Step 1: follow the original pipeline, with two swaps

Read the original `SKILL.md` and its `references/` first and follow them end
to end: script on the seven-beat formula, fact checking, shot list,
storyboard (show it to the user before animating), self-check, animation,
mastering. Two steps change:

### Swap A: voice and word timings (original step 2)

The original calls ElevenLabs. Use `scripts/voice_free.py` instead:

```
python scripts/voice_free.py --text-file out/<slug>/script.txt \
  --out out/<slug>/voice.wav --timings out/<slug>/voice.words.json \
  --lang p --voice pf_dora --speed 1.05
```

It does three things: synthesizes the narration with Kokoro, trims long
pauses to the fast pace the genre needs, then runs Whisper on the trimmed
audio to get start/end times for every word. Timings are measured after
trimming on purpose, so they match the audio the shot list is built on.

The original pipeline reads word timings in its own JSON shape, and I haven't
seen that shape. Before building the shot list, open the original
`scripts/voice` (and whatever reads its output, usually the plan script) and
compare. If the shapes differ, edit `write_timings()` in `voice_free.py` so
the output matches exactly, rather than editing the original scripts. The
generic output is `{"text", "audio", "duration", "words": [{"word", "start",
"end"}]}` with times in seconds.

Language: this user's channel is in Brazilian Portuguese, so the defaults are
`--lang p` with the voice `pf_dora` (female); `pm_alex` and `pm_santa` are the
male pt-BR voices. Generate a short test with each and let the user pick one,
then keep that voice for the whole channel. Other Kokoro language codes
exist (`a` US English, `b` UK English) if the user ever wants them.

Because the narration is Portuguese, write the whole script in Brazilian
Portuguese, following the same seven-beat formula (the formula doesn't depend
on the language). For the TTS to sound natural without an English accent:
write numbers and units out in words ("dez segundos", not "10 s"), avoid
English words and acronyms in the narration or spell them the way a
Brazilian would say them, and listen to any proper noun before moving on. If
a word comes out wrong, respell it phonetically in the narration text only
(keep the correct spelling on screen).

### Swap B: sound effects, ambience, music bed (original step 7)

Don't call the original `scripts/sfx` (ElevenLabs) and don't reuse the
clips in `studio/library/sfx/`: the original README says they were generated
on a paid ElevenLabs plan, and their licence for monetized use isn't
something to assume. Use `scripts/sfx_free.py`, which synthesizes effects
from math (noise, sweeps, decaying tones) and so belongs to the user:

```
python scripts/sfx_free.py --list
python scripts/sfx_free.py whoosh studio/library/sfx_free/whoosh.wav --dur 0.5
python scripts/sfx_free.py --all studio/library/sfx_free/
```

Generate the library once, then reuse it across episodes the way the
original reuses its own. Map each action in the shot list to the nearest
effect (whoosh for movement, pop for appearing, thud for impacts, rewind for
the time-reverse beat, ding for a reveal, riser before the turn, glitch for
breaks). The `pad` effect is a simple ambient bed for music; for more
character the user can drop in a CC0 track (see `references/licenses.md`).

Everything after the audio is generated is unchanged: line the effects up by
their attack, set levels against the voice, then master to -14 LUFS with the
original `mixcheck` and `master` scripts, which only use ffmpeg.

## Step 2: be honest about the limits

- Kokoro sounds good for a free local model but less natural than
  ElevenLabs. Synthesized effects are simple. Say so when delivering, and
  offer to swap in a CC0 sound pack or a different voice if the user wants a
  richer result.
- None of this has been run end to end by the author of this skill. For the
  first episode, generate a short one, listen to it, and fix whatever the
  pipeline stumbles on before doing a batch.
- Keep the original skill's rules: original characters only, original
  stories, every script fact checked and sourced, never claim the viral
  channels were made with any particular tool.

## Step 3: before publishing

Write `out/<slug>/CREDITS.md` listing each component used and its licence
(voice model, Whisper model, any CC0 sounds with the source link). Then
remind the user to check `references/licenses.md`, in particular the
platform policies on repetitive, templated content: publishing one
near-identical episode a day can hurt monetization, so vary topics, voices
and structure and add original commentary.
