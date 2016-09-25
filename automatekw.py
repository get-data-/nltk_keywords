# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:52:47 2016
@author: ktarvin
"""

import os
import sys
import nltk
import pandas as pd


def parseKeywords(argv):
    try:
        filepath = (os.path.dirname(os.path.abspath(__file__)))
        df = pd.read_csv('%s\\%s' % (filepath, argv[0]))
        data = []
        for i in df.index:
            if isinstance(df['MetaDescription1'][i], str):
                sents = nltk.sent_tokenize(df['MetaDescription1'][i])
                for sent in sents:
                    tokens = nltk.word_tokenize(sent)
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
                            else:
                                w = [x[0] for x in n]
                                keyword = '%s %s' % (w[0], w[1])
                                data.append(keyword)
            else:
                pass
        ds = pd.Series(data)
        df = pd.DataFrame(ds)
        df.columns = ['keywords']
        df.to_csv('%s' % (argv[1]))
    except Exception as e:
        raise SystemExit(e)


if __name__ == "__main__":
    try:
        argv = sys.argv[1:]
        parseKeywords(argv)
    except Exception as e:
        raise SystemExit('Exited in general Exception in main Try with %s' % (e))