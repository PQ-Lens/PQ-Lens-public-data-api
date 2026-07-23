# UM-MTE v1.0 data statement

## Dataset summary

UM-MTE v1.0 is a non-synthetic English-Maltese parallel-corpus project
developed at the University of Malta for research on machine translation,
computational linguistics and low-resource language technology. The corpus
contains 13,535 bilingual document- and article-level units drawn from three
publicly accessible source collections: Malta Government Gazette and
legislation material, Newsbook local-news articles, and the Constitution of
Malta.

This drUM preparation folder separates a text-free metadata package from the
complete source-text export. The metadata package can be reviewed for public
deposit now. The complete English and Maltese text remains pending a
source-by-source copyright, licensing and redistribution-rights decision.

UM-MTE v1.0 is one research output of PQ-LENS - PQ Dashboard: Large Language
Models for Enhanced Navigation, Analysis and Synthesis of Maltese Parliamentary
Questions, funded by XJENZA MALTA under the Digital Technologies Programme.
The UM Principal Investigator for PQ-LENS is Prof. Joel Azzopardi. UM-MTE is
not the complete PQ-LENS project dataset and contains no Parliamentary
Question data.

## Composition

The paired corpus comprises:

| Source collection | Bilingual records | Alignment unit |
|---|---:|---|
| Malta Government Gazette and legislation | 8,540 | Legislative document or Gazette notice |
| Newsbook local news | 4,863 | News article |
| Constitution of Malta | 132 | Constitution article |
| **Total** | **13,535** | Mixed document/article units |

The three source collections contain six observed content categories:

| Content category | Bilingual records | Share |
|---|---:|---:|
| Legal notices | 7,067 | 52.213% |
| Newsbook local-news articles | 4,863 | 35.929% |
| Acts | 1,374 | 10.151% |
| Constitution articles | 132 | 0.975% |
| Local-council bye-laws | 96 | 0.709% |
| Government Gazette notices | 3 | 0.022% |
| **Total** | **13,535** | **100.000%** |

Eight additional English-only Gazette records were found in the source store
but are excluded from the release because they do not have Maltese target
text. Court-order records, Parliamentary Question records and smoke-test data
are also excluded.

## Sources and relevant dates

Acts, legal notices and local-council bye-laws come from the official
Legislation Malta indexes maintained by the Office of the State Advocate.
Government Gazette notices come from the Department of Information's official
Government Gazette repository. Their source-date metadata span:

- Acts: 1964-2026;
- legal notices: 1980-2026;
- local-council bye-laws: 2009-2023; and
- the three paired Government Gazette notices: 2026.

Newsbook pairs come from Beacon Media Group's English and Maltese editions.
The English publication dates represented in the corpus run from 15 June 2024
to 28 May 2026, and the Maltese dates run from 16 June 2024 to 28 May 2026.

The Constitution component uses the official English and Maltese point-in-time
versions dated 27 March 2026. Across the dated collections, the source metadata
therefore span 1964-2026.

Every metadata record retains the corresponding source URL and the available
publication, version and source-specific identifier information. Collection
access points are listed in `SOURCE_ATTRIBUTION.md`.

## Pairing and alignment

UM-MTE v1.0 provides document- and article-level correspondence. It does not
claim sentence-level or paragraph-level alignment.

- Acts, legal notices and local-council bye-laws were paired through the same
  European Legislation Identifier in the English and Maltese Legislation Malta
  views.
- Newsbook articles were paired through the publisher site's WPML `hreflang`
  alternate links.
- Government Gazette notices were paired by notice number.
- Constitution text was paired by numbered article.

The legislation source pipeline downloaded the English and Maltese PDFs,
extracted text, removed simple page and repeated electronic-version markers,
repaired some end-of-line hyphenation and normalized horizontal whitespace.
These operations do not establish semantic equivalence, and the legislation
records remain candidates for bilingual spot-checking.

## Text volume

Using a reproducible definition in which each contiguous sequence of
non-whitespace characters is one descriptive token, the full-text corpus
contains:

| Measure | English | Maltese |
|---|---:|---:|
| Whitespace tokens | 18,275,509 | 15,564,612 |
| Mean tokens per unit | 1,350.24 | 1,149.95 |
| Median tokens per unit | 426 | 350 |
| 95th percentile | 5,781.1 | 4,959.3 |

The combined total is 33,840,121 whitespace tokens. These are not
model-tokenizer counts or linguistically segmented word counts. The long
units reflect the document/article-level design; users of limited-context
models must document any chunking, truncation or exclusion.

## Record content

The text-free public metadata files retain stable record and collection
identifiers, language tags, content category, alignment metadata, source URLs,
dates, source-specific identifiers, text lengths, whitespace-token counts and
SHA-256 fingerprints of the omitted English and Maltese text.

The metadata package deliberately removes the English text, Maltese text,
publisher headlines and source-text descriptions. The fingerprints allow an
authorized local copy of a source text to be checked for exact correspondence
without redistributing that text.

The complete permissions-pending files retain the original exported records,
including English in the `text` field and Maltese in
`translation_metadata.target_text`.

## Quality and limitations

The audit of the 13,535 bilingual records found:

| Check | Result |
|---|---:|
| Empty English texts | 0 |
| Empty Maltese texts | 0 |
| English texts containing U+FFFD | 246 |
| Maltese texts containing U+FFFD | 251 |
| English texts not normalized to NFC | 7 |
| Maltese texts not normalized to NFC | 16 |
| Pairs outside a 1:3-3:1 whitespace-token ratio | 110 |
| Exact duplicate bilingual pair groups | 1 |
| Excess records caused by exact duplication | 1 |
| Completed bilingual manual-QA labels | 0 |

The replacement-character figures are lower bounds on extraction noise. They
do not detect broken words, residual headers and footers, spurious spacing or
ordinary-character OCR substitutions. A publisher-provided link or a shared
legal identifier is strong pairing evidence but is not a completed human
adequacy assessment.

Version 1.0 has no fixed corpus-wide train, development or test split. It also
does not include a corpus-wide external-contamination analysis. A separate
100-document model-evaluation artifact is not part of this deposit.

The corpus over-represents formal legal, administrative and edited news text.
It is not a balanced sample of general Maltese or English, and it should not be
presented as representative of informal conversation, dialectal variation,
social media or natural code-switching.

## Intended and out-of-scope uses

Intended uses include English-Maltese and Maltese-English translation
research, legal and administrative translation research, local-news
translation, long-document translation, terminology studies, quality
estimation, provenance analysis and supervised or parameter-efficient model
adaptation where lawful access to the text exists.

UM-MTE is not a certification of translation safety. Legal, medical,
immigration, emergency and other high-stakes uses require qualified human
review. The dataset is not intended for speaker identification, demographic
inference, surveillance or deceptive localized content.

## Rights and licensing

The CC BY 4.0 notice in the metadata-only package applies only to the original
UM-MTE metadata layer, manifest, schema and documentation. It does not license
the publications linked from the records.

Public availability of source pages is not, by itself, permission to
redistribute their full text under a new licence. Before depositing the
complete English and Maltese files, the project must obtain or document an
applicable reuse basis for the Office of the State Advocate, Department of
Information and Beacon Media Group material; record all required attribution
and restrictions; and have the final access level and licence reviewed by the
University of Malta Library/Open Science Department.

## Versioning and integrity

The component exports were frozen from the authoritative University of Malta
data stores on 23 July 2026. Each deposit package includes a
`checksums.sha256` file. Verify a package from its own directory with:

```text
shasum -a 256 -c checksums.sha256
```

The future drUM DOI should be added to `CITATION.cff` after the repository
record has been created.
