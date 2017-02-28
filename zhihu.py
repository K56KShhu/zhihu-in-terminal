import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

"""
url = "https://www.zhihu.com/search?type=content&q=%E5%A4%A9%E6%B0%94"
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

r = requests.get(url, headers=headers)
bs0bj = BeautifulSoup(r.text, "lxml")
questions = bs0bj.findAll("div", {"class":"title"})
for q in questions:
        print("<"+q.get_text()+">\n")
"""

def more_page(driver):
    global topics
    page_button = driver.find_element(By.CLASS_NAME, "zu-button-more")
    page_button.click()
    time.sleep(2)
    titles = driver.find_elements(By.CLASS_NAME, "title")
    for t in titles:
        t = t.text
        if t not in topics:
            print("<"+t+">\n")
            topics.append(t)

xpath_vote = '//li[@class="item clearfix"]//div[@class="entry-left hidden-phone"]/a/'
xpath_author = '//li[@class="item clearfix"]//div[@class="author-line summary-wrapper"]'
xpath_summary = '//li[@class="item clearfix"]//div[@class="summary hidden-expanded"]'


def main():
    driver = webdriver.PhantomJS(executable_path='/home/xu/a-project/python/dog/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.get("https://www.zhihu.com/search?type=content&q=%E5%A4%A9%E6%B0%94")
    time.sleep(1)

    topics = driver.find_element(By.)
    
    
    for t in titles:
        t = t.text
        if t not in topics:
            print("<"+t+">\n")
            topics.append(t)

    show_more = input("* press [m] to show, [q] to quit: ")
    while True:
        if show_more == "m":
            more_page(driver)
            show_more = input("\npress [m] to show more, [q] to quit: ")
        elif show_more == 'q':
            break


if __name__ == "__main__":
    theme = []
    main()

