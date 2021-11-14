from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import re
import csv

browser = webdriver.Chrome('D:\codefiles\chromedriver')
browser.get('http://www.kinopoisk.ru/')

d = pd.read_csv('films.csv', header=None, index_col=0, squeeze=True).to_dict()

time.sleep(50) #время для авторизации и подготовки окна начать сначала, надо пролистать вниз при выборе ответов

for triescount in range(8050):

    restartelement = browser.find_elements_by_css_selector('[class="modal-wrong-answer__restart-button button button_color_gradient-1"]')

    if not restartelement: #окна начать заново нет - начинаем цикл
        pictureid = browser.find_element_by_class_name("game__test-image-img").get_attribute("src") #получаем id картинки

        if pictureid in d.keys():
            pictureanswer = d.get(pictureid) #получаем правильный ответ из словаря
            browser.find_element_by_xpath('//*[text() = ("%s")]' % pictureanswer).click()
            time.sleep(0.85)
         
        if pictureid not in d.keys():
            text = browser.find_element_by_class_name("game__test-answers-item").text #сохраняем первый вариант ответа
            browser.find_element_by_class_name("game__test-answers-item").click() #кликаем первый вариант ответа
            time.sleep(1.4)

            try: #проверяем наличие окна неверный ответ
                browser.find_element_by_css_selector('[class="modal-wrong-answer__button"]')

                rightstring = browser.find_element_by_xpath('.//div[@class="modal-wrong-answer__title"]').text #вытаскиваем текст из окна неверного ответа
                pictureanswer = ''.join(re.findall('«([^"]*)»', rightstring)) #преобразуем и вытаскиваем правильный ответ из текста
                if len(pictureanswer) > 2:
                    d[pictureid]=(pictureanswer) #добавляем название картинки и правильный ответ из окна в словарь
               
                browser.find_element_by_css_selector('[class="modal-wrong-answer__button"]').click()
                time.sleep(1.4)

            except NoSuchElementException: #окна неверный ответ нет - начинаем цикл
                restartelementtwo = browser.find_elements_by_css_selector('[class="modal-wrong-answer__restart-button button button_color_gradient-1"]')
                if not restartelementtwo: #проверяем окно
                    d[pictureid]=(text) #добавляем название картинки и случайно полученный правильный ответ в словарь
                time.sleep(1.4)

    else:
        browser.find_element_by_xpath('.//button[@class="modal-wrong-answer__restart-button button button_color_gradient-1"]').click()
        time.sleep(1.4)

df = pd.DataFrame.from_dict(d, orient="index")
df.to_csv("films.csv") #преобразуем словарь в csv
