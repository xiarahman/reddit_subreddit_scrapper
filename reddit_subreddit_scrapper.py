from bs4 import BeautifulSoup
from requests import get
from fake_useragent import UserAgent
import pandas as pd

ua = UserAgent()

# functional to create user agent
def got_soup(u):
    uag = get(u, headers={'User-Agent': ua.chrome})
    return BeautifulSoup(uag.text, 'html.parser')
SubR = 'Showerthoughts'
url = 'https://old.reddit.com/r/{}?sort=top&t=week'.format(SubR) # old reddit url
soup = got_soup(url)

things = soup.findAll('div', {'class': 'thing'}) # old reddit titles

all_posts = [] # initiate all posts to be appended later with posts

for thing in things:
    likes = thing.find('div', class_='likes').text
    likes = likes.replace('k','').replace('•','0') # remove 'k' and replace '•' with '0'
    if "."  in likes:
        likes = float(likes)
        likes = ('%f' % likes).rstrip('0').replace('.','') # remove leading 0 and points
        likes = int(likes)*100
    else:
        likes = int(likes)
    title = thing.find('p', class_='title').text
    post = {'likes':likes, 'title':title}
    all_posts.append(post)

# function to get sorted likes descending
def myFunc(e):
  return e['likes']
all_posts.sort(key=myFunc, reverse=True)

# print the posts
# for all_post in all_posts:
#     print(all_post['likes'], ' - ', all_post['title'])

all_posts = pd.DataFrame(all_posts, columns = ['likes', 'title'])
all_posts.head()
all_posts.info()
all_posts.to_csv(r'D:/scripts/'+ SubR + '_DS.csv',index=False)
