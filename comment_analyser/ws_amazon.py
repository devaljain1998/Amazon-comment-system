import requests
import csv
import pandas as pd
import pprint

from .models import Review
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .machine_learning import ReviewSentimentalAnalyser
# from average_rating import AverageRating

# Review class

file_count = -1


class AmazonReviewScraper:

    # Empty review list
    reviews_list = []
    count = 0
    average_rating_list = []
    product_details = []
    new_url = ''

    def get_url(url):
        # Get url ( like :- amazon.in / amazon.com)
        new_url = url.split('/')
        get_start_url = new_url[0] + '//' + new_url[2]
        print(url)
        print(get_start_url)
        AmazonReviewScraper.new_url = get_start_url
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
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print()
                print(f'Pagination :- {get_to_next_page}')
                # get_full_url = AmazonReviewScraper.get_url(url) + get_to_next_page
                get_full_url = AmazonReviewScraper.new_url + get_to_next_page

                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print(get_full_url)
                print()
                # count = Review.count

                # if count != 5:
                AmazonReviewScraper.get_all_reviews(get_full_url, csv_writer)

            except Exception as e:
                pass
        else :
            print()

    def open_amazon_url(url, choose):

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome()
        driver.get(url)
        res = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()

        soup = BeautifulSoup(res, 'lxml')


        image = soup.find('div', {'id': 'dp'})

        product_title = soup.find('div', {'id': 'title_feature_div'}).find('div', {'id': 'titleSection'}).find('h1', {'id': 'title'}).find('span', {'id': 'productTitle'}).text
        product_image = image.find('div', {'id': 'dp-container'}).find('div', {'id': 'leftCol'}).find('div', {'id': 'imageBlock'}).find('img', {'id': 'landingImage'})['src']
        product_rating = image.find('div', {'id': 'dp-container'}).find('div', {'id': 'centerCol'}).find('div', {'id': 'averageCustomerReviews_feature_div'}).find('div', {'id': 'averageCustomerReviews'}).find('span', {'id': 'acrPopover'})['title']
        
        container = image.find('div', {'class': 'a-container'})

        # Get see all review link
        review_link = image.find('a', {'data-hook': 'see-all-reviews-link-foot'})['href']
        see_all_review_url = AmazonReviewScraper.get_url(url) + review_link

        # Printing the url
        print(see_all_review_url)
        
        # Opening the CSV file
        global file_count
        file_count = file_count+1
        str_n = str(file_count)
        file_name = 'reviews_' + str_n + '.csv'
        csv_file = open(file_name, 'w')
        read_csv_file = open(file_name, 'r')
        csv_writer = csv.writer(csv_file)
        reader = csv.reader(read_csv_file)
        csv_writer.writerow(['Title', 'Data', 'Rating'])

        # Calling the show all review function
        AmazonReviewScraper.get_all_reviews(see_all_review_url, csv_writer)
        csv_file.close()

        print('-----------------------------------------------------------------------------')
        print('All reviews are fetched Sucessfully')
        pprint.pprint(AmazonReviewScraper.reviews_list)
        ReviewSentimentalAnalyser.filename = file_name
        ReviewSentimentalAnalyser.import_csvfile(choose)
        # AmazonReviewScraper.average_rating_list.append(ReviewSentimentalAnalyser.product_average_rating)
        machine_learning_rating = ReviewSentimentalAnalyser.product_average_rating
        # print(f'Machine Learning Average Rating :- {ReviewSentimentalAnalyser.product_average_rating}')
        AmazonReviewScraper.get_title_image_rating(product_title, product_image, product_rating, machine_learning_rating)

    def __str__(self):
        review = f'{self.title} \n {self.body} \n {self.rating}'
        return review

    def __repr__(self):
        review = f'{self.title} \n {self.body} \n {self.rating}'
        return review

    def get_title_image_rating(title, image, rating, machine_learning_rating):
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
        details['amazon_rating'] = rating
        details['machine_learning_rating'] = ml_rating
        AmazonReviewScraper.product_details.append(details)
    


    def main_function(number_of_links, links, choose_algorithm):
        n = number_of_links
        my_list = links
        choose = choose_algorithm
        for url in my_list:
            AmazonReviewScraper.count = 0
            print('-------------------------------------------------------------------------------')
            print(url)
            AmazonReviewScraper.get_url(url)
            print('-------------------------------------------------------------------------------')
            AmazonReviewScraper.open_amazon_url(url, choose)

        print(AmazonReviewScraper.product_details)
