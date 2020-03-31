# to be improved
import os
import re
import warnings

import spacy
import rowordnet as rwn

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


def sentence_tokenizer(text):
    sentence_list = list()
    sentence = list()

    for word in text:
        sentence.append(word)
        if re.fullmatch(TIP["SFARSIT_PROPOZITIE"], word[0]):
            sentence_list.append(sentence)
            sentence = list()

    if len(sentence) > 0:
        sentence_list.append(sentence)

    return sentence_list


def word_tokenizer(text):
    words = list()
    r = re.compile("(" + TIP["CUVANT"] + ")|(" + TIP["SFARSIT_PROPOZITIE"] + "|" + TIP["PUNCTUATIE"] + ")|("
                   + TIP["ALINIERE"] + ")")

    for section in text:
        if type(section) == str:
            for cuv in r.findall(section):
                if cuv[0] != "":
                    words.append([cuv[0], "CUVANT"])
                elif cuv[1] != "":
                    words.append([cuv[1], "PUNCTUATIE"])
                else:
                    words.append([cuv[2], "ALINIERE"])
        else:
            words.append(section)

    return words


def syn_to_text(syn):
    if syn == "n":
        return "SUBSTANTIV"
    elif syn == "v":
        return "VERB"
    elif syn == "a":
        return "ADJECTIV"
    elif syn == "r":
        return "ADJECTIV"
    else:
        return "CEVA"


# to be made
def lemalize(word):
    return word


def get_type(word, word_sets, wn):
    for set in word_sets:
        if word in set[1]:
            return set[0]

    id_of_synset = wn.synsets(literal=word)
    if id_of_synset:
        syn = str(wn.synset(id_of_synset[0]).pos)
        return syn_to_text(syn)
    """else:
        word = lemalize(word)
        id_of_synset = wn.synsets(literal=word)
        if id_of_synset:
            syn = str(wn.synset(id_of_synset[0]).pos)
            return syn_to_text(syn)"""

    warnings.warn("Could not find type of word: \"" + word + "\".")
    # modify to send message "Reconsiderati folosirea cuvantului ... " cu highlight
    # and another idea for guessing the word
    return "XXX"


def run_name_entity_recognizer(text):
    nlp = spacy.load("data/ner_model")
    doc = nlp(text)

    string_start = 0
    result = list()
    rest_of_text = ""

    for ent in doc.ents:
        string_end = ent.start_char
        rest_of_text = text[string_start:string_end]
        if rest_of_text != "":
            result.append(rest_of_text)
        result.append([ent.text, ent.label_])
        string_start = ent.end_char

    if rest_of_text != "":
        rest_of_text = text[string_start:]
        result.append(rest_of_text)

    if len(doc.ents) == 0:
        return [text]

    return result


def process(text, word_sets_folder="data/word_sets"):
    word_sets = import_word_sets(word_sets_folder)
    wn = rwn.RoWordNet()

    text = run_name_entity_recognizer(text)

    text = word_tokenizer(text)

    text = sentence_tokenizer(text)

    for sentence in text:
        for word in sentence:
            if word[1] == "CUVANT":
                word[1] = get_type(word[0], word_sets, wn)

    return text
