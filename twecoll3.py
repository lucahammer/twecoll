import os
import click
import yaml
import json
from TwitterAPI import TwitterAPI, TwitterPager
from tqdm import tqdm

DIR = 'local_data'
FDAT_DIR = '{}/fdat'.format(DIR)


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

# Get IDs of the accounts a given account follows
# over5000 allows to collect more than 5000 friends


def collect_friends(account_id, cursor=-1, over5000=False):
    ids = []
    r = api.request('friends/ids', {'user_id': account_id, 'cursor': cursor})

    if 'errors' in r.json():
        if r.json()['errors'][0]['code'] == 34:
            return(ids)

    for item in r:
        if isinstance(item, int):
            ids.append(item)
        elif 'message' in item:
            print('{0} ({1})'.format(item['message'], item['code']))

    if over5000:
        if 'next_cursor' in r.json:
            if json['next_cursor'] != 0:
                ids = ids + collect_friends(account_id, json['next_cursor'])

    return(ids)


def get_friends(friend_id):
    friends = []
    try:
        with open('{0}/{1}.f'.format(FDAT_DIR, friend_id)) as f:
            for line in f:
                friends.append(int(line))
    except:
        pass
    return (friends)


def save_friends(user, ids):
    with open('{0}/{1}.f'.format(FDAT_DIR, user), 'w', encoding='utf-8') as f:
        f.write(str.join('\n', (str(x) for x in ids)))


def collect_and_save_friends(user, refresh=False):
    if not refresh and os.path.exists('{0}{1}.f'.format(FDAT_DIR, user)):
        return('Already saved: {}'.format(user))
    else:
        friends = collect_friends(user)
        save_friends(user, friends)
        return('Friends saved: {}'.format(user))


@click.group()
def cli():
    pass

# Collect and save Tweets
@cli.command()
@click.argument('query', required=False)
@click.option('-q',
              help='Optional: search query')
def tweets(query='', filename='', q=''):

    # todo: convert into valid filenames. (function)
    if filename == '':
        if query != '':
            filename = '{0}/{1}.tweets.jsonl'.format(DIR, query)
        else:
            filename = '{0}/{1}.tweets.jsonl'.format(DIR, q)

    if len(q) > 0:
        r = TwitterPager(api, 'search/tweets',
                         {'q': q, 'count': 100, 'tweet_mode': 'extended'})
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


def load_accounts_from_file(filename):
    ids = []
    with open('{}/{}'.format(DIR, filename), 'r', encoding='utf-8') as f:
        for number, line in enumerate(f):
            item = json.loads(line)
            ids.append(item['user']['id'])
    return(list(set(ids)))


'''
# Todos

def init():

def fetch():

def gdf():

def gexf():
'''


@cli.command()
@click.option('--api_key', prompt='Go to https://developer.twitter.com/apps to create an app.\nPlease enter the API key',
              help='The Twitter API key.')
@click.option('--api_key_secret', prompt='Please enter the API key secret',
              help='The Twitter API key secret.')
def twitter_setup(api_key, api_key_secret):
    """Enter and save Twitter app credentials."""
    return(write_config(api_key, api_key_secret))


@cli.command()
@click.argument('assistant')
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
    if not os.path.exists('{}'.format(DIR)):
        os.mkdir('{}'.format(DIR))
    if not os.path.exists('{}'.format(FDAT_DIR)):
        os.mkdir('{}'.format(FDAT_DIR))
    try:
        api = create_api(config)
    except:
        click.echo('Something is wrong with your config.')
        config = twitter_setup()
        api = create_api(config)
    cli()
