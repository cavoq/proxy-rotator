import json
import os
from time import time
from base64 import b64decode

from stem import Signal
from stem.control import Controller
from mitmproxy import http
from dotenv import load_dotenv

load_dotenv()

TOR_CONTROL_PORT = os.environ.get("TOR_CONTROL_PORT", 9051)
PRIVOXY_PORT = os.environ.get("PRIVOXY_PORT", 8118)
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
RENEWAL_INTERVAL = os.environ.get("RENEWAL_INTERVAL", 30)

last_renewal_time = 0


if not all([TOR_CONTROL_PORT, PRIVOXY_PORT, USERNAME, PASSWORD]):
    raise ValueError(
        "Missing environment variables, please check the .env file.")


def renew_tor_identity():
    """Requests a new Tor identity to rotate IP address."""
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
    except Exception as e:
        print(f"Error renewing Tor identity: {e}")


def should_renew(current_time: float) -> bool:
    """Determines if the Tor identity should be renewed based on the elapsed time."""
    global last_renewal_time
    if current_time - last_renewal_time >= RENEWAL_INTERVAL:
        last_renewal_time = current_time
        return True
    return False


def request(flow: http.HTTPFlow):
    """Called for each HTTP request passing through mitmproxy."""
    auth_header = flow.request.headers.get("Proxy-Authorization")

    if not auth_header:
        json_response = {
            "error": "Proxy Authentication Required.",
            "message": "You must provide valid authentication credentials to access this proxy."
        }
        flow.response = http.Response.make(
            407,
            json.dumps(json_response).encode('utf-8'),
            {
                "Content-Type": "application/json",
                "Content-Length": str(len(json.dumps(json_response))),
                "Proxy-Authenticate": 'Basic realm="proxy"',
                "Connection": "close"
            }
        )
        return

    method, credentials = auth_header.split(" ", 1)
    if method.lower() == "basic":
        decoded = b64decode(credentials).decode("utf-8")
        user, passwd = decoded.split(":", 1)

        if user == USERNAME and passwd == PASSWORD:
            current_time = time()
            if should_renew(current_time):
                renew_tor_identity()
