# Local data

The `raw`, `intermediate`, and `processed` directories are intentionally excluded
from version control. Full ClinVar, ClinVar-GKM, CIViC, and generated patient
datasets should not be committed to this repository.

For each source release, record at minimum:

- source name and release/version;
- canonical download URL;
- retrieval date;
- file checksum;
- applicable license or data-use terms; and
- the pipeline configuration and Git commit used to process it.

Small, reviewed examples belong in `examples/` or `tests/fixtures/`.
