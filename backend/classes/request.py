from datetime import datetime

class Request():
    def __init__(self, id: int, user_id: int, img_id: int, reason: str, status: int, created_at: datetime) -> None:
        self.id = id
        self.user_id = user_id
        self.img_id = img_id
        self.reason = reason
        self.status = status
        self.created_at = created_at

    def toJSON(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_id": self.img_id,
            "reason": self.reason,
            "status": self.status,
            "created_at": self.created_at
        }