import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By


s = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
driver = webdriver.PhantomJS(executable_path='/home/xu/a-project/python/dog/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

def get_questions(url, s, driver):
    global bag
    global link_bag
#   r = s.get("https://www.zhihu.com/search?type=content&q=%E8%AF%AD%E6%96%87", headers=headers)
#   bs0bj = BeautifulSoup(r.text, "lxml")

    driver = webdriver.PhantomJS(executable_path='/home/xu/a-project/python/dog/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.get(url)

    # 4 times default
    for i in range(2):
        print("[{}]waiting..." .format(i))
        page_button = driver.find_element(By.CLASS_NAME, "zu-button-more")
        page_button.click()
        time.sleep(1.5)

    bs0bj = BeautifulSoup(driver.page_source, "lxml")

    topics = bs0bj.findAll("li", {"class": "item clearfix"})
    for topic in topics:
        title = topic.find("div", {"class": "title"})
        vote = topic.find("a", {"class": "zm-item-vote-count"})
        link = topic.find("div", {"class": "title"}).find("a")
        if link["href"] not in link_bag:
            link_bag.append(link["href"])
            bag.append([title.get_text(), vote.get_text(), link["href"]])

def show_questions():
    global bah
    index = 0
    for topic in bag:
        print(index, topic)
        index += 1
        if index > 30:
            break

def read_answer_A(url, s, headers):
    r = s.get(url, headers=headers)
    bs0bj = BeautifulSoup(r.text, "lxml")

    question_title = bs0bj.find("h2")
    question_detail = bs0bj.find("div", {"class": "zm-editable-content"})
    answers = bs0bj.findAll("div", {"class": "zm-editable-content clearfix"})
    
    if question_title == None:
        read_answer_B(url, s, headers)
        return 
    else:
        print("<---plane A--->")

    try: 
        print(">" * 150)
        print(question_title.get_text().strip())
        print(question_detail.get_text().strip())
        print(">" * 150)
        for answer in answers:
            print(answer.get_text())
            print(">" * 100)
    except AttributeError:
        print("can't found!")

def read_answer_B(url, s, headers):
    r = s.get(url, headers=headers)
    bs0bj = BeautifulSoup(r.text, "lxml")

    print("<---plane B--->")
    question_title = bs0bj.find("h1", {"class": "QuestionHeader-title"})
    question_detail = bs0bj.find("div", {"class": "QuestionHeader-detail"})
    answers = bs0bj.findAll("div", {"class": "List-item"})

    print(">" * 150)
    print(question_title.get_text().strip())
    print(question_detail.get_text().strip())
    print(">" * 150)

    for answer in answers:
        try:
            print(answer.find("span", {"class": "RichText CopyrightRichText-richText"}).get_text())
            print(">" * 100)
        except:
            continue


bag = []
link_bag = []
while True:
    action = input("what next? ")
    action = action.split(" ")
    if action[0] == "search":
        key_words = action[1:]
        sentence = ''
        for key_word in key_words:
            sentence += key_word
            sentence += ' '
        url = "https://www.zhihu.com/search?type=content&q=" + quote(sentence)
        os.system('clear')
        get_questions(url, s, driver)
        os.system('clear')
        show_questions()


    elif action[0] == "back":
        os.system('clear')
        show_questions()
    elif action[0] == "go":
        try:
            index_enter = int(action[1])
            url = "https://www.zhihu.com" + bag[index_enter][2]
            os.system('clear')
            read_answer_A(url, s, headers)
        except:
            continue
    elif action[0] == "quit":
        print("see you, my friend.")
        break




