from PIL import Image
from docx.api import Document
from pdf2docx import Converter

from core.file_manager import FileManager


class Feature:

    def __init__(self):
        self.file_manager = FileManager()

    def convert_to_pdf(self, path: str, *files: str):
        for wrapper in files:
            for file_name in wrapper:
                doc = Document(path + '/' + fr'{file_name}')
                try:
                    doc.save(path + fr'\converted-{file_name[:-4]}.pdf')
                    print(f"Вы успешно конвертировали файл в '*.pdf' (Файл: {path + '/' + file_name})!")
                except Exception:
                    print("Во время конвертации (docx -> pdf) произошла непредвиденная ошибка!")

    def convert_to_docx(self, path: str, *files: str):
        for wrapper in files:
            for file_name in wrapper:
                provider = Converter(path + '/' + fr'{file_name}')
                try:
                    provider.convert(path + fr"\converted-{file_name[:-3]}.docx")
                except Exception:
                    print("Произошла ошибка при конвертации (pdf -> docx). Повторите попытку позже.")

    def compress_image(self, path: str, *files):
        for wrapper in files:
            for file_name in wrapper:
                image_file = Image.open(path + '/' + fr'{file_name}')
                try:
                    image_file.save(path + fr'\compressed-{file_name}', quality=50)
                except Exception:
                    print("Произошла ошибка при cохранение изображения. Повторите попытку позже.")