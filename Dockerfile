FROM mitmproxy/mitmproxy

RUN apt-get update && \
    apt-get install -y tor privoxy && \
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

EXPOSE 8080 8081 8118 9050

CMD ["sh", "-c", "\
    tor & \
    privoxy /etc/privoxy/config & \
    mitmproxy --mode upstream:http://localhost:8118 \
    --scripts mitmproxy.py"]