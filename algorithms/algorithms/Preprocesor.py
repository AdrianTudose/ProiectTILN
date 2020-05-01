# to be improved
import os
import re
import warnings

import spacy
import rowordnet as rwn

import pickle
from nltk.tokenize.punkt import PunktSentenceTokenizer

TIP = {
    "CUVANT": "[0-9a-zA-ZăîşșţâĂÂÎȘȚ]+",
    "PUNCTUATIE": ",|;|:|-|\(|\)",
    "SFARSIT_PROPOZITIE": "\[\.\.\.\]|\.\.\.|\.|\?!|!\?|\?|!",
    "ALINIERE": "\s|\t|\n"
}


def import_word_sets(folder):
    word_sets = list()
    for file in os.listdir(folder):
        f = open(os.path.join(folder, file), "r")

        word_set = list()
        set_name = file[:-4]

        if not re.match(r"[A-Z]+", set_name):
            raise Exception("Invalid word_set: \"" + file + "\" (filename[set name] must be only UPPERCASE letters).")

        line_text = f.readline()
        line = 1
        while line_text:
            line_text = line_text[:-1]
            if not re.match(r"[a-z]+", line_text):
                raise Exception("Invalid word in word_set: \"" + file + "\" ,line: " + str(
                    line) + " (words must be only lowercase letters).")
            word_set.append(line_text)
            line += 1
            line_text = f.readline()

        word_sets.append([set_name, word_set])

    return word_sets


def sentence_tokenizer(text,tok):
    """sentence_list = list()
    sentence = list()

    for word in text:
        sentence.append(word)
        if re.fullmatch(TIP["SFARSIT_PROPOZITIE"], word[0]):
            sentence_list.append(sentence)
            sentence = list()

    if len(sentence) > 0:
        sentence_list.append(sentence)"""

    return tok.tokenize(text)


def word_tokenizer(text):
    tokenized_text = list()
    for sentence in text:
        words = list()
        r = re.compile("(" + TIP["SFARSIT_PROPOZITIE"] + "|" + TIP["PUNCTUATIE"] + ")|(" + TIP["ALINIERE"] + ")")
        for section in sentence:
            if type(section) == str:
                ind_start = 0
                for cuv in r.finditer(section):
                    ind_end = cuv.start(0)
                    if ind_end != ind_start:
                        words.append([section[ind_start:ind_end],"CUVANT"])

                    words.append([section[cuv.start(0):cuv.end(0)]," "])
                    ind_start = cuv.end(0)
                if ind_start != len(section):
                    words.append([section[ind_start:], "CUVANT"])
            else:
                words.append(section)
        tokenized_text.append(words)
    return tokenized_text


def syn_to_text(syn):
    if syn == "n":
        return "SUBSTANTIV"
    elif syn == "v":
        return "VERB"
    elif syn == "a":
        return "ADJECTIV"
    elif syn == "r":
        return "ADJECTIV"

def get_type(word, word_sets, wn, stop_words):
    lower_word = word[0].lower()
    if lower_word in stop_words:
        return " "
    elif word[1] in ("LOC","FACILITY"):
        return "LOCATIE"
    elif word[1] == "NUMERIC_VALUE":
        return "NUMAR"
    elif word[1] == "DATETIME":
        return "TIMP"
    if word[1] == "CUVANT":
        for set in word_sets:
            if lower_word in set[1]:
                return set[0]

        id_of_synset = wn.synsets(literal=lower_word)
        if id_of_synset:
            syn = str(wn.synset(id_of_synset[0]).pos)
            return syn_to_text(syn)

    return " "


def run_name_entity_recognizer(text):
    nlp = spacy.load("Algorithms/data/ner_model")
    sentence_results = list()

    for sentence in text:
        doc = nlp(sentence)

        string_start = 0
        result = list()
        rest_of_text = ""

        for ent in doc.ents:
            string_end = ent.start_char
            rest_of_text = sentence[string_start:string_end]
            if rest_of_text != "":
                result.append(rest_of_text)
            result.append([ent.text, ent.label_])
            string_start = ent.end_char

        if rest_of_text != "":
            rest_of_text = sentence[string_start:]
            result.append(rest_of_text)

        if len(doc.ents) == 0:
            result = [sentence]

        sentence_results.append(result)

    return sentence_results


def process(text, word_sets_folder="Algorithms/data/word_sets"):
    word_sets = import_word_sets(word_sets_folder)
    wn = rwn.RoWordNet()

    nltk_model_file = open('Algorithms/data/NLTK_model_data/model.txt', 'rb')
    trained = pickle.load(nltk_model_file)

    stop_words = open('Algorithms/data/stop-words-ro.txt','r').read().split("\n")

    sentence_tokenizer = PunktSentenceTokenizer(trained.get_params())

    text = sentence_tokenizer.tokenize(text)

    text = run_name_entity_recognizer(text)

    text = word_tokenizer(text)

    for sentence in text:
        for word in sentence:
            if word[1] != " ":
                word[1] = get_type(word, word_sets, wn, stop_words)

    return text
