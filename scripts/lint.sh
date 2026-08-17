#!/usr/bin/env bash
set -euo pipefail
PYTHONPATH=packages python3 -m ruff check packages services tests scripts
