#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import LTPOption

from LTML import LTML

ServiceURL = 'http://10.248.70.70:12345/ltp'


def ner(input):
    payload = {
        's': input,
        'x': 'n',
        'c': 'utf-8',
        't': LTPOption.NE
    }

    try:
        r = requests.post(ServiceURL, data=payload)
    except Exception as e:
        print e

    result = LTML(r.content)
    pids = result.count_paragraph()
    ner_result = []
    for pid in xrange(pids):
        for sid in xrange(result.count_sentence(pid)):
            print "|".join(
                [word.encode('utf8') for word in result.get_words_by_ner(pid, sid)])
            ner_result = ner_result + [word.encode('utf8') for word in result.get_words_by_ner(pid, sid)]
    return ner_result


def pos(input):
    payload = {
        's': input,
        'x': 'n',
        'c': 'utf-8',
        't': LTPOption.POS
    }
    try:
        r = requests.post(ServiceURL, data=payload)
    except Exception as e:
        print e

    result = LTML(r.content)
    pids = result.count_paragraph()
    pos_result = []
    for pid in xrange(pids):
        for sid in xrange(result.count_sentence(pid)):
            print "|".join(
                [word.encode('utf8') for word in result.get_words_by_pos(pid, sid)])
            pos_result = pos_result + [word.encode('utf8') for word in result.get_words_by_pos(pid, sid)]
    return pos_result


def tokenizer(input):
    payload = {
        's': input,
        'x': 'n',
        'c': 'utf-8',
        't': LTPOption.WS
    }
    try:
        r = requests.post(ServiceURL, data=payload)
    except Exception as e:
        print e

    result = LTML(r.content)
    tokenizer_sentences = []
    pids = result.count_paragraph()
    ws_result = []
    original_sentences = []
    for pid in xrange(pids):
        for sid in xrange(result.count_sentence(pid)):
            tokenizer_sentences.append(
                [word.encode('utf8') for word in result.get_words(pid, sid)])
            original_sentences.append(result.get_sentences(pid, sid))
            ws_result = ws_result + [word.encode(
                'utf8') for word in result.get_words(pid, sid)]
    return (original_sentences, tokenizer_sentences, ws_result)
