"""End-to-end pilot orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .builders import build_records
from .io import read_json, write_json
from .validation import validate_candidate


def run_pilot(input_path: Path, output_dir: Path, seed: int) -> dict[str, Any]:
    candidate = read_json(input_path)
    validate_candidate(candidate)
    patient, answer_key = build_records(candidate, seed)

    manifest = {
        "pipelineVersion": "0.1.0",
        "seed": seed,
        "input": input_path.name,
        "source": candidate["source"],
        "selectionProfile": "precise-simple-alleles",
        "counts": {"accepted": 1, "rejected": 0, "patients": 1, "observations": 1},
        "outputs": {
            "patient": "patient.json",
            "answerKey": "answer-key.json",
        },
    }

    write_json(output_dir / "patient.json", patient)
    write_json(output_dir / "answer-key.json", answer_key)
    write_json(output_dir / "run-manifest.json", manifest)
    return manifest
