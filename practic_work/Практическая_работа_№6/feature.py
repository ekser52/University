import os

from PIL import Image
from docx.api import Document
from pdf2docx import Converter

from user import User
from utils.file_manager import FileManager
from utils.render import ConsoleRender


class Feature:

    def __init__(self, entity: User):
        self.entity = entity
        self.path = entity.get_work_dir()

        self.file_manager = FileManager()

        if not os.path.exists(self.path):
            raise FileNotFoundError("Файл/директория не найден(-а)")

    def change_directory(self):
        new_path = self.entity.await_value(
            lambda path: os.path.isdir(path),
            "Путь не ведет до папки",
            "Введите путь до директории"
        )

        self.entity.set_work_dir(new_path)
        self.path = self.entity.get_work_dir()
        os.chdir(new_path)
        print(f"Вы успешно сменили директорию на {new_path}")

    def convert_to_pdf(self):
        files_with_extension = self.file_manager.get_path_files_by_extension(self.path, "docx")

        ConsoleRender.render_line(
            '\n'.join([
                (lambda index: f'{index}. ')(index) + (files_with_extension[index]) for index in
                range(len(files_with_extension))
            ])
        )

        file_id = int(self.entity.await_value(
            lambda value: str(value).isnumeric(),
            f"Индекс должен быть быть в диапозоне [0;{len(files_with_extension)}] && Тип: int",
            "Выберите номер файла для конвертации"
        ))

        if 0 <= file_id > len(files_with_extension):
            print(f"Индекс должен лежать в диапозоне [0,{len(files_with_extension) - 1}]")
            self.convert_to_docx()
            pass

        file = files_with_extension[file_id]

        doc = Document(self.path + fr'\{file}')
        try:
            doc.save(self.path + fr'\{file[:-4]}.pdf')
            print(f"Вы успешно конвертировали файл в '*.pdf' (Файл: {self.path + file})!")
        except Exception:
            print("Во время конвертации (docx -> pdf) произошла непредвиденная ошибка!")

    def convert_to_docx(self):
        files_with_extension = self.file_manager.get_path_files_by_extension(self.path, "pdf")

        ConsoleRender.render_line(
            '\n'.join([
                (lambda index: f'{index}. ')(index) + (files_with_extension[index]) for index in
                range(len(files_with_extension))
            ])
        )

        file_id = int(self.entity.await_value(
            lambda value: str(value).isnumeric(),
            f"Индекс должен числом (int)",
            "Выберите номер файла для конвертации"
        ))

        if 0 <= file_id > len(files_with_extension):
            print(f"Индекс должен лежать в диапозоне [0,{len(files_with_extension) - 1}]")
            self.convert_to_docx()
            pass

        file = files_with_extension[file_id]

        provider = Converter(self.path + fr'\{file}')
        try:
            provider.convert(self.path + fr"\converted-{file[:-3]}.docx")
        except Exception:
            print("Произошла ошибка при конвертации (pdf -> docx). Повторите попытку позже.")

    def compress_image(self):

        files_with_extensions = self.file_manager.get_path_files_by_extensions(self.path, "jpeg", 'jpg', 'png', 'gif')

        ConsoleRender.render_line(
            '\n'.join([
                (lambda index: f'{index}. ')(index) + (files_with_extensions[index]) for index in
                range(len(files_with_extensions))
            ])
        )

        file_id = self.entity.await_value(
            lambda value: str(value).isnumeric() or str(value) == '*',
            f"Индекс должен числом или действием (int)",
            "Выберите номер файла для конвертации (* - выбрать все)"
        )

        if file_id != '*' and 0 < int(file_id) > len(files_with_extensions):
            print(f"Индекс должен лежать в диапозоне [0,{len(files_with_extensions) - 1}] или быть *")
            self.compress_image()
            pass

        quality = int(self.entity.await_value(
            lambda value: str(value).isnumeric(),
            f"Процент сжатия должен быть числом (int)",
            "Введите качество фотографии (0-100)"
        ))

        if 0 <= int(quality) > 100:
            print("Процент сжатия должен лежать в диапозоне [0,100]")
            self.compress_image()
            pass

        image_tool = self.__ImageToolWrapper()

        if file_id == '*':
            for file in files_with_extensions:
                image_tool.save_with_argument(self.path, file, int(quality))
        else:
            image_tool.save_with_argument(self.path, files_with_extensions[int(file_id)], quality)

    def delete_group_files(self):

        actions_desc = [
            "Все файлы, начинающиеся на подстроку",
            "Все файлы, заканчиввающиеся на подстроку",
            "Все файлы, содержащие подстроку",
            "Все файлы по расширению подстроку",
        ]

        ConsoleRender.render_line(
            '\n'.join([
                (lambda index: f'{index}. ')(index) + (actions_desc[index]) for index in range(len(actions_desc))
            ])
        )

        def delete_startswith_substring(substring: str):
            files = self.file_manager.get_path_files_with_substring(self.path, substring, True)
            for file in files:
                os.remove(self.path + fr'\{file}')
                print(f"Removed {file}")

        def delete_endswith_substring(substring: str):
            files = self.file_manager.get_path_files_with_substring(self.path, substring)
            for file in files:
                os.remove(self.path + fr'\{file}')
                print(f"Removed {file}")
                
        def delete_contains_substring(substring: str):
            files = self.file_manager.get_path_files_contains_substring(self.path, substring)
            for file in files:
                os.remove(self.path + fr'\{file}')
                print(f"Removed {file}")

        def delete_with_extension_substring(extension: str):
            files = self.file_manager.get_path_files_by_extension(self.path, extension)
            for file in files:
                os.remove(self.path + fr'\{file}')
                print(f"Removed {file}")

        actions = {
            '0': lambda obj: delete_startswith_substring(obj),
            '1': lambda obj: delete_endswith_substring(obj),
            '2': lambda obj: delete_contains_substring(obj),
            '3': lambda obj: delete_with_extension_substring(obj)
        }

        action_id = self.entity.await_value(
            lambda value: str(value).isnumeric(),
            f"Индекс должен числом (int)",
            "Выберите номер файла для конвертации (* - выбрать все)"
        )

        argument = self.entity.await_value(
            lambda value: len(str(value)) != 0,
            f"Аргумент не может быть пустым!",
            "Введите аргумент для действия"
        )

        if 0 < int(action_id) >= len(actions.keys()):
            print(f"Индекс действия должен быть в диапозоне [0,{len(actions.keys()) - 1}]")
            self.compress_image()
            pass

        actions[action_id](argument)

    class __ImageToolWrapper:

        @staticmethod
        def save_with_argument(input_path: str, file: str, quality: int):
            image_file = Image.open(input_path + fr'\{file}')

            try:
                image_file.save(input_path + fr'\compressed-{file}', quality=quality)
            except Exception:
                print("Произошла ошибка при cохранение изображения. Повторите попытку позже.")
