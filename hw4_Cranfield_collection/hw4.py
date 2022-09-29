from math import log2, sqrt
from string import punctuation
from nltk import word_tokenize
from stop_list import closed_class_stop_words
import re

class Query:
    def __init__(self, i, w):
        self.I = i
        self.W = w
        self.pre_process()
        self.word_list = set(self.W)
        self.TF = {}
        self.IDF = {}
        self.vector = {}
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
    def calc_TF(self):
        for term in self.W:
            self.TF[term] = self.TF.get(term, 0) + 1
        return self.TF
    def calc_IDF(self, documents):
        n = len(documents)
        for word in self.word_list:
            count = 0
            for document in documents:
                if word in document.word_list:
                    count += 1
            self.IDF[word] = log2(n/count)
        return self.IDF
    def calc_TF_IDF(self, documents):
        self.calc_TF()
        self.calc_IDF(documents)
        for word in self.word_list:
            self.vector[word] = self.TF[word] * self.IDF[word]
        return self.vector
    @staticmethod
    def calc_similarity(v_q, v_d):
        nu = 0
        for a in v_q:
            if a in v_d.keys():
                nu += v_q[a] + v_d[a]
        de = sqrt(sum([x*x for x in v_q.values()])) * sqrt(sum([x*x for x in v_d.values()]))
        if de == 0:
            return 0
        return nu / de


class Abstract(Query):
    def __init__(self, i, t, a, b, w):
        self.I = i
        self.T = t
        self.A = a
        self.B = b
        self.W = w
        self.pre_process()
        self.word_list = set(self.W)
        self.TF = {}
        self.IDF = {}
        self.vector = {}
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

def write_output(filename, context):
    with open(filename, 'w', encoding='utf-8') as f:
        for (id1, id2, similarity) in context:
            f.write(f"{id1} {id2} {similarity}\n")

def main():
    qry = read_query("cran.qry")
    abstracts = read_abstract("cran.all.1400")
    qry_vectors = [(query.I, query.calc_TF_IDF(qry)) for query in qry]
    abstract_vectors = [(a.I, a.calc_TF_IDF(abstracts)) for a in abstracts]
    similarities = [(vid, aid, Query.calc_similarity(v_q, v_d)) for (vid, v_q) in qry_vectors for (aid, v_d) in abstract_vectors]
    write_output("output.txt", similarities)

if __name__ == "__main__":
    main()