from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from gks_synthetic_patient.builders import build_catvar, build_records
from gks_synthetic_patient.errors import CandidateRejected
from gks_synthetic_patient.pipeline import run_pilot
from gks_synthetic_patient.validation import validate_candidate


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "input" / "official_catvrs_example.json"


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class CandidateValidationTests(unittest.TestCase):
    def test_official_fixture_is_accepted(self) -> None:
        validate_candidate(load_fixture())

    def test_ambiguous_normalization_is_rejected(self) -> None:
        candidate = load_fixture()
        candidate["ambiguous_normalizer_result"] = True
        with self.assertRaisesRegex(CandidateRejected, "AMBIGUOUS_NORMALIZATION"):
            validate_candidate(candidate)

    def test_digest_mismatch_is_rejected(self) -> None:
        candidate = load_fixture()
        candidate["defining_allele"]["digest"] = "not-the-id-suffix"
        with self.assertRaisesRegex(CandidateRejected, "VRS_DIGEST_MISMATCH"):
            validate_candidate(candidate)


class BuilderTests(unittest.TestCase):
    def test_catvar_uses_supplied_allele_without_members(self) -> None:
        candidate = load_fixture()
        original_allele = copy.deepcopy(candidate["defining_allele"])
        catvar = build_catvar(candidate)
        self.assertEqual(catvar["constraints"][0]["allele"], original_allele)
        self.assertNotIn("members", catvar)
        self.assertEqual(catvar["mappings"][0]["coding"]["code"], "CA415424538")

    def test_patient_and_answer_key_join_by_observation_id(self) -> None:
        patient, answer_key = build_records(load_fixture(), seed=42)
        observation_id = patient["observations"][0]["id"]
        self.assertEqual(answer_key["answers"][0]["observationId"], observation_id)
        self.assertNotIn("sourceAnnotations", patient["observations"][0])

    def test_generation_is_deterministic_for_same_seed(self) -> None:
        first = build_records(load_fixture(), seed=42)
        second = build_records(load_fixture(), seed=42)
        self.assertEqual(first, second)

    def test_pipeline_writes_three_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            manifest = run_pilot(FIXTURE, output, seed=42)
            self.assertEqual(manifest["counts"]["accepted"], 1)
            self.assertEqual(
                {path.name for path in output.iterdir()},
                {"patient.json", "answer-key.json", "run-manifest.json"},
            )


if __name__ == "__main__":
    unittest.main()
