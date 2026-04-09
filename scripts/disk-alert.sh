#!/bin/bash

THRESHOLD=80
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')

echo "Current disk usage: $DISK_USAGE%"

if [ "$DISK_USAGE" -gt "$THRESHOLD" ]; then
    echo "WARNING: Disk usage is above $THRESHOLD%! Take action now."
else
    echo "OK: Disk usage is under control."
fi
