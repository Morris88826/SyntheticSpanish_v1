import os
import tqdm
import glob
import argparse
from scipy.io import wavfile
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

load_dotenv()
client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

def create_tts_audio(text, voice_id="QZRlT5NqTgs34Uz6r1me", model_id="eleven_multilingual_v2", output_format="wav_16000"):
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
    )
    return audio

corpus_map = {
    'LibriTTS': '/data/mtseng/voice_datasets/LibriTTS'
}

accent_map = {
    'Spanish': 'QZRlT5NqTgs34Uz6r1me',
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate TTS audio using ElevenLabs API")
    parser.add_argument("--corpus", type=str, default="LibriTTS", help="Path to the corpus directory (ex: LibriTTS)")
    parser.add_argument("--accent", type=str, default="Spanish", help="Accent for TTS voice (ex: Spanish)")
    parser.add_argument("--out_dir", type=str, default="./raw_data", help="Directory to save the generated TTS audio")
    args = parser.parse_args()

    assert args.corpus in corpus_map, f"Unsupported corpus: {args.corpus}. Supported corpora: {list(corpus_map.keys())}"

    target_accent = args.accent
    if target_accent not in accent_map:
        raise ValueError(f"Unsupported accent: {target_accent}. Supported accents: {list(accent_map.keys())}")
    voice_id = accent_map[target_accent]
    out_dir = args.out_dir
    data_root_dir = corpus_map[args.corpus]

    os.makedirs(out_dir, exist_ok=True)
    subject_dirs = glob.glob(os.path.join(data_root_dir, 'data', '*'))

    for subject_dir in tqdm.tqdm(subject_dirs):
        speaker_id = os.path.basename(subject_dir)
        wav_paths = glob.glob(os.path.join(subject_dir, 'wav', '*.wav'))
        speaker_out_dir = os.path.join(out_dir, speaker_id)
        os.makedirs(speaker_out_dir, exist_ok=True)

        for wav_path in wav_paths:
            tts_out_path = os.path.join(speaker_out_dir, 'wav', os.path.basename(wav_path))
            if os.path.exists(tts_out_path):
                print(f"File already exists, skipping: {tts_out_path}")
                continue
            os.makedirs(os.path.dirname(tts_out_path), exist_ok=True)
            transcript_path = wav_path.replace('.wav', '.txt').replace('/wav/', '/transcript/')
            assert os.path.exists(transcript_path), f"Transcript not found for {wav_path}"
            with open(transcript_path, 'r') as f:
                text = f.read().strip()
            audio = create_tts_audio(
                text=text
            )
            with open(tts_out_path, "wb") as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)
