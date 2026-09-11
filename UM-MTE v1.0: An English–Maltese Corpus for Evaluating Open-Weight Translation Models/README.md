# UM-MTE v1.0 rights-adjusted release

UM-MTE v1.0 is an English-Maltese corpus project developed at the University
of Malta. This package contains 13,535 bilingual records. Complete English and
Maltese text is included for the 8,540 Gazette/legislation pairs and 132
Constitution articles. For the 4,863 Newsbook pairs, the publisher headlines,
source URLs and metadata are retained, while each article body is replaced by
a copyright notice directing users to the source URL.

The redistributable Gazette/legislation and Constitution source text contains
16,242,368 English and 13,859,369 Maltese whitespace-delimited tokens. The
stored release totals, including the short Newsbook copyright notices, are
16,276,409 English and 13,893,410 Maltese tokens.

## Included files

- `data/full_text/um_mte_v1_gazette_legislation.jsonl.gz` - full text for 8,540
  Gazette and legislation pairs
- `data/full_text/um_mte_v1_newsbook.jsonl.gz` - titles, URLs, metadata and
  copyright notices for 4,863 Newsbook article pairs; article bodies are not
  included
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

The files under `data/full_text/` are gzip-compressed JSON Lines. Each line is
one bilingual record. English appears in the top-level `text` field and
Maltese appears in `translation_metadata.target_text`. In the Newsbook file,
those two fields contain fixed copyright notices rather than article text;
`translation_metadata.source_title` and
`translation_metadata.target_title` retain the English and Maltese headlines.
The records are aligned at document or article level; no sentence-level
alignment is claimed.

The metadata files provide a text-free view of the same records. They retain
identifiers, provenance URLs, dates, alignment metadata and statistics for the
corresponding stored text fields. Newsbook statistics and fingerprints refer
only to the copyright notices, not to the omitted articles.

The package excludes Parliamentary Question data, court-order data and eight
English-only Gazette records.

## Intended use

The Gazette/legislation and Constitution components support English-Maltese
and Maltese-English translation research, legal and administrative
translation, long-document translation, terminology, quality estimation and
model adaptation. The Newsbook component supports headline-pairing and
provenance research; users must follow the retained URLs to access article
content from the publisher.

## Licence

The original UM-MTE metadata layer, manifest, schema and documentation in this
folder are licensed under Creative Commons Attribution 4.0 International.
That licence does not relicense third-party publications. Newsbook article
bodies are not redistributed; copyright remains with Beacon Media Group and
other applicable rights holders. See `SOURCE_ATTRIBUTION.md` for the status of
each source collection.
