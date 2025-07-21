from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Dict

_logger = logging.getLogger("flumes")
_logger.setLevel(logging.INFO)


def emit(event: str, **data: Any) -> None:
    """Emit a structured event.

    For the MVP this just prints a JSON line to stdout and logs via the
    ``logging`` module.  Down the line we can swap this for OpenTelemetry or
    any other sink.
    """
    payload: Dict[str, Any] = {
        "ts": datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
        "event": event,
        "data": data,
    }

    # Print for immediate visibility
    print(json.dumps(payload, ensure_ascii=False))

    # Also forward to python logging for app-level collection
    _logger.debug(payload)
