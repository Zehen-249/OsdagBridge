"""
Project-tracking SQLite layer for OsdagBridge.

The database lives in the user's home directory at ``~/.osdagbridge/osdagbridge.db``
so it survives reinstalls, follows the standard pattern for desktop apps, and
stays isolated from the osdag-side project DB (which lives under
``osdag_gui/data/...``). The OsdagBridge plugin runs inside osdag_gui but
its project records go here, not into osdag_gui's own DB.
"""
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Schema constants ─────────────────────────────────────────────────────────
ID = "id"
PROJECT_NAME = "project_name"
PROJECT_PATH = "project_path"
MODULE_KEY = "module_key"
CREATION_DATE = "creation_date"
LAST_EDITED = "last_edited"
PROJECT_TABLE = "recent_projects"

DB_DIR = Path.home() / ".osdagbridge"
SQLITE_FILE = DB_DIR / "osdagbridge.db"


# ── Connection ───────────────────────────────────────────────────────────────

def _connect() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(SQLITE_FILE))
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ── Schema bootstrap ─────────────────────────────────────────────────────────

def init_project_db() -> None:
    """Idempotently create the ``recent_projects`` table.

    Safe to call from ``CustomWindow.__init__`` on every launch — uses
    ``CREATE TABLE IF NOT EXISTS`` so it is a no-op once the table exists.
    """
    with _connect() as conn:
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {PROJECT_TABLE} (
                {ID}            INTEGER PRIMARY KEY AUTOINCREMENT,
                {PROJECT_NAME}  TEXT NOT NULL,
                {PROJECT_PATH}  TEXT NOT NULL UNIQUE,
                {MODULE_KEY}    TEXT,
                {CREATION_DATE} TEXT,
                {LAST_EDITED}   TEXT
            );
            """
        )


# ── Record helpers ───────────────────────────────────────────────────────────

def insert_recent_project(data: dict) -> int | None:
    """UPSERT a project record, keyed on ``project_path``.

    On a path collision the existing row's name/module_key/last_edited are
    refreshed in place. Returns the row id of the inserted-or-updated record, or ``None`` on error.
    """
    now = datetime.now().isoformat(timespec="seconds")
    creation = data.get(CREATION_DATE, now)
    last_edited = data.get(LAST_EDITED, now)
    try:
        with _connect() as conn:
            conn.execute(
                f"""
                INSERT INTO {PROJECT_TABLE}
                    ({PROJECT_NAME}, {PROJECT_PATH}, {MODULE_KEY}, {CREATION_DATE}, {LAST_EDITED})
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT({PROJECT_PATH}) DO UPDATE SET
                    {PROJECT_NAME}  = excluded.{PROJECT_NAME},
                    {MODULE_KEY}    = excluded.{MODULE_KEY},
                    {LAST_EDITED}   = excluded.{LAST_EDITED};
                """,
                (data[PROJECT_NAME], data[PROJECT_PATH], data.get(MODULE_KEY), creation, last_edited),
            )
            conn.commit()
            row = conn.execute(
                f"SELECT {ID} FROM {PROJECT_TABLE} WHERE {PROJECT_PATH} = ?;",
                (data[PROJECT_PATH],),
            ).fetchone()
            return row[0] if row else None
    except sqlite3.Error as exc:
        print(f"[ERROR] insert_recent_project: {exc}")
        return None


def get_project_by_id(project_id: int) -> dict | None:
    """Return ``{ID, PROJECT_NAME, PROJECT_PATH}`` for ``project_id``, else ``None``.

    This is a simple lookup by ID, used to retrieve project information in the
    desktop app. The structure is designed to match the osdag_gui database
    schema for consistency.

    so the call site in ``CustomWindow.saveDesign`` reads 1:1 across both apps.
    """
    try:
        with _connect() as conn:
            row = conn.execute(
                f"SELECT {ID}, {PROJECT_NAME}, {PROJECT_PATH} "
                f"FROM {PROJECT_TABLE} WHERE {ID} = ?;",
                (project_id,),
            ).fetchone()
            if row:
                return {ID: row[0], PROJECT_NAME: row[1], PROJECT_PATH: row[2]}
            return None
    except sqlite3.Error as exc:
        print(f"[ERROR] get_project_by_id: {exc}")
        return None