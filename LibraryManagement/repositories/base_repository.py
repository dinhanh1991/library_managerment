import json


class JsonRepository:
    """Base class for repositories that persist a list of model objects as JSON."""

    FILE_PATH = None
    ENTITY_NAME = "dữ liệu"

    def _load_json_list(self, factory=None):
        try:
            with self.FILE_PATH.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            raise ValueError(f"File {self.ENTITY_NAME} không hợp lệ: {e}") from e

        if not isinstance(data, list):
            raise ValueError(f"Dữ liệu {self.ENTITY_NAME} phải có dạng danh sách JSON.")

        if factory is None:
            return data

        items = []
        for item in data:
            if not isinstance(item, dict):
                raise ValueError(f"Mỗi dữ liệu {self.ENTITY_NAME} phải có dạng object JSON.")
            items.append(factory(item))
        return items

    def _save_json_list(self, items):
        self.FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        serialized = [item.to_dict() for item in items]
        with self.FILE_PATH.open("w", encoding="utf-8") as file:
            json.dump(serialized, file, ensure_ascii=False, indent=4)
