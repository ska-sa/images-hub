from datetime import datetime

class Image():
    def __init__(self, id: int, high_res_image_filename: str, low_res_image_filename: str, metadata: str, created_at: datetime) -> None:
        self.id = id
        self.high_res_image_filename = high_res_image_filename
        self.low_res_image_filename = low_res_image_filename
        self.metadata = metadata
        self.created_at = created_at

    def toJSON(self) -> dict:
        return {
            "id": self.id,
            "high_res_image_filename": self.high_res_image_filename,
            "low_res_image_filename": self.low_res_image_filename,
            "metadata": self.metadata,
            "created_at": self.created_at
        }