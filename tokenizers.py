from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

def nouns_and_verbs(sentence):
    verbs_nouns = [word for word in word_tokenize(sentence) if nltk.pos_tag([word])[0][1][0] == 'N' or nltk.pos_tag([word])[0][1][0] == 'V']
    return verbs_nouns

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

#Now also includes hypernyms (Hopefully)
def get_synset(token):
    nested_lemmas = [s.lemmas for s in wn.synsets(token)]
    lemmas = []
    for lemma_list in nested_lemmas:
        for lemma in lemma_list:
            lemmas.append(lemma.name.replace('_', ' '))

    list_of_hyps = []
    holder_for_hypers = wn.synsets(token)[0].hypernyms() #The first element is always itself. This way we only get hypernyms for the token itself
    for hyp in holder_for_hypers:
        for lemma in hyp.lemmas:
            lemmas.append(lemma.name.replace('_', ' '))

    return list(set(lemmas)) #Using nested lemmas means lots of duplicated, this removes them

class QuerySynsetExpandingTokenizer(object):
    def __init__(self):
        self.first_run = True

    def __call__(self, doc):
        if self.first_run:
            self.query = doc
            self.query_tokens = [t for t in word_tokenize(doc)]

            self.query_set = set(self.query_tokens)
            self.first_run = False
            return self.query_tokens
        else:
            nouns_verbs = nouns_and_verbs(doc)
            tokens = [t for t in word_tokenize(doc)]
            syns = {}
            for nv in nouns_verbs:
                syns[nv] = get_synset(nv)

            # Replace tokens with synonyms if they occur in the query
            for token in tokens:
                if token in nouns_verbs:
                    overlap = self.query_set.intersection(set(syns[token]))
                    if len(overlap):
                        token = list(overlap)[0]
        return tokens
