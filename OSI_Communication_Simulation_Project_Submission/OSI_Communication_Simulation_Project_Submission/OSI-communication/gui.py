
import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import time
from pathlib import Path

# ================= CONFIGURATION =================

BASE_DIR = Path(__file__).resolve().parent
CLIENT_EXE = BASE_DIR / "client.exe"
SERVER_EXE = BASE_DIR / "server.exe"

LAYERS = [
    ("L7", "Application"),
    ("L6", "Presentation"),
    ("L5", "Session"),
    ("L4", "Transport"),
    ("L3", "Network"),
    ("L2", "Data Link"),
    ("L1", "Physical"),
]

RECEIVER_LAYERS = [
    "Physical",
    "Data Link",
    "Network",
    "Transport",
    "Session",
    "Presentation",
    "Application",
]

BG = "#101b35"
PANEL = "#182746"
BLUE = "#2684ff"
GREEN = "#22c55e"
WHITE = "#ffffff"
GRAY = "#aab8d0"

running = False
active_layer = 0
communication_done = False
communication_success = False

server_output = ""
client_output = ""

# ================= TERMINAL PROGRESS =================

def terminal_progress(title, layer_name, percentage):
    bar_length = 25
    filled = int(bar_length * percentage / 100)
    bar = "█" * filled + "░" * (bar_length - filled)

    print(
        f"\r{title:<15} {layer_name:<15} "
        f"[{bar}] {percentage}%",
        flush=True
    )


# ================= GUI WINDOW =================

root = tk.Tk()
root.title("OSI Model Communication Simulator")
root.geometry("1100x780")
root.configure(bg=BG)
root.resizable(False, False)

title = tk.Label(
    root,
    text="OSI MODEL COMMUNICATION SIMULATOR",
    font=("Arial", 22, "bold"),
    bg=BG,
    fg=WHITE
)
title.pack(pady=(20, 5))

subtitle = tk.Label(
    root,
    text="TCP CLIENT-SERVER COMMUNICATION USING OSI 7 LAYERS",
    font=("Arial", 10),
    bg=BG,
    fg=GRAY
)
subtitle.pack(pady=(0, 18))


# ================= MESSAGE INPUT =================

top = tk.Frame(root, bg=PANEL, padx=18, pady=15)
top.pack(fill="x", padx=35)

