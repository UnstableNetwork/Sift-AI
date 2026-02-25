# Sift AI: The Intelligent Folder Sentinel

**Sift AI** is a local Python automation tool that monitors your file system and uses AI to transform "noise" into organized data. 

### Features
* **Real-time Monitoring:** Watches any folder for new arrivals.
* **Local AI Transcription:** Automatically transcribes audio files (.mp3, .wav, .m4a) using OpenAI's Whisper model.
* **Privacy Focused:** All processing happens locally on your machine—no data is sent to the cloud.

### Installation

1. **Install FFmpeg:**
   Sift requires FFmpeg to process audio.
   - Windows: `choco install ffmpeg`
   - Mac: `brew install ffmpeg`

2. **Clone & Install Dependencies:**
   ```bash
   git clone [https://github.com/UnstableNetwork/Sift-AI.git](https://github.com/unstablenetwork/Sift-AI.git)
   cd Sift-AI
   pip install -r requirements.txt


## Run : ## >>

python sift_sentinel.py
