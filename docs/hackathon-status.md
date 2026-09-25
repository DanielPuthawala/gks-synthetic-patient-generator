# BioHackathon 2026 status

## Goal

Build a reproducible pipeline that turns public genomic knowledge into synthetic
patient records for evaluating variant annotation and evidence-retrieval systems.

## Working vertical slice

The repository now demonstrates:

1. deterministic admission of a precisely defined allele candidate;
2. rejection of ambiguous or internally inconsistent inputs with reason codes;
3. construction of a Cat-VRS `CategoricalVariant` around a supplied VRS Allele;
4. use of a CAID at the categorical-variant layer without inventing members;
5. deterministic creation of a synthetic patient observation;
6. separation of patient-visible data from the evaluation answer key; and
7. capture of source release, record, configuration, and random seed provenance.

The example VRS identifiers and digests come from the official Cat-VRS
documentation. The pipeline verifies their internal consistency but does not
calculate, alter, or repair them.

## Current boundary

The pilot accepts canonical categories defined by one simple VRS Allele. It does
not yet fetch database releases, normalize HGVS expressions, model broad CIViC
categories, or emit clinical classifications. The example answer key verifies
pipeline plumbing only.

## Next milestone

Implement a CIViC release adapter that selects accepted, editor-reviewed simple
alleles; emits the shared candidate format; preserves CIViC evidence identifiers;
and sends broad or ambiguous records to a reason-coded exception queue. A
ClinVar-GKM adapter can then provide already-normalized Cat-VRS and VA-Spec
records through the same downstream patient and answer-key builders.
