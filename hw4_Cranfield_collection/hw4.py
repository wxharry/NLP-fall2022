from string import punctuation
from nltk import word_tokenize
from stop_list import closed_class_stop_words
import re

class Query:
    def __init__(self, i, w):
        self.I = i
        self.W = w
    def __str__(self) -> str:
        return f".I: {self.I}\n.W: {self.W}"
    def __repr__(self) -> str:
        return str(self)
    def pre_process(self):
        tokens = word_tokenize(self.W)
        new_W = []
        for token in tokens:
            if token in closed_class_stop_words or token.isnumeric() or token in punctuation:
                continue
            new_W.append(token)
        self.W = new_W


class Abstract(Query):
    def __init__(self, i, t, a, b, w):
        self.I = i
        self.T = t
        self.A = a
        self.B = b
        self.W = w
    def __str__(self) -> str:
        return f".I: {self.I}\n.T: {self.T}\n.A: {self.A}\n.B: {self.B}\n.W: {self.W}"

def read_query(filename):
    with open(filename, "r", encoding='utf-8') as f:
        context = f.read()
    context = context.replace('\n', ' ').replace('.W', '\n.W').replace('.I', '\n.I')
    re_result = re.findall("\.I (.*)\n\.W (.*)", context)
    queries = []
    for i, w in re_result:
        queries.append(Query(i, w))
    return queries

def read_abstract(filename):
    with open(filename, "r", encoding='utf-8') as f:
        context = f.read()
    context = context.replace('\n', ' ').replace('.W', '\n.W').replace('.I', '\n.I').replace('.A', '\n.A').replace('.B', '\n.B').replace('.T', '\n.T')
    re_result = re.findall("\.I (.*)\n\.T (.*)\n\.A (.*)\n\.B (.*)\n\.W (.*)", context)
    abstracts = []
    for i, t, a, b, w in re_result:
        abstracts.append(Abstract(i, t, a, b, w))
    return abstracts

def get_vector(queries):
    for query in queries:
        query.pre_process()

def main():
    qry = read_query("cran.qry")
    abstract = read_abstract("cran.all.1400")
    qry_vector = get_vector(qry)
    abstract = get_vector(abstract)
    

if __name__ == "__main__":
    main()