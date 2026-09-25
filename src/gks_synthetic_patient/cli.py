"""Command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .errors import CandidateRejected
from .io import read_json
from .pipeline import run_pilot
from .validation import validate_candidate


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gks-synthetic")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser(
        "validate-candidate", help="validate one pilot candidate JSON file"
    )
    validate.add_argument("input", type=Path)

    build = subparsers.add_parser(
        "build-pilot", help="generate one patient and a separate answer key"
    )
    build.add_argument("--input", required=True, type=Path)
    build.add_argument("--output-dir", required=True, type=Path)
    build.add_argument("--seed", required=True, type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "validate-candidate":
            validate_candidate(read_json(args.input))
            print(json.dumps({"status": "accepted", "input": str(args.input)}))
            return 0

        manifest = run_pilot(args.input, args.output_dir, args.seed)
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return 0
    except CandidateRejected as error:
        print(
            json.dumps(
                {"status": "rejected", "code": error.code, "message": error.message}
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
