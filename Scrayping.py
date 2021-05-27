import requests
import re
import os
import urllib
import time
from bs4 import BeautifulSoup

members_url = []
members_name = []
members_img_url = []

res = requests.get('https://nijisanji.ichikara.co.jp/member/')
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.find_all(href=re.compile(r'nijisanji.ichikara.co.jp/member/([a-z | A-Z]+)'))

for i in range(len(links)):
  members_url.append(links[i].attrs['href'])

for url in members_url:
  m = re.match(r'https://nijisanji.ichikara.co.jp/member/([a-z | A-Z]+)', url)
  members_name.append(m.group(1))

for member in members_url:
  res = requests.get(member)
  soup = BeautifulSoup(res.text, 'html.parser')
  img = soup.find(src=re.compile("nijisanji.ichikara.co.jp/wp-content/uploads/elementor/thumbs/"))
  if img:
    members_img_url.append(urllib.parse.quote_plus(img.attrs['src'], safe="/:?=&", encoding='utf-8'))

def download_url(url, dst, name):
  try:
    with urllib.request.urlopen(url) as web_file, open(os.path.join(dst, "%s.png" %name), 'wb') as local_file:
      local_file.write(web_file.read())
  except urllib.error.URLError as e:
    print(e)
  time.sleep(1)

for index, url in enumerate(members_img_url):
  print(url)
  download_url(url, 'folder', members_name[index])