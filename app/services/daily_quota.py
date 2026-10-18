from sqlalchemy import text
from app.database import engine

DAILY_LIMIT = 100

def check_daily_quota() -> bool:
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS rag_daily_quota (day date PRIMARY KEY, count integer NOT NULL DEFAULT 0)"))
        result = conn.execute(text("INSERT INTO rag_daily_quota (day, count) VALUES ((CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Shanghai')::date, 1) ON CONFLICT (day) DO UPDATE SET count = rag_daily_quota.count + 1 WHERE rag_daily_quota.count < :cap RETURNING count"), {"cap": DAILY_LIMIT}).scalar_one_or_none()
        return result is not None
