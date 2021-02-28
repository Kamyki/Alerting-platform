#!/bin/bash

echo "Check config"
if [[ `cat /app/services.yaml` == `cat /app/current_services.yaml` ]]; then
  echo "No status changed. Skipping"
else
  echo "Change detected, reload"
  cat /app/services.yaml > /app/current_services.yaml
  cd /app
  python3 ./primer.py
fi
