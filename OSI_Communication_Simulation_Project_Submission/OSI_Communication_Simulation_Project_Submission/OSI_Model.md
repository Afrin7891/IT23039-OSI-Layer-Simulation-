# OSI (Open Systems Interconnection) Model

## Table of Contents

1. Introduction
2. Definition
3. Why OSI Model Is Needed
4. History of OSI Model
5. OSI Architecture Overview
6. The 7 Layers of OSI Model
7. Layer-by-Layer Explanation
8. Data Encapsulation Process
9. Data Decapsulation Process
10. Protocols Used at Each Layer
11. Devices Used at Each Layer
12. OSI vs TCP/IP Model
13. Advantages
14. Disadvantages
15. Real-Time Examples
16. Major Project Usage
17. Troubleshooting Using OSI Model
18. Interview Questions
19. Conclusion

---

# 1. Introduction

Computers communicate over networks using standardized rules.

Without standards:

```text
Computer A
     X
Computer B
```

Communication becomes difficult because different hardware and software vendors may use different methods.

To solve this problem, networking standards were introduced.

One of the most important standards is the **OSI Model**.

---

# 2. Definition

## Definition

The **OSI (Open Systems Interconnection) Model** is a conceptual framework developed by the International Organization for Standardization (ISO) that describes how data travels from one computer to another through seven distinct layers.

Each layer performs specific functions and communicates with the corresponding layer on another system.

---

## Simple Definition

```text
OSI Model =
7-Layer Framework
for Network Communication
```

---

# 3. Why OSI Model Is Needed

The OSI model provides:

### Standardization

Different systems can communicate.

---

### Interoperability

Devices from different vendors work together.

---

### Modularity

Each layer has a specific responsibility.

---

### Easier Troubleshooting

Network issues can be isolated layer by layer.

---

### Scalability

Network technologies can evolve independently.

---

# 4. History of OSI Model

Developed by:

* ISO (International Organization for Standardization)

Introduced:

* 1984

Goal:

```text
Universal Networking Standard
```

Although modern networks mainly use TCP/IP, OSI remains the most important learning and troubleshooting model.

---

# 5. OSI Architecture Overview

The OSI model contains 7 layers.

```text
+--------------------+
| 7. Application     |
+--------------------+
| 6. Presentation    |
+--------------------+
| 5. Session         |
+--------------------+
| 4. Transport       |
+--------------------+
| 3. Network         |
+--------------------+
| 2. Data Link       |
+--------------------+
| 1. Physical        |
+--------------------+
```

---

## Mnemonic

### Top to Bottom

```text
All
People
Seem
To
Need
Data
Processing
```

---

### Bottom to Top

```text
Please
Do
Not
Throw
Sausage
Pizza
Away
```

---

# 6. The 7 Layers of OSI Model

| Layer | Name         | Main Function      |
| ----- | ------------ | ------------------ |
| 7     | Application  | User Services      |
| 6     | Presentation | Data Format        |
| 5     | Session      | Session Management |
| 4     | Transport    | Reliable Delivery  |
| 3     | Network      | Routing            |
| 2     | Data Link    | Frame Transfer     |
| 1     | Physical     | Bit Transmission   |

---

# 7. Layer-by-Layer Explanation

# Layer 7: Application Layer

## Purpose

Provides services directly to users and applications.

---

## Responsibilities

* Email
* Web Browsing
* File Transfer
* Remote Login

---

## Protocols

* HTTP
* HTTPS
* FTP
* SMTP
* POP3
* IMAP
* DNS

---

## Example

Opening a website:

```text
www.google.com
```

Application Layer starts communication.

---

# Layer 6: Presentation Layer

## Purpose

Handles data representation.

---

## Responsibilities

### Data Translation

Example:

```text
ASCII ↔ Unicode
```

---

### Encryption

Example:

```text
HTTPS
SSL/TLS
```

---

### Compression

Example:

```text
ZIP
JPEG
MP3
```

---

# Layer 5: Session Layer

## Purpose

