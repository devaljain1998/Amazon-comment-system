import requests

from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://www.amazon.in/Apple-iPhone-11-128GB-Black/dp/B07XVLW7YK/ref=sr_1_1_sspa?crid=RMOIQXKSR9M4&dchild=1&keywords=smartphone&qid=1598170586&sprefix=smartphone%2Caps%2C-1&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExSEU5STlaVEtLQ09SJmVuY3J5cHRlZElkPUEwMjE1NzU3MlE1MzdLVk8wQlNJRiZlbmNyeXB0ZWRBZElkPUEwOTQyNzg3MjVHVjlJM0w0VlFVRyZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU='

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
#     print(d.text)
#     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
# div = image.find_all('div', {'class': 'reviewText'})
# print(div.text)
div = image.find_all('div')

# class->reviewText  class->review-rating class->a-profile-content  data-hook->see-all-reviews-link-foot class->review-title-content
for text_review in image.find_all('div', {'class': 'reviewText'}):
    review_text = text_review.span.text
    print(review_text)
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

for title_review in image.find_all('a', {'class': 'review-title'}):
    review_title = title_review.span.text
    print(review_title)
    
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
for star_review in image.find_all('i', {'class': 'a-icon-star'}):
    review_star = star_review.span.text
    print(review_star)
# for d in div:
#     print(d)
#     print('*********************************************************')
#     print(d.text)
#     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')