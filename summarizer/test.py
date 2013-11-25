#!/usr/bin/env python
#!-*- coding: utf-8 -*-
from goose import Goose
from goose.text import StopWordsChinese

from summarizer import Summarizer

import json

g = Goose({'stopwords_class': StopWordsChinese})
url = 'http://sports.sina.com.cn/nba/2013-10-29/00086855748.shtml'
article = g.extract(url=url)
title = article.title
print title
text = article.cleaned_text
print text
summary = Summarizer()
summary_list = summary.summarize(title, text)

print 'summary is below:'

for sentence in summary_list:
    print sentence

summary_json = json.dumps(summary_list)
print summary_json