Creates, maintains, and terminates sessions.

---

## Responsibilities

* Session establishment
* Session synchronization
* Session recovery

---

## Example

```text
Video Conference Session
```

Session layer maintains connection.

---

# Layer 4: Transport Layer

## Purpose

Provides end-to-end communication.

---

## Responsibilities

* Segmentation
* Flow Control
* Error Control
* Reliability

---

## Protocols

### TCP

Reliable

```text
Acknowledgments
Retransmissions
```

---

### UDP

Fast

```text
No Guarantee
```

---

## Example

Web page download.

---

# Layer 3: Network Layer

## Purpose

Responsible for routing packets.

---

## Responsibilities

* Logical Addressing
* Path Selection
* Routing

---

## Protocols

* IP
* ICMP
* OSPF
* RIP
* BGP

---

## Device

Router

---

## Example

```text
Source IP → Destination IP
```

---

# Layer 2: Data Link Layer

## Purpose

Transfers frames between devices on the same network.

---

## Responsibilities

* Framing
* MAC Addressing
* Error Detection

---

## Protocols

* Ethernet
* PPP
* ARP

---

## Device

Switch

---

## Example

```text
MAC Address
00:1A:2B:3C:4D:5E
```

---

# Layer 1: Physical Layer

## Purpose

Transmits raw bits.

---

## Responsibilities

* Electrical Signals
* Optical Signals
* Radio Signals

---

## Devices

* Hub
* Repeater
* Cables
* Connectors

---

## Example

```text
0 1 0 1 1 0
```

Raw binary transmission.

---

# 8. Data Encapsulation Process

When sending data:

```text
Application Data
       ↓
Transport Segment
       ↓
Network Packet
       ↓
Data Link Frame
       ↓
Bits
```

---

## Encapsulation Diagram

```text
Data
 ↓
Segment
 ↓
Packet
 ↓
Frame
 ↓
Bits
```

---

# 9. Data Decapsulation Process

Receiving side:

```text
Bits
 ↓
Frame
 ↓
Packet
 ↓
Segment
 ↓
Data
```

---

# 10. Protocols Used at Each Layer

| Layer        | Protocols                            |
| ------------ | ------------------------------------ |
| Application  | HTTP, HTTPS, FTP, SMTP, DNS          |
| Presentation | SSL, TLS, JPEG, MP3                  |
| Session      | NetBIOS, RPC                         |
| Transport    | TCP, UDP                             |
| Network      | IP, ICMP, OSPF                       |
| Data Link    | Ethernet, PPP, ARP                   |
| Physical     | Fiber, Wi-Fi Signals, Ethernet Cable |

---

# 11. Devices Used at Each Layer

| Layer        | Device        |
| ------------ | ------------- |
| Application  | Gateway       |
| Presentation | Gateway       |
| Session      | Gateway       |
| Transport    | Firewall      |
| Network      | Router        |
| Data Link    | Switch        |
| Physical     | Hub, Repeater |

---

# 12. OSI vs TCP/IP Model

| OSI           | TCP/IP            |
| ------------- | ----------------- |
| 7 Layers      | 4 Layers          |
| Theoretical   | Practical         |
| ISO Standard  | Internet Standard |
| More Detailed | Simpler           |

---

## TCP/IP Mapping

```text
OSI Layer 7
OSI Layer 6
OSI Layer 5
        ↓
Application Layer

OSI Layer 4
        ↓
Transport Layer

OSI Layer 3
        ↓
Internet Layer

OSI Layer 2
OSI Layer 1
        ↓
Network Access Layer
```

---

# 13. Advantages

## Standardized Communication

---

## Vendor Independence

---

## Easy Troubleshooting

---

## Modular Design

---

## Better Learning Framework

---

# 14. Disadvantages

## Complex

7 layers can be difficult to understand.

---

## Mostly Theoretical

Internet primarily uses TCP/IP.

---

## Layer Overlap

Some responsibilities overlap.

---

## Performance Overhead

Strict separation may introduce inefficiencies.

---

