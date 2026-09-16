import json
from pathlib import Path

from LibraryManagement.models.borrower import Borrower


class BorrowerRepository:

    # Đường dẫn file lưu dữ liệu người mượn
    FILE_PATH = Path(__file__).resolve().parents[1] / "data" / "borrowers_list.json"

    # Đọc danh sách người mượn từ file
    def load_borrowers(self):

        try:
            # Mở file JSON để đọc
            with open(self.FILE_PATH, "r", encoding="utf-8") as file:

                # Đọc dữ liệu từ file
                data = json.load(file)

            # Chuyển Dictionary thành đối tượng Borrower
            borrowers = [
                Borrower.from_dict(borrower_data, default_status="borrowed")
                for borrower_data in data
            ]

            return borrowers

        # Nếu file chưa tồn tại thì trả về danh sách rỗng
        except FileNotFoundError:
            return []

    # Lưu danh sách người mượn vào file
    def save_borrowers(self, borrowers):

        try:
            data = []

            # Chuyển từng đối tượng Borrower thành Dictionary
            for borrower in borrowers:
                data.append(borrower.to_dict())

            # Mở file để ghi dữ liệu
            with open(self.FILE_PATH, "w", encoding="utf-8") as file:

                # Lưu dữ liệu dưới dạng JSON
                json.dump(data, file, ensure_ascii=False, indent=4)

        # Xử lý lỗi khi lưu file
        except OSError as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")