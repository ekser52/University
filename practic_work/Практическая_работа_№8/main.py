from translater import Translator

array_lines = [line.replace('\n', '').split() for line in open('source_file.txt', encoding='utf-8').readlines()]

translate_tool = Translator()

collection_words = {}
for wrapper in array_lines:
    for word in wrapper:
        if not word.isalpha(): continue
        normalize_word = translate_tool.word_tool().normalize(word)
        collection_words[normalize_word] = collection_words.get(normalize_word, 1) + 1

sorted_collection = sorted(collection_words.items(), key=lambda item: item[1], reverse=True)

with open('translated.txt', 'w', encoding='utf-8') as file:
    file.write('Слово | Перевод | Количество')

    for word, count in sorted_collection:
        file.write(f'\n{word} | {translate_tool.translate(word)} | {count}')

print('Done')