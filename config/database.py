import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import DATABASE_URL, BASE_DIR

logger = logging.getLogger(__name__)

Base = declarative_base()

# Global Engine & Session Factory
engine = None
SessionLocal = None


def get_engine():
    global engine
    if engine is not None:
        return engine

    target_url = DATABASE_URL
    try:
        if target_url.startswith("mysql"):
            # Attempt to connect to MySQL
            engine = create_engine(
                target_url,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False
            )
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Successfully connected to MySQL database.")
        else:
            engine = create_engine(
                target_url,
                connect_args={"check_same_thread": False} if "sqlite" in target_url else {},
                echo=False
            )
            logger.info("Connected to SQLite database.")
    except Exception as e:
        logger.warning(f"Failed to connect to configured DB ({target_url}): {e}. Falling back to local SQLite.")
        sqlite_path = BASE_DIR / "smart_tourism.db"
        engine = create_engine(
            f"sqlite:///{sqlite_path}",
            connect_args={"check_same_thread": False},
            echo=False
        )

    return engine


def get_session():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return SessionLocal()


def _prepare_query_and_params(query_str, params):
    if params and isinstance(params, (list, tuple)) and "?" in query_str:
        parts = query_str.split("?")
        new_query = ""
        new_params = {}
        for i in range(len(params)):
            new_query += parts[i] + f":p{i}"
            new_params[f"p{i}"] = params[i]
        if len(parts) > len(params):
            new_query += parts[-1]
        return new_query, new_params
    return query_str, params or {}


def fetch_all(query_str, params=None):
    """Executes a SELECT query and returns a list of dictionaries."""
    engine = get_engine()
    q_str, p_dict = _prepare_query_and_params(query_str, params)
    with engine.connect() as conn:
        result = conn.execute(text(q_str), p_dict)
        return [dict(row._mapping) for row in result]


def fetch_one(query_str, params=None):
    """Executes a SELECT query and returns a single dictionary or None."""
    engine = get_engine()
    q_str, p_dict = _prepare_query_and_params(query_str, params)
    with engine.connect() as conn:
        result = conn.execute(text(q_str), p_dict)
        row = result.fetchone()
        return dict(row._mapping) if row else None


def execute_query(query_str, params=None):
    """Executes an INSERT, UPDATE, or DELETE query and commits."""
    engine = get_engine()
    q_str, p_dict = _prepare_query_and_params(query_str, params)
    with engine.begin() as conn:
        result = conn.execute(text(q_str), p_dict)
        return result.lastrowid if hasattr(result, "lastrowid") else None


def init_db():
    """Initializes the database schema and default seed data if needed."""
    from database.queries import init_schema_and_seed
    init_schema_and_seed()
