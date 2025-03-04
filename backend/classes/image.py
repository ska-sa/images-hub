from datetime import datetime

class Image():
    def __init__(self, id: int, high_res_img_fname: str, low_res_img_fname: str, metadata: str, created_at: datetime) -> None:
        self.id = id
        self.high_res_img_fname = high_res_img_fname
        self.low_res_img_fname = low_res_img_fname
        self.metadata = metadata
        self.created_at = created_at

    def toJSON(self) -> dict:
        return {
            "id": self.id,
            "high_res_img_fname": self.high_res_img_fname,
            "low_res_img_fname": self.low_res_img_fname,
            "metadata": self.metadata,
            "created_at": self.created_at
        }