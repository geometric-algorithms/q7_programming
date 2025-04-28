#!/bin/bash

while getopts "abc" opt; do
  case ${opt} in
    a )
      echo "Running A/A.py..."
      python A/A.py
      ;;
    b )
      echo "Running B/B.py..."
      python B/B.py
      ;;
    c )
      echo "Running compare.py..."
      python compare.py
      ;;
    \? )
      echo "Usage: ./run.sh [-a] [-b] [-c]"
      exit 1
      ;;
  esac
done
