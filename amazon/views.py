from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import LinkForm, NumberOfLink, ChooseAlgorithm, GetAllLink

from comment_analyser.ws_amazon import AmazonReviewScraper
from comment_analyser.ws_flipkart import FlipkartReviewScraper
from comment_analyser.product_details import ProductDetails

# Create your views here.


number_of_links = 1
select_algorithm = ''
get_links = []
website_name = ''

def homepage(request):
    return render(request, 'amazon/homepage.html')

@login_required
def get_amazon_review(request):
    reviews = ProductDetails.product_details
    print(reviews)
    content = {
        'reviews' : reviews
    }
    return render(request, 'amazon/get_amazon_review.html', content)

@login_required
def get_link_number(request):
    ProductDetails.product_details = []
    if request.method == 'POST':
        number_form = NumberOfLink(request.POST)
        print(number_form['number'].data)
        global number_of_links
        number_of_links = int(number_form['number'].data)

        return redirect('get-amazon-link')

    else:
        number_form = NumberOfLink

    content = {
        'number_form': number_form,
    }

    return render(request, 'amazon/get_link_number.html', content)

@login_required
def get_amazon_link(request):
    ProductDetails.product_details = []
    if request.method == 'POST':
        link_form = LinkForm(request.POST)
        get_all_links = GetAllLink(request.POST)
        links = get_all_links['get_all_links'].data
        link = links.split(",")
        print(link)
        global get_links
        get_links = link

        return redirect('get-algorithm')

    else:
        link_form = LinkForm
        get_all_links = GetAllLink

    global number_of_links
    link_number = []
    for i in range(0, number_of_links):
        link_number.append(i)

    content = {
        'number_of_links': link_number,
        'link_form': link_form,
        'get_all_links': get_all_links,
    }

    return render(request, 'amazon/get_amazon_link.html', content)

def get_algorithm(request):
    ProductDetails.product_details = []
    if request.method == 'POST':
        choose_algorithm = ChooseAlgorithm(request.POST)
        print(choose_algorithm['algorithm'].data)

        global select_algorithm
        select_algorithm = choose_algorithm['algorithm'].data

        choose_web_scraper(number_of_links, get_links, select_algorithm)

        return redirect('get-amazon-review')

    else:
        choose_algorithm = ChooseAlgorithm

    content = {
        'choose_agorithm': choose_algorithm,
    }


    return render(request, 'amazon/get_algorithm.html', content)

def factory_method_design(obj=''):
    objs = dict(
        amazon = AmazonReviewScraper(),
        flipkart = FlipkartReviewScraper()
    )
    return objs[obj]

def choose_web_scraper(number_of_links, links, choose_agorithm):
    for number in range(0, number_of_links):
        url = links[number]
        link = links[number]
        link = link.split('/')
        link = link[2]
        website = link.split('.')
        global website_name
        website_name = website[1]
        print(website_name)
        choose_class = factory_method_design(website_name)
        print('!!!!!!!!!!!!!!!!!!!')
        choose_class.main_function(number_of_links, url, choose_agorithm)