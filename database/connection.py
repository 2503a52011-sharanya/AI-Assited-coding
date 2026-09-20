import logging
import uuid
import copy
from typing import Dict, Any, List, Optional
from config.settings import settings

logger = logging.getLogger(__name__)

class InMemoryCollection:
    """
    Robust in-memory MongoDB-compatible collection fallback.
    Provides PyMongo-like API so the app functions seamlessly if MongoDB server is offline.
    """
    def __init__(self, name: str):
        self.name = name
        self.documents: List[Dict[str, Any]] = []

    def _matches(self, doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
        if not query:
            return True
        for k, v in query.items():
            if k == "$or" and isinstance(v, list):
                if not any(self._matches(doc, sub_q) for sub_q in v):
                    return False
            elif isinstance(v, dict):
                # Simple operator checks
                doc_val = doc.get(k)
                if "$in" in v:
                    if doc_val not in v["$in"]:
                        return False
                elif "$regex" in v:
                    regex_str = v["$regex"]
                    ignore_case = v.get("$options") == "i"
                    val_str = str(doc_val or "")
                    if ignore_case:
                        if regex_str.lower() not in val_str.lower():
                            return False
                    else:
                        if regex_str not in val_str:
                            return False
                elif "$gte" in v and (doc_val is None or doc_val < v["$gte"]):
                    return False
                elif "$lte" in v and (doc_val is None or doc_val > v["$lte"]):
                    return False
            else:
                if doc.get(k) != v:
                    return False
        return True

    def insert_one(self, document: Dict[str, Any]):
        doc_copy = copy.deepcopy(document)
        if "_id" not in doc_copy:
            doc_copy["_id"] = str(uuid.uuid4())
        self.documents.append(doc_copy)
        class InsertResult:
            inserted_id = doc_copy["_id"]
        return InsertResult()

    def find_one(self, query: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        query = query or {}
        for doc in self.documents:
            if self._matches(doc, query):
                return copy.deepcopy(doc)
        return None

    def find(self, query: Optional[Dict[str, Any]] = None):
        query = query or {}
        results = [copy.deepcopy(doc) for doc in self.documents if self._matches(doc, query)]
        
        class Cursor:
            def __init__(self, items):
                self._items = items
            def sort(self, key_or_list, direction=1):
                if isinstance(key_or_list, str):
                    self._items.sort(key=lambda x: x.get(key_or_list, 0), reverse=(direction == -1))
                elif isinstance(key_or_list, list) and key_or_list:
                    key, d = key_or_list[0]
                    self._items.sort(key=lambda x: x.get(key, 0), reverse=(d == -1))
                return self
            def limit(self, n: int):
                self._items = self._items[:n]
                return self
            def __iter__(self):
                return iter(self._items)
            def __len__(self):
                return len(self._items)
        
        return Cursor(results)

    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]):
        for doc in self.documents:
            if self._matches(doc, query):
                if "$set" in update:
                    doc.update(update["$set"])
                if "$push" in update:
                    for field, val in update["$push"].items():
                        if field not in doc or not isinstance(doc[field], list):
                            doc[field] = []
                        doc[field].append(val)
                class UpdateResult:
                    modified_count = 1
                return UpdateResult()
        class UpdateResult:
            modified_count = 0
        return UpdateResult()

    def delete_one(self, query: Dict[str, Any]):
        for i, doc in enumerate(self.documents):
            if self._matches(doc, query):
                self.documents.pop(i)
                class DeleteResult:
                    deleted_count = 1
                return DeleteResult()
        class DeleteResult:
            deleted_count = 0
        return DeleteResult()

    def count_documents(self, query: Optional[Dict[str, Any]] = None) -> int:
        query = query or {}
        return sum(1 for doc in self.documents if self._matches(doc, query))

    def distinct(self, key: str) -> List[Any]:
        vals = set()
        for doc in self.documents:
            if key in doc:
                vals.add(doc[key])
        return list(vals)


class DatabaseManager:
    """
    Unified database manager.
    Connects to live MongoDB using MONGODB_URI when accessible,
    or falls back smoothly to in-memory store without crashing.
    """
    COLLECTIONS = [
        "users", "providers", "trips", "destinations", "hotels",
        "restaurants", "transportation", "activities", "bookings",
        "reviews", "favorites", "notifications", "weather_cache",
        "ai_recommendations"
    ]

    def __init__(self):
        self.is_connected = False
        self.is_live_mongo = False
        self.client = None
        self.db = None
        self.fallback_collections: Dict[str, InMemoryCollection] = {
            col: InMemoryCollection(col) for col in self.COLLECTIONS
        }
        self._initialize()

    def _initialize(self):
        try:
            import pymongo
            uri = settings.MONGODB_URI
            if uri:
                # Test connection with 1.5s server timeout
                client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=1500)
                client.admin.command('ping')
                self.client = client
                self.db = client[settings.DATABASE_NAME]
                self.is_live_mongo = True
                self.is_connected = True
                logger.info("Successfully connected to live MongoDB instance.")
                return
        except Exception as e:
            logger.warning(f"Live MongoDB connection unavailable ({e}). Using in-memory database store.")

        self.is_live_mongo = False
        self.is_connected = True

    def get_collection(self, name: str):
        if self.is_live_mongo and self.db is not None:
            return self.db[name]
        return self.fallback_collections.setdefault(name, InMemoryCollection(name))

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": "online" if self.is_connected else "offline",
            "type": "MongoDB (Live)" if self.is_live_mongo else "In-Memory Store (Resilient)",
            "database": settings.DATABASE_NAME,
            "uri_configured": bool(settings.MONGODB_URI)
        }

db_manager = DatabaseManager()

def get_db_collection(collection_name: str):
    return db_manager.get_collection(collection_name)
