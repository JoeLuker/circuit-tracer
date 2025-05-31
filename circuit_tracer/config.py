"""Configuration settings for circuit-tracer."""

import os

# Global debug flag for invariance checks
DEBUG_MODE = os.environ.get('CIRCUIT_TRACER_DEBUG', 'false').lower() == 'true'