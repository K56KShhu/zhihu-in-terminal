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



def main():
    driver = webdriver.PhantomJS(executable_path='/home/xu/a-project/python/dog/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
#   driver.get("https://www.zhihu.com/search?type=content&q=%E5%A4%A9%E6%B0%94")
    driver.get("https://www.zhihu.com/search?type=content&q=%E8%AF%AD%E6%96%87")
    time.sleep(1)


#   xpath_topics = '//li[@class="item clearfix"]'
    xpath_topics = '//li[@data-type="Answer"]'
    xpath_vote = '//div[@class="entry-left hidden-phone"]/a'
    xpath_author = '//div[@class="author-line summary-wrapper"]'
    xpath_summary = '//div[@class="summary hidden-expanded"]'
    xpath_title = '//div[@class="title"]'

    L = []
    topics = driver.find_elements(By.XPATH, xpath_topics)
    for topic in topics:
        title = topic.find_element(By.XPATH, xpath_title)
        vote = topic.find_element(By.XPATH, xpath_vote)
        author = topic.find_element(By.XPATH, xpath_author)
        summary = topic.find_element(By.XPATH, xpath_summary)
        L.append([title.text, vote.text, author.text, summary.text])

    
    print(L)
    
    for t in L:
        print(t)
        print("\n")

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

