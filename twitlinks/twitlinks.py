"""
 Authors: Gaurav Kumar <aavrug@gmail.com>

"""

#!/usr/bin/env python
import requests
from requests_oauthlib import OAuth1
import ConfigParser
import re

def search(query, count):
    config = ConfigParser.ConfigParser()
    cnfg = open('./twitlinks/twit.cfg')
    config.readfp(cnfg)
    config.read(cnfg)

    t_app_key = config.get('global', 'app_key')
    t_app_secret_key = config.get('global', 'app_secret_key')
    t_access_token = config.get('global', 'access_token')
    t_access_secret_token = config.get('global', 'access_secret_token')

    auth = OAuth1(t_app_key, t_app_secret_key, t_access_token, t_access_secret_token)
    result = requests.get('https://api.twitter.com/1.1/search/tweets.json?q=%23'+query+'&count='+str(count), auth=auth)
    return result.json()

def get_links(hashtags, total=1):
    results = {}
    if hashtags == '':
        msg = 'You cannot enter a blank tag.'
        return msg
    tagsList = hashtags.strip().split(',')
    for tag in tagsList:
        tag = tag.strip()
        key = tag.replace('#', '')
        result = search(key, count=total)
        results[key] = result
    display_links(results)

def display_links(results):
    links = {}
    for key, result in results.iteritems():
        links[key] = fetch_links(result)
    print links

def fetch_links(tweets):
    urls = []
    data = []
    tweets = tweets['statuses']
    if tweets:
        for tweet in tweets:
            data = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet['text'])
            if data:
                urls.append(data)
    return urls
