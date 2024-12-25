import os


class FileManager:

    def get_path_files_by_extension(self, path: str, extension: str):
        if not os.path.isdir(path):
            raise NotADirectoryError("Путь не ведет до директории")

        return list(filter(lambda name: name[-len(extension):] == extension, os.listdir(path)))

    def get_path_files_with_substring(self, path: str, substring: str, start: bool = False):
        if not os.path.isdir(path):
            raise NotADirectoryError("Путь не ведет до директории")

        return list(filter(lambda name: str(name).startswith(substring) if start else str(name).endswith(substring),
                           os.listdir(path)))

    def get_path_files_contains_substring(self, path: str, substring: str):
        if not os.path.isdir(path):
            raise NotADirectoryError("Путь не ведет до директории")

        return list(filter(lambda name: str(name).__contains__(substring), os.listdir(path)))

    def get_path_files_by_extensions(self, path: str, *extensions):
        if not os.path.isdir(path):
            raise NotADirectoryError("Путь не ведет до директории")

        files = []
        for extension in extensions:
            for file in os.listdir(path):
                if not os.path.basename(file)[-len(extension):].__contains__(extension): continue
                files.append(file)

        return files
