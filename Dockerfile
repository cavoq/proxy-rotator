FROM mitmproxy/mitmproxy

RUN apt-get update && \
    apt-get install -y tor openssl privoxy && \
    rm -rf /var/lib/apt/lists/*

# Tor configuration
RUN mkdir -p /etc/tor
COPY torrc /etc/tor/torrc
RUN chmod 644 /etc/tor/torrc

# Privoxy configuration
COPY privoxy/config /etc/privoxy/config
RUN chmod 644 /etc/privoxy/config

WORKDIR /proxy-rotator

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY mitmproxy.py .

EXPOSE 8080 8081 8118

CMD ["sh", "-c", "\
    tor & \
    privoxy --no-daemon /etc/privoxy/config & \
    mitmproxy --mode reverse:http://localhost:8118 \
    --scripts mitmproxy.py"]