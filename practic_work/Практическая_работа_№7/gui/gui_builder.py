import PySimpleGUI as gui


class GuiBuilder:
    def __init__(self, wrapper_id: str = '', index: int = 0, old_cache: list[list[gui.Element]] = None):
        if old_cache is None:
            self.__cache = [[]]
        else:
            self.__cache = old_cache

        self.instance = gui
        self.index = index
        self.wrapper_id = wrapper_id

    @staticmethod
    def unite_elements(*elements: list[list[gui.Element]]):
        content = []
        for parent in elements:
            for wrapper in parent:
                for item in wrapper:
                    content.append(item)
        return [content]

    def __init_region(self) -> list:
        if len(self.__cache) >= self.index: pass
        self.__cache.insert(self.index, [])
        return self.__cache[self.index]

    def start_at(self, start: int):
        self.index = start
        return self

    def init_wrapper_id(self, id: str):
        self.wrapper_id = id
        return self

    def add_to_line(self, element: gui.Element):
        try:
            elements = self.__cache[self.index]
        except IndexError:
            elements = self.__init_region()

        elements.append(element)

        self.__cache.__setitem__(self.index, elements)
        return self

    def next_line(self):
        return GuiBuilder(self.wrapper_id, self.index + 1, self.__cache)

    def wrapper(self) -> list[list[gui.Element]]:
        content = []
        for index, parent in enumerate(self.__cache):
            content.append(parent)

        self.__cache.clear()
        self.__cache.append([gui.Column(content, key=self.wrapper_id)])

        return self.__cache

    def build(self) -> list[list[gui.Element]]:
        return self.__cache
