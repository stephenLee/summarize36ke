#!/usr/bin/env python
#-*- coding: utf-8 -*-

import feedparser
import urlparse

import redis
import json
import time
import requests

from goose import Goose
from goose.text import StopWordsChinese

from bs4 import BeautifulSoup

from summarizer.summarizer import Summarizer


def parse_feed(feed, r):
    ua_string = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'
    feedparser.USER_AGENT = ua_string
    d = feedparser.parse(feed)
    entries = []
    for i in range(len(d['entries'])):
        entry = {}
        link = d.entries[i]['link']
        article_id = urlparse.urlparse(
            link)[2].split('/')[2].split('.')[0]
        title = d.entries[i]['title']
        entry['id'] = article_id
        entry['link'] = link
        entry['title'] = title
        # get article id from redis
        articles_id = r.smembers('article:ids')
        if article_id not in articles_id:
            entries.append(entry)
            r.sadd('article:ids', article_id)
        else:
            break
    return entries


def get_summary_using_textteaser(title, text):
    summary = Summarizer()
    summary_list = summary.summarize(title, text)
    summary_json = json.dumps(summary_list)
    return summary_json


def login(username, password):
    url = 'http://www.36kr.com/account/sign_in'
    s = requests.Session()
    r = s.get(url)
    soup = BeautifulSoup(r.text)
    csrf_token = soup.find('meta', attrs={'name': 'csrf-token'})
    authenticity_token = csrf_token['content']
    print authenticity_token
    payload = {
        'authenticity_token': authenticity_token,
        'user[login]': username,
        'user[password]': password,
        'commit': u'登录',
        'utf8':	'✓'
    }
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
               'Host': 'www.36kr.com',
               'Referer': 'http://www.36kr.com/account/sign_in'}
    try:
        r = s.post(url, data=payload, headers=headers)
    except Exception as e:
        print e
    # get cookie
    cookies = s.cookies
    return (cookies, authenticity_token)


def reply(article_id, summary, cookies, authenticity_token):
    url = 'http://www.36kr.com/p/%s/replies' % article_id
    payload = {
        'authenticity_token': authenticity_token,
        'reply[body]': summary,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
        'X-CSRF-Token': authenticity_token,
        'Accept':  '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':	'www.36kr.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.36kr.com/p/%s.html' % article_id,
        'X-Requested-With': 'XMLHttpRequest'}
    try:
        r = requests.post(
            url, data=payload, headers=headers, cookies=cookies, allow_redirects=True)
    except Exception as e:
        print e
    print r.status_code


def main():
    r = redis.StrictRedis(host='10.248.70.70', port=6379, db=1)
    g = Goose(
        {'stopwords_class': StopWordsChinese, 'browser_user_agent': 'Mozilla'})
    feed = 'http://www.36kr.com/feed'
    entries = parse_feed(feed, r)
    if len(entries) != 0:
        print 'Login in 36ke:'
        cookies, authenticity_token = login('stephenlee', 'justforfun')
        print cookies
        for entry in entries:
            article_id = entry['id']
            title = entry['title']
            link = entry['link']
            article = g.extract(url=link)
            text = article.cleaned_text
            summary_str = get_summary_using_textteaser(title, text)
            summary_list = json.loads(summary_str)
            summary = ''.join(summary_list)
            print summary
            print 'Reply to aritlce: %s' % article_id
            reply(article_id, summary, cookies, authenticity_token)
            time.sleep(10)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(600)




















