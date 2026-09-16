class Reader:
    def __init__(self, reader_id, name):
        self.reader_id = reader_id
        self.name = name

    def to_dict(self):
        return {
            "reader_id": self.reader_id,
            "name": self.name,
        }

    @staticmethod
    def from_dict(data):
        if "reader_id" not in data or "name" not in data:
            raise ValueError("Dữ liệu độc giả thiếu trường bắt buộc")
        if not isinstance(data["reader_id"], str) or not data["reader_id"].strip():
            raise ValueError("reader_id của độc giả không hợp lệ")
        if not isinstance(data["name"], str) or not data["name"].strip():
            raise ValueError("name của độc giả không hợp lệ")
        return Reader(
            reader_id=data["reader_id"],
            name=data["name"],
        )
