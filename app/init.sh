#!/bin/bash

set -euo pipefail

# Import user interests
PYTHONPATH=$PWD /app/.venv/bin/python app/core/scripts/user_interest/importer.py
