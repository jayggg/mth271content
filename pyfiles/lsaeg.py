import pandas as pd
from scipy.sparse import lil_matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn; seaborn.set();
from numpy.linalg import norm
from scipy.linalg import svd
from spacy.tokens import Span
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import PhraseMatcher


# Add extra terms for named entities
terms = ['SpaceX', 
         'Of Course I Still Love You',
         'Just Read The Instructions']
patterns = [nlp.make_doc(text) for text in terms]
matcher = PhraseMatcher(nlp.vocab)
matcher.add('TerminologyList', None, *patterns)

# Add extra stop words
mystopwords = {'set'}
for stop in mystopwords:
    nlp.vocab[stop].is_stop = True

# Corpus    
c = {'May31': 
     'Two crises convulse a nation: a pandemic and police violence', 
          
     'May30a': 
     'Nation’s first astronaut launch to orbit from home soil in nearly a decade', 
    
     'May30b': 
     'Death of George Floyd at the hands of police set off protests',

     'May27':
     'SpaceX launch of NASA astronauts is postponed over weather'}


def tokensfromdoc(doc):
    d = nlp(doc)
    matches = matcher(d)
    for match_id, start, end in matches:
        term = Span(d, start, end, label='myterms')
        d.ents = list(d.ents) + [term]            
    tokens = [w.lemma_ for w in d 
              # no pronouns
              if w.pos_ != 'PRON'   \
              # no punctuations
              and w.pos_ != 'PUNCT' \
              # not Beginning of a named entity
              and w.ent_iob_ != 'B' \
              # not Inside a named entity
              and w.ent_iob_ != 'I' \
              # not a stop word
              and not w.is_stop]
    tokens += [de.string.rstrip() for de in d.ents]  
    return tokens

def dictokens(corpora):
    d = {}
    for j, dok in enumerate(corpora.keys()):
        for t in tokensfromdoc(corpora[dok]):
            d[t] = d.setdefault(t, [])
            d[t] += [j]
    return d

def tdmatrix(d, corpora):    
    A = lil_matrix((len(d.keys()), len(corpora.keys())), dtype=int)
    for i, t in enumerate(d.keys()):
        for j in d[t]:
            A[i, j] = 1   
    return A

if __name__ == '__main__':
    
    d = dictokens(c)
    A = tdmatrix(d, c)
    Adf = pd.DataFrame(A.toarray(), index=d.keys(), columns=c.keys())

    u, s, vt = svd(A.toarray())
    k = 2                                   # Limit to rank k
    Vt = vt[:k, :]
    US = u[:, :k] @ np.diag(s[:k])
    usp = pd.DataFrame(US, index=d.keys()) # Words as k-vectors

    nation = usp.loc['nation', :].to_numpy()
    cs = nation.dot(np.array([0, 1])) / norm(nation)
    sn = -np.sqrt(1 - cs**2)
    rot = np.array([[cs, -sn], [sn, cs]])
    US = US @ rot.T
    usp = usp @ rot.T
    nation = nation @ rot.T

    w = {}; us = np.round(US, 8)  # w[(x,y)] = list of words at that point
    usr = list(set([tuple(us[i, :]) for i in range(us.shape[0])]))
    for i in range(len(usr)):
        w[usr[i]] = []
        for j in range(usp.shape[0]):
            if norm(usp.iloc[j, :] - usr[i]) < 1e-6:
                w[usr[i]] += [usp.index[j]]            
            
    fig = plt.figure(figsize=(10, 8)); ax = fig.gca()
    ax.scatter(US[: , 0], US[: ,1], alpha=0.5)
    ax.scatter(0, 0,  color='r', marker='*', s=150, alpha=0.6);
    ax.arrow(0, 0, nation[0], nation[1]-0.13,  width=0.025, alpha=0.3, color='orange')
    
    for i, key in enumerate(w.keys()):
        if 'nation' in w[key]:
            # ax.annotate(', '.join(w[key]), (key[0], key[1]),
            #             verticalalignment='top')
            ax.annotate('nation', (-0.16, nation[1]+0.03))
        elif key[0] < 0: 
            ax.annotate(', '.join(w[key]), (key[0]-0.05, key[1]),
                        horizontalalignment='right')
        else:
            ax.annotate(', '.join(w[key]), (key[0]+0.05, key[1]),
                        horizontalalignment='left')

    ax.set_xlim((-3, 3)); ax.set_ylim((-0.1, 1.5));
    ax.grid(True)    

    plt.show()
