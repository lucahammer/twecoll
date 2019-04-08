This is a Python 3 fork of twecoll by [@jdevoo](https://github.com/jdevoo/). The original twecoll isn't maintained anymore, but jdevoo created [nucoll](https://github.com/jdevoo/nucoll) in Go.

Twecoll3 is a Twitter command-line tool written in Python. It can be used to retrieve data from Twitter.

## Installation

```
$ pip install twecoll3
```

Twecoll uses oauth and has been updated to support the 1.1 version of the Twitter REST API. Register your own copy of twecoll3 on http://apps.twitter.com and copy the consumer key and secret.

The first time you run a twecoll3 command, it will ask you for the consumer key and consumer secret. It will then retrieve the oauth token. Follow the instructions on the console.

## Examples

#### Downloading Tweets

Twecoll3 can download up to 3200 tweets for a handle or run search queries (limited to the last 7-10 days).

```
$ twecoll3 tweets luca
```

This would generate a luca.tweets.jsonl file containing all tweets.
In order search for tweets related to a certain hashtag or run a more advanced query, use the -q switch and quotes around the query string:

```
$ twecoll3 tweets -q "#hashtag"
```

This will also generate a .tweets.jsonl file name with the url-encoded search string.

#### Generating a Graph

A retweet network can be generated without further data collection. This works for a user as well as a search query. Retweet network of a user is quite useless.

```
$ twecoll3 network luca
```

If you want to generate a follow network, you first need to generate a file containing the included users.
Then fetch their followings (limited to 5k followings per default; 15 accounts per 15 minutes) and finally generate the network:

```
$ twecoll3 init luca
$ twecoll3 fetch luca
$ twecoll3 edgelist luca
```

## Usage

Twecoll3 has built-in help. Each command can also be invoked with the help switch for additional information about its sub-options.

```
$ twecoll3 --help
usage: twecoll3 [--help]
               {init,fetch,tweets,likes,network,edgelist} ...

Twitter Collection Tool

optional arguments:
    --help            show this help message and exit


sub-commands:
  {resolve,init,fetch,tweets,likes,edgelist}
    assistant           step by step for new users
    resolve             retrieve user_id for screen_name or vice versa
    init                retrieve friends data for screen_name
    fetch               retrieve friends of handles in .dat file
    tweets              retrieve tweets
    network             generate retweet graph in GEXF format
    edgelist            generate follow graph in GDF format
```

## Changes

- Version 2.0 - Rewrite to support Python 3.
