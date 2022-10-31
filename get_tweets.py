import tweepy
import pandas as pd
import time

client = tweepy.Client(
    bearer_token='AAAAAAAAAAAAAAAAAAAAAJ6yiAEAAAAAKAEBbjeBsoSN1JpktBma3z87FQM%3DA6QivZoLjoSgeD7Wl7'
                 'csAuzym0mxyRkpL3JN1NI55siZ3f4a3X')

query = 'diversidade -is:retweet  lang:pt'


def scraptweets(numTweets, numRuns):

    db_tweets = pd.DataFrame(columns=['text']
                             )
    program_start = time.time()
    for i in range(0, numRuns):
        # We will time how long it takes to scrape tweets for each run:
        start_run = time.time()

        tweets = tweepy.Paginator(client.search_recent_tweets, query=query,
                                  tweet_fields=['text'], max_results=100).flatten(numTweets)

        tweet_list = [tweet for tweet in tweets]

        noTweets = 0
        for tweet in tweet_list:  # Pull the values

            try:
                text = tweet.text
            except AttributeError:  # Not a Retweet
                # Add the 11 variables to the empty list - ith_tweet:
                text = tweet.full_text
            ith_tweet = [text]  # Append to dataframe - db_tweets
            # increase counter - noTweets
            db_tweets.loc[len(db_tweets)] = ith_tweet
            noTweets += 1

        # Run ended:
        end_run = time.time()
        duration_run = round((end_run-start_run)/60, 2)

        print('no. of tweets scraped for run {} is {}'.format(i + 1, noTweets))
        print('time take for {} run to complete is {} mins'.format(i+1, duration_run))

        # 15 minute sleep time# Once all runs have completed, save them to a single csv file:
        time.sleep(920)

    db_tweets.to_csv(r'/Users/biancacamargodepaulamelo/PycharmProjects/pythonProject1/tweets90.csv', header=True)

    program_end = time.time()
    print('Scraping has completed!')
    print('Total time taken to scrap is {} minutes.'.format(
        round(program_end - program_start)/60, 2))


scraptweets(2500, 10)
