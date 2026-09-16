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
        return Reader(
            reader_id=data.get("reader_id"),
            name=data.get("name"),
        )
