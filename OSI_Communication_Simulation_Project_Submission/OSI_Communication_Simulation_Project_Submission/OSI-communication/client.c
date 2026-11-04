#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
typedef SOCKET socket_t;
#define CLOSESOCKET closesocket
#else
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
typedef int socket_t;
#define INVALID_SOCKET (-1)
#define SOCKET_ERROR (-1)
#define CLOSESOCKET close
#endif
#include <stdio.h>
#include <string.h>
#include "layers.h"
#define PORT 50555

int main(int argc, char **argv) {
    const char *message = argc > 1 ? argv[1] : "Hello from the OSI communication project!";
    if (!*message || strlen(message) > 500) {
        puts("Message must contain 1-500 characters."); return 1;
    }
#ifdef _WIN32
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2,2), &wsa) != 0) { puts("Winsock startup failed"); return 1; }
#endif
    char packet[MAX_PACKET] = {0};
    puts("========== SENDER: ENCAPSULATION ==========");
    OSI_Encapsulate(message, packet, sizeof(packet));
    if (!packet[0]) { puts("Encapsulation failed."); return 1; }
    printf("\n[CLIENT] Encapsulated packet: %s\n", packet);

    socket_t sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) { puts("Socket creation failed"); return 1; }
    struct sockaddr_in server;
    memset(&server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);
    server.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) == SOCKET_ERROR) {
        puts("Connection failed. Start the server/visualizer first.");
        CLOSESOCKET(sock); return 1;
    }

    size_t sent = 0, length = strlen(packet);
    while (sent < length) {
        int count = send(sock, packet + sent, (int)(length - sent), 0);
        if (count <= 0) { puts("Send failed"); CLOSESOCKET(sock); return 1; }
        sent += (size_t)count;
    }
#ifdef _WIN32
    shutdown(sock, SD_SEND);
#else
    shutdown(sock, SHUT_WR);
#endif
    char reply[256] = {0};
    int n = recv(sock, reply, sizeof(reply)-1, 0);
    if (n > 0) { reply[n] = '\0'; printf("[CLIENT] Server response: %s\n", reply); }
    CLOSESOCKET(sock);
#ifdef _WIN32
    WSACleanup();
#endif
    return 0;
}
