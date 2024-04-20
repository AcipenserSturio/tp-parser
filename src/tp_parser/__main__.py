import argparse
import re
import csv

import nltk
import pandas as pd

SOURCE = "assets/my_grammar.txt"
SENTENCES = "assets/test_sentences.txt"
TATOEBA = "assets/tok_sentences.tsv"
PARSED = "parsed.tsv"

# https://stackoverflow.com/questions/25735644/python-regex-for-splitting-text-into-sentences-sentence-tokenizing#25736082
# Modified to include "!"
SENT_BOUNDARY = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\:)\s"
VOCATIVE_BOUNDARY = r", (?=.* o[\.\?\!]?$)"

with open(SOURCE) as f:
    grammar = f.read()
grammar1 = nltk.CFG.fromstring(grammar)
rd_parser = nltk.RecursiveDescentParser(grammar1)


def add_parsed(sent: str, tree: str):
    with open(PARSED, "a") as f:
        f.write(f"{sent}\t{tree}\n")


def is_parsed(string: str) -> bool:
    with open(PARSED) as f:
        for line in csv.reader(f, delimiter="\t"):
            if not line:
                continue
            sent, tree = line
            if string == sent:
                return True
        return False


def get_test_sentences():
    with open(TATOEBA) as f:
        for _, _, text in csv.reader(f, delimiter="\t"):
            text = re.sub(VOCATIVE_BOUNDARY, ". ", text)
            sents = re.split(SENT_BOUNDARY, text)
            for sent in sents:
                yield sent

    with open(SENTENCES) as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            if "#" in line:
                continue
            yield line


def tokenize(sent: str) -> list:
    sent = re.sub(r"[^\w\s]", "", sent)
    sent = re.sub(r"[A-Z][a-z]*", "LOAN", sent)
    sent = sent.split()
    for index, word in enumerate(sent):
        if index == 0 or index == len(sent)-1:
            continue
        if word == "ala" and sent[index-1] == sent[index+1]:
            word = sent[index+1]
            sent[index+1] = "_" # duplicate
            sent[index] = "_" # ala
            sent[index-1] = f"{word}_ala_{word}"
    sent = [word for word in sent if word != "_"]
    return sent


def parse(sent: str):
    sent = tokenize(sent)
    trees = rd_parser.parse(sent)
    try:
        tree = next(trees)
    except StopIteration:
        # raise ValueError(f"No parse for {sent}")
        return None
    return tree


def test_parser():
    for index, sent in enumerate(get_test_sentences()):
        if is_parsed(sent):
            continue
        print(index)
        tree = parse(sent)
        # tree.pretty_print()

        tree = tree.pformat(margin=99999) if tree else "FAILED"
        if tree == "FAILED":
            print(f"FAILED #{index}: {sent}")

        add_parsed(sent, tree)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="tp-parser",
        description="Parses sentences in Toki Pona.",
    )
    parser.add_argument(
        "--test",
        help="Try parse every sentence in test sentences",
        action="store_true",
    )
    args = parser.parse_args()
    if args.test:
        test_parser()
    else:
        sent = input()
        parse(sent)
