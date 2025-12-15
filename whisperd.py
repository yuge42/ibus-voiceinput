#!/usr/bin/env python3

import os
import socket
import sounddevice as sd
import whisper
import numpy as np

SOCK_PATH = "/tmp/whisper.sock"
SAMPLE_RATE = 16000
RECORD_SECONDS = 5
MODEL_NAME = "base"

def record_audio():
    print("🎤 recording...")
    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    return audio[:, 0]

def main():
    if os.path.exists(SOCK_PATH):
        os.remove(SOCK_PATH)

    print("loading model...")
    model = whisper.load_model(MODEL_NAME)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCK_PATH)
    server.listen(1)

    print(f"whisper daemon listening on {SOCK_PATH}")

    while True:
        conn, _ = server.accept()
        try:
            cmd = conn.recv(1024).decode().strip()
            print("command:", cmd)

            if cmd == "start":
                audio = record_audio()
                print("🧠 transcribing...")
                result = model.transcribe(
                    audio,
                    language="ja",
                    fp16=False,
                    temperature=0.0,
                )
                text = result["text"].strip()
                conn.sendall(text.encode("utf-8"))

            else:
                conn.sendall(b"unknown command")

        except Exception as e:
            conn.sendall(f"error: {e}".encode())
        finally:
            conn.close()

if __name__ == "__main__":
    main()
