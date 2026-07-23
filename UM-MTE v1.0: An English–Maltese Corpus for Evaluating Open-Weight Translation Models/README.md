# UM-MTE v1.0 metadata-only release

UM-MTE v1.0 is an English-Maltese parallel-corpus project developed at the
University of Malta. This package provides the public metadata layer for 13,535
document- and article-level bilingual records without redistributing publisher
or government source text.

## Included files

- `data/um_mte_v1_metadata_gazette_legislation.jsonl.gz` - metadata for 8,540
  Gazette and legislation pairs
- `data/um_mte_v1_metadata_newsbook.jsonl.gz` - metadata for 4,863 Newsbook
  article pairs
- `data/um_mte_v1_metadata_constitution.jsonl.gz` - metadata for 132
  Constitution article pairs
- `data/manifest.json` - counts, source-export checksums and generated-file
  checksums
- `DATA_STATEMENT.md` - detailed description of composition, construction,
  quality, intended uses and rights status
- `DATA_DICTIONARY.md` - field definitions
- `SOURCE_ATTRIBUTION.md` - publisher and source access information
- `QUALITY_REPORT.md` - documented quality limitations
- `FUNDING.txt` - funding acknowledgement
- `CITATION.cff` - suggested citation metadata
- `LICENSE.txt` - CC BY 4.0 notice for this metadata package
- `checksums.sha256` - integrity checks for deposited files

## What is deliberately omitted

The fields containing English text, Maltese text, publisher headlines and
source-text descriptions are omitted. Each record contains text lengths,
whitespace-token counts and SHA-256 fingerprints so an authorized copy can be
verified without exposing the source text.

The package excludes Parliamentary Question data, court-order data and eight
English-only Gazette records.

## Intended use

The metadata supports corpus discovery, provenance auditing, source retrieval,
pair verification, rights review, corpus composition analysis and
reconstruction by users who have lawful access to the original sources. It is
not by itself sufficient for translation-model training.

## Licence

The original UM-MTE metadata layer, manifest, schema and documentation in this
folder are licensed under Creative Commons Attribution 4.0 International.
That licence does not apply to the underlying source publications linked from
the records.
