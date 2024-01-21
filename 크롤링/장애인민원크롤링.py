from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import os
import time
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

url = "https://www.sisul.or.kr" 

titles = []
links = []

for i in range(53):
    url_board = url + "/open_content/calltaxi/qna/qnaMsgList.do?pgno=" + str(i)

    res = request.urlopen(url_board)
    soup = BeautifulSoup(res, "html.parser")

    selector = "#detail_con > div.generalboard > table > tbody > tr > td.left.title > a"

    for a in soup.select(selector):
        titles.append(a.text)
        links.append(url + a.attrs["href"])

board_df = pd.DataFrame({"title": titles, "link": links}) 

urls = board_df['link']
driver = webdriver.Chrome()

contents = []

for x in urls:
    driver.get(x)
    time.sleep(5)

    article = driver.find_element(By.XPATH, '//*[@id="detail_con"]/div[2]/table/tbody/tr[3]/td').text
    # article = driver.find_element(By.CSS_SELECTOR, '#detail_con > div.generalboard > table > tbody > tr:nth-child(3) > td').text
    # //*[@id="detail_con"]/div[2]/table/tbody/tr[3]/td
    # #detail_con > div.generalboard > table > tbody > tr:nth-child(3) > td
    article = article.replace('\n', "")
    article = article.replace('\t', "")
    article = article.replace('\\', "")
    article = article.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")

    contents.append(article)

board_df['content'] = contents
board_df.to_csv('장애인콜택시민원텍스트데이터.csv', index=False)