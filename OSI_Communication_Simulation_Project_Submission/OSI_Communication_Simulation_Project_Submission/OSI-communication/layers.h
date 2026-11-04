#ifndef LAYERS_H
#define LAYERS_H
#define MAX_PACKET 8192
#define MAX_MESSAGE 1024
void OSI_Encapsulate(const char *message, char *packet, int packet_size);
int OSI_Decapsulate(const char *packet, char *message, int message_size);
#endif
