#!/usr/bin/env python3
import sys
import re
from datetime import datetime

# Regex for parsing logs
LOG_RE = re.compile(
    r'(?P<ip>\S+) - - \[(?P<time>[^\]]+)\] "GET (?P<url>\S+) HTTP/1\.1" (?P<code>\d{3}) (?P<size>\d+)'
)

for line in sys.stdin:
    m = LOG_RE.match(line.strip())
    if not m:
        continue

    ip = m.group("ip")
    url = m.group("url")
    code = m.group("code")
    timestamp = m.group("time")
    hour = datetime.strptime(timestamp.split()[0], "%d/%b/%Y:%H:%M:%S").hour

    # Total requests per status code
    print(f"STATUS\t{code}\t1")

    # Top visitors
    print(f"VISITOR\t{ip}\t1")

    # Most visited pages
    print(f"URL\t{url}\t1")

    # Internship page interest
    if url.startswith("/internships/"):
        print(f"INTERNSHIP\t{url}\t1")

    # Error analysis
    if code in ("404", "500"):
        print(f"ERROR\t{url}\t1")

    # Peak traffic hours
    print(f"HOUR\t{hour}\t1")
