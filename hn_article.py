from operator import itemgetter

import requests
import json
from plotly.graph_objs import Bar
from plotly import offline

# Make an API call, and store the response
API_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
response = requests.get(API_URL)
print(f"Status code: {response.status_code}")

# Process infomation about each submission
submission_ids = response.json()
submission_dicts = []
for submission_id in submission_ids[:30]:
    # Make a separate API call for each submission
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    response = requests.get(url)
    print(f"id: {submission_id}\tstatus: {response.status_code}")
    response_dict = response.json()

    # Build a dictionary for each article
    submission_dict = {
        'title' : response_dict['title'],
        'hn_link' : f"https://news.ycombinator.com/item?id={submission_id}",
        'comments' : response_dict['descendants'],
    }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

for submission_dict in submission_dicts:
    print(f"\nTitle: {submission_dict['title']}")
    print(f"Discussion link : {submission_dict['hn_link']}")
    print(f"Comments : {submission_dict['comments']}")

repo_comments, repo_links = [], []
for article in submission_dicts[:5]:
    repo_name  = article['title']
    repo_comment = article['comments']
    repo_url = article['hn_link']
    repo_link = f"<a href='{repo_url}'>{repo_name}</a>"

    repo_comments.append(repo_comment)
    repo_links.append(repo_link)

# Make visualization
data = [{
    'type' : 'bar',
    'x' : repo_links,
    'y' : repo_comments,
    'marker' : {
        'color' : 'rgb(60, 100, 150)',
        'line' : {'width' : 1.5, 'color' : 'rgb(25, 25, 25)'}
    },
    'opacity' : 0.6
}]

title = 'The Five Most Commented Articles'
my_layout = {
    'title' : title,
    'titlefont' : {'size' : 28},
    'xaxis' : {
        'title' : "Article's Name",
        'titlefont' : {'size' : 24},
        'tickfont' : {'size' : 14},
    },
    'yaxis' : {
        'title' : "Comments",
        'titlefont' : {'size' : 24},
        'tickfont' : {'size' : 14},
    },
}

fig = {
    'data' : data,
    'layout' : my_layout,
}

offline.plot(fig, filename='html/hn_visual.html')