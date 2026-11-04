#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "layers.h"

static int add_header(char *data, int size, const char *header) {
    char temp[MAX_PACKET];
    int n = snprintf(temp, sizeof(temp), "%s{%s}", header, data);
    if (n < 0 || n >= size) return 0;
    strcpy(data, temp);
    return 1;
}
static int remove_header(char *data, const char *header) {
    size_t h = strlen(header);
    if (strncmp(data, header, h) != 0 || data[h] != '{') return 0;
    size_t len = strlen(data);
    if (len <= h + 1 || data[len - 1] != '}') return 0;
    memmove(data, data + h + 1, len - h - 2);
    data[len - h - 2] = '\0';
    return 1;
}

/* Sender encapsulation: Application (7) down to Physical (1). */
void OSI_Encapsulate(const char *message, char *packet, int packet_size) {
    snprintf(packet, packet_size, "%s", message);
    printf("[L7 Application] User data created: %s\n", message);

    /* L6 Presentation: hexadecimal representation of message bytes. */
    char encoded[MAX_PACKET] = {0};
    size_t len = strlen(packet);
    if (len * 2 + 1 >= sizeof(encoded)) { packet[0] = '\0'; return; }
    for (size_t i = 0; i < len; ++i)
        snprintf(encoded + i * 2, 3, "%02X", (unsigned char)packet[i]);
    strcpy(packet, encoded);
    printf("[L6 Presentation] Data encoded as hexadecimal.\n");

    if (!add_header(packet, packet_size, "SESSION:OSI-DEMO")) { packet[0]='\0'; return; }
    printf("[L5 Session] Session ID added.\n");
    if (!add_header(packet, packet_size, "TCP:SEGMENT")) { packet[0]='\0'; return; }
    printf("[L4 Transport] TCP segment marker added.\n");
    if (!add_header(packet, packet_size, "IP:127.0.0.1>127.0.0.1")) { packet[0]='\0'; return; }
    printf("[L3 Network] Source and destination IP marker added.\n");
    if (!add_header(packet, packet_size, "ETH:FRAME:CHECK")) { packet[0]='\0'; return; }
    printf("[L2 Data Link] Ethernet-style frame marker added.\n");
    printf("[L1 Physical] Frame converted to a bit-transmission stage.\n");
}

/* Receiver decapsulation: Physical (1) up to Application (7). */
int OSI_Decapsulate(const char *packet, char *message, int message_size) {
    char data[MAX_PACKET];
    snprintf(data, sizeof(data), "%s", packet);
    printf("[L1 Physical] Bits/frame received from TCP socket.\n");
    if (!remove_header(data, "ETH:FRAME:CHECK")) return 0;
    printf("[L2 Data Link] Frame marker and check field validated.\n");
    if (!remove_header(data, "IP:127.0.0.1>127.0.0.1")) return 0;
    printf("[L3 Network] Logical IP marker checked.\n");
    if (!remove_header(data, "TCP:SEGMENT")) return 0;
    printf("[L4 Transport] TCP segment marker processed.\n");
    if (!remove_header(data, "SESSION:OSI-DEMO")) return 0;
    printf("[L5 Session] Session identifier validated.\n");

    /* Presentation decoding. */
    size_t hex_len = strlen(data);
    if (hex_len % 2 || hex_len / 2 >= (size_t)message_size) return 0;
    for (size_t i = 0; i < hex_len; i += 2) {
        char byte[3] = {data[i], data[i+1], '\0'};
        char *end = NULL;
        long value = strtol(byte, &end, 16);
        if (!end || *end) return 0;
        message[i/2] = (char)value;
    }
    message[hex_len/2] = '\0';
    printf("[L6 Presentation] Hexadecimal data decoded.\n");
    printf("[L7 Application] Original user message delivered.\n");
    return 1;
}
