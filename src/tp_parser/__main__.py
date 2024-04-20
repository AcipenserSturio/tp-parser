import argparse
import re

import nltk

SOURCE = "assets/my_grammar.txt"
SENTENCES = "assets/test_sentences.txt"

with open(SOURCE) as f:
    grammar = f.read()
grammar1 = nltk.CFG.fromstring(grammar)
rd_parser = nltk.RecursiveDescentParser(grammar1)

def tokenize(sent: str) -> list:
    sent = re.sub(r"[^\w\s]", "", sent)
    sent = re.sub(r"[A-Z][a-z]*", "LOAN", sent)
    return sent.split()

def parse(sent: str):
    sent = tokenize(sent)
    trees = rd_parser.parse(sent)
    try:
        tree = next(trees)
    except StopIteration:
        raise ValueError(f"No parse for {sent}")
    tree.pretty_print()

def test_parser():
    with open(SENTENCES) as f:
        sentences = [line.strip() for line in f.readlines() if line.strip() and "#" not in line]
        # print(sentences)

    for sent in sentences:
        print("=============================================")
        parse(sent)

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
