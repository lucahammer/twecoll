This is a Python 3 fork of twecoll by [@jdevoo](https://github.com/jdevoo/). The original twecoll isn't maintained anymore, but jdevoo created [nucoll](https://github.com/jdevoo/nucoll) in Go.

Twecoll3 is a Twitter command-line tool written in Python. It can be used to retrieve data from Twitter.

## Installation

Twecoll uses oauth and has been updated to support the 1.1 version of the Twitter REST API. Register your own copy of twecoll3 on http://apps.twitter.com and copy the consumer key and secret.

The first time you run a twecoll3 command, it will ask you for the consumer key and consumer secret. It will then retrieve the oauth token. Follow the instructions on the console. An HTTP Error 401 will be thrown if the key and secret cannot be used to retrieve the access token details.

## Examples

#### Downloading Tweets

Twecoll3 can download up to 3200 tweets for a handle or run search queries.

```
$ twecoll3 tweets luca
```

This would generate a luca.jsonl file containing all tweets including timestamp and text (utf-8).
In order search for tweets related to a certain hashtag or run a more advanced query, use the -q switch and double-quotes around the query string:

```
$ twecoll3 tweets -q "#hashtag"
```

This will also generate a .twt file name with the url-encoded search string.

#### Generating a Graph

It is possible to generate a GML file of your first and second degree relationships on Twitter. This is a two-step process that takes time due to API throttling by Twitter. In order to generate the graph, twecoll3 retrieves the handle's friends (or followers) and all friends-of-friends (2nd degree relationships). It then calculates the relations between those, ignoring 2nd degree relationships to which the handle is not connected. In other words, it looks only for friend relationships among the friends/followers of the handle or query tweets initially supplied.

First retrieve the handle details

```
$ twecoll3 init luca
```

This generates a luca.dat file. It also populates an img directory with avatar images. It is also possible to initialize from a .twt file using the -q option. In this example, retrieve friends of each entry in the .dat file.

```
$ twecoll3 fetch luca
```

This populates the fdat directory. You can now generate the graph file using the defaults.

```
$ twecoll3 edgelist luca
```

This generates a luca.gml file in Graph Model Language. If you have installed the python version of igraph, a .png file will also be generated with a visualization of the GML data. You can also use other packages to visualize your GML file, e.g. Gephi.

The GML file will include friends, followers, memberships and statuses counts as properties. If followers count is not equal to zero, the friends-to-followers and listed-to-followers ratios will be calculated.

## Usage

Twecoll has built-in help, version and API status switches invoked with -h, -v and -s respectively. Each command can also be invoked with the help switch for additional information about its sub-options.

```
$ twecoll3 -h
usage: twecoll3 [-h] [-v] [-s]
               {resolve,init,fetch,tweets,likes,edgelist} ...

Twitter Collection Tool

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -s, --stats           show Twitter throttling stats and exit

sub-commands:
  {resolve,init,fetch,tweets,likes,edgelist}
    resolve             retrieve user_id for screen_name or vice versa
    init                retrieve friends data for screen_name
    fetch               retrieve friends of handles in .dat file
    tweets              retrieve tweets
    likes               retrieve likes
    edgelist            generate graph in GML format
```

## Changes

- Version 1.1 - Initial commit
- Version 1.2 - Added option to init to retrieve followers instead of friends
- Version 1.3 - simplified metrics now included in GML file
- Version 1.4 - Simplified membership retrieval and improved graphs
- Version 1.5 - Changes to community finding and visualization
- Version 1.6 - Added support for multiple arguments in edgelist
- Version 1.7 - Added ability to add list members to dat file
- Version 1.8 - Fetch tweets from list for a given user
- Version 1.9 - Renamed favorites to likes
- Version 1.10 - Restored possibility to mix files using edgelist
- Version 1.11 - Suppress nodes with missing data in edgelist by default
- Version 1.12 - Improved init
- Version 1.13 - Added option to skip mentions from queries in init
- Version 2.0 - Rewrite to support Python 3.
