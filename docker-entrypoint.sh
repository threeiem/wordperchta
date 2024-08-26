#!/bin/sh
set -e

# Python script to install and configure services 
python3 scripts/setup_environment.py

# Execute command passed to docker run (default is manage_sites.py)
exec "$@"
