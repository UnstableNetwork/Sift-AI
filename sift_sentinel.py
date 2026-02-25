import os
import time
import whisper
import torch
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
WATCH_PATH = "./drops"  # The folder to watch
MODEL_SIZE = "base"      # 'tiny', 'base', or 'small'
SUPPORTED_AUDIO = {'.mp3', '.wav', '.m4a', '.flac'}

# Ensure the watch directory exists
if not os.path.exists(WATCH_PATH):
    os.makedirs(WATCH_PATH)

class SiftAI:
    def __init__(self, model_name):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Initializing AI on {self.device}...")
        self.model = whisper.load_model(model_name, device=self.device)
        print("AI Model Loaded & Ready.")

    def process_file(self, file_path):
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in SUPPORTED_AUDIO:
            self.transcribe(file_path)
        else:
            print(f"Skipping {os.path.basename(file_path)} (Unsupported extension)")

    def transcribe(self, file_path):
        print(f"Transcribing: {os.path.basename(file_path)}...")
        try:
            # fp16=False prevents the CPU warning you saw earlier
            result = self.model.transcribe(file_path, fp16=(self.device == "cuda"))
            
            # Save the transcript next to the original file
            output_path = os.path.splitext(file_path)[0] + ".txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result["text"].strip())
            
            print(f"✨ Success! Saved to: {os.path.basename(output_path)}")
        except Exception as e:
            print(f"Error transcribing {file_path}: {e}")

class SiftHandler(FileSystemEventHandler):
    def __init__(self, ai_engine):
        self.ai_engine = ai_engine

    def on_created(self, event):
        # Ignore folders and hidden files
        if event.is_directory or os.path.basename(event.src_path).startswith('.'):
            return
        
        # Give the OS a split second to finish writing the file to disk
        time.sleep(1) 
        self.ai_engine.process_file(event.src_path)

if __name__ == "__main__":
    # 1. Initialize the AI Engine
    engine = SiftAI(MODEL_SIZE)

    # 2. Setup the Watcher
    event_handler = SiftHandler(engine)
    observer = Observer()
    observer.schedule(event_handler, WATCH_PATH, recursive=False)
    
    print(f"Sift is now watching: {os.path.abspath(WATCH_PATH)}")
    print("Drop an audio file in there to see the magic. (Ctrl+C to stop)")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Sift is shutting down...")
        observer.stop()
    observer.join()
