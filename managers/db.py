# data/db.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load from .env file
load_dotenv()



# read once at import time
_SUPABASE_URL = os.getenv("SUPABASE_URL")
_SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not _SUPABASE_URL or not _SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY environment variables must be set")

supa: Client = create_client(_SUPABASE_URL, _SUPABASE_KEY)

# ---- simple CRUD helpers ----
def insert(table: str, row: dict | list[dict]):
    resp = supa.table(table).insert(row).execute()
    data = resp.data
    if not data:
        raise RuntimeError("insert returned no data")
    first = data[0] if isinstance(data, list) else data
    try:
        return first["id"]
    except (TypeError, KeyError):
        raise RuntimeError("insert result missing 'id'")


def select(table: str, filters: dict | None = None) -> list[dict]:
    """Return list of dicts."""
    q = supa.table(table).select("*")
    if filters:
        for k, v in filters.items():
            q = q.eq(k, v)
    return q.execute().data

def update(table: str, filters: dict, values: dict) -> list[dict]:
    """Return updated rows."""
    q = supa.table(table).update(values)
    for k, v in filters.items():
        q = q.eq(k, v)
    return q.execute().data

def delete(table: str, filters: dict) -> list[dict]:
    """Return deleted rows."""
    q = supa.table(table).delete()
    for k, v in filters.items():
        q = q.eq(k, v)
    return q.execute().data