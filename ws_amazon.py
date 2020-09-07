import requests
import csv
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver

# class Review():
#     def __init__(self, title, body, rating):
#     str, repr 

# class Review:
#     pass



# reviews = []


# url = 'https://www.amazon.in/PTron-HBE6-Headphone-Earphone-Headset/dp/B07D4CN9T7/ref=sr_1_1_sspa?crid=35QWQDH0ATDLW&dchild=1&keywords=earphones+under+200&qid=1599149099&sprefix=earpho%2Caps%2C313&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFSVVhETVFIM0xCTjkmZW5jcnlwdGVkSWQ9QTA0NjExNDcyRDBGQ1REQjBFS0RUJmVuY3J5cHRlZEFkSWQ9QTA0MzI2MjMzRlNEQzYxVENMSkNFJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='

url = input("Enter URL here : ")

#Get url (amazon.in / amazon.com)
new_url = url.split('/')
get_start_url = new_url[0]  +'//'+ new_url[2]
count = 0
def get_all_reviews(show_all_reviews, csv_writer):
    driver = webdriver.Chrome()
    driver.get(show_all_reviews)
    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    soup = BeautifulSoup(res, 'lxml')
    for reviews in soup.find_all('div', {'data-hook' : 'review'}):
        rating = reviews.find('i', {'data-hook': 'review-star-rating'})
        rating_text = rating.span.text
        title = reviews.find('a', {'data-hook': 'review-title'})
        title_text = title.span.text
        body = reviews.find('span', {'data-hook': 'review-body'})
        body_text = body.span.text
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # print(rating_text)
        # print()
        # print(title_text)
        # print()
        # print(body_text)
        # print()
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        csv_writer.writerow([title_text,body_text,rating_text])


    #Check for  the next page
    pagination = soup.find('div', {'id' : 'cm_cr-pagination_bar'})
    next_page = pagination.find('li', {'class': 'a-last'})
    get_to_next_page = next_page.a['href']
    get_full_url = get_start_url + get_to_next_page
    print(get_full_url)
    global count
    count = count+1
    print(count)
    if count != 5:
        if get_to_next_page != None:
            get_all_reviews(get_full_url, csv_writer)
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

    #Opening the CSV file
    csv_file = open('reviews.csv', 'w')
    read_csv_file = open('reviews.csv', 'r')
    csv_writer = csv.writer(csv_file)
    reader = csv.reader(read_csv_file)
    csv_writer.writerow(['Title', 'Data', 'Rating'])

    #Calling the show all review function
    get_all_reviews(see_all_review_url, csv_writer)

    csv_file.close()

open_amazon_url(url)
