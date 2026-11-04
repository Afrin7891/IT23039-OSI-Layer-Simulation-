CC = gcc
CFLAGS = -Wall -Wextra -std=c11
ifeq ($(OS),Windows_NT)
    SOCKET_LIBS = -lws2_32
    EXE = .exe
else
    SOCKET_LIBS =
    EXE =
endif

all: osi_client$(EXE) osi_server$(EXE)

osi_client$(EXE): client.c layers.c layers.h
	$(CC) $(CFLAGS) -o $@ client.c layers.c $(SOCKET_LIBS)

osi_server$(EXE): server.c layers.c layers.h
	$(CC) $(CFLAGS) -o $@ server.c layers.c $(SOCKET_LIBS)

clean:
	rm -f osi_client osi_server osi_client.exe osi_server.exe *.o
.PHONY: all clean
