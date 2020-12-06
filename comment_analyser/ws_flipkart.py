import csv

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from .models import Review
from .machine_learning import ReviewSentimentalAnalyser
from .product_details import ProductDetails

class FlipkartReviewScraper:
    url = ''
    get_new_url = ''
    count = 0
    reviews_list = []
    product_details = []

    def get_url(self, url):
        # print(url)
        self.url = url
        new_url = url.split('/')
        self.get_new_url = new_url[0] + '//' + new_url[2]
        print(self.get_new_url)
        pass

    def get_all_reviews(self, reviews, csv_writer):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(options=options)
        driver.get(reviews)
        res = driver.execute_script(
            "return document.documentElement.outerHTML")
        driver.quit()

        soup = BeautifulSoup(res, 'lxml')
        for reviews in soup.find_all('div', {'class': '_1AtVbE'}):
            try:
                title = reviews.find('p', {'class', '_2-N8zT'}).text
                try:
                    body = reviews.find('div', {'class', 't-ZTKy'}).text
                    try:
                        rating = reviews.find('div', {'class', '_3LWZlK'}).text
                        review = Review(title, body, rating)
                        self.reviews_list.append({'title': review.title, 'body': review.body, 'rating': review.rating})

                        self.reviews_list.append(review)

                        self.reviews_list.append(review)

                        csv_writer.writerow([title, body, rating])
                    except Exception:
                        print('Not Found')
                        pass
                except Exception:
                    pass
                pass
            except Exception:
                try:
                    title = reviews.find('div', {'class', 't-ZTKy'}).find('div', {'class': '_6K-7Co'}).text
                    body = ''
                    rating = reviews.find('div', {'class', 't-ZTKy'}).find('div', {'class': '_3LWZlK'}).text
                    review = Review(title, body, rating)
                    self.reviews_list.append({'title': review.title, 'body': review.body, 'rating': review.rating})

                    self.reviews_list.append(review)

                    self.reviews_list.append(review)

                    csv_writer.writerow([title, body, rating])
                except Exception:
                    pass

        if self.count <= 3:
            try:
                self.count += 1
                print(
                    f'\n Fetching all the reviews from Page No :-{self.count} \n')
                next_page = soup.find('nav', {'class': 'yFHi8N'}).find(
                    'a', {'class': '_1LKTO3'})['href']
                next_page_span = soup.find('nav', {'class': 'yFHi8N'}).find('a', {'class': '_1LKTO3'}).span.text

                if next_page_span == 'Next':
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    print()
                    print(f'Pagination :- {next_page}')
                    get_full_url = self.get_new_url + next_page

                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    print(get_full_url)
                    print()

                    self.get_all_reviews(get_full_url, csv_writer)
                else:
                    return

            except Exception:
                pass
        else:
            print('Count :- ', self.count)

    def open_flipkart_url(self, url, choose):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome()
        driver.get(url)
        res = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()

        soup = BeautifulSoup(res, 'lxml')

        flipkart = soup.find('div', {'id': 'container'})

        product_title = flipkart.find('span', {'class': 'B_NuCI'}).text

        find_image = flipkart.find('div', {'class': '_3kidJX'})
        product_image = find_image.find_all('img')[0]['src']

        product_rating = flipkart.find('div', {'class': '_3LWZlK'}).text

        find_reviews = flipkart.find('div', {'class': 'JOpGWq'})
        get_all_reviews_link = find_reviews.find_all('a')
        reviews = find_reviews.find_all('a')[len(get_all_reviews_link)-1]['href']

        print(product_title)
        print(product_image)
        print(product_rating)
        reviews = self.get_new_url + reviews
        print(reviews)

        file_name = product_title+'.csv'
        csv_file = open(file_name, 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Title', 'Data', 'Rating'])

        self.get_all_reviews(reviews, csv_writer)
        csv_file.close()

        print('-----------------------------------------------------------------------------')
        print('All reviews are fetched Sucessfully')
        print(self.reviews_list)

        review_sentiment_analyser = ReviewSentimentalAnalyser()
        ReviewSentimentalAnalyser.filename = file_name
        rating = review_sentiment_analyser.import_csvfile(choose)

        percision = review_sentiment_analyser.percision
        recall = review_sentiment_analyser.recall
        f1_score = review_sentiment_analyser.f1_score

        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('-------------------------------------------------------')
        machine_learning_rating = review_sentiment_analyser.product_average_rating
        print(review_sentiment_analyser.product_average_rating)
        print(percision, recall, f1_score)

        self.get_title_image_rating(product_title, product_image, product_rating, machine_learning_rating, percision, recall, f1_score)

    def get_title_image_rating(self, title, image, rating, machine_learning_rating, percision, recall, f1_score):
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
        details['original_rating'] = str(rating) +  ' out of 5 starts'
        details['machine_learning_rating'] = ml_rating
        details['percision'] = percision
        details['recall'] = recall
        details['f1_score'] = f1_score
        details['webpage'] = 'Flipkart'

        self.product_details.append(details)
        print(self.product_details)
        product_details = ProductDetails()
        product_details.get_product_details(details)

    def main_function(self, number_of_links, url, choose_algorithm):
        print('abncdasdbasfadsfhds')
        print(number_of_links, url, choose_algorithm)
        print(url)
        self.get_url(url)
        self.open_flipkart_url(url, choose_algorithm)