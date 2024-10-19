import json
import os
from stem import Signal
from stem.control import Controller
from mitmproxy import http
from dotenv import load_dotenv

load_dotenv()

TOR_CONTROL_PORT = os.environ.get("TOR_CONTROL_PORT", 9051)
PRIVOXY_PORT = os.environ.get("PRIVOXY_PORT", 8118)
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

if not all([TOR_CONTROL_PORT, PRIVOXY_PORT, USERNAME, PASSWORD]):
    raise ValueError(
        "Missing environment variables: TOR_CONTROL_PORT, PRIVOXY_PORT, USERNAME, PASSWORD")


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
    auth_header = flow.request.headers.get("Proxy-Authorization")

    if not auth_header:
        json_response = {
            "error": "Proxy Authentication Required",
            "message": "You must provide valid authentication credentials to access this proxy."
        }
        flow.response = http.Response.make(
            407,
            json.dumps(json_response).encode('utf-8'),
            {
                "Content-Type": "application/json",
                "Proxy-Authenticate": 'Basic realm="proxy"'
            }
        )

    method, credentials = auth_header.split(" ", 1)
    if method.lower() == "basic":
        import base64
        decoded = base64.b64decode(credentials).decode("utf-8")
        user, passwd = decoded.split(":", 1)

        if user == USERNAME and passwd == PASSWORD:
            renew_tor_identity()
