# GKS Synthetic Patient Generator

Generate reproducible synthetic patient records from real-world genomic
knowledge using GA4GH Genomic Knowledge Standards (GKS).

## Project status

This repository contains an early pilot developed during DBCLS BioHackathon
2026 and Togothon 168. The current vertical slice accepts a curated, precisely defined allele
record, constructs a Cat-VRS `CategoricalVariant`, and writes two deliberately
separate artifacts:

- a synthetic patient record containing observable variant information; and
- a private answer key containing source-derived annotations for evaluation.

The included fixture exercises the pipeline using an allele published in the
official Cat-VRS examples. It tests the pipeline mechanics and is not itself a
clinical benchmark case.

## Design principles

- Source records and database releases are versioned and retained as provenance.
- HGVS expressions, coordinates, reference bases, and GA4GH digests are never
  repaired or invented by the pipeline.
- Multiple or ambiguous normalization results are rejected for review.
- A ClinGen Allele Registry identifier (CAID) may identify the categorical
  variant without requiring additional Cat-VRS members.
- Patient inputs and gold-standard annotations are written to separate files.
- Rejected records receive explicit, machine-readable reason codes.

## Quick start

Python 3.10 or later is required.

```bash
python -m pip install -e .
gks-synthetic build-pilot \
  --input examples/input/official_catvrs_example.json \
  --output-dir outputs/pilot \
  --seed 20260925
```

The command creates:

```text
outputs/pilot/
├── patient.json
├── answer-key.json
└── run-manifest.json
```

Validate an input without producing output:

```bash
gks-synthetic validate-candidate \
  examples/input/official_catvrs_example.json
```

Run the tests without installing development dependencies:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Planned source adapters

1. **ClinVar-GKM:** consume precomputed VRS, Cat-VRS, and VA-Spec records as a
   high-confidence baseline.
2. **CIViC:** initially select accepted, editor-reviewed, simple allele records
   with a precise CAID or normalized VRS allele. Broader categories, copy-number
   changes, fusions, and complex molecular profiles will enter through explicit
   later phases.

Both adapters will emit the same internal candidate format so patient assembly,
gold-answer construction, validation, and evaluation remain source-independent.

## Repository layout

```text
config/                         Reproducible run configuration
data/                           Local upstream and derived data (not committed)
examples/input/                 Small, inspectable input fixtures
examples/output/                Committed demonstration outputs
src/gks_synthetic_patient/      Pipeline package
tests/                          Unit tests and rejection cases
```

## Data and licensing

The project code is licensed under Apache License 2.0. Upstream datasets and
records retain their original licenses and terms; see [data/README.md](data/README.md).

## Safety and scope

Generated records are synthetic and intended for research, interoperability
testing, and benchmark development. They must not be represented as real
patients or used for clinical decision-making.
