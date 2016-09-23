# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:52:47 2016

@author: ktarvin
"""

import nltk
#from nltk import sent_tokenize
#from nltk import word_tokenize
from nltk import pos_tag
import pandas as pd



#chunkGram = r'''Chunk: {<JJ.?>*<NN.?>*<NN>?}'''
#chunkParser = nltk.RegexParser(chunkGram)
#chunked = chunkParser.parse(tagged)

try:
    fp = r'C:\Users\ktarvin\Desktop\Motionpoint\meta_description_all.csv'
    df = pd.read_csv(fp)
    #print(df['MetaDescription1'])
    data = []
    for i in df.index:
        if isinstance(df['MetaDescription1'][i], str):
            sents = nltk.sent_tokenize(df['MetaDescription1'][i])
            for sent in sents:
                tokens = nltk.word_tokenize(sent)
                tagged_tokens = pos_tag(tokens)
                chunkGram = r'''Chunk: {<JJ.?><NN>}'''
                chunkParser = nltk.RegexpParser(chunkGram)
                chunked = chunkParser.parse(tagged_tokens)
                for n in chunked:
                    if isinstance(n, nltk.tree.Tree):               
                        if n.label() == 'NP':
                            pass
                            #print(n)
                        else:
                            w = [x[0] for x in n]
                            keyword = '%s %s' % (w[0], w[1])
                            #print(keyword)
                            data.append(keyword)
                #data.append(tagged_tokens)
        else:
            pass
    df2 = pd.Series(data)
    df3 = pd.DataFrame(df2)
    df3.columns = ['keywords']
    df3.to_csv('mpKeywords.csv')
except Exception as e:
    raise SystemExit(e)
