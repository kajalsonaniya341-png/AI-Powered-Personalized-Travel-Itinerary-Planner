"""Shared test setup.

Tests NEVER touch a real MongoDB: API tests replace the database dependency with
`FakeDB`, a tiny in-memory stand-in. No MONGODB_URI is needed.
"""
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
# Must be set before `app.config` is imported.
os.environ["JWT_SECRET"] = "test-secret-only-for-automated-tests-0123456789-abcdef"
os.environ["MONGODB_URI"] = ""
os.environ["SEED_ON_STARTUP"] = "false"


def load_sample_places() -> list:
    return json.loads((ROOT / "data" / "places.json").read_text(encoding="utf-8"))["places"]


class FakeCollection:
    """Supports just the PyMongo calls this project uses (equality filters only)."""

    def __init__(self):
        self.docs = []
        self.unique_keys = []

    def create_index(self, keys, unique=False, **_):
        if unique:
            self.unique_keys.append([keys] if isinstance(keys, str) else [k for k, _ in keys])

    @staticmethod
    def _match(doc, query):
        return all(doc.get(k) == v for k, v in (query or {}).items())

    def _check_unique(self, new_doc):
        from pymongo.errors import DuplicateKeyError

        for fields in self.unique_keys:
            for doc in self.docs:
                if all(doc.get(f) == new_doc.get(f) for f in fields):
                    raise DuplicateKeyError("duplicate key")

    def find(self, query=None, *_, **__):
        return [dict(d) for d in self.docs if self._match(d, query)]

    def find_one(self, query=None, *_, **__):
        for d in self.docs:
            if self._match(d, query):
                return dict(d)
        return None

    def insert_one(self, doc):
        from bson import ObjectId

        self._check_unique(doc)
        doc["_id"] = ObjectId()
        self.docs.append(dict(doc))
        return SimpleNamespace(inserted_id=doc["_id"])

    def update_one(self, query, update, upsert=False):
        from bson import ObjectId

        for d in self.docs:
            if self._match(d, query):
                before = dict(d)
                d.update(update.get("$set", {}))
                return SimpleNamespace(upserted_id=None, modified_count=int(before != d))
        if upsert:
            new = {**query, **update.get("$set", {}), "_id": ObjectId()}
            self.docs.append(new)
            return SimpleNamespace(upserted_id=new["_id"], modified_count=0)
        return SimpleNamespace(upserted_id=None, modified_count=0)

    def delete_one(self, query):
        for i, d in enumerate(self.docs):
            if self._match(d, query):
                del self.docs[i]
                return SimpleNamespace(deleted_count=1)
        return SimpleNamespace(deleted_count=0)


class FakeDB:
    def __init__(self):
        self.users, self.places, self.trips = FakeCollection(), FakeCollection(), FakeCollection()
        self.users.create_index("email", unique=True)
        self.places.create_index([("name", 1), ("city", 1)], unique=True)


@pytest.fixture
def sample_places():
    """Plain place dicts shaped like serialize_place() output (no database needed)."""
    from app.models.place import serialize_place

    return [serialize_place({**p, "_id": f"id{i}"}) for i, p in enumerate(load_sample_places())]


@pytest.fixture
def fake_db():
    pytest.importorskip("pymongo")
    db = FakeDB()
    for p in load_sample_places():
        db.places.insert_one(dict(p))
    return db


@pytest.fixture
def client(fake_db):
    for module in ("fastapi", "httpx", "bcrypt"):
        pytest.importorskip(module)
    from fastapi.testclient import TestClient

    from app.database import get_db
    from app.main import app

    app.dependency_overrides[get_db] = lambda: fake_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def register(client, username="alice", email="alice@example.com", password="correct-horse-1"):
    return client.post("/api/auth/register", json={"username": username, "email": email, "password": password})


@pytest.fixture
def auth_headers(client):
    token = register(client).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_headers(client):
    token = register(client, "bob", "bob@example.com").json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


PLAN_BODY = {"destination": "Jaipur", "days": 3, "budget": 15000, "travelers": 2,
             "interests": ["history", "culture"], "travel_style": "balanced"}
