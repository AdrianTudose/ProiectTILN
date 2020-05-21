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

                    #words.append([section[cuv.start(0):cuv.end(0)]," "])
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

def words_clasifier(text, word_sets):
    new_text = list()

    for sentence in text:
        new_sentence=list()
        for word in sentence:
            lower_word = word[0].lower()
            if word[1] in ("LOC","FACILITY"):
                new_sentence.append([word[0],"LOCATIE"])
            elif word[1] == "NUMERIC_VALUE":
                new_sentence.append([word[0],"NUMAR"])
            elif word[1] == "DATETIME":
                new_sentence.append([word[0],"TIMP"])
            if word[1] == "CUVANT":
                for set in word_sets:
                    if lower_word in set[1]:
                        new_sentence.append([word[0],set[0]])

        if len(new_sentence) > 0:
            new_text.append(new_sentence)

    return new_text


def run_name_entity_recognizer(text):
    nlp = spacy.load("algorithms/data/ner_model")
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


def process(text, word_sets_folder="algorithms/data/word_sets"):
    word_sets = import_word_sets(word_sets_folder)
    wn = rwn.RoWordNet()

    nltk_model_file = open('algorithms/data/NLTK_model_data/model.txt', 'rb')
    trained = pickle.load(nltk_model_file)

    stop_words = open('algorithms/data/stop-words-ro.txt','r').read().split("\n")

    sentence_tokenizer = PunktSentenceTokenizer(trained.get_params())

    text = sentence_tokenizer.tokenize(text)

    text = run_name_entity_recognizer(text)

    text = word_tokenizer(text)

    text = words_clasifier(text,word_sets)

    return text
