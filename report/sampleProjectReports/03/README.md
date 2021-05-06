# TweetTrump

The following instruction are oriented towards UNIX-like OS.
By the way, the application was largely developed and tested on Windows 10 OS and lastly Ubuntu.

# Requirements:

* Redis (extracted inside the folder `redis`)
* Python (3.6 is good enough)
* Python packages (listed in `requirements.txt`)
* Internet Connection

# first steps

Install Python package `virtualenv
```
pipx install virtualenv
```

Position inside the project folder and create the virtual environment

```
$ virtualenv .venv
```

then activate it

```
$ source bin/activate
```

And then, inside the environment, we will install all python packages required with:

```
$ pip install -r requirements.txt
```

## Run the System

The system is designed with two indipendent module `redis_tweet.py` and `redis_sentiment.py`
The former can be seen as the *producer* of new tweets, while the second would be the *consumer*.

Since it was used Redis, it is safe to run first the producer without losing any tweets.

```
$ pip3 src/redis_tweets.py
```

and then we will run the consumer

```
$ pip3 src/redis_sentiment.py
```

Both programs are schedule to run the same jobs every ~30 secs.
So they need you to interrupt them (i.e. `ctlr+c`)

## Run the Application

In order to run the web application is it necessery to enter the `/myapp/` folder,
and then run start the local server with:

```
$ flask run
```

Now you should be able to browse through the application in any web browser at:

http://127.0.0.1:5000/home

___

In case of necessity, please contact us:  
Alessandro P. - [alessandro.piotti@studenti.unitn.it](mailto:alessandro.piotti@studenti.unitn.it)  
Fabio T.D.T. - [f.taddeidallatorre@studenti.unitn.it](mailto:f.taddeidallatorre@studenti.unitn.it)

