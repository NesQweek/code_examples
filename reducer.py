#!/usr/bin/python3
import sys

track_counts = {}

for line in sys.stdin:
    line = line.strip()
    track_id, count = line.split('\t')
    track_counts[track_id] = track_counts.get(track_id, 0) + int(count)

for track_id, count in track_counts.items():
    print(f'{track_id}\t{count}')