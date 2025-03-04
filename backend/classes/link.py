from datetime import datetime

class Link():
    def __init__(self, id: int, image_id: int, key: str, limit: int, created_at: datetime) -> None:
        self.id = id
        self.image_id = image_id
        self.key = key
        self.limit = limit
        self.created_at = created_at

    def toJSON(self) -> dict:
        return {
            "id": self.id,
            "image_id": self.image_id,
            "key": self.key,
            "limit": self.limit,
            "created_at": self.created_at
        }