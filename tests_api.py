import json
import tempfile
import unittest
from pathlib import Path

from app import create_app


class ApiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store_path = Path(self.temp_dir.name) / "store.json"
        app = create_app(
            {"TESTING": True, "DATA_STORE_PATH": self.store_path, "ENABLE_ADMIN_ENDPOINTS": False}
        )
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _seed_store(self, record_count: int = 0) -> None:
        dataset_id = "court_orders"
        records = {}
        for idx in range(1, record_count + 1):
            records[f"r{idx}"] = {
                "id": f"r{idx}",
                "dataset_id": dataset_id,
                "text": f"text-{idx}",
                "language": "eng_Latn",
                "language_pair": None,
                "synthetic_status": "unknown",
                "translation_metadata": {},
                "provenance": {
                    "source_text": "Manual registry export",
                    "source_type": "manual_entry",
                },
                "attributes": {},
                "created_at": "2026-01-01T10:00:00+00:00",
                "updated_at": "2026-01-01T10:00:00+00:00",
            }

        state = {
            "datasets": {
                dataset_id: {
                    "id": dataset_id,
                    "summary": "Court order metadata.",
                    "description": "A few sentences describing the dataset.",
                    "language_mode": "bilingual_aligned",
                    "synthetic_status": "non_synthetic",
                    "synthetic_details": {},
                    "provenance": {
                        "source_url": "https://example.com/public-registry",
                        "source_type": "web",
                    },
                    "created_at": "2026-01-01T10:00:00+00:00",
                    "updated_at": "2026-01-01T10:00:00+00:00",
                }
            },
            "records": {dataset_id: records},
        }
        self.store_path.write_text(json.dumps(state), encoding="utf-8")

    def _load_store(self) -> dict:
        return json.loads(self.store_path.read_text(encoding="utf-8"))

    def test_public_dataset_mutation_endpoints_are_disabled(self) -> None:
        self._seed_store()

        create_response = self.client.post(
            "/datasets",
            json={
                "id": "bad_dataset",
                "summary": "Should not be created publicly.",
                "language_mode": "monolingual",
                "synthetic_status": "unknown",
                "provenance": {"source_url": "https://example.com"},
            },
        )
        update_response = self.client.patch("/datasets/court_orders", json={"summary": "changed"})
        delete_response = self.client.delete("/datasets/court_orders")

        self.assertEqual(create_response.status_code, 405)
        self.assertEqual(update_response.status_code, 405)
        self.assertEqual(delete_response.status_code, 405)
        self.assertEqual(
            self._load_store()["datasets"]["court_orders"]["summary"],
            "Court order metadata.",
        )

    def test_public_record_mutation_endpoints_are_disabled(self) -> None:
        self._seed_store(record_count=1)

        create_response = self.client.post(
            "/datasets/court_orders/records",
            json={
                "id": "r2",
                "text": "hello",
                "language": "eng_Latn",
                "provenance": {"source_text": "manual"},
            },
        )
        update_response = self.client.patch(
            "/datasets/court_orders/records/r1",
            json={"text": "changed"},
        )
        delete_response = self.client.delete("/datasets/court_orders/records/r1")

        self.assertEqual(create_response.status_code, 405)
        self.assertEqual(update_response.status_code, 405)
        self.assertEqual(delete_response.status_code, 405)
        self.assertEqual(self._load_store()["records"]["court_orders"]["r1"]["text"], "text-1")

    def test_batch_defaults_to_natural_order(self) -> None:
        self._seed_store(record_count=3)

        response = self.client.get("/datasets/court_orders/records")
        body = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["order"], "natural")
        self.assertEqual(body["batch_size"], 100)
        self.assertEqual([item["id"] for item in body["data"]], ["r1", "r2", "r3"])

    def test_batch_shuffle_is_reproducible_with_seed(self) -> None:
        self._seed_store(record_count=5)

        first = self.client.get(
            "/datasets/court_orders/records?order=shuffle&seed=42&batch_size=5"
        ).get_json()
        second = self.client.get(
            "/datasets/court_orders/records?order=shuffle&seed=42&batch_size=5"
        ).get_json()

        self.assertEqual(
            [item["id"] for item in first["data"]],
            [item["id"] for item in second["data"]],
        )

    def test_split_sampling_returns_disjoint_sets_without_mutating_data(self) -> None:
        self._seed_store(record_count=10)
        before = self._load_store()

        response = self.client.post(
            "/datasets/court_orders/splits/sample",
            json={
                "splits": {"dev": 3, "test": 3, "eval": 2},
                "order": "shuffle",
                "seed": 12,
                "disjoint": True,
            },
        )
        body = response.get_json()

        self.assertEqual(response.status_code, 200)
        all_ids = []
        for split_name in ["dev", "test", "eval"]:
            ids = [item["id"] for item in body["splits"][split_name]]
            all_ids.extend(ids)
        self.assertEqual(len(all_ids), len(set(all_ids)))
        self.assertEqual(self._load_store(), before)


if __name__ == "__main__":
    unittest.main()
