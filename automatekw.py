# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:52:47 2016

@author: ktarvin
"""

import os
import nltk
import pandas as pd

try:
    filepath = (os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv('%s\\translations_meta_description_all.csv' % (filepath))
    data = []
    for i in df.index:
        if isinstance(df['MetaDescription1'][i], str):
            sents = nltk.sent_tokenize(df['MetaDescription1'][i])
            for sent in sents:
                tokens = nltk.word_tokenize(sent)
                tagged = nltk.pos_tag(tokens)
                tagged_tokens = nltk.pos_tag(tokens)
                chunkGram = r'''
                Chunk: {<JJ.?><NN>}
                {<JJ><NN.?>}
                {<NN.?><NN.?>}
                {<NN|NN.?><NN|NN.?><NN|NN.?>}
                {<VBG><NN|NN.?><NN|NN.?>}
                {<JJ|JJ.?><NN|NN.?><NN|NN.?>}
                '''
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
    print(df3.head())
    df3.to_csv('translationsKeywords.csv')
except Exception as e:
    raise SystemExit(e)
