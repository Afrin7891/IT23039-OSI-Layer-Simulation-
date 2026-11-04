#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
typedef SOCKET socket_t;
#define CLOSESOCKET closesocket
#define SOCKET_ERROR_CODE WSAGetLastError()
#else
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
typedef int socket_t;
#define INVALID_SOCKET (-1)
#define SOCKET_ERROR (-1)
#define CLOSESOCKET close
#define SOCKET_ERROR_CODE 0
#endif
#include <stdio.h>
#include <string.h>
#include "layers.h"
#define PORT 50555

int main(void) {
#ifdef _WIN32
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2,2), &wsa) != 0) { puts("Winsock startup failed"); return 1; }
#endif
    socket_t listener = socket(AF_INET, SOCK_STREAM, 0);
    if (listener == INVALID_SOCKET) { puts("Socket creation failed"); return 1; }
#ifndef _WIN32
    int yes = 1;
    setsockopt(listener, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes));
#endif
    struct sockaddr_in address;
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    address.sin_port = htons(PORT);

    if (bind(listener, (struct sockaddr *)&address, sizeof(address)) == SOCKET_ERROR ||
        listen(listener, 1) == SOCKET_ERROR) {
        printf("Bind/listen failed (error %d). Port %d may be busy.\n", SOCKET_ERROR_CODE, PORT);
        CLOSESOCKET(listener);
#ifdef _WIN32
        WSACleanup();
#endif
        return 1;
    }
    printf("[SERVER] Listening on 127.0.0.1:%d\n", PORT);
    fflush(stdout);

    socket_t client = accept(listener, NULL, NULL);
    if (client == INVALID_SOCKET) {
        puts("Accept failed"); CLOSESOCKET(listener); return 1;
    }

    char packet[MAX_PACKET] = {0};
    int total = 0, n;
    while ((n = recv(client, packet + total, (int)sizeof(packet) - total - 1, 0)) > 0) {
        total += n;
        if (total >= (int)sizeof(packet) - 1) break;
    }
    packet[total] = '\0';
    printf("\n[SERVER] Received %d bytes using a real TCP socket.\n", total);
    printf("[SERVER] Encapsulated packet: %s\n", packet);

    char message[MAX_MESSAGE] = {0};
    puts("\n========== RECEIVER: DECAPSULATION ==========");
    if (total > 0 && OSI_Decapsulate(packet, message, sizeof(message))) {
        printf("\n[SERVER] FINAL MESSAGE: %s\n", message);
        const char ack[] = "ACK: Message received successfully";
        send(client, ack, (int)strlen(ack), 0);
    } else {
        puts("[SERVER] ERROR: Invalid or incomplete packet.");
    }

    CLOSESOCKET(client);
    CLOSESOCKET(listener);
#ifdef _WIN32
    WSACleanup();
#endif
    return total > 0 ? 0 : 1;
}
