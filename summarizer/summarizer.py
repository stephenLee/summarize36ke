#!/usr/bin/env python
#-*- coding: utf-8 -*-
import parser
import math
import operator

from collections import OrderedDict


class Summarizer(object):
    def __init__(self, summarySize=3, keywordsSize=10):
        self.summarySize = summarySize
        self.keywordsSize = keywordsSize

    def summarize(self, title, text):
        titleWords = parser.splitWords(title)
        original_sentences, tokenizer_sentences, keywords_list= parser.getKeywords(text)
        topKeywords = dict(keywords_list[:self.keywordsSize])
        sentence_score = {}
        for i, sentence in enumerate(tokenizer_sentences):
            titleFeature = parser.titleScore(titleWords, sentence)
            sentenceLength = parser.sentenceLength(sentence)
            sentencePosition = parser.sentencePosition(
                i, len(tokenizer_sentences))
            sbsFeature = self.sbs(sentence, topKeywords)
            dbsFeature = self.dbs(sentence, topKeywords)
            keywordFrequency = (sbsFeature + dbsFeature) / 2 * 10.0
            totalScore = (
                titleFeature * 1.5 + keywordFrequency * 2.0 + sentenceLength * 0.5 + sentencePosition * 1.0) / 4.0
            sentence_score[' '.join(sentence)] = (totalScore, i)
        size = self.summarySize
        tmp_summary = sorted(
            sentence_score.iteritems(), key=operator.itemgetter(1, 0), reverse=True)[:size]
        summary_list = [item[1][1] for item in tmp_summary]
        summary_list = sorted(summary_list)
        summary = [original_sentences[i] for i in summary_list]
        return summary

    def sbs(self, words, topKeywords):
        if len(words) == 0:
            return 0
        else:
            filter_keys = filter(lambda x: x in topKeywords.keys(), words)
            summ = 0
            for key in filter_keys:
                summ += topKeywords[key]
        return 1 / abs(len(words)) * summ

    # fucking abstract part
    def dbs(self, words, topKeywords):
        if len(words) == 0:
            return 0
        else:
            k = len(
                filter(lambda x: x in topKeywords.keys(), words)) + 1
            summ = 0
            firstWord = ()
            secondWord = ()
            ordered_topKeywords = OrderedDict(topKeywords)
            for i in xrange(len(words)):
                try:
                    index = ordered_topKeywords(words[i])
                except TypeError:
                    continue
                score = topKeywords[index][1]
                if len(firstWord) == 0:
                    firstWord = (i, score)
                else:
                    secondWord = firstWord
                    firstWord = (i, score)
                    summ += (
                        firstWord[1] * secondWord[1]) / math.pow(
                            (firstWord[0] - secondWord[0]), 2)

            return (1.0 / (k * (k + 1.0))) * summ




















