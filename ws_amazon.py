import requests
import csv
import pandas as pd

from models import Review
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Review class


class AmazonReviewScraper:

    # Empty review list
    reviews_list = []
    count = 0

    def get_url(url):
        # Get url ( like :- amazon.in / amazon.com)
        new_url = url.split('/')
        get_start_url = new_url[0] + '//' + new_url[2]
        return str(get_start_url)

    # Getting all the specific product reviews
    def get_all_reviews(show_all_reviews, csv_writer):

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(options=options)
        driver.get(show_all_reviews)
        res = driver.execute_script(
            "return document.documentElement.outerHTML")
        driver.quit()

        soup = BeautifulSoup(res, 'lxml')
        for reviews in soup.find_all('div', {'data-hook': 'review'}):
            rating = reviews.find('i', {'data-hook': 'review-star-rating'})
            rating_text = rating.span.text
            title = reviews.find('a', {'data-hook': 'review-title'})
            title_text = title.span.text
            body = reviews.find('span', {'data-hook': 'review-body'})
            body_text = body.span.text

            # Creating instance of class Review
            review = Review(title_text, body_text, rating_text)

            # Pushing the instance in review list
            AmazonReviewScraper.reviews_list.append(
                {'title': review.title, 'body': review.body, 'rating': review.rating})

            # Printing the console statement

            csv_writer.writerow([title_text, body_text, rating_text])

        #Pagination in reviews
        try:
            # Check for  the next page
            pagination = soup.find('div', {'id': 'cm_cr-pagination_bar'})
            next_page = pagination.find('li', {'class': 'a-last'})
            get_to_next_page = next_page.a['href']
            get_full_url = AmazonReviewScraper.get_url(url) + get_to_next_page
            print(get_full_url)
            # count = Review.count
            AmazonReviewScraper.count = AmazonReviewScraper.count+1
            print(
                f'\n Fetcing all the reviews from Page No :-{AmazonReviewScraper.count} \n')

            # if count != 5:
            AmazonReviewScraper.get_all_reviews(get_full_url, csv_writer)

        except Exception as e:
            pass

    def open_amazon_url(url):

        driver = webdriver.Chrome()
        driver.get(url)
        res = driver.execute_script(
            "return document.documentElement.outerHTML")
        driver.quit()

        soup = BeautifulSoup(res, 'lxml')
        image = soup.find('div', {'id': 'dp'})
        container = image.find('div', {'class': 'a-container'})

        # Get see all review link
        review_link = image.find(
            'a', {'data-hook': 'see-all-reviews-link-foot'})['href']
        see_all_review_url = AmazonReviewScraper.get_url(url) + review_link

        # Printing the url
        print(see_all_review_url)

        # Opening the CSV file
        csv_file = open('reviews.csv', 'w')
        read_csv_file = open('reviews.csv', 'r')
        csv_writer = csv.writer(csv_file)
        reader = csv.reader(read_csv_file)
        csv_writer.writerow(['Title', 'Data', 'Rating'])

        # Calling the show all review function
        AmazonReviewScraper.get_all_reviews(see_all_review_url, csv_writer)

        csv_file.close()

    def __str__(self):
        review = f'{self.title} \n {self.body} \n {self.rating}'
        return review

    def __repr__(self):
        review = f'{self.title} \n {self.body} \n {self.rating}'
        return review


# url = 'https://www.amazon.in/PTron-HBE6-Headphone-Earphone-Headset/dp/B07D4CN9T7/ref=sr_1_1_sspa?crid=35QWQDH0ATDLW&dchild=1&keywords=earphones+under+200&qid=1599149099&sprefix=earpho%2Caps%2C313&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFSVVhETVFIM0xCTjkmZW5jcnlwdGVkSWQ9QTA0NjExNDcyRDBGQ1REQjBFS0RUJmVuY3J5cHRlZEFkSWQ9QTA0MzI2MjMzRlNEQzYxVENMSkNFJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='
# Input URL
url = input("Enter URL here : ")

get_all_reviews = AmazonReviewScraper.open_amazon_url(url)
# open_amazon_url(url)
print('-----------------------------------------------------------------------------')
print(f'\n\n\n{AmazonReviewScraper.reviews_list}\n\n\n')
print('All reviews are fetched Sucessfully')
