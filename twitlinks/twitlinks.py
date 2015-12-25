"""
 Authors: Gaurav Kumar <aavrug@gmail.com>

"""

#!/usr/bin/env python
from twython import Twython
import ConfigParser
import re

def twitter_setup():
    config = ConfigParser.ConfigParser()
    cnfg = open('./twit.cfg')
    config.readfp(cnfg)
    config.read(cnfg)

    t_app_key = config.get('global', 'app_key')
    t_app_secret_key = config.get('global', 'app_secret_key')
    t_access_token = config.get('global', 'access_token')
    t_access_secret_token = config.get('global', 'access_secret_token')

    return Twython(app_key=t_app_key,
                app_secret=t_app_secret_key,
                oauth_token=t_access_token,
                oauth_token_secret=t_access_secret_token)

def get_links(hashtags, total=1):
    results = {}
    twit = twitter_setup()
    #results = twit.search(q=hashtags, count=total)
    if hashtags == '':
        msg = 'You cannot enter a blank tag.'
        return msg
    tagsList = hashtags.strip().split(',')
    for tag in tagsList:
        tag = tag.strip()
        result = twit.search(q=tag, count=total)
    	key = tag.replace('#', '')
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
