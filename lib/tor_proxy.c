#include "tor_proxy.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>

#define ERROR_BUFFER_SIZE 256

static int tor_socket = -1;
static char last_error[ERROR_BUFFER_SIZE];

bool tor_connect(const char *host, int port)
{
    struct sockaddr_in server;
    tor_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (tor_socket == -1)
    {
        snprintf(last_error, ERROR_BUFFER_SIZE, "Socket creation failed: %s", strerror(errno));
        return false;
    }

    server.sin_addr.s_addr = inet_addr(host);
    server.sin_family = AF_INET;
    server.sin_port = htons(port);

    if (connect(tor_socket, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        snprintf(last_error, ERROR_BUFFER_SIZE, "Connection to tor failed: %s", strerror(errno));
        close(tor_socket);
        return false;
    }

    return true;
}

bool tor_is_connected()
{
    return tor_socket != -1;
}

void tor_disconnect()
{
    if (tor_socket != -1)
    {
        close(tor_socket);
        tor_socket = -1;
    }
}

bool tor_request_new_identity()
{
    if (tor_socket == -1)
    {
        snprintf(last_error, sizeof(last_error), "Not connected to Tor");
        return false;
    }

    const char *newnym_command = "SIGNAL NEWNYM\n";
    if (send(tor_socket, newnym_command, strlen(newnym_command), 0) < 0)
    {
        snprintf(last_error, sizeof(last_error), "Failed to send SIGNAL NEWNYM: %s", strerror(errno));
        return false;
    }

    char response[256];
    int recv_len = recv(tor_socket, response, sizeof(response) - 1, 0);
    if (recv_len < 0)
    {
        snprintf(last_error, sizeof(last_error), "Failed to receive response from Tor: %s", strerror(errno));
        return false;
    }
    response[recv_len] = '\0';

    // Check if the response starts with "250" (success response code in Tor's control protocol)
    if (strncmp(response, "250", 3) != 0)
    {
        snprintf(last_error, sizeof(last_error), "Failed to request new identity: %s", response);
        return false;
    }

    return true;
}

const char *tor_last_error()
{
    return last_error;
}