#!/usr/bin/env python3
"""Free narration for the What If pipeline: Kokoro TTS + Whisper word timings.

Replaces the ElevenLabs voice step. Steps:
  1. synthesize the script with Kokoro (local, no API key)
  2. trim long pauses with ffmpeg (genre pace)
  3. transcribe the trimmed audio with faster-whisper to get per-word times

Usage:
  python voice_free.py --check
  python voice_free.py --text-file script.txt --out voice.wav \
      --timings voice.words.json --lang p --voice pf_dora --speed 1.05

Not tested end to end by the author: Kokoro and faster-whisper download their
models on first run, which needs internet on the user's machine.
"""
import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SAMPLE_RATE = 24000  # Kokoro output rate

# Kokoro language code -> Whisper language code
WHISPER_LANG = {
    "a": "en", "b": "en", "e": "es", "f": "fr", "h": "hi",
    "i": "it", "j": "ja", "p": "pt", "z": "zh",
}


def have(module):
    return importlib.util.find_spec(module) is not None


def check():
    rows = [
        ("numpy", have("numpy"), "pip install numpy"),
        ("soundfile", have("soundfile"), "pip install soundfile"),
        ("kokoro", have("kokoro"), "pip install kokoro"),
        ("faster-whisper", have("faster_whisper"), "pip install faster-whisper"),
        ("ffmpeg", shutil.which("ffmpeg") is not None, "install ffmpeg (brew/apt/choco)"),
        ("espeak-ng", shutil.which("espeak-ng") is not None,
         "install espeak-ng (needed by Kokoro for some languages)"),
    ]
    ok = True
    for name, present, hint in rows:
        print(f"{'OK     ' if present else 'MISSING'} {name}" + ("" if present else f"  -> {hint}"))
        ok = ok and present
    return 0 if ok else 1


def synthesize(text, lang, voice, speed, out_wav):
    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline

    pipeline = KPipeline(lang_code=lang)
    chunks = []
    for _graphemes, _phonemes, audio in pipeline(text, voice=voice, speed=speed):
        arr = audio.numpy() if hasattr(audio, "numpy") else np.asarray(audio)
        chunks.append(arr)
    if not chunks:
        raise RuntimeError("Kokoro returned no audio. Check the text and --lang/--voice.")
    sf.write(str(out_wav), np.concatenate(chunks), SAMPLE_RATE)


def tighten(in_wav, out_wav, max_gap, keep):
    """Cut silences longer than max_gap seconds down to `keep` seconds."""
    if not shutil.which("ffmpeg"):
        print("warning: ffmpeg not found, skipping pause trimming", file=sys.stderr)
        shutil.copy(in_wav, out_wav)
        return
    flt = (
        "silenceremove=start_periods=0:stop_periods=-1:"
        f"stop_duration={max_gap}:stop_threshold=-45dB:stop_silence={keep}"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(in_wav), "-af", flt, str(out_wav)],
        check=True,
    )


def audio_duration(path):
    if shutil.which("ffprobe"):
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)],
            capture_output=True, text=True, check=True,
        )
        return round(float(r.stdout.strip()), 3)
    import soundfile as sf
    info = sf.info(str(path))
    return round(info.frames / info.samplerate, 3)


def word_timings(wav, whisper_lang, model_size):
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(str(wav), word_timestamps=True, language=whisper_lang)
    words = []
    for seg in segments:
        for w in seg.words or []:
            token = w.word.strip()
            if token:
                words.append({"word": token, "start": round(w.start, 3), "end": round(w.end, 3)})
    return words


def write_timings(path, text, audio_path, duration, words):
    """Generic shape. If the original pipeline expects a different JSON shape,
    edit ONLY this function so the output matches it."""
    payload = {
        "text": text,
        "audio": str(audio_path),
        "duration": duration,
        "words": words,
    }
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="list installed/missing dependencies")
    ap.add_argument("--text-file", help="narration script, plain text")
    ap.add_argument("--text", help="narration as a string (alternative to --text-file)")
    ap.add_argument("--out", help="output narration .wav")
    ap.add_argument("--timings", help="output word-timings .json")
    ap.add_argument("--lang", default="p", help="Kokoro language code: p=pt-BR (default), a=US English, b=UK, ...")
    ap.add_argument("--voice", default="pf_dora", help="Kokoro voice name (pt-BR: pf_dora, pm_alex, pm_santa)")
    ap.add_argument("--speed", type=float, default=1.05)
    ap.add_argument("--max-gap", type=float, default=0.30, help="cut pauses longer than this (s)")
    ap.add_argument("--keep-gap", type=float, default=0.12, help="leave this much silence (s)")
    ap.add_argument("--whisper-model", default="base", help="tiny, base, small...")
    ap.add_argument("--whisper-lang", help="override Whisper language code")
    args = ap.parse_args()

    if args.check:
        return check()

    if not (args.out and args.timings and (args.text or args.text_file)):
        ap.error("--out, --timings and one of --text/--text-file are required (or use --check)")

    missing = [m for m in ("numpy", "soundfile", "kokoro", "faster_whisper") if not have(m)]
    if missing:
        print("Missing Python packages: " + ", ".join(missing), file=sys.stderr)
        print("Run with --check for install commands.", file=sys.stderr)
        return 1

    text = args.text if args.text else Path(args.text_file).read_text(encoding="utf-8").strip()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    Path(args.timings).parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "raw.wav"
        print("1/3 synthesizing with Kokoro...")
        synthesize(text, args.lang, args.voice, args.speed, raw)
        print("2/3 trimming long pauses...")
        tighten(raw, out, args.max_gap, args.keep_gap)

    print("3/3 measuring word timings with Whisper...")
    wl = args.whisper_lang or WHISPER_LANG.get(args.lang, "en")
    words = word_timings(out, wl, args.whisper_model)
    write_timings(args.timings, text, out, audio_duration(out), words)
    print(f"done: {out} ({len(words)} words) and {args.timings}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
