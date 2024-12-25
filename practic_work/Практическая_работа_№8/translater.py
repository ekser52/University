from deep_translator import GoogleTranslator
import pymorphy3 as morphy


class Translator:

    def __init__(self):
        self.morphy = morphy.MorphAnalyzer()
        self.translator = GoogleTranslator()

    def translate(self, word: str) -> str:
        return self.translator.translate(word)

    def word_tool(self):
        return self.WordWrapper(self.morphy)

    class WordWrapper:

        def __init__(self, morphy_instance: morphy.MorphAnalyzer):
            self.morphy = morphy_instance

        def normalize(self, word: str) -> str:
            return self.morphy.parse(word)[0].normal_form
