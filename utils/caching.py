import json
import time
from database.queries import fetch_one, execute_query


def get_cached_api_response(cache_key: str):
    """Retrieves cached API response if not expired."""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    row = fetch_one(
        "SELECT response_json FROM api_cache WHERE cache_key = :key AND expires_at > :now",
        {"key": cache_key, "now": current_time}
    )
    if row:
        try:
            return json.loads(row["response_json"])
        except Exception:
            return None
    return None


def set_cached_api_response(cache_key: str, data: dict, ttl_seconds: int = 86400):
    """Saves API response with expiration TTL."""
    expires_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + ttl_seconds))
    execute_query("""
    INSERT INTO api_cache (cache_key, response_json, expires_at)
    VALUES (:key, :json, :exp)
    ON CONFLICT(cache_key) DO UPDATE SET
        response_json=excluded.response_json,
        expires_at=excluded.expires_at
    """, {"key": cache_key, "json": json.dumps(data), "exp": expires_at})
