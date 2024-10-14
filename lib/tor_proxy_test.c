#include <assert.h>
#include <stdio.h>
#include "tor_proxy.h"

void test_tor_connect()
{
    if (tor_connect("127.0.0.1", 9050) == false)
    {
        printf("[error] tor_connect: %s\n", tor_last_error());
        assert(false);
    }
    else
    {
        printf("[success] tor_connect\n");
    }
}

void test_tor_is_connected()
{
    if (!tor_is_connected())
    {
        printf("[error] tor_is_connected: expected true, got false\n");
        assert(false);
    }
    else
    {
        printf("[success] tor_is_connected\n");
    }
}

void test_tor_request_new_identity()
{
    if (tor_request_new_identity() == false)
    {
        printf("[error] tor_request_new_identity: %s\n", tor_last_error());
        assert(false);
    }
    else
    {
        printf("[success] tor_request_new_identity\n");
    }
}

void test_tor_disconnect()
{
    tor_disconnect();
    if (tor_is_connected())
    {
        printf("[error] tor_disconnect: expected false, got true\n");
        assert(false);
    }
    else
    {
        printf("[success] tor_disconnect\n");
    }
}

int main()
{
    test_tor_connect();
    test_tor_is_connected();
    test_tor_request_new_identity();
    test_tor_disconnect();

    return 0;
}