# 15. Real-Time Examples

## Example 1: Opening a Website

```text
Browser
 ↓
HTTP
 ↓
TCP
 ↓
IP
 ↓
Ethernet
 ↓
Cable/Wi-Fi
```

---

## Example 2: Sending Email

```text
SMTP
TCP
IP
Ethernet
```

---

## Example 3: Video Streaming

```text
Application
UDP
IP
Wi-Fi
```

---

## Example 4: Online Gaming

```text
Game Client
UDP
IP
Network
```

---

## Example 5: Video Calling

```text
Zoom/Teams
UDP/TCP
IP
Internet
```

---

# 16. Major Project Usage

## Banking Systems

Uses:

```text
HTTPS
TCP
IP
```

for secure communication.

---

## E-Commerce Platforms

Uses:

```text
Application Layer → Web Services
Transport Layer → TCP
Network Layer → IP
```

---

## Cloud Platforms

Uses all layers extensively.

Examples:

* Virtual Networks
* Load Balancers
* Firewalls

---

## Social Media Platforms

Uses:

```text
HTTPS
TCP
IP
Ethernet
```

for billions of requests.

---

# 17. Troubleshooting Using OSI Model

## Example

Cannot access website.

Check:

### Layer 1

Cable connected?

---

### Layer 2

Switch working?

---

### Layer 3

IP address configured?

---

### Layer 4

TCP port open?

---

### Layer 7

HTTP service running?

---

## Benefit

Problem isolated quickly.

---

# 18. Interview Questions

### Q1. What Is the OSI Model?

A 7-layer networking framework.

---

### Q2. How Many Layers Exist?

7 Layers.

---

### Q3. Which Layer Uses IP?

Network Layer.

---

### Q4. Which Layer Uses TCP/UDP?

Transport Layer.

---

### Q5. Which Layer Uses HTTP?

Application Layer.

---

### Q6. Which Device Works at Layer 3?

Router.

---

### Q7. Which Device Works at Layer 2?

Switch.

---

### Q8. Difference Between TCP and UDP?

TCP = Reliable

UDP = Faster

---

# 19. Conclusion

The OSI Model is the foundation of networking concepts and provides a standardized framework for understanding how data travels across networks.

Its seven layers separate networking responsibilities into manageable components, making communication, troubleshooting, and protocol design easier.

The OSI model is widely used for:

* Network Design
* Troubleshooting
* Security Analysis
* Cloud Computing
* System Administration
* Networking Interviews

Even though modern networks use the TCP/IP model in practice, understanding the OSI model is essential for every network engineer, system administrator, cloud engineer, DevOps engineer, and software developer.

### Quick Interview Cheat Sheet

| Layer | Name         | Protocols                   | Devices  |
| ----- | ------------ | --------------------------- | -------- |
| 7     | Application  | HTTP, HTTPS, FTP, DNS       | Gateway  |
| 6     | Presentation | SSL, TLS, JPEG              | Gateway  |
| 5     | Session      | RPC, NetBIOS                | Gateway  |
| 4     | Transport    | TCP, UDP                    | Firewall |
| 3     | Network      | IP, ICMP, OSPF              | Router   |
| 2     | Data Link    | Ethernet, ARP               | Switch   |
| 1     | Physical     | Cable, Fiber, Wi-Fi Signals | Hub      |

### Real-World Request Flow

```text
User opens https://www.google.com

Application Layer  → HTTP/HTTPS
Presentation Layer → SSL/TLS Encryption
Session Layer      → Session Management
Transport Layer    → TCP
Network Layer      → IP Routing
Data Link Layer    → Ethernet/Wi-Fi Frame
Physical Layer     → Bits over Cable/Fiber/Wireless
```

A common networking interview progression is:

**OSI Model → TCP/IP → IP Addressing → Subnetting → TCP vs UDP → DNS → HTTP/HTTPS → Routing → Switching → Firewalls → Load Balancers → Cloud Networking**

Mastering the OSI Model makes all advanced networking topics much easier to understand.
