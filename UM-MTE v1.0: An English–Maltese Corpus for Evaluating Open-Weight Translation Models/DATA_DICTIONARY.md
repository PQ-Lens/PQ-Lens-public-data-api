# UM-MTE v1.0 metadata data dictionary

Each compressed JSONL file contains one JSON object per bilingual record.

| Field | Description |
|---|---|
| `id` | Stable record identifier from the source data store. |
| `dataset_id` | Internal collection identifier. |
| `dataset_version` | UM-MTE release version, currently `1.0`. |
| `collection` | Human-readable source collection. |
| `content_category` | One of `acts`, `legal_notices`, `local_council_bye_laws`, `government_gazette_notices`, `newsbook_local_news`, or `constitution_articles`. |
| `language` | Source language tag, normally `eng_Latn`. |
| `language_pair` | Pair tag, normally `eng_Latn-mlt_Latn`. |
| `synthetic_status` | Indicates whether the content is synthetic. All included records are `non_synthetic`. |
| `alignment.type` | Document/article pairing type recorded by the source pipeline. |
| `alignment.status` | Recorded alignment-review status where available. |
| `alignment.confidence` | Qualitative confidence where available; not a numeric score. |
| `alignment.pairing_signal` | Metadata signal used to pair a record, such as a WPML alternate link. |
| `alignment.source_language` | Recorded source language. |
| `alignment.target_language` | Recorded target language. |
| `alignment.source_unit` | Source alignment unit where recorded. |
| `alignment.target_unit` | Target alignment unit where recorded. |
| `provenance.source_type` | Source type declared by the original record. |
| `provenance.source_url` | Primary source or English-side URL. |
| `provenance.target_url` | Maltese-side URL where explicitly recorded. |
| `provenance.english_pdf_url` | Official English PDF URL where recorded. |
| `provenance.maltese_pdf_url` | Official Maltese PDF URL where recorded. |
| `provenance.source_collection` | Source-collection label where recorded. |
| `provenance.publication_date_english` | English/source publication date where recorded. |
| `provenance.publication_date_maltese` | Maltese publication date where recorded. |
| `provenance.version_date` | Point-in-time version date where applicable. |
| `provenance.identifiers` | Source-specific ELI, Gazette, notice, article, WordPress or pair identifiers. |
| `text_statistics.english_characters` | JavaScript Unicode-string length of the omitted English field. |
| `text_statistics.maltese_characters` | JavaScript Unicode-string length of the omitted Maltese field. |
| `text_statistics.english_whitespace_tokens` | Unicode-aware whitespace-token count used by the paper audit. |
| `text_statistics.maltese_whitespace_tokens` | Unicode-aware whitespace-token count used by the paper audit. |
| `text_statistics.english_sha256` | SHA-256 fingerprint of the exact omitted English UTF-8 text. |
| `text_statistics.maltese_sha256` | SHA-256 fingerprint of the exact omitted Maltese UTF-8 text. |
| `created_at` | Original record-creation timestamp. |
| `updated_at` | Original record-update timestamp. |

Fields without an available value are omitted rather than stored as null.
