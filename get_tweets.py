import tweepy
import pandas as pd
import time

client = tweepy.Client(
    bearer_token='#############')

query = 'diversidade -is:retweet  lang:pt'

# coleta o tweets com a quantidade desejada e numero de runs desejados e faz uma pausa de 15 min entre cada run


def collect_tweets(num_tweets, num_runs):

    db_tweets = pd.DataFrame(columns=['text'])
    program_start = time.time()
    for i in range(0, num_runs):
        # começa a rodada
        start_run = time.time()

        tweets = tweepy.Paginator(client.search_recent_tweets, query=query,
                                  tweet_fields=['text'], max_results=100).flatten(num_tweets)

        tweet_list = [tweet for tweet in tweets]

        n_tweets = 0
        for tweet in tweet_list:

            text = tweet.text
            array = [text]
            db_tweets.loc[len(db_tweets)] = array
            n_tweets += 1

        # Termina a rodada:
        end_run = time.time()
        duration_run = round((end_run-start_run)/60, 2)

        print('No. de tweets coletados nessa rodada {} é {}'.format(i + 1, n_tweets))
        print('Tempo gasto na coleta {} foi {} minutos'.format(i+1, duration_run))


        time.sleep(920)

    # salvar o arquivo no destino
    # db_tweets.to_csv(r'path', header=True)

    # Encerra o número total de rodadas
    program_end = time.time()
    print('A coleta está completa!')
    print('O tempo total foi de {} hrs.'.format(
        round(program_end - program_start)/60, 2))


collect_tweets(3000, 20)
