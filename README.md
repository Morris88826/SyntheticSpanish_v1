# SyntheticSpanish v1

A parallel speech corpus pairing native American-English LibriTTS recordings with synthetic Spanish-accented versions of the same utterances.

## Authors

[Mu-Ruei Tseng](https://scholar.google.com/citations?user=X0tFoE8AAAAJ&hl=en), Waris Quamer, Ghady Nasrallah, and Ricardo Gutierrez-Osuna

## Overview

| | |
|---|---|
| **Speakers** | 375 |
| **Utterances** | 54,478 |
| **Total duration** | ~89 hours |
| **Format** | WAV (16 kHz, mono) |
| **Pairs** | Native (LibriTTS) ↔ Dorado (Spanish-accented) |

## Pipeline

```
LibriTTS corpus  →  ElevenLabs TTS (Elio, Spanish accent)  →  Seed-VC  →  Parallel dataset
  (native speech)      (accent synthesis)                     (voice conversion)
```

1. **LibriTTS** — source utterances from `train-clean-100` and `train-other-500` subsets
2. **ElevenLabs** — synthesized using speaker ID `QZRlT5NqTgs34Uz6r1me` (Elio) to introduce a Spanish accent
3. **Seed-VC** — voice conversion applied to further refine the accent transfer

## Repository Structure

```
SyntheticSpanish_v1/
├── data/                   # Dorado (Spanish-accented) WAV files, by speaker
├── parallel_data/
│   ├── golden_speakers/    # Native LibriTTS WAV files, by speaker
│   └── elevenlab_tts/      # Raw ElevenLabs synthesis output
├── raw_data/               # Raw synthesized data before preprocessing
├── metadata/
│   ├── speakers.csv        # Per-speaker metadata (gender, subset, name)
│   ├── metadata.csv        # Per-speaker stats (num samples, total seconds)
│   └── american_to_spanish.csv  # Parallel file mapping (src → tgt)
├── demo/                   # Demo audio samples (4 pairs)
│   └── manifest.json       # Sample manifest for demo page
├── demo.html               # Interactive demo page (GitHub Pages)
├── preprocess.ipynb        # Preprocessing pipeline
├── clean.ipynb             # Data cleaning notebook
└── verify.ipynb            # Verification notebook
```

## Usage

### Metadata

`metadata/american_to_spanish.csv` maps each native source WAV to its Spanish-accented counterpart:

```csv
src_wav,tgt_wav
/path/to/LibriTTS/.../4222_12898_000011_000002.wav,/path/to/SyntheticSpanish_v1/data/4222/wav/...wav
```

`metadata/speakers.csv` lists speaker information:

```csv
READER,GENDER,SUBSET,NAME
31,M,train-other-500,Martin Clifton
...
```

### Preprocessing

Run `preprocess.ipynb` to regenerate metadata from raw data.

## Demo

See [`demo.html`](demo.html) for an interactive listening comparison between native and Dorado speakers.

## Data Sources

- [LibriTTS](https://www.openslr.org/60/) — Zen et al., 2019
- [ElevenLabs](https://elevenlabs.io) — TTS synthesis
- [Seed-VC](https://github.com/Plachtaa/seed-vc) — Voice conversion
