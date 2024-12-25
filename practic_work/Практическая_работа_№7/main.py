import typing

from gui.gui_handler import GuiHandler
from gui.gui_builder import GuiBuilder

import PySimpleGUI as gui

layout = (GuiBuilder().init_wrapper_id("main-layout")
          .add_to_line(gui.FolderBrowse(key='change_dir'))
          .add_to_line(gui.Text(key='active_dir'))
          .next_line()
          .add_to_line(gui.Button('Поиск', key='apply_changes'))
          .next_line()
          .add_to_line(gui.Listbox(values=[], select_mode=gui.LISTBOX_SELECT_MODE_EXTENDED, enable_events=True, size=(60, 20), key='view_files'))
          .next_line()
          .add_to_line(gui.Button('Преобразовать PDF в Docx', key='pdf_to_docx', disabled=False))
          .add_to_line(gui.Button('Преобразовать Docx в PDF', key='docx_to_pdf', disabled=False))
          .next_line()
          .add_to_line(gui.Button('Сжать изображение', key='compress_image', disabled=False))
          .add_to_line(gui.Button('Удалить группу файлов', key='delete_group_file', disabled=True))
          .wrapper())

handler_window = GuiHandler(gui.Window('Window', layout, finalize=True))

while True:
    iter_window, event, values = gui.read_all_windows()

    if event is None and iter_window is None: continue

    events = {
        'apply_changes': lambda _: handler_window.event().change_directory_event('active_dir', 'view_files'),
        'view_files': lambda _: handler_window.event().select_files_event('view_files'),
        'pdf_to_docx': lambda _: handler_window.event().call_button_function('active_dir', 'view_files', lambda feature, path, files: feature.convert_to_docx(path, files)),
        'docx_to_pdf': lambda _: handler_window.event().call_button_function('active_dir', 'view_files', lambda feature, path, files: feature.convert_to_pdf(path, files)),
        'compress_image': lambda _: handler_window.event().call_button_function('active_dir', 'view_files', lambda feature, path, files: feature.compress_image(path, files))
    }

    if event is not None:
        events[event](None)

    handler_window.handle_event(
        event, iter_window,
        lambda handler: typing.cast(GuiHandler, handler).get_window_instance().close(),
        lambda search: gui.WINDOW_CLOSED == typing.cast(tuple, search)[0]
    )