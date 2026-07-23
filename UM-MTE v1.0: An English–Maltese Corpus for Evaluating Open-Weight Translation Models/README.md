# UM-MTE v1.0 full release

UM-MTE v1.0 is an English-Maltese parallel-corpus project developed at the
University of Malta. This package provides the complete English and Maltese
text and the corresponding metadata for 13,535 document- and article-level
bilingual records.

The corpus contains 8,540 Malta Government Gazette and legislation pairs,
4,863 Newsbook article pairs and 132 Constitution articles. It contains
18,275,509 English and 15,564,612 Maltese whitespace-delimited tokens.

## Included files

- `data/full_text/um_mte_v1_gazette_legislation.jsonl.gz` - full text for 8,540
  Gazette and legislation pairs
- `data/full_text/um_mte_v1_newsbook.jsonl.gz` - full text for 4,863 Newsbook
  article pairs
- `data/full_text/um_mte_v1_constitution.jsonl.gz` - full text for 132
  Constitution article pairs
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
- `LICENSE.txt` - licence and source-rights notice
- `checksums.sha256` - integrity checks for deposited files

## Record format

The full-text files are gzip-compressed JSON Lines. Each line is one bilingual
document or article. English appears in the top-level `text` field and Maltese
appears in `translation_metadata.target_text`. The files are aligned at
document or article level; no sentence-level alignment is claimed.

The metadata files provide a text-free view of the same records. They retain
identifiers, provenance URLs, dates, alignment metadata, text lengths,
whitespace-token counts and SHA-256 text fingerprints.

The package excludes Parliamentary Question data, court-order data and eight
English-only Gazette records.

## Intended use

Intended uses include English-Maltese and Maltese-English translation
research, legal and administrative translation, local-news translation,
long-document translation, terminology, quality estimation and supervised or
parameter-efficient model adaptation.

## Licence

The original UM-MTE metadata layer, manifest, schema and documentation in this
folder are licensed under Creative Commons Attribution 4.0 International.
Source-derived full text is redistributed under the applicable permissions and
reuse basis confirmed by the project. Copyright and attribution in the
underlying publications remain with their respective publishers or public
bodies; see `SOURCE_ATTRIBUTION.md`.
