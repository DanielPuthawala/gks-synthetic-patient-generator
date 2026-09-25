"""Deterministic validation for the deliberately narrow pilot input profile."""

from __future__ import annotations

from typing import Any

from .errors import CandidateRejected


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise CandidateRejected(code, message)


def validate_vrs_allele(allele: dict[str, Any]) -> None:
    """Validate supplied VRS identity fields without calculating or repairing them."""

    _require(allele.get("type") == "Allele", "NOT_VRS_ALLELE", "type must be Allele")

    allele_id = allele.get("id")
    digest = allele.get("digest")
    _require(
        isinstance(allele_id, str) and allele_id.startswith("ga4gh:VA."),
        "MISSING_VRS_ID",
        "a computed ga4gh:VA identifier is required",
    )
    _require(
        isinstance(digest, str) and allele_id == f"ga4gh:VA.{digest}",
        "VRS_DIGEST_MISMATCH",
        "the supplied Allele id and digest disagree",
    )

    location = allele.get("location")
    _require(isinstance(location, dict), "MISSING_LOCATION", "location is required")
    _require(
        location.get("type") == "SequenceLocation",
        "UNSUPPORTED_LOCATION",
        "pilot supports SequenceLocation alleles only",
    )

    location_id = location.get("id")
    location_digest = location.get("digest")
    _require(
        isinstance(location_id, str) and location_id.startswith("ga4gh:SL."),
        "MISSING_LOCATION_ID",
        "a computed ga4gh:SL identifier is required",
    )
    _require(
        isinstance(location_digest, str)
        and location_id == f"ga4gh:SL.{location_digest}",
        "LOCATION_DIGEST_MISMATCH",
        "the supplied SequenceLocation id and digest disagree",
    )

    sequence_reference = location.get("sequenceReference")
    _require(
        isinstance(sequence_reference, dict),
        "MISSING_SEQUENCE_REFERENCE",
        "sequenceReference is required",
    )
    _require(
        isinstance(sequence_reference.get("refgetAccession"), str)
        and sequence_reference["refgetAccession"].startswith("SQ."),
        "MISSING_REFGET_ACCESSION",
        "a refget SQ accession is required",
    )

    start = location.get("start")
    end = location.get("end")
    _require(
        isinstance(start, int) and isinstance(end, int) and 0 <= start <= end,
        "INVALID_INTERVAL",
        "start and end must define a valid zero-based interval",
    )

    state = allele.get("state")
    _require(
        isinstance(state, dict) and state.get("type") == "LiteralSequenceExpression",
        "UNSUPPORTED_STATE",
        "pilot supports LiteralSequenceExpression states only",
    )
    _require(
        isinstance(state.get("sequence"), str),
        "MISSING_ALTERNATE_SEQUENCE",
        "literal alternate sequence is required",
    )


def validate_candidate(candidate: dict[str, Any]) -> None:
    """Validate eligibility for the precise-simple-allele pilot."""

    _require(
        candidate.get("status") == "accepted",
        "NOT_ACCEPTED",
        "record is not accepted",
    )
    _require(
        candidate.get("scope") == "simple_allele",
        "UNSUPPORTED_SCOPE",
        "pilot accepts simple alleles only",
    )
    _require(
        candidate.get("category_kind") == "canonical_allele",
        "UNSUPPORTED_CATEGORY_KIND",
        "pilot accepts canonical allele categories only",
    )
    _require(
        candidate.get("ambiguous_normalizer_result") is False,
        "AMBIGUOUS_NORMALIZATION",
        "normalizer result must be explicitly unambiguous",
    )

    source = candidate.get("source")
    _require(
        isinstance(source, dict),
        "MISSING_SOURCE",
        "source provenance is required",
    )
    for field in ("name", "record_id", "release", "retrieved_from"):
        _require(
            bool(source.get(field)),
            "INCOMPLETE_SOURCE",
            f"source.{field} is required",
        )

    category = candidate.get("category")
    _require(
        isinstance(category, dict),
        "MISSING_CATEGORY",
        "category metadata is required",
    )
    _require(bool(category.get("id")), "MISSING_CATEGORY_ID", "category.id is required")
    _require(
        bool(category.get("name")),
        "MISSING_CATEGORY_NAME",
        "category.name is required",
    )

    validate_vrs_allele(candidate.get("defining_allele", {}))


def validate_catvar(catvar: dict[str, Any]) -> None:
    """Check invariants of a catvar emitted by this pilot."""

    _require(catvar.get("type") == "CategoricalVariant", "NOT_CATVAR", "wrong type")
    constraints = catvar.get("constraints")
    _require(
        isinstance(constraints, list) and len(constraints) == 1,
        "INVALID_CONSTRAINT_COUNT",
        "canonical allele pilot emits exactly one defining constraint",
    )
    constraint = constraints[0]
    _require(
        constraint.get("type") == "DefiningAlleleConstraint",
        "INVALID_CONSTRAINT",
        "constraint must be DefiningAlleleConstraint",
    )
    validate_vrs_allele(constraint.get("allele", {}))
