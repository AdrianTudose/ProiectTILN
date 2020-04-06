from nltk.corpus import gutenberg
from pprint import pprint
import pickle
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer

sentences = "Biserica din cărămidă de la sfârșitul secolului XV-lea, de lângă Palatul Culturii, este Biserica Sf Nicolae." \
            " O plimbare de 5 minute spre nord, pe Bulevardul Ștefan cel Mare, te duce la Biserica Trei Ierarhi " \
            "(str Ștefan cel Mare și Sfânt nr 28). Biserica Armenească de la începutul secolului XIX-lea se află pe" \
            " Strada Armenească, o plimbare de 8 minute la nord-est de Piața Palatului, pe Strada Costache Negri. Mergi " \
            "puțin mai departe spre nord, până pe Strada Cuza Vodă nr 51, unde se înalță Mănăstirea Golia. Biserica Sf. " \
            "Nicolae Domnesc este situată în centrul orașului, pe Str. Anastasie Panu nr. 65, în preajma vechii Curți " \
            "Domnești, între Palatul Culturii și Casa cu arcade (Casa Dosoftei)."

with open('data/NLTK_model_data/model.txt', 'rb') as file:
    trainer = pickle.load(file)

tokenizer = PunktSentenceTokenizer(trainer.get_params())
# Test the tokenizer on a piece of text
print(tokenizer.tokenize(sentences))

# View the learned abbreviations
print(tokenizer._params.abbrev_types)
# set([...])

# Here's how to debug every split decision
# for decision in tokenizer.debug_decisions(sentences):
#     pprint(decision)
#     print('=' * 30)