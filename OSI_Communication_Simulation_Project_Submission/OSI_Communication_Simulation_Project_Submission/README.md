# OSI Communication Simulation Project

This project is based on the supplied `OSI_Communication_Simulation_Project` repository and has been adapted to match the assignment brief for Windows 11.

## Assignment requirements covered
- C-based client and server applications.
- Real TCP socket communication between two separate C processes.
- Seven-layer sender encapsulation (Layer 7 to Layer 1).
- Seven-layer receiver decapsulation (Layer 1 to Layer 7).
- Python user application to visualize the zig-zag data flow.
- Progress output after every two OSI layers.
- Source code, build instructions, and project documentation.

## Project structure
```text
OSI_Communication_Simulation_Project/
├── OSI-communication/
│   ├── client.c
│   ├── server.c
│   ├── layers.c
│   ├── layers.h
│   └── Makefile
├── python/
│   └── visualizer.py
├── OSI_Model.md
├── requirements.txt
├── run.bat
└── README.md
```

## Windows 11 prerequisites
Install:
1. Python 3.9 or newer
2. GCC compiler (MinGW-w64) and add its `bin` directory to Windows PATH
3. VS Code

Check in VS Code terminal:
```powershell
python --version
gcc --version
```

No third-party Python packages are required. The visualizer uses only the Python standard library.

## Run (recommended)
Open the repository root folder in VS Code, then run:
```powershell
python python/visualizer.py
```
Custom message:
```powershell
python python/visualizer.py --message "Hello Server from Afrin!"
```
Or double-click `run.bat` from File Explorer. You can also pass a custom message to the batch file, for example `run.bat --message "Hello Server"`.
The Python application compiles both C programs, starts the C server, launches the C client, verifies the recovered message, and prints the two-direction OSI layer flow.

## Run manually
Open two terminals in the `OSI-communication` folder.

Terminal 1:
```powershell
gcc -Wall -Wextra -std=c11 -o osi_server.exe server.c layers.c -lws2_32
.\osi_server.exe
```
Terminal 2:
```powershell
gcc -Wall -Wextra -std=c11 -o osi_client.exe client.c layers.c -lws2_32
.\osi_client.exe "Hello Server"
```

## Layer simulation
| Layer | Sender (encapsulation) | Receiver (decapsulation) |
|---|---|---|
| 7 Application | Create user message | Deliver recovered message |
| 6 Presentation | Encode bytes as hexadecimal | Decode hexadecimal |
| 5 Session | Add session ID | Validate session ID |
| 4 Transport | Add TCP segment marker; use TCP socket | Process TCP segment marker |
| 3 Network | Add logical IP marker | Validate IP marker |
| 2 Data Link | Add Ethernet-style frame/check marker | Validate frame/check marker |
| 1 Physical | Show bit transmission stage over socket | Receive frame from socket |

## Technical accuracy note
The program uses a real TCP socket for communication between the C client and C server. The visible OSI layer headers are educational simulation markers; this program does not create real Ethernet, IP, or physical-layer headers. The operating system implements the actual TCP/IP stack. The Python program visualizes the complete seven-layer conceptual path.

## Troubleshooting
- `gcc is not recognized`: install MinGW-w64, add its `bin` directory to PATH, restart VS Code.
- `python is not recognized`: install Python with "Add Python to PATH", or use `py python/visualizer.py`.
- Port 50555 busy: close any process using that port and retry.
- If a firewall dialog appears, allow local/private network access for local testing.

## Submission checklist
- Run the project on your own PC.
- Take a screenshot showing successful output and Windows username or date/time.
- Upload the complete project folder to your own GitHub repository.
- Submit the GitHub repository URL and screenshot.

## Important academic note
This is an educational OSI simulation. The C programs exchange the encapsulated data over a genuine TCP socket. The visible Session, IP, and Ethernet-style fields are simulated headers for demonstrating the OSI concepts; they are not raw Ethernet/IP packets. Your operating system handles the actual TCP/IP networking stack.
