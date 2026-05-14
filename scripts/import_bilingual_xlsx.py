#!/usr/bin/env python3
"""Import bilingual.xlsx Maltese-English rows into the JSON data store.

The script is intentionally idempotent: existing records are treated as already
imported, and the final verification step confirms that every row in
bilingual.xlsx is available in the generated data store with the expected
metadata.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openpyxl import load_workbook

DATASET_ID = "court_orders_bilingual"
SOURCE_LANGUAGE = "eng_Latn"
TARGET_LANGUAGE = "mlt_Latn"
LANGUAGE_PAIR = f"{SOURCE_LANGUAGE}-{TARGET_LANGUAGE}"
WORKSHEET_NAME = "Bilingual"
EXPECTED_HEADERS = ("English", "Maltese")
DEFAULT_STORE_PATH = Path("data_store.json")

DATASET_SUMMARY = (
    "A bilingual legal-text dataset derived from Court Notices published on the "
    "Government of Malta website. It contains parallel Maltese–English text pairs "
    "extracted from court notice PDFs and converted into structured text format."
)
DATASET_DESCRIPTION = (
    "This dataset contains Court Notices from the Government of Malta website "
    "(gov.mt). It contains Maltese–English pairs for each court notice. The "
    "original dataset format was PDF text; these extracts have been converted "
    "into structured text pairs in both Maltese and English. The dataset contains "
    "2,310 rows of data. The latest record date is 7 May 2026, and the earliest "
    "record date is 22 November 2022. The dataset is suitable for Maltese–English "
    "and English–Maltese machine translation tasks, legal NLP research tasks, and "
    "bilingual legal language analysis."
)


class ImportErrorWithDetails(Exception):
    """Raised when import or verification cannot continue safely."""


@dataclass(frozen=True)
class BilingualRow:
    row_number: int
    english_text: str
    maltese_text: str

    @property
    def record_id(self) -> str:
        return f"bilingual_row_{self.row_number:04d}"


def normalize_cell(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip()


def load_rows(path: Path) -> list[BilingualRow]:
    if not path.exists():
        raise ImportErrorWithDetails(f"Excel file not found: {path}")

    workbook = load_workbook(path, read_only=True, data_only=True)
    if WORKSHEET_NAME not in workbook.sheetnames:
        raise ImportErrorWithDetails(
            f"Worksheet '{WORKSHEET_NAME}' not found in {path}. "
            f"Available sheets: {', '.join(workbook.sheetnames)}"
        )

    worksheet = workbook[WORKSHEET_NAME]
    headers = tuple(normalize_cell(worksheet.cell(row=1, column=idx).value) for idx in range(1, 3))
    if headers != EXPECTED_HEADERS:
        raise ImportErrorWithDetails(
            f"Expected headers {EXPECTED_HEADERS}, found {headers} in {path}"
        )

    rows: list[BilingualRow] = []
    for row_number in range(2, worksheet.max_row + 1):
        english_text = normalize_cell(worksheet.cell(row=row_number, column=1).value)
        maltese_text = normalize_cell(worksheet.cell(row=row_number, column=2).value)
        if not english_text and not maltese_text:
            continue
        if not english_text or not maltese_text:
            print(
                f"Skipping row {row_number}: both English and Maltese text are required for a bilingual pair",
                file=sys.stderr,
            )
            continue
        rows.append(
            BilingualRow(
                row_number=row_number,
                english_text=english_text,
                maltese_text=maltese_text,
            )
        )
    return rows


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_store(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"datasets": {}, "records": {}}

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_store(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(".tmp")
    with temp_path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
    temp_path.replace(path)


def dataset_payload() -> dict[str, Any]:
    return {
        "id": DATASET_ID,
        "summary": DATASET_SUMMARY,
        "description": DATASET_DESCRIPTION,
        "language_mode": "bilingual_aligned",
        "synthetic_status": "non_synthetic",
        "synthetic_details": {},
        "provenance": {
            "source_url": "https://www.gov.mt/",
            "source_text": "Court Notices from the Government of Malta website exported from PDF text into bilingual.xlsx.",
            "source_type": "web",
        },
    }


def ensure_dataset(state: dict[str, Any]) -> str:
    payload = dataset_payload()
    now = utc_now()
    datasets = state.setdefault("datasets", {})
    state.setdefault("records", {}).setdefault(DATASET_ID, {})

    existing = datasets.get(DATASET_ID)
    if existing:
        created_at = existing.get("created_at", now)
        existing.update(payload)
        existing["created_at"] = created_at
        existing["updated_at"] = now
        return "updated"

    datasets[DATASET_ID] = {**payload, "created_at": now, "updated_at": now}
    return "created"


def build_record_payload(row: BilingualRow, xlsx_path: Path) -> dict[str, Any]:
    return {
        "id": row.record_id,
        "text": row.english_text,
        "language": SOURCE_LANGUAGE,
        "language_pair": LANGUAGE_PAIR,
        "synthetic_status": "non_synthetic",
        "translation_metadata": {
            "source_language": SOURCE_LANGUAGE,
            "target_language": TARGET_LANGUAGE,
            "target_text": row.maltese_text,
            "alignment_type": "row_aligned",
            "source_column": "English",
            "target_column": "Maltese",
        },
        "provenance": {
            "source_text": f"{xlsx_path.name}, worksheet {WORKSHEET_NAME}, row {row.row_number}",
            "source_type": "file",
        },
        "attributes": {
            "excel_file": xlsx_path.name,
            "worksheet": WORKSHEET_NAME,
            "row_number": row.row_number,
            "original_source": "Government of Malta Court Notices",
            "original_source_url": "https://www.gov.mt/",
            "original_format": "pdf",
            "structured_format": "xlsx",
        },
    }


def insert_records(state: dict[str, Any], rows: list[BilingualRow], xlsx_path: Path) -> tuple[int, int]:
    now = utc_now()
    records_map = state.setdefault("records", {}).setdefault(DATASET_ID, {})
    created = 0
    existing = 0

    for row in rows:
        if row.record_id in records_map:
            existing += 1
            continue

        records_map[row.record_id] = {
            **build_record_payload(row, xlsx_path),
            "dataset_id": DATASET_ID,
            "created_at": now,
            "updated_at": now,
        }
        created += 1

    return created, existing


def get_all_records(state: dict[str, Any]) -> list[dict[str, Any]]:
    return list(state.setdefault("records", {}).setdefault(DATASET_ID, {}).values())


def verify_inserted(expected_rows: list[BilingualRow], actual_records: list[dict[str, Any]]) -> None:
    expected_by_id = {row.record_id: row for row in expected_rows}
    actual_by_id = {record.get("id"): record for record in actual_records}
    missing_ids = sorted(set(expected_by_id) - set(actual_by_id))
    if missing_ids:
        preview = ", ".join(missing_ids[:10])
        raise ImportErrorWithDetails(f"Missing {len(missing_ids)} expected records: {preview}")

    failures: list[str] = []
    for record_id, expected in expected_by_id.items():
        record = actual_by_id[record_id]
        translation_metadata = record.get("translation_metadata") or {}
        attributes = record.get("attributes") or {}
        checks = {
            "language": record.get("language") == SOURCE_LANGUAGE,
            "language_pair": record.get("language_pair") == LANGUAGE_PAIR,
            "synthetic_status": record.get("synthetic_status") == "non_synthetic",
            "text": record.get("text") == expected.english_text,
            "target_language": translation_metadata.get("target_language") == TARGET_LANGUAGE,
            "target_text": translation_metadata.get("target_text") == expected.maltese_text,
            "row_number": attributes.get("row_number") == expected.row_number,
        }
        bad_fields = [name for name, ok in checks.items() if not ok]
        if bad_fields:
            failures.append(f"{record_id}: {', '.join(bad_fields)}")

    if failures:
        preview = "; ".join(failures[:10])
        raise ImportErrorWithDetails(f"Verification failed for {len(failures)} records: {preview}")

    if len(actual_records) < len(expected_rows):
        raise ImportErrorWithDetails(
            f"Data store contains {len(actual_records)} records but {len(expected_rows)} rows were expected"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import bilingual.xlsx Maltese-English court notice pairs into the JSON data store."
    )
    parser.add_argument("--xlsx", default="bilingual.xlsx", type=Path, help="Path to bilingual.xlsx")
    parser.add_argument(
        "--store-path",
        default=DEFAULT_STORE_PATH,
        type=Path,
        help=f"Path to the JSON data store to write (default: {DEFAULT_STORE_PATH})",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = load_rows(args.xlsx)
    if not rows:
        raise ImportErrorWithDetails(f"No importable bilingual rows found in {args.xlsx}")

    state = load_store(args.store_path)
    dataset_status = ensure_dataset(state)
    created, existing = insert_records(state, rows, args.xlsx)
    save_store(args.store_path, state)

    records = get_all_records(state)
    verify_inserted(rows, records)

    print(
        "Import verified successfully: "
        f"dataset {dataset_status}, {len(rows)} expected rows, {created} created, "
        f"{existing} already existed, {len(records)} records available in dataset "
        f"'{DATASET_ID}' at {args.store_path}."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ImportErrorWithDetails as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
