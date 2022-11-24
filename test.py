from bs4 import BeautifulSoup
import requests
import openpyxl
from openpyxl.workbook import Workbook
from lxml import etree
from time import sleep
import pandas as pd
import datetime

def scrapeReviews(url):
    df= pd.DataFrame(columns=["movie",'user',"rate","title","review","url"])
    # url = "https://www.imdb.com/title/tt9114286/reviews?spoiler=hide&sort=userRating&dir=desc&ratingFilter=0"
    path= ""
    while True:        
        source = requests.get(url)
        source.raise_for_status()
        soup = BeautifulSoup(source.text, 'html.parser')
        dom = etree.HTML(str(soup))
        if path =="": 
            path= dom.xpath('//div[@class="load-more-data"]/@data-ajaxurl')[0]
            movieName=dom.xpath('//h3[@itemprop="name"]/a/text()')[0]

        user = dom.xpath('//span[@class="display-name-link"]/a/text()')
        reviewRate = dom.xpath('//span[@class="point-scale"]/preceding-sibling::span/text()')
        reviewTitle = dom.xpath('//a[@class="title"]/text()') 
        reviewContent = [revC.text for revC in dom.xpath('//div[contains(@class,"text show-more__control")]')]
        reviewLink= dom.xpath('//a[@class="title"]/@href')

        try:
            paginationKey = dom.xpath('//div[@class="load-more-data"]/@data-key')[0]
        except IndexError:
            print(url)
            break
        print(user,url,"\n")
        url= f"https://www.imdb.com{path}&paginationKey={paginationKey}"  
        dff = pd.DataFrame({
            "movie":movieName,
            'user':user,
            "rate":reviewRate,
            "title":reviewTitle,
            "review":reviewContent,
            "url":[f"https://www.imdb.com{x}" for x in  reviewLink]
        })
        df= pd.concat([df,dff], ignore_index=True,sort=False)
    return df
# dfReviews = scrapeReviews("https://www.imdb.com/title/tt9114286/reviews?spoiler=hide&sort=userRating&dir=desc&ratingFilter=0")
# dfReviews.to_csv("waw.csv",index=False)
def getTime():
    return datetime.datetime.now().strftime("%H:%M:%S")

scrapedMovieNames= pd.read_csv("movieDetails.csv")["Name"].tolist()
print(getTime(),scrapedMovieNames )
















def scrapeMovies(url):    
    source = requests.get(url)
    source.raise_for_status()
    soup = BeautifulSoup(source.text, 'html.parser')
    dom = etree.HTML(str(soup))

    movieTitle = dom.xpath('//h3[@class="lister-item-header"]/a/text()')
    year    = [etree.tostring(y) for y in  dom.xpath('//h3[@class="lister-item-header"]/span[last()]')]
    # year    = [x.text[-5:-1] for x in  dom.xpath('//h3[@class="lister-item-header"]/span[last()]')]
    rating  = dom.xpath('//*[@class="inline-block ratings-imdb-rating"]/strong/text()')
    
    tree= [etree.parse(y).xpath("/text()") for y in year]
    print(tree)
    # metascore =""
    runtime =""
    genre   =""
    votes   =""

    return
# dfMovies = scrapeMovies("https://www.imdb.com/search/title/?title_type=feature&user_rating=1.0,10.0&genres=sci-fi&count=250")
# dfMovies
