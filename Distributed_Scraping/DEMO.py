import multiprocessing as mp
import time
from urllib.request import urlopen ,urljoin
from bs4 import BeautifulSoup
import re

base_url = 'http://morvanzhou.github.io/'
# base_url = 'http://www.baidu.com'

if base_url !='http://morvanzhou.github.io/':
    restricted_crawl = True
else:
    restricted_crawl = False

def crawl(url):
    response = urlopen(url)
    return response.read()

def parse(html):
    soup = BeautifulSoup(html,'lxml')
    urls = soup.find_all('a' , {'href' : re.compile('^/.+?/$')})
    title = soup.find('h1').get_text().strip()
    page_urls = set([urljoin(base_url,url['href'])for url in urls],)
    url = soup.find('meta' , {'property':'og:url'})['content']
    return title, page_urls, url

# prase(crawl(base_url))

unseen = set([base_url,])
seen = set()
pool = mp.Pool(4)

count, t1 = 1, time.time()

#normal method -----too slow
# while len(unseen) != 0:
#     if restricted_crawl and len(seen) > 20:
#         break
#
#     print('\nDistributed Crawling...')
#     htmls = [crawl(url) for url in unseen]
#
#     print('\nDistributed parsing...')
#     results = [parse(html) for html in htmls]
#
    # print('\nAnalysing...')
    # seen.update(unseen)
    # unseen.clear()
#
#     for title, page_urls, url in results:
#         print(count,title,url)
#         count += 1
#         unseen.update(page_urls - seen)
#
# print('Total time: %.1f s' % (time.time()-t1),)

while len(unseen) !=0:
    if restricted_crawl and len(seen) > 20:
        break

    print('\nDistributed Crawling...')
    crawl_jobs = [pool.apply_async(crawl , args=(url,)) for url in unseen]
    htmls = [j.get() for j in crawl_jobs]

    print('\nDistributed parsing...')
    parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
    results = [j.get() for j in parse_jobs]

    print('\nAnalysing...')
    seen.update(unseen)
    unseen.clear()

    for title, page_urls, url in results:
        print(count, title, url)
        count +=1
        unseen.update(page_urls - seen)
# htmls = [crawl(url) for url in unseen]
# print(htmls)
print('Total time: %.1f s' % (time.time()-t1),)