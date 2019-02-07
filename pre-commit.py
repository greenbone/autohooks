#!/usr/bin/env python3

import sys

try:
    from autohooks.precommit import run
    sys.exit(run())
except ImportError:
    print('autohooks not installed. Ignoring pre-commit hook.')
    sys.exit(0)

