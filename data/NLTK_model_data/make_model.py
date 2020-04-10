from nltk.corpus import gutenberg
from pprint import pprint
import pickle
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer

# print(dir(gutenberg))
# print(gutenberg.fileids())

text = ""
# for file_id in gutenberg.fileids():
#     text += gutenberg.raw(file_id)

with open('eminescu.txt', 'r') as file:
    text = file.read()

with open('hogas.txt', 'r', encoding='utf8') as file:
    text += file.read()

with open('bucuresti.txt', 'r', encoding='utf8') as file:
    text += file.read()

with open('pesteri.txt', 'r', encoding='utf8') as file:
    text += file.read()

# print(len(text))

trainer = PunktTrainer()
trainer.INCLUDE_ALL_COLLOCS = True
trainer.train(text)

with open('model.txt', 'wb') as file:
    pickle.dump(trainer, file)