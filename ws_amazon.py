import requests

from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://www.amazon.in/PTron-HBE6-Headphone-Earphone-Headset/dp/B07D4CN9T7/ref=sr_1_1_sspa?crid=35QWQDH0ATDLW&dchild=1&keywords=earphones+under+200&qid=1599149099&sprefix=earpho%2Caps%2C313&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFSVVhETVFIM0xCTjkmZW5jcnlwdGVkSWQ9QTA0NjExNDcyRDBGQ1REQjBFS0RUJmVuY3J5cHRlZEFkSWQ9QTA0MzI2MjMzRlNEQzYxVENMSkNFJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='

# url = input("Enter URL here : ")

#Get url (amazon.in / amazon.com)
new_url = url.split('/')
get_start_url = new_url[0]  +'//'+ new_url[2]

def get_all_reviews(show_all_reviews):
    driver = webdriver.Chrome()
    driver.get(show_all_reviews)
    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    soup = BeautifulSoup(res, 'lxml')
    reviews = soup.find('div', {'class': 'reviews-content'})
    
    #Getting all the rating from the page
    for rating in reviews.find_all('i', {'data-hook': 'review-star-rating'}):
        rating_text = rating.span.text
        print(rating_text)

    #Getting all the review title from the page
    for title in reviews.find_all('a', {'data-hook': 'review-title'}):
        title_text = title.span.text
        print(title_text)

    counter = 0
    #Getting all the review data from the page
    for data in reviews.find_all('span', {'data-hook' : 'review-body'}):
        counter = counter+1
        data_text = data.span.text
        print(data_text)
        print(counter)

    #Check for  the next page
    pagination = soup.find('div', {'id' : 'cm_cr-pagination_bar'})
    next_page = pagination.find('li', {'class': 'a-last'})
    get_to_next_page = next_page.a['href']
    get_full_url = get_start_url + get_to_next_page
    print(get_full_url)
    if get_to_next_page != None:
        get_all_reviews(get_full_url)
    else:
        print()

def open_amazon_url(url):

    driver = webdriver.Chrome()
    driver.get(url)
    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    soup = BeautifulSoup(res, 'lxml')
    image = soup.find('div', {'id':'dp'})
    container = image.find('div', {'class':'a-container'})

    #Get see all review link
    review_link = image.find('a', {'data-hook' : 'see-all-reviews-link-foot'})['href']
    see_all_review_url = get_start_url + review_link

    #Printing the url
    print(see_all_review_url)

    #Calling the show all review function
    get_all_reviews(see_all_review_url)

open_amazon_url(url)
