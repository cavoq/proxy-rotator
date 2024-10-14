#ifndef TOR_PROXY_H
#define TOR_PROXY_H

#include <stdbool.h>

bool tor_connect(const char *host, int port);
void tor_disconnect();
bool tor_request_new_identity();
bool tor_is_connected();
const char *tor_last_error();

#endif // TOR_PROXY_H