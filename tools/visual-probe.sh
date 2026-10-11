#!/usr/bin/env bash
# Визуальный регресс в headless Chrome: overflow на 1440/1024/768/640,
# контракты адаптива (рельс <=1024, медиа <=768) и prefers-reduced-motion.
# Зависимости: google-chrome; CDP-драйвер голый — python3 stdlib + websocket-хендшейк.
# Использование:
#   ./tools/visual-probe.sh                # локальный dev-сервер (должен быть запущен)
#   ./tools/visual-probe.sh https://kislyakov.pro
set -u

BASE="${1:-http://127.0.0.1:8000}"
CHROME="${CHROME:-google-chrome}"
PORT="${PROBE_PORT:-9223}"
TMP="$(mktemp -d)"
CHROME_PID=""

cleanup() {
    [ -n "$CHROME_PID" ] && kill "$CHROME_PID" 2>/dev/null
    rm -rf "$TMP"
}
trap cleanup EXIT

command -v "$CHROME" >/dev/null 2>&1 || {
    echo "FAIL  google-chrome не найден (переопределить: CHROME=chromium ...)"; exit 1
}

# --- chrome headless с CDP на localhost:PORT ---
"$CHROME" --headless=new --disable-gpu --remote-debugging-port="$PORT" \
    --user-data-dir="$TMP" --no-first-run --no-default-browser-check \
    --disable-background-networking --disable-extensions about:blank \
    >/dev/null 2>&1 &
CHROME_PID=$!

for _ in $(seq 1 40); do
    curl -fsS --max-time 2 -o /dev/null "http://127.0.0.1:$PORT/json/version" 2>/dev/null && break
    sleep 0.25
done
curl -fsS --max-time 2 -o /dev/null "http://127.0.0.1:$PORT/json/version" 2>/dev/null || {
    echo "FAIL  chrome не поднял CDP (порт занят? PROBE_PORT=9333 ./tools/visual-probe.sh)"; exit 1
}

PYOUT="$(python3 - "$BASE" "$PORT" <<'PY'
import base64, json, os, socket, struct, sys, time, urllib.parse, urllib.request

BASE, PORT = sys.argv[1], sys.argv[2]

def http_json(method, path):
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", method=method)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode() or "null")

