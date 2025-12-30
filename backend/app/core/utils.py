from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import uuid
from bson import ObjectId


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_current_timestamp() -> datetime:
    return datetime.utcnow()


def normalize_tags(tags: Union[List[str], str]) -> List[str]:
    if isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(',')]
    return [tag.lower().strip() for tag in tags if tag.strip()]


def validate_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def paginate_results(
    items: List[Any], 
    page: int = 1, 
    per_page: int = 20
) -> Dict[str, Any]:
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = items[start:end]
    
    return {
        "items": paginated_items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


def create_response(
    success: bool = True, 
    message: str = "Success", 
    data: Optional[Any] = None,
    error: Optional[str] = None
) -> Dict[str, Any]:
    response = {
        "success": success,
        "message": message,
        "timestamp": get_current_timestamp()
    }
    
    if data is not None:
        response["data"] = data
    
    if error is not None:
        response["error"] = error
    
    return response