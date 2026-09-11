# UM-MTE v1.0 data statement

## Dataset summary

UM-MTE v1.0 is a non-synthetic English-Maltese corpus project developed at the
University of Malta for research on machine translation, computational
linguistics and low-resource language technology. The release contains 13,535
bilingual records drawn from three publicly accessible source collections:
Malta Government Gazette and legislation material, Newsbook local-news
articles, and the Constitution of Malta.

Complete English and Maltese source text is included for 8,672 records from
the Gazette/legislation and Constitution components. The 4,863 Newsbook
records retain publisher headlines, source URLs, identifiers, dates and
article-level pairing metadata, but their article bodies are replaced by fixed
English and Maltese copyright notices directing users to the source URLs. A
text-free metadata view accompanies each component.

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
| Newsbook local news | 4,863 | Headline and article-link pair; bodies omitted |
| Constitution of Malta | 132 | Constitution article |
| **Total** | **13,535** | Mixed document/article units |

The three source collections contain six observed content categories:

| Content category | Bilingual records | Share |
|---|---:|---:|
| Legal notices | 7,067 | 52.213% |
| Newsbook local-news title/link records | 4,863 | 35.929% |
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

Newsbook title/link pairs come from Beacon Media Group's English and Maltese
editions. The English publication dates represented in the metadata run from
15 June 2024 to 28 May 2026, and the Maltese dates run from 16 June 2024 to 28
May 2026. Article bodies are not included in the release.

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
- Newsbook records were paired through the publisher site's WPML `hreflang`
  alternate links. Both publisher headlines and URLs remain, but the article
  bodies are omitted.
- Government Gazette notices were paired by notice number.
- Constitution text was paired by numbered article.

The legislation source pipeline downloaded the English and Maltese PDFs,
extracted text, removed simple page and repeated electronic-version markers,
repaired some end-of-line hyphenation and normalized horizontal whitespace.
These operations do not establish semantic equivalence, and the legislation
records remain candidates for bilingual spot-checking.

## Text volume

Using a reproducible definition in which each contiguous sequence of
non-whitespace characters is one descriptive token, the 8,672 records that
retain source text contain:

| Measure | English | Maltese |
|---|---:|---:|
| Whitespace tokens | 16,242,368 | 13,859,369 |
| Mean tokens per unit | 1,872.97 | 1,598.17 |
| Median tokens per unit | 516 | 418 |
| 95th percentile | 8,207.4 | 7,131.3 |

The combined retained source-text total is 30,101,737 whitespace tokens. Each
Newsbook copyright notice contains seven whitespace-delimited tokens, so the
stored release totals reported in `data/manifest.json` are 16,276,409 English
and 13,893,410 Maltese tokens. The notices are not corpus text and should not
be treated as translation-training material. These counts are not
model-tokenizer counts or linguistically segmented word counts.

## Record content

The text-free metadata files retain stable record and collection identifiers,
language tags, content category, alignment metadata, source URLs, dates,
source-specific identifiers and statistics for the corresponding stored text
fields. For Newsbook records, those statistics and fingerprints describe only
the fixed copyright notices; they do not describe or fingerprint the omitted
article bodies.

The files under `data/full_text/` are gzip-compressed JSON Lines, with one
bilingual record per line. The Gazette/legislation and Constitution files
retain English in `text` and Maltese in `translation_metadata.target_text`.
In the Newsbook file, these fields contain copyright notices. The English and
Maltese publisher headlines remain in `translation_metadata.source_title` and
`translation_metadata.target_title`, and the corresponding URLs remain in the
record provenance and attributes.

## Quality and limitations

The audit of the 8,672 records that retain source text found:

| Check | Result |
|---|---:|
| Empty English texts | 0 |
| Empty Maltese texts | 0 |
| English texts containing U+FFFD | 246 |
| Maltese texts containing U+FFFD | 251 |
| English texts not normalized to NFC | 7 |
| Maltese texts not normalized to NFC | 15 |
| Pairs outside a 1:3-3:1 whitespace-token ratio | 16 |
| Exact duplicate bilingual pair groups | 1 |
| Excess records caused by exact duplication | 1 |
| Completed bilingual manual-QA labels | 0 |

The replacement-character figures are lower bounds on extraction noise. They
do not detect broken words, residual headers and footers, spurious spacing or
ordinary-character OCR substitutions. A publisher-provided link or a shared
legal identifier is strong pairing evidence but is not a completed human
adequacy assessment.

All 4,863 Newsbook records were separately verified after sanitization: both
publisher headlines and both URLs remain present, and the English and Maltese
body fields contain only the documented copyright notices.

Version 1.0 has no fixed corpus-wide train, development or test split. It also
does not include a corpus-wide external-contamination analysis. A separate
100-document model-evaluation artifact is not part of this deposit.

The retained source-text corpus over-represents formal legal and administrative
text. Newsbook contributes paired headlines and provenance, not article text.
The release is not a balanced sample of general Maltese or English, and it
should not be presented as representative of informal conversation, dialectal
variation, social media or natural code-switching.

## Intended and out-of-scope uses

The Gazette/legislation and Constitution components support English-Maltese
and Maltese-English translation research, legal and administrative translation
research, long-document translation, terminology studies, quality estimation
and model adaptation. The Newsbook component supports headline-pairing and
provenance research. It does not provide article text for local-news
translation or model training; users must follow the retained source URLs.

UM-MTE is not a certification of translation safety. Legal, medical,
immigration, emergency and other high-stakes uses require qualified human
review. The dataset is not intended for speaker identification, demographic
inference, surveillance or deceptive localized content.

## Rights and licensing

The CC BY 4.0 notice applies to the original UM-MTE selection, metadata layer,
manifest, schema and documentation; it does not relicense third-party
publications. Newsbook article bodies are not redistributed. Publisher
headlines, URLs and metadata are retained, and copyright remains with Beacon
Media Group and any other applicable rights holders. The Gazette/legislation
and Constitution components continue to include source text under their
applicable permissions and reuse basis. Source access points and attribution
are listed in `SOURCE_ATTRIBUTION.md`.

## Versioning and integrity

The component exports were frozen from the authoritative University of Malta
data stores on 23 July 2026. The Newsbook bodies were replaced with copyright
notices in September 2026. The release includes a `checksums.sha256` file.
Verify it from the release directory with:

```text
shasum -a 256 -c checksums.sha256
```

The future drUM DOI should be added to `CITATION.cff` after the repository
record has been created.
