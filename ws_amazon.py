import requests

from bs4 import BeautifulSoup
from selenium import webdriver

url = input("Enter URL here : ")

def get_all_reviews(show_all_reviews):
    driver = webdriver.Chrome()
    driver.get(show_all_reviews)
    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    soup = BeautifulSoup(res, 'lxml')
    image = soup.find_all('div')
    # container = image.find('div', {'class':'a-container'})
    print(image)

def open_amazon_url(url):

    #Get url (amazon.in / amazon.com)
    new_url = url.split('/')
    get_start_url = new_url[0]  +'//'+ new_url[2]

    driver = webdriver.Chrome()
    driver.get(url)
    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    soup = BeautifulSoup(res, 'lxml')
    image = soup.find('div', {'id':'dp'})
    container = image.find('div', {'class':'a-container'})
    
    
    # div = image.find('div', {'id':'dpx-anywhere-atf_feature_div'})
    # print(container.text)
    # div = container.find_all('div')
    # for d in div:
    #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #     print(d)
    #     print('**********************************************')
    #     print(d.text)
    #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    ####################################################################
    ####################################################################
    ####################################################################

    # counter = 0
    # div = image.find_all('div')
    # for text_review in image.find_all('div', {'class': 'reviewText'}):
    #     counter = counter+1
    #     review_text = text_review.span.text
    #     print(review_text)
    #     print(counter)
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # counter = 0
    # for title_review in image.find_all('a', {'class': 'review-title'}):
    #     counter = counter+1
    #     review_title = title_review.span.text
    #     print(review_title)
    #     print(counter)
        
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # # for star_review in image.find_all('span', {'class': 'a-icon-alt'}):
    # counter = 0
    # for star_review in image.find_all('i', {'class': 'review-rating'}):
    #     counter = counter+1
    #     review_star = star_review.span.text
    #     print(review_star)
    #     print(counter)

    #Get see all review link
    print()
    print('***************************************************')
    print()
    review_link = image.find('a', {'data-hook' : 'see-all-reviews-link-foot'})['href']
    see_all_review_url = get_start_url + review_link
    print(see_all_review_url)
    get_all_reviews(see_all_review_url)
open_amazon_url(url)
