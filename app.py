from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_STORE_PATH = BASE_DIR / "data_store.json"
ORDERS = {"natural", "shuffle"}


class ApiError(Exception):
    def __init__(self, message: str, status_code: int = 400, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class DataStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _initial_state(self) -> dict[str, Any]:
        return {"datasets": {}, "records": {}}

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            state = self._initial_state()
            self.save(state)
            return state

        with self.path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def save(self, state: dict[str, Any]) -> None:
        temp_path = self.path.with_suffix(".tmp")
        with temp_path.open("w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2)
        temp_path.replace(self.path)


def parse_positive_int(name: str, default: int, *, minimum: int = 1, maximum: int = 10_000) -> int:
    raw = request.args.get(name)
    if raw is None:
        return default

    try:
        value = int(raw)
    except ValueError as exc:  # pragma: no cover
        raise ApiError(f"{name} must be an integer", 400) from exc

    if value < minimum or value > maximum:
        raise ApiError(f"{name} must be between {minimum} and {maximum}", 400)
    return value


def parse_optional_int(name: str) -> int | None:
    raw = request.args.get(name)
    if raw is None:
        return None
    try:
        return int(raw)
    except ValueError as exc:
        raise ApiError(f"{name} must be an integer", 400) from exc


def create_app(config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update({"DATA_STORE_PATH": DEFAULT_STORE_PATH})
    if config:
        app.config.update(config)

    store = DataStore(Path(app.config["DATA_STORE_PATH"]))

    @app.errorhandler(ApiError)
    def handle_api_error(exc: ApiError):
        response = {"error": exc.message, "details": exc.details, "timestamp": utc_now()}
        return jsonify(response), exc.status_code

    @app.errorhandler(404)
    def not_found(_: Any):
        return jsonify({"error": "Resource not found", "timestamp": utc_now()}), 404

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        response = {"error": exc.name, "details": {"reason": exc.description}, "timestamp": utc_now()}
        return jsonify(response), exc.code

    @app.errorhandler(Exception)
    def internal_error(exc: Exception):
        return (
            jsonify({"error": "Internal server error", "details": {"reason": str(exc)}, "timestamp": utc_now()}),
            500,
        )

    @app.get("/health")
    def health() -> Any:
        return jsonify({"status": "ok", "timestamp": utc_now()})

    @app.get("/languages")
    def languages() -> Any:
        return jsonify(
            {
                "languages": [
                    {"code": "eng_Latn", "label": "English"},
                    {"code": "mlt_Latn", "label": "Maltese"},
                ]
            }
        )

    @app.get("/datasets")
    def list_datasets() -> Any:
        state = store.load()
        datasets = list(state["datasets"].values())
        return jsonify({"datasets": datasets, "count": len(datasets)})

    @app.get("/datasets/<dataset_id>")
    def get_dataset(dataset_id: str) -> Any:
        state = store.load()
        dataset = state["datasets"].get(dataset_id)
        if not dataset:
            raise ApiError(f"Dataset '{dataset_id}' not found", 404)
        return jsonify({"dataset": dataset})

    def get_dataset_or_404(dataset_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
        state = store.load()
        dataset = state["datasets"].get(dataset_id)
        if not dataset:
            raise ApiError(f"Dataset '{dataset_id}' not found", 404)
        records_map = state["records"].setdefault(dataset_id, {})
        return state, records_map

    @app.get("/datasets/<dataset_id>/records")
    def list_records(dataset_id: str) -> Any:
        _, records_map = get_dataset_or_404(dataset_id)

        order = request.args.get("order", "natural")
        if order not in ORDERS:
            raise ApiError("order must be one of natural|shuffle", 400)

        seed = parse_optional_int("seed")
        batch_size = parse_positive_int("batch_size", 100)
        cursor = parse_positive_int("cursor", 0, minimum=0, maximum=10_000_000)

        language_filter = request.args.get("language")
        synthetic_filter = request.args.get("synthetic_status")

        records = list(records_map.values())
        if language_filter:
            records = [row for row in records if row.get("language") == language_filter]
        if synthetic_filter:
            records = [row for row in records if row.get("synthetic_status") == synthetic_filter]

        if order == "shuffle":
            if seed is not None:
                rng = random.Random(seed)
                rng.shuffle(records)
            else:
                random.shuffle(records)

        total = len(records)
        end = cursor + batch_size
        batch = records[cursor:end]
        next_cursor = end if end < total else None

        return jsonify(
            {
                "dataset_id": dataset_id,
                "total_records": total,
                "batch_size": batch_size,
                "cursor": cursor,
                "next_cursor": next_cursor,
                "order": order,
                "seed": seed,
                "data": batch,
            }
        )

    @app.get("/datasets/<dataset_id>/records/<record_id>")
    def get_record(dataset_id: str, record_id: str) -> Any:
        _, records_map = get_dataset_or_404(dataset_id)
        record = records_map.get(record_id)
        if not record:
            raise ApiError(f"Record '{record_id}' not found", 404)
        return jsonify({"record": record})

    @app.post("/datasets/<dataset_id>/splits/sample")
    def sample_splits(dataset_id: str) -> Any:
        payload = request.get_json(silent=True) or {}
        splits = payload.get("splits")
        if not isinstance(splits, dict) or not splits:
            raise ApiError("splits must be a non-empty object", 400)

        order = payload.get("order", "shuffle")
        if order not in ORDERS:
            raise ApiError("order must be one of natural|shuffle", 400)

        seed = payload.get("seed")
        disjoint = payload.get("disjoint", True)
        filters = payload.get("filters", {})

        _, records_map = get_dataset_or_404(dataset_id)
        records = list(records_map.values())
        if language := filters.get("language"):
            records = [item for item in records if item.get("language") == language]
        if synthetic_status := filters.get("synthetic_status"):
            records = [item for item in records if item.get("synthetic_status") == synthetic_status]

        if order == "shuffle":
            rng = random.Random(seed)
            rng.shuffle(records)

        cursor = 0
        response_splits: dict[str, list[dict[str, Any]]] = {}
        for split_name, split_size in splits.items():
            if not isinstance(split_size, int) or split_size < 0:
                raise ApiError(f"split '{split_name}' must be a non-negative integer", 400)

            if disjoint:
                split_data = records[cursor : cursor + split_size]
                cursor += split_size
            else:
                split_data = records[:split_size]
            response_splits[split_name] = split_data

        return jsonify(
            {
                "dataset_id": dataset_id,
                "order": order,
                "seed": seed,
                "disjoint": disjoint,
                "splits": response_splits,
            }
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
