"""Application-wide configuration values."""

import os

# Capture the process's launch directory so file tools operate on the project
# the user invoked iagent from, rather than the location of this package.
WORKING_DIRECTORY = os.getcwd()
MAX_CHARS = 10_000
MAX_ITERATIONS = 20
