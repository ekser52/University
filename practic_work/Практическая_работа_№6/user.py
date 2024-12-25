from typing import Any


class User:

    def __init__(self, work_dir: str):
        self.work_dir = work_dir

    def select(self, objects: dict[str, Any]) -> tuple:
        operation_id = self.await_value(
            lambda value: str(value).isdigit(),
            f"Необходимо ввести число!",
            "Выберите действие"
        )

        if not (0 <= int(operation_id) < len(objects)):
            print(f"Число должно быть в диапозоне [0;{len(objects.keys()) - 1}]")
            return None, None
            pass

        return str(operation_id), objects[operation_id]

    @staticmethod
    def await_value(validator, error_message: str, view_text: str):
        entered_value = None
        attempt = 1
        while entered_value is None or not validator(entered_value):
            if attempt > 1:
                print(error_message)

            entered_value = input(f'{view_text}: ')
            attempt += 1

            if validator(entered_value):
                return entered_value

    def set_work_dir(self, new_dir: str):
        self.work_dir = new_dir

    def get_work_dir(self) -> str:
        return self.work_dir
