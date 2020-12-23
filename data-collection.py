import twitter
import time
import pandas as pd

def oauth_login():
    CONSUMER_KEY = 'G0aUIZWXmT73uFM4cDKYyEOIb'
    CONSUMER_SECRET = 'cEm3FsUgWNPu44BO3PKTRyy4CEYazHV0PS51BHoTsKkbrTnyML'
    OAUTH_TOKEN = '1310722997628567552-ceq2m7K7h97cs5Zs77fVuLh33MOrXc'
    OAUTH_TOKEN_SECRET = 'GAN1tboAUNPaaymhkyvd8snx0cTJv3Njq8etaZM8Vh5BA'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


twitter_api = oauth_login()

print(twitter_api)




def twitter_search(twitter_api, q, max_results=1000, **kw):
    # See https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
    # and https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
    # for details on advanced search criteria that may be useful for
    # keyword arguments

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q=q, count=1000, **kw)

    statuses = search_results['statuses']

    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://developer.twitter.com/en/docs/basics/rate-limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.

    # Enforce a reasonable limit
    max_results = min(100000, max_results)

    for _ in range(1000):  # 10*100 = 1000
        if _ % 100 == 0:
            time.sleep(60 * 15)
            print(_)

        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError as e:  # No more results when next_results doesn't exist
            break

        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([kv.split('=')
                       for kv in next_results[1:].split("&")])

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

        if len(statuses) > max_results:
            break

    return statuses


def save_to_pandas(data, fname):
    df = pd.DataFrame.from_records(data)
    df.to_pickle(fname)
    return df


def load_from_mongo(fname):
    df = pd.read_pickle(fname)
    return df


q = 'Tesla'

twitter_api = oauth_login()

results = twitter_search(twitter_api, q, max_results=100000)

df = save_to_pandas(results, 'search_results_{}.pkl'.format(q))

df.to_csv('Spotify.csv', encoding='utf-8-sig')
