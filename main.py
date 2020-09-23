import argparse
import csv
import datetime
import logging
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError
import re

is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')

logging.basicConfig(level=logging.INFO)

import news_page_objects as news
from common import config


logger = logging.getLogger(__name__)

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info(f'Beginning scraper for {host}')
    homepage = news.HomePage(news_site_uid, host)

    articles =[]
    for link in homepage.article_links:

        article = _fetch_article(news_site_uid, host, link)
        
        if article:
            logger.info('Article fetched!!')
            articles.append(article)
            #print(article.title)

    #print(len(articles))
    _save_articles(news_site_uid, articles)

def _fetch_article(news_site_uid, host, link):
    logger.info(f'Start fetching article at {link}')

    article = None

    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Invalid article. There is no body')
        return None

    return article

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    news_sites_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_sites',
                        help='The news site that you want to scrape',
                        type=str,
                        choices=news_sites_choices)

    args = parser.parse_args()
    _news_scraper(args.news_sites)

def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return f'{host}{link}'
    else:
        return f'{host}/{link}'

def _save_articles(news_site_uid, articles):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = f'{news_site_uid}_{now}_articles.csv'

    csv_headers = list(filter(lambda property: not property.startswith(''), dir(articles[0])))

    with open(out_file_name, mode='w+', encoding= 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles:
            row = (str(getattr(article, prop)) for prop in csv_headers)
            write.writerow(row)

