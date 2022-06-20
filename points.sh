#!/bin/bash
PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
"${PYTHON_VERSION}"