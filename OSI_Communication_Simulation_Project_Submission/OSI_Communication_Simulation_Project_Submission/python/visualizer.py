import argparse
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "OSI-communication"
BUILD = SRC
WINDOWS = os.name == "nt"
LAYERS = [
    (7, "Application", "Create user data"),
    (6, "Presentation", "Encode data as hexadecimal"),
    (5, "Session", "Add session identifier"),
    (4, "Transport", "Prepare TCP segment"),
    (3, "Network", "Add logical IP addressing"),
    (2, "Data Link", "Create frame/check marker"),
    (1, "Physical", "Transmit bits through TCP socket"),
]

def layer_flow(title, items, arrow):
    print("\n" + "=" * 68)
    print(title.center(68))
    print("=" * 68)
    for i, (number, name, detail) in enumerate(items, 1):
        print(f"  Layer {number}: {name:<15} {arrow} {detail}")
        if i % 2 == 0:
            print(f"  >>> PROGRESS: {i}/7 layers completed\n")
        time.sleep(0.18)
    if len(items) % 2:
        print("  >>> PROGRESS: 7/7 layers completed")

def compile_c():
    ext = ".exe" if WINDOWS else ""
    client = BUILD / ("osi_client" + ext)
    server = BUILD / ("osi_server" + ext)
    cc = os.environ.get("CC", "gcc")
    libs = ["-lws2_32"] if WINDOWS else []
    for output, source in [(client, "client.c"), (server, "server.c")]:
        cmd = [cc, "-Wall", "-Wextra", "-std=c11", "-I", str(SRC),
               "-o", str(output), str(SRC/source), str(SRC/"layers.c"), *libs]
        subprocess.run(cmd, cwd=ROOT, check=True)
    return client, server

def main():
    parser = argparse.ArgumentParser(description="OSI 7-layer C socket simulation with Python visualization")
    parser.add_argument("--message", default="Hello from Python OSI visualizer!")
    args = parser.parse_args()
    if not args.message.strip() or len(args.message) > 500:
        parser.error("Message must contain 1 to 500 characters.")

    try:
        client_exe, server_exe = compile_c()
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print("[ERROR] GCC compilation failed. Install MinGW-w64 and add gcc to PATH.")
        print(error)
        return 1

    print("\nOSI 7-LAYER COMMUNICATION SIMULATION")
    print("C Client  --->  Real TCP Socket  --->  C Server")
    layer_flow("SENDER: ENCAPSULATION (LAYER 7 TO LAYER 1)", LAYERS, "↓")

    server = subprocess.Popen([str(server_exe)], cwd=ROOT,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        time.sleep(0.6)
        if server.poll() is not None:
            output, _ = server.communicate()
            print("[SERVER START ERROR]\n" + output)
            return 1
        client = subprocess.run([str(client_exe), args.message], cwd=ROOT,
                                capture_output=True, text=True, timeout=10)
        server_output, _ = server.communicate(timeout=5)
        if client.returncode != 0 or "FINAL MESSAGE:" not in server_output:
            print("[CLIENT OUTPUT]\n" + client.stdout + client.stderr)
            print("[SERVER OUTPUT]\n" + server_output)
            print("Communication failed.")
            return 1

        print("\n[NETWORK] Real TCP socket transfer completed: 127.0.0.1:50555")
        layer_flow("RECEIVER: DECAPSULATION (LAYER 1 TO LAYER 7)",
                   list(reversed(LAYERS)), "↑")
        print("\n========== C CLIENT OUTPUT ==========")
        print(client.stdout)
        print("========== C SERVER OUTPUT ==========")
        print(server_output)
        print("SUCCESS: Server recovered the original message and sent ACK.")
        print("Note: Layer headers are educational markers; TCP is real socket communication.")
        return 0
    finally:
        if server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=2)
            except subprocess.TimeoutExpired:
                server.kill()

if __name__ == "__main__":
    raise SystemExit(main())
