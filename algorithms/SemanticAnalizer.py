import re

from algorithms.Preprocesor import TIP

rule_position = list()
rules = list()


def make_rule(text, file, line):
    rule = ""
    splitede_text = re.findall("(\s)|([A-Z]+)|(\"(?:" + TIP["CUVANT"] + "|\s" + ")+\")|(\?\(.+\))", text)

    for k, cuvant in enumerate(splitede_text):
        if cuvant[0] != "":
            rule += r"\s+"
        elif cuvant[1] != "":
            rule += r"([0-9]+){" + cuvant[1] + "}"
            rule_position.append(line)
        elif cuvant[2] != "":
            rule += "{[A-Z]+}\s".join(re.findall(TIP["CUVANT"], cuvant[2][1:-1])) + "{[A-Z]+}\s"
        elif cuvant[3] != "":
            rule += r"(?:" + make_rule(cuvant[3][2:-1], file, line) + ")?"
        else:
            raise Exception("Invalid expression in \"" + file + "\" ,line: " + str(line + 1) + ".")

    return rule


def import_rules(filename):
    return_regex = ""

    with open(filename) as file:
        data = file.readlines()
        for j, line in enumerate(data):
            line = line.split("\n")
            rules.append(line[0])
            return_regex += "(?:"
            return_regex += make_rule(line[0], filename, j)
            return_regex += ")"
            if j != len(data) - 1:
                return_regex += "|"

    return return_regex

#you need to have more than one rule with one element
def analise(sentences, rules_file="data/semantic_rules.txt"):
    query = import_rules(rules_file)
    matching_rules = list()
    r = re.compile(query)

    for j, sentence in enumerate(sentences):
        extended_sentence = " ".join([str(i) + "{" + x[1] + "}" if x[1] != " " else ""
                                      for i, x in enumerate(sentence)])
        result = r.findall(extended_sentence)

        for sequence_matched in result:
            word_seq = [j]
            words = list()
            seq_rule = ""
            for i, seq in enumerate(sequence_matched):
                if seq != "":
                    words.append(sentence[int(seq)][0])
                    word_seq.append(int(seq))
                    seq_rule = rule_position[i]

            matching_rules.append([words,seq_rule, word_seq])

    return matching_rules
