import requests
import csv
import pandas as pd
import pprint

from .models import Review
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from .machine_learning import ReviewSentimentalAnalyser
from .product_details import ProductDetails
# from average_rating import AverageRating


class AmazonReviewScraper:

    # Empty review list
    reviews_list = []
    count = 0
    average_rating_list = []
    product_details = []
    new_url = ''

    def get_url(self, url):
        # Get url ( like :- amazon.in / amazon.com)
        new_url = url.split('/')
        get_start_url = new_url[0] + '//' + new_url[2]
        print(url)
        print(get_start_url)
        self.new_url = get_start_url
        return str(get_start_url)

    # Getting all the specific product reviews
    def get_all_reviews(self, show_all_reviews, csv_writer):

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(show_all_reviews)
        res = driver.execute_script("return document.documentElement.outerHTML")
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
            self.reviews_list.append(
                {'title': review.title, 'body': review.body, 'rating': review.rating}
            )

            self.reviews_list.append(review)

            # Printing the console statement
            csv_writer.writerow([title_text, body_text, rating_text])

        #Pagination in reviews
        if self.count <= 99:
            try:
                self.count = self.count+1
                print(f'\n Fetching all the reviews from Page No :-{self.count} \n')
                # Check for  the next page
                pagination = soup.find('div', {'id': 'cm_cr-pagination_bar'})
                next_page = pagination.find('li', {'class': 'a-last'})
                get_to_next_page = next_page.a['href']
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print()
                print(f'Pagination :- {get_to_next_page}')
                # get_full_url = self.get_url(url) + get_to_next_page
                get_full_url = self.new_url + get_to_next_page

                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print(get_full_url)
                print()
                # count = Review.count

                # if count != 5:
                self.get_all_reviews(get_full_url, csv_writer)

            except Exception as e:
                pass
        else :
            print()

    def open_amazon_url(self, url, choose):

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome()
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        res = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()

        soup = BeautifulSoup(res, 'lxml')


        image = soup.find('div', {'id': 'dp'})
        # print("Image")

        product_title = image.find('div', {'id': 'dp-container'}).find('div', {'id': 'centerCol'}).find('span', {'id': 'productTitle'}).text
        # print(product_title)
        product_image = image.find('div', {'id': 'dp-container'}).find('div', {'id': 'leftCol'}).find('div', {'id': 'imageBlock'}).find('div', {'id': 'main-image-container'}).find_all('img')[0]['src']
        # print(product_image)
        product_rating = image.find('div', {'id': 'dp-container'}).find('div', {'id': 'centerCol'}).find('div', {'id': 'averageCustomerReviews_feature_div'}).find('div', {'id': 'averageCustomerReviews'}).find('span', {'id': 'acrPopover'})['title']
        # print("Rating")
        container = image.find('div', {'class': 'a-container'})
        # print("Container")
        # Get see all review link
        review_link = image.find('a', {'data-hook': 'see-all-reviews-link-foot'})['href']
        see_all_review_url = self.get_url(url) + review_link

        # Printing the url
        print(see_all_review_url)
        
        # Opening the CSV file
        
        file_name = product_title + '.csv'
        csv_file = open(file_name, 'w')
        read_csv_file = open(file_name, 'r')
        csv_writer = csv.writer(csv_file)
        reader = csv.reader(read_csv_file)
        csv_writer.writerow(['Title', 'Data', 'Rating'])

        # Calling the show all review function
        self.get_all_reviews(see_all_review_url, csv_writer)
        csv_file.close()

        print('-----------------------------------------------------------------------------')
        print('All reviews are fetched Sucessfully')
        pprint.pprint(self.reviews_list)

        review_sentiment_analyser = ReviewSentimentalAnalyser()

        ReviewSentimentalAnalyser.filename = file_name
        rating = review_sentiment_analyser.import_csvfile(choose)
        # self.average_rating_list.append(review_sentiment_analyser.product_average_rating)

        percision = review_sentiment_analyser.percision
        recall = review_sentiment_analyser.recall
        f1_score = review_sentiment_analyser.f1_score
        true_positive = review_sentiment_analyser.true_positive
        true_negative = review_sentiment_analyser.true_negative
        false_positive = review_sentiment_analyser.false_positive
        false_negative = review_sentiment_analyser.false_negative

        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('-------------------------------------------------------')
        machine_learning_rating = review_sentiment_analyser.product_average_rating
        print(review_sentiment_analyser.product_average_rating)
        print(percision, recall, f1_score)

        self.get_title_image_rating(product_title, product_image, product_rating, machine_learning_rating, percision, recall, f1_score, true_positive, true_negative ,false_positive ,false_negative)

    def __str__(self):
        review = f'{self.title} \n {self.body} \n {self.rating}'
        return review

    def __repr__(self):
        review = f'{self.title} \n {self.body} \n {self.rating}'
        return review

    def get_title_image_rating(self, title, image, rating, machine_learning_rating, percision, recall, f1_score, true_positive, true_negative, false_positive ,false_negative):
        details = {}
        roundof = round(machine_learning_rating, 1)
        ml_rating = str(roundof) + ' out of 5 starts'
        title = title.split('\n')
        for get_title in title:
            if get_title != '':
                title = get_title
                break

        details['title'] = title
        details['image'] = image
        details['original_rating'] = rating
        details['machine_learning_rating'] = ml_rating
        details['percision'] = percision
        details['recall'] = recall
        details['f1_score'] = f1_score
        details['true_positive'] = true_positive        
        details['true_negative'] = true_negative
        details['false_positive'] = false_positive
        details['false_negative'] = false_negative        
        details['webpage'] = 'Amazon'

        self.product_details.append(details)
        product_details = ProductDetails()
        product_details.get_product_details(details)
    


    def main_function(self, number_of_links, url, choose_algorithm):
        print('abncdasdbasfadsfhds')
        print(number_of_links, url, choose_algorithm)
        print(url)
        self.get_url(url)
        self.open_amazon_url(url, choose_algorithm)
        print('AMAZON')
