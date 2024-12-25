import os


class FileManager:

    def has_similar_extension(self, extension: tuple, files: list):
        for wrapper in files:
            iter_extension = wrapper[len(wrapper) - 1]
            if iter_extension == extension[len(extension) - 1]: continue
            return False

        return True

    def get_extension(self, file):
        return os.path.splitext(file)

    def get_all_files(self, path: str) -> list:
        if path == '': return list()
        return os.listdir(path)

    def get_path_files_by_extension(self, path: str, extension: str) -> list:
        if not os.path.isdir(path):
            raise NotADirectoryError("Путь не ведет до директории")

        return list(filter(lambda name: name[-len(extension):] == extension, os.listdir(path)))

    def get_path_files_with_substring(self, path: str, substring: str, start: bool = False) -> list:
        if not os.path.isdir(path):
            raise NotADirectoryError("Путь не ведет до директории")

        return list(filter(lambda name: str(name).startswith(substring) if start else str(name).endswith(substring),
                           os.listdir(path)))

    def get_path_files_contains_substring(self, path: str, substring: str) -> list:
        if not os.path.isdir(path):
            raise NotADirectoryError("Путь не ведет до директории")

        return list(filter(lambda name: str(name).__contains__(substring), os.listdir(path)))

    def get_path_files_by_extensions(self, path: str, *extensions) -> list:
        if not os.path.isdir(path):
            raise NotADirectoryError("Путь не ведет до директории")

        files = []
        for extension in extensions:
            for file in os.listdir(path):
                if not os.path.basename(file)[-len(extension):].__contains__(extension): continue
                files.append(file)

        return files