# --- минимальный websocket (stdlib), как требует zero-dep политика ---
def ws_connect(host, port, path):
    s = socket.create_connection((host, port), timeout=30)
    key = base64.b64encode(os.urandom(16)).decode()
    req = (f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\n"
           f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
    s.sendall(req.encode())
    resp = b""
    while b"\r\n\r\n" not in resp:
        part = s.recv(4096)
        if not part:
            raise ConnectionError("ws handshake: connection closed")
        resp += part
    if b"101" not in resp.split(b"\r\n", 1)[0]:
        raise ConnectionError(f"ws handshake failed: {resp[:120]!r}")
    return s

def _recv_exact(s, n):
    buf = b""
    while len(buf) < n:
        part = s.recv(n - len(buf))
        if not part:
            raise ConnectionError("ws socket closed")
        buf += part
    return buf

def ws_send(s, obj):
    payload = json.dumps(obj).encode("utf-8")
    n = len(payload)
    head = bytearray([0x81])  # FIN + text
    mask = os.urandom(4)
    if n < 126:
        head.append(0x80 | n)
    elif n < 65536:
        head.append(0x80 | 126); head += struct.pack(">H", n)
    else:
        head.append(0x80 | 127); head += struct.pack(">Q", n)
    masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    s.sendall(bytes(head) + mask + masked)

def ws_recv(s):
    msg = b""
    while True:
        h = _recv_exact(s, 2)
        fin = h[0] & 0x80
        op = h[0] & 0x0F
        masked = h[1] & 0x80
        n = h[1] & 0x7F
        if n == 126:
            n = struct.unpack(">H", _recv_exact(s, 2))[0]
        elif n == 127:
            n = struct.unpack(">Q", _recv_exact(s, 8))[0]
        key = _recv_exact(s, 4) if masked else None
        data = _recv_exact(s, n)
        if key:
            data = bytes(b ^ key[i % 4] for i, b in enumerate(data))
        if op == 8:
            raise ConnectionError("ws closed by peer")
        if op == 9:  # ping -> pong
            pong = bytearray([0x8A, 0x80 | n])
            s.sendall(bytes(pong) + data)
            continue
        if op in (1, 0):
            msg += data
            if fin:
                return json.loads(msg.decode("utf-8"))

class CDP:
    def __init__(self, s):
        self.s = s
        self._id = 0
    def call(self, method, params=None, wait=30):
        self._id += 1
        mid = self._id
        ws_send(self.s, {"id": mid, "method": method, "params": params or {}})
        deadline = time.time() + wait
        while time.time() < deadline:
            msg = ws_recv(self.s)
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
        raise TimeoutError(method)

def evaluate(cdp, expr):
    res = cdp.call("Runtime.evaluate", {
        "expression": expr, "returnByValue": True, "awaitPromise": True})
    if "exceptionDetails" in res:
        raise RuntimeError(f"evaluate exception: {res['exceptionDetails']}")
    return res["result"].get("value")

# --- контракты адаптива (зеркалят AGENTS ## Project overview) ---
PAGE_JS = r"""
(() => {
    const vw = window.innerWidth;
    const doc = document.documentElement;
    const hidden = sel => {
        const el = document.querySelector(sel);
        return !el || getComputedStyle(el).display === 'none'
            || getComputedStyle(el).visibility === 'hidden';
    };
    let marquee = null;
    document.querySelectorAll('.marquee').forEach(m => {
        const name = getComputedStyle(m).animationName;
        if (name && name !== 'none') marquee = name;
    });
    return {
        overflow: doc.scrollWidth - vw,
        railHidden: hidden('.hero-timeline'),
        marqueeAnimated: !!marquee,
    };
})()
"""
MEDIA_JS = r"""
(() => {
    const el = document.querySelector('.portfolio-preview-media');
    if (!el) return { mediaPresent: false, mediaHidden: true };
    const cs = getComputedStyle(el);
    return {
        mediaPresent: true,
        mediaHidden: cs.display === 'none' || cs.visibility === 'hidden',
    };
})()
"""

passes = fails = 0
def check(cond, label):
    global passes, fails
    if cond:
        passes += 1
        print("PASS  " + label)
    else:
        fails += 1
        print("FAIL  " + label)

try:
    target = http_json("PUT", "/json/new?" + urllib.parse.quote(BASE, safe=""))
except Exception as e:
    print(f"FAIL  создать CDP-target: {e}")
    print(f"# counts: {passes} {fails + 1}"); sys.exit(0)

ws_path = urllib.parse.urlparse(target["webSocketDebuggerUrl"]).path
conn = ws_connect("127.0.0.1", int(PORT), ws_path)
cdp = CDP(conn)
for domain in ("Page", "Runtime", "Emulation"):
    try:
        cdp.call(f"{domain}.enable")
    except Exception:
        pass

def wait(expr, tries=80):
    for _ in range(tries):
        try:
            if evaluate(cdp, expr):
                return True
        except Exception:
            pass
        time.sleep(0.25)
    return False

def navigate(reduced):
    cdp.call("Emulation.setEmulatedMedia", {
        "features": [{"name": "prefers-reduced-motion",
                      "value": "reduce" if reduced else "no-preference"}]})
    cdp.call("Page.navigate", {"url": BASE + "/"})
    wait("document.readyState === 'complete'", tries=60)
    time.sleep(1.2)  # дать reveal-анимации устояться (иначе транзиент -10px)

def open_portfolio():
    # карточки рендерятся только при открытии панели (disclosure)
    evaluate(cdp, "document.getElementById('portfolio-btn').click()")
    wait("!!document.querySelector('.portfolio-layout')")
    time.sleep(1.2)

cases = [
    (1440, False, "1440px", [
        (lambda r: r["overflow"] <= 0, "нет горизонтального переполнения"),
        (lambda r: not r["railHidden"], "таймлайн-рельс виден"),
        (lambda r: not r["mediaHidden"], "медиа-превью карточек видно"),
    ]),
    (1024, False, "1024px", [
        (lambda r: r["overflow"] <= 0, "нет горизонтального переполнения"),
        (lambda r: r["railHidden"], "таймлайн-рельс скрыт (<=1024)"),
        (lambda r: not r["mediaHidden"], "медиа-превью видно"),
    ]),
    (768, False, "768px", [
        (lambda r: r["overflow"] <= 0, "нет горизонтального переполнения"),
        (lambda r: r["railHidden"], "таймлайн-рельс скрыт"),
        (lambda r: r["mediaHidden"], "медиа-превью скрыто (<=768)"),
    ]),
    (640, False, "640px", [
        (lambda r: r["overflow"] <= 0, "нет горизонтального переполнения"),
        (lambda r: r["railHidden"], "таймлайн-рельс скрыт"),
        (lambda r: r["mediaHidden"], "медиа-превью скрыто"),
    ]),
    (1440, True, "reduced-motion", [
        (lambda r: r["overflow"] <= 0, "нет горизонтального переполнения"),
        (lambda r: not r["marqueeAnimated"], "marquee без анимации"),
    ]),
]

for width, reduced, label, checks in cases:
    cdp.call("Emulation.setDeviceMetricsOverride", {
        "width": width, "height": 900, "deviceScaleFactor": 1, "mobile": False})
    try:
        navigate(reduced)
        page = evaluate(cdp, PAGE_JS)
        if not reduced:
            open_portfolio()
            media = evaluate(cdp, MEDIA_JS)
            page.update(media)
    except Exception as e:
        for _cond, text in checks:
            check(False, f"{label}: {text} (не удалось проверить: {e})")
        continue
    for cond, text in checks:
        check(cond(page), f"{label}: {text}")

print(f"# counts: {passes} {fails}")
PY
)"
printf '%s\n' "$PYOUT" | sed '/^# counts:/d'
COUNTS="$(printf '%s\n' "$PYOUT" | sed -n 's/^# counts: //p')"
COUNTS="${COUNTS:-0 0}"

echo ""
echo "Итого: ${COUNTS%% *} ок, ${COUNTS##* } ошибок (BASE=$BASE)"
[ "${COUNTS##* }" -eq 0 ]