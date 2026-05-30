import requests
from collections import Counter
def get_posts():

    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts"
    )

    return response.json()
def get_user_posts(user_id):

    posts = get_posts()

    return [
        post
        for post in posts
        if post["userId"] == user_id
    ]


def posts_per_user():

    posts = get_posts()

    counter = Counter()

    for post in posts:
        counter[post["userId"]] += 1

    return counter

