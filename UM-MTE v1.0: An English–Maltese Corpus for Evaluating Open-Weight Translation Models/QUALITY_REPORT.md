# UM-MTE v1.0 quality report

The following findings describe the 8,672 bilingual records that retain source
text: 8,540 Gazette/legislation pairs and 132 Constitution articles. The 4,863
Newsbook records are excluded from these text-quality findings because their
article bodies have been replaced by fixed copyright notices.

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
| Excess record caused by exact duplication | 1 |
| Completed bilingual manual-QA labels | 0 |

The retained source text is aligned at legislative-document, Gazette-notice or
Constitution-article level. Newsbook records retain publisher headlines,
source URLs and article-level pairing metadata, but not article bodies. No
sentence-level or paragraph-level alignment is claimed.

All 4,863 Newsbook records were checked after sanitization: both titles and
both source URLs remain present, and both body fields contain the documented
copyright notices.

The corpus has no fixed corpus-wide train, development or test split. The
separate 100-document model-evaluation artifact is not included in this
package.

The Unicode replacement-character counts are lower bounds on extraction noise:
they do not detect broken words, residual headers, spurious spaces or
ordinary-character OCR substitutions.
