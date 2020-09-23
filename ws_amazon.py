import requests
import csv
import pandas as pd
import pprint

from models import Review
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from machine_learning import MachineLearning

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
                {'title': review.title, 'body': review.body, 'rating': review.rating}
            )

            AmazonReviewScraper.reviews_list.append(review)

            # Printing the console statement
            csv_writer.writerow([title_text, body_text, rating_text])

        #Pagination in reviews
        if AmazonReviewScraper.count <= 99:
            try:
                AmazonReviewScraper.count = AmazonReviewScraper.count+1
                print(f'\n Fetching all the reviews from Page No :-{AmazonReviewScraper.count} \n')
                # Check for  the next page
                pagination = soup.find('div', {'id': 'cm_cr-pagination_bar'})
                next_page = pagination.find('li', {'class': 'a-last'})
                get_to_next_page = next_page.a['href']
                get_full_url = AmazonReviewScraper.get_url(url) + get_to_next_page
                print(get_full_url)
                # count = Review.count

                # if count != 5:
                AmazonReviewScraper.get_all_reviews(get_full_url, csv_writer)

            except Exception as e:
                pass
        else :
            print()

    def open_amazon_url(url):

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome()
        driver.get(url)
        res = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()

        soup = BeautifulSoup(res, 'lxml')
        image = soup.find('div', {'id': 'dp'})
        container = image.find('div', {'class': 'a-container'})

        # Get see all review link
        review_link = image.find('a', {'data-hook': 'see-all-reviews-link-foot'})['href']
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

        print('-----------------------------------------------------------------------------')
        print('All reviews are fetched Sucessfully')
        pprint.pprint(AmazonReviewScraper.reviews_list)
        MachineLearning.import_csvfile()


    def __str__(self):
        review = f'{self.title} \n {self.body} \n {self.rating}'
        return review

    def __repr__(self):
        review = f'{self.title} \n {self.body} \n {self.rating}'
        return review

# Input URL
n = int(input('Enter number of products want to compare : '))

my_list = [input('Enter URL here as input # %s  : ' % i) for i in range(n)]

print('-------------------------------------------------------------------------------')
print(my_list)
print('-------------------------------------------------------------------------------')

# url = input("Enter URL here : ")
for url in my_list:
    AmazonReviewScraper.count = 0
    print('-------------------------------------------------------------------------------')
    print(url)
    print('-------------------------------------------------------------------------------')
    AmazonReviewScraper.open_amazon_url(url)

# url = "https://www.amazon.in/Nursery-Rhymes-Vol-1/dp/B00LIV50BO/ref=pd_rhf_gw_p_img_1?_encoding=UTF8&psc=1&refRID=KM54MFCWWWQZKH2EBP49"

# url = input('Enter URL here : ')

# get_all_reviews = AmazonReviewScraper.open_amazon_url(url)