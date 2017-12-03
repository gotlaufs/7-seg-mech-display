#!/usr/bin/env python3

import facebook
import requests


def some_action(post):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    #print(post['created_time'])
    print(post)
    id = post["id"]
    comments = graph.get_connections(id, 'comments')

    print(comments)

# Graph API explorer token for 7-seg Parrot page
access_token = "EAACEdEose0cBACQJil85gDqiRttA7wbTn1wlS2WosKDAbKzjRBLxD8lHpxjf7WebNUZCUwPSg0tKeY23L8GOxIYSCZCnXZBWs2DIiRx1nPb1KzC8zwqs07ifXSUHeQa4Y8J50u8KHdv5BywUVCWxbvIUgZAS9UAShffXqn9VT4hY2XSNE5imVIou4RYdlOwdfIlJdSHEjQZDZD"

# Look at Bill Gates's profile for this example by using his Facebook id.
user = 'EK7seg'

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
posts = graph.get_connections(profile['id'], 'posts')

# Wrap this block in a while loop so we can keep paginating requests until
# finished.
while True:
    try:
        # Perform some action on each post in the collection we receive from
        # Facebook.
        [some_action(post=post) for post in posts['data']]
        # Attempt to make a request to the next page of data, if it exists.
        posts = requests.get(posts['paging']['next']).json()
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        break