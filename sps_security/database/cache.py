"""
database/cache.py
A memória do antivírus usando SQLite.
Evita re-escanear o mesmo arquivo duas vezes.
"""

import sqlite3
from pathlib import Path
from datetime import datetime

DB_DIR = Path.home() / ".sps_security"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "cache.db"


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria todas as tabelas necessárias."""
    with _conn() as c:
        c.executescript("""
            CREATE TABLE IF NOT EXISTS scan_cache (
                sha256      TEXT PRIMARY KEY,
                result      TEXT NOT NULL,
                score       INTEGER NOT NULL,
                threat_name TEXT,
                scanned_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS quarantine_log (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                original_path   TEXT NOT NULL,
                quarantine_path TEXT NOT NULL,
                sha256          TEXT NOT NULL,
                threat_name     TEXT,
                quarantined_at  TEXT NOT NULL,
                restored        INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS scan_stats (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_path   TEXT NOT NULL,
                total_files INTEGER NOT NULL,
                clean       INTEGER NOT NULL,
                threats     INTEGER NOT NULL,
                suspicious  INTEGER NOT NULL,
                duration_s  REAL NOT NULL,
                scanned_at  TEXT NOT NULL
            );
        """)


def cache_get(sha256: str):
    init_db()
    with _conn() as c:
        row = c.execute(
            "SELECT * FROM scan_cache WHERE sha256 = ?", (sha256,)
        ).fetchone()
        if row:
            return dict(row)
    return None


def cache_set(sha256, result, score, threat_name=None):
    init_db()
    with _conn() as c:
        c.execute("""
            INSERT OR REPLACE INTO scan_cache
            (sha256, result, score, threat_name, scanned_at)
            VALUES (?, ?, ?, ?, ?)
        """, (sha256, result, score, threat_name, datetime.now().isoformat()))


def quarantine_add(original_path, quarantine_path, sha256, threat_name=None):
    init_db()
    with _conn() as c:
        c.execute("""
            INSERT INTO quarantine_log
            (original_path, quarantine_path, sha256, threat_name, quarantined_at)
            VALUES (?, ?, ?, ?, ?)
        """, (original_path, quarantine_path, sha256, threat_name,
              datetime.now().isoformat()))


def quarantine_list():
    init_db()
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM quarantine_log ORDER BY quarantined_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def quarantine_restore_mark(quarantine_path):
    init_db()
    with _conn() as c:
        c.execute(
            "UPDATE quarantine_log SET restored = 1 WHERE quarantine_path = ?",
            (quarantine_path,)
        )


def stats_add(scan_path, total, clean, threats, suspicious, duration):
    init_db()
    with _conn() as c:
        c.execute("""
            INSERT INTO scan_stats
            (scan_path, total_files, clean, threats, suspicious, duration_s, scanned_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (scan_path, total, clean, threats, suspicious, duration,
              datetime.now().isoformat()))


def get_stats():
    init_db()
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM scan_stats ORDER BY scanned_at DESC LIMIT 20"
        ).fetchall()
        return [dict(r) for r in rows]
