from stem import Signal
from stem.control import Controller
from mitmproxy import http

TOR_CONTROL_PORT = 9051
PRIVOXY_PORT = 8118


def renew_tor_identity():
    """Requests a new Tor identity to rotate IP address."""
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
    except Exception as e:
        print(f"Error renewing Tor identity: {e}")


def request(flow: http.HTTPFlow):
    """Called for each HTTP request passing through mitmproxy."""
    renew_tor_identity()
    #flow.request.proxy = f"http://127.0.0.1:{PRIVOXY_PORT}"
