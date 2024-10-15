#!/bin/bash

CERT_DIR="certs"

openssl req -new -x509 -keyout "$CERT_DIR/proxy-rotator.key" \
    -out "$CERT_DIR/proxy-rotator.crt" -days 365 -nodes \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=mitmproxy"

cat "$CERT_DIR/proxy-rotator.key" "$CERT_DIR/proxy-rotator.crt" > "$CERT_DIR/proxy-rotator.pem"