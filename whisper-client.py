#!/usr/bin/env python3

import socket

SOCK_PATH = "/tmp/whisper.sock"

def main():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(SOCK_PATH)

    print("sending start")
    sock.sendall(b"start")

    data = sock.recv(4096)
    print("➡ result:", data.decode())

    sock.close()

if __name__ == "__main__":
    main()
