import os
import click
import yaml
import json
from TwitterAPI import TwitterAPI, TwitterPager
from tqdm import tqdm

DIR = 'local_data'


def load_config(file='config.yaml'):
    if os.path.exists(file):
        with open(file, 'r') as ymlfile:
            config = yaml.safe_load(ymlfile)
        return (config)
    else:
        click.echo('No configuration found.')
        return(twitter_setup())


def write_config(api_key, api_secret_key, file='config.yaml'):
    config = dict(
        twitter=dict(
            api_key=api_key,
            api_secret_key=api_secret_key
        )
    )
    with open(file, 'w') as ymlfile:
        yaml.dump(config, ymlfile, default_flow_style=False)
    return (load_config(file))


def create_api(config):
    api = TwitterAPI(config['twitter']['api_key'],
                     config['twitter']['api_secret_key'],
                     auth_type='oAuth2'
                     )
    return (api)


# Collect and save Tweets
def tweets(query, filename='', q=False):
    if filename == '':
        filename = '/{0}/{1}.tweets.jsonl'.format(DIR, query)

    if q:
        r = TwitterPager(api, 'search/tweets',
                         {'q': query, 'count': 100, 'tweet_mode': 'extended'})
    else:
        r = TwitterPager(api, 'statuses/user_timeline',
                         {'screen_name': query, 'count': 100, 'tweet_mode': 'extended'})

    n = 0
    with open(filename, 'a', encoding='utf-8') as f:
        for item in r.get_iterator(wait=2):
            n += 1
            if n % 1000 == 0:
                click.echo('{0} Tweets already collected. Oldest from {1}.'.format(
                    n, item['created_at']))
            if 'full_text' in item:
                json.dump(item, f)
                f.write('\n')
            elif 'message' in item and item['code'] == 88:
                click.echo(
                    'SUSPEND, RATE LIMIT EXCEEDED: {}\n'.format(item['message']))
                break
    click.echo('Saved {0} Tweets in {1}'.format(n, filename))
    return


'''
# Todos
def load():

def init():

def fetch():

def gdf():

def gexf():
'''


@click.command()
@click.option('--api_key', prompt='Go to https://developer.twitter.com/apps to create an app.\nPlease enter the API key',
              help='The Twitter API key.')
@click.option('--api_key_secret', prompt='Please enter the API key secret',
              help='The Twitter API key secret.')
def twitter_setup(api_key, api_key_secret):
    """Enter and save Twitter app credentials."""
    return(write_config(api_key, api_key_secret))


@click.command()
@click.option('--goal',
              type=click.Choice(
                  ['collect tweets', 'init accounts', 'fetch follows', 'create network', 'reset keys']),
              prompt='What do you want to do?',
              help='Choose a goal.')
def assistant(goal):
    """Step by step assistant for new users"""
    if goal == 'collect tweets':
        tweet_type = click.prompt(
            'Which method do you want to use to collect tweets?',
            type=click.Choice(
                ['query', 'user']
            ))
        if tweet_type == 'query':
            query = click.prompt('Please enter your search query')
            tweets(query, q=True)
        if tweet_type == 'user':
            query = click.prompt('Please enter the screen name')
            tweets(query)
    click.echo('Assistant finished.')


if __name__ == '__main__':
    config = load_config()
    os.mkdir('/{}'.format(DIR))
    try:
        api = create_api(config)
    except:
        click.echo('Something is wrong with your config.')
        config = twitter_setup()
        api = create_api()
    assistant()
