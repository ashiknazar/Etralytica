#!/usr/bin/env python3
import sys

current_key = None
count = 0

for raw in sys.stdin:
    line = raw.strip()
    if not line:
        continue
    try:
        key, val = line.split("\t", 1)
        val = int(val)
    except ValueError:
        continue

    if current_key == key:
        count += val
    else:
        if current_key is not None:
            print(f"{current_key}\t{count}")
        current_key = key
        count = val

# flush
if current_key is not None:
    print(f"{current_key}\t{count}")
