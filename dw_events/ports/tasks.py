"""Task interfaces — re-exported from dw-core, their one true home.

This module used to DUPLICATE dw-core's callback interfaces, which
made issubclass/isinstance checks fail across the seam whenever a
task implemented one copy and a consumer checked the other. The
duplicates are gone; imports from here keep working.
"""
from dw_core.ports import (
    TaskETACallback,
    TaskETAListenerInterface,
    TaskProgressCallback,
    TaskProgressListenerInterface,
)

__all__ = [
    'TaskProgressCallback',
    'TaskETACallback',
    'TaskProgressListenerInterface',
    'TaskETAListenerInterface',
]
