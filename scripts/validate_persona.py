"""Validate one managed or explicit external persona directory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from persona_runtime_contracts import persona_directory_errors, resolve_persona_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("persona_id")
    parser.add_argument("--persona-dir", type=Path, help="Explicit external directory; omit for managed resolution")
    args = parser.parse_args()
    try:
        directory = resolve_persona_dir(args.persona_id, args.persona_dir)
        errors = persona_directory_errors(directory, args.persona_id)
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
        directory = args.persona_dir
    print(json.dumps({"valid": not errors, "persona_dir": str(directory) if directory else None, "errors": errors}, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
