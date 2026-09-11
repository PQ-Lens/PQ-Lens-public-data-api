#!/usr/bin/env python3
"""Replace UM-MTE Newsbook article bodies with copyright notices.

The command is a dry run unless ``--apply`` is supplied. It preserves record
identifiers, titles, URLs, dates, and alignment metadata; refreshes the
Newsbook metadata statistics; updates the manifest; and regenerates the
release checksums deterministically.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any, Iterable


RELEASE_DIRECTORY = (
    "UM-MTE v1.0: An English–Maltese Corpus for Evaluating Open-Weight "
    "Translation Models"
)
NEWSBOOK_DATASET_ID = "newsbook_local_bilingual"
EXPECTED_RECORDS = 4_863
ENGLISH_NOTICE = "Please refer to URL due to copyright."
MALTESE_NOTICE = (
    "Jekk jogħġbok irreferi għall-URL minħabba d-drittijiet tal-awtur."
)


class SanitizationError(RuntimeError):
    """Raised when the release does not match the expected structure."""


def read_jsonl_gzip(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SanitizationError(
                    f"{path}: invalid JSON on line {line_number}: {exc}"
                ) from exc
            if not isinstance(record, dict):
                raise SanitizationError(
                    f"{path}: line {line_number} is not a JSON object"
                )
            records.append(record)
    return records


def write_jsonl_gzip(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as raw_handle:
            with gzip.GzipFile(fileobj=raw_handle, mode="wb", mtime=0) as zipped:
                with io.TextIOWrapper(zipped, encoding="utf-8", newline="\n") as text:
                    for record in records:
                        text.write(
                            json.dumps(
                                record,
                                ensure_ascii=False,
                                sort_keys=True,
                                separators=(",", ":"),
                            )
                        )
                        text.write("\n")
        os.replace(temporary_path, path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def utf16_length(value: str) -> int:
    """Return JavaScript-compatible string length (UTF-16 code units)."""
    return len(value.encode("utf-16-le")) // 2


def whitespace_tokens(value: str) -> int:
    return len(re.findall(r"\S+", value, flags=re.UNICODE))


def text_statistics(english: str, maltese: str) -> dict[str, Any]:
    return {
        "english_characters": utf16_length(english),
        "maltese_characters": utf16_length(maltese),
        "english_whitespace_tokens": whitespace_tokens(english),
        "maltese_whitespace_tokens": whitespace_tokens(maltese),
        "english_sha256": hashlib.sha256(english.encode("utf-8")).hexdigest(),
        "maltese_sha256": hashlib.sha256(maltese.encode("utf-8")).hexdigest(),
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_and_sanitize_records(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if len(records) != EXPECTED_RECORDS:
        raise SanitizationError(
            f"Expected {EXPECTED_RECORDS} Newsbook records, found {len(records)}"
        )

    seen_ids: set[str] = set()
    sanitized: list[dict[str, Any]] = []
    for index, original in enumerate(records, start=1):
        record = dict(original)
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            raise SanitizationError(f"Record {index} has no valid id")
        if record_id in seen_ids:
            raise SanitizationError(f"Duplicate Newsbook record id: {record_id}")
        seen_ids.add(record_id)

        if record.get("dataset_id") != NEWSBOOK_DATASET_ID:
            raise SanitizationError(
                f"{record_id}: unexpected dataset_id {record.get('dataset_id')!r}"
            )

        translation = dict(record.get("translation_metadata") or {})
        attributes = record.get("attributes") or {}
        required_values = {
            "English title": translation.get("source_title"),
            "Maltese title": translation.get("target_title"),
            "English URL": attributes.get("en_url"),
            "Maltese URL": attributes.get("mt_url"),
        }
        missing = [name for name, value in required_values.items() if not value]
        if missing:
            raise SanitizationError(f"{record_id}: missing {', '.join(missing)}")

        record["text"] = ENGLISH_NOTICE
        translation["target_text"] = MALTESE_NOTICE
        record["translation_metadata"] = translation
        sanitized.append(record)

    return sanitized


def refresh_metadata(
    metadata: list[dict[str, Any]], sanitized_records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    if len(metadata) != EXPECTED_RECORDS:
        raise SanitizationError(
            f"Expected {EXPECTED_RECORDS} Newsbook metadata records, found {len(metadata)}"
        )
    records_by_id = {record["id"]: record for record in sanitized_records}
    if len(records_by_id) != EXPECTED_RECORDS:
        raise SanitizationError("Sanitized Newsbook record IDs are not unique")

    refreshed: list[dict[str, Any]] = []
    metadata_ids: set[str] = set()
    for original in metadata:
        item = dict(original)
        record_id = item.get("id")
        if record_id not in records_by_id:
            raise SanitizationError(
                f"Metadata record {record_id!r} has no matching Newsbook record"
            )
        metadata_ids.add(record_id)
        record = records_by_id[record_id]
        item["text_statistics"] = text_statistics(
            record["text"], record["translation_metadata"]["target_text"]
        )
        refreshed.append(item)

    missing_metadata = set(records_by_id) - metadata_ids
    if missing_metadata:
        raise SanitizationError(
            f"Missing metadata for {len(missing_metadata)} Newsbook records"
        )
    return refreshed


def component_text_counts(path: Path) -> tuple[int, int, int]:
    records = read_jsonl_gzip(path)
    english = 0
    maltese = 0
    for record in records:
        english += whitespace_tokens(record.get("text", ""))
        translation = record.get("translation_metadata") or {}
        maltese += whitespace_tokens(translation.get("target_text", ""))
    return len(records), english, maltese


def refresh_manifest(release_dir: Path) -> dict[str, Any]:
    manifest_path = release_dir / "data" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["release_type"] = "full_text_with_newsbook_rights_placeholders_and_metadata"
    manifest["text_included"] = True
    manifest["newsbook_article_text_included"] = False
    manifest["description"] = (
        "Full English and Maltese text for the Gazette/legislation and "
        "Constitution components, plus titles, source URLs, identifiers, "
        "metadata and copyright notices in place of Newsbook article text."
    )

    total_records = 0
    total_english = 0
    total_maltese = 0
    for component in manifest.get("components", []):
        full_text_path = release_dir / component["full_text_file"]
        metadata_path = release_dir / component["metadata_file"]
        count, english, maltese = component_text_counts(full_text_path)
        if count != component.get("records"):
            raise SanitizationError(
                f"{full_text_path}: manifest records={component.get('records')}, "
                f"actual records={count}"
            )
        component["english_whitespace_tokens"] = english
        component["maltese_whitespace_tokens"] = maltese
        component["full_text_file_sha256"] = sha256_file(full_text_path)
        component["full_text_file_bytes"] = full_text_path.stat().st_size
        component["metadata_file_sha256"] = sha256_file(metadata_path)
        component["metadata_file_bytes"] = metadata_path.stat().st_size
        if component.get("collection") == "Newsbook local news":
            component["content_status"] = "titles_urls_and_copyright_placeholders"
        total_records += count
        total_english += english
        total_maltese += maltese

    manifest["records"] = total_records
    manifest["english_whitespace_tokens"] = total_english
    manifest["maltese_whitespace_tokens"] = total_maltese
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def refresh_checksums(release_dir: Path) -> None:
    checksum_path = release_dir / "checksums.sha256"
    paths = sorted(
        path
        for path in release_dir.rglob("*")
        if path.is_file() and path != checksum_path
    )
    lines = [
        f"{sha256_file(path)}  ./{path.relative_to(release_dir).as_posix()}"
        for path in paths
    ]
    checksum_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify_release(release_dir: Path) -> dict[str, Any]:
    full_text_path = (
        release_dir / "data" / "full_text" / "um_mte_v1_newsbook.jsonl.gz"
    )
    metadata_path = release_dir / "data" / "um_mte_v1_metadata_newsbook.jsonl.gz"
    records = read_jsonl_gzip(full_text_path)
    metadata = read_jsonl_gzip(metadata_path)

    if len(records) != EXPECTED_RECORDS or len(metadata) != EXPECTED_RECORDS:
        raise SanitizationError("Newsbook record or metadata count changed")
    for record in records:
        if record.get("text") != ENGLISH_NOTICE:
            raise SanitizationError(f"{record.get('id')}: English text is not sanitized")
        target = (record.get("translation_metadata") or {}).get("target_text")
        if target != MALTESE_NOTICE:
            raise SanitizationError(f"{record.get('id')}: Maltese text is not sanitized")

    expected_stats = text_statistics(ENGLISH_NOTICE, MALTESE_NOTICE)
    for item in metadata:
        if item.get("text_statistics") != expected_stats:
            raise SanitizationError(
                f"{item.get('id')}: metadata text statistics are inconsistent"
            )

    manifest = json.loads(
        (release_dir / "data" / "manifest.json").read_text(encoding="utf-8")
    )
    component = next(
        (
            item
            for item in manifest.get("components", [])
            if item.get("collection") == "Newsbook local news"
        ),
        None,
    )
    if not component or component.get("content_status") != (
        "titles_urls_and_copyright_placeholders"
    ):
        raise SanitizationError("Manifest does not record Newsbook sanitization")

    checksum_path = release_dir / "checksums.sha256"
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ./", 1)
        path = release_dir / relative
        if sha256_file(path) != digest:
            raise SanitizationError(f"Checksum mismatch: {relative}")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    default_release = Path(__file__).resolve().parents[1] / RELEASE_DIRECTORY
    parser.add_argument("--release-dir", type=Path, default=default_release)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the sanitized payload, metadata, manifest, and checksums.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    release_dir = args.release_dir.resolve()
    full_text_path = (
        release_dir / "data" / "full_text" / "um_mte_v1_newsbook.jsonl.gz"
    )
    metadata_path = release_dir / "data" / "um_mte_v1_metadata_newsbook.jsonl.gz"

    records = read_jsonl_gzip(full_text_path)
    sanitized = validate_and_sanitize_records(records)
    metadata = read_jsonl_gzip(metadata_path)
    refreshed_metadata = refresh_metadata(metadata, sanitized)

    sample = sanitized[0]
    print(f"Newsbook records matched: {len(sanitized)}")
    print(f"Sample id: {sample['id']}")
    print(
        "Titles retained: "
        f"{sample['translation_metadata']['source_title']} | "
        f"{sample['translation_metadata']['target_title']}"
    )
    print(f"English replacement: {ENGLISH_NOTICE}")
    print(f"Maltese replacement: {MALTESE_NOTICE}")

    if not args.apply:
        print("Dry run only; no files changed. Re-run with --apply to write changes.")
        return 0

    write_jsonl_gzip(full_text_path, sanitized)
    write_jsonl_gzip(metadata_path, refreshed_metadata)
    manifest = refresh_manifest(release_dir)
    refresh_checksums(release_dir)
    verify_release(release_dir)
    print(
        "Sanitization complete: "
        f"records={manifest['records']} "
        f"english_whitespace_tokens={manifest['english_whitespace_tokens']} "
        f"maltese_whitespace_tokens={manifest['maltese_whitespace_tokens']}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SanitizationError as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1) from exc
