# proxy-rotator

Modern rotating TOR proxy.

## Usage

**Create a `.env` file:**

```bash
USERNAME=<username>
PASSWORD=<password>
PRIVOXY_PORT=<port>
TOR_PORT=<port>
```

**Build the container:**
```bash
docker build -t proxy-rotator .
```

**Run the container:**

```bash
docker run --env-file .env -it -p 8080:8080 proxy-rotator
```

**Test the proxy:**

```bash
curl -x http://localhost:8080 -U username:password http://httpbin.org/ip
```