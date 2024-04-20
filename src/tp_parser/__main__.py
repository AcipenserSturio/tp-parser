import nltk

SOURCE = "assets/my_grammar.txt"
SENTENCES = "assets/test_sentences.txt"

with open(SOURCE) as f:
    grammar = f.read()
grammar1 = nltk.CFG.fromstring(grammar)
rd_parser = nltk.RecursiveDescentParser(grammar1)

def test_parser():
    with open(SENTENCES) as f:
        sentences = [line.strip() for line in f.readlines() if line.strip() and "#" not in line]
        # print(sentences)

    for sent in sentences:
        print("=============================================")
        trees = rd_parser.parse(sent.split())
        try:
            tree = next(trees)
        except StopIteration:
            raise ValueError(f"No parse for {sent}")
        tree.pretty_print()

if __name__ == "__main__":
    sent = input()
    if sent == "test":
        test_parser()
    else:
        for tree in rd_parser.parse(sent.split()):
            tree.pretty_print()
            break
