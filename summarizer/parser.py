#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import division

import operator

from ltp import ltp


# read stopwords
def get_stopwords(path):
    stopwords = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
#            line = line.decode('utf-8')
            stopwords.append(line)
    return stopwords

stopWords = get_stopwords('/home/lxd/elasticsearch-0.90.3/python/corpus/stop_words')
# sentence length: couputed using this formula
# (ideal - Math.abs(ideal-words.size)) / ideal


def sentenceLength(sentence, ideal=20):
    return 1-(abs(ideal-len(sentence)) / ideal)


def splitWords(source):
    return ltp.tokenizer(source)[2]


def titleScore(titleWords, sentence):
    count = 0
    for word in titleWords:
        if word not in stopWords:
            if word in sentence:
                count += 1
    return count / len(titleWords)


def getKeywords(text):
    original_sentences, tokenizer_sentences, keyWords = ltp.tokenizer(text)
    article_keyword = {}  # word:count
    for w in keyWords:
        if w not in stopWords:
            article_keyword[w] = article_keyword.setdefault(
                w, 0) + 1
    # list article_keyword
    keywords_list = sorted(
        article_keyword.iteritems(), key=operator.itemgetter(1), reverse=True)
    return (original_sentences, tokenizer_sentences, keywords_list)


def sentencePosition(ctr, sentenceCount):
    normalized = ctr / sentenceCount
    if normalized > 0 and normalized <= 0.1:
        return 0.17
    elif normalized > 0.1 and normalized <= 0.2:
        return 0.23
    elif normalized > 0.2 and normalized <= 0.3:
        return 0.14
    elif normalized > 0.3 and normalized <= 0.4:
        return 0.08
    elif normalized > 0.4 and normalized <= 0.5:
        return 0.05
    elif normalized > 0.5 and normalized <= 0.6:
        return 0.04
    elif normalized > 0.6 and normalized <= 0.7:
        return 0.06
    elif normalized > 0.7 and normalized <= 0.8:
        return 0.04
    elif normalized > 0.8 and normalized <= 0.9:
        return 0.04
    elif normalized > 0.9 and normalized <= 1.0:
        return 0.15
    else:
        return 0.0
