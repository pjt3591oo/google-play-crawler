import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs

from config.URL_config import TOP_URL, LOGIN_URL, BASE_URL
from config.ACCOUNT_config import EMAIL, PASSWORD

from models.commends import Commends
from database import db_session

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time

import sqlalchemy

def make_payload(page):
    return "start=%s&num=60&numChildren=0&cctcss=tall-cover&cllayout=NORMAL"%(page)


def connect_category(url):

    querystring = {"authuser": "0"}

    start = 0
    targets = list()
    pre_count = len(targets)
    current_count = len(targets)

    is_last = False

    while not is_last:
        payload = make_payload(start)
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
            'user-agen': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

        res = rq.post(url, data=payload, headers=headers, params=querystring)
        cate_soup = BeautifulSoup(res.content, 'lxml')
        pre_count = len(targets)
        current_soup = cate_soup.select('.card-content .details a.title')

        for s in current_soup:
            is_exist = False
            data = {'title': s.get('title'), 'link': urljoin(BASE_URL, s.get('href')), 'queryString': parse_qs(urlparse(s.get('href')).query)['id'][0]}
            for target in targets:
                if data['queryString'] == target['queryString']:
                    is_exist = True
            if not is_exist:
                targets.append(data)

        current_count = len(targets)

        if current_count == pre_count:
            is_last = True

        start += 60

    return targets


def google_login():
    driver = webdriver.Chrome('chromedriver')
    driver.get(LOGIN_URL)
    email = driver.find_element_by_css_selector('#Email')
    time.sleep(0.4)
    email.click()
    email.send_keys(EMAIL)
    email.send_keys(Keys.ENTER)
    time.sleep(0.4)

    password = driver.find_element_by_css_selector('#Passwd')
    password.send_keys(PASSWORD)
    password.send_keys(Keys.ENTER)


def get_category():
    lines = open('googleplay_catepory_link.txt', 'r').readlines()

    return [line.split('\n')[0] for line in lines]


def get_rating(rating_soup):

    if not len(rating_soup):
        return 0

    rating_style = rating_soup[0].get('style').split('.')[0]
    rating_style = re.sub('[^0-9]', '', rating_style)

    rating = int(rating_style) / 20
    return rating


def get_text(soup):
    if not len(soup):
        return ''

    return soup[0].text


def file_save(file_name, data):
    print(data)
    a = open(file_name, 'a')
    a.write(str(data['authorRating']) + ':::' + str(data['reviewContent']) + '\n')


def db_save(data):
    try:
        commend = Commends(data)
        db_session.add(commend)
        db_session.commit()
    except sqlalchemy.exc.DataError as err:
        db_session.rollback()


def data_parse(link):
    try:
        res = rq.get(link)
        soup = BeautifulSoup(res.content, 'lxml')

        app_title = get_text(soup.select('.id-app-title'))
        app_rating = get_rating(soup.select('.current-rating')) or 0.0
        app_rating_count = get_text(soup.select('.rating-count')) or 0
        review_columns = soup.select('.multicol div .single-review')

        for reviews_column_soup in review_columns:
            review_author_name = get_text(reviews_column_soup.select('.author-name'))
            review_date = get_text(reviews_column_soup.select('.review-date'))
            rating = get_rating(reviews_column_soup.select('.review-info-star-rating .current-rating')) or 0.0

            review_content = get_text(reviews_column_soup.select('.review-body')).replace('전체 리뷰', '').strip()

            data = {
                'title': str(app_title),
                'rating': float(app_rating),
                'ratingCount': int(app_rating_count),
                'authorName': str(review_author_name),
                'Date': review_date,
                'authorRating': float(rating),
                'reviewContent': str(review_content),
                'link': link,
            }

            file_save('commends.txt', data)
            # db_save(data)
    except:
        file_save('error.txt', link)


if __name__ ==  "__main__":
    print('commend collecting crawler')
    url = "https://play.google.com/store/apps/category/DATING/collection/topgrossing"

    categories = get_category()
    for category_link in categories:
        targets = connect_category(category_link)
        for target in targets:
            data_parse(target['link'])