"""
نظام إعدادات السيرفرات - SQLite Database V2
تحسينات: WAL + busy_timeout + معاملات ذرية + دعم حذف الإعدادات + Heartbeat
"""
import sqlite3
import os
import threading
import time
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv("SERVER_SETTINGS_DB", os.path.join(BASE_DIR, "server_settings.db"))

_local = threading.local()

# حقول الـ IDs
ID_FIELDS = ["admin_role_id", "ticket_role_id", "ticket_manager_role_id",
             "high_role_id", "auto_role_id", "log_channel_id",
             "ticket_category_id", "welcome_channel_id"]

# حقول الـ boolean
BOOL_FIELDS = ["spam_enabled", "flood_enabled", "mention_enabled",
               "invite_enabled", "badwords_enabled",
               "join_notification", "leave_notification"]


def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=30000")
    return conn


def init_db():
    """إنشاء جداول قاعدة البيانات"""
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS guild_settings (
            guild_id INTEGER PRIMARY KEY,
            guild_name TEXT NOT NULL DEFAULT '',
            admin_role_id INTEGER,
            ticket_role_id INTEGER,
            ticket_manager_role_id INTEGER,
            high_role_id INTEGER,
            auto_role_id INTEGER,
            log_channel_id INTEGER,
            ticket_category_id INTEGER,
            welcome_channel_id INTEGER,
            spam_enabled INTEGER DEFAULT 1,
            flood_enabled INTEGER DEFAULT 1,
            mention_enabled INTEGER DEFAULT 1,
            invite_enabled INTEGER DEFAULT 1,
            badwords_enabled INTEGER DEFAULT 1,
            join_notification INTEGER DEFAULT 1,
            leave_notification INTEGER DEFAULT 0,
            settings_version INTEGER NOT NULL DEFAULT 1,
            updated_at TEXT NOT NULL,
            updated_by TEXT DEFAULT ''
        );
        
        CREATE TABLE IF NOT EXISTS settings_audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER NOT NULL,
            guild_name TEXT DEFAULT '',
            user_id TEXT NOT NULL,
            user_name TEXT DEFAULT '',
            setting_key TEXT NOT NULL,
            old_value TEXT DEFAULT '',
            new_value TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS bot_guilds (
            guild_id INTEGER PRIMARY KEY,
            guild_name TEXT NOT NULL DEFAULT '',
            member_count INTEGER DEFAULT 0,
            bot_connected INTEGER DEFAULT 0,
            last_heartbeat TEXT DEFAULT '',
            roles_snapshot TEXT DEFAULT '[]',
            channels_snapshot TEXT DEFAULT '[]',
            updated_at TEXT NOT NULL
        );
        
        CREATE INDEX IF NOT EXISTS idx_audit_guild ON settings_audit_log(guild_id);
        CREATE INDEX IF NOT EXISTS idx_audit_id ON settings_audit_log(id);
    """)
    conn.commit()
    conn.close()


def get_guild_settings(guild_id: int):
    """جلب إعدادات سيرفر"""
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM guild_settings WHERE guild_id = ?", (guild_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)


def get_all_guilds() -> list:
    """جلب كل السيرفرات المسجلة"""
    conn = get_conn()
    rows = conn.execute("SELECT * FROM guild_settings ORDER BY guild_name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def _audit_value(value):
    """تحويل القيمة لتخزين في audit log"""
    if value is None:
        return ""
    return str(value)


def save_guild_settings(guild_id: int, data: dict, user_id: str = "", user_name: str = "") -> bool:
    """حفظ إعدادات سيرفر مع تسجيل التغييرات ودعم الحذف"""
    conn = get_conn()
    now = datetime.now(timezone.utc).isoformat()[:19]
    
    try:
        with conn:
            # جلب الإعدادات القديمة
            old = conn.execute(
                "SELECT * FROM guild_settings WHERE guild_id = ?", (guild_id,)
            ).fetchone()
            old_dict = dict(old) if old else {}
            
            # بناء القيم الجديدة - دعم الحذف الفعلي
            merged = {}
            for key in ID_FIELDS:
                if key in data:
                    merged[key] = data[key]  # يمكن أن  None (حذف)
                else:
                    merged[key] = old_dict.get(key)
            
            for key in BOOL_FIELDS:
                if key in data:
                    merged[key] = 1 if data[key] else 0
                else:
                    merged[key] = old_dict.get(key)
            
            # تحديث رقم الإصدار
            new_version = (old_dict.get("settings_version", 0) + 1) if old_dict else 1
            
            # تحديث أو إنشاء
            conn.execute("""
                INSERT INTO guild_settings (
                    guild_id, guild_name, admin_role_id, ticket_role_id,
                    ticket_manager_role_id, high_role_id, auto_role_id,
                    log_channel_id, ticket_category_id, welcome_channel_id,
                    spam_enabled, flood_enabled, mention_enabled, invite_enabled,
                    badwords_enabled, join_notification, leave_notification,
                    settings_version, updated_at, updated_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET
                    guild_name=excluded.guild_name,
                    admin_role_id=excluded.admin_role_id,
                    ticket_role_id=excluded.ticket_role_id,
                    ticket_manager_role_id=excluded.ticket_manager_role_id,
                    high_role_id=excluded.high_role_id,
                    auto_role_id=excluded.auto_role_id,
                    log_channel_id=excluded.log_channel_id,
                    ticket_category_id=excluded.ticket_category_id,
                    welcome_channel_id=excluded.welcome_channel_id,
                    spam_enabled=excluded.spam_enabled,
                    flood_enabled=excluded.flood_enabled,
                    mention_enabled=excluded.mention_enabled,
                    invite_enabled=excluded.invite_enabled,
                    badwords_enabled=excluded.badwords_enabled,
                    join_notification=excluded.join_notification,
                    leave_notification=excluded.leave_notification,
                    settings_version=excluded.settings_version,
                    updated_at=excluded.updated_at,
                    updated_by=excluded.updated_by
            """, (
                guild_id,
                data.get("guild_name") or old_dict.get("guild_name", ""),
                merged.get("admin_role_id"),
                merged.get("ticket_role_id"),
                merged.get("ticket_manager_role_id"),
                merged.get("high_role_id"),
                merged.get("auto_role_id"),
                merged.get("log_channel_id"),
                merged.get("ticket_category_id"),
                merged.get("welcome_channel_id"),
                merged.get("spam_enabled", 1),
                merged.get("flood_enabled", 1),
                merged.get("mention_enabled", 1),
                merged.get("invite_enabled", 1),
                merged.get("badwords_enabled", 1),
                merged.get("join_notification", 1),
                merged.get("leave_notification", 0),
                new_version,
                now,
                user_name
            ))
            
            # تسجيل التغييرات في Audit Log
            if old_dict:
                changes = []
                for key in ID_FIELDS + BOOL_FIELDS:
                    old_val = old_dict.get(key)
                    new_val = merged.get(key)
                    if _audit_value(old_val) != _audit_value(new_val):
                        changes.append((key, _audit_value(old_val), _audit_value(new_val)))
                
                for key, old_v, new_v in changes:
                    conn.execute("""
                        INSERT INTO settings_audit_log 
                        (guild_id, guild_name, user_id, user_name, setting_key, old_value, new_value, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (guild_id, data.get("guild_name") or old_dict.get("guild_name", ""), user_id, user_name, key, old_v, new_v, now))
            else:
                # تسجيل إنشاء جديد
                conn.execute("""
                    INSERT INTO settings_audit_log 
                    (guild_id, guild_name, user_id, user_name, setting_key, old_value, new_value, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (guild_id, data.get("guild_name", ""), user_id, user_name, "created", "", "تم إنشاء إعدادات السيرفر", now))
        
        return True
    except Exception as e:
        print(f"[DB ERROR] {e}", flush=True)
        return False
    finally:
        conn.close()


def get_audit_log(guild_id: int, limit: int = 50, offset: int = 0) -> list:
    """جلب سجل التغييرات لسيرفر مع pagination"""
    conn = get_conn()
    rows = conn.execute("""
        SELECT * FROM settings_audit_log 
        WHERE guild_id = ? 
        ORDER BY id DESC 
        LIMIT ? OFFSET ?
    """, (guild_id, limit, offset)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_audit_log_count(guild_id: int) -> int:
    """عدد سجلات التغييرات"""
    conn = get_conn()
    count = conn.execute(
        "SELECT COUNT(*) FROM settings_audit_log WHERE guild_id = ?", (guild_id,)
    ).fetchone()[0]
    conn.close()
    return count


def delete_guild_settings(guild_id: int) -> bool:
    """حذف إعدادات سيرفر"""
    conn = get_conn()
    try:
        with conn:
            conn.execute("DELETE FROM guild_settings WHERE guild_id = ?", (guild_id,))
            conn.execute("DELETE FROM settings_audit_log WHERE guild_id = ?", (guild_id,))
        return True
    finally:
        conn.close()


# ═══════════════════════════════════════════════════════════════
# Bot Heartbeat & Guild Snapshot
# ═══════════════════════════════════════════════════════════════

def update_bot_heartbeat(guild_id: int, guild_name: str = "", member_count: int = 0,
                         roles: list = None, channels: list = None):
    """تحديث حالة البوت في السيرفر"""
    conn = get_conn()
    now = datetime.now(timezone.utc).isoformat()[:19]
    try:
        with conn:
            conn.execute("""
                INSERT INTO bot_guilds (guild_id, guild_name, member_count, bot_connected, last_heartbeat, roles_snapshot, channels_snapshot, updated_at)
                VALUES (?, ?, ?, 1, ?, ?, ?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET
                    guild_name=excluded.guild_name,
                    member_count=excluded.member_count,
                    bot_connected=1,
                    last_heartbeat=excluded.last_heartbeat,
                    roles_snapshot=excluded.roles_snapshot,
                    channels_snapshot=excluded.channels_snapshot,
                    updated_at=excluded.updated_at
            """, (guild_id, guild_name, member_count, now,
                  str(roles or []), str(channels or []), now))
    finally:
        conn.close()


def set_bot_disconnected(guild_id: int):
    """تسجيل انقطاع البوت"""
    conn = get_conn()
    try:
        with conn:
            conn.execute(
                "UPDATE bot_guilds SET bot_connected = 0 WHERE guild_id = ?",
                (guild_id,)
            )
    finally:
        conn.close()


def get_bot_guilds() -> list:
    """جلب السيرفرات اللي البوت فيها"""
    conn = get_conn()
    rows = conn.execute("SELECT * FROM bot_guilds ORDER BY guild_name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_bot_guild(guild_id: int):
    """جلب سيرفر معين"""
    conn = get_conn()
    row = conn.execute("SELECT * FROM bot_guilds WHERE guild_id = ?", (guild_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def serialize_settings(s: dict) -> dict:
    """تحويل الإعدادات لصيغة آمنة لـ JavaScript"""
    out = dict(s)
    out["guild_id"] = str(out["guild_id"])
    for k in ID_FIELDS:
        if out.get(k) is not None:
            out[k] = str(out[k])
    for k in BOOL_FIELDS:
        out[k] = bool(out.get(k))
    return out


init_db()
