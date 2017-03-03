import os
import time
import requests
from threading import Thread
from bs4 import BeautifulSoup
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


s = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

def get_questions(url):
    global one_topic_bag
    global link_bag

    driver = webdriver.PhantomJS(executable_path='/home/xu/a-project/python/dog/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.get(url)

    # 2 times default
    for i in range(2):
        print("[{}]waiting..." .format(i))
        try:
            page_button = driver.find_element(By.CLASS_NAME, "zu-button-more")
            page_button.click()
            time.sleep(1.5)
        except NoSuchElementException:
            break

    bs0bj = BeautifulSoup(driver.page_source, "lxml")

    topics = bs0bj.findAll("li", {"class": "item clearfix"})
    for topic in topics:
        title = topic.find("div", {"class": "title"})
        vote = topic.find("a", {"class": "zm-item-vote-count"})
        link = topic.find("div", {"class": "title"}).find("a")
        if link["href"] not in link_bag:
            link_bag.append(link["href"])
            one_topic_bag.append([link["href"], title.get_text(), vote.get_text()])

    return driver

def get_more_questions(url, driver):
    global one_topic_bag
    global link_bag
    global is_first_search

    for i in range(3):
        print("[{}]waiting..." .format(i))
        try:
            page_button = driver.find_element(By.CLASS_NAME, "zu-button-more")
            page_button.click()
            time.sleep(1.5)
        except NoSuchElementException:
            break

    bs0bj = BeautifulSoup(driver.page_source, "lxml")

    topics = bs0bj.findAll("li", {"class": "item clearfix"})
    for topic in topics:
        title = topic.find("div", {"class": "title"})
        vote = topic.find("a", {"class": "zm-item-vote-count"})
        link = topic.find("div", {"class": "title"}).find("a")
        if link["href"] not in link_bag:
            link_bag.append(link["href"])
            one_topic_bag.append([link["href"], title.get_text(), vote.get_text()])

    return driver



def show_questions():
    global one_topic_bag
    global first_search
    index = 0
    for topic in one_topic_bag:
        print("[{:d}] {} (vote {}) " .format(index, topic[1], topic[2]))
        index += 1

def read_answer_A(url, s, headers):
    r = s.get(url, headers=headers)
    bs0bj = BeautifulSoup(r.text, "lxml")

    question_title = bs0bj.find("h2")
    question_detail = bs0bj.find("div", {"class": "zm-editable-content"})
    answers = bs0bj.findAll("div", {"class": "zm-editable-content clearfix"})
    
    # there are some problems may be caused by cookies because of no login
    if question_title == None:
        read_answer_B(url, s, headers)
        return 
    else:
        print("<---plane A--->")

    i = 0
    try: 
        print(">" * 150)
        print(question_title.get_text().strip())
        print(question_detail.get_text().strip())
        print(">" * 150)
        for answer in answers:
            print(i)
            i += 1
            print(answer.get_text(separator='\n'))
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
            print(answer.find("span", {"class": "RichText CopyrightRichText-richText"}).get_text(separator='\n'))
            print(">" * 100)
        except:
            continue

def show_search_history():
    global search_history_bag
    for history in search_history_bag:
        print(history)

begin = time.time()
search_history_bag = []
link_bag = []
answers_bag = []
is_first_search = True
os.system('clear')
while True:
    action = input("\nwhat next? ")
    action = action.split(" ")
    # search the questions
    if action[0] == "search":
        one_topic_bag = []
        key_words = action[1:]
        search_history_bag.append(key_words)
        sentence = ''
        for key_word in key_words:
            sentence += key_word
            sentence += ' '
        url = "https://www.zhihu.com/search?type=content&q=" + quote(sentence)
        first_search_driver = get_questions(url)
        is_first_search = False
        os.system('clear')
        show_questions()
    # search more questions in the basic of the first search
    elif action[0] == "more" and is_first_search == False:
        get_more_questions(url, first_search_driver)
        os.system('clear')
        show_questions()
    # back to the question page
    elif action[0] == "back":
        os.system('clear')
        show_questions()
    # get into one of the question
    elif action[0] == "go":
        try:
            index_enter = int(action[1])
            url = "https://www.zhihu.com" + one_topic_bag[index_enter][0]
            os.system('clear')
            read_answer_A(url, s, headers)
        except:
            continue
    # quit the program
    elif action[0] == "quit":
        end = time.time()
        seconds = end - begin
        if seconds < 60:
            print("* spend {:.2f} seconds" .format(seconds))
        else:
            minutes = seconds / 60
            print("* spend {:.2f} minutes" .format(minutes))
        print("* see you, my friend.")
        break
    # get some help information
    elif action[0] == "help":
        print("* search [key words]      <----support multiple key words")
        print("* go [question index]")
        print("* back                    <----back to questions page")
        print("* help                    <----show this page")
        print("                          <----made by zkyyo")
    # show the history of the key words
    elif action[0] == "history":
        show_search_history()
    # author
    elif action[0] == "zkyyo":
        print("* it's me")


