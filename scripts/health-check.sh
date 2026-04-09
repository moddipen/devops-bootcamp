#!/bin/bash

echo "===== SERVER HEALTH REPORT ====="
echo "Date: $(date)"
echo ""

echo "--- CPU Cores ---"
nproc

echo ""
echo "--- Memory Usage ---"
free -h

echo ""
echo "--- Disk Usage ---"
df -h /

echo ""
echo "--- Top 5 Processes by CPU ---"
ps aux --sort=-%cpu | head -6

echo ""
echo "===== END OF REPORT ====="
