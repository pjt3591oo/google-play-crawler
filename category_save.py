import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from config.URL_config import TOP_URL, LOGIN_URL, BASE_URL
from config.ACCOUNT_config import EMAIL, PASSWORD

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

driver = webdriver.Chrome('chromedriver')


def show(list):
    for li in list:
        print(li)


def get_bigCategory():
    res = rq.get(TOP_URL)
    soup = BeautifulSoup(res.content, 'lxml')

    categories = [urljoin(TOP_URL, a_tag.get('href'))
                  for a_tag in soup.select('.nav-list-item a')
                    if len(urlparse(a_tag.get('href')).path.split('/')) == 3 and a_tag.get('href').find('store') > -1
                  ]
    categories = list(set(categories))
    print(categories)
    return categories


def get_soup():
    return BeautifulSoup(str(driver.page_source), 'lxml')


def get_category(big_categories):
    '''
    email #Email
    password #Passwd
    '''

    all_categories = list()

    for big_category in big_categories:
        print(big_category)
        driver.get(big_category)
        big_cate_soup = get_soup()
        categories = big_cate_soup.select('.submenu-item-wrapper li a.child-submenu-link')

        all_categories += [urljoin(BASE_URL, a_tag.get('href')) for a_tag in categories]

    return all_categories


def connect_categories(categories):

    all_see_more = list()

    for category_link in categories:
        driver.get(category_link)
        see_more_soup = get_soup().select('a.see-more')

        more = [urljoin(BASE_URL, a_tag.get('href')) for a_tag in see_more_soup]

        all_see_more += more

        for a in more:
            print(a)

    return all_see_more


def google_login():
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


def save(data, finename):
    f = open(finename, 'a')
    f.write(data + '\n')


if __name__ == "__main__":
    print('category collecting crawler')

    google_login()
    big_categories = get_bigCategory()
    categories = get_category(big_categories)
    categories_views = connect_categories(categories)

    for category_link in categories_views:
        save(category_link, 'googleplay_catepory_link.txt')
    driver.quit()