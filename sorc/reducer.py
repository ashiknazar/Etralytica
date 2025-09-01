#!/usr/bin/env python3
import sys

current_key = None
count = 0

for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) != 3:
        continue

    key_type, key_value, value = parts
    value = int(value)

    full_key = f"{key_type}|{key_value}"

    if current_key == full_key:
        count += value
    else:
        if current_key is not None:
            kt, kv = current_key.split("|")
            print(f"{kt}\t{kv}\t{count}")
        current_key = full_key
        count = value

# Flush last key
if current_key is not None:
    kt, kv = current_key.split("|")
    print(f"{kt}\t{kv}\t{count}")
