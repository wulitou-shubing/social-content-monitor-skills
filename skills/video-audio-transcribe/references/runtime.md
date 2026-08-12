# Runtime requirements

## Required software

- Python 3.10 or later
- `yt-dlp` for online media downloads
- `faster-whisper` for speech recognition
- `ffmpeg` for MP3 extraction and for media formats that require external decoding

Create a virtual environment and install Python dependencies from the skill directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Install `ffmpeg` with the operating system package manager. Examples:

```bash
brew install ffmpeg
sudo apt install ffmpeg
```

Do not run either command without user approval.

## Whisper model storage

The first transcription downloads the selected model. Later runs reuse the local Hugging Face cache. Model sizes and download times vary. Do not delete the cache unless the user asks.

The default endpoint is `https://huggingface.co`. To use a mirror explicitly:

```bash
python scripts/transcribe.py input.mp4 --hf-endpoint "https://example-mirror.invalid"
```

If the mirror fails and official fallback is permitted, add `--fallback-to-official`.

## Hardware defaults

The script defaults to CPU with `int8`, which works on common computers. CUDA users may choose a compatible device and compute type supported by their faster-whisper/CTranslate2 installation.
