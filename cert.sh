#!/bin/bash

CERT_DIR="certs"

openssl req -new -x509 -keyout "$CERT_DIR/mitmproxy.key" \
    -out "$CERT_DIR/mitmproxy.crt" -days 365 -nodes \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=mitmproxy"
