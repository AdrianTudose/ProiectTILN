from nltk.corpus import gutenberg
from pprint import pprint
import pickle
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer

# print(dir(gutenberg))
# print(gutenberg.fileids())

text = ""
# for file_id in gutenberg.fileids():
#     text += gutenberg.raw(file_id)

with open('../data/NLTK_model_data/eminescu.txt', 'r') as file:
    text = file.read()

with open('../data/NLTK_model_data/hogas.txt', 'r', encoding='utf8') as file:
    text += file.read()

with open('../data/NLTK_model_data/bucuresti.txt', 'r', encoding='utf8') as file:
    text += file.read()

with open('../data/NLTK_model_data/pesteri.txt', 'r', encoding='utf8') as file:
    text += file.read()

# print(len(text))

trainer = PunktTrainer()
trainer.INCLUDE_ALL_COLLOCS = True
trainer.train(text)

with open('../data/NLTK_model_data/model.txt', 'wb') as file:
    pickle.dump(trainer, file)