tk.Label(
    top,
    text="Enter Message:",
    font=("Arial", 12, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(anchor="w")

message_entry = tk.Entry(
    top,
    font=("Arial", 12),
    bg="#243657",
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)
message_entry.pack(fill="x", pady=10, ipady=8)

message_entry.insert(
    0,
    "Hello from the OSI communication project!"
)

start_button = tk.Button(
    top,
    text="START SIMULATION",
    font=("Arial", 12, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground="#1766d1",
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=10
)
start_button.pack(pady=5)


# ================= STATUS =================

status_label = tk.Label(
    root,
    text="Ready to start communication",
    font=("Arial", 12, "bold"),
    bg=BG,
    fg="#facc15"
)
status_label.pack(pady=15)


# ================= OSI LAYER DISPLAY =================

canvas = tk.Canvas(
    root,
    width=1020,
    height=300,
    bg=BG,
    highlightthickness=0
)
canvas.pack(padx=30)

canvas.create_text(
    245, 20,
    text="SENDER (ENCAPSULATION)",
    fill="#60a5fa",
    font=("Arial", 13, "bold")
)

canvas.create_text(
    775, 20,
    text="RECEIVER (DECAPSULATION)",
    fill="#4ade80",
    font=("Arial", 13, "bold")
)

# Sender layers
for i, (layer, name) in enumerate(LAYERS):
    x = 75 + (i % 2) * 35
    y = 55 + i * 34

    canvas.create_rectangle(
        x, y, x + 300, y + 27,
        fill=PANEL,
        outline="#405477",
        width=1,
        tags=f"sender_{i}"
    )

    canvas.create_text(
        x + 150, y + 13,
        text=f"{layer} - {name}",
        fill=WHITE,
        font=("Arial", 10, "bold"),
        tags=f"sender_text_{i}"
    )

# Receiver layers (L1 to L7)
for i, name in enumerate(RECEIVER_LAYERS):
    x = 610 + (i % 2) * 35
    y = 55 + i * 34

    canvas.create_rectangle(
        x, y, x + 300, y + 27,
        fill=PANEL,
        outline="#405477",
        width=1,
        tags=f"receiver_{i}"
    )

    canvas.create_text(
        x + 150, y + 13,
        text=f"L{i+1} - {name}",
        fill=WHITE,
        font=("Arial", 10, "bold"),
        tags=f"receiver_text_{i}"
    )

canvas.create_text(
    510, 145,
    text="TCP SOCKET",
    fill="#facc15",
    font=("Arial", 13, "bold")
)

canvas.create_line(
    410, 145, 600, 145,
    fill=BLUE,
    width=3,
    arrow=tk.LAST
)


# ================= PROGRESS BAR =================

progress_label = tk.Label(
    root,
    text="Sender Progress: 0/7 (0%)",
    font=("Arial", 11, "bold"),
    bg=BG,
    fg=WHITE
)
progress_label.pack(pady=(5, 4))

progress_bg = tk.Frame(
    root,
    bg="#334563",
    height=13
)
progress_bg.pack(fill="x", padx=70)
progress_bg.pack_propagate(False)

progress_bar = tk.Frame(
    progress_bg,
    bg=BLUE,
    width=0,
    height=13
)
progress_bar.place(x=0, y=0, relheight=1)


# ================= COMMUNICATION LOG =================

tk.Label(
    root,
    text="COMMUNICATION LOG",
    font=("Arial", 11, "bold"),
    bg=BG,
    fg=WHITE
).pack(pady=(12, 5))

log_box = tk.Text(
    root,
    height=7,
    bg="#0b1428",
    fg="#dbeafe",
    font=("Consolas", 9),
    relief="flat",
    wrap="word"
)
log_box.pack(fill="both", padx=35, pady=(0, 15))


def log(message):
    log_box.insert("end", message + "\n")
    log_box.see("end")


# ================= RESET LAYERS =================

def reset_layers():
    for i in range(7):
        canvas.itemconfig(
            f"sender_{i}",
            fill=PANEL,
            outline="#405477"
        )

        canvas.itemconfig(
            f"sender_text_{i}",
            fill=WHITE
        )

        canvas.itemconfig(
            f"receiver_{i}",
            fill=PANEL,
            outline="#405477"
        )

        canvas.itemconfig(
            f"receiver_text_{i}",
            fill=WHITE
        )


# ================= REAL TCP COMMUNICATION =================

def run_communication(message):
    global communication_done
    global communication_success
    global server_output
    global client_output

    server_process = None

    try:
        if not CLIENT_EXE.exists():
            raise FileNotFoundError("client.exe not found!")

        if not SERVER_EXE.exists():
            raise FileNotFoundError("server.exe not found!")

        no_window = getattr(subprocess, "CREATE_NO_WINDOW", 0)

        # Start server
        server_process = subprocess.Popen(
            [str(SERVER_EXE)],
            cwd=str(BASE_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=no_window
        )

        time.sleep(0.8)

        if server_process.poll() is not None:
            server_output, _ = server_process.communicate(timeout=3)

            raise RuntimeError(
                "Server could not start. "
                "Another server may already be running.\n"
                + server_output
            )

        # Start client and send message
        client_result = subprocess.run(
            [str(CLIENT_EXE), message],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=12,
            creationflags=no_window
        )

        client_output = (
            client_result.stdout + client_result.stderr
        )

        # Get server result
        server_output, _ = server_process.communicate(
            timeout=8
        )

        communication_success = (
            client_result.returncode == 0
            and "FINAL MESSAGE:" in server_output
            and message in server_output
        )

    except Exception as error:
        communication_success = False

        server_output += "\nERROR: " + str(error)

        if server_process is not None:
            if server_process.poll() is None:
                server_process.kill()

                try:
                    extra, _ = server_process.communicate(
                        timeout=2
                    )
                    server_output += extra
                except Exception:
                    pass

    finally:
        communication_done = True

        root.after(
            0,
            finish_simulation
        )


# ================= FINISH SIMULATION =================

def finish_simulation():
    global running

    if server_output:
        log("\n--- SERVER OUTPUT ---")
        log(server_output.strip())

    if client_output:
        log("\n--- CLIENT OUTPUT ---")
        log(client_output.strip())

    if communication_success:
        status_label.config(
            text="SUCCESS: Message delivered successfully!",
            fg=GREEN
        )

        log("\nSUCCESS: Real TCP communication completed.")

    else:
        status_label.config(
            text="Communication failed. Check the log below.",
            fg="#f87171"
        )

        log("\nFAILED: Please check the error above.")

    running = False

    start_button.config(
        state="normal",
        text="START SIMULATION"
    )


# ================= ENCAPSULATION ANIMATION =================

def animate_layer():
    global active_layer

    if active_layer < 7:
        i = active_layer

        layer_name = LAYERS[i][1]
        percentage = int(((i + 1) / 7) * 100)

        # GUI animation
        canvas.itemconfig(
            f"sender_{i}",
            fill=BLUE,
            outline=BLUE
        )

        canvas.itemconfig(
            f"sender_text_{i}",
            fill=WHITE
        )

        progress_bar.config(
            width=int(950 * (i + 1) / 7)
        )

        progress_label.config(
            text=f"Sender Progress: {i+1}/7 ({percentage}%)"
        )

        status_label.config(
            text=f"Sender: {layer_name} Layer"
        )

        # GUI log
        log(
            f"[Sender] {LAYERS[i][0]} "
            f"{layer_name} Layer - Encapsulation"
        )

        # Terminal percentage
        terminal_progress(
            "ENCAPSULATION",
            layer_name,
            percentage
        )

        active_layer += 1

        root.after(
            450,
            animate_layer
        )

    else:
        print(
            "\nEncapsulation completed!\n",
            flush=True
        )

        status_label.config(
            text="Encapsulation complete. Decapsulating...",
            fg="#facc15"
        )

        root.after(
            300,
            animate_decapsulation,
            0
        )


# ================= DECAPSULATION ANIMATION =================

def animate_decapsulation(index):
    if index < 7:
        layer_name = RECEIVER_LAYERS[index]
        percentage = int(((index + 1) / 7) * 100)

        # GUI receiver animation
        canvas.itemconfig(
            f"receiver_{index}",
            fill=GREEN,
            outline=GREEN
        )

        canvas.itemconfig(
            f"receiver_text_{index}",
            fill=WHITE
        )

        # GUI progress
        progress_bar.config(
            width=int(950 * (index + 1) / 7)
        )

        progress_label.config(
            text=f"Receiver Progress: {index+1}/7 ({percentage}%)"
        )

        status_label.config(
            text=f"Receiver: {layer_name} Layer"
        )

        log(
            f"[Receiver] L{index+1} "
            f"{layer_name} Layer - Decapsulation"
        )

        # Terminal percentage
        terminal_progress(
            "DECAPSULATION",
            layer_name,
            percentage
        )

        root.after(
            450,
            animate_decapsulation,
            index + 1
        )

    else:
        print(
            "\nDecapsulation completed!\n",
            flush=True
        )

        status_label.config(
            text="Waiting for communication result...",
            fg="#facc15"
        )

        check_completion()


# ================= CHECK COMMUNICATION =================

def check_completion():
    if communication_done:
        finish_simulation()
    else:
        root.after(
            200,
            check_completion
        )


# ================= START SIMULATION =================

def start_simulation():
    global running
    global active_layer
    global communication_done
    global communication_success
    global server_output
    global client_output

    if running:
        return

    message = message_entry.get().strip()

    if not message:
        messagebox.showwarning(
            "Empty Message",
            "Please enter a message."
        )
        return

    if len(message) > 500:
        messagebox.showwarning(
            "Message Too Long",
            "Message must be 500 characters or less."
        )
        return

    # Reset variables
    running = True
    active_layer = 0

    communication_done = False
    communication_success = False

    server_output = ""
    client_output = ""

    reset_layers()

    progress_bar.config(width=0)

    progress_label.config(
        text="Sender Progress: 0/7 (0%)"
    )

    log_box.delete(
        "1.0",
        "end"
    )

    # Terminal output
    print("\n" + "=" * 55)
    print("       OSI COMMUNICATION SIMULATION STARTED")
    print("=" * 55)

    print("\nMessage:", message)
    print("\n========== ENCAPSULATION ==========\n")

    # GUI output
    log("OSI Communication Simulation Started")
    log("Message: " + message)
    log("Starting real TCP client-server communication...")

    status_label.config(
        text="Starting server and client...",
        fg="#facc15"
    )

    start_button.config(
        state="disabled",
        text="RUNNING..."
    )

    # Start actual TCP communication in background
    threading.Thread(
        target=run_communication,
        args=(message,),
        daemon=True
    ).start()

    # Start GUI animation
    root.after(
        450,
        animate_layer
    )


# ================= BUTTON ACTION =================

start_button.config(
    command=start_simulation
)

# ================= RUN GUI =================

root.mainloop()
