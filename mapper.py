#!/usr/bin/python3
import sys

for line in sys.stdin:
    line = line.strip()
    parts = line.split(',')
    track_id = parts[3]
    count = 1
    print(f'{track_id}\t{count}')