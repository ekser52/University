import typing

import PySimpleGUI as gui
from core.feature import FileManager
from core.feature import Feature


class GuiHandler:
    def __init__(self, instance: gui.Window):
        self.window = instance

    def handle_event(self, event_key: str, window: gui.Window, execute, event_filter=None):
        passed = True
        if event_filter is not None:
            passed = event_filter((event_key, window))

        if passed:
            if window == self.window:
                execute(self)

    def get_element_by_key(self, key: str):
        try:
            return self.window.find_element(key)
        except KeyError:
            print(f"Не удалось найти элемент с id {key}")

    def change_state_element(self, disabled, keys: list):
        for key in keys:
            self.window[key].update(disabled=disabled)

        self.window.refresh()

    def get_window_instance(self) -> gui.Window:
        return self.window

    def event(self):
        return self.EventHandler(self)

    class EventHandler:

        def __init__(self, gui_handler):
            self.gui_handler = typing.cast(GuiHandler, gui_handler)

            self.manager = FileManager()

        def change_directory_event(self, target_element: str, to_view: str):
            element_content = self.gui_handler.get_element_by_key(target_element)
            element_view = self.gui_handler.get_element_by_key(to_view)

            files = self.manager.get_all_files(str(element_content.get()))

            update = []
            for index, file in enumerate(files):
                file_info = self.manager.get_extension(file)

                if file_info[len(file_info) - 1].strip() in ['.pdf', '.docx', '.jpg', '.jpeg', '.gif']:
                    update.append(file)

            element_view.update(update)

        def select_files_event(self, container: str):
            element_content = self.gui_handler.get_element_by_key(container)
            selected_elements = element_content.get()

            elements = ['docx_to_pdf', 'pdf_to_docx', 'compress_image']
            self.gui_handler.change_state_element(False, elements)

            extensions = [self.manager.get_extension(file) for file in selected_elements]
            main_trace_extension = self.manager.get_extension(selected_elements[0])

            if not self.manager.has_similar_extension(main_trace_extension, extensions):
                self.gui_handler.change_state_element(True, elements)
            else:
                consumer = {
                    '.docx': 'docx_to_pdf',
                    '.pdf': 'pdf_to_docx',
                    '.jpg': 'compress_image',
                    '.jpeg': 'compress_image',
                    '.gif': 'compress_image',
                    '.png': 'compress_image',
                }

                elements.remove(consumer[main_trace_extension[len(main_trace_extension) - 1]])
                self.gui_handler.change_state_element(True, elements)

        def call_button_function(self, path_container: str, list_container: str, function):
            element_content = self.gui_handler.get_element_by_key(list_container)
            path_container = self.gui_handler.get_element_by_key(path_container)

            function(Feature(), path_container.get(), element_content.get())
