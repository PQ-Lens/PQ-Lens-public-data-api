# UM-MTE v1.0 quality report

The following findings describe the 13,535 bilingual full-text records from
which this text-free metadata package was generated.

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
| Excess record caused by exact duplication | 1 |
| Completed bilingual manual-QA labels | 0 |

The data are aligned at legislative-document, Gazette-notice, news-article or
Constitution-article level. No sentence-level or paragraph-level alignment is
claimed.

The corpus has no fixed corpus-wide train, development or test split. The
separate 100-document model-evaluation artifact is not included in this
package.

The Unicode replacement-character counts are lower bounds on extraction noise:
they do not detect broken words, residual headers, spurious spaces or
ordinary-character OCR substitutions.
