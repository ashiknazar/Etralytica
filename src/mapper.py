#!/usr/bin/env python3
import sys
import re

# Example line:
# 192.168.0.12 - - [28/Aug/2025:12:03:11 +0000] "GET /index.html HTTP/1.1" 200 5321
LOG_RE = re.compile(
    r'(?P<ip>\S+) - - \[(?P<time>[^\]]+)\] "GET (?P<url>\S+) HTTP/1\.1" (?P<code>\d{3}) (?P<size>\d+)'
)

for line in sys.stdin:
    m = LOG_RE.match(line.strip())
    if not m:
        continue
    code = m.group("code")  # "200", "404", "500", ...
    # Emit <key, 1>. For this job the key is the status code.
    print(f"{code}\t1")
