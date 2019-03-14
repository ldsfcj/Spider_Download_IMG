from bs4 import BeautifulSoup
import requests
import re
import os

URL = 'http://www.ngchina.com.cn/animals/'

html = requests.get(URL).text
soup = BeautifulSoup(html, 'lxml')
img_url = soup.find_all('ul' , {'class' : 'img_list'})
# img_source = soup.find_all('img',re.compile('src=(.*?)'))
# print(len(img_url))
# print(img_url)
os.makedirs('./pictures/' , exist_ok=True)
# imgs = img_url.find_all('img')
# print(img_url)
for ul in img_url:
    imgs = ul.find_all('img')
    for img in imgs:
        img_src = img['src']
        r = requests.get(img_src, stream=True)
        img_name = img_src.split('/')[-1]
        with open('./pictures/%s' % img_name,'wb') as f:
            for chunk in r.iter_content(chunk_size=256):
                f.write(chunk)
        print('Download %s successfully!' % img_name)