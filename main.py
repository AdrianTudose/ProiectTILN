import os
import re
import warnings

import nltk as nltk
import rowordnet as rwn

# to be improved
ro_word = "[a-zA-Z]+"
TIP_PUNCTUATIE = "PUNCTUATIE"


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
                raise Exception("Invalid word in word_set: \"" + file + "\" ,line: \"" + str(
                    line) + "\" (words must be only lowercase letters).")
            word_set.append(line_text)
            line += 1
            line_text = f.readline()

        word_sets.append([set_name, word_set])

    return word_sets


# to be improved
def sentence_tokenizer(text):
    return nltk.sent_tokenize(text)


# to be improved
def word_tokenizer(text):
    return nltk.word_tokenize(text)


# to be completed
def syn_to_text(syn):
    if syn == "n":
        return "SUBSTANTIV"
    elif syn == "v":
        return "VERB"
    elif syn == "r":
        return "ADVERB"
    elif syn == "a":
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
    else:
        word = lemalize(word)
        id_of_synset = wn.synsets(literal=word)
        if id_of_synset:
            syn = str(wn.synset(id_of_synset[0]).pos)
            return syn_to_text(syn)

    warnings.warn("Could not find type of word: \"" + word + "\".")
    return "XXX"


def preprocesare(text, word_sets_folder="word_sets"):
    word_sets = import_word_sets(word_sets_folder)
    wn = rwn.RoWordNet()
    list_of_sentences = list()
    for sentence in sentence_tokenizer(text):
        new_sent = list()
        for word in nltk.word_tokenize(sentence):
            new_word = list()
            if re.match(ro_word, word):
                new_word.append(word)
                new_word.append(get_type(word, word_sets, wn))
                new_sent.append(new_word)
            else:
                new_sent.append([word, TIP_PUNCTUATIE])
        list_of_sentences.append(new_sent)
    return list_of_sentences


# to be improved
def import_reguli(filename):
    return_regex = ""
    with open(filename) as file:
        data = file.readlines()
        for j, i in enumerate(data):
            i = i.split("\n")
            return_regex += "("
            for k, cuvant in enumerate(i[0].split(" ")):
                if cuvant.startswith("?"):
                    return_regex += r"((" + ro_word + "){" + cuvant + "})?"
                else:
                    return_regex += r"(" + ro_word + "){" + cuvant + "}"
                if k != len(i[0].split(" ")) - 1:
                    return_regex += r"\s"
            return_regex += ")"
            if j != len(data) - 1:
                return_regex += "|"
    return return_regex


def analiza_semantica(propozitii, rules_file="semantic_rules.txt"):
    query = import_reguli(rules_file)
    string_seqences = list()
    entire_text = ""
    r = re.compile(query)
    for propozitie in propozitii:
        propozitie_parti_de_vorbire = " ".join(
            [x[0] + "{" + x[1] + "}" if x[1] != TIP_PUNCTUATIE else "" for x in propozitie])
        entire_text += propozitie_parti_de_vorbire

        result = r.findall(propozitie_parti_de_vorbire)
        for sequence_matched in result:
            string_seq = ""
            not_first = True
            for seq in sequence_matched:
                if seq != "":
                    if not_first == False:
                        string_seq += seq + " "
                    else:
                        not_first = False
            string_seqences.append(string_seq)

    positions_list = [(match.start(),match.end()) for match in r.finditer(entire_text)]
    return string_seqences, positions_list
