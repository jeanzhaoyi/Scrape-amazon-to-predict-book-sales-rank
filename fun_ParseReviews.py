import requests  
from lxml import html
import json
import re 
from itertools import compress
import os
from time import sleep

def download(URL):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(URL,headers = headers) # this is the review page, not the product page
    print("Downloading and processing: " + URL + "\n")
    sleep(5)
    return page


def ParseReviews(review_url):
    review_url = review_url + "&sortBy=recent" # change it to sort by dates
# the URL is a string starting with "/gp/...." that is a product from parsing a booklist
    page = download("https://www.amazon.com"+ review_url + "&pageNumber=1") # this is the review page, not the product page

    ASIN = review_url[20:30]

    product_url = "https://www.amazon.com/dp/product/" + ASIN
    product_site = download(product_url) 

    parser = html.fromstring(page.text) # full review
    tree = html.fromstring(product_site.content) # product page

    # publishing date
    XPATH_CONTENT = '//div[@class="content"]/div'

    book_info = tree.xpath(XPATH_CONTENT)

    publish_date = ''
    publisher = ''
    for cont in book_info:
        t_cont = cont.xpath('//li//text()')
        for x in t_cont: #./div//div//i//text()
            temp_search = re.findall(r'\w+ \d+, \d{4}', x)
            if(len(temp_search)==1): # length represents the number of strings found that matches this pattern
                publish_date = temp_search
                publisher = re.split(r'[;\(]',x)[0]

    # Sales Ranking
    XPATH_RANK = '//li[@id="SalesRank"]/text()'
    rank_contained = tree.xpath(XPATH_RANK)
    
    sales_rank = int(re.findall(r'\d+', rank_contained[1])[0]) 

    # Book name
    XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
    raw_product_name = tree.xpath(XPATH_PRODUCT_NAME)
    product_name = ''.join(raw_product_name).strip()

    # Number of reviews
    xpath_numberReviews = '//span[@class="a-size-base"][@id="acrCustomerReviewText"]//text()' 
    raw_n_reviews = tree.xpath(xpath_numberReviews)
    n_reviews = int(re.findall(r'\d+', raw_n_reviews[0])[0])

    # Average book rating from all reviews
    xpath_rating = '//a//i[@class="a-icon a-icon-star a-star-4-5"]//span[@class="a-icon-alt"]//text()'
    raw_rating = tree.xpath(xpath_rating)[0]
    agg_rating = float(re.findall(r'[^ab-z]+ ', raw_rating)[0])

    # rating dictionary of all review breakup percentages
    XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
    total_ratings  = tree.xpath(XPATH_AGGREGATE_RATING)

    ratings_dict = {}

    #grabing the rating  section in product page
    for ratings in total_ratings:
        extracted_rating = ratings.xpath('./td//a//text()')
        if extracted_rating:
            rating_key = extracted_rating[0] 
            raw_raing_value = extracted_rating[1]
            rating_value = raw_raing_value
            if rating_key:
                ratings_dict.update({rating_key:rating_value})

    # find the maximum page number for all the reviews
    t_review_links = parser.xpath('//a/@href')
    index_link = list(map(lambda x: re.search(r'pageNumber=', x)!=None, t_review_links )) #

    page_links = list(compress(t_review_links, index_link))
    page_N = int(re.findall(r'\d+',page_links[-2])[-1]) # number for the total pages

    #page_N = int(re.findall(r'\d+$',page_links[-2])[0]) # number for the total pages
    page_N = min(500, page_N) # reduce the maximum number of pages

    # first parse the first page, or full review page 1
    XPATH_REVIEW_TEXT = '//span[@class="a-size-base review-text"][contains(@data-hook,"review-body")]//text()'
    reviews_temp = parser.xpath(XPATH_REVIEW_TEXT)

    # also parse the review header in the first page
    XPATH_REVIEW_HEADER = '//a[@data-hook="review-title"]//text()'
    reviews_title = parser.xpath(XPATH_REVIEW_HEADER)

    # then add the rest of the review pages
    for page_n in range(2,page_N +1,1): # USE PAGE_N found above
        temp_url = 'https://www.amazon.com' + review_url +'&pageNumber='+str(page_n)
        temp_page = download(temp_url)
        temp_parser = html.fromstring(temp_page.text)
        reviews_temp += temp_parser.xpath(XPATH_REVIEW_TEXT)
        reviews_title += temp_parser.xpath(XPATH_REVIEW_HEADER)

    data = {
                'url':product_url,
                'name':product_name,
                'ASIN': ASIN,
                'publisher': publisher,
                'publish_date':publish_date,
                'sales_rank':sales_rank,
                'number_reviews': n_reviews,
                'average_rating': agg_rating,        
                'rating_perc':ratings_dict,
                'reviews':reviews_temp,
                'review_titles': reviews_title
            }
    return data